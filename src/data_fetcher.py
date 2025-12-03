import random
from datetime import datetime, timedelta

def generate_mock_tweet():
    """生成模拟推文"""
    topics = [
        "Bitcoin price analysis",
        "Ethereum network upgrade", 
        "Crypto market trends",
        "DeFi platform review",
        "NFT market update"
    ]
    
    sentiments = [
        ("positive", "🚀 Bullish outlook", ["#BTC", "#Crypto"]),
        ("negative", "⚠️ Market concerns", ["#Trading", "#Warning"]),
        ("neutral", "📊 Technical analysis", ["#Analysis", "#Data"])
    ]
    
    topic = random.choice(topics)
    sentiment, text, tags = random.choice(sentiments)
    
    full_text = f"{topic}: {text} {' '.join(tags)}"
    
    return {
        'text': full_text,
        'created_at': (datetime.utcnow() - timedelta(hours=random.randint(0, 72))).isoformat() + 'Z',
        'like_count': random.randint(10, 1000),
        'retweet_count': random.randint(1, 200)
    }

def fetch_recent_tweets(query, max_results=5):
    """获取模拟数据"""
    print(f"🔍 模拟搜索: {query}")
    print(f"📊 生成 {max_results} 条模拟数据...")
    
    tweets = []
    for i in range(max_results):
        tweets.append(generate_mock_tweet())
    
    print(f"✅ 数据准备完成")
    return tweets

if __name__ == "__main__":
    # 测试
    test_data = fetch_recent_tweets("Bitcoin", 2)
    for i, tweet in enumerate(test_data):
        print(f"{i+1}: {tweet['text']}")
