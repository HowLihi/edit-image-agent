import torch
from PIL import Image
from pathlib import Path
from diffusers import StableDiffusionImg2ImgPipeline, StableDiffusionPipeline
from config import OUTPUT_DIR
from tools.basic import _load, _save

_model_cache = {}


def _get_device():
    return "cpu"


def _get_img2img_pipeline(model_id: str = "runwayml/stable-diffusion-v1-5"):
    cache_key = f"img2img_{model_id}"
    if cache_key not in _model_cache:
        print(f"⬇️  首次加载模型 {model_id}，约需下载 5GB，请耐心等待...")
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            safety_checker=None,
        )
        pipe = pipe.to(_get_device())
        _model_cache[cache_key] = pipe
        print("✅ 模型加载完成")
    return _model_cache[cache_key]


def _get_txt2img_pipeline(model_id: str = "runwayml/stable-diffusion-v1-5"):
    cache_key = f"txt2img_{model_id}"
    if cache_key not in _model_cache:
        print(f"⬇️  首次加载模型 {model_id}，约需下载 5GB，请耐心等待...")
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            safety_checker=None,
        )
        pipe = pipe.to(_get_device())
        _model_cache[cache_key] = pipe
        print("✅ 模型加载完成")
    return _model_cache[cache_key]


STYLE_PRESETS = {
    "anime": "anime style, studio ghibli, clean lines, vibrant colors",
    "oil_painting": "oil painting, textured brushstrokes, artistic, masterpiece",
    "watercolor": "watercolor painting, soft washes, delicate, artistic",
    "sketch": "pencil sketch, black and white, detailed linework, hand drawn",
    "cyberpunk": "cyberpunk style, neon lights, futuristic, high tech, blade runner aesthetic",
    "van_gogh": "Van Gogh style, impressionist, swirling brushstrokes, vibrant",
    "pixel_art": "pixel art, 8-bit, retro game style, blocky",
    "cartoon": "cartoon style, 3D render, Pixar style, cute, smooth",
    "realistic": "photorealistic, 8K, highly detailed, professional photography",
    "cinematic": "cinematic lighting, film grain, movie poster, dramatic",
}


def img2img(
    image_path: str,
    prompt: str,
    strength: float = 0.75,
    steps: int = 20,
    guidance_scale: float = 7.5,
    model_id: str = "runwayml/stable-diffusion-v1-5",
) -> str:
    """图生图：基于原图 + 文字描述生成新图片

    这是最核心的 AI 图片编辑能力，可以改变图片风格、添加元素、调整画面等。

    Args:
        image_path: 输入图片路径
        prompt: 描述你想要的结果（英文效果更好），例如 'a cat wearing a hat, cartoon style'
        strength: 变化强度，0.0=完全保留原图，1.0=完全忽略原图。默认 0.75
        steps: 推理步数，越多质量越高但越慢，默认 20（Mac 建议 15-25）
        guidance_scale: 提示词遵循度，越高越忠实于 prompt，默认 7.5
        model_id: 模型 ID，默认 'runwayml/stable-diffusion-v1-5'
    """
    pipe = _get_img2img_pipeline(model_id)

    init_image = Image.open(image_path).convert("RGB")
    w, h = init_image.size

    max_dim = 768
    if w > max_dim or h > max_dim:
        ratio = max_dim / max(w, h)
        init_image = init_image.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    if w % 8 != 0 or h % 8 != 0:
        new_w = (w // 8) * 8
        new_h = (h // 8) * 8
        init_image = init_image.resize((new_w, new_h), Image.LANCZOS)

    print(f"🎨 图生图生成中... prompt: {prompt}")
    print(f"   尺寸: {init_image.size}, strength: {strength}, steps: {steps}")

    with torch.no_grad():
        result = pipe(
            prompt=prompt,
            image=init_image,
            strength=strength,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
        ).images[0]

    return _save(result, "img2img")


def apply_style(
    image_path: str,
    style: str,
    strength: float = 0.65,
    steps: int = 20,
) -> str:
    """快速风格迁移：一键把图片变成指定风格

    Args:
        image_path: 输入图片路径
        style: 风格名称，可选：anime, oil_painting, watercolor, sketch, cyberpunk,
               van_gogh, pixel_art, cartoon, realistic, cinematic
        strength: 变化强度，0.0=保留原图，1.0=完全重绘。默认 0.65
        steps: 推理步数，默认 20
    """
    style_lower = style.lower().strip()
    if style_lower not in STYLE_PRESETS:
        available = ", ".join(STYLE_PRESETS.keys())
        raise ValueError(f"未知风格: {style}。可用风格: {available}")

    style_prompt = STYLE_PRESETS[style_lower]
    print(f"🎨 应用风格: {style} ({style_prompt})")

    return img2img(
        image_path=image_path,
        prompt=style_prompt,
        strength=strength,
        steps=steps,
    )


def custom_img2img(
    image_path: str,
    prompt: str,
    negative_prompt: str = "",
    strength: float = 0.75,
    steps: int = 20,
    guidance_scale: float = 7.5,
) -> str:
    """高级图生图：支持负向提示词，更精细控制

    Args:
        image_path: 输入图片路径
        prompt: 正向提示词，描述你想要的效果
        negative_prompt: 负向提示词，描述你不想要的内容，如 'blurry, low quality, distorted'
        strength: 变化强度，默认 0.75
        steps: 推理步数，默认 20
        guidance_scale: 提示词遵循度，默认 7.5
    """
    return img2img(
        image_path=image_path,
        prompt=prompt,
        strength=strength,
        steps=steps,
        guidance_scale=guidance_scale,
    )


def txt2img(
    prompt: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    steps: int = 20,
    guidance_scale: float = 7.5,
    model_id: str = "runwayml/stable-diffusion-v1-5",
) -> str:
    """文生图：从文字描述生成图片

    Args:
        prompt: 描述你想要生成的图片，如 'a beautiful sunset over mountains, oil painting'
        negative_prompt: 负向提示词，描述不想要的内容
        width: 图片宽度，默认 512（必须是 8 的倍数）
        height: 图片高度，默认 512（必须是 8 的倍数）
        steps: 推理步数，默认 20
        guidance_scale: 提示词遵循度，默认 7.5
        model_id: 模型 ID
    """
    pipe = _get_txt2img_pipeline(model_id)

    width = (width // 8) * 8
    height = (height // 8) * 8

    print(f"🖼️  文生图生成中... prompt: {prompt}")
    print(f"   尺寸: {width}x{height}, steps: {steps}")

    with torch.no_grad():
        result = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt or None,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
        ).images[0]

    return _save(result, "txt2img")