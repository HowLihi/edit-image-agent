from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pathlib import Path
import io
from tools.basic import _load, _save
from config import OUTPUT_DIR


def remove_background(image_path: str) -> str:
    """移除图片背景（抠图），返回透明背景 PNG

    Args:
        image_path: 输入图片路径
    """
    try:
        from rembg import remove
        with open(image_path, "rb") as f:
            input_data = f.read()
        output_data = remove(input_data)
        out = OUTPUT_DIR / f"nobg_{_next_id()}.png"
        with open(out, "wb") as f:
            f.write(output_data)
        return str(out)
    except ImportError:
        raise ImportError("请安装 rembg: pip install rembg")


def add_text(
    image_path: str,
    text: str,
    x: int = 0,
    y: int = 0,
    font_size: int = 32,
    color: str = "white",
    position: str = "center",
) -> str:
    """在图片上添加文字

    Args:
        image_path: 输入图片路径
        text: 要添加的文字
        x: X 坐标（position='custom' 时生效）
        y: Y 坐标（position='custom' 时生效）
        font_size: 字体大小，默认 32
        color: 文字颜色，默认 'white'
        position: 文字位置，可选 'center', 'top', 'bottom', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'custom'
    """
    img = _load(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except (IOError, OSError):
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w, h = img.size

    positions = {
        "center": (w // 2 - tw // 2, h // 2 - th // 2),
        "top": (w // 2 - tw // 2, 20),
        "bottom": (w // 2 - tw // 2, h - th - 20),
        "top-left": (20, 20),
        "top-right": (w - tw - 20, 20),
        "bottom-left": (20, h - th - 20),
        "bottom-right": (w - tw - 20, h - th - 20),
        "custom": (x, y),
    }

    px, py = positions.get(position, positions["center"])
    draw.text((px, py), text, font=font, fill=color)
    result = Image.alpha_composite(img, overlay)
    return _save(result, "text")


def composite_images(
    background_path: str,
    overlay_path: str,
    x: int = 0,
    y: int = 0,
    position: str = "center",
    overlay_scale: float = 1.0,
) -> str:
    """将一张图片叠加到另一张图片上

    Args:
        background_path: 背景图片路径
        overlay_path: 要叠加的图片路径
        x: 叠加 X 坐标（position='custom' 时生效）
        y: 叠加 Y 坐标（position='custom' 时生效）
        position: 叠加位置，可选 'center', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'custom'
        overlay_scale: 叠加图片缩放比例，默认 1.0
    """
    bg = _load(background_path).convert("RGBA")
    overlay = _load(overlay_path).convert("RGBA")

    if overlay_scale != 1.0:
        nw = int(overlay.width * overlay_scale)
        nh = int(overlay.height * overlay_scale)
        overlay = overlay.resize((nw, nh), Image.LANCZOS)

    bw, bh = bg.size
    ow, oh = overlay.size

    positions = {
        "center": (bw // 2 - ow // 2, bh // 2 - oh // 2),
        "top-left": (0, 0),
        "top-right": (bw - ow, 0),
        "bottom-left": (0, bh - oh),
        "bottom-right": (bw - ow, bh - oh),
        "custom": (x, y),
    }

    px, py = positions.get(position, positions["center"])
    bg.paste(overlay, (px, py), overlay)
    return _save(bg, "composite")


def auto_enhance(image_path: str) -> str:
    """自动增强图片（亮度、对比度、色彩、锐度综合优化）

    Args:
        image_path: 输入图片路径
    """
    img = _load(image_path)

    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = ImageEnhance.Color(img).enhance(1.1)
    img = ImageEnhance.Sharpness(img).enhance(1.2)

    return _save(img, "enhance")


_counter = 0


def _next_id() -> int:
    global _counter
    _counter += 1
    return _counter