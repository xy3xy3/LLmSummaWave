# LLmSummaWave

## 配置

需要配置`config.py`,默认使用硅基流动

```python
base_url = "https://api.siliconflow.cn/v1"
api_key = "你的key"
system_prompt = """你是一个善于改写文本的专家,该文本由音频转录而来,可能存在断句错误,不连贯的地方,词语错误
请改写为通顺的转录文本并直接输出改写结果"""
chat_model = "Qwen/Qwen2.5-7B-Instruct"
whisper_model = "FunAudioLLM/SenseVoiceSmall"
```

也可以尝试用思维链获取更好结果,不过目前没写自动提取,需要手动提取文本
```python
system_prompt = """你是一个善于改写文本的专家,该文本由音频转录而来,可能存在断句错误,不连贯的,词语拼写错误等问题.
文本背景:数字图像处理,老师期末复习总结
请改写为通顺的转录文本.你可以通过反思来判断需要怎么改写文本,最终把完整的文本放在代码块```````中
用户输入为转录的待处理音频
Let's think step by step."""
chat_model = "Qwen/QVQ-72B-Preview"
```

新用户走邀请链接注册免费获取14R余额:https://cloud.siliconflow.cn/i/eOWUQWuT

如果使用openai,请改`whisper`模型的名字和`gpt`模型的名字

## 使用

把音频放在`audio`文件夹,然后运行`main.py`,结果保存在`res.txt`