#!/usr/bin/env python3
"""
Xiaohongshu Daily Autoposter - Main Entry Point
Automated daily content generation and posting for Xiaohongshu
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_loader import get_config, Config
from content_generator import ContentGenerator
from image_generator import ImageGenerator
from scheduler import Scheduler, ContentCalendar


class Autoposter:
    """Main autoposter orchestrator."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize autoposter.
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config = get_config(config_path)
        self.content_gen = ContentGenerator(self.config.content)
        self.image_gen = ImageGenerator({
            'width': self.config.get_image_dimensions()[0],
            'height': self.config.get_image_dimensions()[1],
            'quality': self.config.get_image_quality(),
            'format': self.config.get_image_format(),
            'theme': self.config.get_image_theme()
        })
        
        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger('XiaohongshuAutoposter')
        
        # Output directory
        self.output_dir = Path(self.config.get_output_dir())
        
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_dir = self.output_dir / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f'autoposter_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=getattr(logging, self.config.get_log_level()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def run_daily(self, topic: str = None, preview: bool = False) -> dict:
        """
        Run daily content generation.
        
        Args:
            topic: Specific topic to generate (optional)
            preview: Preview mode (don't save files)
            
        Returns:
            Result dictionary
        """
        self.logger.info("Starting daily content generation")
        
        try:
            # Select topic
            if not topic:
                topics = self.config.get_topics()
                topic = self._select_topic(topics)
            
            self.logger.info(f"Selected topic: {topic}")
            
            # Generate content
            self.logger.info("Generating content...")
            post = self.content_gen.generate_complete_post(topic)
            
            # Generate cover image
            self.logger.info("Generating cover image...")
            if not preview:
                image_path = self._generate_cover_image(post['title'], topic)
            else:
                image_path = None
            
            # Save output
            if not preview:
                files = self._save_output(post, image_path)
            else:
                files = {'preview': True}
            
            result = {
                'success': True,
                'topic': topic,
                'title': post['title'],
                'files': files,
                'generated_at': datetime.now().isoformat()
            }
            
            self.logger.info(f"Daily content generated successfully: {topic}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Daily generation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'topic': topic,
                'generated_at': datetime.now().isoformat()
            }
    
    def _select_topic(self, topics: list) -> str:
        """Select a topic from the list (round-robin or random)."""
        import random
        
        # Check calendar for today's scheduled topic
        calendar = ContentCalendar()
        today = datetime.now().strftime('%Y-%m-%d')
        scheduled = calendar.get_post(today)
        
        if scheduled and scheduled.get('topic'):
            return scheduled['topic']
        
        # Otherwise random selection
        return random.choice(topics)
    
    def _generate_cover_image(self, title: str, topic: str) -> str:
        """Generate and save cover image."""
        # Select random theme
        themes = ['vibrant', 'modern-minimalist', 'warm-vintage', 'tech-blue', 'nature-green']
        theme = self.config.get_image_theme() or random.choice(themes)
        
        # Generate image
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_path = str(self.output_dir / date_str / f'cover.png')
        
        return self.image_gen.generate_and_save(
            title=title,
            topic=topic,
            output_path=output_path,
            theme=theme
        )
    
    def _save_output(self, post: dict, image_path: str = None) -> dict:
        """Save generated content to files."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        post_dir = self.output_dir / date_str
        post_dir.mkdir(parents=True, exist_ok=True)
        
        files = {}
        
        # Save content markdown
        content_path = post_dir / 'content.md'
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(self._format_content(post))
        files['content'] = str(content_path)
        
        # Save title options
        if post.get('title_variants'):
            titles_path = post_dir / 'title_options.md'
            with open(titles_path, 'w', encoding='utf-8') as f:
                f.write(self._format_titles(post['title_variants']))
            files['titles'] = str(titles_path)
        
        # Save metadata
        metadata_path = post_dir / 'metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=2)
        files['metadata'] = str(metadata_path)
        
        # Copy image if generated
        if image_path and os.path.exists(image_path):
            files['image'] = image_path
        
        return files
    
    def _format_content(self, post: dict) -> str:
        """Format content for markdown output."""
        lines = [
            f"# {post['title']}",
            "",
            "---",
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
    
    def _format_titles(self, titles: list) -> str:
        """Format title variants for output."""
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
    
    def generate_specific(self, topic: str, preview: bool = False) -> dict:
        """
        Generate content for a specific topic.
        
        Args:
            topic: Content topic
            preview: Preview mode
            
        Returns:
            Result dictionary
        """
        self.logger.info(f"Generating specific topic: {topic}")
        return self.run_daily(topic=topic, preview=preview)
    
    def list_topics(self) -> list:
        """List available topics."""
        return self.config.get_topics()
    
    def get_calendar(self, month: str = None) -> dict:
        """Get content calendar."""
        calendar = ContentCalendar()
        return calendar.get_schedule(month)


def run_daily_post(topic: str = None) -> dict:
    """
    Convenience function for running daily post generation.
    
    Args:
        topic: Optional specific topic
        
    Returns:
        Result dictionary
    """
    autoposter = Autoposter()
    return autoposter.run_daily(topic=topic)


def main():
    """Main entry point with CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Xiaohongshu Daily Autoposter - Automated content generation"
    )
    
    parser.add_argument(
        '--mode', 
        choices=['daily', 'generate', 'schedule', 'calendar'],
        default='daily',
        help='Operating mode'
    )
    
    parser.add_argument(
        '--topic', '-t',
        type=str,
        help='Specific topic for content generation'
    )
    
    parser.add_argument(
        '--time',
        type=str,
        default='08:00',
        help='Daily posting time (HH:MM)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./output',
        help='Output directory'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview mode (don\'t save files)'
    )
    
    parser.add_argument(
        '--trigger-now',
        action='store_true',
        help='Trigger immediate generation'
    )
    
    parser.add_argument(
        '--theme',
        type=str,
        help='Image theme (vibrant, modern-minimalist, warm-vintage, tech-blue, nature-green)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to config.yaml file'
    )
    
    args = parser.parse_args()
    
    # Initialize autoposter
    autoposter = Autoposter(config_path=args.config)
    
    # Handle themes
    if args.theme:
        autoposter.config._config['image']['default_theme'] = args.theme
    
    if args.trigger_now:
        # Manual trigger
        result = autoposter.run_daily(topic=args.topic, preview=args.preview)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'daily':
        # Run daily generation
        result = autoposter.run_daily(topic=args.topic, preview=args.preview)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'generate':
        # Generate specific topic
        if not args.topic:
            print("Error: --topic required for generate mode")
            sys.exit(1)
        
        result = autoposter.generate_specific(args.topic, preview=args.preview)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'schedule':
        # Start scheduler
        scheduler = Scheduler(autoposter.config.scheduler)
        
        if args.trigger_now:
            # Immediate trigger
            result = scheduler.trigger_now(args.topic)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Start scheduled execution
            scheduler.start(args.time)
            print(f"Scheduler started. Daily execution at {args.time}")
            print("Press Ctrl+C to stop...")
            
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop()
                print("\nScheduler stopped.")
        
    elif args.mode == 'calendar':
        # Show calendar
        calendar = autoposter.get_calendar()
        print(json.dumps(calendar, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
