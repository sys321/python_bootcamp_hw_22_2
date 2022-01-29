import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
from common.logger import logger
import time
from bs4 import BeautifulSoup
import re
import json
import pika
import requests


################################################################################
# url processor
################################################################################

def urlp_read_wiki(country: str) -> str:
    """Получить URL wiki-страницы с информацией о стране.

    Returns:
        str: URL.
    """
    result = None

    try:
        if not country:
            raise Exception(f"Parameter value = null")

        response = requests.get(
            url = WIKI_URL + WIKI_COUNTRY_LIST,
            headers = {'User-Agent': WIKI_USER_AGENT}
        )
        if response.status_code != 200:
            raise Exception(f"Response = {response.status_code} / {response.text}")

        re_clear = re.compile("\[.+?\]")
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find("table").find("tbody").find_all("tr")
        for row in rows:
            if not row:
                continue
            col = row.find("td")
            if not col:
                continue
            data = re.sub(re_clear, '', col.text).strip("\r\n\t \xa0")
            if country.upper() == data.upper():
                result = WIKI_URL + col.find("a").attrs["href"]
                break
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_URLP_NAME, "method": "urlp_read_wiki"})

    return result


def urlp_write_cache(country: str, country_url: str) -> bool:
    """Поместить информацию о стране в кэш.

    Args:
        country (str): Страна.
        country_url (str): URL wiki-страницы с описанием страны.

    Returns:
        bool: Успешно (True) или нет (False).
    """
    result = False

    try:
        if not country or \
           not country_url:
            raise Exception(f"Parameter value = null")

        response = requests.post(
            url = MS_CACHE_URL + "/proc_country",
            json = {"country": country, "country_url": country_url}
        )
        if response.status_code != 200:
            raise Exception(f"Response = {response.status_code} / {response.text}")

        result = True
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_URLP_NAME, "method": "urlp_write_cache"})

    return result


def urlp_call_fp(email: str, country: str, country_url: str) -> bool:
    """Отправить сообщение в очередь на обработку к микросервису fp.

    Args:
        email (str): Адрес электронной почты пользователя.
        country (str): Страна.
        country_url (str): URL на страницу wiki с описанием страны.

    Returns:
        bool: Успешно (True) или нет (False).
    """
    result = False

    try:
        if not email or \
           not country:
            raise Exception(f"Parameter value = null")

        response = requests.post(
            url = MS_MB_URL + "/call_fp",
            json = {"email": email, "country": country, "country_url": country_url}
        )
        if response.status_code != 200:
            raise Exception(f"{response.status_code}: {response.text}")

        result = True
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_URLP_NAME, "method": "urlp_call_fp"})

    return result


def urlp_proc_country(ch, method, properties, body) -> None:
    """Обработать страну.

    Получить URL wiki-страницы, записать в кэш, отправить сообщение в очередь.

    Returns:
        None: None
    """
    try:
        data = json.loads(body.decode())
        country_url = urlp_read_wiki(data['country'])
        if country_url:
            urlp_write_cache(data['country'], country_url)
        urlp_call_fp(data['email'], data['country'], country_url)
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_URLP_NAME, "method": "urlp_proc_country"})

    return None


################################################################################
# ожидание сообщений в очереди
################################################################################

def mb_receive_data() -> None:
    parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    try:
        channel = connection.channel()
        channel.queue_declare(queue = MS_MB_QUEUE_URLP)
        channel.basic_consume(queue = MS_MB_QUEUE_URLP,
                              auto_ack = True,
                              on_message_callback = urlp_proc_country)
        channel.start_consuming()
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    time.sleep(int(MS_URLP_RUN_DELAY))
    mb_receive_data()