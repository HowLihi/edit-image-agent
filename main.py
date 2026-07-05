import argparse
import sys
from pathlib import Path
from agent.core import ImageEditAgent


def main():
    parser = argparse.ArgumentParser(
        description="图片编辑 AI Agent - 用自然语言编辑图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py -i photo.jpg "把图片裁剪成正方形，然后调亮一点"
  python main.py -i photo.jpg "把这张图转成黑白，加个复古滤镜"
  python main.py -i photo.jpg "移除背景"
  python main.py -i photo.jpg "加个水印'我的照片'在右下角"
  python main.py --web
        """,
    )
    parser.add_argument("request", nargs="?", help="自然语言编辑需求（使用 --web 时可选）")
    parser.add_argument("-i", "--image", help="输入图片路径")
    parser.add_argument("-w", "--web", action="store_true", help="启动 Web UI 界面")
    parser.add_argument("--port", type=int, default=7860, help="Web UI 端口，默认 7860")
    parser.add_argument("--reset", action="store_true", help="每次请求后重置对话上下文")

    args = parser.parse_args()

    if args.web:
        try:
            from ui.gradio_app import launch_ui
            launch_ui(port=args.port)
        except ImportError:
            print("请先安装 gradio: pip install gradio")
            sys.exit(1)
        return

    if not args.request:
        parser.print_help()
        return

    if args.image and not Path(args.image).exists():
        print(f"错误：图片文件不存在 - {args.image}")
        sys.exit(1)

    agent = ImageEditAgent()

    print(f"\n{'='*60}")
    print(f"  🎨 图片编辑 Agent")
    print(f"  📝 需求: {args.request}")
    if args.image:
        print(f"  🖼️  输入: {args.image}")
    print(f"{'='*60}\n")

    print("🤔 Agent 正在分析你的需求...\n")
    result = agent.run(args.request, args.image)
    print(f"\n✅ Agent 回复:\n{result}")

    if args.reset:
        agent.reset()


if __name__ == "__main__":
    main()