from requests import *
from nonebot import on_message, on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-ollama",
    description="连接你的本地ollama模型",
    usage="@你的bot对话即可",
    type="application",
    config=Config,
    homepage="https://github.com/MaStAr1128/nonebot-plugin-ollama"
)

plugin_config = get_plugin_config(Config).ollama

messages = []

# 清空记录
ollamaClear = on_command(cmd="clear", priority=plugin_config.min_priority, block=True, rule=to_me())
@ollamaClear.handle()
async def ollamaClear_handle(bot=Bot, event=Event):
    messages.clear()
    await ollamaClear.send("System: 对话记录已清空.")

# 聊天
ollama = on_message(priority=plugin_config.min_priority+1, block=False, rule=to_me())
@ollama.handle()
async def ollama_handle(bot=Bot, event=Event):

    # 获取消息
    msg= str(event.get_message())
    # 判断是否为空
    if msg == '':
        await ollama.send("Warning: Empty message.")
    # 判断是否达到记录上限
    elif len(messages) >= 2 * plugin_config.max_histories:
        messages.clear()
        await ollama.send(f"Warning: 对话记录已达到{plugin_config.max_histories}条的上限，现已清空.")
    # 向ollama发送请求
    else:
        messages.append({
            "role": 'user',
            "content": msg,
        })

        parameters = {
            "model": plugin_config.model,
            "messages": messages,
            "stream": False,
        }

        response = post(plugin_config.url+'api/chat', json=parameters)
        if response.status_code == 200:
            await ollama.send(response.json()["message"]["content"])
            messages.append(response.json()["message"])
        else:
            await ollama.send(f"Error: {response.status_code}")