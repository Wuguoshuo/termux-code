"""
Image Generator for Xiaohongshu Daily Autoposter
Creates platform-optimized cover images with themed templates
"""

import random
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class ImageGenerator:
    """Generates Xiaohongshu cover images with themed templates."""
    
    # 主题颜色配置
    THEMES = {
        'vibrant': {
            'colors': ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#F38181'],
            'background': '#FFFFFF',
            'accent': '#FF6B6B'
        },
        'modern-minimalist': {
            'colors': ['#2D3436', '#636E72', '#B2BEC3', '#DFE6E9', '#FFFFFF'],
            'background': '#FFFFFF',
            'accent': '#2D3436'
        },
        'warm-vintage': {
            'colors': ['#E17055', '#FDCB6E', '#FFEAA7', '#D63031', '#634232'],
            'background': '#FFF9E6',
            'accent': '#E17055'
        },
        'tech-blue': {
            'colors': ['#0984E3', '#74B9FF', '#00CEC9', '#2D3436', '#FFFFFF'],
            'background': '#F0F8FF',
            'accent': '#0984E3'
        },
        'nature-green': {
            'colors': ['#00B894', '#55EFC4', '#FDCB6E', '#6C5CE7', '#2D3436'],
            'background': '#F0FFF0',
            'accent': '#00B894'
        }
    }
    
    # 布局变体
    LAYOUTS = [
        'centered',      # 居中标题
        'bottom-heavy',  # 底部强调
        'split',         # 左右分割
        'card',          # 卡片样式
        'gradient'       # 渐变背景
    ]
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize image generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.width = self.config.get('width', 1000)
        self.height = self.config.get('height', 1500)
        self.quality = self.config.get('quality', 95)
        self.output_format = self.config.get('format', 'PNG')
        self.default_theme = self.config.get('theme', 'vibrant')
        
        # 字体设置
        self.font_sizes = {
            'title': 72,
            'subtitle': 48,
            'body': 36,
            'tag': 28
        }
    
    def generate_cover(self, title: str, topic: str = None, theme: str = None, 
                       layout: str = None) -> Image.Image:
        """
        Generate a Xiaohongshu cover image.
        
        Args:
            title: Main title text
            topic: Content topic (for context)
            theme: Visual theme name
            layout: Layout variant
            
        Returns:
            PIL Image object
        """
        theme = theme or self.default_theme
        layout = layout or random.choice(self.LAYOUTS)
        
        # Get theme colors
        theme_config = self.THEMES.get(theme, self.THEMES['vibrant'])
        colors = theme_config['colors']
        background_color = self._hex_to_rgb(theme_config['background'])
        accent_color = self._hex_to_rgb(theme_config['accent'])
        
        # Create base image
        img = Image.new('RGB', (self.width, self.height), background_color)
        draw = ImageDraw.Draw(img)
        
        # Apply layout
        if layout == 'centered':
            self._layout_centered(img, draw, title, colors, accent_color)
        elif layout == 'bottom-heavy':
            self._layout_bottom_heavy(img, draw, title, colors, accent_color)
        elif layout == 'split':
            self._layout_split(img, draw, title, colors, accent_color)
        elif layout == 'card':
            self._layout_card(img, draw, title, colors, accent_color)
        elif layout == 'gradient':
            self._layout_gradient(img, draw, title, colors, accent_color)
        else:
            self._layout_centered(img, draw, title, colors, accent_color)
        
        return img
    
    def _layout_centered(self, img: Image.Image, draw: ImageDraw.Draw, 
                        title: str, colors: List[str], accent_color: Tuple) -> None:
        """Create centered layout."""
        # Draw decorative circles
        center_x, center_y = self.width // 2, self.height // 2
        
        # Large accent circle
        radius = min(self.width, self.height) // 3
        self._draw_circle(img, center_x, center_y, radius, colors[0], alpha=100)
        
        # Smaller accent circle
        self._draw_circle(img, center_x, center_y, radius // 2, colors[1], alpha=150)
        
        # Title text
        self._draw_text_centered(img, title, center_x, center_y, 
                                size=self.font_sizes['title'], 
                                color=colors[4] if len(colors) > 4 else (0, 0, 0))
        
        # Decorative elements
        self._draw_decorative_dots(img, colors)
    
    def _layout_bottom_heavy(self, img: Image.Image, draw: ImageDraw.Draw,
                             title: str, colors: List[str], accent_color: Tuple) -> None:
        """Create bottom-heavy layout with title at bottom."""
        # Gradient background
        for y in range(self.height):
            # Interpolate colors
            ratio = y / self.height
            r = int(colors[0][1:3], 16) * (1 - ratio) + int(colors[1][1:3], 16) * ratio
            g = int(colors[0][3:5], 16) * (1 - ratio) + int(colors[1][3:5], 16) * ratio
            b = int(colors[0][5:7], 16) * (1 - ratio) + int(colors[1][5:7], 16) * ratio
            for x in range(self.width):
                draw.point((x, y), fill=(r, g, b))
        
        # Bottom panel for title
        panel_height = self.height // 3
        panel_y = self.height - panel_height
        
        # Draw accent rectangle at bottom
        self._draw_rounded_rectangle(img, 50, panel_y + 30, 
                                    self.width - 50, self.height - 50,
                                    colors[2], radius=30)
        
        # Draw title
        self._draw_text_centered(img, title, self.width // 2, 
                                panel_y + panel_height // 2,
                                size=self.font_sizes['title'],
                                color=colors[4] if len(colors) > 4 else (0, 0, 0))
        
        # Top decorative element
        self._draw_triangle(img, self.width // 2, 100, colors[0])
    
    def _layout_split(self, img: Image.Image, draw: ImageDraw.Draw,
                     title: str, colors: List[str], accent_color: Tuple) -> None:
        """Create split layout with diagonal division."""
        # Left side color
        self._draw_diagonal_split(img, colors[0], colors[1])
        
        # Title on the lighter side
        text_x = self.width // 4
        text_y = self.height // 2
        
        self._draw_text(img, title, text_x, text_y,
                       size=self.font_sizes['title'],
                       color=colors[4] if len(colors) > 4 else (255, 255, 255),
                       anchor='mm')
        
        # Decorative circle on right
        self._draw_circle(img, self.width * 3 // 4, self.height // 3, 
                         150, colors[2], alpha=80)
        
        # Tag-style decoration
        self._draw_tag(img, "爆款推荐", colors[3], colors[4])
    
    def _layout_card(self, img: Image.Image, draw: ImageDraw.Draw,
                    title: str, colors: List[str], accent_color: Tuple) -> None:
        """Create card-style layout."""
        # Background pattern
        self._draw_pattern(img, colors)
        
        # Central card
        card_padding = 60
        self._draw_rounded_rectangle(img, card_padding, card_padding,
                                    self.width - card_padding, self.height - card_padding,
                                    colors[4] if len(colors) > 4 else '#FFFFFF',
                                    radius=40, fill=True)
        
        # Inner border
        inner_padding = 80
        self._draw_rounded_rectangle(img, inner_padding, inner_padding,
                                    self.width - inner_padding, self.height - inner_padding,
                                    colors[0], radius=30, width=5)
        
        # Title
        self._draw_text_centered(img, title, self.width // 2, 
                                self.height // 2,
                                size=self.font_sizes['title'],
                                color=colors[0])
        
        # Corner decorations
        self._draw_corner_decorations(img, colors)
    
    def _layout_gradient(self, img: Image.Image, draw: ImageDraw.Draw,
                        title: str, colors: List[str], accent_color: Tuple) -> None:
        """Create gradient background layout."""
        # Full gradient background
        self._draw_radial_gradient(img, colors[0], colors[1])
        
        # Overlay
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Semi-transparent overlay
        for y in range(self.height):
            alpha = int(30 + 40 * (y / self.height))
            overlay_draw.line((0, y, self.width, y), fill=(255, 255, 255, alpha))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Title with shadow
        self._draw_text_shadowed(img, title, self.width // 2, self.height // 2,
                                size=self.font_sizes['title'],
                                text_color=(255, 255, 255),
                                shadow_color=colors[0])
        
        # Shine effect
        self._draw_shine(img)
    
    # Helper drawing methods
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _draw_circle(self, img: Image.Image, x: int, y: int, radius: int, 
                    color: str, alpha: int = 255) -> None:
        """Draw a circle on the image."""
        color_rgb = self._hex_to_rgb(color)
        
        # Create temp image for alpha handling
        temp = Image.new('RGBA', img.size, (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp)
        
        temp_draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                         fill=color_rgb + (alpha,))
        
        # Composite
        img.paste(temp, (0, 0), temp)
    
    def _draw_rounded_rectangle(self, img: Image.Image, x1: int, y1: int,
                               x2: int, y2: int, color: str, radius: int = 20,
                               width: int = 0, fill: bool = False) -> None:
        """Draw a rounded rectangle."""
        color_rgb = self._hex_to_rgb(color)
        
        # Create temp image
        temp = Image.new('RGBA', img.size, (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp)
        
        if fill:
            temp_draw.rounded_rectangle([x1, y1, x2, y2], radius=radius,
                                       fill=color_rgb)
        else:
            temp_draw.rounded_rectangle([x1, y1, x2, y2], radius=radius,
                                       outline=color_rgb, width=width)
        
        img.paste(temp, (0, 0), temp)
    
    def _draw_triangle(self, img: Image.Image, x: int, y: int, color: str) -> None:
        """Draw a decorative triangle."""
        color_rgb = self._hex_to_rgb(color)
        size = 80
        
        temp = Image.new('RGBA', img.size, (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp)
        
        points = [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size)
        ]
        
        temp_draw.polygon(points, fill=color_rgb + (180,))
        
        img.paste(temp, (0, 0), temp)
    
    def _draw_diagonal_split(self, img: Image.Image, color1: str, color2: str) -> None:
        """Draw diagonal color split background."""
        color1_rgb = self._hex_to_rgb(color1)
        color2_rgb = self._hex_to_rgb(color2)
        
        draw = ImageDraw.Draw(img)
        
        # Draw diagonal
        for i in range(self.width + self.height):
            # Interpolate
            t = i / (self.width + self.height)
            r = int(color1_rgb[0] * (1 - t) + color2_rgb[0] * t)
            g = int(color1_rgb[1] * (1 - t) + color2_rgb[1] * t)
            b = int(color1_rgb[2] * (1 - t) + color2_rgb[2] * t)
            
            if i < self.height:
                # Left triangle
                draw.line([(0, i), (i, 0)], fill=(r, g, b), width=3)
            else:
                # Right triangle
                draw.line([(i - self.height, self.height), 
                          (self.width, i - self.height + self.width - self.height)],
                         fill=(r, g, b), width=3)
    
    def _draw_pattern(self, img: Image.Image, colors: List[str]) -> None:
        """Draw background pattern."""
        draw = ImageDraw.Draw(img)
        
        # Draw dots pattern
        spacing = 50
        for x in range(0, self.width, spacing):
            for y in range(0, self.height, spacing):
                color = colors[(x + y) // spacing % len(colors)]
                color_rgb = self._hex_to_rgb(color)
                radius = 3
                draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                            fill=color_rgb + (30,))
    
    def _draw_decorative_dots(self, img: Image.Image, colors: List[str]) -> None:
        """Draw decorative dots around the image."""
        draw = ImageDraw.Draw(img)
        
        # Corner dots
        corners = [(50, 50), (self.width - 50, 50), 
                  (50, self.height - 50), (self.width - 50, self.height - 50)]
        
        for i, (x, y) in enumerate(corners):
            color = colors[i % len(colors)]
            color_rgb = self._hex_to_rgb(color)
            draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill=color_rgb)
    
    def _draw_corner_decorations(self, img: Image.Image, colors: List[str]) -> None:
        """Draw corner decorations."""
        draw = ImageDraw.Draw(img)
        
        # Corner accents
        corners = [(30, 30), (self.width - 30, 30)]
        
        for i, (x, y) in enumerate(corners):
            color = colors[i % len(colors)]
            color_rgb = self._hex_to_rgb(color)
            # Draw small circle
            draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=color_rgb)
    
    def _draw_tag(self, img: Image.Image, text: str, bg_color: str, text_color: str) -> None:
        """Draw a tag-style element."""
        draw = ImageDraw.Draw(img)
        
        # Tag position
        x, y = self.width - 120, 80
        
        bg_rgb = self._hex_to_rgb(bg_color)
        text_rgb = self._hex_to_rgb(text_color)
        
        # Tag background
        self._draw_rounded_rectangle(img, x - 10, y - 20, x + 100, y + 20,
                                    bg_color, radius=10, fill=True)
        
        # Tag text
        draw.text((x + 45, y), text, fill=text_rgb, anchor='mm')
    
    def _draw_shine(self, img: Image.Image) -> None:
        """Draw shine effect."""
        draw = ImageDraw.Draw(img)
        
        # Diagonal shine line
        for i in range(0, max(self.width, self.height), 10):
            alpha = int(50 * (1 - i / max(self.width, self.height)))
            color = (255, 255, 255, alpha)
            
            x1 = i if i < self.width else self.width
            y1 = 0 if i < self.width else i - self.width
            x2 = 0 if i + 100 > self.width else i + 100
            y2 = i + 100 if i < self.width else self.height
            
            draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    
    def _draw_radial_gradient(self, img: Image.Image, color1: str, color2: str) -> None:
        """Draw radial gradient background."""
        color1_rgb = self._hex_to_rgb(color1)
        color2_rgb = self._hex_to_rgb(color2)
        
        center_x, center_y = self.width // 2, self.height // 2
        max_radius = int(((self.width // 2) ** 2 + (self.height // 2) ** 2) ** 0.5)
        
        for r in range(max_radius, 0, -10):
            # Interpolate color
            t = 1 - (r / max_radius)
            color = (
                int(color1_rgb[0] * (1 - t) + color2_rgb[0] * t),
                int(color1_rgb[1] * (1 - t) + color2_rgb[1] * t),
                int(color1_rgb[2] * (1 - t) + color2_rgb[2] * t)
            )
            
            # Draw circle
            temp = Image.new('RGB', img.size, color)
            mask = Image.new('L', img.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            
            # Create gradient mask
            mask_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
                             fill=int(255 * (1 - t)))
            
            # Composite
            img.paste(temp, (0, 0), mask)
    
    def _draw_text_centered(self, img: Image.Image, text: str, x: int, y: int,
                           size: int = 48, color: str = '#000000') -> None:
        """Draw centered text."""
        self._draw_text(img, text, x, y, size, color, anchor='mm')
    
    def _draw_text(self, img: Image.Image, text: str, x: int, y: int,
                  size: int = 48, color: str = '#000000',
                  anchor: str = 'lt') -> None:
        """Draw text on image."""
        draw = ImageDraw.Draw(img)
        color_rgb = self._hex_to_rgb(color)
        
        # Use default font if specific font not available
        try:
            # Try to use a system font
            font_path = self._get_font_path()
            if font_path:
                font = ImageFont.truetype(font_path, size)
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        draw.text((x, y), text, fill=color_rgb, font=font, anchor=anchor)
    
    def _draw_text_shadowed(self, img: Image.Image, text: str, x: int, y: int,
                           size: int = 48, text_color: str = '#FFFFFF',
                           shadow_color: str = '#000000') -> None:
        """Draw text with shadow effect."""
        offset = 4
        
        # Draw shadow
        self._draw_text(img, text, x + offset, y + offset, size, shadow_color, anchor='mm')
        
        # Draw main text
        self._draw_text(img, text, x, y, size, text_color, anchor='mm')
    
    def _get_font_path(self) -> str:
        """Get path to available font."""
        # Common font paths
        font_paths = [
            '/usr/share/fonts/truetype/noto/NotoSansSC-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            '/System/Library/Fonts/PingFang.ttc',  # macOS
            'C:\\Windows\\Fonts\\msyh.ttc',  # Windows
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def save_image(self, img: Image.Image, path: str, quality: int = None) -> str:
        """
        Save image to file.
        
        Args:
            img: PIL Image object
            path: Output file path
            quality: Quality setting (1-100)
            
        Returns:
            Path to saved file
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Determine format
        if path.endswith('.png'):
            img.save(path, 'PNG')
        elif path.endswith('.jpg') or path.endswith('.jpeg'):
            quality = quality or self.quality
            img.save(path, 'JPEG', quality=quality)
        else:
            # Default to PNG
            if not path.endswith('.png'):
                path += '.png'
            img.save(path, 'PNG')
        
        return path
    
    def generate_and_save(self, title: str, topic: str = None, output_path: str = None,
                         theme: str = None, layout: str = None) -> str:
        """
        Generate and save cover image.
        
        Args:
            title: Main title text
            topic: Content topic
            output_path: Output file path
            theme: Visual theme
            layout: Layout variant
            
        Returns:
            Path to saved image
        """
        # Generate image
        img = self.generate_cover(title, topic, theme, layout)
        
        # Determine output path
        if not output_path:
            from datetime import datetime
            date_str = datetime.now().strftime('%Y-%m-%d')
            output_dir = Path('./output') / date_str
            os.makedirs(output_dir, exist_ok=True)
            output_path = str(output_dir / f'cover.{self.output_format.lower()}')
        
        # Save
        self.save_image(img, output_path)
        
        return output_path


# Convenience function
def create_cover_image(title: str, topic: str = None, output_path: str = None,
                      theme: str = 'vibrant', **kwargs) -> str:
    """
    Create a Xiaohongshu cover image.
    
    Args:
        title: Main title text
        topic: Content topic
        output_path: Output file path
        theme: Visual theme
        **kwargs: Additional arguments
        
    Returns:
        Path to saved image
    """
    config = {
        'width': 1000,
        'height': 1500,
        'quality': 95,
        'format': 'PNG',
        'theme': theme
    }
    config.update(kwargs)
    
    generator = ImageGenerator(config)
    return generator.generate_and_save(title, topic, output_path, theme)
