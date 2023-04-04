from typing import Any

from fastapi import FastAPI


def get_all_sub_apps(app: FastAPI) -> list[FastAPI]:
    return [route.app for route in app.routes if hasattr(route, "app") and isinstance(route.app, FastAPI)]


def execute_object_function(obj: Any, func: str, *args, **kwargs):
    def inner():
        object_function = getattr(obj, func)
        return object_function(*args, **kwargs)

    return inner()


async def execute_async_object_function(obj: Any, func: str, *args, **kwargs):
    async def inner():
        object_function = getattr(obj, func)
        return await object_function(*args, **kwargs)

    return await inner()


def case_free_pop(data: dict, key: Any, default_value: Any | None = None):
    if isinstance(key, str):
        for k in (key, key.upper(), key.lower()):
            if k in data:
                return data.pop(k)
    else:
        if key in data:
            return data.pop(key)
    return default_value
