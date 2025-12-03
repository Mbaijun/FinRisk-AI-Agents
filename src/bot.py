import yaml
import pandas as pd
from datetime import datetime
import os
import sys

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

print("=" * 60)
print("🧠 加密货币情绪分析机器人 v1.0")
print("=" * 60)

try:
    # 动态导入，便于调试
    from src.data_fetcher import fetch_recent_tweets
    from src.sentiment_analyzer import analyze_sentiments, generate_summary
    
    print("✅ 所有模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

def load_config():
    """从配置文件加载设置"""
    config_path = os.path.join(project_root, 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️  使用默认配置（读取配置文件失败: {e}）")
        return {"target_coin": "Bitcoin OR BTC", "tweet_count": 5}

def main():
    """主程序"""
    # 1. 加载配置
    config = load_config()
    query = config.get('target_coin', 'Bitcoin OR BTC')
    count = config.get('tweet_count', 5)
    
    print(f"📈 分析目标: {query}")
    print(f"📊 分析数量: {count}条")
    print("-" * 60)
    
    # 2. 获取数据
    print("🔄 正在获取数据...")
    tweets = fetch_recent_tweets(query, count)
    
    if not tweets:
        print("❌ 未获取到数据，程序退出")
        return
    
    print(f"✅ 成功获取 {len(tweets)} 条数据")
    
    # 3. 情感分析
    print("🤖 正在分析情绪...")
    analyzed_tweets = analyze_sentiments(tweets)
    
    # 4. 生成报告
    print("📊 生成分析报告...")
    summary, stats = generate_summary(analyzed_tweets)
    
    # 5. 输出结果
    print("\n" + "=" * 60)
    print("📋 情绪分析报告")
    print("=" * 60)
    print(summary)
    
    # 6. 显示示例（修复置信度显示）
    print("\n" + "=" * 60)
    print("🔍 数据示例")
    print("=" * 60)
    
    for i, tweet in enumerate(analyzed_tweets[:3], 1):
        text_preview = tweet.get('text', '')[:80] + "..." if len(tweet.get('text', '')) > 80 else tweet.get('text', '')
        confidence = tweet.get('confidence', 0)
        
        # 格式化置信度显示
        if confidence == 0:
            confidence_display = "N/A"
        else:
            confidence_display = f"{confidence:.3f}"
        
        print(f"{i}. {text_preview}")
        print(f"   情绪: {tweet.get('sentiment', '未知')} (置信度: {confidence_display})")
        print()
    
    print("=" * 60)
    print("🎯 分析完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
