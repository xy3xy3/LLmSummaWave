import os
import traceback

from openai import OpenAI

from utills import slice_mp3
from config import base_url, api_key, system_prompt, chat_model, whisper_model
class openaiApi:
    def __init__(self):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def audio2text(self, path, tmp_path, prompt="") -> tuple:
        #判断path存在
        if not os.path.exists(path):
            return None, f"{path}文件不存在"
        text, errmsg = self.whisper(path, tmp_path)
        if errmsg:
            return None, f"whisper失败{errmsg}"

        text, errmsg = self.chat(text, system_prompt)
        if errmsg:
            return None, f"chat失败{errmsg}"
        return text, errmsg

    def whisper(self, path, tmp_path) -> tuple:
        text = ""
        files = slice_mp3(path, tmp_path)
        if not files:
            print("切割音频失败")
            files = [path]
        for file in files:
            audio_file = open(file, "rb")
            if not audio_file:
                print("音频文件打开失败")
                continue
            try:
                response = self.client.audio.transcriptions.create(
                    file=audio_file,
                    model=whisper_model,
                )
                text = f"{text}{response.text}"
            except Exception as e:
                errmsg = f"whisper{str(e)}\n{traceback.format_exc()}"
                print(errmsg)
                return None, errmsg
        return text, ""

    def chat(self, user_prompt, system_prompt="") -> tuple:
        try:
            response = self.client.chat.completions.create(
                model=chat_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
            )
            print(f"转录前文本：{user_prompt}")
            return response.choices[0].message.content, ""
        except Exception as e:
            errmsg = f"{str(e)}\n{traceback.format_exc()}"
            print(errmsg)
            return None, errmsg

if __name__ == "__main__":
    api = openaiApi()
    path = ""
    tmp_path = ""
    text, errmsg = api.audio2text(path, tmp_path)
    print(text, errmsg)