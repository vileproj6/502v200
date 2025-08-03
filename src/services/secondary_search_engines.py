#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Secondary Search Engines
Motores de busca secundários para ampliar cobertura
"""

import logging
import time
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import json
import random

logger = logging.getLogger(__name__)

class SecondarySearchEngines:
    """Motores de busca secundários para máxima cobertura"""
    
    def __init__(self):
        """Inicializa motores secundários"""
        self.engines = {
            'yandex': {
                'enabled': True,
                'base_url': 'https://yandex.com/search/',
                'priority': 5,
                'error_count': 0
            },
            'baidu': {
                'enabled': True,
                'base_url': 'https://www.baidu.com/s',
                'priority': 6,
                'error_count': 0
            },
            'startpage': {
                'enabled': True,
                'base_url': 'https://www.startpage.com/sp/search',
                'priority': 7,
                'error_count': 0
            },
            'searx': {
                'enabled': True,
                'base_url': 'https://searx.org/search',
                'priority': 8,
                'error_count': 0
            },
            'ecosia': {
                'enabled': True,
                'base_url': 'https://www.ecosia.org/search',
                'priority': 9,
                'error_count': 0
            },
            'brazilian_sites': {
                'enabled': True,
                'sites': [
                    'https://www.uol.com.br/busca/',
                    'https://busca.terra.com.br/',
                    'https://www.bing.com/search?cc=br'
                ],
                'priority': 3,
                'error_count': 0
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        
        logger.info(f"Secondary Search Engines inicializado com {len(self.engines)} motores")
    
    def search_all_secondary_engines(self, query: str, max_results_per_engine: int = 10) -> List[Dict[str, Any]]:
        """Busca em todos os motores secundários"""
        
        all_results = []
        
        for engine_name, engine_config in self.engines.items():
            if not engine_config['enabled'] or engine_config['error_count'] >= 3:
                continue
            
            try:
                logger.info(f"🔍 Buscando em {engine_name}...")
                
                if engine_name == 'yandex':
                    results = self._search_yandex(query, max_results_per_engine)
                elif engine_name == 'baidu':
                    results = self._search_baidu(query, max_results_per_engine)
                elif engine_name == 'startpage':
                    results = self._search_startpage(query, max_results_per_engine)
                elif engine_name == 'searx':
                    results = self._search_searx(query, max_results_per_engine)
                elif engine_name == 'ecosia':
                    results = self._search_ecosia(query, max_results_per_engine)
                elif engine_name == 'brazilian_sites':
                    results = self._search_brazilian_sites(query, max_results_per_engine)
                else:
                    continue
                
                if results:
                    all_results.extend(results)
                    logger.info(f"✅ {engine_name}: {len(results)} resultados")
                else:
                    logger.warning(f"⚠️ {engine_name}: 0 resultados")
                
                # Delay entre motores
                time.sleep(random.uniform(1.0, 3.0))
                
            except Exception as e:
                logger.error(f"❌ Erro em {engine_name}: {str(e)}")
                self.engines[engine_name]['error_count'] += 1
                continue
        
        # Remove duplicatas
        unique_results = self._remove_duplicates(all_results)
        
        logger.info(f"📊 Busca secundária: {len(unique_results)} resultados únicos de {len(all_results)} totais")
        
        return unique_results
    
    def _search_yandex(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca no Yandex"""
        
        try:
            search_url = f"https://yandex.com/search/?text={quote_plus(query)}&lr=21"  # lr=21 = Brasil
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Yandex usa estrutura específica
                result_items = soup.find_all('li', class_='serp-item')
                
                for item in result_items[:max_results]:
                    title_elem = item.find('h2')
                    if title_elem:
                        link_elem = title_elem.find('a')
                        if link_elem:
                            title = title_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            # Yandex às vezes usa URLs relativas
                            if url.startswith('/'):
                                url = 'https://yandex.com' + url
                            
                            snippet_elem = item.find('div', class_='text-container')
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            
                            if url and title and url.startswith('http'):
                                results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': 'yandex'
                                })
                
                return results
            else:
                raise Exception(f"Yandex retornou status {response.status_code}")
                
        except Exception as e:
            raise e
    
    def _search_baidu(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca no Baidu (limitado fora da China)"""
        
        try:
            # Baidu tem limitações geográficas, mas tentamos
            search_url = f"https://www.baidu.com/s?wd={quote_plus(query)}"
            
            # Headers específicos para Baidu
            baidu_headers = {
                **self.headers,
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7'
            }
            
            response = requests.get(search_url, headers=baidu_headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Baidu usa estrutura específica
                result_items = soup.find_all('div', class_='result')
                
                for item in result_items[:max_results]:
                    title_elem = item.find('h3')
                    if title_elem:
                        link_elem = title_elem.find('a')
                        if link_elem:
                            title = title_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            snippet_elem = item.find('span', class_='content-right_8Zs40')
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            
                            if url and title and url.startswith('http'):
                                results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': 'baidu'
                                })
                
                return results
            else:
                raise Exception(f"Baidu retornou status {response.status_code}")
                
        except Exception as e:
            raise e
    
    def _search_startpage(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca no Startpage"""
        
        try:
            search_url = f"https://www.startpage.com/sp/search?query={quote_plus(query)}&language=portuguese"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Startpage usa estrutura específica
                result_items = soup.find_all('div', class_='w-gl__result')
                
                for item in result_items[:max_results]:
                    title_elem = item.find('h3')
                    if title_elem:
                        link_elem = title_elem.find('a')
                        if link_elem:
                            title = title_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            snippet_elem = item.find('p', class_='w-gl__description')
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            
                            if url and title and url.startswith('http'):
                                results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': 'startpage'
                                })
                
                return results
            else:
                raise Exception(f"Startpage retornou status {response.status_code}")
                
        except Exception as e:
            raise e
    
    def _search_searx(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca no SearX (instância pública)"""
        
        try:
            # Usa instância pública do SearX
            search_url = f"https://searx.org/search?q={quote_plus(query)}&format=json&language=pt-BR"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('results', [])[:max_results]:
                    title = item.get('title', '')
                    url = item.get('url', '')
                    snippet = item.get('content', '')
                    
                    if url and title and url.startswith('http'):
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'searx'
                        })
                
                return results
            else:
                raise Exception(f"SearX retornou status {response.status_code}")
                
        except Exception as e:
            raise e
    
    def _search_ecosia(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca no Ecosia"""
        
        try:
            search_url = f"https://www.ecosia.org/search?q={quote_plus(query)}&region=br"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Ecosia usa estrutura específica
                result_items = soup.find_all('div', class_='result')
                
                for item in result_items[:max_results]:
                    title_elem = item.find('a', class_='result__title')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        
                        snippet_elem = item.find('p', class_='result__snippet')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        if url and title and url.startswith('http'):
                            results.append({
                                'title': title,
                                'url': url,
                                'snippet': snippet,
                                'source': 'ecosia'
                            })
                
                return results
            else:
                raise Exception(f"Ecosia retornou status {response.status_code}")
                
        except Exception as e:
            raise e
    
    def _search_brazilian_sites(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca em sites brasileiros específicos"""
        
        all_results = []
        
        # Sites brasileiros para busca direta
        brazilian_search_sites = [
            {
                'name': 'UOL Busca',
                'url': f"https://busca.uol.com.br/web/?q={quote_plus(query)}",
                'selector': '.result'
            },
            {
                'name': 'Terra Busca',
                'url': f"https://busca.terra.com.br/Default.aspx?query={quote_plus(query)}",
                'selector': '.result-item'
            }
        ]
        
        for site in brazilian_search_sites:
            try:
                response = requests.get(site['url'], headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Busca resultados com seletor genérico
                    result_items = soup.find_all(['div', 'li'], class_=lambda x: x and 'result' in x.lower())
                    
                    for item in result_items[:max_results//len(brazilian_search_sites)]:
                        # Extrai título e URL de forma genérica
                        link_elem = item.find('a', href=True)
                        if link_elem:
                            title = link_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            # Extrai snippet
                            snippet_elem = item.find('p') or item.find('span')
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            
                            if url and title and url.startswith('http'):
                                all_results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': f"brazilian_{site['name'].lower().replace(' ', '_')}"
                                })
                
            except Exception as e:
                logger.warning(f"⚠️ Erro em {site['name']}: {e}")
                continue
        
        return all_results
    
    def search_academic_sources(self, query: str, max_results: int = 15) -> List[Dict[str, Any]]:
        """Busca em fontes acadêmicas e especializadas"""
        
        academic_results = []
        
        # Fontes acadêmicas e especializadas
        academic_sources = [
            {
                'name': 'Google Scholar',
                'url': f"https://scholar.google.com/scholar?q={quote_plus(query)}&hl=pt-BR",
                'selector': '.gs_rt'
            },
            {
                'name': 'ResearchGate',
                'url': f"https://www.researchgate.net/search?q={quote_plus(query)}",
                'selector': '.nova-legacy-v-publication-item'
            },
            {
                'name': 'SSRN',
                'url': f"https://www.ssrn.com/en/index.cfm/ssrn-search/?term={quote_plus(query)}",
                'selector': '.search-result'
            }
        ]
        
        for source in academic_sources:
            try:
                # Headers acadêmicos
                academic_headers = {
                    **self.headers,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
                
                response = requests.get(source['url'], headers=academic_headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Busca resultados acadêmicos
                    result_items = soup.find_all(['div', 'article'], class_=lambda x: x and any(
                        keyword in x.lower() for keyword in ['result', 'paper', 'publication', 'article']
                    ))
                    
                    for item in result_items[:max_results//len(academic_sources)]:
                        link_elem = item.find('a', href=True)
                        if link_elem:
                            title = link_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            # URLs relativas
                            if url.startswith('/'):
                                from urllib.parse import urljoin
                                url = urljoin(source['url'], url)
                            
                            snippet_elem = item.find(['p', 'div', 'span'], class_=lambda x: x and 'abstract' in x.lower() if x else False)
                            if not snippet_elem:
                                snippet_elem = item.find('p')
                            
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            
                            if url and title and url.startswith('http'):
                                academic_results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': f"academic_{source['name'].lower().replace(' ', '_')}",
                                    'type': 'academic'
                                })
                
            except Exception as e:
                logger.warning(f"⚠️ Erro em fonte acadêmica {source['name']}: {e}")
                continue
        
        return academic_results
    
    def search_news_sources(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Busca em fontes de notícias especializadas"""
        
        news_results = []
        
        # Fontes de notícias brasileiras
        news_sources = [
            {
                'name': 'Google News BR',
                'url': f"https://news.google.com/search?q={quote_plus(query)}&hl=pt-BR&gl=BR&ceid=BR:pt-419",
                'selector': 'article'
            },
            {
                'name': 'Valor Econômico',
                'url': f"https://valor.globo.com/busca/?q={quote_plus(query)}",
                'selector': '.result-item'
            },
            {
                'name': 'InfoMoney',
                'url': f"https://www.infomoney.com.br/busca/?q={quote_plus(query)}",
                'selector': '.search-result'
            },
            {
                'name': 'Exame',
                'url': f"https://exame.com/busca/?q={quote_plus(query)}",
                'selector': '.search-item'
            }
        ]
        
        for source in news_sources:
            try:
                response = requests.get(source['url'], headers=self.headers, timeout=12)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Busca artigos de notícias
                    result_items = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                        keyword in x.lower() for keyword in ['result', 'item', 'article', 'news']
                    ))
                    
                    for item in result_items[:max_results//len(news_sources)]:
                        link_elem = item.find('a', href=True)
                        if link_elem:
                            title = link_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            # URLs relativas
                            if url.startswith('/'):
                                from urllib.parse import urljoin
                                url = urljoin(source['url'], url)
                            
                            snippet_elem = item.find(['p', 'div'], class_=lambda x: x and 'summary' in x.lower() if x else False)
                            if not snippet_elem:
                                snippet_elem = item.find('p')
                            
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                            
                            if url and title and url.startswith('http'):
                                news_results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': f"news_{source['name'].lower().replace(' ', '_')}",
                                    'type': 'news'
                                })
                
            except Exception as e:
                logger.warning(f"⚠️ Erro em fonte de notícias {source['name']}: {e}")
                continue
        
        return news_results
    
    def search_specialized_databases(self, query: str, context: Dict[str, Any], max_results: int = 10) -> List[Dict[str, Any]]:
        """Busca em bases de dados especializadas"""
        
        segmento = context.get('segmento', '').lower()
        specialized_results = []
        
        # Bases especializadas por segmento
        if 'medicina' in segmento or 'saúde' in segmento:
            specialized_results.extend(self._search_medical_databases(query, max_results))
        
        if 'tecnologia' in segmento or 'digital' in segmento:
            specialized_results.extend(self._search_tech_databases(query, max_results))
        
        if 'negócios' in segmento or 'consultoria' in segmento:
            specialized_results.extend(self._search_business_databases(query, max_results))
        
        return specialized_results
    
    def _search_medical_databases(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca em bases médicas"""
        
        medical_results = []
        
        medical_sources = [
            {
                'name': 'CFM',
                'url': f"https://portal.cfm.org.br/busca/?q={quote_plus(query)}",
                'domain': 'portal.cfm.org.br'
            },
            {
                'name': 'ANVISA',
                'url': f"https://www.gov.br/anvisa/pt-br/busca?SearchableText={quote_plus(query)}",
                'domain': 'gov.br'
            },
            {
                'name': 'Ministério da Saúde',
                'url': f"https://www.gov.br/saude/pt-br/busca?SearchableText={quote_plus(query)}",
                'domain': 'gov.br'
            }
        ]
        
        for source in medical_sources:
            try:
                response = requests.get(source['url'], headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Busca resultados
                    result_items = soup.find_all(['div', 'article'], limit=max_results//len(medical_sources))
                    
                    for item in result_items:
                        link_elem = item.find('a', href=True)
                        if link_elem and source['domain'] in link_elem.get('href', ''):
                            title = link_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            if url.startswith('/'):
                                url = f"https://{source['domain']}{url}"
                            
                            snippet = item.get_text(strip=True)[:200]
                            
                            if url and title:
                                medical_results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': f"medical_{source['name'].lower()}",
                                    'type': 'specialized_medical'
                                })
                
            except Exception as e:
                logger.warning(f"⚠️ Erro em base médica {source['name']}: {e}")
                continue
        
        return medical_results
    
    def _search_tech_databases(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca em bases tecnológicas"""
        
        tech_results = []
        
        tech_sources = [
            {
                'name': 'TechCrunch',
                'url': f"https://techcrunch.com/search/{quote_plus(query)}/",
                'domain': 'techcrunch.com'
            },
            {
                'name': 'Wired',
                'url': f"https://www.wired.com/search/?q={quote_plus(query)}",
                'domain': 'wired.com'
            },
            {
                'name': 'MIT Technology Review',
                'url': f"https://www.technologyreview.com/search/?s={quote_plus(query)}",
                'domain': 'technologyreview.com'
            }
        ]
        
        for source in tech_sources:
            try:
                response = requests.get(source['url'], headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    result_items = soup.find_all(['article', 'div'], limit=max_results//len(tech_sources))
                    
                    for item in result_items:
                        link_elem = item.find('a', href=True)
                        if link_elem:
                            title = link_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            if url.startswith('/'):
                                url = f"https://{source['domain']}{url}"
                            
                            snippet = item.get_text(strip=True)[:200]
                            
                            if url and title and len(title) > 10:
                                tech_results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': f"tech_{source['name'].lower().replace(' ', '_')}",
                                    'type': 'specialized_tech'
                                })
                
            except Exception as e:
                logger.warning(f"⚠️ Erro em base tech {source['name']}: {e}")
                continue
        
        return tech_results
    
    def _search_business_databases(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca em bases de negócios"""
        
        business_results = []
        
        business_sources = [
            {
                'name': 'Harvard Business Review',
                'url': f"https://hbr.org/search?term={quote_plus(query)}",
                'domain': 'hbr.org'
            },
            {
                'name': 'McKinsey',
                'url': f"https://www.mckinsey.com/search?q={quote_plus(query)}",
                'domain': 'mckinsey.com'
            },
            {
                'name': 'BCG',
                'url': f"https://www.bcg.com/search?query={quote_plus(query)}",
                'domain': 'bcg.com'
            }
        ]
        
        for source in business_sources:
            try:
                response = requests.get(source['url'], headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    result_items = soup.find_all(['article', 'div'], limit=max_results//len(business_sources))
                    
                    for item in result_items:
                        link_elem = item.find('a', href=True)
                        if link_elem:
                            title = link_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            if url.startswith('/'):
                                url = f"https://{source['domain']}{url}"
                            
                            snippet = item.get_text(strip=True)[:200]
                            
                            if url and title and len(title) > 10:
                                business_results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet,
                                    'source': f"business_{source['name'].lower().replace(' ', '_')}",
                                    'type': 'specialized_business'
                                })
                
            except Exception as e:
                logger.warning(f"⚠️ Erro em base business {source['name']}: {e}")
                continue
        
        return business_results
    
    def _remove_duplicates(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove resultados duplicados"""
        
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Retorna status dos motores"""
        
        status = {}
        
        for engine_name, engine_config in self.engines.items():
            status[engine_name] = {
                'enabled': engine_config['enabled'],
                'available': engine_config['error_count'] < 3,
                'priority': engine_config['priority'],
                'error_count': engine_config['error_count']
            }
        
        return status
    
    def reset_engine_errors(self, engine_name: str = None):
        """Reset contadores de erro"""
        
        if engine_name and engine_name in self.engines:
            self.engines[engine_name]['error_count'] = 0
            logger.info(f"🔄 Reset erros do motor: {engine_name}")
        else:
            for engine in self.engines.values():
                engine['error_count'] = 0
            logger.info("🔄 Reset erros de todos os motores secundários")

# Instância global
secondary_search_engines = SecondarySearchEngines()