# proxy_server.py - 代理服务器绕过ngrok警告
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    # 添加header绕过ngrok警告
    headers = {
        'ngrok-skip-browser-warning': 'true',
        'User-Agent': 'Mozilla/5.0'
    }
    
    # 转发所有请求
    target_url = f'http://localhost:7860/{path}'
    
    if request.method == 'GET':
        resp = requests.get(target_url, headers=headers)
    elif request.method == 'POST':
        resp = requests.post(target_url, 
                            headers=headers, 
                            data=request.get_data(),
                            cookies=request.cookies)
    else:
        return 'Method not allowed', 405
    
    # 返回响应
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                       if name.lower() not in excluded_headers]
    
    response = Response(resp.content, resp.status_code, response_headers)
    return response

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PROXY_PORT', 8080))
    print(f"Proxy server running on http://localhost:{port}")
    print(f"Access via: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)