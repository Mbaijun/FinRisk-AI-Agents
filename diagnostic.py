import gradio as gr
import sys
import os
from datetime import datetime

print("=" * 60)
print("FinRisk AI Agents - 诊断模式")
print("=" * 60)
print(f"Python: {sys.version}")
print(f"Gradio: {gr.__version__}")
print(f"工作目录: {os.getcwd()}")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# 最简单的界面
def test_func(text):
    return f"✅ 收到: {text}"

# 创建极简界面
demo = gr.Interface(
    fn=test_func,
    inputs=gr.Textbox(label="测试输入"),
    outputs=gr.Textbox(label="测试输出"),
    title="FinRisk AI Agents - 诊断版",
    description="如果这个能运行，说明Gradio基础功能正常"
)

if __name__ == "__main__":
    print("🚀 启动诊断应用...")
    print("🌐 访问地址: http://localhost:7861")
    print("=" * 60)
    
    try:
        demo.launch(
            server_name="0.0.0.0",
            server_port=7861,  # 使用不同端口避免冲突
            share=False,
            show_error=True,
            quiet=False
        )
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
