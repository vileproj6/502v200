#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Production Content Extractor
Wrapper atualizado que redireciona para RobustContentExtractor
"""

import logging
from typing import Dict, List, Optional, Any
from services.robust_content_extractor import robust_content_extractor

logger = logging.getLogger(__name__)

class ProductionContentExtractor:
    """Wrapper atualizado para compatibilidade com RobustContentExtractor"""

    def __init__(self):
        """Inicializa wrapper atualizado"""
        self.extractor = robust_content_extractor
        logger.info("✅ Production Content Extractor inicializado (wrapper para RobustContentExtractor)")

    def extract_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo de URL"""
        return self.extractor.extract_content(url)

    def safe_extract_content(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Extração segura de conteúdo"""
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
        return self.extractor.get_extractor_stats()

    def reset_extractor_stats(self, extractor_name: Optional[str] = None):
        """Reset estatísticas dos extratores"""
        return self.extractor.reset_extractor_stats(extractor_name)

    def batch_extract(self, urls: List[str], max_workers: int = 5) -> Dict[str, Optional[str]]:
        """Extrai conteúdo de múltiplas URLs"""
        return self.extractor.batch_extract(urls, max_workers)

    def clear_cache(self):
        """Limpa cache de extração"""
        return self.extractor.clear_cache()

    def test_extraction(self, url: str) -> Dict[str, Any]:
        """Testa extração para URL específica"""
        return self.extractor.test_extraction(url)

# Instância global atualizada
production_content_extractor = ProductionContentExtractor()