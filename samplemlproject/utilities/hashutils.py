import hashlib
import string

ALPHANUMERICLIST = list(string.digits + string.ascii_lowercase)


def generate_short_id(
    run_id, id_len=4
):
    hash_value = hashlib.md5(
        str([run_id]).encode()
    ).hexdigest()
    hash_value = int(hash_value, base=16)
    poss_values = len(ALPHANUMERICLIST) ** id_len
    hash_value = hash_value % poss_values
    str_value = base10toN(hash_value, ALPHANUMERICLIST)
    str_value = str_value.rjust(id_len, "0")
    return str_value


def base10toN(num, base_chars):
    """Change ``num'' to given base with character list"""

    converted_string, modstring = "", ""
    currentnum = num
    base = len(base_chars)
    if not 1 < base:
        raise ValueError("base must be between >= 2")
    if not num:
        return "0"
    while currentnum > 0:
        currentnum, mod = divmod(currentnum, base)
        converted_string = base_chars[mod] + converted_string
    return converted_string
