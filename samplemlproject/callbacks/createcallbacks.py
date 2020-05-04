from typing import List, Any

from ccmlutils.utilities.factoryutils import class_or_func_creation


def create_callbacks(input_list: List[dict]) -> List[Any]:
    callback_list = []
    for cur_dict in input_list:
        callback_list.append(class_or_func_creation(cur_dict))

    return callback_list


def create_callbacks_node(input_list: List[dict]) -> dict:
    return dict(callbacks=create_callbacks(input_list))
