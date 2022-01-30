from datetime import datetime
import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.constants import *
from common.logger import logger
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UniqueConstraint, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import FastAPI, Body
import uvicorn


################################################################################
# database - postgres
################################################################################
engine = create_engine(url = POSTGRES_URL)


################################################################################
# models
################################################################################

DBModel = declarative_base()


class DBModelExt(DBModel):
    """Расширение для базовой модели. Добавляются конвертации в строку и словарь.
    """
    __abstract__ = True

    def __str__(self) -> str:
        return " / ".join(str(getattr(self, column.name)) \
            for column in self.__table__.columns)

    def to_dict(self):
        return {column.name: getattr(self, column.name) \
            for column in self.__table__.columns}


class DBUser(DBModelExt):
    """Таблица с пользователями.
    """
    __tablename__ = "users"

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True, index = True)
    email = Column(String, nullable = False, unique = True, index = True)
    requests = relationship("DBRequest", back_populates = "user", passive_deletes = True)

    def __init__(self, email: str) -> None:
        self.email = email


class DBRequest(DBModelExt):
    """Таблица с запросами пользователей (гимны каких стран хотели).
    """
    __tablename__ = "requests"

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = 'CASCADE'), nullable = False, index = True)
    country = Column(String, nullable = False)
    ts = Column(DateTime, nullable = False)
    user = relationship("DBUser", back_populates = "requests")

    def __init__(self, user_id: int, country: str, ts: datetime) -> None:
        self.country = country
        self.user_id = user_id
        self.ts = ts


class DBSubscriber(DBModelExt):
    """Таблица с подписчиками
       (кому отправлять pdf отчёт с информацией о пользователях и запросах).
    """
    __tablename__ = "subscribers"

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True, index = True)
    email = Column(String, nullable = False, unique = True, index = True)

    def __init__(self, email: str) -> None:
        self.email = email


DBModel.metadata.create_all(engine)


################################################################################
# CRUD
################################################################################

DBSession = sessionmaker(autocommit = False, autoflush = False, bind = engine)


def db_clear_all() -> None:
    """Удалить все данные из таблиц БД.
    """
    global DBSession
    with DBSession() as session:
        session.query(DBSubscriber).delete()
        session.query(DBRequest).delete()
        session.query(DBUser).delete()
        session.commit()
    return None


def db_create_user(email: str) -> DBUser:
    """Создать нового пользователя.

    Args:
        email (str): Адрес электронной почты.

    Raises:
        IntegrityError: Пользователь с заданным email уже существует.

    Returns:
        DBUser: Пользователь в виде модели DBUser.
    """
    global DBSession
    with DBSession() as session:
        user = DBUser(email = email)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def db_create_subscriber(email: str) -> DBSubscriber:
    """Создать нового подписчика.

    Args:
        email (str): Адрес электронной почты.

    Raises:
        IntegrityError: Подписчик с заданным email уже существует.

    Returns:
        DBSubscriber: Подписчик в виде модели DBSubscriber.
    """
    global DBSession
    with DBSession() as session:
        subscriber = DBSubscriber(email = email)
        session.add(subscriber)
        session.commit()
        session.refresh(subscriber)
    return subscriber


def db_journalize_request(email: str, country: str) -> DBRequest:
    """Журнализировать запрос пользователя.

    Args:
        email (str): Адрес электронной почты пользователя.
        country (str): Страна, гимн которой хотят получить.

    Returns:
        DBRequest: Запрос в виде модели DBRequest.
    """
    global DBSession
    with DBSession() as session:
        # Проверяем существование пользователя. Если нет, то создаём.
        try:
            user = session.query(DBUser).filter(DBUser.email == email).one()
        except NoResultFound:
            user = db_create_user(email)
        # Создаём запрос.
        request = DBRequest(user_id = user.id, country = country, ts = datetime.now())
        session.add(request)
        # Коммит.
        session.commit()
        session.refresh(request)
    return request


def db_stats_data() -> dict:
    """Получить статистические данные. Кто-что-когда запрашивал.

    Returns:
        dict: {"subscribers": [], "requests": []}
    """
    global DBSession
    data = {"subscribers": [], "requests": []}
    with DBSession() as session:
        subscribers = session.query(DBSubscriber)
        data["subscribers"] = [subscriber.email for subscriber in subscribers]
        requests = session.query(DBRequest)
        data["requests"] = [[request.user.email, request.country, request.ts]
            for request in requests]
    return data


################################################################################
# app/routes
################################################################################

app = FastAPI()


@app.post("/clear_all")
async def route_clear_all() -> dict:
    """Маршрут - удалить все данные из таблиц БД.

    Returns:
        dict: {"status_code": число, "status_message": текст}.
    """
    try:
        db_clear_all()
        result = {"status_code": "0", "status_message": "Success"}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_DB_NAME, "method": "route_clear_all"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/create_user")
async def route_create_user(email: str = Body(..., embed = True)) -> dict:
    """Маршрут - создать нового пользователя.

    Args:
        email (str): Адрес электронной почты пользователя.

    Returns:
        dict: {"status_code": число, "status_message": текст[, "data": словарь]}.
    """
    try:
        user = db_create_user(email)
        result = {"status_code": "0", "status_message": "Success", "data": user.to_dict()}
    except IntegrityError as exc:
        result = {"status_code": "1", "status_message": str(exc)}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_DB_NAME, "method": "route_create_user"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/create_subscriber")
async def route_create_subscriber(email: str = Body(..., embed = True)) -> dict:
    """Маршрут - создать нового подписчика.

    Args:
        email (str): Адрес электронной почты подписчика.

    Returns:
        dict: {"status_code": число, "status_message": текст[, "data": словарь]}.
    """
    try:
        subscriber = db_create_subscriber(email)
        result = {"status_code": "0", "status_message": "Success", "data": subscriber.to_dict()}
    except IntegrityError as exc:
        result = {"status_code": "1", "status_message": str(exc)}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_DB_NAME, "method": "route_create_subscriber"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/journalize_request")
async def route_journalize_request(email: str = Body(...), country: str = Body(...)) -> dict:
    """Маршрут - обработать запрос пользователя.

    Args:
        email (str): Адрес электронной почты пользователя.
        country (str): Страна, гимн которой хотят получить.

    Returns:
        dict: {"status_code": число, "status_message": текст[, "data": словарь]}.
    """
    try:
        request = db_journalize_request(email, country)
        result = {"status_code": "0", "status_message": "Success", "data": request.to_dict()}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_DB_NAME, "method": "route_journalize_request"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


@app.post("/stats_data")
async def route_stats_data() -> dict:
    """Маршрут - получить статистические данные. Кто-что-когда запрашивал.

    Returns:
        dict: {"status_code": число, "status_message": текст[, "data": словарь]}.
    """
    try:
        data = db_stats_data()
        result = {"status_code": "0", "status_message": "Success", "data": data}
    except Exception as exc:
        logger.debug(str(exc), extra = {"ms": MS_DB_NAME, "method": "route_stats_data"})
        result = {"status_code": "-1", "status_message": f"Something went wrong: {exc}"}
    return result


if __name__ == "__main__":
    time.sleep(int(MS_DB_RUN_DELAY))
    uvicorn.run(
        app = "ms_2_db:app",
        host = MS_DB_FASTAPI_HOST,
        port = int(MS_DB_FASTAPI_PORT),
        reload = True)