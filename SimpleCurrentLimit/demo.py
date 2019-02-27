#! usr/bin/env python3
# -*-coding:utf-8-*-

import redis
import time

client = redis.StrictRedis()


def is_action_allowed(user_id, action, period, max_count):
    """
    简单限流
    :param user_id: 用户标记
    :param action: 限制行为
    :param period: 时间窗口
    :param max_count: 最大次数
    :return: bool
    """
    key = "history:%s:%s" % (user_id, action)
    now = int(time.time() * 1000)  # 毫秒
    with client.pipeline() as pipe:
        pipe.zadd(key, {now: now})  # value score 都使用毫秒时间戳
        pipe.zremrangebyscore(key, 0, now - period * 1000)  # 移除period之前的行为
        pipe.zcard(key)
        pipe.expire(key, period + 1)  # 设置过期时间,避免不活跃的持续占用内存
        current_count = pipe.execute()[2]
    return current_count <= max_count  # 比较是否超出限制


for i in range(20):
    if is_action_allowed("test", "comment", 60, 5):
        # success
        pass
    else:
        # fail
        pass
    time.sleep(1)
