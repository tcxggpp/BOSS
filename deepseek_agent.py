from openai import OpenAI
import json
client = OpenAI(
    api_key="APL",
    base_url="https://api.deepseek.com"
)
def get_weather(location):
    if "梧州" in location:
        return "梧州今天多云，气温 22 度，很适合去骑楼城吃龟苓膏。"
    else:
        return f"{location}的天气数据未获取到，但肯定没有梧州好。"
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：梧州",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

print("正在呼叫 DeepSeek 大脑思考中...\n")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "帮我查一下广西梧州现在的天气怎么样？"}
    ],
    tools=tools,
    tool_choice="auto",
)

message = response.choices[0].message
if message.tool_calls:
    print("[Agent 的决策]：DeepSeek 觉得需要调用外部工具！")
    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"-> 调用了工具: {function_name}")
        print(f"-> 提取的参数: {arguments}")
        if function_name == "get_weather":
            result = get_weather(arguments["location"])
            print(f"-> 工具返回结果: {result}")
else:
    print("[Agent 的决策]：大模型直接回答：", message.content)