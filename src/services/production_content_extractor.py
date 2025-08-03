#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Production Content Extractor
Wrapper que funciona com ou sem RobustContentExtractor
"""

import logging
from typing import Dict, List, Optional, Any

# Importação condicional
try:
    from .robust_content_extractor import robust_content_extractor
    HAS_ROBUST_EXTRACTOR = True
except ImportError:
    HAS_ROBUST_EXTRACTOR = False
    robust_content_extractor = None
logger = logging.getLogger(__name__)

class ProductionContentExtractor:
    """Wrapper que funciona com ou sem RobustContentExtractor"""

    def __init__(self):
        """Inicializa wrapper"""
        self.extractor = robust_content_extractor if HAS_ROBUST_EXTRACTOR else None
        
        if HAS_ROBUST_EXTRACTOR:
            logger.info("✅ Production Content Extractor inicializado com RobustContentExtractor")
        else:
            logger.warning("⚠️ Production Content Extractor inicializado sem RobustContentExtractor")

    def extract_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo de URL"""
        if self.extractor:
            return self.extractor.extract_content(url)
        else:
            logger.warning("⚠️ Extrator não disponível")
            return None

    def safe_extract_content(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Extração segura de conteúdo"""
        if not self.extractor:
            return {
                'success': False,
                'error': 'Extrator não disponível',
                'url': url,
                'metadata': {'extraction_method': 'unavailable'}
            }
        
        try:
            content = self.extractor.extract_content(url)
            
            if content:
                return {
                    'success': True,
                    'content': content,
                    'url': url,
                    'metadata': {
                        'content_length': len(content),
                        'word_count': len(content.split()),
                        'extraction_method': 'robust_extractor'
                    },
                    'validation': {
                        'valid': len(content) > 200,
                        'score': min(100, len(content) / 50),  # Score baseado no tamanho
                        'reason': 'Conteúdo extraído com sucesso'
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Nenhum conteúdo extraído',
                    'url': url,
                    'metadata': {'extraction_method': 'robust_extractor'}
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url,
                'metadata': {'extraction_method': 'robust_extractor'}
            }

    def get_extraction_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de extração"""
        if self.extractor:
            return self.extractor.get_extractor_stats()
        else:
            return {'error': 'Extrator não disponível'}

    def reset_extractor_stats(self, extractor_name: Optional[str] = None):
        """Reset estatísticas dos extratores"""
        if self.extractor:
            return self.extractor.reset_extractor_stats(extractor_name)

    def batch_extract(self, urls: List[str], max_workers: int = 5) -> Dict[str, Optional[str]]:
        """Extrai conteúdo de múltiplas URLs"""
        if self.extractor:
            return self.extractor.batch_extract(urls, max_workers)
        else:
            return {url: None for url in urls}

    def clear_cache(self):
        """Limpa cache de extração"""
        if self.extractor:
            return self.extractor.clear_cache()

    def test_extraction(self, url: str) -> Dict[str, Any]:
        """Testa extração para URL específica"""
        if self.extractor:
            return self.extractor.test_extraction(url)
        else:
            return {
                'success': False,
                'error': 'Extrator não disponível',
                'url': url
            }

# Instância global
production_content_extractor = ProductionContentExtractor()