from dataclasses import dataclass


@dataclass
class BaseResponse:
    def __init__(self, data, code=200, msg='ACK'):
        self.code = code
        self.msg = msg
        self.data = data

    def __dict__(self):
        return {'code': self.code,
                'msg': self.msg,
                'data': self.data}
