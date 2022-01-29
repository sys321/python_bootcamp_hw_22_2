import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
from common.logger import logger
import time
import requests
import smtplib
from fpdf import FPDF, HTMLMixin
from email.message import EmailMessage
import schedule
import time


################################################################################
# stats
################################################################################

def stats_read_data() -> tuple:
    """Получить статистические данные из db.

    Returns:
        tuple: ([subscribers], [requests])
    """
    data = {"subscribers": None, "requests": None}
    try:
        response = requests.post(
            url = MS_DB_URL + "/stats_data"
        )
        if response.status_code != 200:
            raise Exception(f"Response = {response.status_code} / {response.text}")
        data = response.json()
        if data["status_code"] != "0":
            raise Exception(f'{MS_DB_NAME}: {data["status_code"]} -> {data["status_message"]}')
        data = data["data"]
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_STATS_NAME, "method": "stats_read_data"})

    return data["subscribers"], data["requests"]


def stats_gen_report(requests: list, file_path: str) -> bool:
    """Сгенерировать отчёт в pdf файл.

    Args:
        requests (list): Список с информацией о запросах пользователей.
        file_path (str): Локальный путь, где сохранить файл с отчётом.

    Returns:
        bool: Успешно (True) или нет (False).
    """
    result = False
    try:
        report = (
            '<table border="1" align="center" width="100%">'
            '<thead>'
              '<tr>'
                '<th width="10%">#</th>'
                '<th width="30%">Timestamp</th>'
                '<th width="30%">E-mail</th>'
                '<th width="30%">Country</th>'
              '</tr>'
            '</thead>'
            '<tbody>'
        )
        if len(requests) > 0:
            for rownum, request in enumerate(requests):
                report += (
                    '<tr>'
                      f'<td>{rownum + 1}</td>'
                      f'<td>{request[2]}</td>'
                      f'<td>{request[0]}</td>'
                      f'<td>{request[1]}</td>'
                    '</tr>'
                )
        else:
            report += (
                '<tr>'
                  '<td>-</td>'
                  '<td>-</td>'
                  '<td>-</td>'
                  '<td>-</td>'
                '</tr>'
            )
        report += (
            '</tbody>'
            '</table>'
        )

        class HTML2PDF(FPDF, HTMLMixin):
            pass
        pdf = HTML2PDF()
        pdf.add_page()
        pdf.write_html(report)
        pdf.output(file_path, 'F')

        result = True
    except Exception as exc:
        print(str(exc))
        logger.debug(str(exc), extra = {"ms": MS_STATS_NAME, "method": "stats_gen_report"})

    return result


def stats_send_email(sender: str, recipients: list, subject: str, content: str, attachment: str = None) -> bool:
    """Отправить email с отчётом-вложением.

    Args:
        sender (str): Адрес отправителя.
        recipient (list): Адреса получателей.
        subject (str): Тема/заголовок.
        content (str): Тест сообщения.
        attachment (str, optional): Имя файла-вложения.

    Returns:
        bool: Успешно (True) или нет (False).
    """
    result = False

    if not recipients or len(recipients) == 0:
        return result

    try:
        em = EmailMessage()
        em['From'] = sender
        em['To'] = ", ".join(recipients)
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
        logger.debug(str(exc), extra = {"ms": MS_STATS_NAME, "method": "stats_send_email"})

    return result


def stats_proc() -> None:
    """Обработать статистические данные, сформировать и отправить отчёт.

    Returns:
        None: None
    """
    try:
        subscribers, requests = stats_read_data()
        status = stats_gen_report(requests, "report.pdf")
        if status:
            stats_send_email(
                sender = SMTP_SENDER_EMAIL,
                recipients = subscribers,
                subject = "Stats report",
                content = "See attachments ..",
                attachment = "report.pdf")
        else:
            stats_send_email(
                sender = SMTP_SENDER_EMAIL,
                recipients = subscribers,
                subject = "Stats report",
                content = "Nope!")
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_STATS_NAME, "method": "stats_proc"})

    return None


if __name__ == "__main__":
    time.sleep(int(MS_STATS_RUN_DELAY))
    schedule.every(int(MS_STATS_INTERVAL)).minutes.do(stats_proc)

    while True:
        schedule.run_pending()
        time.sleep(10)