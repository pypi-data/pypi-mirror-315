"""股票"""
from copy import deepcopy
from typing import Any

from loguru import logger

from . import utils


def coderename(target: str | dict, restore: bool = False) -> str | dict | None:
    """
    正向:
        coderename('000001') => 'sz000001'
        coderename({'code': '000001', 'name': '平安银行'}) => {'code': 'sz000001', 'name': '平安银行'}
    反向:
        coderename('sz000001', restore=True) => '000001'
        coderename({'code': 'sz000001', 'name': '平安银行'}) => {'code': '000001', 'name': '平安银行'}
    """

    try:

        _object: Any = None
        _code_name: Any = None

        # 判断 target 是 string 还是 dictionary
        if isinstance(target, str) and utils.v_true(target, str):
            _code_name = target
        elif isinstance(target, dict) and utils.v_true(target, dict):
            _object = deepcopy(target)
            _code_name = str(deepcopy(target["code"]))
        else:
            return None

        # 是否还原
        if restore:
            if len(_code_name) == 8 and ("sh" in _code_name or "sz" in _code_name):
                _code_name = _code_name[2:8]
            else:
                return None
        else:
            if _code_name[0:2] == "00":
                _code_name = "sz" + _code_name
            elif _code_name[0:2] == "60":
                _code_name = "sh" + _code_name
            else:
                return None

        # 返回结果
        if utils.v_true(target, str):
            return _code_name

        if utils.v_true(target, dict):
            _object["code"] = _code_name
            return _object

        return None

    except Exception as e:
        logger.exception(e)
        return None
