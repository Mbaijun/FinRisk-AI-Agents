import sys
import subprocess
import os

def check_and_install():
    """检查并安装缺失的包"""
    packages = [
        "fastapi",
        "uvicorn", 
        "pandas",
        "numpy",
        "plotly",
        "scipy",
        "requests",
        "pydantic"
    ]
    
    print("Checking dependencies...")
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(f"   ✅ {package} installed")
            except:
                print(f"   ❌ Failed to install {package}")
    
    print("\nTesting complete_api...")
    try:
        import complete_api
        print("✅ complete_api can be imported")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def create_simple_api():
    """创建一个简化版的API"""
    simple_code = '''from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI(title="FinRisk Simple API", version="1.0")

@app.get("/")
def root():
    return {"service": "FinRisk", "status": "running", "time": datetime.now().isoformat()}

@app.get("/health")
def health():
    return {"status": "healthy", "time": datetime.now().isoformat()}

@app.get("/stocks")
def stocks():
    return {"stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]}

if __name__ == "__main__":
    print("Starting FinRisk Simple API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open("simple_fixed_api.py", "w", encoding="utf-8") as f:
        f.write(simple_code)
    
    print("Created simple_fixed_api.py")
    return "simple_fixed_api.py"

if __name__ == "__main__":
    print("=" * 50)
    print("FinRisk API Fix Tool")
    print("=" * 50)
    
    if check_and_install():
        print("\n✅ Dependencies OK, trying to run complete_api...")
        try:
            import complete_api
            print("complete_api imported successfully!")
            
            # 尝试运行
            print("\nTrying to run complete_api...")
            import subprocess
            subprocess.run([sys.executable, "complete_api.py"])
        except Exception as e:
            print(f"\n❌ Error running complete_api: {e}")
            print("\nCreating simple API instead...")
            simple_file = create_simple_api()
            print(f"\nRun: python {simple_file}")
    else:
        print("\nCreating simple API...")
        simple_file = create_simple_api()
        print(f"\nRun: python {simple_file}")
    
    print("\n" + "=" * 50)
