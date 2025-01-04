import math
import traceback
import ffmpeg
import os

def convert_audio_to_mp3(input_file, output_file):
    """
    将音频文件转换为 MP3 格式。

    :param input_file: 输入的音频文件路径
    :param output_file: 输出的 MP3 文件路径
    """
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file)
            .run(overwrite_output=True, quiet=True)
        )
    except Exception as e:
        print(f"转换 {input_file} 到 MP3 失败: {str(e)}")
        return False
    return True
def slice_mp3(input_file, output_dir, max_size_mb=10):
    """
    将 MP3 文件切片为多个大小上限为 max_size_mb 的文件。

    :param input_file: 输入的 MP3 文件路径
    :param output_dir: 输出目录
    :param max_size_mb: 每个切片的最大大小（MB）
    :return: 切片文件的列表
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取音频文件的总时长（秒）
    probe = ffmpeg.probe(input_file)
    duration = float(probe['format']['duration'])

    # 计算音频文件的总大小（字节）
    file_size = os.path.getsize(input_file)
    max_size_bytes = max_size_mb * 1024 * 1024

    # 计算需要切片的数量
    num_slices = math.ceil(file_size / max_size_bytes)

    # 计算每个切片的时间长度（秒）
    slice_duration = duration / num_slices

    # 切片并保存
    slices = []
    for i in range(num_slices):
        start_time = i * slice_duration
        end_time = start_time + slice_duration
        # 获取源文件名字
        input_file_name = os.path.basename(input_file)

        output_file = os.path.join(output_dir, f"{input_file_name}_slice_{i+1}.mp3")
        (
            ffmpeg
            .input(input_file, ss=start_time, to=end_time)
            .output(output_file)
            .run(overwrite_output=True, quiet=True)
        )
        slices.append(output_file)

    return slices
