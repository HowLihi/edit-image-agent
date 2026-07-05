import tools
from tools.ai_generation import img2img, apply_style, txt2img

FUNCTION_MAP = {
    "crop": tools.crop,
    "resize": tools.resize,
    "rotate": tools.rotate,
    "flip": tools.flip,
    "convert_format": tools.convert_format,
    "adjust_brightness": tools.adjust_brightness,
    "adjust_contrast": tools.adjust_contrast,
    "adjust_saturation": tools.adjust_saturation,
    "adjust_sharpness": tools.adjust_sharpness,
    "blur": tools.blur,
    "grayscale": tools.grayscale,
    "sepia": tools.sepia,
    "invert": tools.invert,
    "edge_enhance": tools.edge_enhance,
    "emboss": tools.emboss,
    "remove_background": tools.remove_background,
    "add_text": tools.add_text,
    "composite_images": tools.composite_images,
    "auto_enhance": tools.auto_enhance,
    "img2img": img2img,
    "apply_style": apply_style,
    "txt2img": txt2img,
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "crop",
            "description": "裁剪图片到指定区域",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "x": {"type": "integer", "description": "裁剪区域左上角 X 坐标"},
                    "y": {"type": "integer", "description": "裁剪区域左上角 Y 坐标"},
                    "width": {"type": "integer", "description": "裁剪宽度（像素）"},
                    "height": {"type": "integer", "description": "裁剪高度（像素）"},
                },
                "required": ["image_path", "x", "y", "width", "height"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "resize",
            "description": "调整图片尺寸",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "width": {"type": "integer", "description": "目标宽度（像素）"},
                    "height": {"type": "integer", "description": "目标高度（像素）"},
                    "maintain_aspect": {"type": "boolean", "description": "是否保持宽高比，默认 true"},
                },
                "required": ["image_path", "width", "height"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rotate",
            "description": "旋转图片",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "degrees": {"type": "number", "description": "旋转角度（正数顺时针）"},
                    "expand": {"type": "boolean", "description": "是否扩展画布，默认 true"},
                },
                "required": ["image_path", "degrees"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "flip",
            "description": "翻转图片（水平或垂直）",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "direction": {
                        "type": "string",
                        "enum": ["horizontal", "vertical"],
                        "description": "翻转方向：horizontal 水平翻转，vertical 垂直翻转",
                    },
                },
                "required": ["image_path", "direction"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_format",
            "description": "转换图片格式（如 PNG 转 JPEG）",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "target_format": {
                        "type": "string",
                        "enum": ["JPEG", "PNG", "WEBP", "BMP"],
                        "description": "目标格式",
                    },
                },
                "required": ["image_path", "target_format"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_brightness",
            "description": "调整图片亮度",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "factor": {"type": "number", "description": "亮度因子，1.0 原始，>1 变亮，<1 变暗"},
                },
                "required": ["image_path", "factor"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_contrast",
            "description": "调整图片对比度",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "factor": {"type": "number", "description": "对比度因子，1.0 原始，>1 增强，<1 减弱"},
                },
                "required": ["image_path", "factor"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_saturation",
            "description": "调整图片饱和度",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "factor": {"type": "number", "description": "饱和度因子，1.0 原始，>1 增强，<1 减弱（0=黑白）"},
                },
                "required": ["image_path", "factor"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_sharpness",
            "description": "调整图片锐度",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "factor": {"type": "number", "description": "锐度因子，1.0 原始，>1 锐化，<1 模糊"},
                },
                "required": ["image_path", "factor"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "blur",
            "description": "对图片进行高斯模糊",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "radius": {"type": "number", "description": "模糊半径，默认 5.0，越大越模糊"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grayscale",
            "description": "将图片转为黑白灰度图",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sepia",
            "description": "添加复古棕褐色（老照片）滤镜",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "invert",
            "description": "反色处理（底片效果）",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edge_enhance",
            "description": "边缘增强滤镜",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "emboss",
            "description": "浮雕效果滤镜",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_background",
            "description": "移除图片背景（AI 抠图），返回透明背景 PNG",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_text",
            "description": "在图片上添加文字",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "text": {"type": "string", "description": "要添加的文字内容"},
                    "x": {"type": "integer", "description": "文字 X 坐标（position='custom' 时生效）"},
                    "y": {"type": "integer", "description": "文字 Y 坐标（position='custom' 时生效）"},
                    "font_size": {"type": "integer", "description": "字体大小，默认 32"},
                    "color": {"type": "string", "description": "文字颜色，默认 'white'"},
                    "position": {
                        "type": "string",
                        "enum": ["center", "top", "bottom", "top-left", "top-right", "bottom-left", "bottom-right", "custom"],
                        "description": "文字位置，默认 'center'",
                    },
                },
                "required": ["image_path", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "composite_images",
            "description": "将一张图片叠加到另一张图片上（如加水印、拼图）",
            "parameters": {
                "type": "object",
                "properties": {
                    "background_path": {"type": "string", "description": "背景图片路径"},
                    "overlay_path": {"type": "string", "description": "要叠加的图片路径"},
                    "x": {"type": "integer", "description": "X 坐标（position='custom' 时生效）"},
                    "y": {"type": "integer", "description": "Y 坐标（position='custom' 时生效）"},
                    "position": {
                        "type": "string",
                        "enum": ["center", "top-left", "top-right", "bottom-left", "bottom-right", "custom"],
                        "description": "叠加位置，默认 'center'",
                    },
                    "overlay_scale": {"type": "number", "description": "叠加图片缩放比例，默认 1.0"},
                },
                "required": ["background_path", "overlay_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "auto_enhance",
            "description": "一键自动增强图片（亮度、对比度、色彩、锐度综合优化）",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                },
                "required": ["image_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "img2img",
            "description": "AI 图生图：基于原图 + 文字描述，用 Stable Diffusion 生成新图片。可以改变风格、添加元素、调整画面。这是最核心的 AI 编辑能力。",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "prompt": {
                        "type": "string",
                        "description": "描述你想要的结果，英文效果更好。例如 'a cat wearing a hat, oil painting style'",
                    },
                    "strength": {
                        "type": "number",
                        "description": "变化强度，0.0=完全保留原图，1.0=完全忽略原图。风格迁移建议 0.6-0.75，微调建议 0.3-0.5",
                    },
                    "steps": {
                        "type": "integer",
                        "description": "推理步数，默认 20。Mac 上建议 15-25，越多质量越高但越慢",
                    },
                    "guidance_scale": {
                        "type": "number",
                        "description": "提示词遵循度，默认 7.5。越高越忠实于 prompt",
                    },
                },
                "required": ["image_path", "prompt"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_style",
            "description": "一键风格迁移：把图片变成指定艺术风格。可用风格：anime(动漫), oil_painting(油画), watercolor(水彩), sketch(素描), cyberpunk(赛博朋克), van_gogh(梵高), pixel_art(像素风), cartoon(3D卡通), realistic(写实), cinematic(电影感)",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "输入图片路径"},
                    "style": {
                        "type": "string",
                        "enum": ["anime", "oil_painting", "watercolor", "sketch", "cyberpunk", "van_gogh", "pixel_art", "cartoon", "realistic", "cinematic"],
                        "description": "目标风格",
                    },
                    "strength": {"type": "number", "description": "变化强度，默认 0.65"},
                    "steps": {"type": "integer", "description": "推理步数，默认 20"},
                },
                "required": ["image_path", "style"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "txt2img",
            "description": "AI 文生图：从纯文字描述生成图片。可用于创建素材、背景图等",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "描述你想要生成的图片，英文效果更好"},
                    "negative_prompt": {"type": "string", "description": "负向提示词，描述不想要的内容，如 'blurry, low quality'"},
                    "width": {"type": "integer", "description": "图片宽度，默认 512"},
                    "height": {"type": "integer", "description": "图片高度，默认 512"},
                    "steps": {"type": "integer", "description": "推理步数，默认 20"},
                    "guidance_scale": {"type": "number", "description": "提示词遵循度，默认 7.5"},
                },
                "required": ["prompt"],
            },
        },
    },
]


def execute_tool(name: str, arguments: dict) -> str:
    func = FUNCTION_MAP.get(name)
    if not func:
        raise ValueError(f"未知工具: {name}")
    return func(**arguments)