# spotify_million_playlist_dataset_challenge  
  
## フォルダ構成  
### ./data以下  
  rawdata: 生データ、検証用にプレイリストファイルを減らしている  
  processed: 加工後データ  
### ./src以下  
  dashboard.py: streamlitのダッシュボードアプリ  
  recommend.py: streamlitのレコメンドアプリ  

## Dashboard  
  ./srcでstreamlit run dashboard.pyを実行。localhost(8501)で確認

## Recommend
  ./srcでstreamlit run recommend.pyを実行。localhost(8501)で確認

### 設計思想
  多腕バンディットをベースにして、独自にArmを設計。  
  ユーザーごとに後のArmの選択が最適化をできるだけ短い思考で見つけることを目的にした。
  
## Requirements  
  Dockerfile参照  
  python3.8  

## Note  
  ・データベースの設計はしていません。  
  ・全プレイリストで検証する場合はdatasetのzipをapp/data/rawに格納し、  
    app/src/preprocessing.pyで中間ファイルをつくる必要がある。   
