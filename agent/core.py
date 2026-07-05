import json
import traceback
from agent.llm import create_client
from agent.tools_registry import TOOL_DEFINITIONS, execute_tool
from config import MAX_TOOL_CALLS

SYSTEM_PROMPT = """你是一个专业的图片编辑助手。用户会用自然语言描述他们的图片编辑需求。

你可以使用提供的工具来编辑图片。请按照以下规则操作：

1. 仔细分析用户的需求，将其分解为一系列编辑步骤
2. 每个步骤调用一个合适的工具
3. 工具调用之间可以传递上一步的输出路径作为下一步的输入
4. 如果用户没有指定某些参数，使用合理的默认值
5. 处理完成后，用中文告诉用户做了什么操作

注意事项：
- 图片路径参数必须使用用户提供的准确路径，或上一步工具返回的输出路径
- 调整类操作（亮度、对比度等）的 factor 参数：1.0 为原始值，>1 增强，<1 减弱
- 坐标参数以像素为单位，从图片左上角(0,0)开始
- 如果用户说"稍微调亮一点"，factor 约 1.2；"明显调亮"约 1.5
- 如果用户说"裁剪成正方形"，取图片宽高较小值作为边长，从中心裁剪
- 如果用户说"加个水印"，默认放在右下角，半透明白色

请直接调用工具完成任务，不要只给建议。"""


class ImageEditAgent:
    def __init__(self):
        self.llm = create_client()
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def run(self, user_request: str, image_path: str | None = None) -> str:
        """执行一次图片编辑对话

        Args:
            user_request: 用户的自然语言编辑需求
            image_path: 可选的输入图片路径
        """
        if image_path:
            user_content = f"用户请求：{user_request}\n输入图片路径：{image_path}"
        else:
            user_content = f"用户请求：{user_request}"

        self.messages.append({"role": "user", "content": user_content})

        tool_call_count = 0
        last_result_path = None

        while tool_call_count < MAX_TOOL_CALLS:
            response = self.llm.chat(self.messages, TOOL_DEFINITIONS)

            if response.get("tool_calls"):
                self.messages.append({
                    "role": "assistant",
                    "content": response.get("content"),
                    "tool_calls": [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": json.dumps(tc["arguments"], ensure_ascii=False),
                            },
                        }
                        for tc in response["tool_calls"]
                    ],
                })

                for tc in response["tool_calls"]:
                    tool_name = tc["name"]
                    tool_args = tc["arguments"]

                    if "image_path" in tool_args and tool_args["image_path"] == "PREVIOUS_RESULT" and last_result_path:
                        tool_args["image_path"] = last_result_path

                    try:
                        result_path = execute_tool(tool_name, tool_args)
                        result_msg = f"工具 {tool_name} 执行成功，输出文件：{result_path}"
                        last_result_path = result_path
                    except Exception as e:
                        result_msg = f"工具 {tool_name} 执行失败：{str(e)}\n{traceback.format_exc()}"

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": result_msg,
                    })

                    tool_call_count += 1

            else:
                self.messages.append({
                    "role": "assistant",
                    "content": response["content"],
                })
                break

        if tool_call_count >= MAX_TOOL_CALLS:
            return "已达到最大工具调用次数限制，请简化您的请求。"

        return response.get("content", "处理完成")

    def reset(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]