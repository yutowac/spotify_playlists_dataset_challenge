# spotify_million_playlist_dataset_challenge  
  
## フォルダ構成  
### ./data/  
  1.raw: 生データ、検証用にプレイリストファイルを減らしている  
  2.processed: 加工後データ  
### ./src/  
  1.dashboard.py: streamlitのダッシュボードアプリ  
  2.recommend.py: streamlitのレコメンドアプリ  

## アプリケーション
### 1.Dashboard  
  ./srcでstreamlit run dashboard.pyを実行。localhost(8501)で確認

### 2.Recommend
  ./srcでstreamlit run recommend.pyを実行。localhost(8501)で確認

### 設計思想
  多腕バンディットをベースにして、独自に4つArmを設計。
    Arm1:その曲が含まれるプレイリスト群で最も出現頻度が高いトラック  
    Arm2:その曲の直後に配置されている最も出現頻度が高いトラック  
    Arm3:プレイリスト内で出現頻度が高いTop50トラックから選択されたトラック  
    Arm4:ランダムに選択されたトラック  
  ユーザーごとにArmの選択の最適化をできるだけ短い思考で見つけることを目的にした。
  納期の兼ね合いもあったのでジャストアイデア＋先行事例を参考にした。  
  イプシロンの学習は無しとした。
  
## Requirements  
  Dockerfile参照  
  python3.8  

## Note  
  ・データベースの設計はしていない。  
  ・全プレイリストで検証する場合はdatasetのzipをapp/data/rawに格納し、  
    app/src/preprocessing.pyで中間ファイルをつくる必要がある。
  ・整理されたコードより草案から早めに動作させることを優先した
