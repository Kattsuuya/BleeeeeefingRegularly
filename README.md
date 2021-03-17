# Bleeeeeefing Regularly

## 概要

Notionに書いた日次・週次BleeeeeefingをSlackに自動で投稿してくれるスクリプトです。

1. [レポジトリのフォーク](#1-レポジトリのフォーク)
2. [トークンなどの情報を取得](#2-トークンなどの情報を取得)
3. [実行](#3-実行)

## 1. レポジトリのフォーク

本ページの右上の`Fork`ボタンを押して、レポジトリをフォークしてください。

## 2. トークンなどの情報を取得

以下の3つの情報が必要になります。

- Slack APIのOAuth Access Token
- NotionのToken
- Bleeeeeefing内容が書いてあるNotionページのURL

取得した情報はフォークしたレポジトリのRepository secretsに追加します。

本ページ上部の`Settings`→`Secrets`→`New repository secret`ボタンから追加することができます。

### Slack API

1. [slack api](https://api.slack.com/apps)にアクセス
2. `Create New App`をクリックして、`App Name`に任意の名前を入力し、`Development Slack Workspace`で導入したい先のワークスペースを選択
3. 遷移先ページ左側のメニューから`OAuth & Permissions`をクリック
4. `Add an OAuth Scope`をクリックし、`chat:write`を選択
5. ページトップの`Install to Workspace`をクリック
6. `許可する`をクリック
7. OAuth Access Tokenが表示されるのでコピー（"xoxp-"で始める文字列になっていることを確認してください。）
8. `SLACK_TOKEN`という名前でsecretsに追加する

### Notion Token

ブラウザのCookieから`token_v2`という名前に対応する値を取得します。

#### Chromeの場合

1. ブラウザ版Notionを開く
2. 右クリック→`検証`→`Application`→`Storage`→`Cookies`→`https://www.notion.so`→`token_v2`の値をコピー
3. .envファイルに書き込む
4. `NOTION_TOKEN`という名前でsecretsに追加する

### BleeeeeefingトップページのURL

1. ブラウザ上で開いたときのURLをコピーする
2. `TOP_PAGE_URL`という名前でsecretsに追加する

## 3. 実行

### 日次報告

本ページ上部の`Actions`→`daily bleeeeeefing`→`Run workflow`で実行します。
初回はボタンを押した直後に1回実行されますが、以降は`.github/workflows/daily_cron.yml`に書いたルールに従って定期的に実行されます。

### 週次報告

本ページ上部の`Actions`→`weekly bleeeeeefing`→`Run workflow`で実行します。
初回はボタンを押した直後に1回実行されますが、以降は`.github/workflows/weekly_cron.yml`に書いたルールに従って定期的に実行されます。

週次報告をSlackに投稿した後、次週のNotionページが自動生成されます。

### （初回のみ）テンプレート作成

本ページ上部の`Actions`→`make template`→`Run workflow`で実行します。

**テンプレートの作成と週次報告には5分程度かかります。予めご了承ください。**
