# Bleeeeeefing Regularly

## 概要

Notionに書いた日次・週次BleeeeeefingをSlackに自動で投稿してくれるスクリプトです。

1. [インストール](#1-インストール)
2. [トークンなどの情報を取得](#2-トークンなどの情報を取得)
3. [実行](#3-実行)
4. [定期的に実行させる設定](#4-定期的に実行させる設定)

## 想定環境

- Python 3.8+
- Poetry 1.1.4+

## 1. インストール

```bash
$ git clone https://github.com/KindMaple/BleeeeeefingRegularly.git
$ cd BleeeeeefingRegularly
$ poetry install
```

## 2. トークンなどの情報を取得

以下の3つの情報が必要になります。

- Slack APIのOAuth Access Token
- NotionのToken
- Bleeeeeefing内容が書いてあるNotionページのURL

### Slack API

1. [slack api](https://api.slack.com/apps)にアクセス
2. `Create New App`をクリックして、`App Name`に任意の名前を入力し、`Development Slack Workspace`で導入したい先のワークスペースを選択
3. 遷移先ページ左側のメニューから`OAuth & Permissions`をクリック
4. `Add an OAuth Scope`をクリックし、`chat:write`を選択
5. ページトップの`Install to Workspace`をクリック
6. `許可する`をクリック
7. OAuth Access Tokenが表示されるのでコピー（"xoxp-"で始める文字列になっていることを確認してください。）
8. .envファイルに書き込む

### Notion Token

ブラウザのCookieから`token_v2`という名前に対応する値を取得します。

#### Chromeの場合

1. ブラウザ版Notionを開く
2. 右クリック→`検証`→`Application`→`Storage`→`Cookies`→`https://www.notion.so`→`token_v2`の値をコピー
3. .envファイルに書き込む

#### BleeeeeefingトップページのURL

ブラウザ上で開いたときのURLをそのままコピーして.envファイルに書き込みます。

## 3. 実行

```bash
# （初回のみ）テンプレートの作成
$ poetry run template
# 日次報告の場合
$ poetry run daily
# 週次報告の場合
$ poetry run weekly
```

!! テンプレートの作成と週次報告には5分程度かかります

## 4. 定期的に実行させる設定

### Linuxの場合

```bash
$ crontab -e
$ crontab -l
PJ_ROOT=/path/to/BleeeeeefingRegularly
POETRY=/path/to/poetry  # Try `which poetry`

# Bleeeeeefing
# 日次報告
59 23 * * * cd $PJ_ROOT && $POETRY run daily
# 週次報告
00 11 * * 5 cd $PJ_ROOT && $POETRY run weekly
```

### Windowsの場合

タスクスケジューラの「タスクの作成」から「操作」を指定
- プログラム/スクリプト → `/path/to/poetry`
- 引数の追加 → `poetry run daily (or weekly)`
- 開始 → `/path/to/BleeeeeefingRegularly`

「トリガー」に任意の時間を指定することで定期実行できます。