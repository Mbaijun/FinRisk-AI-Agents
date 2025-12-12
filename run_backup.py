import os
import sys
import gradio as gr

# 【关键步骤】在导入 gradio 前，设置环境变量绕过可能的代理问题[citation:7]
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

def analyze(ticker):
    return f"分析请求: {ticker}。✅ Gradio 6.0.2 界面运行正常！"

# 【关键步骤】使用正确的 Gradio 6.x API 创建界面
with gr.Blocks(title="FinRisk AI Agents 测试版") as demo:
    gr.Markdown("# 🚀 FinRisk AI Agents 测试界面")
    input_box = gr.Textbox(label="输入股票代码", placeholder="例如：AAPL")
    output_box = gr.Textbox(label="分析结果")
    btn = gr.Button("分析")
    btn.click(fn=analyze, inputs=input_box, outputs=output_box)

if __name__ == "__main__":
    print("正在启动服务器...")
    # 尝试不同的端口，避免冲突[citation:4]
    try:
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False, inbrowser=True)
    except Exception as e:
        print(f"端口7860失败: {e}，尝试7865...")
        demo.launch(server_name="0.0.0.0", server_port=7865, share=False, inbrowser=True)