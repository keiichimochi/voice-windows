from flask import Flask, render_template, Response, request, jsonify
import pyautogui
import io
from PIL import Image
import time
import threading
import os
from dotenv import load_dotenv
import easyocr
import numpy as np
import google.generativeai as genai
import requests
import json
import base64
import pygame
import tempfile
import functools

load_dotenv()

# Gemini APIの設定
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Aivis Speech APIの設定
AIVIS_API_URL = os.getenv('AIVIS_API_URL', 'http://localhost:10101')
AIVIS_SPEAKER_ID = int(os.getenv('AIVIS_SPEAKER_ID', '488039072'))

# Pygameの初期化
pygame.mixer.init()

app = Flask(__name__)

# 画面サイズを取得
screen_width, screen_height = pyautogui.size()

# EasyOCRの初期化（初回の読み込みに時間がかかるので、起動時に初期化）
reader = easyocr.Reader(['ja', 'en'])

# 最新のスクリーンショットを保持する変数
latest_screenshot = None
latest_text = ""
screenshot_lock = threading.Lock()
text_lock = threading.Lock()

# キャプチャ領域の設定（デフォルト値を画面サイズに）
capture_region = {
    'left': 0,
    'top': 0,
    'width': screen_width,
    'height': screen_height
}

# 音声合成済みテキストを保持するセット
synthesized_history = set()

def should_synthesize(text):
    """音声合成すべきテキストかどうかを判定する"""
    # 改行を含むテキストを行ごとに分割して処理
    lines = text.strip().split('\n')
    # 各行をチェックして"ナリ"で終わる行があるか確認
    nari_lines = [line.strip() for line in lines if line.strip().endswith("ナリ")]
    
    # "ナリ"で終わる行があり、かつまだ合成していない場合のみTrue
    return len(nari_lines) > 0 and text not in synthesized_history

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"[DEBUG] 関数開始: {func.__name__}")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[DEBUG] 関数終了: {func.__name__}, 実行時間: {end_time - start_time:.2f}秒")
        return result
    return wrapper

@timing_decorator
def synthesize_speech(text):
    try:
        # 音声合成条件をチェック
        if not should_synthesize(text):
            print(f"[DEBUG] 音声合成をスキップ: {text}")
            return False
            
        print(f"[DEBUG] 音声合成開始: {text}")
        
        # audio_queryエンドポイントを呼び出し
        print("[DEBUG] audio_queryエンドポイントを呼び出し中...")
        query_response = requests.post(
            f"{AIVIS_API_URL}/audio_query",
            params={'text': text, 'speaker': AIVIS_SPEAKER_ID}
        )
        query_response.raise_for_status()
        query_data = query_response.json()
        print("[DEBUG] audio_query成功")

        # synthesisエンドポイントを呼び出し
        print("[DEBUG] synthesisエンドポイントを呼び出し中...")
        synthesis_response = requests.post(
            f"{AIVIS_API_URL}/synthesis",
            params={'speaker': AIVIS_SPEAKER_ID},
            json=query_data
        )
        synthesis_response.raise_for_status()
        print("[DEBUG] synthesis成功")

        # 音声データを一時ファイルに保存
        print("[DEBUG] 音声データを一時ファイルに保存中...")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file_path = temp_file.name
        temp_file.close()  # 明示的にファイルを閉じる
        
        with open(temp_file_path, 'wb') as f:
            f.write(synthesis_response.content)
        print(f"[DEBUG] 一時ファイル保存完了: {temp_file_path}")

        try:
            # 音声を再生
            print("[DEBUG] 音声再生開始...")
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()

            # 再生が終わるまで待機
            print("[DEBUG] 音声再生中...")
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            print("[DEBUG] 音声再生完了")
            
            # 再生完了後、少し待ってからファイルを削除
            time.sleep(0.5)
            
        finally:
            # 一時ファイルを削除
            try:
                print("[DEBUG] 一時ファイルを削除中...")
                pygame.mixer.music.unload()  # 明示的にアンロード
                os.unlink(temp_file_path)
                print("[DEBUG] 一時ファイル削除完了")
            except Exception as e:
                print(f"[WARNING] 一時ファイル削除に失敗: {e}")

        # 履歴に追加
        synthesized_history.add(text)
        print(f"[DEBUG] 合成履歴に追加: {text}")

        return True
    except Exception as e:
        print(f"[ERROR] 音声合成エラー: {str(e)}")
        print(f"[ERROR] エラーの詳細: {type(e).__name__}")
        if isinstance(e, requests.exceptions.RequestException):
            print(f"[ERROR] リクエストエラーの詳細: {e.response.text if hasattr(e, 'response') else 'レスポンスなし'}")
        return False

@timing_decorator
def extract_japanese_sentences(text):
    try:
        if not text.strip():
            print("[DEBUG] 入力テキストが空のため処理をスキップ")
            return ""
            
        print(f"[DEBUG] Gemini APIで日本語文章を抽出中... 入力テキスト: {text[:100]}...")
        prompt = f"""
以下のテキストから、"ナリ"で終わる日本語の文章のみを抽出してください。
"ナリ"で終わっていない文章は除外してください。
記号や単語のみ、英語の文章も除外してください。
抽出した文章は改行で区切って出力してください。

テキスト:
{text}
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        print(f"[DEBUG] 抽出された日本語文章: {text}")
        
        # 抽出したテキストを音声合成
        if text:
            print(f"[DEBUG] 音声合成を開始... テキスト: {text}")
            if synthesize_speech(text):
                print("[DEBUG] 音声合成が正常に完了")
            else:
                print("[DEBUG] 音声合成をスキップ")
        else:
            print("[DEBUG] 抽出されたテキストが空のため音声合成をスキップ")
            
        return text
    except Exception as e:
        print(f"[ERROR] Gemini APIエラー: {e}")
        return text

@timing_decorator
def extract_text_from_image(image):
    try:
        print("[DEBUG] 画像からテキスト抽出開始")
        
        # PIL ImageをNumPy配列に変換
        image_np = np.array(image)
        print("[DEBUG] 画像をNumPy配列に変換完了")
        
        # EasyOCRで日本語と英語のテキストを抽出
        print("[DEBUG] EasyOCRでテキスト抽出中...")
        results = reader.readtext(image_np)
        print(f"[DEBUG] EasyOCR抽出結果: {len(results)}件")
        
        # 日本語文字列のみを抽出
        japanese_texts = []
        for result in results:
            text = result[1]
            # 日本語が含まれているかチェック（ひらがな、カタカナ、漢字のいずれかを含む）
            if any(ord(char) in range(0x3040, 0x30FF) or ord(char) in range(0x4E00, 0x9FFF) for char in text):
                japanese_texts.append(text)
        print(f"[DEBUG] 日本語テキスト抽出結果: {len(japanese_texts)}件")
        
        # 抽出された日本語テキストを結合
        raw_text = '\n'.join(japanese_texts)
        print(f"[DEBUG] 抽出された生テキスト: {raw_text}")
        
        # Gemini APIで日本語文章を抽出
        text = extract_japanese_sentences(raw_text)
        
        print(f"[DEBUG] 最終的な抽出テキスト: {text}")
        return text
    except Exception as e:
        print(f"[ERROR] OCRエラー: {e}")
        return ""

@timing_decorator
def take_screenshot():
    try:
        print(f"[DEBUG] スクリーンショット取得開始 - 領域: {capture_region}")
        # 指定された領域のスクリーンショットを取得
        screenshot = pyautogui.screenshot(region=(
            capture_region['left'],
            capture_region['top'],
            capture_region['width'],
            capture_region['height']
        ))
        print("[DEBUG] スクリーンショット取得完了")
        
        # テキスト抽出
        print("[DEBUG] テキスト抽出処理開始")
        extracted_text = extract_text_from_image(screenshot)
        print("[DEBUG] テキスト抽出処理完了")
        
        # PILイメージをバイト列に変換
        print("[DEBUG] 画像をバイト列に変換中...")
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        print("[DEBUG] 画像変換完了")
        
        return screenshot, img_byte_arr, extracted_text
    except Exception as e:
        print(f"[ERROR] スクリーンショットエラー: {e}")
        return None, None, ""

@app.route('/')
def index():
    # 画面のサイズを取得
    screen_width, screen_height = pyautogui.size()
    return render_template('index.html', 
                         screen_width=screen_width,
                         screen_height=screen_height,
                         capture_region=capture_region)

@app.route('/update_region', methods=['POST'])
def update_region():
    global capture_region
    try:
        capture_region = {
            'left': int(request.form['left']),
            'top': int(request.form['top']),
            'width': int(request.form['width']),
            'height': int(request.form['height'])
        }
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400

@app.route('/capture', methods=['POST'])
def capture():
    global latest_screenshot, latest_text
    try:
        print("[DEBUG] /capture エンドポイント処理開始")
        _, img_bytes, text = take_screenshot()
        if img_bytes is None:
            print("[ERROR] スクリーンショット取得失敗")
            return {'status': 'error', 'message': 'Failed to capture screenshot'}, 500
            
        with screenshot_lock:
            latest_screenshot = img_bytes
        with text_lock:
            latest_text = text
            
        print(f"[DEBUG] 抽出されたテキスト: {text}")
        print("[DEBUG] /capture エンドポイント処理完了")
        return {'status': 'success', 'text': text}
    except Exception as e:
        print(f"[ERROR] キャプチャ処理エラー: {str(e)}")
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/screenshot')
def get_screenshot():
    global latest_screenshot
    with screenshot_lock:
        if latest_screenshot is None:
            return "No screenshot available", 404
        return Response(latest_screenshot, mimetype='image/png')

@app.route('/text')
def get_text():
    global latest_text
    with text_lock:
        return jsonify({'text': latest_text})

if __name__ == '__main__':
    print("EasyOCRを初期化中... しばらくお待ちください...")
    # Flaskアプリを起動
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 