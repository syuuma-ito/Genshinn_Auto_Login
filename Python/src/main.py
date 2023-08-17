import os
import sys

import requests

import logger

# =============================================
# ここは人によって変わる

# ログインボーナス受け取り画面のURLのact_idの値
ACT_ID = ""

# 以下はCookieから取得
# ~~_v2 でもOK (2023/08/15日 現在)
ltoken = ""
ltuid = ""
# =============================================

URL_GET_STATUS = "https://hk4e-api-os.hoyolab.com/event/sol/info"
URL_SIGN = "https://hk4e-api-os.hoyolab.com/event/sol/sign"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ja-Jp,ja;q=0.5",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "https://webstatic-sea.mihoyo.com",
    "Connection": "keep-alive",
    "Referer": f"https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id={ACT_ID}&lang=ja-jp",
}
params = (("lang", "ja-jp"), ("act_id", ACT_ID))
json = {"act_id": ACT_ID}
cookies = {
    "ltoken": ltoken,
    "ltuid": ltuid,
}
# 簡易的なロガーを設定
log = logger.logger()


def get_status():
    log.debug("Getting status...")
    response = requests.get(
        URL_GET_STATUS, headers=headers, params=params, cookies=cookies
    )

    res = response.json()
    log.debug(res)

    if res.get("data") is None:
        log.error("Cookieが間違っているか、URLが間違っています")
        log.error(f"サーバーからの情報 : {res['message']}")
        sys.exit()

    status = res["data"]
    log.debug(res["message"])
    log.info("=============================")
    log.info(f"今日:{status['today']}")
    log.info(f"ログイン日数:{status['total_sign_day']}")
    if status["is_sign"]:
        log.info("今日のログイン: [青]true[/]")
    else:
        log.info("今日のログイン: [赤]false[/]")
    log.info("=============================")

    return res["data"]


def sign():
    params = ("lang", "ja-jp")
    log.debug("Signing...")
    response = requests.post(
        URL_SIGN, headers=headers, params=params, cookies=cookies, json=json
    )
    res = response.json()
    log.debug(res)

    if res.get("data") is None:
        log.error("Cookieが間違っているか、URLが間違っています")
        log.error(f"サーバーからの情報 : {res['message']}")
        sys.exit()

    log.debug(res["message"])
    return res


if __name__ == "__main__":
    status = get_status()
    if status["is_sign"]:
        log.info("[青]ログインボーナスを受け取り済みです。[/]")
    else:
        log.info("[黄色]ログインボーナスを受け取ります。[/]")
        sign()
        log.info("[青]完了しました。[/]")
