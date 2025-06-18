import os
from utills import slice_mp3, convert_audio_to_mp3
from api.openaiApi import openaiApi


def process_audio_files(audio_dir, res_dir, tmp_dir):
    """
    处理 audio 文件夹中的所有音频文件，将其转换为文本并保存到 res 文件夹中。

    :param audio_dir: 音频文件夹路径
    :param res_dir: 结果文件夹路径
    :param tmp_dir: 临时文件夹路径
    """
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    api = openaiApi()

    for filename in os.listdir(audio_dir):
        input_file = os.path.join(audio_dir, filename)
        if os.path.isfile(input_file):
            print(f"处理 {filename}...")
            # 转换音频文件为 MP3 格式
            output_file = os.path.join(tmp_dir, f"{os.path.splitext(filename)[0]}.mp3")
            if not convert_audio_to_mp3(input_file, output_file):
                print(f"转换 {filename} 失败")
                continue
            print(f"开始调用audio2text方法")
            # 调用 openaiApi 的 audio2text 方法
            text, errmsg = api.audio2text(output_file, tmp_dir)
            if errmsg:
                print(f"处理 {filename} 失败: {errmsg}")
                continue

            # 保存结果到 res 文件夹
            output_text_file = os.path.join(res_dir, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_text_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"成功处理 {filename}，结果保存到 {output_text_file}")

if __name__ == "__main__":
    audio_dir = "audio"
    res_dir = "res"
    tmp_dir = "tmp"

    process_audio_files(audio_dir, res_dir, tmp_dir)