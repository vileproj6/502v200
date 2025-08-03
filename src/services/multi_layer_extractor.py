#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Multi-Layer Extractor
Sistema de extração em múltiplas camadas com fallbacks inteligentes
"""

import logging
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.robust_content_extractor import robust_content_extractor
from services.playwright_extractor import playwright_extractor
from services.content_quality_validator import content_quality_validator
from services.url_resolver import url_resolver
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class MultiLayerExtractor:
    """Sistema de extração em múltiplas camadas com estratégias avançadas"""
    
    def __init__(self):
        """Inicializa o extrator multi-camadas"""
        self.extraction_layers = [
            ('static_extraction', self._extract_static_content),
            ('dynamic_extraction', self._extract_dynamic_content),
            ('aggressive_extraction', self._extract_aggressive_content),
            ('fallback_extraction', self._extract_fallback_content)
        ]
        
        self.quality_thresholds = {
            'min_content_length': 500,
            'min_quality_score': 60.0,
            'min_word_count': 100
        }
        
        self.stats = {
            'total_attempts': 0,
            'successful_extractions': 0,
            'layer_usage': {layer[0]: 0 for layer in self.extraction_layers},
            'quality_distribution': {'high': 0, 'medium': 0, 'low': 0, 'failed': 0}
        }
        
        logger.info("Multi-Layer Extractor inicializado com 4 camadas")
    
    def extract_with_multiple_strategies(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Extrai conteúdo usando múltiplas estratégias em camadas"""
        
        self.stats['total_attempts'] += 1
        
        logger.info(f"🔍 Iniciando extração multi-camadas para: {url}")
        
        # Resolve URL primeiro
        try:
            resolved_url = url_resolver.resolve_redirect_url(url)
            if resolved_url != url:
                logger.info(f"🔄 URL resolvida: {resolved_url}")
                url = resolved_url
        except Exception as e:
            logger.warning(f"⚠️ Erro ao resolver URL: {e}")
        
        # Salva tentativa de extração
        salvar_etapa("extracao_tentativa", {
            "url": url,
            "context": context,
            "timestamp": time.time()
        }, categoria="pesquisa_web")
        
        # CORREÇÃO: Tenta cada camada apenas uma vez
        for i, (layer_name, layer_func) in enumerate(self.extraction_layers):
            try:
                logger.info(f"🔍 Tentando camada {i+1}/{len(self.extraction_layers)}: {layer_name}")
                
                start_time = time.time()
                result = layer_func(url, context)
                extraction_time = time.time() - start_time
                
                if result['success']:
                    # Valida qualidade
                    validation = content_quality_validator.validate_content(
                        result['content'], url, context
                    )
                    
                    # Verifica se atende critérios mínimos
                    if self._meets_quality_criteria(result, validation):
                        self.stats['layer_usage'][layer_name] += 1
                        self.stats['successful_extractions'] += 1
                        
                        # Classifica qualidade
                        quality_class = self._classify_quality(validation['score'])
                        self.stats['quality_distribution'][quality_class] += 1
                        
                        # Adiciona metadados
                        result.update({
                            'extraction_layer': layer_name,
                            'extraction_time': extraction_time,
                            'quality_validation': validation,
                            'meets_criteria': True
                        })
                        
                        # Salva extração bem-sucedida
                        salvar_etapa("extracao_sucesso", {
                            "url": url,
                            "layer": layer_name,
                            "content_length": len(result['content']),
                            "quality_score": validation['score'],
                            "extraction_time": extraction_time
                        }, categoria="pesquisa_web")
                        
                        logger.info(f"✅ Extração bem-sucedida com {layer_name}: {len(result['content'])} chars, qualidade {validation['score']:.1f}%")
                        return result
                    else:
                        logger.warning(f"⚠️ Camada {i+1} ({layer_name}) não atendeu critérios de qualidade")
                else:
                    logger.warning(f"⚠️ Camada {i+1} ({layer_name}) falhou: {result.get('error', 'Erro desconhecido')}")
                    
            except Exception as e:
                logger.error(f"❌ Erro na camada {i+1} ({layer_name}): {e}")
                salvar_erro(f"extracao_{layer_name}", e, contexto={"url": url})
        
        # Todas as camadas falharam
        self.stats['quality_distribution']['failed'] += 1
        
        error_result = {
            'success': False,
            'error': 'Todas as camadas de extração falharam',
            'content': None,
            'url': url,
            'layers_attempted': len(self.extraction_layers)
        }
        
        # Salva falha total
        salvar_erro("extracao_total_falha", Exception("Todas as camadas falharam"), contexto={"url": url})
        
        logger.error(f"❌ FALHA TOTAL: Todas as camadas falharam para {url}")
        return error_result
    
    def _extract_static_content(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Camada 1: Extração estática tradicional"""
        
        try:
            content = robust_content_extractor.extract_content(url)
            
            if content:
                return {
                    'success': True,
                    'content': content,
                    'method': 'static_robust',
                    'url': url
                }
            else:
                return {
                    'success': False,
                    'error': 'Extração estática não retornou conteúdo',
                    'content': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro na extração estática: {str(e)}',
                'content': None
            }
    
    def _extract_dynamic_content(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Camada 2: Extração dinâmica com Playwright"""
        
        if not playwright_extractor.available:
            return {
                'success': False,
                'error': 'Playwright não disponível',
                'content': None
            }
        
        try:
            result = playwright_extractor.extract_content_sync(url)
            
            if result['success']:
                return {
                    'success': True,
                    'content': result['content'],
                    'method': 'playwright_dynamic',
                    'url': url,
                    'page_type': result.get('page_type'),
                    'metadata': result.get('metadata', {})
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Extração dinâmica falhou'),
                    'content': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro na extração dinâmica: {str(e)}',
                'content': None
            }
    
    def _extract_aggressive_content(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Camada 3: Extração agressiva com múltiplas tentativas"""
        
        try:
            import requests
            from bs4 import BeautifulSoup
            import re
            
            # Múltiplas tentativas com diferentes configurações
            session = requests.Session()
            
            # Headers mais agressivos
            aggressive_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
            
            session.headers.update(aggressive_headers)
            
            # Tentativas com diferentes configurações
            attempts = [
                {'timeout': 30, 'verify': False, 'allow_redirects': True},
                {'timeout': 20, 'verify': True, 'allow_redirects': True},
                {'timeout': 15, 'verify': False, 'allow_redirects': False}
            ]
            
            for i, config in enumerate(attempts, 1):
                try:
                    logger.info(f"🔄 Tentativa agressiva {i}/{len(attempts)}")
                    
                    response = session.get(url, **config)
                    
                    if response.status_code == 200:
                        # Detecta encoding
                        if response.encoding is None:
                            response.encoding = 'utf-8'
                        
                        html = response.text
                        
                        if len(html) > 1000:  # HTML substancial
                            # Extração agressiva com BeautifulSoup
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Remove apenas elementos críticos
                            for element in soup(['script', 'style', 'noscript']):
                                element.decompose()
                            
                            # Extrai todo texto disponível
                            all_text = soup.get_text()
                            
                            # Filtra e limpa
                            lines = all_text.split('\n')
                            meaningful_lines = []
                            
                            for line in lines:
                                line = line.strip()
                                if (len(line) > 20 and  # Linha substancial
                                    not re.match(r'^[\s\W]*$', line) and  # Não só símbolos
                                    not line.lower().startswith(('menu', 'nav', 'footer', 'header'))):
                                    meaningful_lines.append(line)
                            
                            if meaningful_lines:
                                content = '\n'.join(meaningful_lines)
                                
                                if len(content) > 200:  # Conteúdo mínimo
                                    return {
                                        'success': True,
                                        'content': content,
                                        'method': f'aggressive_attempt_{i}',
                                        'url': url,
                                        'html_length': len(html)
                                    }
                    
                    time.sleep(1)  # Delay entre tentativas
                    
                except Exception as e:
                    logger.warning(f"⚠️ Tentativa agressiva {i} falhou: {e}")
                    continue
            
            return {
                'success': False,
                'error': 'Todas as tentativas agressivas falharam',
                'content': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro na extração agressiva: {str(e)}',
                'content': None
            }
    
    def _extract_fallback_content(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Camada 4: Extração de fallback com técnicas alternativas"""
        
        try:
            import requests
            from urllib.parse import urlparse
            
            # Tenta diferentes abordagens de fallback
            fallback_strategies = [
                self._try_mobile_version,
                self._try_amp_version,
                self._try_cached_version,
                self._try_alternative_endpoints
            ]
            
            for strategy in fallback_strategies:
                try:
                    result = strategy(url, context)
                    if result['success']:
                        return result
                except Exception as e:
                    logger.warning(f"⚠️ Estratégia de fallback falhou: {e}")
                    continue
            
            return {
                'success': False,
                'error': 'Todas as estratégias de fallback falharam',
                'content': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro no fallback: {str(e)}',
                'content': None
            }
    
    def _try_mobile_version(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Tenta versão mobile do site"""
        
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urlparse
            
            parsed = urlparse(url)
            
            # Tenta URLs mobile comuns
            mobile_urls = [
                f"https://m.{parsed.netloc}{parsed.path}",
                f"https://mobile.{parsed.netloc}{parsed.path}",
                url.replace('www.', 'm.')
            ]
            
            mobile_headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
            }
            
            for mobile_url in mobile_urls:
                try:
                    response = requests.get(mobile_url, headers=mobile_headers, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Remove elementos desnecessários
                        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                            element.decompose()
                        
                        text = soup.get_text()
                        
                        if len(text) > 200:
                            return {
                                'success': True,
                                'content': text,
                                'method': 'mobile_version',
                                'mobile_url': mobile_url,
                                'url': url
                            }
                            
                except Exception as e:
                    continue
            
            return {'success': False, 'error': 'Versões mobile não disponíveis'}
            
        except Exception as e:
            return {'success': False, 'error': f'Erro na versão mobile: {str(e)}'}
    
    def _try_amp_version(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Tenta versão AMP do site"""
        
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urlparse
            
            parsed = urlparse(url)
            
            # URLs AMP comuns
            amp_urls = [
                f"https://amp.{parsed.netloc}{parsed.path}",
                f"{url}/amp",
                f"{url}?amp=1",
                url.replace('www.', 'amp.')
            ]
            
            for amp_url in amp_urls:
                try:
                    response = requests.get(amp_url, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # AMP tem estrutura mais limpa
                        amp_content = soup.find('amp-story') or soup.find('article') or soup.find('main')
                        
                        if amp_content:
                            text = amp_content.get_text()
                            
                            if len(text) > 200:
                                return {
                                    'success': True,
                                    'content': text,
                                    'method': 'amp_version',
                                    'amp_url': amp_url,
                                    'url': url
                                }
                                
                except Exception as e:
                    continue
            
            return {'success': False, 'error': 'Versões AMP não disponíveis'}
            
        except Exception as e:
            return {'success': False, 'error': f'Erro na versão AMP: {str(e)}'}
    
    def _try_cached_version(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Tenta versão em cache (Google Cache, Archive.org)"""
        
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import quote
            
            # URLs de cache
            cache_urls = [
                f"https://webcache.googleusercontent.com/search?q=cache:{quote(url)}",
                f"https://web.archive.org/web/{url}"
            ]
            
            for cache_url in cache_urls:
                try:
                    response = requests.get(cache_url, timeout=20)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Remove elementos de cache
                        for element in soup(['script', 'style', '.cache-header', '#cache-info']):
                            element.decompose()
                        
                        text = soup.get_text()
                        
                        if len(text) > 200:
                            return {
                                'success': True,
                                'content': text,
                                'method': 'cached_version',
                                'cache_url': cache_url,
                                'url': url
                            }
                            
                except Exception as e:
                    continue
            
            return {'success': False, 'error': 'Versões em cache não disponíveis'}
            
        except Exception as e:
            return {'success': False, 'error': f'Erro na versão cache: {str(e)}'}
    
    def _try_alternative_endpoints(self, url: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Tenta endpoints alternativos (RSS, API, sitemap)"""
        
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin, urlparse
            
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Endpoints alternativos
            alternative_endpoints = [
                f"{base_url}/rss",
                f"{base_url}/feed",
                f"{base_url}/rss.xml",
                f"{base_url}/feed.xml",
                f"{base_url}/sitemap.xml",
                f"{base_url}/api/content",
                f"{base_url}/content.json"
            ]
            
            for endpoint in alternative_endpoints:
                try:
                    response = requests.get(endpoint, timeout=10)
                    
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '').lower()
                        
                        if 'xml' in content_type:
                            # Parse XML/RSS
                            soup = BeautifulSoup(response.content, 'xml')
                            
                            # Extrai conteúdo de RSS/XML
                            items = soup.find_all(['item', 'entry', 'url'])
                            
                            if items:
                                texts = []
                                for item in items[:10]:  # Primeiros 10 itens
                                    title = item.find(['title', 'headline'])
                                    description = item.find(['description', 'summary', 'content'])
                                    
                                    if title:
                                        texts.append(title.get_text())
                                    if description:
                                        texts.append(description.get_text())
                                
                                if texts:
                                    combined_text = '\n\n'.join(texts)
                                    
                                    if len(combined_text) > 200:
                                        return {
                                            'success': True,
                                            'content': combined_text,
                                            'method': 'xml_feed',
                                            'endpoint': endpoint,
                                            'url': url
                                        }
                        
                        elif 'json' in content_type:
                            # Parse JSON
                            try:
                                import json
                                data = response.json()
                                
                                # Extrai texto de estruturas JSON comuns
                                text_fields = ['content', 'text', 'body', 'description', 'summary']
                                extracted_texts = []
                                
                                def extract_text_recursive(obj):
                                    if isinstance(obj, dict):
                                        for key, value in obj.items():
                                            if key.lower() in text_fields and isinstance(value, str):
                                                extracted_texts.append(value)
                                            elif isinstance(value, (dict, list)):
                                                extract_text_recursive(value)
                                    elif isinstance(obj, list):
                                        for item in obj:
                                            extract_text_recursive(item)
                                
                                extract_text_recursive(data)
                                
                                if extracted_texts:
                                    combined_text = '\n\n'.join(extracted_texts)
                                    
                                    if len(combined_text) > 200:
                                        return {
                                            'success': True,
                                            'content': combined_text,
                                            'method': 'json_api',
                                            'endpoint': endpoint,
                                            'url': url
                                        }
                                        
                            except json.JSONDecodeError:
                                continue
                                
                except Exception as e:
                    continue
            
            return {'success': False, 'error': 'Endpoints alternativos não disponíveis'}
            
        except Exception as e:
            return {'success': False, 'error': f'Erro nos endpoints alternativos: {str(e)}'}
    
    def _meets_quality_criteria(self, result: Dict[str, Any], validation: Dict[str, Any]) -> bool:
        """Verifica se resultado atende critérios de qualidade"""
        
        if not result['success'] or not result['content']:
            return False
        
        content = result['content']
        
        # Critérios básicos
        if len(content) < self.quality_thresholds['min_content_length']:
            return False
        
        if len(content.split()) < self.quality_thresholds['min_word_count']:
            return False
        
        if not validation['valid']:
            return False
        
        if validation['score'] < self.quality_thresholds['min_quality_score']:
            return False
        
        return True
    
    def _classify_quality(self, score: float) -> str:
        """Classifica qualidade do conteúdo"""
        
        if score >= 80:
            return 'high'
        elif score >= 60:
            return 'medium'
        elif score >= 40:
            return 'low'
        else:
            return 'failed'
    
    def batch_extract_multilayer(self, urls: List[str], context: Dict[str, Any] = None, max_workers: int = 3) -> Dict[str, Dict[str, Any]]:
        """Extrai múltiplas URLs usando sistema multi-camadas"""
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.extract_with_multiple_strategies, url, context): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results[url] = result
                except Exception as e:
                    results[url] = {
                        'success': False,
                        'error': f'Erro na extração paralela: {str(e)}',
                        'content': None
                    }
        
        # Estatísticas do lote
        successful = sum(1 for result in results.values() if result['success'])
        total = len(results)
        
        logger.info(f"📊 Extração multi-camadas em lote: {successful}/{total} sucessos ({successful/total*100:.1f}%)")
        
        return results
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas abrangentes"""
        
        total = self.stats['total_attempts']
        success_rate = (self.stats['successful_extractions'] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            'success_rate': success_rate,
            'layer_efficiency': {
                layer: (usage / total * 100) if total > 0 else 0 
                for layer, usage in self.stats['layer_usage'].items()
            },
            'quality_percentages': {
                quality: (count / total * 100) if total > 0 else 0
                for quality, count in self.stats['quality_distribution'].items()
            }
        }
    
    def reset_stats(self):
        """Reset estatísticas"""
        self.stats = {
            'total_attempts': 0,
            'successful_extractions': 0,
            'layer_usage': {layer[0]: 0 for layer in self.extraction_layers},
            'quality_distribution': {'high': 0, 'medium': 0, 'low': 0, 'failed': 0}
        }
        logger.info("🔄 Estatísticas do extrator multi-camadas resetadas")

# Instância global
multi_layer_extractor = MultiLayerExtractor()