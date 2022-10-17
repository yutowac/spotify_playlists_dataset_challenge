# spotify_million_playlist_dataset_challenge

## フォルダ構成
./data以下：rawdataとpreprocessing後データ
./src以下：dashboardアプリとrecommendアプリ

## Dashboard
./srcでstreamlit run dashboard.pyを実行しlocalhostで確認

## Recommend
./srcでstreamlit run recommend.pyを実行しlocalhostで確認

### 設計思想
多腕バンディットをベースにして、独自のArmを設計

## Requirements
Docker環境参照

## Note
・データベースの設計はしていません。
・プロジェクトファイルを閲覧者の環境にダウンロードしてください。
・中間データはアップしていないので前処理が必要です。Google Colaboratoryなど高速処理の環境推奨です。
