import gradio as gr
import datetime

def echo(x):
    return f"[{datetime.datetime.now()}] 收到: {x}"

gr.Interface(
    fn=echo,
    inputs="text",
    outputs="text",
    title="FinRisk AI Agents - 极简版",
    description="测试Gradio是否工作"
).launch(server_name="0.0.0.0", server_port=7862, show_error=True)
