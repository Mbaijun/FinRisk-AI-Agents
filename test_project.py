#!/usr/bin/env python
"""
FinRisk-AI-Agents Project Integrity Test
"""
import os
import sys
import json
from pathlib import Path

print("=== FinRisk-AI-Agents Integrity Test ===")
print()

base_dir = Path(__file__).parent
print(f"Project Directory: {base_dir}")
print()

# 1. Check required files
print("1. Checking Required Files:")
print("-" * 40)

required_files = [
    ("README.md", "Project documentation"),
    ("requirements.txt", "Dependencies"),
    ("vercel.json", "Vercel config"),
    ("run.py", "Local entry point"),
    ("api/index.py", "Vercel entry"),
    ("api/main.py", "FastAPI app"),
    ("api/endpoints.py", "API endpoints"),
    ("utils/logger.py", "Logging util"),
]

all_ok = True
for file_name, desc in required_files:
    file_path = base_dir / file_name
    if file_path.exists():
        print(f"  [OK]  {file_name:25} - {desc}")
    else:
        print(f"  [FAIL] {file_name:25} - {desc} (MISSING)")
        all_ok = False

print()

# 2. Check Vercel config
print("2. Checking Vercel Configuration:")
print("-" * 40)

vercel_path = base_dir / "vercel.json"
if vercel_path.exists():
    try:
        with open(vercel_path, 'r') as f:
            config = json.load(f)
        
        # Check build config
        builds = config.get("builds", [])
        has_api_entry = False
        for build in builds:
            if build.get("src", "").endswith("api/index.py"):
                has_api_entry = True
                break
        
        if has_api_entry:
            print(f"  [OK]  Vercel config points to api/index.py")
        else:
            print(f"  [WARN] Vercel entry point may be incorrect")
            
        print(f"  [INFO] {len(builds)} build configs found")
        
    except Exception as e:
        print(f"  [FAIL] Vercel config error: {e}")
        all_ok = False
else:
    print(f"  [FAIL] vercel.json not found")
    all_ok = False

print()

# 3. Test imports
print("3. Testing Python Imports:")
print("-" * 40)

sys.path.insert(0, str(base_dir))

modules_to_test = [
    "api.main",
    "utils.logger",
    "api.endpoints",
]

for module in modules_to_test:
    try:
        __import__(module)
        print(f"  [OK]  {module}")
    except ImportError as e:
        print(f"  [FAIL] {module}: {e}")
        all_ok = False

print()

# 4. Summary
print("4. Test Summary:")
print("-" * 40)

if all_ok:
    print("  [SUCCESS] All tests passed!")
    print()
    print("  Next steps:")
    print("    1. Install dependencies: pip install -r requirements.txt")
    print("    2. Test locally: python run.py")
    print("    3. Deploy to Vercel: Push to GitHub and import in Vercel")
else:
    print("  [FAILURE] Some tests failed. Please fix the issues above.")
    print()
    print("  Common fixes:")
    print("    - Create missing files")
    print("    - Check vercel.json configuration")
    print("    - Install missing dependencies")

print("=" * 40)
