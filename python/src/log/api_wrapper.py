from functools import wraps
from src.log.token_exception import TokenException
from src.log.api_login_old import *


def relogin(h=print, **kw):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            token = login_and_save_token(kwargs['env']) if 'env' in kwargs else login_and_save_token()
            print('--------------------------------1 %s' % token)
            print('%s %s %s' % (token, args, kwargs))
            content = func(token, *args, **kwargs)
            print('--------------------------------2')
            try:
                j = check_response(content)
                print('--------------------------------3')
                return h(j, **kw)
            except TokenException as ex:
                clear_token()
                print('--------------------------------4')
                return wrapped_function(*args, **kwargs)
            except Exception as ex:
                print(j)
                print(ex)
            # return func(token, *args, **kwargs)
        return wrapped_function
    return logging_decorator


if __name__ == "__main__":
    print('api_wrapper')