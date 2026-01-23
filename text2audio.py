from gtts import gTTS
from pydub import AudioSegment
import os
import re
import tempfile
try:
    from pydub.playback import play
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("警告: pydub.playbackが使用できません。音声は再生されません。")

def text_to_speech(text):
    try:
        print(f"音声合成中: {text}")
        
        # テキストを言語ごとに分割
        segments = re.findall(r'[^\x00-\x7F]+|[\x00-\x7F]+', text)
        
        # 各セグメントを音声に変換して結合
        for segment in segments:
            if segment.strip():  # 空のセグメントを無視
                lang = 'ja' if re.search(r'[^\x00-\x7F]', segment) else 'en'
                
                # 一時ファイルを使用
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                    temp_filename = tmp_file.name
                
                try:
                    tts = gTTS(text=segment, lang=lang)
                    tts.save(temp_filename)
                    
                    if PYDUB_AVAILABLE:
                        try:
                            segment_audio = AudioSegment.from_mp3(temp_filename)
                            # 再生速度を変更 (1.2倍速)
                            if lang == 'ja':
                                tunning_speed = 1.2
                            else:
                                tunning_speed = 1.0
                            new_frame_rate = int(segment_audio.frame_rate * tunning_speed)
                            faster_audio = segment_audio._spawn(segment_audio.raw_data, overrides={'frame_rate': new_frame_rate})
                            faster_audio = faster_audio.set_frame_rate(segment_audio.frame_rate)
                            play(faster_audio)
                        except Exception as audio_error:
                            print(f"音声再生エラー: {audio_error}")
                            # シンプルなシステム音で代用
                            os.system(f'start "" "{temp_filename}"')
                    else:
                        # pydubが使えない場合はシステムのデフォルトプレイヤーで再生
                        os.system(f'start "" "{temp_filename}"')
                        
                except Exception as e:
                    print(f"音声合成エラー: {e}")
                finally:
                    # 一時ファイルを削除
                    try:
                        if os.path.exists(temp_filename):
                            os.unlink(temp_filename)
                    except:
                        pass
                        
    except Exception as e:
        print(f"音声出力エラー: {e}")


if __name__ == "__main__":
    # ユーザーからテキストデータを入力
    text = input("テキストを入力してください: ")
    text_to_speech(text)