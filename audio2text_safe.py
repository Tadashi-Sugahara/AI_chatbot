"""
ALSA エラーを回避する音声入力モジュール
"""
import time
import random

def speech_to_text_dummy():
    """ダミー音声入力関数 - テスト用"""
    print("音声入力モード: 何か話してください...")
    time.sleep(2)  # 音声入力をシミュレート
    
    # デモ用のサンプル入力
    sample_inputs = [
        "今日の天気はどうですか？",
        "プログラミングについて教えて",
        "おすすめの本は？",
        "もういいや"
    ]
    
    # ランダムにサンプル入力を返す（デモ用）
    return random.choice(sample_inputs)

def speech_to_text_safe():
    """安全な音声入力 - エラー時はNoneを返す"""
    try:
        import speech_recognition as sr
        
        # recognizer と microphone オブジェクトを作成
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("音声入力待機中...")
            # ノイズ調整
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            # 音声録音 (タイムアウト10秒、フレーズ長20秒)
            audio = r.listen(source, timeout=10, phrase_time_limit=20)
            
            print("音声を認識中...")
            # Google音声認識を使用
            text = r.recognize_google(audio, language='ja-JP')
            return text
            
    except sr.UnknownValueError:
        print("音声を認識できませんでした")
        return None
    except sr.RequestError as e:
        print(f"音声認識サービスエラー: {e}")
        return None
    except sr.WaitTimeoutError:
        print("音声入力がタイムアウトしました")
        return None
    except Exception as e:
        print(f"音声入力エラー: {e}")
        return None

# 音声入力の実装を選択
speech_to_text = speech_to_text_safe  # 実際の音声認識を使用
# speech_to_text = speech_to_text_dummy  # デモ用ダミー関数を使用