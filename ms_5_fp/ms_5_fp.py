import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
from common.logger import logger
import time
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import json
import pika
import requests


################################################################################
# file processor
################################################################################

def fp_read_wiki(country_url: str) -> str:
    """Получить URL аудиофайла с гимном.

    Args:
        country_url (str): URL wiki-страницы с описанием страны.

    Returns:
        str: URL аудиофайла.
    """
    result = None

    try:
        if not country_url:
            raise Exception(f"Parameter value = null")

        response = requests.get(
            url = country_url,
            headers = {'User-Agent': WIKI_USER_AGENT}
        )
        if response.status_code != 200:
            raise Exception(f"Response = {response.status_code} / {response.text}")

        soup = BeautifulSoup(response.text, "html.parser")
        for audio in soup.select('audio'):
            for source in audio.find_all("source"):
                result = "https:" + source.get("src") if source.get("src") else None
                break
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_FP_NAME, "method": "fp_read_wiki"})

    return result


def fp_download_file(file_url: str, file_path: str) -> bool:
    """Скачать аудиофайл по заданному URL.

    Args:
        file_url (str): URL аудиофайла.
        file_path (str): Локальный путь, где разместить скачанный аудиофайл.

    Returns:
        bool: Успешно (True) или нет (False).
    """
    result = False

    try:
        response = requests.get(
            url = file_url,
            stream = True, 
            headers = {'User-Agent': WIKI_USER_AGENT}
        )
        if response.status_code != 200:
            raise Exception(f"Response = {response.status_code} / {response.text}")

        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "wb") as file:
            file.write(response.content)

        result = True
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_FP_NAME, "method": "fp_download_file"})

    return result


def fp_send_email(sender: str, recipient: str, subject: str, content: str, attachment: str = None) -> bool:
    """Отправить email с аудиофайлом-вложением.

    Args:
        sender (str): Адрес отправителя.
        recipient (str): Адрес получателя.
        subject (str): Тема/заголовок.
        content (str): Тест сообщения.
        attachment (str, optional): Имя файла-вложения.

    Returns:
        bool: Успешно (True) или нет (False).
    """
    result = False

    try:
        em = EmailMessage()
        em['From'] = sender
        em['To'] = recipient
        em['Subject'] = subject
        em.set_content(content)

        if attachment:
            with open(attachment, "rb") as file:
                em.add_attachment(file.read(),
                    maintype = "application",
                    subtype = "octet-stream",
                    filename = os.path.basename(attachment))

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.set_debuglevel(False)
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(em)

        result = True
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_FP_NAME, "method": "fp_send_email"})

    return result


def fp_proc_file(ch, method, properties, body) -> None:
    """Обработать файл.

    Получить URL аудиофайла, скачать, отправить на заданный email.

    Returns:
        None: None
    """
    try:
        data = json.loads(body.decode())
        if data["country_url"]:
            file_url = fp_read_wiki(data["country_url"])
        else:
            file_url = None
        if file_url:
            file_path = os.path.basename(file_url)
            status = fp_download_file(file_url, file_path)
        else:
            status = False
        if status:
            fp_send_email(
                sender = SMTP_SENDER_EMAIL,
                recipient = data["email"],
                subject = "National anthem: " + data["country"],
                content = "See attachments ..",
                attachment = file_path)
        else:
            fp_send_email(
                sender = SMTP_SENDER_EMAIL,
                recipient = data["email"],
                subject = "National anthem: " + data["country"],
                content = 'National anthem for "' + data["country"] + '" not found!')
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_FP_NAME, "method": "fp_proc_file"})

    return None


################################################################################
# ожидание сообщений в очереди
################################################################################

def mb_receive_data() -> None:
    parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    try:
        channel = connection.channel()
        channel.queue_declare(queue = MS_MB_QUEUE_FP)
        channel.basic_consume(queue = MS_MB_QUEUE_FP,
                              auto_ack = True,
                              on_message_callback = fp_proc_file)
        channel.start_consuming()
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    time.sleep(int(MS_FP_RUN_DELAY))
    mb_receive_data()