
# 感谢Linky小伙伴对于Windows版本运行说明以及代码的贡献!
from aip import AipSpeech
from playsound import playsound # windows环境下playsound运行可能不稳定
# pip install pygame
import pygame # 导入pygame，playsound报错或运行不稳定时直接使用
import pyttsx3
import asyncio
# pip install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk
import pyttsx3
from aip import AipSpeech
from edge_tts import Communicate
from playsound import playsound


class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def text_to_speech_and_play(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 5,  # 语速
            'vol': 5,  # 音量大小
            'per': 4  # 发声人 百度丫丫
        })  # 得到音频的二进制文件

        if not isinstance(result, dict):
            with open("./audio.mp3", "wb") as f:
                f.write(result)
        else:
            print("语音合成失败", result)
        # playsound('./audio.mp3')  # playsound无法运行时删去此行改用pygame，若正常运行择一即可
        self.play_audio_with_pygame('audio.mp3')  # 注意pygame只能识别mp3格式

    def play_audio_with_pygame(self, audio_file_path):
        # 代码来自Linky的贡献
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()


class Pyttsx3TTS:
    def __init__(self):
        pass

    def text_to_speech_and_play(self, text=""):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


class AzureTTS:
    def __init__(self, AZURE_API_KEY, AZURE_REGION):
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_REGION = AZURE_REGION
        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        # The language of the voice that speaks.
        self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaoyouNeural"
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config,
                                                              audio_config=self.audio_config)

    def text_to_speech_and_play(self, text):
        # Get text from the console and synthesize to the default speaker.
        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled:{}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details :{}".format(cancellation_details.error_details))
                    print("Didy you set the speech resource key and region values?")


class EdgeTTS:
    def __init__(self, voice: str = "zh-CN-XiaoyiNeural", rate: str = "+0%", volume: str = "+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume

    async def text_to_speech_and_play(self, text):
        # voices = await VoicesManager.create()
        # voice = voices.find(Gender="Female", Language="zh")
        # communicate = edge_tts.Communicate(text, random.choice(voice)["Name"])
        communicate = Communicate(text, self.voice)
        await communicate.save('./audio.wav')
        playsound('./audio.wav')


if __name__ == '__main__':
    # APP_ID = ''
    # API_KEY = ''
    # SECRET_KEY = ''
    # baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    # baidutts.text_to_speech_and_play('春天来了，每天的天气都很好！')
    #
    # pyttsx3tts = Pyttsx3TTS()
    # pyttsx3tts.text_to_speech_and_play('春天来了，每天的天气都很好！')
    #
    # AZURE_API_KEY = ""
    # AZURE_REGION = ""
    # azuretts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    # azuretts.text_to_speech_and_play("嗯，你好，我是你的智能小伙伴，我的名字叫Murphy，你可以和我畅所欲言，我是很会聊天的哦！")
    edgetts = EdgeTTS()
    asyncio.run(edgetts.text_to_speech_and_play(
        "嗯，你好，我是你的智能小伙伴，我的名字叫Murphy，你可以和我畅所欲言，我是很会聊天的哦！"))
