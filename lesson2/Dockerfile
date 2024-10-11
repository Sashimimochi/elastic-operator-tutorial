# ベースイメージとしてPythonを使用
FROM python:3.11-slim

# Flaskをインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションのソースコードをコピー
COPY app.py /app/app.py

# 作業ディレクトリを設定
WORKDIR /app

# コンテナ起動時に実行するコマンド
CMD ["python", "app.py"]
