"""股票"""
import re
from copy import deepcopy

from loguru import logger
from pandas import DataFrame

from . import utils


def coderename(target: str | dict, restore: bool = False) -> str | dict | None:
    """代码重命名"""

    # 正向:
    #     coderename('000001') => 'sz000001'
    #     coderename({'code': '000001', 'name': '平安银行'}) => {'code': 'sz000001', 'name': '平安银行'}
    # 反向:
    #     coderename('sz000001', restore=True) => '000001'
    #     coderename({'code': 'sz000001', 'name': '平安银行'}) => {'code': '000001', 'name': '平安银行'}

    # 判断参数类型
    match True:
        case True if True not in [isinstance(target, str), isinstance(target, dict)]:
            logger.error("argument type error: target")
            return None
        case _:
            pass

    # 判断参数数据
    match True:
        case True if True not in [utils.isTrue(target, str), utils.isTrue(target, dict)]:
            logger.error("argument data error: data")
            return None
        case _:
            pass

    try:

        # 初始化
        code_object: dict = {}
        code_name: str | dict = ""

        # 判断 target 是 string 还是 dictionary
        if isinstance(target, str) and utils.isTrue(target, str):
            code_name = target
        elif isinstance(target, dict) and utils.isTrue(target, dict):
            code_object = deepcopy(target)
            code_name = str(deepcopy(target["code"]))
        else:
            return None

        # 是否还原
        if utils.isTrue(restore, bool):
            if len(code_name) == 8 and re.match(r"^(sz|sh)", code_name):
                code_name = deepcopy(code_name[2:8])
            else:
                return None
        else:
            if code_name[0:2] == "00":
                code_name = f"sz{code_name}"
            elif code_name[0:2] == "60":
                code_name = f"sh{code_name}"
            else:
                return None

        # 返回结果
        if utils.isTrue(target, str):
            return code_name

        if utils.isTrue(target, dict):
            code_object["code"] = code_name
            return code_object

        return None

    except Exception as e:
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def kdj_vector(df: DataFrame, cp: int = 9, sp1: int = 3, sp2: int = 3) -> DataFrame | None:
    """KDJ计算器"""

    # 计算周期：Calculation Period, 也可使用 Lookback Period 表示回溯周期, 指用于计算指标值的时间周期.
    # 移动平均周期: Smoothing Period 或 Moving Average Period, 指对指标进行平滑处理时采用的周期.
    # 同花顺默认参数: 9 3 3
    # https://www.daimajiaoliu.com/daima/4ed4ffa26100400
    # 说明: KDJ 指标的中文名称又叫随机指标, 融合了动量观念、强弱指标和移动平均线的一些优点, 能够比较迅速、快捷、直观地研判行情, 被广泛用于股市的中短期趋势分析.
    # 有采用 ewm 使用 com=2 的, 但是如果使用 com=2 在默认值的情况下KDJ值是正确的.
    # 但是非默认值, 比如调整参数, 尝试慢速 KDJ 时就不对了, 最终采用 alpha = 1/m 的情况, 对比同花顺数据, 是正确的.

    # 判断参数类型
    match True:
        case True if not isinstance(df, DataFrame):
            logger.error("argument type error: df")
            return None
        case _:
            pass

    try:
        low_list = df['low'].rolling(cp).min()
        high_list = df['high'].rolling(cp).max()
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        df['K'] = rsv.ewm(alpha=1 / sp1, adjust=False).mean()
        df['D'] = df['K'].ewm(alpha=1 / sp2, adjust=False).mean()
        df['J'] = (3 * df['K']) - (2 * df['D'])
        return df
    except Exception as e:
        logger.exception(e)
        return None
