from random import choices
from typing import Tuple, Optional

import numpy as np
from pydantic import BaseModel
from xhm_config import conf
from xhm_log import error

try:
    from redis.connection import ConnectionPool
    from xhm_redis import XHMRedis

    REDIS_ENABLED = True
except ImportError:
    REDIS_ENABLED = False


def inverse_softmax(x):
    """
     Compute inverse softmax values for each a set/list of scores x,
    for which higher score is mapped to lower value.

    """
    e_x = np.exp(np.max(x) - x)
    return e_x / e_x.sum()


class LLMConfig:
    MAX_SCORE: int = 100
    PRE_CACHE: str = "llm_config"

    @classmethod
    def get_pool(cls):
        return ConnectionPool(
            host=conf.get("xhm_config_redis.host"),
            port=conf.get("xhm_config_redis.port"),
            password=conf.get("xhm_config_redis.password"),
            db=3,
            encoding="utf-8",
            decode_responses=True,
        )

    def __init__(self):
        if REDIS_ENABLED:
            self._cache = XHMRedis(connection_pool=self.get_pool())
        else:
            self._cache = None

    def get_config_repair_key(self, sid: str, ori_keys_available: str, attempt_number=0) -> (str, str):
        # 本函数主要是优选可用的key
        api_key, score = self._get_available_key(sid=sid, attempt_number=attempt_number,
                                                 ori_keys_available=ori_keys_available)

        return api_key, str(score)

    def _get_available_key(self, sid: str, ori_keys_available: str, attempt_number: int = 0) -> Tuple[str, float]:
        """随机从key池选择一个key
        """
        # 获取所有key，注意直接加key分数不能小于0，否则不会被选择
        if REDIS_ENABLED:
            keys_available = self._cache.zrangebyscore(f"{self.PRE_CACHE}_{sid}",
                                                       min=0, max='+inf', withscores=True)
        else:
            keys_available = []

        if len(keys_available) == 0:
            # 从数据库初始化keys
            keys = ori_keys_available.split(",")
            keys_available = [(element, 1.0) for element in keys]
            if REDIS_ENABLED:
                self._cache.zadd(f"{self.PRE_CACHE}_{sid}", mapping={key: 1 for key in keys})
        if attempt_number <= 1:
            # 第一次按权重随机选
            scores = list(zip(*keys_available))[1]
            w = inverse_softmax(scores)
            return choices(keys_available, k=1, weights=w)[0]
        else:
            # retry的时候按分数升序依次选
            return keys_available[(attempt_number - 1) % len(keys_available)]

    def error_key(self, sid: str, api_key: str = "", score: str = "0", error_type=""):
        """Move API_KEY to discarded keys pool if the corresponding ERROR_TYPE implies that
                the key need to be discarded. Fill up the available keys pool if needed.

        """

        if api_key != "":
            error(f"sid: {sid} api_key:{api_key} error: {error_type}")
            # increase the score to reduce the weight when randomly choosing a key
            if float(score) < self.MAX_SCORE:
                self._cache.zincrby(f"{self.PRE_CACHE}_{sid}", 1.0, api_key)


_llm_conf = LLMConfig()


class LLMInfo(BaseModel):
    sid: str
    # OPENAI_API_KEY
    api_key: Optional[str] = ""
    # OPENAI_API_BASE
    api_base: Optional[str] = ""
    proxy: Optional[str] = ""
    api_type: Optional[str] = ""
    api_version: Optional[str] = ""
    score: Optional[str] = ""
    query: Optional[dict] = {}
    # 额外的属性,重试的次数
    attempt_number: int = 0
    keys: str = ""

    def __call__(self):
        api_key, score = _llm_conf.get_config_repair_key(sid=self.sid,
                                                         ori_keys_available=self.keys,
                                                         attempt_number=self.attempt_number)
        self.api_key = api_key
        self.score = score
        return self

    def error_key(self, error_type=""):
        if self.sid and self.api_key:
            _llm_conf.error_key(sid=self.sid, api_key=self.api_key, score=self.score, error_type=error_type)
