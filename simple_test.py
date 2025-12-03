print('=' * 50)
print('FinRisk API Simple Test')
print('=' * 50)

# 测试基本导入
print('\n1. Testing basic imports...')
try:
    import sys
    print(f'Python: {sys.version}')
except:
    print('Error with sys')

# 测试FastAPI
print('\n2. Testing FastAPI...')
try:
    from fastapi import FastAPI
    print('✅ FastAPI import successful')
except Exception as e:
    print(f'❌ FastAPI import failed: {e}')

# 测试其他关键包
print('\n3. Testing other packages...')
packages = ['numpy', 'pandas', 'uvicorn']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except Exception as e:
        print(f'❌ {pkg}: {e}')

print('\n' + '=' * 50)
print('Test complete!')
print('=' * 50)

# 等待输入，防止窗口关闭
input('\nPress Enter to exit...')
