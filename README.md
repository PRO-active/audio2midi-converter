# audio2midi-converter

このアプリはローカルで動き、MP3 や WAV 形式の音声ファイルを MIDI 形式に変換する、簡単な Streamlit アプリです。

### 概要

- このアプリは Google の magenta が開発した [MT3](https://github.com/magenta/mt3) というモデルのチェックポイントを利用して構築されています。
- Dockerfile を使用してイメージをビルドし、コンテナを実行することで起動します。

### 起動方法

1. Docker をインストールしてください。
2. ターミナルでプロジェクトのディレクトリに移動します。
3. 次のコマンドを実行して、Docker イメージをビルドします：
   ```
   docker build -t audio2midi .
   ```
4. 以下のコマンドを使用して、コンテナを実行します：
   ```
   docker run -p 8501:8501 audio2midi
   ```
5. ブラウザで `http://localhost:8501` にアクセスし、アプリを使用できます。

### 注意事項

- 現時点では、パッケージの関係で Windows でのみ動作します。
- アプリを実行するには、Docker が必要です。
