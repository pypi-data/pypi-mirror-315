import redis
import time
from flask import Flask, has_app_context
from flask.globals import app_ctx

from flask_redis_stream_pubsub import util

DEFAULT_STREAM_MAX_LEN = 2048
PRODUCER_SESSION_BUFFER_SIZE = 32


class Producer:
    __slots__ = ['maxlen', '__rcli']

    def __init__(self, redis_url='', maxlen=DEFAULT_STREAM_MAX_LEN):
        self.maxlen = maxlen
        self.__rcli = None
        if redis_url:
            self.__rcli = redis.from_url(redis_url, decode_responses=True)

    def init_redis(self, redis_url=''):
        self.__rcli = redis.from_url(redis_url, decode_responses=True)

    def init_app(self, app: Flask, config_prefix='PUBSUB_REDIS'):
        redis_url = app.config.get(
            "{0}_URL".format(config_prefix), "redis://localhost:6379/0"
        )

        rcli = redis.from_url(redis_url, decode_responses=True)
        self.__rcli = rcli

    def publish(self, stream_name: str, payload: dict, maxlen=None):
        __maxlen = maxlen if maxlen else self.maxlen
        payload['__PUBLISH_TIME'] = int(time.time() * 1000)
        payload['__SOURCE'] = 'producer'
        return self.__rcli.xadd(stream_name, payload, maxlen=__maxlen)

    @property
    def session(self):
        if has_app_context():
            if not hasattr(app_ctx, 'producer_session'):
                app_ctx.producer_session = ProducerSession(self.__rcli, self.maxlen)
            return app_ctx.producer_session

        return ProducerSession(self.__rcli, self.maxlen)


class ProducerSession:
    __slots__ = ['__rcli', 'maxlen', 'msgs']

    def __init__(self, rcli: redis.Redis, maxlen=None):
        self.__rcli = rcli
        self.msgs = []
        self.maxlen = maxlen

    def add(self, stream_name: str, payload: dict, maxlen=None):
        __maxlen = maxlen if maxlen else self.maxlen
        self.msgs.append({
            'name': stream_name,
            'payload': payload,
            'maxlen': maxlen,
        })

    def clear(self):
        self.msgs = []

    def commit(self):
        self.publish()

    def publish(self):
        __msgs = self.msgs[:]
        self.clear()

        __msg_groups = util.chunk_array(__msgs, PRODUCER_SESSION_BUFFER_SIZE)
        res = []

        for msg_list in __msg_groups:
            with self.__rcli.pipeline() as pipe:
                current_time = int(time.time() * 1000)
                for msg in msg_list:
                    payload = msg['payload']
                    payload['__PUBLISH_TIME'] = current_time
                    payload['__SOURCE'] = 'producer'
                    pipe.xadd(msg['name'], payload, maxlen=msg['maxlen'])

                pipe_res = pipe.execute()
                if isinstance(pipe_res, list):
                    res.extend(pipe_res)

        return res
