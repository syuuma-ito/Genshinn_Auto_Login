// =============================================
// ここは人によって変わる

// ログインボーナス受け取り画面のURLのact_idの値
const ACT_ID = "";

// 以下はCookieから取得
// ~~_v2 でもOK (2023/08/15日 現在)
const cookies = "";

// =============================================

const sign_url = `https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=ja-jp&act_id=${ACT_ID}`;
const status_url = `https://sg-hk4e-api.hoyolab.com/event/sol/info?lang=ja-jp&act_id=${ACT_ID}`;
const header = {
    Cookie: cookies,
    Accept: "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    Connection: "keep-alive",
    "x-rpc-app_version": "2.34.1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "x-rpc-client_type": "4",
    Referer: "https://act.hoyolab.com/",
    Origin: "https://act.hoyolab.com",
};

function main() {
    const status = getStatus();

    if (status.data === null) {
        console.log(status);
        throw new Error(`エラー : ${status.message}`);
    }
    if (status.data.is_sign) {
        console.log("ログインボーナスを受け取り済みです。");
    } else {
        console.log("ログインボーナスを受け取ります");
        const response = autoSign();
        console.log(response);
        console.log(response.message);
        if (response.data?.gt_result?.is_risk) {
            throw new Error("CAPTCHAによってブロックされました");
        }
        console.log("受け取りました");
    }
}

function getStatus() {
    const options = {
        method: "GET",
        headers: header,
        muteHttpExceptions: true,
    };

    const httpResponses = UrlFetchApp.fetch(status_url, options);
    const response = JSON.parse(httpResponses.getContentText());
    return response;
}

function autoSign() {
    const options = {
        method: "POST",
        headers: header,
        muteHttpExceptions: true,
    };

    const httpResponses = UrlFetchApp.fetch(sign_url, options);
    const response = JSON.parse(httpResponses.getContentText());
    return response;
}
