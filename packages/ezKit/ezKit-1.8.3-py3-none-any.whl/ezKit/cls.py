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

    if not utils.v_true(target, str):
        logger.error(f"error type: {target}")
        return None

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

        if utils.v_true(df, bool) is False:
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
    payload: dict,
    end: str = "basic",
    data_type: str = "stock",
    df: bool = False
) -> dict | pd.DataFrame | None:
    """股票或板块的最新数据"""

    match True:
        case True if isinstance(payload, dict) is False:
            logger.error("Incorrect function argument type: payload")
            return None
        case True if isinstance(end, str) is False:
            logger.error("Incorrect function argument type: end")
            return None
        case True if isinstance(data_type, str) is False:
            logger.error("Incorrect function argument type: data_type")
            return None
        case _:
            pass

    info: str = "获取股票最新数据"

    if utils.v_true(data_type, str) is True and data_type == "plate":
        info = "获取板块最新数据"

    try:

        logger.info(f"{info} ......")

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}

        # https://x-quote.cls.cn/quote/stock/basic?secu_code={code}
        api = f"https://x-quote.cls.cn/quote/stock/{end}"

        if data_type == "plate":
            # https://x-quote.cls.cn/web_quote/plate/stocks?secu_code=cls80382
            # https://x-quote.cls.cn/web_quote/plate/stocks?secu_code={code}
            # https://x-quote.cls.cn/web_quote/plate/industry?secu_code={code}
            api = f"https://x-quote.cls.cn/web_quote/plate/{end}"

        # response = requests.get(api, headers=headers, timeout=10)
        response = requests.get(api, headers=headers, params=payload, timeout=10)

        response_dict: dict = response.json()

        if utils.v_true(df, bool) is False:
            logger.success(f"{info} [成功]")
            return response_dict

        if data_type == "plate" and utils.v_true(df, bool) is True:
            logger.error(f"{info} [错误]")
            return None

        if response_dict["data"]["trade_status"] == "STOPT":
            logger.error(f"{info} [停牌]")
            return None

        data_object = {
            # "date": [pd.to_datetime(date_today)],
            "open": [float(response_dict["data"]["open_px"])],
            "close": [float(response_dict["data"]["last_px"])],
            "high": [float(response_dict["data"]["high_px"])],
            "low": [float(response_dict["data"]["low_px"])],
            "volume": [int(response_dict["data"]["business_amount"])],
            "turnover": [float(response_dict["data"]["tr"])]
        }
        logger.success(f"{info} [成功]")
        return pd.DataFrame(data=data_object)

    except Exception as e:
        logger.error(f"{info} [失败]")
        logger.exception(e)
        return None
