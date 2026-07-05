from PIL import Image
from pathlib import Path
from config import OUTPUT_DIR


def _load(path: str) -> Image.Image:
    return Image.open(path).convert("RGBA")


def _save(img: Image.Image, prefix: str = "result") -> str:
    out = OUTPUT_DIR / f"{prefix}_{_next_id()}.png"
    img.save(out)
    return str(out)


_counter = 0


def _next_id() -> int:
    global _counter
    _counter += 1
    return _counter


def crop(image_path: str, x: int, y: int, width: int, height: int) -> str:
    """裁剪图片

    Args:
        image_path: 输入图片路径
        x: 裁剪区域左上角 X 坐标
        y: 裁剪区域左上角 Y 坐标
        width: 裁剪宽度
        height: 裁剪高度
    """
    img = _load(image_path)
    result = img.crop((x, y, x + width, y + height))
    return _save(result, "crop")


def resize(image_path: str, width: int, height: int, maintain_aspect: bool = True) -> str:
    """调整图片尺寸

    Args:
        image_path: 输入图片路径
        width: 目标宽度
        height: 目标高度
        maintain_aspect: 是否保持宽高比，默认 True
    """
    img = _load(image_path)
    if maintain_aspect:
        img.thumbnail((width, height), Image.LANCZOS)
        return _save(img, "resize")

    result = img.resize((width, height), Image.LANCZOS)
    return _save(result, "resize")


def rotate(image_path: str, degrees: float, expand: bool = True) -> str:
    """旋转图片

    Args:
        image_path: 输入图片路径
        degrees: 旋转角度（正数顺时针）
        expand: 是否扩展画布以容纳完整图片，默认 True
    """
    img = _load(image_path)
    result = img.rotate(-degrees, expand=expand, resample=Image.BICUBIC)
    return _save(result, "rotate")


def flip(image_path: str, direction: str = "horizontal") -> str:
    """翻转图片

    Args:
        image_path: 输入图片路径
        direction: 翻转方向，'horizontal' 水平翻转，'vertical' 垂直翻转
    """
    img = _load(image_path)
    if direction == "horizontal":
        result = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        result = img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError(f"未知翻转方向: {direction}，可选 'horizontal' 或 'vertical'")
    return _save(result, "flip")


def convert_format(image_path: str, target_format: str) -> str:
    """转换图片格式

    Args:
        image_path: 输入图片路径
        target_format: 目标格式，如 'JPEG', 'PNG', 'WEBP', 'BMP'
    """
    img = _load(image_path)
    if target_format.upper() in ("JPEG", "JPG"):
        img = img.convert("RGB")
    out = OUTPUT_DIR / f"convert_{_next_id()}.{target_format.lower()}"
    img.save(out, format=target_format.upper())
    return str(out)