from PIL import Image, ImageFilter, ImageOps
from tools.basic import _load, _save


def blur(image_path: str, radius: float = 5.0) -> str:
    """高斯模糊

    Args:
        image_path: 输入图片路径
        radius: 模糊半径，越大越模糊，默认 5.0
    """
    img = _load(image_path)
    result = img.filter(ImageFilter.GaussianBlur(radius=radius))
    return _save(result, "blur")


def grayscale(image_path: str) -> str:
    """转为黑白灰度图

    Args:
        image_path: 输入图片路径
    """
    img = _load(image_path)
    result = ImageOps.grayscale(img)
    return _save(result, "grayscale")


def sepia(image_path: str) -> str:
    """复古棕褐色滤镜

    Args:
        image_path: 输入图片路径
    """
    img = _load(image_path).convert("RGB")
    width, height = img.size
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            gray = int(r * 0.299 + g * 0.587 + b * 0.114)
            nr = min(int(gray * 1.2), 255)
            ng = min(int(gray * 0.95), 255)
            nb = min(int(gray * 0.7), 255)
            pixels[x, y] = (nr, ng, nb)

    return _save(img, "sepia")


def invert(image_path: str) -> str:
    """反色处理

    Args:
        image_path: 输入图片路径
    """
    img = _load(image_path)
    if img.mode == "RGBA":
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
        inverted = ImageOps.invert(rgb)
        r2, g2, b2 = inverted.split()
        result = Image.merge("RGBA", (r2, g2, b2, a))
    else:
        result = ImageOps.invert(img.convert("RGB"))
    return _save(result, "invert")


def edge_enhance(image_path: str) -> str:
    """边缘增强滤镜

    Args:
        image_path: 输入图片路径
    """
    img = _load(image_path)
    result = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return _save(result, "edge")


def emboss(image_path: str) -> str:
    """浮雕效果

    Args:
        image_path: 输入图片路径
    """
    img = _load(image_path)
    result = img.filter(ImageFilter.EMBOSS)
    return _save(result, "emboss")