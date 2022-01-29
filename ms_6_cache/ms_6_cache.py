import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
from common.logger import logger
import time
import redis
from fastapi import FastAPI, Body
import uvicorn


################################################################################
# cache - redis
################################################################################

cache = redis.StrictRedis(
    host = REDIS_HOST,
    port = REDIS_PORT,
    #password=REDIS_PASSWORD,
    charset = "utf-8",
    decode_responses = True)


################################################################################
# app/routes
################################################################################

app = FastAPI()


@app.post("/clear_all")
async def route_clear_all() -> dict:
    """Маршрут - удалить все данные из кэш.
    """
    global cache
    try:
        answer = cache.flushall()
        result = {"status_code": ("0" if answer else "1"),
                  "status_message": ("Success" if answer else "Failure")}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_CACHE_NAME, "method": "route_clear_all"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/set_country")
async def route_set_country(country: str = Body(...), country_url: str = Body(...)) -> dict:
    """Маршрут - записать данные о стране в кэш.

    Args:
        country (str): Страна.
        country_url (str): URL wiki-страницы с описанием страны.

    Returns:
        dict: {"status_code": число, "status_message" : текст}.
    """
    global cache
    try:
        answer = cache.set(country, country_url)
        result = {"status_code": ("0" if answer else "1"),
                  "status_message": ("Success" if answer else "Failure")}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_CACHE_NAME, "method": "route_set_country"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/get_country")
async def route_get_country(country: str = Body(..., embed = True)) -> dict:
    """Маршрут - получить данные о стране из кэш.

    Args:
        country (str): Страна.

    Returns:
        dict: {"status_code": число, "status_message": текст, "url": URL}.
    """
    global cache
    try:
        answer = cache.get(country)
        result = {"status_code": ("0" if answer else "1"),
                  "status_message": ("Success" if answer else "Failure"),
                  "url": answer}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_CACHE_NAME, "method": "route_get_country"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/proc_country")
async def route_proc_country(country: str = Body(...), country_url: str = Body(...)) -> dict:
    """Маршрут - обработать данные о стране.

    Если данных нет в кэш, то записать. Просто так. Скоре всего,
    выпонять только set быстрее по скорости, чем get + set.

    Args:
        country (str): Страна.
        country_url (str): URL wiki-страницы с описанием страны.

    Returns:
        dict: {"status_code": число, "status_message": текст}.
    """
    global cache
    try:
        answer = cache.get(country)
        if not answer or answer != country_url:
            answer = cache.set(country, country_url)
        result = {"status_code": ("0" if answer else "1"),
                  "status_message": ("Success" if answer else "Failure")}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_CACHE_NAME, "method": "route_proc_country"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


if __name__ == "__main__":
    time.sleep(int(MS_CACHE_RUN_DELAY))
    uvicorn.run(
        app = "ms_6_cache:app",
        host = MS_CACHE_FASTAPI_HOST,
        port = int(MS_CACHE_FASTAPI_PORT),
        reload = True)