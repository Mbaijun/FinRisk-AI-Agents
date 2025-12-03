import warnings
warnings.filterwarnings('ignore')
import os
import random
import re
from typing import Dict, List, Any, Tuple

# 设置HuggingFace国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
print("🔧 已设置HuggingFace国内镜像")

# ==================== 模型加载部分 ====================
AI_AVAILABLE = False
sentiment_analyzer = None
MODEL_TYPE = ""

try:
    print("正在加载优化的情感分析系统...")
    from transformers import pipeline
    import torch
    
    # 使用金融模型
    model_name = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
    print(f"使用模型: {model_name}")
    
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=model_name,
        device=-1,
        truncation=True,
        max_length=512,
        top_k=3
    )
    
    MODEL_TYPE = "financial"
    print("✅ 金融情感分析模型加载成功")
    AI_AVAILABLE = True
    
except Exception as e:
    print(f"⚠️ 模型加载失败: {e}")
    AI_AVAILABLE = False

# ==================== 增强版规则匹配系统 ====================
class EnhancedRuleAnalyzer:
    """增强的基于规则的智能分析器（专门针对加密货币优化）"""
    
    def __init__(self):
        # 加密货币专用词典（更详细）
        self.crypto_positive_patterns = [
            # 价格相关
            (r'\b(break|突破|surge|soar|rally|moon|🚀)\b', 0.9),
            (r'\$[0-9,]+(\s*[kKmMbB])?\s*(high|record|新高|记录)', 0.85),
            (r'\b(bullish|牛市|看涨|上涨|uptrend)\b', 0.8),
            (r'\b(growth|增长|profit|盈利|gain|收益)\b', 0.75),
            
            # 情绪相关
            (r'\b(amazing|great|excellent|best|incredible|awesome)\b', 0.8),
            (r'\b(positive|optimistic|bullish|optimism)\b', 0.7),
            (r'🚀|📈|✅|🎯|🔥|💎', 1.0),  # 加密货币常用表情
            
            # 市场相关
            (r'\b(institution(al)?|机构|adoption|采用|adopt)\b', 0.7),
            (r'\b(ATH|all time high|历史新高)\b', 0.9),
            (r'\b(HODL|hold|持有|长期持有)\b', 0.6),
        ]
        
        self.crypto_negative_patterns = [
            # 价格相关
            (r'\b(crash|崩溃|暴跌|flash crash|闪崩|wipe out)\b', 0.95),
            (r'\b(drop|下跌|fall|decline|plummet| plunge)\b', 0.8),
            (r'\b(bearish|熊市|看跌|下跌|downtrend)\b', 0.8),
            (r'\b(loss|损失|亏损|rekt|liquidat(e|ion))\b', 0.85),
            
            # 风险相关
            (r'\b(warning|警告|alert|警报|caution|谨慎)\b', 0.7),
            (r'\b(risk|风险|danger|危险|concern|担忧)\b', 0.7),
            (r'\b(scam|骗局|fraud|欺诈|fake|假)\b', 0.9),
            (r'⚠️|📉|❌|💥|😱', 1.0),  # 负面表情
            
            # 监管相关
            (r'\b(regulat(e|ory|ion)|监管|SEC|禁令|ban)\b', 0.7),
            (r'\b(delay|推迟|reject|拒绝|uncertainty|不确定)\b', 0.65),
            (r'\b(FUD|fear|恐惧|恐慌|panic)\b', 0.8),
        ]
        
        self.crypto_neutral_patterns = [
            # 技术分析相关
            (r'\b(technical analysis|技术分析|TA|指标|indicator)\b', 0.8),
            (r'\b(consolidation|整理|横盘|sideways|range)\b', 0.7),
            (r'\b(support|支撑|resistance|阻力|level|水平)\b', 0.6),
            (r'📊|⚖️|📋|📐', 0.8),  # 中性表情
            
            # 市场状态
            (r'\b(stable|稳定|steady|平稳|flat|持平)\b', 0.7),
            (r'\b(volume|成交量|liquidity|流动性|流通性)\b', 0.5),
            (r'\b(mixed|混合|neutral|中性|balanced|平衡)\b', 0.8),
            
            # 一般描述
            (r'\b(analysis|分析|report|报告|update|更新)\b', 0.6),
            (r'\b(data|数据|statistics|统计|figure|数字)\b', 0.5),
            (r'\b(show|显示|indicate|表明|suggest|建议)\b', 0.4),
        ]
        
        # 特殊案例修正规则（针对已知的AI误判）
        self.correction_rules = [
            # 格式：如果文本包含X且AI说是Y，则修正为Z
            (r'🚀.*bullish', '负面', '正面'),  # 包含🚀和bullish不应是负面
            (r'warning.*🚀', '正面', '负面'),  # 包含warning和🚀可能是讽刺
            (r'analysis.*#', '正面', '中性'),   # 分析类带标签的通常是中性
        ]
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """使用增强规则分析单条文本"""
        text_lower = text.lower()
        
        # 初始化分数
        pos_score = 0
        neg_score = 0
        neu_score = 0
        
        # 计算正面分数
        for pattern, weight in self.crypto_positive_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                pos_score += weight * len(matches)
        
        # 计算负面分数
        for pattern, weight in self.crypto_negative_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                neg_score += weight * len(matches)
        
        # 计算中性分数
        for pattern, weight in self.crypto_neutral_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                neu_score += weight * len(matches)
        
        # 综合判断
        total_score = pos_score + neg_score + neu_score
        
        if total_score == 0:
            return '中性', 0.5 + random.random() * 0.2
        
        # 判断逻辑（考虑相对权重）
        pos_ratio = pos_score / total_score
        neg_ratio = neg_score / total_score
        neu_ratio = neu_score / total_score
        
        if neu_ratio > 0.5:
            # 中性特征占主导
            return '中性', 0.6 + neu_ratio * 0.3
        elif pos_ratio > neg_ratio:
            if pos_ratio > 0.6:
                return '正面', 0.7 + pos_ratio * 0.2
            else:
                return '正面', 0.6 + random.random() * 0.2
        elif neg_ratio > pos_ratio:
            if neg_ratio > 0.6:
                return '负面', 0.7 + neg_ratio * 0.2
            else:
                return '负面', 0.6 + random.random() * 0.2
        else:
            # 势均力敌
            return '中性', 0.5 + random.random() * 0.2
    
    def apply_corrections(self, text: str, ai_sentiment: str) -> str:
        """应用特殊修正规则"""
        for pattern, wrong_sentiment, correct_sentiment in self.correction_rules:
            if re.search(pattern, text, re.IGNORECASE) and ai_sentiment == wrong_sentiment:
                return correct_sentiment
        return ai_sentiment

# 初始化增强规则分析器
rule_analyzer = EnhancedRuleAnalyzer()

# ==================== AI分析函数 ====================
def analyze_with_ai(text_list: List[str]) -> List[Dict[str, Any]]:
    """使用AI模型分析文本"""
    try:
        results = sentiment_analyzer(text_list)
        analyzed = []
        
        for text, result in zip(text_list, results):
            if isinstance(result, list):
                top_result = result[0]
                label = top_result['label'].upper()
                score = top_result['score']
            else:
                label = result['label'].upper()
                score = result['score']
            
            # 应用特殊修正规则
            raw_sentiment = '正面' if 'POSITIVE' in label else '负面' if 'NEGATIVE' in label else '中性'
            corrected_sentiment = rule_analyzer.apply_corrections(text, raw_sentiment)
            
            analyzed.append({
                'text': text,
                'sentiment': corrected_sentiment,
                'confidence': round(score, 3),
                'source': f'AI模型({MODEL_TYPE})',
                'raw_ai_sentiment': raw_sentiment  # 记录原始AI判断
            })
        
        return analyzed
        
    except Exception as e:
        print(f"AI分析出错: {e}")
        return None

# ==================== 优化的混合智能分析 ====================
def hybrid_analyze_sentiments(tweet_dicts: List[Dict]) -> List[Dict]:
    """优化的混合智能分析：更智能的阈值和决策"""
    
    if not tweet_dicts:
        return []
    
    total = len(tweet_dicts)
    print(f"🤖 智能分析 {total} 条文本...")
    
    # 1. 首先使用AI分析
    if AI_AVAILABLE:
        print(f"✅ 使用{MODEL_TYPE}模型进行初步分析")
        texts = [tweet['text'] for tweet in tweet_dicts]
        ai_results = analyze_with_ai(texts)
        
        if ai_results:
            decision_stats = {'ai_high': 0, 'ai_low': 0, 'consistent': 0, 'conflict_rule': 0}
            
            for tweet, ai_result in zip(tweet_dicts, ai_results):
                ai_sentiment = ai_result['sentiment']
                ai_confidence = ai_result['confidence']
                raw_ai_sentiment = ai_result.get('raw_ai_sentiment', ai_sentiment)
                
                # 2. 同时使用规则分析
                rule_sentiment, rule_confidence = rule_analyzer.analyze(tweet['text'])
                
                # 3. 优化的智能决策逻辑
                # 调整阈值：金融模型通常过于自信，需要更保守
                if ai_confidence > 0.95 and ai_sentiment == rule_sentiment:
                    # 非常高置信度且一致：信任AI
                    final_sentiment = ai_sentiment
                    final_confidence = (ai_confidence + rule_confidence) / 2
                    decision_reason = "AI超高置信度且一致"
                    decision_stats['ai_high'] += 1
                elif ai_confidence < 0.7:
                    # 较低置信度：使用规则
                    final_sentiment = rule_sentiment
                    final_confidence = rule_confidence
                    decision_reason = "AI置信度较低，使用规则"
                    decision_stats['ai_low'] += 1
                elif ai_sentiment == rule_sentiment:
                    # 一致：采用（即使置信度不是特别高）
                    final_sentiment = ai_sentiment
                    final_confidence = (ai_confidence + rule_confidence) / 2
                    decision_reason = "AI与规则一致"
                    decision_stats['consistent'] += 1
                else:
                    # 冲突：优先规则（对加密货币更了解）
                    final_sentiment = rule_sentiment
                    final_confidence = rule_confidence
                    decision_reason = "AI与规则冲突，优先规则"
                    decision_stats['conflict_rule'] += 1
                
                # 存储结果
                tweet.update({
                    'sentiment': final_sentiment,
                    'confidence': round(final_confidence, 3),
                    'source': f'混合智能({decision_reason})',
                    'ai_sentiment': ai_sentiment,
                    'ai_confidence': ai_confidence,
                    'raw_ai_sentiment': raw_ai_sentiment,
                    'rule_sentiment': rule_sentiment,
                    'rule_confidence': rule_confidence,
                })
            
            print(f"✅ 混合智能分析完成")
            print(f"📊 决策统计: {decision_stats}")
            return tweet_dicts
    
    # 4. AI不可用：完全使用规则
    print("📝 AI不可用，使用规则匹配分析")
    for tweet in tweet_dicts:
        sentiment, confidence = rule_analyzer.analyze(tweet['text'])
        tweet.update({
            'sentiment': sentiment,
            'confidence': confidence,
            'source': '纯规则匹配'
        })
    
    return tweet_dicts

# ==================== 主分析函数 ====================
def analyze_sentiments(tweet_dicts: List[Dict]) -> List[Dict]:
    """主分析函数 - 使用优化的混合智能系统"""
    return hybrid_analyze_sentiments(tweet_dicts)

# ==================== 总结生成函数 ====================
def generate_summary(analyzed_tweets: List[Dict]) -> Tuple[str, Dict]:
    """生成详细的分析总结"""
    if not analyzed_tweets:
        return "暂无数据", {}
    
    total = len(analyzed_tweets)
    counts = {'正面': 0, '中性': 0, '负面': 0}
    
    for tweet in analyzed_tweets:
        sentiment = tweet.get('sentiment', '中性')
        counts[sentiment] += 1
    
    # 计算百分比
    percentages = {}
    for sentiment, count in counts.items():
        percentages[sentiment] = round(count / total * 100, 1)
    
    # 确定主要情绪
    dominant = max(counts, key=counts.get) if counts else '中性'
    
    # 简化的总结（保持与bot.py兼容）
    summary = f"""
    情绪分析总结（共 {total} 条数据）：
    • 正面情绪: {counts['正面']}条 ({percentages['正面']}%)
    • 中性情绪: {counts['中性']}条 ({percentages['中性']}%)
    • 负面情绪: {counts['负面']}条 ({percentages['负面']}%)
    
    整体市场情绪: {dominant}
    """
    
    return summary, counts

# ==================== 测试代码 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 优化版混合智能系统测试")
    print("=" * 60)
    
    # 专门测试之前有问题的案例
    test_cases = [
        ("DeFi platform review: 🚀 Bullish outlook #BTC #Crypto", "正面", "之前误判为负面"),
        ("Market crash warning! Very bad news for investors.", "负面", "明显负面"),
        ("Technical analysis shows consolidation pattern.", "中性", "技术分析"),
        ("Price surge but regulatory concerns remain.", "负面", "复杂负面"),
    ]
    
    test_data = [{'text': text} for text, _, _ in test_cases]
    
    print(f"测试 {len(test_data)} 个关键案例...")
    results = analyze_sentiments(test_data)
    
    print("\n📋 分析结果:")
    for i, (item, (text, expected, note)) in enumerate(zip(results, test_cases), 1):
        actual = item['sentiment']
        confidence = item['confidence']
        source = item['source']
        
        is_correct = "✅" if actual == expected else "❌"
        
        print(f"\n{i}. {note}")
        print(f"   文本: {text[:50]}...")
        print(f"   预期: {expected} | 实际: {actual} {is_correct}")
        print(f"   置信度: {confidence:.3f} | 方式: {source}")
        
        if 'ai_sentiment' in item:
            print(f"   AI原始: {item.get('raw_ai_sentiment', item['ai_sentiment'])} ({item['ai_confidence']:.3f})")
            print(f"   规则分析: {item['rule_sentiment']} ({item['rule_confidence']:.3f})")
