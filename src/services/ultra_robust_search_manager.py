#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Ultra Robust Search Manager
Gerenciador de busca ultra-robusto com múltiplas camadas e sistemas secundários
"""

import logging
import time
import asyncio
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.production_search_manager import production_search_manager
from services.secondary_search_engines import secondary_search_engines
from services.multi_layer_extractor import multi_layer_extractor
from services.url_filter_manager import url_filter_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class UltraRobustSearchManager:
    """Gerenciador de busca ultra-robusto com sistemas redundantes"""
    
    def __init__(self):
        """Inicializa o gerenciador ultra-robusto"""
        self.search_layers = [
            ('primary_engines', self._search_primary_engines),
            ('secondary_engines', self._search_secondary_engines),
            ('specialized_sources', self._search_specialized_sources),
            ('academic_sources', self._search_academic_sources),
            ('news_sources', self._search_news_sources)
        ]
        
        self.extraction_strategies = [
            ('multi_layer', multi_layer_extractor.extract_with_multiple_strategies),
            ('robust_static', self._extract_with_robust_static),
            ('emergency_extraction', self._emergency_extraction)
        ]
        
        self.quality_requirements = {
            'min_sources': 5,
            'min_total_content': 10000,
            'min_avg_quality': 60.0,
            'min_unique_domains': 3
        }
        
        self.stats = {
            'total_searches': 0,
            'successful_searches': 0,
            'total_extractions': 0,
            'successful_extractions': 0,
            'layer_performance': {},
            'quality_metrics': {}
        }
        
        logger.info("Ultra Robust Search Manager inicializado")
    
    def execute_comprehensive_search(
        self, 
        query: str, 
        context: Dict[str, Any],
        max_results: int = 50,
        require_high_quality: bool = True
    ) -> Dict[str, Any]:
        """Executa busca abrangente com múltiplas camadas"""
        
        self.stats['total_searches'] += 1
        
        logger.info(f"🚀 Iniciando busca ultra-robusta para: {query}")
        
        # Salva início da busca
        salvar_etapa("busca_iniciada", {
            "query": query,
            "context": context,
            "max_results": max_results,
            "timestamp": time.time()
        }, categoria="pesquisa_web")
        
        # Gera queries expandidas
        expanded_queries = self._generate_expanded_queries(query, context)
        
        # Salva queries expandidas
        salvar_etapa("queries_expandidas", {
            "original_query": query,
            "expanded_queries": expanded_queries
        }, categoria="pesquisa_web")
        
        # Executa busca em todas as camadas
        all_search_results = []
        
        for layer_name, layer_func in self.search_layers:
            try:
                logger.info(f"🔍 Executando camada: {layer_name}")
                
                layer_start_time = time.time()
                layer_results = layer_func(expanded_queries, max_results // len(self.search_layers))
                layer_time = time.time() - layer_start_time
                
                if layer_results:
                    all_search_results.extend(layer_results)
                    
                    # Salva resultados da camada
                    salvar_etapa(f"busca_{layer_name}", {
                        "layer": layer_name,
                        "results_count": len(layer_results),
                        "execution_time": layer_time,
                        "results": layer_results[:10]  # Primeiros 10 para economia de espaço
                    }, categoria="pesquisa_web")
                    
                    logger.info(f"✅ {layer_name}: {len(layer_results)} resultados em {layer_time:.2f}s")
                else:
                    logger.warning(f"⚠️ {layer_name}: 0 resultados")
                
                # Atualiza estatísticas da camada
                self.stats['layer_performance'][layer_name] = {
                    'results_count': len(layer_results),
                    'execution_time': layer_time,
                    'success': len(layer_results) > 0
                }
                
            except Exception as e:
                logger.error(f"❌ Erro na camada {layer_name}: {e}")
                salvar_erro(f"busca_{layer_name}", e, contexto={"query": query})
                continue
        
        # Remove duplicatas e aplica filtros
        filtered_results = self._filter_and_deduplicate(all_search_results)
        
        # Salva resultados filtrados
        salvar_etapa("resultados_filtrados", {
            "original_count": len(all_search_results),
            "filtered_count": len(filtered_results),
            "filter_stats": url_filter_manager.get_stats()
        }, categoria="pesquisa_web")
        
        # Executa extração de conteúdo em paralelo
        extracted_content = self._execute_parallel_extraction(filtered_results, context)
        
        # Valida qualidade final
        quality_validation = self._validate_search_quality(extracted_content)
        
        # Salva validação de qualidade
        salvar_etapa("validacao_qualidade_busca", quality_validation, categoria="pesquisa_web")
        
        # Compila resultado final
        final_result = {
            'query': query,
            'expanded_queries': expanded_queries,
            'search_results': filtered_results,
            'extracted_content': extracted_content,
            'quality_validation': quality_validation,
            'statistics': {
                'total_search_results': len(all_search_results),
                'filtered_results': len(filtered_results),
                'successful_extractions': len([c for c in extracted_content if c['success']]),
                'unique_domains': len(set(self._extract_domain(r['url']) for r in filtered_results)),
                'total_content_length': sum(len(c.get('content', '')) for c in extracted_content if c['success']),
                'avg_quality_score': self._calculate_avg_quality(extracted_content)
            },
            'layer_performance': self.stats['layer_performance'],
            'meets_quality_requirements': quality_validation['meets_requirements'],
            'timestamp': time.time()
        }
        
        # Salva resultado final
        salvar_etapa("busca_completa_final", final_result, categoria="pesquisa_web")
        
        if quality_validation['meets_requirements']:
            self.stats['successful_searches'] += 1
            logger.info(f"✅ Busca ultra-robusta concluída com sucesso: {len(extracted_content)} extrações")
        else:
            logger.warning(f"⚠️ Busca concluída mas não atende critérios de qualidade: {quality_validation['issues']}")
        
        return final_result
    
    def _generate_expanded_queries(self, original_query: str, context: Dict[str, Any]) -> List[str]:
        """Gera queries expandidas para máxima cobertura"""
        
        segmento = context.get('segmento', '')
        produto = context.get('produto', '')
        publico = context.get('publico', '')
        
        expanded_queries = [original_query]
        
        # Queries baseadas no contexto
        if segmento:
            expanded_queries.extend([
                f"mercado {segmento} Brasil 2024 dados estatísticas",
                f"análise competitiva {segmento} oportunidades",
                f"tendências {segmento} crescimento futuro",
                f"investimento {segmento} venture capital Brasil",
                f"regulamentação {segmento} mudanças legais",
                f"inovação {segmento} tecnologia disruptiva"
            ])
        
        if produto:
            expanded_queries.extend([
                f"demanda {produto} Brasil consumo",
                f"preço médio {produto} mercado brasileiro",
                f"concorrentes {produto} análise competitiva",
                f"cases sucesso {produto} empresas brasileiras"
            ])
        
        if publico:
            expanded_queries.extend([
                f"comportamento {publico} Brasil pesquisa",
                f"perfil demográfico {publico} dados IBGE",
                f"hábitos consumo {publico} tendências"
            ])
        
        # Queries de inteligência de mercado
        expanded_queries.extend([
            f"startups {original_query} unicórnios brasileiros",
            f"fusões aquisições {original_query} M&A Brasil",
            f"IPO {original_query} bolsa valores",
            f"pesquisa mercado {original_query} institutos",
            f"relatório setorial {original_query} consultorias"
        ])
        
        # Remove duplicatas e queries muito similares
        unique_queries = []
        for query in expanded_queries:
            if query not in unique_queries and len(query.split()) >= 3:
                unique_queries.append(query)
        
        return unique_queries[:15]  # Máximo 15 queries
    
    def _search_primary_engines(self, queries: List[str], max_results: int) -> List[Dict[str, Any]]:
        """Busca nos motores primários"""
        
        primary_results = []
        
        for query in queries[:8]:  # Primeiras 8 queries nos motores primários
            try:
                results = production_search_manager.search_with_fallback(query, max_results // len(queries))
                primary_results.extend(results)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca primária para '{query}': {e}")
                continue
        
        return primary_results
    
    def _search_secondary_engines(self, queries: List[str], max_results: int) -> List[Dict[str, Any]]:
        """Busca nos motores secundários"""
        
        secondary_results = []
        
        for query in queries[8:12]:  # Queries 8-12 nos motores secundários
            try:
                results = secondary_search_engines.search_all_secondary_engines(query, max_results // len(queries))
                secondary_results.extend(results)
                time.sleep(2)  # Rate limiting maior
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca secundária para '{query}': {e}")
                continue
        
        return secondary_results
    
    def _search_specialized_sources(self, queries: List[str], max_results: int) -> List[Dict[str, Any]]:
        """Busca em fontes especializadas"""
        
        specialized_results = []
        
        for query in queries[:5]:  # Primeiras 5 queries em fontes especializadas
            try:
                results = secondary_search_engines.search_specialized_databases(query, {}, max_results // len(queries))
                specialized_results.extend(results)
                time.sleep(1.5)
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca especializada para '{query}': {e}")
                continue
        
        return specialized_results
    
    def _search_academic_sources(self, queries: List[str], max_results: int) -> List[Dict[str, Any]]:
        """Busca em fontes acadêmicas"""
        
        academic_results = []
        
        for query in queries[:3]:  # Primeiras 3 queries em fontes acadêmicas
            try:
                results = secondary_search_engines.search_academic_sources(query, max_results // len(queries))
                academic_results.extend(results)
                time.sleep(2)
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca acadêmica para '{query}': {e}")
                continue
        
        return academic_results
    
    def _search_news_sources(self, queries: List[str], max_results: int) -> List[Dict[str, Any]]:
        """Busca em fontes de notícias"""
        
        news_results = []
        
        for query in queries[:5]:  # Primeiras 5 queries em notícias
            try:
                results = secondary_search_engines.search_news_sources(query, max_results // len(queries))
                news_results.extend(results)
                time.sleep(1)
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca de notícias para '{query}': {e}")
                continue
        
        return news_results
    
    def _filter_and_deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filtra e remove duplicatas"""
        
        # Aplica filtros de URL
        filtered_results = url_filter_manager.filtrar_lista_urls(results)
        
        # Remove duplicatas por URL
        seen_urls = set()
        unique_results = []
        
        for result in filtered_results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        # Ordena por prioridade (se disponível)
        unique_results.sort(key=lambda x: x.get('filtro', {}).get('prioridade', 1), reverse=True)
        
        return unique_results
    
    def _execute_parallel_extraction(self, search_results: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Executa extração de conteúdo em paralelo"""
        
        self.stats['total_extractions'] += len(search_results)
        
        extracted_content = []
        
        # Limita número de extrações para performance
        results_to_extract = search_results[:30]  # Top 30 resultados
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_result = {
                executor.submit(self._extract_single_url, result, context): result 
                for result in results_to_extract
            }
            
            for future in as_completed(future_to_result):
                result = future_to_result[future]
                try:
                    extraction_result = future.result()
                    extracted_content.append(extraction_result)
                    
                    if extraction_result['success']:
                        self.stats['successful_extractions'] += 1
                        
                except Exception as e:
                    logger.error(f"❌ Erro na extração paralela de {result.get('url', 'URL desconhecida')}: {e}")
                    extracted_content.append({
                        'success': False,
                        'error': str(e),
                        'url': result.get('url', ''),
                        'title': result.get('title', '')
                    })
        
        return extracted_content
    
    def _extract_single_url(self, search_result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai conteúdo de uma única URL usando múltiplas estratégias"""
        
        url = search_result.get('url', '')
        
        if not url:
            return {
                'success': False,
                'error': 'URL vazia',
                'url': url,
                'title': search_result.get('title', '')
            }
        
        # Tenta cada estratégia de extração
        for strategy_name, strategy_func in self.extraction_strategies:
            try:
                logger.debug(f"🔍 Tentando {strategy_name} para {url}")
                
                if strategy_name == 'multi_layer':
                    result = strategy_func(url, context)
                else:
                    result = strategy_func(url)
                
                if result['success'] and result.get('content'):
                    # Adiciona metadados do resultado de busca
                    result.update({
                        'search_title': search_result.get('title', ''),
                        'search_snippet': search_result.get('snippet', ''),
                        'search_source': search_result.get('source', ''),
                        'extraction_strategy': strategy_name
                    })
                    
                    logger.debug(f"✅ {strategy_name} bem-sucedida para {url}")
                    return result
                else:
                    logger.debug(f"⚠️ {strategy_name} falhou para {url}: {result.get('error', 'Sem conteúdo')}")
                    continue
                    
            except Exception as e:
                logger.warning(f"⚠️ Erro em {strategy_name} para {url}: {e}")
                continue
        
        # Todas as estratégias falharam
        return {
            'success': False,
            'error': 'Todas as estratégias de extração falharam',
            'url': url,
            'title': search_result.get('title', ''),
            'strategies_attempted': len(self.extraction_strategies)
        }
    
    def _extract_with_robust_static(self, url: str) -> Dict[str, Any]:
        """Extração estática robusta como fallback"""
        
        try:
            from services.robust_content_extractor import robust_content_extractor
            
            content = robust_content_extractor.extract_content(url)
            
            if content:
                return {
                    'success': True,
                    'content': content,
                    'method': 'robust_static_fallback',
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
    
    def _emergency_extraction(self, url: str) -> Dict[str, Any]:
        """Extração de emergência como último recurso"""
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Tentativa de emergência com configurações mínimas
            response = requests.get(
                url, 
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; ARQV30Bot/2.0)'},
                verify=False
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extrai qualquer texto disponível
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                
                # Filtra linhas com pelo menos 20 caracteres
                lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 20]
                
                if lines:
                    content = '\n'.join(lines[:50])  # Primeiras 50 linhas
                    
                    if len(content) > 100:
                        return {
                            'success': True,
                            'content': content,
                            'method': 'emergency_extraction',
                            'url': url,
                            'warning': 'Extração de emergência - qualidade limitada'
                        }
            
            return {
                'success': False,
                'error': 'Extração de emergência falhou',
                'content': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro na extração de emergência: {str(e)}',
                'content': None
            }
    
    def _validate_search_quality(self, extracted_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valida qualidade da busca completa"""
        
        successful_extractions = [c for c in extracted_content if c['success']]
        
        # Calcula métricas
        total_content_length = sum(len(c.get('content', '')) for c in successful_extractions)
        unique_domains = len(set(self._extract_domain(c.get('url', '')) for c in successful_extractions))
        
        # Calcula qualidade média
        quality_scores = []
        for content in successful_extractions:
            if content.get('quality_validation', {}).get('score'):
                quality_scores.append(content['quality_validation']['score'])
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Verifica se atende requisitos
        meets_requirements = (
            len(successful_extractions) >= self.quality_requirements['min_sources'] and
            total_content_length >= self.quality_requirements['min_total_content'] and
            avg_quality >= self.quality_requirements['min_avg_quality'] and
            unique_domains >= self.quality_requirements['min_unique_domains']
        )
        
        # Identifica problemas
        issues = []
        if len(successful_extractions) < self.quality_requirements['min_sources']:
            issues.append(f"Poucas fontes: {len(successful_extractions)} < {self.quality_requirements['min_sources']}")
        
        if total_content_length < self.quality_requirements['min_total_content']:
            issues.append(f"Pouco conteúdo: {total_content_length} < {self.quality_requirements['min_total_content']}")
        
        if avg_quality < self.quality_requirements['min_avg_quality']:
            issues.append(f"Qualidade baixa: {avg_quality:.1f} < {self.quality_requirements['min_avg_quality']}")
        
        if unique_domains < self.quality_requirements['min_unique_domains']:
            issues.append(f"Poucos domínios: {unique_domains} < {self.quality_requirements['min_unique_domains']}")
        
        return {
            'meets_requirements': meets_requirements,
            'successful_extractions': len(successful_extractions),
            'total_content_length': total_content_length,
            'unique_domains': unique_domains,
            'avg_quality_score': avg_quality,
            'issues': issues,
            'quality_distribution': self._analyze_quality_distribution(successful_extractions)
        }
    
    def _extract_domain(self, url: str) -> str:
        """Extrai domínio de uma URL"""
        
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.lower().replace('www.', '')
        except:
            return 'unknown'
    
    def _calculate_avg_quality(self, extracted_content: List[Dict[str, Any]]) -> float:
        """Calcula qualidade média"""
        
        quality_scores = []
        
        for content in extracted_content:
            if content['success'] and content.get('quality_validation', {}).get('score'):
                quality_scores.append(content['quality_validation']['score'])
        
        return sum(quality_scores) / len(quality_scores) if quality_scores else 0
    
    def _analyze_quality_distribution(self, successful_extractions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analisa distribuição de qualidade"""
        
        distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for content in successful_extractions:
            quality_score = content.get('quality_validation', {}).get('score', 0)
            
            if quality_score >= 80:
                distribution['high'] += 1
            elif quality_score >= 60:
                distribution['medium'] += 1
            else:
                distribution['low'] += 1
        
        return distribution
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas abrangentes"""
        
        total_searches = self.stats['total_searches']
        search_success_rate = (self.stats['successful_searches'] / total_searches * 100) if total_searches > 0 else 0
        
        total_extractions = self.stats['total_extractions']
        extraction_success_rate = (self.stats['successful_extractions'] / total_extractions * 100) if total_extractions > 0 else 0
        
        return {
            **self.stats,
            'search_success_rate': search_success_rate,
            'extraction_success_rate': extraction_success_rate,
            'primary_engine_status': production_search_manager.get_provider_status(),
            'secondary_engine_status': secondary_search_engines.get_engine_status(),
            'url_filter_stats': url_filter_manager.get_stats()
        }
    
    def reset_all_stats(self):
        """Reset todas as estatísticas"""
        
        self.stats = {
            'total_searches': 0,
            'successful_searches': 0,
            'total_extractions': 0,
            'successful_extractions': 0,
            'layer_performance': {},
            'quality_metrics': {}
        }
        
        # Reset componentes
        production_search_manager.reset_provider_errors()
        secondary_search_engines.reset_engine_errors()
        url_filter_manager.reset_stats()
        
        logger.info("🔄 Todas as estatísticas do sistema de busca resetadas")

# Instância global
ultra_robust_search_manager = UltraRobustSearchManager()