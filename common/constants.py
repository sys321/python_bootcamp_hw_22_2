import os

# 3firm
POSTGRES_USER = os.getenv("POSTGRES_USER") or "tmp_user"#"user"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "tmp_password"#"1234"
POSTGRES_HOST = os.getenv("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.getenv("POSTGRES_PORT") or "5432"
POSTGRES_DB = os.getenv("POSTGRES_DB") or "tmp_db"##"stats"
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

RABBITMQ_USER = os.getenv("RABBITMQ_USER") or "user"
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD") or "1234"
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST") or "localhost"
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT") or "5672"
RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}"

REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = os.getenv("REDIS_PORT") or "6379"
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or "password"

SMTP_HOST = os.getenv("SMTP_HOST") or "smtp.mail.ru"
SMTP_PORT = os.getenv("SMTP_PORT") or 465
SMTP_USER = os.getenv("SMTP_USER") or "server@mail"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or "password"
SMTP_SENDER_EMAIL = os.getenv("SMTP_SENDER_EMAIL") or "server@mail"

# microservice 1 - user interface
MS_UI_NAME = "MS_1_UI"
MS_UI_RUN_DELAY = os.getenv("MS_UI_RUN_DELAY") or 0
MS_UI_FASTAPI_HOST = os.getenv("MS_UI_FASTAPI_HOST") or "0.0.0.0"
MS_UI_FASTAPI_PORT = os.getenv("MS_UI_FASTAPI_PORT") or "8001"
MS_UI_HOST = os.getenv("MS_UI_HOST") or "localhost"
MS_UI_PORT = os.getenv("MS_UI_PORT") or "8001"
MS_UI_URL = f"http://{MS_UI_HOST}:{MS_UI_PORT}"

# microservice 2 - database
MS_DB_NAME = "MS_2_DB"
MS_DB_RUN_DELAY = os.getenv("MS_DB_RUN_DELAY") or 0
MS_DB_FASTAPI_HOST = os.getenv("MS_DB_FASTAPI_HOST") or "0.0.0.0"
MS_DB_FASTAPI_PORT = os.getenv("MS_DB_FASTAPI_PORT") or "8002"
MS_DB_HOST = os.getenv("MS_DB_HOST") or "localhost"
MS_DB_PORT = os.getenv("MS_DB_PORT") or "8002"
MS_DB_URL = f"http://{MS_DB_HOST}:{MS_DB_PORT}"

# microservice 3 - message broker
MS_MB_NAME = "MS_3_MB"
MS_MB_RUN_DELAY = os.getenv("MS_MB_RUN_DELAY") or 0
MS_MB_FASTAPI_HOST = os.getenv("MS_MB_FASTAPI_HOST") or "0.0.0.0"
MS_MB_FASTAPI_PORT = os.getenv("MS_MB_FASTAPI_PORT") or "8003"
MS_MB_QUEUE_URLP = "URL_PROCESSOR"
MS_MB_QUEUE_FP = "FILE_PROCESSOR"
MS_MB_HOST = os.getenv("MS_MB_HOST") or "localhost"
MS_MB_PORT = os.getenv("MS_MB_PORT") or "8003"
MS_MB_URL = f"http://{MS_MB_HOST}:{MS_MB_PORT}"

# microservice 4 - url processor
MS_URLP_NAME = "MS_4_URLP"
MS_URLP_RUN_DELAY = os.getenv("MS_URLP_RUN_DELAY") or 0
WIKI_URL = "https://en.wikipedia.org"
WIKI_COUNTRY_LIST = "/wiki/List_of_countries_by_population_(United_Nations)"
WIKI_USER_AGENT = "CoolTool/0.0 (https://example.org/cool-tool/; cool-tool@example.org) generic-library/0.0"

# microservice 5 - file processor
MS_FP_NAME = "MS_5_FP"
MS_FP_RUN_DELAY = os.getenv("MS_FP_RUN_DELAY") or 0

# microservice 6 - cache
MS_CACHE_NAME = "MS_6_CACHE"
MS_CACHE_RUN_DELAY = os.getenv("MS_CACHE_RUN_DELAY") or 0
MS_CACHE_FASTAPI_HOST = os.getenv("MS_CACHE_FASTAPI_HOST") or "0.0.0.0"
MS_CACHE_FASTAPI_PORT = os.getenv("MS_CACHE_FASTAPI_PORT") or "8006"
MS_CACHE_HOST = os.getenv("MS_CACHE_HOST") or "localhost"
MS_CACHE_PORT = os.getenv("MS_CACHE_PORT") or "8006"
MS_CACHE_URL = f"http://{MS_CACHE_HOST}:{MS_CACHE_PORT}"

# microservice 7 - stats
MS_STATS_NAME = "MS_7_STATS"
MS_STATS_RUN_DELAY = os.getenv("MS_STATS_RUN_DELAY") or 0
MS_STATS_INTERVAL = os.getenv("MS_STATS_INTERVAL") or "1" # minutes

# unit-tests
UT_USER_EMAIL = os.getenv("UT_USER_EMAIL") or "user@mail"
UT_SUBSCRIBER_EMAIL = os.getenv("UT_SUBSCRIBER_EMAIL") or "subscriber@mail"
UT_COUNTRY = os.getenv("UT_COUNTRY") or "Russia"
UT_COUNTRY_URL = os.getenv("UT_COUNTRY_URL") or "https://en.wikipedia.org/wiki/Russia"
UT_NA_URL = os.getenv("UT_NA_URL") or "https://upload.wikimedia.org/wikipedia/commons/transcoded/4/41/National_Anthem_of_Russia_%282000%29%2C_instrumental%2C_one_verse.ogg/National_Anthem_of_Russia_%282000%29%2C_instrumental%2C_one_verse.ogg.mp3"
