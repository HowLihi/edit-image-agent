import gradio as gr
from pathlib import Path
from agent.core import ImageEditAgent

agent = ImageEditAgent()


def process_image(user_request, image):
    if image is None:
        return "请先上传一张图片", None

    if isinstance(image, str):
        image_path = image
    else:
        image_path = image

    result = agent.run(user_request, image_path)

    output_files = sorted(Path("output").glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    output_path = str(output_files[0]) if output_files else None

    return result, output_path


def launch_ui(port: int = 7860):
    with gr.Blocks(
        title="图片编辑 AI Agent",
        theme=gr.themes.Soft(),
        css="""
        .main-container { max-width: 900px; margin: 0 auto; }
        .output-image { max-height: 500px; object-fit: contain; }
        """,
    ) as demo:
        gr.Markdown("""
        # 🎨 图片编辑 AI Agent

        用自然语言描述你的编辑需求，Agent 会智能调用工具完成编辑。

        **支持的操作：** 裁剪、缩放、旋转、翻转、格式转换、亮度/对比度/饱和度/锐度调整、
        模糊、黑白、复古滤镜、反色、边缘增强、浮雕、AI 抠图、添加文字、图片叠加、一键增强
        """)

        with gr.Row():
            with gr.Column(scale=1):
                input_image = gr.Image(
                    label="上传图片",
                    type="filepath",
                    height=300,
                )
                request_input = gr.Textbox(
                    label="编辑需求",
                    placeholder="例如：把这张图裁剪成正方形，调亮一点，加个复古滤镜",
                    lines=3,
                )
                with gr.Row():
                    submit_btn = gr.Button("🚀 开始编辑", variant="primary", size="lg")
                    reset_btn = gr.Button("🔄 重置对话", size="lg")

            with gr.Column(scale=1):
                output_text = gr.Textbox(
                    label="Agent 执行日志",
                    lines=10,
                    interactive=False,
                )
                output_image = gr.Image(
                    label="编辑结果",
                    type="filepath",
                    height=300,
                )

        gr.Examples(
            examples=[
                ["把图片裁剪成正方形", None],
                ["调亮一点，对比度增强一点，然后转成黑白", None],
                ["移除背景", None],
                ["加个水印'我的照片'在右下角", None],
                ["一键自动增强", None],
                ["添加复古棕褐色滤镜", None],
            ],
            inputs=[request_input, input_image],
            label="💡 试试这些示例",
        )

        submit_btn.click(
            fn=process_image,
            inputs=[request_input, input_image],
            outputs=[output_text, output_image],
        )

        reset_btn.click(
            fn=lambda: (agent.reset(), "", ""),
            outputs=[output_text, output_image],
        )

    demo.launch(server_port=port, share=False)
    print(f"\n🎨 Web UI 已启动: http://localhost:{port}")