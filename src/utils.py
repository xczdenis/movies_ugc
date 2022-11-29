from functools import wraps


def to_params(*query_params, _required: bool = False):
    """
    Декоратор, который извлекает все параметры, указанные query_params, из
    kwargs и кладет их в аргумент params. Если _required = True, то каждый параметр
    в query_params считается обязательным. Если какого-либо параметра нет среди kwargs,
    то выдается ошибка AttributeError.
    """

    def _wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            params = (kwargs.pop("params", None) or {}).copy()
            for p in query_params:
                if p in kwargs:
                    v = kwargs.pop(p)
                    if v is not None:
                        params[p] = v
                elif _required:
                    raise AttributeError("Missing argument '%s'" % p)

            return func(*args, params=params, **kwargs)

        return _wrapped

    return _wrapper


def required_params(*query_params):
    """
    Декоратор, который извлекает все параметры, указанные query_params, из
    kwargs и кладет их в аргумент params. Если какого-либо параметра нет среди kwargs,
    то выдается ошибка AttributeError
    """
    return to_params(*query_params, _required=True)
