# -*- coding: utf-8 -*-
import sys
print(f"Python路径: {sys.executable}")
print(f"Python版本: {sys.version}")

try:
    import fastapi
    print("✓ FastAPI 已安装")
except ImportError:
    print("✗ FastAPI 未安装")

try:
    import streamlit
    print("✓ Streamlit 已安装")
except ImportError:
    print("✗ Streamlit 未安装")

try:
    import pandas
    print("✓ Pandas 已安装")
except ImportError:
    print("✗ Pandas 未安装")

try:
    import numpy
    print("✓ NumPy 已安装")
except ImportError:
    print("✗ NumPy 未安装")
