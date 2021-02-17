import datetime
import os

from dotenv import load_dotenv
from icecream import ic
from notion.block import PageBlock
from notion.client import NotionClient
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# .envファイルを読み込み、環境変数として扱う
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
SLACK_TOKEN = os.environ.get("OAuth_Access_Token")
NOTION_TOKEN = os.environ.get("token_v2")
TOP_PAGE_URL = os.environ.get("top_page")

# 各種サービスに接続するインスタンス
slack_client = WebClient(token=SLACK_TOKEN)
notion_client = NotionClient(token_v2=NOTION_TOKEN)

channel = "#bleeeeeefing"

today = datetime.date.today()

# Bleeeeeefingのページを管理しているトップページ
top_page = notion_client.get_block(TOP_PAGE_URL)


def str_to_date(date: str) -> datetime.date:
    """
    例) "20210214" → datetime.date(2021, 2, 14)
    """
    tdatetime = datetime.datetime.strptime(date, "%Y%m%d")
    return datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)


def title_contains_desired_date(child: PageBlock, target_date: datetime.date) -> bool:
    """
    child.titleは1週間を表す"20210212〜20210218"のような形式の文字列である。
    target_dateがこの週に含まれていればTrueを返す。
    """
    splitted_title = child.title.split("〜")
    if len(splitted_title) != 2:
        # "〜"で区切れなければ日付の形式をとったノートでないと判断して終了
        return False
    # タイトルに含まれている日付をdatetime.dateオブジェクトに変換
    week_begin, week_end = map(str_to_date, splitted_title)
    if week_begin <= target_date <= week_end:
        # 該当する週のブロックである
        return True
    return False


def to_pretty(content: list) -> list:
    """
    Slack投稿用に文字列を加工する
    """
    ret = []
    for line in content:
        if line in ["Done", "TODO", "Problems"]:
            # 見出し語はアスタリスクで囲う（Slackのボールド体はアスタリスク1つ）
            ret.append(f"*{line}*")
        else:
            # それ以外はリストの要素とする
            ret.append(f"• {line}")
    return ret


def fetch_page_content_by_date(date: datetime.date) -> str:
    """
    引数で指定した日付のBleeeeeefingページの内容を取得する
    """
    # 今週のサブページを取得
    this_week = [
        child for child in top_page.children if title_contains_desired_date(child, date)
    ][0]
    # 日毎のページを集約したコレクションを取得
    this_week_reports = [
        child
        for child in this_week.children
        if title_contains_desired_date(child, date)
    ][0]
    # 今日の日付のページを取得
    filter_params = {
        "filters": [
            {
                "property": "title",
                "filter": {
                    "operator": "string_is",
                    "value": {
                        "type": "exact",
                        "value": date.strftime("%Y%m%d"),
                    },
                },
            }
        ],
        "operator": "and",
    }
    today_report = this_week_reports.collection.query(filter=filter_params)[0]
    # 本文を抜き出して
    content = [child.title for child in today_report.children]
    # 文字列を加工する
    content = to_pretty(content)
    return content


def post_to_slack(content: str) -> None:
    """
    Slackのbleeeeeefingチャンネルに投稿する
    Copied from https://github.com/slackapi/python-slack-sdk#sending-a-message-to-slack
    """
    try:
        response = slack_client.chat_postMessage(channel=channel, text=content)
        assert response["message"]["text"] == content
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


def daily_bleeeeeefing() -> None:
    """
    日次報告
    """
    # 今日のBleeeeeefing内容
    contents = fetch_page_content_by_date(today)
    # 先頭に今日の日付を挿入
    contents.insert(0, today.strftime("%Y/%m/%d"))
    # Slackに投稿
    content = "\n".join(contents)
    post_to_slack(content)


def weekly_bleeeeeefing() -> None:
    """
    週次報告
    """
    print("Weekly Bleeeeeefing (not implemented)")


if __name__ == "__main__":
    ...
