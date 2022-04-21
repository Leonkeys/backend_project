import base64
import hmac
import time
import json
import copy
from core import content


class Jwt:
    @staticmethod  # 静态方法的装饰器封装一下  专门负责做计算用的函数
    def encode(self_payload, key, algorithm=content.HS256):
        header = {'typ': 'JWT', 'alg': algorithm}
        header_json = json.dumps(header, separators=(',', ':'), sort_keys=True)
        header_json_base64 = Jwt.b64encode(header_json.encode())

        self_payload_copy = copy.deepcopy(self_payload)
        self_payload_copy_json = json.dumps(self_payload_copy, separators=(',', ':'), sort_keys=True)
        self_payload_copy_json_base64 = Jwt.b64encode(self_payload_copy_json.encode())

        hm = hmac.new(key.encode(), header_json_base64 + b'.' + self_payload_copy_json_base64,
                      digestmod=content.HASHES[algorithm])
        hm_base64 = Jwt.b64encode(hm.digest())

        return header_json_base64 + b'.' + self_payload_copy_json_base64 + b'.' + hm_base64

    @staticmethod
    def decode(token, key, algorithm=content.HS256):

        header_bs, payload_bs, signature_bs = token.split(b".")
        hm = hmac.new(key.encode(), header_bs + b"." + payload_bs, digestmod=content.HASHES[algorithm])
        if signature_bs != Jwt.b64encode(hm.digest()):
            raise ExpiredSignatureError

        payload_js = Jwt.b64decode(payload_bs)
        payload = json.loads(payload_js)

        now = time.time()
        if int(now) > int(payload["exp"]):
            raise JWTError
        return payload

    @staticmethod
    def b64encode(js):
        return base64.urlsafe_b64encode(js).replace(b"=", b"")

    @staticmethod
    def b64decode(bs):
        rem = len(bs) % 4
        if rem > 0:
            bs += b'=' * (4 - rem)

        return base64.urlsafe_b64decode(bs)


class JWTError(Exception):
    pass


class ExpiredSignatureError(JWTError):
    pass
