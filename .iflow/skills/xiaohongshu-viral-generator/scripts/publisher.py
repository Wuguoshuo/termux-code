"""
Publisher for Xiaohongshu Viral Generator
Handles posting content to Xiaohongshu platform
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BasePublisher(ABC):
    """Abstract base class for content publishers."""
    
    @abstractmethod
    def publish(self, title: str, body: str, images: List[str]) -> str:
        """Publish content to platform.
        
        Args:
            title: Content title
            body: Content body
            images: List of image paths
            
        Returns:
            Published content ID
        """
        pass
    
    @abstractmethod
    def save_as_draft(self, title: str, body: str, images: List[str]) -> str:
        """Save content as draft.
        
        Args:
            title: Content title
            body: Content body
            images: List of image paths
            
        Returns:
            Draft ID
        """
        pass


class XiaohongshuPublisher(BasePublisher):
    """Publisher for Xiaohongshu platform using Creator Tools API."""
    
    def __init__(self, api_key: str = None, config: Dict[str, Any] = None):
        """
        Initialize Xiaohongshu publisher.
        
        Args:
            api_key: Xiaohongshu API key
            config: Configuration dictionary
        """
        self.api_key = api_key or os.getenv("XIAOHONGSHU_API_KEY")
        self.config = config or {}
        self.base_url = "https://open.xiaohongshu.com/api"
        
        if not self.api_key:
            logger.warning("XIAOHONGSHU_API_KEY not set. Publishing will be disabled.")
    
    def _make_request(self, endpoint: str, method: str = 'POST',
                      data: Dict = None, files: Dict = None) -> Dict:
        """Make API request to Xiaohongshu."""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        if files:
            # Multi-part request for images
            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                data=data,
                files=files,
                timeout=120
            )
        else:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=60)
            else:
                response = requests.post(
                    url, headers=headers, json=data, timeout=60
                )
        
        response.raise_for_status()
        return response.json()
    
    def publish(self, title: str, body: str, images: List[str]) -> str:
        """
        Publish content to Xiaohongshu.
        
        Args:
            title: Post title
            body: Post body (Markdown format)
            images: List of image file paths
            
        Returns:
            Published note ID or empty string if failed
        """
        if not self.api_key:
            logger.error("Cannot publish: API key not configured")
            return ""
        
        try:
            # Upload images first
            image_ids = self._upload_images(images)
            
            # Create note payload
            payload = {
                "title": title,
                "content": self._convert_markdown(body),
                "images": image_ids,
                "type": "normal"
            }
            
            # Publish note
            response = self._make_request("notes/publish", data=payload)
            
            note_id = response.get("data", {}).get("note_id", "")
            logger.info(f"Published note: {note_id}")
            
            return note_id
            
        except Exception as e:
            logger.error(f"Failed to publish: {e}")
            return ""
    
    def save_as_draft(self, title: str, body: str, 
                      images: List[str]) -> str:
        """
        Save content as draft.
        
        Args:
            title: Post title
            body: Post body
            images: List of image file paths
            
        Returns:
            Draft ID
        """
        if not self.api_key:
            logger.error("Cannot save draft: API key not configured")
            return ""
        
        try:
            # Upload images
            image_ids = self._upload_images(images)
            
            # Create draft payload
            payload = {
                "title": title,
                "content": self._convert_markdown(body),
                "images": image_ids,
                "type": "normal"
            }
            
            # Save as draft
            response = self._make_request("drafts/create", data=payload)
            
            draft_id = response.get("data", {}).get("draft_id", "")
            logger.info(f"Saved draft: {draft_id}")
            
            return draft_id
            
        except Exception as e:
            logger.error(f"Failed to save draft: {e}")
            return ""
    
    def _upload_images(self, images: List[str]) -> List[str]:
        """Upload images and return image IDs."""
        image_ids = []
        
        for image_path in images:
            try:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        files = {"image": (os.path.basename(image_path), f, "image/png")}
                        data = {"type": "normal"}
                        
                        response = self._make_request(
                            "images/upload", data=data, files=files
                        )
                        
                        image_id = response.get("data", {}).get("image_id", "")
                        if image_id:
                            image_ids.append(image_id)
                            
            except Exception as e:
                logger.warning(f"Failed to upload image {image_path}: {e}")
        
        return image_ids
    
    def _convert_markdown(self, markdown_text: str) -> str:
        """
        Convert Markdown to Xiaohongshu HTML format.
        
        Args:
            markdown_text: Markdown formatted text
            
        Returns:
            HTML formatted text
        """
        # Basic Markdown to Xiaohongshu HTML conversion
        import re
        
        text = markdown_text
        
        # Headers
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # Line breaks
        text = text.replace('\n', '<br>')
        
        return text
    
    def get_publishing_status(self, note_id: str) -> Dict[str, Any]:
        """Check publishing status of a note.
        
        Args:
            note_id: Note ID to check
            
        Returns:
            Status dictionary
        """
        if not self.api_key:
            return {"status": "error", "message": "API key not configured"}
        
        try:
            response = self._make_request(
                f"notes/{note_id}/status", method='GET'
            )
            return response.get("data", {})
            
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return {"status": "error", "message": str(e)}


class MockPublisher(BasePublisher):
    """Mock publisher for testing without API access."""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
    
    def publish(self, title: str, body: str, images: List[str]) -> str:
        """Mock publish - saves to local file."""
        from datetime import datetime
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_path = Path(self.output_dir) / date_str / "published_note.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "title": title,
            "body": body,
            "images": images,
            "published_at": datetime.now().isoformat(),
            "note_id": f"mock_{date_str}_{hash(title) % 10000}"
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Mock publish saved: {output_path}")
        return data["note_id"]
    
    def save_as_draft(self, title: str, body: str, 
                      images: List[str]) -> str:
        """Mock save as draft."""
        from datetime import datetime
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_path = Path(self.output_dir) / date_str / "draft_note.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "title": title,
            "body": body,
            "images": images,
            "saved_at": datetime.now().isoformat(),
            "draft_id": f"draft_{date_str}_{hash(title) % 10000}"
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Mock draft saved: {output_path}")
        return data["draft_id"]


def create_publisher(provider: str = 'xiaohongshu', **kwargs) -> BasePublisher:
    """
    Factory function to create publisher.
    
    Args:
        provider: Publisher type (xiaohongshu, mock)
        **kwargs: Additional configuration
        
    Returns:
        Publisher instance
    """
    if provider == 'xiaohongshu':
        return XiaohongshuPublisher(**kwargs)
    elif provider == 'mock':
        return MockPublisher(**kwargs)
    else:
        raise ValueError(f"Unknown publisher: {provider}")
