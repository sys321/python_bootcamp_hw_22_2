import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
from common.logger import logger
import time
import requests
from fastapi import FastAPI, Body
import uvicorn


################################################################################
# app/routes
################################################################################

app = FastAPI()


@app.post("/proc_request")
async def route_proc_request(email: str = Body(...), country: str = Body(...)) -> dict:
    """Маршрут - обработать запрос пользователя.

    Args:
        email (str): Адрес электронной почты пользователя.
        country (str): Страна, гимн которой хотят получить.

    Returns:
        dict: {"status_code": число, "status_message": текст}.
    """
    result = False

    try:
        if not email or \
           not country:
            raise Exception(f"Parameter value = null")

        # Пишем информацию о запросе пользователя в базу данных, для сбора статистики.
        response = requests.post(
            url = MS_DB_URL + "/journalize_request",
            json = {"email": email, "country": country}
        )
        if response.status_code != 200:
            raise Exception(f"{MS_DB_NAME}: {response.status_code}-> {response.text}")
        data = response.json()
        if data["status_code"] != "0":
            raise Exception(f'{MS_DB_NAME}: {data["status_code"]} -> {data["status_message"]}')

        # Проверяем наличие данных о стране в кэш.
        response = requests.post(
            url = MS_CACHE_URL + "/get_country",
            json = {"country": country}
        )
        if response.status_code != 200:
            raise Exception(f"{MS_CACHE_NAME}: {response.status_code}-> {response.text}")
        data = response.json()
        if data["status_code"] not in "01":
            raise Exception(f'{MS_CACHE_NAME}: {data["status_code"]} -> {data["status_message"]}')

        # Данных о стране нет в кэш, вызываем url processor.
        if data["status_code"] != "0":
            response = requests.post(
                url = MS_MB_URL + "/call_urlp",
                json = {"email": email, "country": country}
            )

        # Данных о стране есть в кэш, вызываем file processor.
        else:
            response = requests.post(
                url = MS_MB_URL + "/call_fp",
                json = {"email": email, "country": country, "country_url": data["url"]}
            )

        if response.status_code != 200:
            raise Exception(f"{MS_MB_NAME}: {response.status_code} -> {response.text}")
        data = response.json()
        if data["status_code"] != "0":
            raise Exception(f'{MS_MB_NAME}: {data["status_code"]} -> {data["status_message"]}')

        result = {"status_code": "0", "status_message": "Success"}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_UI_NAME, "method": "route_proc_request"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}

    return result


if __name__ == "__main__":
    time.sleep(int(MS_UI_RUN_DELAY))
    uvicorn.run(
        app = "ms_1_ui:app",
        host = MS_UI_FASTAPI_HOST,
        port = int(MS_UI_FASTAPI_PORT),
        reload = True)