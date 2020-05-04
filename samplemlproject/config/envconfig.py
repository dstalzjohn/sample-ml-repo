from os import getenv, environ

from samplemlproject.utilities.hashutils import generate_short_id

RUN_ID_KEY = "RUN_ID"
SHORT_ID_KEY = "SHORT_ID"
PIPELINE_KEY = "PIPELINE"


def get_run_id() -> str:
    return getenv(RUN_ID_KEY)


def get_short_id() -> str:
    return getenv(SHORT_ID_KEY)


def replace_id_keys(input_str: str) -> str:
    input_str = input_str.replace("$" + SHORT_ID_KEY, get_short_id())
    input_str = input_str.replace("$" + RUN_ID_KEY, get_run_id())

    return input_str


def set_pipeline_name(name: str):
    """
    Sets a pipeline name if not already set.
    """
    if getenv(PIPELINE_KEY) is None:
        environ[PIPELINE_KEY] = name


def get_pipeline_name() -> str:
    return getenv(PIPELINE_KEY)



