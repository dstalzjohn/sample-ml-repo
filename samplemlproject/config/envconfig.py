from os import getenv

RUN_ID_KEY = "RUN_ID"


def get_run_id() -> str:
    return getenv(RUN_ID_KEY)
