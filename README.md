# Voice Windows

画面上のテキストを読み上げるWindowsアプリケーション。日本語テキストを検出して、AIによる音声合成で読み上げます。

## 機能

- スクリーンショットからのテキスト抽出（OCR）
- 日本語文章の抽出と整形（Gemini API）
- 音声合成による読み上げ（VOICEVOX）
- キャプチャ領域の指定
- "ナリ"で終わる文章の自動検出と読み上げ

## 必要なもの

- Python 3.12以上
- VOICEVOX（ローカルで起動）
- Google Cloud Platformのアカウント（Gemini APIのため）

## セットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/keiichimochi/voice-windows.git
cd voice-windows
```

2. 仮想環境を作成して有効化
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. 依存パッケージをインストール
```bash
python -m pip install -r requirements.txt
```

4. 環境変数の設定
- `.env.sample`を`.env`にコピー
- 必要な情報を設定
  - `GEMINI_API_KEY`: Google Cloud PlatformのAPIキー
  - `AIVIS_API_URL`: VOICEVOXのエンドポイントURL
  - `AIVIS_SPEAKER_ID`: 使用する話者のID

5. VOICEVOXを起動
- VOICEVOXアプリケーションを起動し、APIサーバーを有効にする

6. アプリケーションを起動
```bash
python app.py
```

## 使い方

1. ブラウザで`http://localhost:5000`にアクセス
2. キャプチャ領域を設定（デフォルトは全画面）
3. 「スクリーンショットを取得」ボタンをクリック
4. 検出されたテキストが表示され、"ナリ"で終わる文章が自動的に読み上げられます

## 注意事項

- 初回起動時はEasyOCRのモデルダウンロードのため時間がかかります
- テキスト検出の精度は画面の解像度や文字の品質に依存します
- 音声合成にはVOICEVOXの起動が必要です 