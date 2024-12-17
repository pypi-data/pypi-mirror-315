import os
import uuid
import time
import json
import logging
import datetime
import platform
import binascii
import threading
from typing import Optional
from typing import Union
from typing import Dict
from typing import Any

from redis import Redis
import yaml
from zenutils.strutils import TEXT

__all__ = [
    "SimQ",
]
_logger = logging.getLogger(__name__)


class SimQ(object):
    """基于redis的消息队列。"""

    def __init__(
        self,
        db: Redis,
        prefix: str = "simq",
        ack_event_expire: int = 60 * 60 * 24,
        done_item_expire: int = 60 * 60 * 24 * 7,
        worker_status_expire: int = 60 * 5,
        running_timeout: int = 60 * 5,
        default_running_timeout_action: str = "recover",
        running_timeout_handler_policies: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        """基于redis的消息队列。

        构造参数:
            db(Redis): redis连接
            prefix(str): 数据前缀
            ack_event_expire(int): 消息已处理通知的保存时长
            done_item_expire(int): 已处理消息的保存时长
            worker_status_expire(int): 执行器状态过期时间
            running_timeout(int): 全局消息执行超时时长。默认为5分钟。
            default_running_timeout_action(str): 全局消息超时处理策略。默认为回收重试。
            running_timeout_handler_policies(Dict[str, Dict[str, Any]]): 按channel指定消息超时策略。例如：
                ```
                    {
                        "debug.ping": {
                            "running_timeout": 10,
                            "action": "drop"
                        },
                        "debug.echo": {
                            "running_timeout": 60,
                            "action": "recover"
                        }
                    }
                ```
        """
        self.db = db
        self.prefix = prefix
        self.ack_event_expire = ack_event_expire
        self.done_item_expire = done_item_expire
        self.worker_status_expire = worker_status_expire
        self.running_timeout = running_timeout
        self.default_running_timeout_action = default_running_timeout_action
        self.running_timeout_handler_policies = running_timeout_handler_policies or {}
        # 其他内部变量
        self.last_running_keys = {}

    def hset(self, key, data):
        mapping = {}
        for item, value in data.items():
            mapping[item] = yaml.safe_dump(value)
        self.db.hset(key, mapping=mapping)

    def hgetall(self, key):
        data = {}
        mapping = self.db.hgetall(key)
        for item, value in mapping.items():
            item = TEXT(item)
            data[item] = yaml.safe_load(value)
        return data

    def get_worker_key(self, worker):
        return f"{self.prefix}:worker:{worker}"

    def get_mq_key(self, channel):
        return f"{self.prefix}:mq:{channel}"

    def get_running_key(self, channel, running_id):
        return f"{self.prefix}:running:{channel}:{running_id}"

    def get_running_keys(self, channel=None):
        if channel:
            rkeys = [
                TEXT(x) for x in self.db.keys(f"{self.prefix}:running:{channel}:*")
            ]
        else:
            rkeys = [TEXT(x) for x in self.db.keys(f"{self.prefix}:running:*")]
        return set(rkeys)

    def get_id_from_running_key(self, rkey):
        ids = self.db.lrange(rkey, 0, -1)
        if ids:
            return TEXT(ids[0])
        else:
            return None

    def get_done_key(self, id):
        return f"{self.prefix}:done:{id}"

    def get_item_key(self, id):
        return f"{self.prefix}:item:{id}"

    def get_default_worker(self):
        node = platform.node()
        pid = os.getpid()
        return f"{node}:{pid}"

    def rpush(
        self,
        channel: str,
        data: Any,
        id: str = None,
    ) -> str:
        """在队首插入消息。

        参数:
            channel(str): 消息队列名称。
            data(str): 消息体。可以为任意可json序列化内容。
            id(str): 消息编号。默认为空，表示自动生成随机消息编号。

        返回值:
            str: 消息编号。
        """
        nowtime = time.time()
        id = id or str(uuid.uuid4())
        qkey = self.get_mq_key(channel=channel)
        ikey = self.get_item_key(id=id)
        msg = {
            "id": id,
            "channel": channel,
            "add_time": nowtime,
            "mod_time": nowtime,
            "status": "ready",
            "data": data,
        }
        self.hset(ikey, msg)
        self.db.rpush(qkey, id)
        return id

    def lpush(
        self,
        channel,
        data,
        id=None,
    ) -> str:
        """在队尾插入消息。

        参数:
            channel(str): 消息队列名称。
            data(str): 消息体。可以为任意可json序列化内容。
            id(str): 消息编号。默认为空，表示自动生成随机消息编号。

        返回值:
            str: 消息编号。
        """
        nowtime = time.time()
        id = id or str(uuid.uuid4())
        qkey = self.get_mq_key(channel=channel)
        ikey = self.get_item_key(id=id)
        msg = {
            "id": id,
            "channel": channel,
            "add_time": nowtime,
            "mod_time": nowtime,
            "status": "ready",
            "data": data,
        }
        self.hset(ikey, msg)
        self.db.lpush(qkey, id)
        return id

    def pop(
        self,
        channel: str,
        worker: Optional[str] = None,
        timeout: int = 5,
    ) -> Dict[str, Any]:
        """消息提取。

        参数:
            channel(str): 消息队列名称。
            worker(str): 消息执行器名称。默认为空，表示自动生成执行器名称：{node}.{pid}。
            timeout(int): 等待超时时长。默认为5秒。

        返回值:
            Dict[str, Any]: 消息详情。
        """
        nowtime = time.time()
        worker = worker or self.get_default_worker()
        running_id = str(uuid.uuid4())
        qkey = self.get_mq_key(channel=channel)
        rkey = self.get_running_key(channel=channel, running_id=running_id)
        id = self.db.brpoplpush(qkey, rkey, timeout=timeout)
        if id is None:
            return None
        id = TEXT(id)
        ikey = self.get_item_key(id=id)
        msg = self.hgetall(key=ikey)
        if not msg:
            return None
        # 处理被取消的消息
        if msg.get("cancel_flag", False):
            self.hset(
                ikey,
                {
                    "cancel_status": "canceled",
                    "canceled_time": nowtime,
                    "status": "canceled",
                    "mod_time": nowtime,
                    "done_time": nowtime,
                    "result": None,
                },
            )
            rkey = self.get_running_key(channel=channel, running_id=running_id)
            self.db.delete(rkey)
            dkey = self.get_done_key(id=msg["id"])
            self.db.lpush(dkey, msg["id"])
            self.db.expire(dkey, self.ack_event_expire)
            self.db.expire(ikey, self.done_item_expire)
            return None
        # 更新消息状态
        update_msg = {
            "running_id": running_id,
            "start_time": nowtime,
            "mod_time": nowtime,
            "status": "running",
            "worker": worker,
        }
        msg.update(update_msg)
        self.hset(ikey, update_msg)
        return msg

    def ack(
        self,
        id: str,
        result: Optional[Any] = None,
    ) -> bool:
        """消息确认。

        确认该消息已处理，同时提交消息处理结果。

        参数:
            id(str): 消息编号。
            result(any): 消息执行结果。

        返回值:
            bool: 消息是否成功确认。

        """
        nowtime = time.time()
        ikey = self.get_item_key(id=id)
        msg = self.hgetall(key=ikey)
        if not msg:
            return False
        update_msg = {
            "ack_time": nowtime,
            "mod_time": nowtime,
            "status": "done",
            "result": result,
        }
        self.hset(ikey, update_msg)
        channel = msg.get("channel", None)
        if channel:
            rkey = self.get_running_key(channel=channel, running_id=msg["running_id"])
            self.db.delete(rkey)
        dkey = self.get_done_key(id=id)
        self.db.lpush(dkey, id)
        self.db.expire(dkey, self.ack_event_expire)
        self.db.expire(ikey, self.done_item_expire)
        return True

    def drop(self, id: str):
        """消息丢弃。

        丢弃该消息。

        参数:
            id(str): 消息编号。

        返回值:
            bool: 消息是否成功丢弃。

        """
        nowtime = time.time()
        ikey = self.get_item_key(id=id)
        msg = self.hgetall(key=ikey)
        if not msg:
            return False
        update_msg = {
            "drop_time": nowtime,
            "done_time": nowtime,
            "mod_time": nowtime,
            "status": "drop",
            "result": None,
        }
        self.hset(ikey, update_msg)
        channel = msg.get("channel", None)
        if channel:
            rkey = self.get_running_key(channel=channel, running_id=msg["running_id"])
            self.db.delete(rkey)
        dkey = self.get_done_key(id=id)
        self.db.lpush(dkey, id)
        self.db.expire(dkey, self.ack_event_expire)
        self.db.expire(ikey, self.done_item_expire)
        return True

    def query(
        self,
        id: str,
        timeout: int = 0,
    ) -> Dict[str, Any]:
        """查询消息详情。

        参数:
            id(str): 消息编号。
            timeout(int): 等待n秒或消息被处理。默认为0，表示不等待。

        返回值:
            Dict[str, Any]: 消息详情。

        """
        ikey = self.get_item_key(id=id)
        if timeout == 0:
            msg = self.hgetall(ikey)
            if not msg:
                return None
            return msg
        else:
            dkey = self.get_done_key(id=id)
            self.db.brpop(dkey, timeout=timeout)
            msg = self.hgetall(ikey)
            if not msg:
                return None
            return msg

    def cancel(
        self,
        id: str,
    ) -> Union[bool, None]:
        """取消消息。

        取消消息时，只是将消息标记为取消。等消息被取出时，才会实际进行消息的取消操作。
        消息被成功取消时，消息不会被删除，另外还会生成消息完成通知队列。

        参数:
            id: 消息编号

        返回值:
            True: 消息体正常，并且消息未处理前取消，则取消成功。
            False: 消息体异常，或者消息已经处理完成，则取消失败。
            None，消息体正常，并且消息正在处理时，返回None值。后面，如果消息成功执行，则消息成功执行。如果消息被回退，则消息被取消。
        """
        nowtime = time.time()
        ikey = self.get_item_key(id=id)
        msg = self.hgetall(key=ikey)
        if not msg:
            return False
        update_msg = {
            "cancel_flag": True,
            "mod_time": nowtime,
        }
        if not "cancel_time" in msg:
            update_msg["cancel_time"] = nowtime
        if msg["status"] in ["done"]:
            return_flag = False
        elif msg["status"] in ["canceling", "canceled"]:
            return_flag = True
        elif msg["status"] in ["ready"]:
            update_msg["status"] = "canceling"
            return_flag = True
        else:
            return_flag = None
        self.hset(ikey, update_msg)
        return return_flag

    def ret(
        self,
        id: str,
        return_reason: Optional[str] = None,
    ) -> bool:
        """消息退回。

        消息被执行器获取后，由于执行器停止或异常，需要及时回退消息的，可以调用此方法。

        参数:
            id: 消息编号。

        返回值:
            bool: 是否成功退回。

        """
        nowtime = time.time()
        ikey = self.get_item_key(id=id)
        msg = self.hgetall(ikey)
        # 没有消息体，无法return
        if not msg:
            return False
        # 状态不为running，无法return
        if msg.get("status", "unknown") != "running":
            return False
        # 如果存在running状态变量，则删除
        channel = msg.get("channel", None)
        if not channel:
            return False
        running_id = msg.get("running_id", None)
        if not running_id:
            return False
        if "running_id" in msg:
            rkey = self.get_running_key(channel=channel, running_id=running_id)
            self.db.delete(rkey)
        # 更新消息状态
        update_msg = {
            "return_flag": True,
            "return_time": nowtime,
            "return_reason": return_reason,
            "mod_time": nowtime,
            "retry_count": msg.get("retry_count", 0) + 1,
        }
        # 如果已经标记为取消，退回时直接取消
        cancel_flag = msg.get("cancel_flag", False)
        if cancel_flag:
            update_msg["status"] = "canceled"
            dkey = self.get_done_key(id=id)
            self.db.lpush(dkey, id)
            self.db.expire(dkey, self.ack_event_expire)
            self.db.expire(ikey, self.done_item_expire)
        else:
            update_msg["status"] = "ready"
            update_msg["worker"] = None
        self.hset(ikey, update_msg)
        if not cancel_flag:
            qkey = self.get_mq_key(channel=channel)
            self.db.lpush(qkey, id)
        return True

    def update_worker_status(
        self,
        worker: Optional[str] = None,
        expire: int = 0,
    ) -> None:
        """更新执行器状态。

        参数:
            worker(str): 执行器名称。默认为{node}.{pid}。
            expire(int): 执行器状态过期时间。默认使用系统过期时间。系统默认过期时间为60秒。必须为整数，否则会出现异常。

        返回值:
            无

        """
        nowtime = time.time()
        expire = expire or self.worker_status_expire
        worker = worker or self.get_default_worker()
        wkey = self.get_worker_key(worker=worker)
        info = self.hgetall(wkey)
        if not info:
            self.hset(
                wkey,
                {
                    "worker": worker,
                    "start_time": nowtime,
                    "update_time": nowtime,
                },
            )
        else:
            self.hset(
                wkey,
                {
                    "update_time": nowtime,
                },
            )
        self.db.expire(wkey, expire)

    def get_worker_status(
        self,
        worker: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取执行器状态详情。

        参数:
            worker(str): 执行器名称。默认为{node}.{pid}。

        返回值:
            Dict[str, Any]: 执行器详情。主要字段有：
                worker(str): 执行器名称
                start_time(float): 执行器启动时间戳。
                update_time(float): 执行器状态最近更新时间戳。
                ttl(float): 执行器状态信息超时剩余时长。
        """
        worker = worker or self.get_default_worker()
        wkey = self.get_worker_key(worker)
        info = self.hgetall(wkey)
        if not info:
            return None
        ttl = self.db.ttl(wkey)
        info["ttl"] = ttl
        return info

    def recovery(
        self,
        channel=None,
        running_timeout_handler_policies=None,
    ):
        """恢复异常消息。

        对被执行器取走后长时间未确认的消息进行处理。

        处理策略：
            1）超时未确认的消息，直接标记为done，并且设置超时错误标记。
            2）超时未确认的消息，做退回处理。

        处理超时的判断依据：
            1）消息执行器状态为空。
            2）消息执行超过指定时长。

        参数:
            channel(str): 消息队列名称。不指定消息队列名称，则针对所有消息队列。

        返回值:
            int: 回收的消息数量。

        """
        lkey = channel or "__all__"
        current_rkeys = self.get_running_keys(channel=channel)
        last_running_rkeys = self.last_running_keys.get(lkey, None)
        if not last_running_rkeys:
            self.last_running_keys[lkey] = current_rkeys
            return 0
        else:
            self.last_running_keys[lkey] = current_rkeys
            rkeys_to_check = current_rkeys.intersection(last_running_rkeys)
            counter = 0
            for rkey in rkeys_to_check:
                id = self.get_id_from_running_key(rkey=rkey)
                ikey = self.get_item_key(id=id)
                msg = self.hgetall(ikey)
                # running记录中指定了无效的消息
                # 删除running记录，并记录异常
                if not msg:
                    self.db.delete(rkey)
                    counter += 1
                    _logger.error(
                        "执行记录中指定的ID没有找到对应的消息体：rkey=%s, ikey=%s, id=%s",
                        rkey,
                        ikey,
                        id,
                    )
                    continue
                # 获取回收策略
                running_timeout_handler_policy = self.get_running_timeout_handler_policy(
                    msg,
                    running_timeout_handler_policies=running_timeout_handler_policies,
                )
                # 消息执行器状态为空
                # 根据消息回收策略执行回收
                worker = msg.get("worker", None)
                wkey = self.get_worker_key(worker)
                info = self.hgetall(wkey)
                if not info:
                    self.running_timeout_handler(
                        msg,
                        running_timeout_handler_policy=running_timeout_handler_policy,
                        running_timoeut_reason="执行器状态异常",
                    )
                    counter += 1
                    continue
                # 消息执行超过指定时长
                # 根据消息回收策略执行回收
                start_time = msg.get("start_time", 0)
                nowtime = time.time()
                delta = nowtime - start_time
                if delta > running_timeout_handler_policy["running_timeout"]:
                    self.running_timeout_handler(
                        msg,
                        running_timeout_handler_policy=running_timeout_handler_policy,
                        running_timoeut_reason="执行超时",
                    )
                    counter += 1
                    continue

    def running_timeout_handler(
        self,
        msg,
        running_timeout_handler_policy=None,
        running_timoeut_reason="未指定原因",
    ):
        """消息处理超时回调处理函数。

        参数：
            msg(Dict[str, Any]): 消息详情。
            running_timeout_handler_policy(Dict[str, Any]): 消息处理超时回调处理策略。
            running_timoeut_reason(str): 消息处理超时原因。

        返回值：
            bool: 是否正确处理。

        """
        id = msg.get("id", None)
        if not id:
            _logger.info(
                "处理超时消息回收时遇到了错误的消息体: reason=%s, msg=%s",
                running_timoeut_reason,
                msg,
            )
            return False
        running_timeout_handler_policy = (
            running_timeout_handler_policy or self.get_running_timeout_handler_policy()
        )
        action = running_timeout_handler_policy["action"]
        if action == "drop":
            _logger.info(
                "超时消息的处理：处理方式=丢弃, 超时原因=%s, 消息体=%s",
                running_timoeut_reason,
                msg,
            )
            self.drop(id=id)
            return True
        elif action == "recover":
            _logger.info(
                "超时消息的处理：处理方式=回收, 超时原因=%s, 消息体=%s",
                running_timoeut_reason,
                msg,
            )
            self.ret(id=id, return_reason=running_timoeut_reason)
            return True

    def get_running_timeout_handler_policy(
        self,
        msg,
        running_timeout_handler_policies=None,
    ):
        """获取消息处理超时策略。

        参数：
            msg(Dict[str, Any]): 消息详情。

        返回值：
            Dict[str, Any]: 消息处理超时策略。如：
                ```
                    {
                        "running_timeout": 10,
                        "action": "drop"
                    }
                ```
        """
        running_timeout_handler_policies = (
            running_timeout_handler_policies or self.running_timeout_handler_policies
        )
        channel = msg.get("channel", None)
        policy = running_timeout_handler_policies.get(channel, {})
        return {
            "running_timeout": policy.get("running_timeout", self.running_timeout),
            "action": policy.get("action", self.default_running_timeout_action),
        }
