from pathlib import Path
from typing import Dict, Any, Optional
from importlib import import_module

from samplemlproject.config.envconfig import replace_id_keys


class ImportException(Exception):
    pass


def class_or_func_creation_node(input_dict=None) -> Dict[str, Any]:
    return {'class': class_or_func_creation(input_dict)}


def class_or_func_creation(input_dict: Optional[dict] = None) -> Any:
    """
    Imports dynamically a class or function. When `type` is used the object is initialized with
    the given `params` accordingly. Otherwise (with `function`-keyword) only the imported object is returned.
    :param input_dict: dict with keywords (type and params) or function
    :return: Initialized or imported object/class/function.
    """
    use_params: bool = False
    if "type" in input_dict:
        cur_type: str = input_dict.pop("type")
        use_params = True
    elif "function" in input_dict:
        cur_type: str = input_dict.pop("function")
    else:
        raise ImportException("Neither type nor function keyword in param dict!")

    type_list = cur_type.rsplit(".", 1)
    imported_module = import_module(type_list[0])
    imported_type = getattr(imported_module, type_list[1])
    if use_params:
        try:
            init_class = imported_type(**input_dict["params"])
        except KeyError as e:
            raise ImportException("Keyword params required when using type to import") from e
    else:
        init_class = imported_type

    return init_class


def subs_path_and_create_folder(filepath: str) -> str:
    filepath = replace_id_keys(filepath)
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    return filepath