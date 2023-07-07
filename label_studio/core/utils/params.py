import os
from rest_framework.exceptions import ValidationError


def cast_bool_from_str(value):
    if isinstance(value, str):
        if value.lower() in ['true', 'yes', 'on', '1']:
            value = True
        elif value.lower() in ['false', 'no', 'not', 'off', '0']:
            value = False
        else:
            raise ValueError(f'Incorrect bool value "{value}". '
                             f'It should be one of [1, 0, true, false, yes, no]')
    return value


def bool_from_request(params, key, default):
    """ Get boolean value from request GET, POST, etc

    :param params: dict POST, GET, etc
    :param key: key to find
    :param default: default value
    :return: boolean
    """
    value = params.get(key, default)

    try:
        if isinstance(value, str):
            value = cast_bool_from_str(value)
        return bool(int(value))
    except Exception as e:
        raise ValidationError({key: str(e)})


def int_from_request(params, key, default):
    """ Get integer from request GET, POST, etc

    :param params: dict POST, GET, etc
    :param key: key to find
    :param default: default value
    :return: int
    """
    value = params.get(key, default)

    # str
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            raise ValidationError({key: f'Incorrect value in key "{key}" = "{value}". It should be digit string.'})
        except Exception as e:
            raise ValidationError({key: str(e)})
    # int
    elif isinstance(value, int):
        return value
    # other
    else:
        raise ValidationError({key: f'Incorrect value type in key "{key}" = "{value}". '
                                    f'It should be digit string or integer.'})


def float_from_request(params, key, default):
    """ Get float from request GET, POST, etc

    :param params: dict POST, GET, etc
    :param key: key to find
    :param default: default value
    :return: float
    """
    value = params.get(key, default)

    # str
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise ValidationError({key: f'Incorrect value in key "{key}" = "{value}". It should be digit string.'})
    elif isinstance(value, (float, int)):
        return float(value)
    else:
        raise ValidationError({key: f'Incorrect value type in key "{key}" = "{value}". '
                                    f'It should be digit string or float.'})


def list_of_strings_from_request(params, key, default):
    """ Get list of strings from request GET, POST, etc

    :param params: dict POST, GET, etc
    :param key: key to find
    :param default: default value
    :return: float
    """
    value = params.get(key, default)
    if value is None:
        return
    if not isinstance(value, str):
        raise ValidationError({key: f'Incorrect value type in key "{key}" = "{value}". '
                                    f'It should be digit string or float.'})
    splitters = (',', ';', '|')
    return next(
        (value.split(splitter) for splitter in splitters if splitter in value),
        [value],
    )


def get_env(name, default=None, is_bool=False):
    for env_key in [f'LABEL_STUDIO_{name}', f'HEARTEX_{name}', name]:
        value = os.environ.get(env_key)
        if value is not None:
            return bool_from_request(os.environ, env_key, default) if is_bool else value
    return default


def get_bool_env(key, default):
    return get_env(key, default, is_bool=True)


def get_env_list_int(key, default=None):
    """
    "1,2,3" in env variable => [1, 2, 3] in python
    """
    if value := get_env(key):
        return [int(el) for el in value.split(',')]
    else:
        return [] if default is None else default


def get_all_env_with_prefix(prefix=None, is_bool=True, default_value=None):
    return {
        key: bool_from_request(os.environ, key, default_value)
        if is_bool
        else os.environ[key]
        for key in os.environ
        if key.startswith(prefix)
    }
