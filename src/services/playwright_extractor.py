#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Playwright Extractor
Extrator avançado para páginas dinâmicas usando Playwright
"""

import os
import logging
import time
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

# Import condicional do Playwright
try:
    from playwright.async_api import async_playwright, Browser, Page
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

class PlaywrightExtractor:
    """Extrator avançado para páginas dinâmicas com JavaScript"""
    
    def __init__(self):
        """Inicializa o extrator Playwright"""
        self.available = HAS_PLAYWRIGHT
        self.browser = None
        self.context = None
        
        # Configurações otimizadas
        self.browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding'
        ]
        
        self.page_timeout = 30000  # 30 segundos
        self.wait_timeout = 10000  # 10 segundos para elementos
        
        self.stats = {
            'total_extractions': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'dynamic_pages_handled': 0,
            'js_heavy_pages': 0,
            'auth_pages_detected': 0
        }
        
        if self.available:
            logger.info("✅ Playwright Extractor inicializado")
        else:
            logger.warning("⚠️ Playwright não disponível - instale com: pip install playwright && playwright install")
    
    async def extract_dynamic_content(self, url: str, wait_for_content: bool = True) -> Dict[str, Any]:
        """Extrai conteúdo de páginas dinâmicas"""
        
        if not self.available:
            return {
                'success': False,
                'error': 'Playwright não disponível',
                'content': None
            }
        
        self.stats['total_extractions'] += 1
        
        try:
            # Inicia browser se necessário
            if not self.browser:
                await self._init_browser()
            
            # Cria nova página
            page = await self.context.new_page()
            
            try:
                # Configura timeouts
                page.set_default_timeout(self.page_timeout)
                
                # Intercepta requests para otimizar
                await page.route("**/*.{png,jpg,jpeg,gif,svg,ico,woff,woff2}", lambda route: route.abort())
                
                logger.info(f"🌐 Navegando para: {url}")
                
                # Navega para a página
                response = await page.goto(url, wait_until='domcontentloaded')
                
                if not response or response.status >= 400:
                    return {
                        'success': False,
                        'error': f'HTTP {response.status if response else "No response"}',
                        'content': None
                    }
                
                # Detecta tipo de página
                page_type = await self._detect_page_type(page)
                logger.info(f"🔍 Tipo de página detectado: {page_type}")
                
                # Aguarda carregamento baseado no tipo
                if page_type == 'dynamic':
                    await self._wait_for_dynamic_content(page)
                    self.stats['dynamic_pages_handled'] += 1
                elif page_type == 'js_heavy':
                    await self._wait_for_js_content(page)
                    self.stats['js_heavy_pages'] += 1
                elif page_type == 'auth_required':
                    self.stats['auth_pages_detected'] += 1
                    return {
                        'success': False,
                        'error': 'Página requer autenticação',
                        'content': None,
                        'page_type': page_type
                    }
                
                # Extrai conteúdo principal
                content = await self._extract_main_content(page)
                
                # Extrai metadados
                metadata = await self._extract_metadata(page)
                
                if content and len(content) > 100:
                    self.stats['successful_extractions'] += 1
                    
                    return {
                        'success': True,
                        'content': content,
                        'metadata': metadata,
                        'page_type': page_type,
                        'url': url,
                        'extraction_method': 'playwright'
                    }
                else:
                    self.stats['failed_extractions'] += 1
                    return {
                        'success': False,
                        'error': 'Conteúdo insuficiente extraído',
                        'content': content,
                        'metadata': metadata
                    }
                
            finally:
                await page.close()
                
        except Exception as e:
            self.stats['failed_extractions'] += 1
            logger.error(f"❌ Erro na extração Playwright: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    async def _init_browser(self):
        """Inicializa browser Playwright"""
        try:
            try:
                self.playwright = await async_playwright().start()
                
                # Usa Chromium para melhor compatibilidade
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=self.browser_args
                )
            except Exception as browser_error:
                logger.error(f"❌ Playwright não disponível: {browser_error}")
                self.available = False
                return None
            
            # Cria contexto com configurações otimizadas
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='pt-BR',
                timezone_id='America/Sao_Paulo',
                extra_http_headers={
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
                }
            )
            
            logger.info("✅ Browser Playwright inicializado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar browser: {e}")
            self.available = False
            raise
    
    async def _detect_page_type(self, page: Page) -> str:
        """Detecta tipo de página para estratégia de extração"""
        
        try:
            # Verifica se é página de autenticação
            auth_indicators = await page.evaluate("""
                () => {
                    const text = document.body.innerText.toLowerCase();
                    const authKeywords = ['login', 'sign in', 'entrar', 'fazer login', 'autenticação', 'senha', 'password'];
                    return authKeywords.some(keyword => text.includes(keyword));
                }
            """)
            
            if auth_indicators:
                return 'auth_required'
            
            # Verifica se é página dinâmica (React, Angular, Vue)
            dynamic_indicators = await page.evaluate("""
                () => {
                    return !!(window.React || window.angular || window.Vue || 
                             document.querySelector('[data-reactroot]') ||
                             document.querySelector('[ng-app]') ||
                             document.querySelector('[data-v-]'));
                }
            """)
            
            if dynamic_indicators:
                return 'dynamic'
            
            # Verifica se é página pesada em JS
            js_heavy = await page.evaluate("""
                () => {
                    const scripts = document.querySelectorAll('script').length;
                    const text = document.body.innerText;
                    return scripts > 10 && text.length < 500;
                }
            """)
            
            if js_heavy:
                return 'js_heavy'
            
            return 'static'
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao detectar tipo de página: {e}")
            return 'unknown'
    
    async def _wait_for_dynamic_content(self, page: Page):
        """Aguarda carregamento de conteúdo dinâmico"""
        
        try:
            # Aguarda elementos comuns de conteúdo
            content_selectors = [
                'main', 'article', '.content', '#content', 
                '.post', '.article', '.entry', '.text-content',
                '[role="main"]', '[role="article"]'
            ]
            
            for selector in content_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    logger.info(f"✅ Conteúdo dinâmico carregado: {selector}")
                    break
                except:
                    continue
            
            # Aguarda estabilização do DOM
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            # Aguarda um pouco mais para renderização
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.warning(f"⚠️ Timeout aguardando conteúdo dinâmico: {e}")
    
    async def _wait_for_js_content(self, page: Page):
        """Aguarda carregamento de conteúdo JavaScript"""
        
        try:
            # Aguarda que o body tenha conteúdo substancial
            await page.wait_for_function("""
                () => {
                    const text = document.body.innerText;
                    return text && text.length > 200;
                }
            """, timeout=15000)
            
            logger.info("✅ Conteúdo JavaScript carregado")
            
        except Exception as e:
            logger.warning(f"⚠️ Timeout aguardando conteúdo JS: {e}")
    
    async def _extract_main_content(self, page: Page) -> Optional[str]:
        """Extrai conteúdo principal da página"""
        
        try:
            # Estratégias de extração em ordem de prioridade
            extraction_strategies = [
                # Estratégia 1: Elementos semânticos
                """
                () => {
                    const main = document.querySelector('main');
                    if (main) return main.innerText;
                    
                    const article = document.querySelector('article');
                    if (article) return article.innerText;
                    
                    return null;
                }
                """,
                
                # Estratégia 2: Seletores de conteúdo
                """
                () => {
                    const selectors = ['.content', '#content', '.post-content', '.article-content', '.entry-content'];
                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element && element.innerText.length > 200) {
                            return element.innerText;
                        }
                    }
                    return null;
                }
                """,
                
                # Estratégia 3: Maior bloco de texto
                """
                () => {
                    const elements = document.querySelectorAll('div, section, article');
                    let maxText = '';
                    let maxLength = 0;
                    
                    elements.forEach(el => {
                        const text = el.innerText;
                        if (text && text.length > maxLength && text.length > 200) {
                            maxLength = text.length;
                            maxText = text;
                        }
                    });
                    
                    return maxText || null;
                }
                """,
                
                # Estratégia 4: Body completo (filtrado)
                """
                () => {
                    // Remove elementos de navegação
                    const toRemove = document.querySelectorAll('nav, header, footer, aside, .menu, .navigation, .sidebar');
                    toRemove.forEach(el => el.remove());
                    
                    return document.body.innerText;
                }
                """
            ]
            
            for i, strategy in enumerate(extraction_strategies, 1):
                try:
                    content = await page.evaluate(strategy)
                    
                    if content and len(content.strip()) > 200:
                        logger.info(f"✅ Conteúdo extraído com estratégia {i}: {len(content)} caracteres")
                        return self._clean_extracted_content(content)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Estratégia {i} falhou: {e}")
                    continue
            
            logger.warning("⚠️ Todas as estratégias de extração falharam")
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro na extração de conteúdo: {e}")
            return None
    
    async def _extract_metadata(self, page: Page) -> Dict[str, Any]:
        """Extrai metadados da página"""
        
        try:
            metadata = await page.evaluate("""
                () => {
                    const title = document.title || '';
                    const description = document.querySelector('meta[name="description"]')?.content || '';
                    const keywords = document.querySelector('meta[name="keywords"]')?.content || '';
                    const author = document.querySelector('meta[name="author"]')?.content || '';
                    const canonical = document.querySelector('link[rel="canonical"]')?.href || '';
                    
                    return {
                        title,
                        description,
                        keywords,
                        author,
                        canonical,
                        url: window.location.href
                    };
                }
            """)
            
            # Adiciona informações de extração
            metadata.update({
                'extraction_timestamp': datetime.now().isoformat(),
                'extraction_method': 'playwright',
                'page_load_time': await page.evaluate('performance.timing.loadEventEnd - performance.timing.navigationStart')
            })
            
            return metadata
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair metadados: {e}")
            return {}
    
    def _clean_extracted_content(self, content: str) -> str:
        """Limpa conteúdo extraído"""
        
        if not content:
            return ""
        
        # Remove quebras de linha excessivas
        import re
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Remove espaços excessivos
        content = re.sub(r'[ \t]+', ' ', content)
        
        # Remove caracteres de controle
        content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
        
        # Filtra linhas significativas
        lines = content.split('\n')
        meaningful_lines = []
        
        for line in lines:
            line = line.strip()
            if (len(line) > 15 and  # Linha substancial
                not line.lower() in ['menu', 'home', 'contato', 'sobre', 'login', 'cadastro'] and
                not re.match(r'^[\s\W]*$', line)):  # Não só símbolos
                meaningful_lines.append(line)
        
        content = '\n'.join(meaningful_lines)
        
        # Limita tamanho
        if len(content) > 15000:
            content = content[:15000] + "... [conteúdo truncado para otimização]"
        
        return content.strip()
    
    def extract_content_sync(self, url: str) -> Dict[str, Any]:
        """Versão síncrona para compatibilidade"""
        
        try:
            # Executa em loop de eventos
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(self.extract_dynamic_content(url))
                return result
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"❌ Erro na extração síncrona: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    async def batch_extract(self, urls: List[str]) -> Dict[str, Dict[str, Any]]:
        """Extrai conteúdo de múltiplas URLs em paralelo"""
        
        if not self.available:
            return {}
        
        try:
            if not self.browser:
                await self._init_browser()
            
            # Limita concorrência para não sobrecarregar
            semaphore = asyncio.Semaphore(3)
            
            async def extract_with_semaphore(url):
                async with semaphore:
                    return await self.extract_dynamic_content(url)
            
            # Executa extrações em paralelo
            tasks = [extract_with_semaphore(url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Organiza resultados
            batch_results = {}
            for url, result in zip(urls, results):
                if isinstance(result, Exception):
                    batch_results[url] = {
                        'success': False,
                        'error': str(result),
                        'content': None
                    }
                else:
                    batch_results[url] = result
            
            return batch_results
            
        except Exception as e:
            logger.error(f"❌ Erro na extração em lote: {e}")
            return {}
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do extrator"""
        
        total = self.stats['total_extractions']
        success_rate = (self.stats['successful_extractions'] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            'success_rate': success_rate,
            'available': self.available,
            'browser_active': self.browser is not None
        }
    
    async def close(self):
        """Fecha browser e limpa recursos"""
        
        try:
            if self.context:
                await self.context.close()
                self.context = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            
            logger.info("✅ Playwright Extractor fechado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao fechar Playwright: {e}")

# Instância global
playwright_extractor = PlaywrightExtractor()

# Função de conveniência síncrona
def extract_dynamic_content(url: str) -> Dict[str, Any]:
    """Função de conveniência para extração dinâmica"""
    return playwright_extractor.extract_content_sync(url)