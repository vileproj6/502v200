#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Selenium Extractor
Extrator alternativo usando Selenium para páginas complexas
"""

import os
import logging
import time
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Import condicional do Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

class SeleniumExtractor:
    """Extrator usando Selenium para páginas JavaScript pesadas"""
    
    def __init__(self):
        """Inicializa o extrator Selenium"""
        self.available = HAS_SELENIUM
        self.driver = None
        
        # Configurações do Chrome
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-logging')
        self.chrome_options.add_argument('--disable-web-security')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.wait_timeout = 20  # segundos
        
        self.stats = {
            'total_extractions': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'js_pages_handled': 0,
            'auth_pages_detected': 0
        }
        
        if self.available:
            logger.info("✅ Selenium Extractor inicializado")
        else:
            logger.warning("⚠️ Selenium não disponível - instale com: pip install selenium webdriver-manager")
    
    def extract_js_heavy_content(self, url: str) -> Dict[str, Any]:
        """Extrai conteúdo de páginas JavaScript pesadas"""
        
        if not self.available:
            return {
                'success': False,
                'error': 'Selenium não disponível',
                'content': None
            }
        
        self.stats['total_extractions'] += 1
        
        try:
            # Inicializa driver se necessário
            if not self.driver:
                self._init_driver()
            
            logger.info(f"🌐 Navegando com Selenium para: {url}")
            
            # Navega para a página
            self.driver.get(url)
            
            # Aguarda carregamento inicial
            time.sleep(3)
            
            # Detecta tipo de página
            page_type = self._detect_page_type_selenium()
            
            if page_type == 'auth_required':
                self.stats['auth_pages_detected'] += 1
                return {
                    'success': False,
                    'error': 'Página requer autenticação',
                    'content': None,
                    'page_type': page_type
                }
            
            # Aguarda carregamento de conteúdo JavaScript
            if page_type == 'js_heavy':
                self._wait_for_js_content_selenium()
                self.stats['js_pages_handled'] += 1
            
            # Extrai conteúdo
            content = self._extract_content_selenium()
            
            if content and len(content) > 200:
                self.stats['successful_extractions'] += 1
                
                return {
                    'success': True,
                    'content': content,
                    'method': 'selenium',
                    'page_type': page_type,
                    'url': url,
                    'extraction_timestamp': datetime.now().isoformat()
                }
            else:
                self.stats['failed_extractions'] += 1
                return {
                    'success': False,
                    'error': 'Conteúdo insuficiente extraído',
                    'content': content,
                    'page_type': page_type
                }
                
        except Exception as e:
            self.stats['failed_extractions'] += 1
            logger.error(f"❌ Erro na extração Selenium: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    def _init_driver(self):
        """Inicializa driver Selenium"""
        
        try:
            # Usa WebDriver Manager para gerenciar ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            
            # Configurações adicionais
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            
            logger.info("✅ Driver Selenium inicializado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar driver Selenium: {e}")
            raise
    
    def _detect_page_type_selenium(self) -> str:
        """Detecta tipo de página usando Selenium"""
        
        try:
            # Verifica indicadores de autenticação
            auth_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'login') or contains(text(), 'sign in') or contains(text(), 'entrar')]")
            
            if auth_elements:
                return 'auth_required'
            
            # Verifica se é página JavaScript pesada
            script_tags = self.driver.find_elements(By.TAG_NAME, 'script')
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            
            if len(script_tags) > 15 and len(body_text) < 500:
                return 'js_heavy'
            
            return 'normal'
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao detectar tipo de página: {e}")
            return 'unknown'
    
    def _wait_for_js_content_selenium(self):
        """Aguarda carregamento de conteúdo JavaScript"""
        
        try:
            # Aguarda que o body tenha conteúdo substancial
            wait = WebDriverWait(self.driver, self.wait_timeout)
            
            # Aguarda elementos comuns de conteúdo
            content_selectors = [
                (By.TAG_NAME, 'main'),
                (By.TAG_NAME, 'article'),
                (By.CLASS_NAME, 'content'),
                (By.ID, 'content'),
                (By.CLASS_NAME, 'post'),
                (By.CLASS_NAME, 'article')
            ]
            
            for selector_type, selector_value in content_selectors:
                try:
                    wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                    logger.info(f"✅ Conteúdo JavaScript carregado: {selector_value}")
                    break
                except:
                    continue
            
            # Aguarda estabilização
            time.sleep(5)
            
            # Verifica se o conteúdo realmente carregou
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            
            if len(body_text) < 200:
                # Aguarda mais um pouco
                time.sleep(5)
            
        except Exception as e:
            logger.warning(f"⚠️ Timeout aguardando conteúdo JavaScript: {e}")
    
    def _extract_content_selenium(self) -> Optional[str]:
        """Extrai conteúdo usando Selenium"""
        
        try:
            # Estratégias de extração em ordem de prioridade
            extraction_strategies = [
                self._extract_semantic_elements,
                self._extract_content_divs,
                self._extract_largest_text_block,
                self._extract_full_body
            ]
            
            for strategy in extraction_strategies:
                try:
                    content = strategy()
                    
                    if content and len(content.strip()) > 200:
                        logger.info(f"✅ Conteúdo extraído com {strategy.__name__}: {len(content)} caracteres")
                        return self._clean_selenium_content(content)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Estratégia {strategy.__name__} falhou: {e}")
                    continue
            
            logger.warning("⚠️ Todas as estratégias de extração Selenium falharam")
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro na extração Selenium: {e}")
            return None
    
    def _extract_semantic_elements(self) -> Optional[str]:
        """Extrai usando elementos semânticos"""
        
        semantic_selectors = ['main', 'article', 'section[role="main"]']
        
        for selector in semantic_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    texts = []
                    for element in elements:
                        text = element.text
                        if len(text) > 100:
                            texts.append(text)
                    
                    if texts:
                        return '\n\n'.join(texts)
                        
            except Exception as e:
                continue
        
        return None
    
    def _extract_content_divs(self) -> Optional[str]:
        """Extrai usando divs de conteúdo"""
        
        content_selectors = [
            '.content', '#content', '.post-content', '.article-content',
            '.entry-content', '.page-content', '.text-content', '.main-content'
        ]
        
        for selector in content_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    texts = []
                    for element in elements:
                        text = element.text
                        if len(text) > 100:
                            texts.append(text)
                    
                    if texts:
                        return '\n\n'.join(texts)
                        
            except Exception as e:
                continue
        
        return None
    
    def _extract_largest_text_block(self) -> Optional[str]:
        """Extrai o maior bloco de texto"""
        
        try:
            all_divs = self.driver.find_elements(By.TAG_NAME, 'div')
            
            largest_text = ""
            largest_size = 0
            
            for div in all_divs:
                try:
                    text = div.text
                    if len(text) > largest_size and len(text) > 200:
                        largest_size = len(text)
                        largest_text = text
                except:
                    continue
            
            return largest_text if largest_size > 200 else None
            
        except Exception as e:
            return None
    
    def _extract_full_body(self) -> Optional[str]:
        """Extrai todo o body como último recurso"""
        
        try:
            body = self.driver.find_element(By.TAG_NAME, 'body')
            return body.text
        except Exception as e:
            return None
    
    def _clean_selenium_content(self, content: str) -> str:
        """Limpa conteúdo extraído pelo Selenium"""
        
        if not content:
            return ""
        
        # Remove quebras de linha excessivas
        import re
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Remove espaços excessivos
        content = re.sub(r'[ \t]+', ' ', content)
        
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
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do extrator"""
        
        total = self.stats['total_extractions']
        success_rate = (self.stats['successful_extractions'] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            'success_rate': success_rate,
            'available': self.available,
            'driver_active': self.driver is not None
        }
    
    def close(self):
        """Fecha driver e limpa recursos"""
        
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            logger.info("✅ Selenium Extractor fechado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao fechar Selenium: {e}")

# Instância global
selenium_extractor = SeleniumExtractor()