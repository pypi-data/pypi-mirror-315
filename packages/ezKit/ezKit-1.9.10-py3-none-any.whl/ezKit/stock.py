"""股票"""
import re
from copy import deepcopy

import akshare as ak
import numpy as np
import talib as ta
from loguru import logger
from pandas import DataFrame
from sqlalchemy.engine import Engine

from . import utils


def coderename(
    target: str | dict,
    restore: bool = False
) -> str | dict | None:
    """代码重命名"""

    # 正向:
    #     coderename('000001') => 'sz000001'
    #     coderename({'code': '000001', 'name': '平安银行'}) => {'code': 'sz000001', 'name': '平安银行'}
    # 反向:
    #     coderename('sz000001', restore=True) => '000001'
    #     coderename({'code': 'sz000001', 'name': '平安银行'}) => {'code': '000001', 'name': '平安银行'}

    # 判断参数是否正确
    match True:
        case True if not utils.isTrue(target, (str, dict)):
            logger.error("argument error: target")
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


def kdj_vector(
    df: DataFrame,
    kdj_options: tuple[int, int, int] = (9, 3, 3)
) -> DataFrame | None:
    """KDJ计算器"""

    # 计算周期：Calculation Period, 也可使用 Lookback Period 表示回溯周期, 指用于计算指标值的时间周期.
    # 移动平均周期: Smoothing Period 或 Moving Average Period, 指对指标进行平滑处理时采用的周期.
    # 同花顺默认参数: 9 3 3
    # https://www.daimajiaoliu.com/daima/4ed4ffa26100400
    # 说明: KDJ 指标的中文名称又叫随机指标, 融合了动量观念、强弱指标和移动平均线的一些优点, 能够比较迅速、快捷、直观地研判行情, 被广泛用于股市的中短期趋势分析.
    # 有采用 ewm 使用 com=2 的, 但是如果使用 com=2 在默认值的情况下KDJ值是正确的.
    # 但是非默认值, 比如调整参数, 尝试慢速 KDJ 时就不对了, 最终采用 alpha = 1/m 的情况, 对比同花顺数据, 是正确的.

    # 判断参数是否正确
    match True:
        case True if not utils.isTrue(df, DataFrame):
            logger.error("argument error: df")
            return None
        case True if not any([utils.isTrue(kdj_options, tuple), all(utils.isTrue(item, int) for item in kdj_options)]):
            logger.error("argument error: kdj_options")
            return None
        case _:
            pass

    try:
        low_list = df['low'].rolling(kdj_options[0]).min()
        high_list = df['high'].rolling(kdj_options[0]).max()
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        df['K'] = rsv.ewm(alpha=1 / kdj_options[1], adjust=False).mean()
        df['D'] = df['K'].ewm(alpha=1 / kdj_options[2], adjust=False).mean()
        df['J'] = (3 * df['K']) - (2 * df['D'])
        return df
    except Exception as e:
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def data_vector(
    df: DataFrame,
    macd_options: tuple[int, int, int] = (12, 26, 9),
    kdj_options: tuple[int, int, int] = (9, 3, 3)
) -> DataFrame | None:
    """数据运算"""

    # 判断参数是否正确
    match True:
        case True if not utils.isTrue(df, DataFrame):
            logger.error("argument error: df")
            return None
        case True if not any([utils.isTrue(macd_options, tuple), all(utils.isTrue(item, int) for item in macd_options)]):
            logger.error("argument error: macd_options")
            return None
        case True if not any([utils.isTrue(kdj_options, tuple), all(utils.isTrue(item, int) for item in kdj_options)]):
            logger.error("argument error: kdj_options")
            return None
        case _:
            pass

    try:

        # 数据为空
        if isinstance(df, DataFrame) and df.empty:
            return None

        # ------------------------------------------------------------------------------------------

        # 计算均线: 3,7日均线
        # pylint: disable=E1101
        # df['SMA03'] = ta.SMA(df['close'], timeperiod=3)  # type: ignore
        # df['SMA07'] = ta.SMA(df['close'], timeperiod=7)  # type: ignore

        # 3,7日均线金叉: 0 无, 1 金叉, 2 死叉
        # df['SMA37_X'] = 0
        # sma37_position = df['SMA03'] > df['SMA07']
        # df.loc[sma37_position[(sma37_position is True) & (sma37_position.shift() is False)].index, 'SMA37_X'] = 1  # type: ignore
        # df.loc[sma37_position[(sma37_position is False) & (sma37_position.shift() is True)].index, 'SMA37_X'] = 2  # type: ignore

        # 计算均线: 20,25日均线
        # df['SMA20'] = ta.SMA(df['close'], timeperiod=20)  # type: ignore
        # df['SMA25'] = ta.SMA(df['close'], timeperiod=25)  # type: ignore

        # 20,25日均线金叉: 0 无, 1 金叉, 2 死叉
        # df['SMA225_X'] = 0
        # sma225_position = df['SMA20'] > df['SMA25']
        # df.loc[sma225_position[(sma225_position is True) & (sma225_position.shift() is False)].index, 'SMA225_X'] = 1  # type: ignore
        # df.loc[sma225_position[(sma225_position is False) & (sma225_position.shift() is True)].index, 'SMA225_X'] = 2  # type: ignore

        # ------------------------------------------------------------------------------------------

        # 计算 MACD: 默认参数 12 26 9
        macd_dif, macd_dea, macd_bar = ta.MACD(df['close'].values, fastperiod=macd_options[0], slowperiod=macd_options[1], signalperiod=macd_options[2])  # type: ignore
        macd_dif[np.isnan(macd_dif)], macd_dea[np.isnan(macd_dea)], macd_bar[np.isnan(macd_bar)] = 0, 0, 0

        # https://www.bilibili.com/read/cv10185856
        df['MACD'] = 2 * (macd_dif - macd_dea)
        df['MACD_DIF'] = macd_dif
        df['MACD_DEA'] = macd_dea

        # MACD 金叉死叉: 0 无, 1 金叉, 2 死叉
        df['MACD_X'] = 0
        macd_position = df['MACD_DIF'] > df['MACD_DEA']
        df.loc[macd_position[(macd_position is True) & (macd_position.shift() is False)].index, 'MACD_X'] = 1  # type: ignore
        df.loc[macd_position[(macd_position is False) & (macd_position.shift() is True)].index, 'MACD_X'] = 2  # type: ignore

        # ------------------------------------------------------------------------------------------

        # 计算 KDJ: : 默认参数 9 3 3
        kdj_data = kdj_vector(df, kdj_options)

        if kdj_data is not None:

            # KDJ 数据
            df['K'] = kdj_data['K'].values
            df['D'] = kdj_data['D'].values
            df['J'] = kdj_data['J'].values

            # KDJ 金叉死叉: 0 无, 1 金叉, 2 死叉
            df['KDJ_X'] = 0
            kdj_position = df['J'] > df['D']
            df.loc[kdj_position[(kdj_position is True) & (kdj_position.shift() is False)].index, 'KDJ_X'] = 1  # type: ignore
            df.loc[kdj_position[(kdj_position is False) & (kdj_position.shift() is True)].index, 'KDJ_X'] = 2  # type: ignore

        # ------------------------------------------------------------------------------------------

        return df

    except Exception as e:
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def get_code_name_from_akshare() -> DataFrame | None:
    """获取股票代码和名称"""
    info = "获取股票代码和名称"
    try:
        logger.info(f"{info} ......")
        df: DataFrame = ak.stock_info_a_code_name()
        if df.empty:
            logger.error(f"{info} [失败]")
            return None
        # 排除 ST、证券和银行
        # https://towardsdatascience.com/8-ways-to-filter-pandas-dataframes-d34ba585c1b8
        df = df[df.code.str.contains("^00|^60") & ~df.name.str.contains("ST|证券|银行")]
        logger.success(f"{info} [成功]")
        return df
    except Exception as e:
        logger.error(f"{info} [失败]")
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def get_stock_data_from_akshare(
    code: str,
    adjust: str = "qfq",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "20500101",
    timeout: float = 10
) -> DataFrame | None:
    """从 akshare 获取股票数据"""
    info = f"获取股票数据: {code}"
    try:
        logger.info(f"{info} ......")
        # https://akshare.akfamily.xyz/data/stock/stock.html#id22
        df: DataFrame = ak.stock_zh_a_hist(symbol=code, adjust=adjust, period=period, start_date=start_date, end_date=end_date, timeout=timeout)
        df = df.rename(columns={
            "日期": "date",
            "开盘": "open",
            "收盘": "close",
            "最高": "high",
            "最低": "low",
            "成交量": "volume",
            "成交额": "turnover"
        })
        df = df.round({'turnover': 4})
        logger.success(f"{info} [成功]")
        return df[['date', 'open', 'close', 'high', 'low', 'volume', 'turnover']].copy()
    except Exception as e:
        logger.error(f"{info} [失败]")
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def save_data_to_database(engine: Engine, code: str, latest: bool = False) -> bool:
    """保存股票所有数据到数据库"""

    # 默认将所有数据保存到数据库中的表里
    # 如果 latest 为 True, 插入最新的数据到数据库中的表里
    #   即: 将最后一条数据插入到数据库中的表里

    info: str = "保存股票所有数据到数据库"

    if utils.isTrue(latest, bool):
        info = "保存股票最新数据到数据库"

    try:

        logger.info(f"{info} ......")

        df: DataFrame | None = get_stock_data_from_akshare(code)

        if df is None:
            logger.error(f"{info} [获取数据失败]")
            return False

        name = coderename(code)

        if not isinstance(name, str):
            logger.error(f"{info} [代码名称转换失败]")
            return False

        if utils.isTrue(latest, bool):
            df = df.tail(1)
            df.to_sql(name=name, con=engine, if_exists="append", index=False)
        else:
            df.to_sql(name=name, con=engine, if_exists="replace", index=False)

        logger.success(f"{info} [成功]")

        return True

    except Exception as e:
        logger.success(f"{info} [失败]")
        logger.exception(e)
        return False
