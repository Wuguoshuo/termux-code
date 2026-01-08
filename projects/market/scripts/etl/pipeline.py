#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六堡茶价格数据采集器

支持:
- API对接模式
- 网页爬虫模式
- 定时任务调度
"""

import requests
import json
import time
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """数据抽取器基类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.name = config.get('name', 'unknown')
    
    @abstractmethod
    def extract(self) -> List[Dict]:
        """从数据源抽取数据"""
        pass
    
    def run(self) -> List[Dict]:
        """运行抽取流程"""
        logger.info(f"开始从 [{self.name}] 抽取数据")
        try:
            data = self.extract()
            logger.info(f"成功抽取 {len(data)} 条数据")
            return data
        except Exception as e:
            logger.error(f"抽取数据失败: {e}")
            raise


class APIExtractor(BaseExtractor):
    """API数据抽取器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.api_url = config.get('api_url', '')
        self.api_key = config.get('api_key', '')
        self.auth_type = config.get('auth_type', 'none')
        self.timeout = config.get('timeout', 30)
    
    def _get_headers(self) -> Dict:
        """获取请求头"""
        headers = {'Content-Type': 'application/json'}
        if self.auth_type == 'bearer':
            headers['Authorization'] = f'Bearer {self.api_key}'
        elif self.auth_type == 'apikey':
            headers['X-API-Key'] = self.api_key
        return headers
    
    def extract(self) -> List[Dict]:
        """从API抽取数据"""
        try:
            response = requests.get(
                self.api_url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 字段映射
            mapping = self.config.get('field_mapping', {})
            mapped_data = self._map_fields(data, mapping)
            
            return mapped_data
            
        except requests.RequestException as e:
            logger.error(f"API请求失败: {e}")
            raise
    
    def _map_fields(self, data: Dict, mapping: Dict) -> List[Dict]:
        """字段映射"""
        if isinstance(data, list):
            return [self._map_fields(item, mapping) for item in data]
        
        mapped = {}
        for src_field, dst_field in mapping.items():
            if src_field in data:
                mapped[dst_field] = data[src_field]
        
        return mapped


class CrawlerExtractor(BaseExtractor):
    """网页爬虫抽取器"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.base_url = config.get('base_url', '')
        self.selectors = config.get('selectors', {})
        self.headers = config.get('headers', {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = config.get('timeout', 30)
    
    def extract(self) -> List[Dict]:
        """从网页抽取数据"""
        try:
            from bs4 import BeautifulSoup
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = self._parse_page(soup)
            
            return items
            
        except ImportError:
            logger.error("请安装 beautifulsoup4: pip install beautifulsoup4")
            raise
        except requests.RequestException as e:
            logger.error(f"网页请求失败: {e}")
            raise
    
    def _parse_page(self, soup: BeautifulSoup) -> List[Dict]:
        """解析页面"""
        items = []
        container = soup.select_one(self.selectors.get('container', 'tbody'))
        
        if container:
            for row in container.select(self.selectors.get('row', 'tr')):
                item = self._parse_row(row, soup)
                if item:
                    items.append(item)
        
        return items
    
    def _parse_row(self, row, soup) -> Optional[Dict]:
        """解析行数据"""
        return None


class ManualExtractor(BaseExtractor):
    """手动录入数据"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.manual_data = config.get('data', [])
    
    def extract(self) -> List[Dict]:
        """返回手动配置的数据"""
        return self.manual_data


class PriceETLPipeline:
    """价格数据ETL管道"""
    
    def __init__(self):
        self.extractors: Dict[str, BaseExtractor] = {}
        self.transformers = []
        self.validators = []
    
    def register_extractor(self, name: str, extractor: BaseExtractor):
        """注册抽取器"""
        self.extractors[name] = extractor
    
    def add_transformer(self, transformer: callable):
        """添加转换器"""
        self.transformers.append(transformer)
    
    def add_validator(self, validator: callable):
        """添加校验器"""
        self.validators.append(validator)
    
    def run(self, source_name: str) -> Dict:
        """运行ETL流程"""
        if source_name not in self.extractors:
            raise ValueError(f"未找到数据源: {source_name}")
        
        extractor = self.extractors[source_name]
        
        # Extract
        raw_data = extractor.run()
        
        # Transform
        cleaned_data = self._transform(raw_data)
        
        # Validate
        valid_data, errors = self._validate(cleaned_data)
        
        # 记录错误
        for error in errors:
            logger.warning(f"数据校验警告: {error}")
        
        return {
            'source': source_name,
            'extracted': len(raw_data),
            'cleaned': len(cleaned_data),
            'valid': len(valid_data),
            'errors': len(errors),
            'data': valid_data
        }
    
    def run_all(self) -> List[Dict]:
        """运行所有数据源"""
        results = []
        for name in self.extractors:
            try:
                result = self.run(name)
                results.append(result)
            except Exception as e:
                logger.error(f"数据源 [{name}] 处理失败: {e}")
                results.append({
                    'source': name,
                    'error': str(e)
                })
        return results
    
    def _transform(self, data: List[Dict]) -> List[Dict]:
        """数据清洗转换"""
        cleaned = []
        for item in data:
            transformed = item
            
            for transformer in self.transformers:
                transformed = transformer(transformed)
            
            cleaned.append(transformed)
        
        return cleaned
    
    def _validate(self, data: List[Dict]) -> tuple:
        """数据校验"""
        valid = []
        errors = []
        
        for item in data:
            item_errors = []
            
            for validator in self.validators:
                result = validator(item)
                if result is not True:
                    item_errors.append(result)
            
            if not item_errors:
                valid.append(item)
            else:
                errors.append({
                    'item': item,
                    'errors': item_errors
                })
        
        return valid, errors


# 默认转换器
def clean_price(value):
    """清洗价格数据"""
    if isinstance(value, str):
        return float(value.replace('¥', '').replace(',', '').strip())
    return value

def standardize_date(value, format='%Y-%m-%d'):
    """标准化日期格式"""
    if isinstance(value, datetime):
        return value.strftime(format)
    return value


# 默认校验器
def required_field(field_name):
    """必填字段校验"""
    def validator(item):
        if field_name not in item or item[field_name] is None:
            return f"缺少必填字段: {field_name}"
        return True
    return validator

def price_range_validator(min_price=0, max_price=100000):
    """价格范围校验"""
    def validator(item):
        price = item.get('price', 0)
        if price < min_price or price > max_price:
            return f"价格超出范围: {price}"
        return True
    return validator


# 主程序入口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='六堡茶价格数据采集器')
    parser.add_argument('--source', type=str, help='指定数据源名称')
    parser.add_argument('--config', type=str, default='config.json', help='配置文件路径')
    args = parser.parse_args()
    
    # 加载配置
    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 创建ETL管道
    pipeline = PriceETLPipeline()
    
    # 添加转换器
    pipeline.add_transformer(lambda x: {**x, 'price': clean_price(x.get('price', 0))})
    
    # 添加校验器
    pipeline.add_validator(required_field('product_name'))
    pipeline.add_validator(price_range_validator())
    
    # 注册数据源
    for source_config in config.get('sources', []):
        source_type = source_config.get('type')
        
        if source_type == 'api':
            extractor = APIExtractor(source_config)
        elif source_type == 'crawler':
            extractor = CrawlerExtractor(source_config)
        elif source_type == 'manual':
            extractor = ManualExtractor(source_config)
        else:
            logger.warning(f"未知的数据源类型: {source_type}")
            continue
        
        pipeline.register_extractor(source_config['name'], extractor)
    
    # 运行
    if args.source:
        result = pipeline.run(args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        results = pipeline.run_all()
        print(json.dumps(results, ensure_ascii=False, indent=2))
