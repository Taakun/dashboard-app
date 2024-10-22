# dashborad-app

Dash + Plotly で作成した分析ダッシュボード

画像

## 概要
Dash + Plotly を使って分析ダッシュボードを作成しました。
また、Google Cloudを使用してデプロイしています。

- アプリケーションはこちら！
[URL](https://dash-app-229764408210.asia-northeast1.run.app)

## アプリケーションの構成
1. DockerfileをArtifact Registryにpushする。

2. pushしたDockerfileをCloud RunにPullする。これにより、userがアプリケーションにアクセス可能になる。

3. userがアプリケーションにアクセスした際には、BigQueryのAPIを使ってデータを取得している。

画像

## 前準備
- Docker Desktop がインストールされている。
- Google Cloud SDK がインストールされている。
- サービスアカウントのキーをダウンロードしてある。

## 環境構築方法

1. Google Cloud CLIでの設定
- gcloudの認証
Google Cloudに認証するために以下のコマンドを実行する

```
gcloud auth login
```

- プロジェクトの設定
使用するプロジェクトを設定する

```
gcloud config set project YOUR_PROJECT_ID
```

YOUR_PROJECT_IDは、使用するGoogle CloudプロジェクトのIDに置き換える。

- Docker認証の設定
Artifact Registryを使ってDockerを認証できるようにする。

```
gcloud auth configure-docker REGION-docker.pkg.dev
```

REGIONは、Artifact Registryリポジトリが作成されたリージョンに置き換える（例: us-central1）

3. Dockerイメージのビルド
ローカルでDockerイメージをビルドする。

Dockerfileのあるディレクトリで以下のコマンドを実行

```
docker-compose up -d --build
```

この時、以下のURLにアクセスすることで、ホストマシンのウェブブラウザからアクセスできる。

- http://127.0.0.1:8050

4. DockerイメージをArtifact Registryにタグ付け
ビルドしたDockerイメージをArtifact Registryにプッシュするために、リポジトリのURLでタグ付けする。

```
docker tag YOUR_IMAGE_NAME REGION-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPOSITORY_NAME/YOUR_IMAGE_NAME
```

5. DockerイメージをArtifact Registryにプッシュ

```
docker push REGION-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPOSITORY_NAME/YOUR_IMAGE_NAME
```

6. アプリケーションのデプロイ
Google Cloud Runを使用してデプロイする。

## 現状の課題と今後の展望
BigQueryからの読み込みが遅いことが挙げられます。

これは、複数のテーブルを同時に読み込んでいるためです。

そこで、データをjson形式で管理します。ここで、RFirestoreやealtime Databaseを使用することが想定されます。

これにより、読み込み速度を向上されることが期待されます。