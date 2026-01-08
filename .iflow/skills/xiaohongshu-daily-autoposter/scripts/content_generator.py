"""
Content Generator for Xiaohongshu Daily Autoposter
Generates viral Xiaohongshu posts using proven patterns
"""

import random
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class ContentGenerator:
    """Generates viral Xiaohongshu content using proven patterns."""
    
    # 爆款标题模板库
    TITLE_TEMPLATES = {
        'contrast': [
            "你不{action}，绝对会后悔{reason}！",
            "别再{problem}了！{solution}才是正确姿势",
            "{problem}？{solution}一次性搞定",
            "曾经{problem}的我，现在竟然{solution}",
            "别说我没提醒你：{action}真的会上瘾"
        ],
        'numeric': [
            "{number}天{solution}，{result}！",
            "{number}个{method}，小白也能学会",
            "{number}分钟解决{problem}，亲测有效！",
            "{number}年经验总结：{action}就对了",
            "学会了这{number}点，{result}不是梦"
        ],
        'emotional': [
            "绝绝子！这个{method}真的救了我的{problem}",
            "救命！终于让我找到了{solution}",
            "太卷了！这样{action}简直逆天",
            "破防了！{result}竟然这么简单",
            "我不允许还有人不知道{method}"
        ],
        'authority': [
            "{expert}都在用的{method}，效果惊艳",
            "{famous}同款{solution}，{result}",
            "专业人士推荐的{action}方式",
            "{celebrity}都在做的{method}",
            "{brand}内部员工都在用的{method}"
        ],
        'howto': [
            "如何{solution}？这篇告诉你",
            "手把手教你{action}，{result}",
            "小白必看：{action}完整攻略",
            "{problem}怎么办？看这一篇就够了",
            "新手入门：{method}从零到一"
        ]
    }
    
    # 开头钩子模板
    OPENING_HOOKS = {
        'pain_point': [
            "你是否也有这样的困扰？",
            "有没有和我一样的姐妹？",
            "是不是每次都{problem}？",
            "说起{problem}，我真的太有发言权了",
            "如果你也{problem}，请继续看下去"
        ],
        'experience': [
            "作为一个{identity}，",
            "经历了{number}次失败后，",
            "{time}前，我的{problem}还是这样的...",
            "自从开始{action}后，",
            "花了我{number}个月总结出来的经验，"
        ],
        'numeric': [
            "3个月前，我还是一个{identity}，",
            "{number}万人都在看的{method}，",
            "{number}天时间，我竟然{solution}了！",
            "超过{number}人点赞的{method}分享给你",
            "{number}年{identity}的真实经历，"
        ],
        'question': [
            "你有没有想过，{question}？",
            "为什么别人能{result}，而你不行？",
            "如果我说{action}可以{solution}，你会信吗？",
            "有没有一种方法能{action}？",
            "为什么{number}个人里只有1个人知道{method}？"
        ]
    }
    
    # 爆款关键词
    VIRAL_KEYWORDS = [
        "绝绝子", "停止摆烂", "压箱底", "建议收藏", "好用到哭",
        "大数据", "教科书般", "小白必看", "宝藏", "神器",
        "都给我冲", "划重点", "笑不活了", "YYDS", "秘方",
        "我不允许", "停止摆烂", "上天在提醒你", "挑战全网",
        "手把手", "揭秘", "普通女生", "沉浸式", "有手就能做",
        "吹爆", "好用哭了", "搞钱必看", "狠狠搞钱", "打工人",
        "吐血整理", "家人们", "隐藏", "高级感", "治愈",
        "破防了", "万万没想到", "爆款", "永远可以相信", "被夸爆",
        "手残党必备", "正确姿势", "疯狂点赞", "超有料", "到碗里来",
        "小确幸", "老板娘哭了", "懂得都懂", "欲罢不能", "老司机"
    ]
    
    # 表情符号映射
    EMOJI_MAP = {
        'positive': ["✨", "💫", "🌟", "⭐", "🔥", "💥", "⚡", "🚀", "💪", "👑"],
        'neutral': ["📌", "📝", "💡", "🎯", "🎨", "💻", "📱", "📷", "🎬", "📚"],
        'action': ["👉", "👈", "👆", "👇", "🔄", "↗️", "↘️", "⬆️", "⬇️"],
        'emotional': ["❤️", "💕", "😍", "🥰", "🤩", "😊", "😉", " wink", "😎", "😏"]
    }
    
    # 话题标签模板
    HASHTAG_TEMPLATES = {
        '职场效率': ['#职场效率', '#工作效率', '#时间管理', '#职场干货', '#打工人'],
        '生活美学': ['#生活美学', '#氛围感', '#精致生活', '#生活仪式感', '#家居美学'],
        '学习成长': ['#学习成长', '#自我提升', '#终身学习', '#自律', '#个人成长'],
        '时间管理': ['#时间管理', '#效率工具', '#番茄工作法', '#GTD', '#高效生活'],
        '个人成长': ['#个人成长', '#自我成长', '#心理成长', '#认知提升', '#突破自我']
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize content generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.min_length = self.config.get('min_length', 300)
        self.max_length = self.config.get('max_length', 800)
        self.title_count = self.config.get('title_count', 5)
        self.template_style = self.config.get('templates', 'viral')
    
    def generate_title(self, topic: str, style: str = 'mixed') -> str:
        """
        Generate a viral title for the given topic.
        
        Args:
            topic: Content topic/keyword
            style: Title style (contrast, numeric, emotional, authority, howto, mixed)
            
        Returns:
            Generated title string
        """
        if style == 'mixed':
            style = random.choice(list(self.TITLE_TEMPLATES.keys()))
        
        templates = self.TITLE_TEMPLATES.get(style, self.TITLE_TEMPLATES['emotional'])
        template = random.choice(templates)
        
        # Generate context-specific placeholders
        context = self._generate_context(topic)
        
        # Fill in the template
        title = template.format(**context)
        
        # Add emoji
        emoji = random.choice(self.EMOJI_MAP['positive'])
        title = f"{emoji} {title}"
        
        # Ensure title is not too long
        if len(title) > 25:
            title = title[:24] + "..."
        
        return title
    
    def generate_title_variants(self, topic: str, count: int = None) -> List[str]:
        """
        Generate multiple title variants for A/B testing.
        
        Args:
            topic: Content topic
            count: Number of variants to generate
            
        Returns:
            List of title variants
        """
        count = count or self.title_count
        styles = list(self.TITLE_TEMPLATES.keys())
        variants = []
        
        for i in range(count):
            style = styles[i % len(styles)]
            title = self.generate_title(topic, style)
            variants.append(title)
        
        return variants
    
    def generate_opening(self, topic: str, style: str = 'pain_point') -> str:
        """
        Generate an engaging opening hook.
        
        Args:
            topic: Content topic
            style: Opening style (pain_point, experience, numeric, question)
            
        Returns:
            Generated opening paragraph
        """
        hooks = self.OPENING_HOOKS.get(style, self.OPENING_HOOKS['pain_point'])
        template = random.choice(hooks)
        context = self._generate_context(topic)
        
        opening = template.format(**context)
        
        # Add emoji at the beginning
        emoji = random.choice(self.EMOJI_MAP['neutral'])
        opening = f"{emoji} {opening}"
        
        return opening
    
    def generate_body(self, topic: str, opening: str = None, style: str = 'steps') -> str:
        """
        Generate main body content.
        
        Args:
            topic: Content topic
            opening: Pre-generated opening hook
            style: Body structure (steps, story, comparison)
            
        Returns:
            Generated body content
        """
        context = self._generate_context(topic)
        
        if style == 'steps':
            body = self._generate_steps_body(context)
        elif style == 'story':
            body = self._generate_story_body(context)
        elif style == 'comparison':
            body = self._generate_comparison_body(context)
        else:
            body = self._generate_steps_body(context)
        
        # Add emoji to body paragraphs
        body = self._add_emojis_to_body(body)
        
        # Ensure minimum length
        if len(body) < self.min_length:
            body += self._generate_additional_content(context)
        
        return body
    
    def _generate_steps_body(self, context: Dict) -> str:
        """Generate step-by-step body content."""
        steps = [
            "首先，我们需要了解{problem}的底层逻辑。",
            "其次，找到适合自己的{method}，这很关键。",
            "然后，制定一个可执行的行动计划。",
            "接着，按照计划坚持执行{number}天。",
            "最后，总结复盘，持续优化。"
        ]
        
        body_parts = []
        for i, step in enumerate(steps, 1):
            step_text = step.format(**context)
            emoji = random.choice(self.EMOJI_MAP['action'])
            body_parts.append(f"{emoji} {step_text}")
        
        return "\n\n".join(body_parts)
    
    def _generate_story_body(self, context: Dict) -> str:
        """Generate story-style body content."""
        story_parts = [
            "记得刚开始的时候，我对{problem}一无所知。",
            "尝试了很多方法，但效果都不理想。",
            "直到有一天，我发现了这个{method}。",
            "抱着试试看的心态，我坚持了{number}天。",
            "结果真的让我惊喜，{result}！",
            "现在把这个方法分享给同样困扰的你们。"
        ]
        
        body_parts = []
        for part in story_parts:
            emoji = random.choice(self.EMOJI_MAP['emotional'])
            body_parts.append(f"{emoji} {part.format(**context)}")
        
        return "\n\n".join(body_parts)
    
    def _generate_comparison_body(self, context: Dict) -> str:
        """Generate comparison-style body content."""
        comparison_parts = [
            "很多人在{problem}上有误区，认为{solution}很困难。",
            "但实际上，只要掌握正确的方法，{result}并不难。",
            "让我来告诉你正确的做法。",
            "对比一下，你就知道差距在哪里。",
            "选择大于努力，用对方法事半功倍。"
        ]
        
        body_parts = []
        for part in comparison_parts:
            emoji = random.choice(self.EMOJI_MAP['neutral'])
            body_parts.append(f"{emoji} {part.format(**context)}")
        
        return "\n\n".join(body_parts)
    
    def _generate_additional_content(self, context: Dict) -> str:
        """Generate additional content to meet length requirements."""
        tips = [
            f"💡 小贴士：{context.get('method', '这个方法')}需要坚持才能看到效果。",
            f"⭐ 坚持{number}天，你会感谢现在的自己。".format(number=random.randint(7, 30)),
            f"💪 相信自己，你一定可以{context.get('result', '做到')}！"
        ]
        return "\n\n" + "\n\n".join(random.sample(tips, min(2, len(tips))))
    
    def _add_emojis_to_body(self, body: str) -> str:
        """Add emojis to body content."""
        paragraphs = body.split('\n\n')
        enhanced_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                # Add emoji at start and end
                start_emoji = random.choice(self.EMOJI_MAP['positive'])
                end_emoji = random.choice(self.EMOJI_MAP['emotional'])
                enhanced_paragraphs.append(f"{start_emoji} {para.strip()} {end_emoji}")
        
        return "\n\n".join(enhanced_paragraphs)
    
    def generate_closing(self, topic: str, style: str = 'interactive') -> str:
        """
        Generate closing call-to-action.
        
        Args:
            topic: Content topic
            style: Closing style (interactive, challenge, teaser)
            
        Returns:
            Generated closing paragraph
        """
        closings = {
            'interactive': [
                "你们有遇到过类似的情况吗？评论区告诉我吧！",
                "大家还有什么好方法？一起交流一下！",
                "如果你觉得有用，记得点赞收藏哦~"
            ],
            'challenge': [
                "如果你也想要{result}，就从今天开始行动吧！",
                "坚持{number}天，改变看得见！加油！",
                "让我们一起成为更好的自己！"
            ],
            'teaser': [
                "下期分享更精彩的{method}，记得关注不迷路！",
                "更多干货内容，请持续关注~",
                "有问题可以私信我，我会一一回复的！"
            ]
        }
        
        selected_closings = closings.get(style, closings['interactive'])
        closing = random.choice(selected_closings)
        
        context = self._generate_context(topic)
        closing = closing.format(**context)
        
        emoji = random.choice(self.EMOJI_MAP['positive'])
        return f"{emoji} {closing}"
    
    def generate_hashtags(self, topic: str, count: int = 5) -> List[str]:
        """
        Generate relevant hashtags for the topic.
        
        Args:
            topic: Content topic
            count: Number of hashtags to generate
            
        Returns:
            List of hashtag strings
        """
        # Get base hashtags for topic
        base_tags = self.HASHTAG_TEMPLATES.get(topic, ['#小红书', '#爆款', '#干货分享'])
        
        # Add some viral hashtags
        viral_tags = random.sample(self.VIRAL_KEYWORDS, min(3, count - len(base_tags)))
        viral_hashtags = [f"#{tag}" for tag in viral_tags]
        
        # Combine and shuffle
        all_tags = base_tags + viral_hashtags
        random.shuffle(all_tags)
        
        return all_tags[:count]
    
    def generate_complete_post(self, topic: str, style: str = 'mixed') -> Dict[str, Any]:
        """
        Generate a complete Xiaohongshu post.
        
        Args:
            topic: Content topic
            style: Overall content style
            
        Returns:
            Dictionary containing all post components
        """
        # Generate title variants
        title_variants = self.generate_title_variants(topic, self.title_count)
        main_title = title_variants[0]
        
        # Generate content components
        opening_style = random.choice(list(self.OPENING_HOOKS.keys()))
        body_style = random.choice(['steps', 'story', 'comparison'])
        closing_style = random.choice(list(['interactive', 'challenge', 'teaser']))
        
        opening = self.generate_opening(topic, opening_style)
        body = self.generate_body(topic, opening, body_style)
        closing = self.generate_closing(topic, closing_style)
        
        # Combine body
        full_body = f"{opening}\n\n{body}\n\n{closing}"
        
        # Generate hashtags
        hashtags = self.generate_hashtags(topic)
        
        return {
            'title': main_title,
            'title_variants': title_variants,
            'body': full_body,
            'opening': opening,
            'closing': closing,
            'hashtags': hashtags,
            'topic': topic,
            'generated_at': datetime.now().isoformat(),
            'metadata': {
                'style': style,
                'body_style': body_style,
                'opening_style': opening_style,
                'closing_style': closing_style,
                'length': len(full_body)
            }
        }
    
    def _generate_context(self, topic: str) -> Dict[str, str]:
        """
        Generate context dictionary for template filling.
        
        Args:
            topic: Content topic
            
        Returns:
            Dictionary with context variables
        """
        # Define topic-specific context
        topic_contexts = {
            '职场效率': {
                'problem': '工作效率低',
                'solution': '提升效率',
                'method': '高效工作法',
                'result': '效率翻倍',
                'identity': '职场人',
                'action': '提升效率',
                'expert': '职场导师',
                'famous': '职场大神',
                'brand': '世界500强',
                'celebrity': '职场精英',
                'time': '1年前',
                'number': str(random.randint(3, 7))
            },
            '生活美学': {
                'problem': '生活太枯燥',
                'solution': '打造美学生活',
                'method': '生活美学技巧',
                'result': '生活更有品质',
                'identity': '生活家',
                'action': '提升生活品质',
                'expert': '美学专家',
                'famous': '生活博主',
                'brand': '无印良品',
                'celebrity': '文艺青年',
                'time': '半年前',
                'number': str(random.randint(5, 10))
            },
            '学习成长': {
                'problem': '学习没方法',
                'solution': '高效学习',
                'method': '学习技巧',
                'result': '成绩提升',
                'identity': '学习者',
                'action': '高效学习',
                'expert': '学习专家',
                'famous': '学霸',
                'brand': '知名高校',
                'celebrity': '高考状元',
                'time': '3个月前',
                'number': str(random.randint(3, 5))
            },
            '时间管理': {
                'problem': '时间不够用',
                'solution': '管理时间',
                'method': '时间管理术',
                'result': '时间自由',
                'identity': '忙碌族',
                'action': '管理时间',
                'expert': '时间管理大师',
                'famous': '效率达人',
                'brand': '知名咨询公司',
                'celebrity': '成功人士',
                'time': '2个月前',
                'number': str(random.randint(7, 21))
            },
            '个人成长': {
                'problem': '成长遇瓶颈',
                'solution': '突破自我',
                'method': '成长方法论',
                'result': '脱胎换骨',
                'identity': '追求者',
                'action': '突破自我',
                'expert': '成长教练',
                'famous': '成功学大师',
                'brand': '知名培训机构',
                'celebrity': '行业领袖',
                'time': '1年前',
                'number': str(random.randint(30, 90))
            }
        }
        
        # Get context for topic, or generate generic context
        if topic in topic_contexts:
            context = topic_contexts[topic].copy()
        else:
            context = {
                'problem': '遇到困难',
                'solution': '解决问题',
                'method': '实用方法',
                'result': '达成目标',
                'identity': '普通人',
                'action': '采取行动',
                'expert': '专业人士',
                'famous': '行业专家',
                'brand': '知名品牌',
                'celebrity': '知名人士',
                'time': '最近',
                'number': str(random.randint(3, 7))
            }
        
        # Add topic to context
        context['topic'] = topic
        
        return context
    
    def save_post(self, post: Dict[str, Any], output_dir: str = './output') -> Dict[str, str]:
        """
        Save generated post to files.
        
        Args:
            post: Generated post dictionary
            output_dir: Output directory path
            
        Returns:
            Dictionary with file paths
        """
        # Create output directory with date
        from datetime import datetime
        date_str = datetime.now().strftime('%Y-%m-%d')
        post_dir = Path(output_dir) / date_str
        post_dir.mkdir(parents=True, exist_ok=True)
        
        files = {}
        
        # Save main content
        content_path = post_dir / 'content.md'
        content = self._format_post_for_save(post)
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(content)
        files['content'] = str(content_path)
        
        # Save title variants
        if post.get('title_variants'):
            titles_path = post_dir / 'title_options.md'
            titles_content = self._format_titles_for_save(post['title_variants'])
            with open(titles_path, 'w', encoding='utf-8') as f:
                f.write(titles_content)
            files['titles'] = str(titles_path)
        
        # Save metadata
        metadata_path = post_dir / 'metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=2)
        files['metadata'] = str(metadata_path)
        
        return files
    
    def _format_post_for_save(self, post: Dict[str, Any]) -> str:
        """Format post for saving to markdown file."""
        lines = [
            f"# {post['title']}",
            "",
            "---",
            "",
            f"**话题**: {post['topic']}",
            f"**生成时间**: {post['generated_at']}",
            "",
            "---",
            "",
            "## 正文",
            "",
            post['body'],
            "",
            "## 话题标签",
            "",
            " ".join(post['hashtags']),
            "",
            "---",
            "",
            "## 标题变体（供选择）",
            "",
        ]
        
        for i, title in enumerate(post.get('title_variants', []), 1):
            lines.append(f"{i}. {title}")
        
        return "\n".join(lines)
    
    def _format_titles_for_save(self, titles: List[str]) -> str:
        """Format title variants for saving."""
        lines = [
            "# 可选标题",
            "",
            "以下是为您的内容生成的标题变体：",
            ""
        ]
        
        for i, title in enumerate(titles, 1):
            lines.append(f"## 选项 {i}")
            lines.append("")
            lines.append(title)
            lines.append("")
        
        return "\n".join(lines)
