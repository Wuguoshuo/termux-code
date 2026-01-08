#!/usr/bin/env python3
"""
Test script for Xiaohongshu Daily Autoposter
Verifies core functionality
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from datetime import datetime


def test_config_loader():
    """Test configuration loading."""
    print("Testing config_loader...")
    try:
        from config_loader import Config, get_config
        config = Config()
        
        # Test basic getters
        assert config.get_posting_time() == "08:00"
        assert config.get_topics() is not None
        assert len(config.get_topics()) > 0
        
        print("  ✓ Config loader works correctly")
        return True
    except Exception as e:
        print(f"  ✗ Config loader failed: {e}")
        return False


def test_content_generator():
    """Test content generation."""
    print("Testing content_generator...")
    try:
        from content_generator import ContentGenerator
        generator = ContentGenerator()
        
        # Test title generation
        title = generator.generate_title("职场效率", style="contrast")
        assert title is not None
        assert len(title) > 0
        print(f"  ✓ Generated title: {title}")
        
        # Test title variants
        variants = generator.generate_title_variants("职场效率", count=3)
        assert len(variants) == 3
        print(f"  ✓ Generated {len(variants)} title variants")
        
        # Test complete post generation
        post = generator.generate_complete_post("职场效率")
        assert post['title'] is not None
        assert post['body'] is not None
        assert len(post['hashtags']) > 0
        print(f"  ✓ Generated complete post with {len(post['body'])} chars")
        
        return True
    except Exception as e:
        print(f"  ✗ Content generator failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_generator():
    """Test image generation."""
    print("Testing image_generator...")
    try:
        from image_generator import ImageGenerator
        generator = ImageGenerator({
            'width': 1000,
            'height': 1500,
            'quality': 95,
            'format': 'PNG',
            'theme': 'vibrant'
        })
        
        # Test image generation
        img = generator.generate_cover(
            title="测试标题",
            topic="职场效率",
            theme="vibrant",
            layout="centered"
        )
        
        assert img is not None
        assert img.size == (1000, 1500)
        print(f"  ✓ Generated image: {img.size}")
        
        return True
    except Exception as e:
        print(f"  ✗ Image generator failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scheduler():
    """Test scheduler functionality."""
    print("Testing scheduler...")
    try:
        from scheduler import Scheduler, ContentCalendar
        
        # Test calendar
        calendar = ContentCalendar()
        test_date = (datetime.now().strftime('%Y-%m-%d'))
        
        # Add and remove test post
        calendar.add_post(test_date, "测试话题")
        assert calendar.get_post(test_date) is not None
        
        calendar.remove_post(test_date)
        assert calendar.get_post(test_date) is None
        
        print("  ✓ Calendar operations work correctly")
        
        # Test scheduler creation
        scheduler = Scheduler()
        status = scheduler.get_status()
        assert 'state' in status
        
        print("  ✓ Scheduler initialization works")
        
        return True
    except Exception as e:
        print(f"  ✗ Scheduler failed: {e}")
        return False


def test_autoposter():
    """Test main autoposter."""
    print("Testing autoposter...")
    try:
        # Import main module
        sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
        from autoposter import Autoposter
        
        autoposter = Autoposter()
        
        # Test list topics
        topics = autoposter.list_topics()
        assert len(topics) > 0
        print(f"  ✓ Available topics: {topics}")
        
        # Test preview generation (no files created)
        result = autoposter.run_daily(topic="职场效率", preview=True)
        assert result['success'] == True
        assert result['topic'] == "职场效率"
        print(f"  ✓ Preview generation works: {result['title']}")
        
        return True
    except Exception as e:
        print(f"  ✗ Autoposter failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Xiaohongshu Daily Autoposter - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Config Loader", test_config_loader),
        ("Content Generator", test_content_generator),
        ("Image Generator", test_image_generator),
        ("Scheduler", test_scheduler),
        ("Autoposter", test_autoposter),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 Testing {name}...")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
