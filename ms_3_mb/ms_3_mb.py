import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
from common.logger import logger
import time
import pika
import json
from fastapi import FastAPI, Body
import uvicorn


################################################################################
# message broker - rabbitmq/pika
################################################################################

def mb_send_data(data: dict, queue_name: str) -> None:
    parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    try:
        channel = connection.channel()
        channel.queue_declare(queue = queue_name)
        channel.basic_publish(exchange = '',
                              routing_key = queue_name,
                              body = json.dumps(data))
    finally:
        if connection.is_open:
            connection.close()


################################################################################
# app/routes
################################################################################

app = FastAPI()


@app.post("/call_urlp")
async def route_call_urlp(email: str = Body(...), country: str = Body(...)) -> dict:
    """Маршрут - отправить сообщение в очередь на обработку к микросервису urlp.

    Args:
        email (str): Адрес электронной почты пользователя.
        country (str): Страна, гимн которой хотят получить.

    Returns:
        dict: {"status_code": число, "status_message": текст}.
    """
    try:
        mb_send_data({"email": email, "country": country}, MS_MB_QUEUE_URLP)
        result = {"status_code": "0", "status_message": "Success"}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_MB_NAME, "method": "route_call_urlp"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/call_fp")
async def route_call_fp(email: str = Body(...), country: str = Body(...), country_url: str = Body(default = None)) -> dict:
    """Маршрут - отправить сообщение в очередь на обработку к микросервису fp.

    Args:
        email (str): Адрес электронной почты пользователя.
        country (str): Страна, гимн которой хотят получить.
        country_url (str): URL wiki-страницы с описанием страны.

    Returns:
        dict: {"status_code": число, "status_message": текст}.
    """
    try:
        mb_send_data({"email": email, "country": country, "country_url": country_url}, MS_MB_QUEUE_FP)
        result = {"status_code": "0", "status_message": "Success"}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_MB_NAME, "method": "route_call_fp"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


if __name__ == "__main__":
    time.sleep(int(MS_MB_RUN_DELAY))
    uvicorn.run(
        app = "ms_3_mb:app",
        host = MS_MB_FASTAPI_HOST,
        port = int(MS_MB_FASTAPI_PORT),
        reload = True)