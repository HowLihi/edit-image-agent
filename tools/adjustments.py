from PIL import Image, ImageEnhance
from tools.basic import _load, _save


def adjust_brightness(image_path: str, factor: float) -> str:
    """调整亮度

    Args:
        image_path: 输入图片路径
        factor: 亮度因子，1.0 为原始亮度，>1 变亮，<1 变暗
    """
    img = _load(image_path)
    enhancer = ImageEnhance.Brightness(img)
    result = enhancer.enhance(factor)
    return _save(result, "brightness")


def adjust_contrast(image_path: str, factor: float) -> str:
    """调整对比度

    Args:
        image_path: 输入图片路径
        factor: 对比度因子，1.0 为原始，>1 增强对比，<1 减弱对比
    """
    img = _load(image_path)
    enhancer = ImageEnhance.Contrast(img)
    result = enhancer.enhance(factor)
    return _save(result, "contrast")


def adjust_saturation(image_path: str, factor: float) -> str:
    """调整饱和度

    Args:
        image_path: 输入图片路径
        factor: 饱和度因子，1.0 为原始，>1 增强，<1 减弱（0 为黑白）
    """
    img = _load(image_path)
    enhancer = ImageEnhance.Color(img)
    result = enhancer.enhance(factor)
    return _save(result, "saturation")


def adjust_sharpness(image_path: str, factor: float) -> str:
    """调整锐度

    Args:
        image_path: 输入图片路径
        factor: 锐度因子，1.0 为原始，>1 更锐利，<1 更模糊
    """
    img = _load(image_path)
    enhancer = ImageEnhance.Sharpness(img)
    result = enhancer.enhance(factor)
    return _save(result, "sharpness")