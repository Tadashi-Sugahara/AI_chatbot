import speech_recognition as sr
import sys

def speech_to_text():
    try:
        # Create a recognizer object
        r = sr.Recognizer()

        # マイクが利用可能かチェック
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                print("エラー: マイクロホンが見つかりません")
                return "マイクロホンが見つかりません"
        except Exception as e:
            print(f"マイクロホンチェックエラー: {e}")

        # Capture audio from the microphone
        # マイクから音声を取得
        audio = None
        try:
            with sr.Microphone() as source:
                print("何か話してください！")
                # ノイズの調整
                r.adjust_for_ambient_noise(source, duration=1)
                # タイムアウトとフレーズの終了を検出するためのパラメータを設定
                audio = r.listen(source, timeout=20, phrase_time_limit=15)
                print("音声が正常にキャプチャされました。")
        except sr.WaitTimeoutError:
            print("タイムアウト: 音声の待機時間が終了しました")
            return "音声の待機がタイムアウトしました"
        except sr.RequestError as e:
            print(f"音声認識サービスエラー: {e}")
            return "音声認識サービスエラーが発生しました"
        except Exception as e:
            print(f"音声キャプチャエラー: {e}")
            return "音声取得中にエラーが発生しました"

        # Convert speech to text
        if audio is None:
            return "音声データが取得できませんでした"
        
        try:
            print("音声をテキストに変換中...")
            text = r.recognize_google(audio, language="ja-JP")
            print(f"認識されたテキスト: {text}")
            return text
        except sr.UnknownValueError:
            print("音声を認識できませんでした")
            return "音声を認識できませんでした"
        except sr.RequestError as e:
            print(f"サービスエラー: {str(e)}")
            return f"サービスエラー: {str(e)}"
        except Exception as e:
            print(f"予期しないエラー: {str(e)}")
            return f"予期しないエラー: {str(e)}"
            
    except Exception as e:
        print(f"音声認識初期化エラー: {e}")
        return f"音声認識初期化エラー: {e}"
        return "音声認識エラーが発生しました"

if __name__ == "__main__":
    text = speech_to_text()
    print("Recognized text:", text)