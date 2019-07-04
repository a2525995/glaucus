from rest_framework.exceptions import APIException

"""自定义exception 只要继承CPAPIException即可"""
class CPAPIException(APIException):
    status_code = 200
    default_code = '99999'
    default_detail = '未分类错误'

class TokenAuthicationError(CPAPIException):
    status_code = 503
    default_code = 1099
    default_detail = '秘钥认证失败'


class ParamError(CPAPIException):
    status_code = 400
    default_code = 1001
    default_detail = '传参错误'


class InternalError(CPAPIException):
    status_code = 500
    default_code = 1002
    default_detail = '服务器内部错误'


class APIExceptionFactory():
    @staticmethod
    def get_exception(exception=None):
        for _exception in CPAPIException.__subclasses__():
            if isinstance(exception, _exception):
                return _exception
        return CPAPIException


if __name__ == '__main__':
    a = CPAPIException()
    b = APIExceptionFactory.get_exception(a)
    print(b.default_code)
