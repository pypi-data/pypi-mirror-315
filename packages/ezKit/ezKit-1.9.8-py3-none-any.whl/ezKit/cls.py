"""财联社数据"""
import re

import pandas as pd
import requests
from loguru import logger

from . import stock, utils


def up_down_analysis(
    target: str = "up_pool",
    df: bool = False
) -> list | pd.DataFrame | None:
    """涨停跌停数据"""

    # 判断参数是否正确
    match True:
        case True if not utils.isTrue(target, str):
            logger.error("argument error: target")
            return None
        case _:
            pass

    info: str = "获取涨停池股票"
    match True:
        case True if target == "up_pool":
            info = "获取涨停池股票"
        case True if target == "continuous_up_pool":
            info = "获取连板池股票"
        case True if target == "up_open_pool":
            info = "获取炸板池股票"
        case True if target == "down_pool":
            info = "获取跌停池股票"
        case _:
            pass

    try:
        logger.info(f"{info} ......")

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}

        # 涨停池: https://x-quote.cls.cn/quote/index/up_down_analysis?rever=1&way=last_px&type=up_pool
        # 连板池: https://x-quote.cls.cn/quote/index/up_down_analysis?rever=1&way=last_px&type=continuous_up_pool
        # 炸板池: https://x-quote.cls.cn/quote/index/up_down_analysis?rever=1&way=last_px&type=up_open_pool
        # 跌停池: https://x-quote.cls.cn/quote/index/up_down_analysis?rever=1&way=last_px&type=down_pool
        api = f"https://x-quote.cls.cn/quote/index/up_down_analysis?rever=1&way=last_px&type={target}"

        response = requests.get(api, headers=headers, timeout=10)

        response_dict: dict = response.json()

        result: list = []

        for i in response_dict["data"]:

            # if re.match(r"^(sz00|sh60)", i["secu_code"]):
            #     print(i["secu_code"])

            # if re.search(r"ST|银行", i["secu_name"]):
            #     print(i["secu_name"])

            # 主板, 非ST, 非银行, 非证券
            if (not re.match(r"^(sz00|sh60)", i["secu_code"])) or re.search(r"ST|银行|证券", i["secu_name"]):
                continue

            if target in ["up_pool", "up_pool"]:
                result.append({
                    "code": stock.coderename(i["secu_code"], restore=True),
                    "name": i["secu_name"],
                    "up_days": i["limit_up_days"],
                    "reason": i["up_reason"]
                })

            if target in ["up_open_pool", "down_pool"]:
                result.append({
                    "code": stock.coderename(i["secu_code"], restore=True),
                    "name": i["secu_name"]
                })

        if not utils.isTrue(df, bool):
            logger.success(f"{info} [成功]")
            return result

        # data: pd.DataFrame = pd.DataFrame(response_dict["data"], columns=["secu_code", "secu_name", "limit_up_days", "up_reason"])
        # data = data.rename(columns={"secu_code": "code", "secu_name": "name", "limit_up_days": "up_days", "up_reason": "reason"})

        return pd.DataFrame(data=pd.DataFrame(result))

    except Exception as e:
        logger.error(f"{info} [失败]")
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def latest_data(
    payload: str | dict,
    data_type: str = "stock",
    df: bool = False
) -> list | pd.DataFrame | None:
    """股票或板块的最新数据"""

    # 热门板块
    #   https://www.cls.cn/hotPlate
    # 行业板块
    #   https://x-quote.cls.cn/web_quote/plate/plate_list?rever=1&way=change&type=industry
    # 概念板块
    #   https://x-quote.cls.cn/web_quote/plate/plate_list?rever=1&way=change&type=concept
    # 地域板块
    #   https://x-quote.cls.cn/web_quote/plate/plate_list?rever=1&way=change&type=area

    # ----------------------------------------------------------------------------------------------

    # 判断参数类型
    match True:
        case True if not utils.isTrue(payload, (str, dict)):
            logger.error("argument error: payload")
            return None
        case True if not utils.isTrue(data_type, str):
            logger.error("argument error: data_type")
            return None
        case _:
            pass

    # ----------------------------------------------------------------------------------------------

    # 判断数据类型. 数据类型: 个股, 板块 (产业链: industry)
    if data_type not in ["stock", "plate"]:
        logger.error("data_type error")
        return None

    # ----------------------------------------------------------------------------------------------

    # 日志信息

    # 个股 (默认)
    info: str = "获取股票最新数据"

    # 板块
    if data_type == "plate":
        info = "获取板块最新数据"

    # match True:
    #     case True if data_type == "plate":
    #         info = "获取板块最新数据"
    #     case True if data_type == "industry":
    #         info = "获取产业链最新数据"
    #     case _:
    #         pass

    # ----------------------------------------------------------------------------------------------

    try:

        logger.info(f"{info} ......")

        # ------------------------------------------------------------------------------------------

        # HTTP User Agent
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

        # HTTP Headers
        headers = {"User-Agent": user_agent}

        # ------------------------------------------------------------------------------------------

        # 请求参数
        params: dict = {}

        # 默认请求参数
        if isinstance(payload, str) and utils.isTrue(payload, str):
            params = {"secu_code": payload}

        # 请求参数
        if isinstance(payload, dict) and utils.isTrue(payload, dict):
            params = payload

        # ------------------------------------------------------------------------------------------

        # 不直接在API后面跟参数, 使用 params 传递参数

        # API: 股票
        # api: str = f"https://x-quote.cls.cn/quote/stock/basic?secu_code={code}"
        api: str = "https://x-quote.cls.cn/quote/stock/basic"

        # API: 板块
        if data_type == "plate":
            # api = f"https://x-quote.cls.cn/web_quote/plate/stocks?secu_code={code}"
            api = "https://x-quote.cls.cn/web_quote/plate/stocks"

        # match True:
        #     case True if data_type == "plate":
        #         # 板块
        #         # api = f"https://x-quote.cls.cn/web_quote/plate/stocks?secu_code={code}"
        #         api = "https://x-quote.cls.cn/web_quote/plate/stocks"
        #     case True if data_type == "industry":
        #         # 产业链
        #         # api = f"https://x-quote.cls.cn/web_quote/plate/industry?secu_code={code}"
        #         api = "https://x-quote.cls.cn/web_quote/plate/industry"
        #     case _:
        #         pass

        # ------------------------------------------------------------------------------------------

        # 获取数据
        # response = requests.get(api, headers=headers, timeout=10)
        response = requests.get(api, headers=headers, params=params, timeout=10)

        # 转换数据类型
        response_dict: dict = response.json()

        # 判断数据是否正确
        if True not in [utils.isTrue(response_dict["data"], dict), utils.isTrue(response_dict["data"], list)]:
            logger.error(f"{info} [失败]")
            return None

        # ------------------------------------------------------------------------------------------

        # 个股

        if data_type == "stock":

            # 停牌, 返回 None
            if response_dict["data"]["trade_status"] == "STOPT":
                logger.error(f"{info} [停牌]")
                return None

            # pd.DataFrame 数据
            if utils.isTrue(df, bool):
                df_data = {
                    # "date": [pd.to_datetime(date_today)],
                    "open": [float(response_dict["data"]["open_px"])],
                    "close": [float(response_dict["data"]["last_px"])],
                    "high": [float(response_dict["data"]["high_px"])],
                    "low": [float(response_dict["data"]["low_px"])],
                    "volume": [int(response_dict["data"]["business_amount"])],
                    "turnover": [float(response_dict["data"]["tr"])]
                }
                logger.success(f"{info} [成功]")
                return pd.DataFrame(data=df_data)

            # 默认返回的数据
            logger.success(f"{info} [成功]")
            return response_dict["data"]

        # ------------------------------------------------------------------------------------------

        # 板块

        # 板块数据不能转换为 pd.DataFrame
        if (data_type == "plate") and utils.isTrue(df, bool):
            logger.error(f"{info} [错误]")
            return None

        # 数据结果
        result: list = []

        # 筛选 主板, 非ST, 非银行, 非证券 的股票
        for i in response_dict["data"]["stocks"]:
            if (re.match(r"^(sz00|sh60)", i["secu_code"])) and (not re.search(r"ST|银行|证券", i["secu_name"])):
                result.append(i)

        # 返回数据
        logger.success(f"{info} [成功]")
        return result

    except Exception as e:
        logger.error(f"{info} [失败]")
        logger.exception(e)
        return None


# --------------------------------------------------------------------------------------------------


def plate_codes(
    plate: str
) -> list | None:
    """获取板块成分股代码"""

    # 判断参数是否正确
    match True:
        case True if not utils.isTrue(plate, str):
            logger.error("argument error: plate")
            return None
        case _:
            pass

    info: str = "获取板块成分股代码"

    try:

        logger.info(f"{info} ......")

        items = latest_data(payload=plate, data_type="plate")

        if isinstance(items, list):
            codes: list = [stock.coderename(i["secu_code"], restore=True) for i in items]
            codes.sort()
            logger.success(f"{info} [成功]")
            return codes

        logger.error(f"{info} [失败]")
        return None

    except Exception as e:
        logger.error(f"{info} [失败]")
        logger.exception(e)
        return None
