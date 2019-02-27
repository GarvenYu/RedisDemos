#! usr/bin/env python3
# -*-coding:utf-8-*-

import redis
import uuid
import time

client = redis.StrictRedis()


def acquire_lock(lockname, timeout=10, locktimeout=10):
    id = uuid.uuid4()
    end = time.time() + timeout
    lockname = 'lock:' + lockname
    while time.time() < end:
        if client.setnx(lockname, id):
            # 获取到了锁
            # 设置过期时间
            client.expire(lockname, locktimeout)
            return id
        elif not client.ttl(lockname):
            # 如果锁没有被设置过期时间
            client.expire(lockname, locktimeout)
        time.sleep(.001)
    return False
