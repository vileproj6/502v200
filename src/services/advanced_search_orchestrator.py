#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Advanced Search Orchestrator
Orquestrador de busca avançado com múltiplas fontes e validação rigorosa
"""

import time
import logging
import asyncio
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.production_search_manager import production_search_manager
from services.secondary_search_engines import secondary_search_engines
from services.robust_content_extractor import robust_content_extractor
from services.content_quality_validator import content_quality_validator
from services.url_filter_manager import url_filter_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class AdvancedSearchOrchestrator:
    """Orquestrador de busca avançado com múltiplas camadas"""
    
    def __init__(self):
        """Inicializa orquestrador avançado"""
        self.search_layers = [
            ('primary_engines', self._search_primary_engines),
            ('secondary_engines', self._search_secondary_engines),
            ('specialized_sources', self._search_specialized_sources),
            ('academic_sources', self._search_academic_sources),
            ('news_sources', self._search_news_sources),
            ('industry_reports', self._search_industry_reports)
        ]
        
        self.quality_thresholds = {
            'min_content_length': 800,
            'min_quality_score': 65.0,
            'min_word_count': 150,
            'max_navigation_ratio': 0.25
        }
        
        self.extraction_strategies = [
            ('robust_static', robust_content_extractor.extract_content),
            ('quality_validated', self._extract_with_validation),
            ('multi_attempt', self._extract_with_multiple_attempts)
        ]
        
        logger.info("Advanced Search Orchestrator inicializado")
    
    def execute_comprehensive_search(
        self, 
        query: str, 
        context: Dict[str, Any],
        max_results_per_layer: int = 15,
        require_high_quality: bool = True
    ) -> Dict[str, Any]:
        """Executa busca abrangente em múltiplas camadas"""
        
        logger.info(f"🚀 Iniciando busca abrangente para: {query}")
        
        # Gera queries expandidas
        expanded_queries = self._generate_intelligent_queries(query, context)
        
        # Salva queries
        salvar_etapa("queries_expandidas", {
            "original_query": query,
            "expanded_queries": expanded_queries,
            "context": context
        }, categoria="pesquisa_web")
        
        # Executa busca em todas as camadas
        all_search_results = []
        layer_performance = {}
        
        for layer_name, layer_func in self.search_layers:
            try:
                logger.info(f"🔍 Executando camada: {layer_name}")
                
                layer_start = time.time()
                layer_results = layer_func(expanded_queries, max_results_per_layer, context)
                layer_time = time.time() - layer_start
                
                if layer_results:
                    all_search_results.extend(layer_results)
                    layer_performance[layer_name] = {
                        'results_count': len(layer_results),
                        'execution_time': layer_time,
                        'success': True
                    }
                    logger.info(f"✅ {layer_name}: {len(layer_results)} resultados em {layer_time:.2f}s")
                else:
                    layer_performance[layer_name] = {
                        'results_count': 0,
                        'execution_time': layer_time,
                        'success': False
                    }
                    logger.warning(f"⚠️ {layer_name}: 0 resultados")
                
            except Exception as e:
                logger.error(f"❌ Erro na camada {layer_name}: {e}")
                layer_performance[layer_name] = {
                    'results_count': 0,
                    'execution_time': 0,
                    'success': False,
                    'error': str(e)
                }
                salvar_erro(f"busca_{layer_name}", e, contexto={"query": query})
        
        # Filtra e remove duplicatas
        filtered_results = self._filter_and_deduplicate_results(all_search_results)
        
        # Executa extração de conteúdo em paralelo
        extracted_content = self._execute_parallel_extraction(filtered_results, context)
        
        # Valida qualidade final
        quality_validation = self._validate_search_quality(extracted_content)
        
        # Compila resultado final
        final_result = {
            'original_query': query,
            'expanded_queries': expanded_queries,
            'layer_performance': layer_performance,
            'search_results_summary': self._create_results_summary(filtered_results),
            'content_analysis': self._analyze_extracted_content(extracted_content),
            'quality_validation': quality_validation,
            'statistics': {
                'total_search_results': len(all_search_results),
                'filtered_results': len(filtered_results),
                'successful_extractions': len([c for c in extracted_content if c.get('success')]),
                'unique_domains': len(set(self._extract_domain(r['url']) for r in filtered_results)),
                'avg_quality_score': self._calculate_avg_quality(extracted_content),
                'total_content_length': sum(len(c.get('content', '')) for c in extracted_content if c.get('success'))
            },
            'meets_quality_requirements': quality_validation.get('meets_requirements', False)
        }
        
        # Salva resultado final
        salvar_etapa("busca_abrangente_final", final_result, categoria="pesquisa_web")
        
        return final_result
    
    def _generate_intelligent_queries(self, base_query: str, context: Dict[str, Any]) -> List[str]:
        """Gera queries inteligentes expandidas"""
        
        segmento = context.get('segmento', '')
        produto = context.get('produto', '')
        publico = context.get('publico', '')
        
        queries = [base_query]
        
        # Queries baseadas no contexto
        if segmento:
            queries.extend([
                f"mercado {segmento} Brasil 2024 dados estatísticas IBGE",
                f"análise competitiva {segmento} principais empresas líderes",
                f"tendências {segmento} inovação tecnologia disrupção",
                f"investimentos {segmento} venture capital funding rodadas",
                f"regulamentação {segmento} mudanças legais compliance",
                f"cases sucesso {segmento} empresas brasileiras unicórnios",
                f"desafios {segmento} problemas soluções oportunidades",
                f"futuro {segmento} predições especialistas consultoria"
            ])
        
        if produto:
            queries.extend([
                f"demanda {produto} Brasil consumo mercado potencial",
                f"preço {produto} ticket médio benchmarks concorrência",
                f"inovação {produto} tecnologia features diferenciação",
                f"distribuição {produto} canais vendas marketplace"
            ])
        
        if publico:
            queries.extend([
                f"comportamento {publico} Brasil pesquisa consumo hábitos",
                f"perfil demográfico {publico} dados IBGE renda educação",
                f"jornada compra {publico} processo decisão fatores"
            ])
        
        # Queries de inteligência de mercado
        queries.extend([
            f"relatórios setoriais {segmento} McKinsey BCG Deloitte PwC",
            f"pesquisas mercado {segmento} institutos dados primários",
            f"startups {segmento} ecossistema inovação Brasil",
            f"fusões aquisições {segmento} M&A consolidação mercado",
            f"IPO {segmento} bolsa valores B3 mercado capitais"
        ])
        
        # Remove duplicatas e queries muito similares
        unique_queries = []
        for query in queries:
            if (query not in unique_queries and 
                len(query.split()) >= 4 and
                not any(self._queries_too_similar(query, existing) for existing in unique_queries)):
                unique_queries.append(query)
        
        return unique_queries[:15]  # Top 15 queries
    
    def _search_primary_engines(self, queries: List[str], max_results: int, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca nos motores primários"""
        
        primary_results = []
        
        for query in queries[:8]:  # Primeiras 8 queries
            try:
                results = production_search_manager.search_with_fallback(query, max_results // len(queries))
                
                # Adiciona contexto da query
                for result in results:
                    result['search_query'] = query
                    result['search_layer'] = 'primary'
                
                primary_results.extend(results)
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca primária para '{query}': {e}")
                continue
        
        return primary_results
    
    def _search_secondary_engines(self, queries: List[str], max_results: int, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca nos motores secundários"""
        
        secondary_results = []
        
        for query in queries[8:12]:  # Queries 8-12
            try:
                results = secondary_search_engines.search_all_secondary_engines(query, max_results // len(queries))
                
                for result in results:
                    result['search_query'] = query
                    result['search_layer'] = 'secondary'
                
                secondary_results.extend(results)
                time.sleep(2)  # Rate limiting maior
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca secundária para '{query}': {e}")
                continue
        
        return secondary_results
    
    def _search_specialized_sources(self, queries: List[str], max_results: int, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca em fontes especializadas"""
        
        specialized_results = []
        
        for query in queries[:5]:
            try:
                results = secondary_search_engines.search_specialized_databases(query, context, max_results // len(queries))
                
                for result in results:
                    result['search_query'] = query
                    result['search_layer'] = 'specialized'
                
                specialized_results.extend(results)
                time.sleep(1.5)
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca especializada para '{query}': {e}")
                continue
        
        return specialized_results
    
    def _search_academic_sources(self, queries: List[str], max_results: int, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca em fontes acadêmicas"""
        
        academic_results = []
        
        for query in queries[:3]:
            try:
                results = secondary_search_engines.search_academic_sources(query, max_results // len(queries))
                
                for result in results:
                    result['search_query'] = query
                    result['search_layer'] = 'academic'
                
                academic_results.extend(results)
                time.sleep(2)
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca acadêmica para '{query}': {e}")
                continue
        
        return academic_results
    
    def _search_news_sources(self, queries: List[str], max_results: int, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca em fontes de notícias"""
        
        news_results = []
        
        for query in queries[:5]:
            try:
                results = secondary_search_engines.search_news_sources(query, max_results // len(queries))
                
                for result in results:
                    result['search_query'] = query
                    result['search_layer'] = 'news'
                
                news_results.extend(results)
                time.sleep(1)
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca de notícias para '{query}': {e}")
                continue
        
        return news_results
    
    def _search_industry_reports(self, queries: List[str], max_results: int, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca em relatórios da indústria"""
        
        industry_results = []
        segmento = context.get('segmento', '').lower()
        
        # URLs específicas por segmento
        industry_sources = {
            'tecnologia': [
                'https://www.mckinsey.com/industries/technology-media-and-telecommunications',
                'https://www.bcg.com/industries/technology-media-telecommunications',
                'https://www2.deloitte.com/global/en/industries/technology.html'
            ],
            'saúde': [
                'https://www.mckinsey.com/industries/healthcare-systems-and-services',
                'https://www.bcg.com/industries/health-care',
                'https://www2.deloitte.com/global/en/industries/life-sciences-health-care.html'
            ],
            'financeiro': [
                'https://www.mckinsey.com/industries/financial-services',
                'https://www.bcg.com/industries/financial-institutions',
                'https://www2.deloitte.com/global/en/industries/financial-services.html'
            ]
        }
        
        # Seleciona fontes baseadas no segmento
        sources = []
        for key, urls in industry_sources.items():
            if key in segmento:
                sources.extend(urls)
                break
        
        if not sources:
            sources = industry_sources['tecnologia']  # Default
        
        # Busca em relatórios da indústria
        for source_url in sources[:3]:
            try:
                # Simula busca em relatórios (implementação específica seria necessária)
                industry_results.append({
                    'title': f'Relatório da indústria - {segmento}',
                    'url': source_url,
                    'snippet': f'Análise especializada do mercado de {segmento}',
                    'source': 'industry_report',
                    'search_layer': 'industry'
                })
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na busca de relatórios: {e}")
                continue
        
        return industry_results
    
    def _filter_and_deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filtra e remove duplicatas com validação aprimorada"""
        
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
        
        # Ordena por prioridade e qualidade
        unique_results.sort(key=lambda x: (
            x.get('filtro', {}).get('prioridade', 0),
            1 if x.get('search_layer') == 'primary' else 0.8,
            len(x.get('snippet', ''))
        ), reverse=True)
        
        logger.info(f"🔍 Filtros aplicados: {len(unique_results)}/{len(results)} URLs aprovadas")
        
        return unique_results
    
    def _execute_parallel_extraction(self, search_results: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Executa extração paralela com múltiplas estratégias"""
        
        extracted_content = []
        
        # Limita para performance mas garante qualidade
        results_to_extract = search_results[:25]  # Top 25 resultados
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_result = {
                executor.submit(self._extract_single_url_advanced, result, context): result 
                for result in results_to_extract
            }
            
            for future in as_completed(future_to_result):
                result = future_to_result[future]
                try:
                    extraction_result = future.result()
                    extracted_content.append(extraction_result)
                    
                    if extraction_result.get('success'):
                        logger.debug(f"✅ Extraído: {result.get('url', '')}")
                    
                except Exception as e:
                    logger.warning(f"❌ Erro na extração de {result.get('url', '')}: {e}")
                    extracted_content.append({
                        'success': False,
                        'error': str(e),
                        'url': result.get('url', ''),
                        'title': result.get('title', '')
                    })
        
        return extracted_content
    
    def _extract_single_url_advanced(self, search_result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai conteúdo de URL única com estratégias avançadas"""
        
        url = search_result.get('url', '')
        
        if not url:
            return {
                'success': False,
                'error': 'URL vazia',
                'url': url
            }
        
        # Tenta múltiplas estratégias
        for strategy_name, strategy_func in self.extraction_strategies:
            try:
                if strategy_name == 'robust_static':
                    content = strategy_func(url)
                elif strategy_name == 'quality_validated':
                    content = strategy_func(url, context)
                elif strategy_name == 'multi_attempt':
                    content = strategy_func(url, context)
                else:
                    continue
                
                if content:
                    # Valida qualidade
                    validation = content_quality_validator.validate_content(content, url, context)
                    
                    if (validation['valid'] and 
                        validation['score'] >= self.quality_thresholds['min_quality_score'] and
                        len(content) >= self.quality_thresholds['min_content_length']):
                        
                        return {
                            'success': True,
                            'content': content,
                            'url': url,
                            'title': search_result.get('title', ''),
                            'source': search_result.get('source', ''),
                            'search_layer': search_result.get('search_layer', ''),
                            'extraction_strategy': strategy_name,
                            'quality_validation': validation,
                            'content_stats': {
                                'length': len(content),
                                'word_count': len(content.split()),
                                'quality_score': validation['score']
                            }
                        }
                
            except Exception as e:
                logger.debug(f"⚠️ Estratégia {strategy_name} falhou para {url}: {e}")
                continue
        
        # Todas as estratégias falharam
        return {
            'success': False,
            'error': 'Todas as estratégias de extração falharam',
            'url': url,
            'title': search_result.get('title', ''),
            'strategies_attempted': len(self.extraction_strategies)
        }
    
    def _extract_with_validation(self, url: str, context: Dict[str, Any]) -> Optional[str]:
        """Extração com validação rigorosa"""
        
        try:
            content = robust_content_extractor.extract_content(url)
            
            if content:
                validation = content_quality_validator.validate_content(content, url, context)
                
                if validation['valid'] and validation['score'] >= 70:
                    return content
            
            return None
            
        except Exception as e:
            logger.debug(f"Extração com validação falhou para {url}: {e}")
            return None
    
    def _extract_with_multiple_attempts(self, url: str, context: Dict[str, Any]) -> Optional[str]:
        """Extração com múltiplas tentativas"""
        
        import requests
        from bs4 import BeautifulSoup
        
        # Múltiplas configurações de tentativa
        attempt_configs = [
            {'timeout': 20, 'verify': False, 'allow_redirects': True},
            {'timeout': 15, 'verify': True, 'allow_redirects': True},
            {'timeout': 10, 'verify': False, 'allow_redirects': False}
        ]
        
        for i, config in enumerate(attempt_configs):
            try:
                response = requests.get(url, **config)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove elementos desnecessários
                    for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                        element.decompose()
                    
                    text = soup.get_text()
                    
                    # Limpa texto
                    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 20]
                    content = '\n'.join(lines)
                    
                    if len(content) > 500:
                        return content
                
                time.sleep(1)  # Delay entre tentativas
                
            except Exception as e:
                logger.debug(f"Tentativa {i+1} falhou para {url}: {e}")
                continue
        
        return None
    
    def _validate_search_quality(self, extracted_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valida qualidade da busca completa"""
        
        successful_extractions = [c for c in extracted_content if c.get('success')]
        
        # Calcula métricas
        total_content_length = sum(c.get('content_stats', {}).get('length', 0) for c in successful_extractions)
        unique_domains = len(set(self._extract_domain(c.get('url', '')) for c in successful_extractions))
        
        quality_scores = [c.get('quality_validation', {}).get('score', 0) for c in successful_extractions]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Verifica requisitos
        meets_requirements = (
            len(successful_extractions) >= 5 and
            total_content_length >= 15000 and
            avg_quality >= 65.0 and
            unique_domains >= 3
        )
        
        # Identifica problemas
        issues = []
        if len(successful_extractions) < 5:
            issues.append(f"Poucas extrações: {len(successful_extractions)} < 5")
        if total_content_length < 15000:
            issues.append(f"Pouco conteúdo: {total_content_length} < 15000")
        if avg_quality < 65.0:
            issues.append(f"Qualidade baixa: {avg_quality:.1f} < 65.0")
        if unique_domains < 3:
            issues.append(f"Poucos domínios: {unique_domains} < 3")
        
        return {
            'meets_requirements': meets_requirements,
            'successful_extractions': len(successful_extractions),
            'total_content_length': total_content_length,
            'unique_domains': unique_domains,
            'avg_quality_score': avg_quality,
            'issues': issues,
            'quality_distribution': self._analyze_quality_distribution(successful_extractions)
        }
    
    def _create_results_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cria resumo dos resultados (sem dados brutos)"""
        
        summary = {
            'total_results': len(results),
            'sources_by_layer': {},
            'sources_by_engine': {},
            'top_domains': {},
            'quality_distribution': {}
        }
        
        # Agrupa por camada
        for result in results:
            layer = result.get('search_layer', 'unknown')
            summary['sources_by_layer'][layer] = summary['sources_by_layer'].get(layer, 0) + 1
            
            source = result.get('source', 'unknown')
            summary['sources_by_engine'][source] = summary['sources_by_engine'].get(source, 0) + 1
            
            domain = self._extract_domain(result.get('url', ''))
            summary['top_domains'][domain] = summary['top_domains'].get(domain, 0) + 1
        
        # Top 10 domínios
        summary['top_domains'] = dict(sorted(summary['top_domains'].items(), key=lambda x: x[1], reverse=True)[:10])
        
        return summary
    
    def _analyze_extracted_content(self, extracted_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisa conteúdo extraído (sem incluir conteúdo bruto)"""
        
        successful = [c for c in extracted_content if c.get('success')]
        
        analysis = {
            'total_attempts': len(extracted_content),
            'successful_extractions': len(successful),
            'success_rate': len(successful) / len(extracted_content) * 100 if extracted_content else 0,
            'content_statistics': {},
            'quality_analysis': {},
            'extraction_methods': {}
        }
        
        if successful:
            # Estatísticas de conteúdo
            content_lengths = [c.get('content_stats', {}).get('length', 0) for c in successful]
            word_counts = [c.get('content_stats', {}).get('word_count', 0) for c in successful]
            quality_scores = [c.get('content_stats', {}).get('quality_score', 0) for c in successful]
            
            analysis['content_statistics'] = {
                'avg_content_length': sum(content_lengths) / len(content_lengths),
                'total_content_length': sum(content_lengths),
                'avg_word_count': sum(word_counts) / len(word_counts),
                'avg_quality_score': sum(quality_scores) / len(quality_scores)
            }
            
            # Análise de qualidade
            high_quality = [c for c in successful if c.get('content_stats', {}).get('quality_score', 0) >= 80]
            medium_quality = [c for c in successful if 60 <= c.get('content_stats', {}).get('quality_score', 0) < 80]
            low_quality = [c for c in successful if c.get('content_stats', {}).get('quality_score', 0) < 60]
            
            analysis['quality_analysis'] = {
                'high_quality_count': len(high_quality),
                'medium_quality_count': len(medium_quality),
                'low_quality_count': len(low_quality),
                'quality_distribution': {
                    'high': len(high_quality) / len(successful) * 100,
                    'medium': len(medium_quality) / len(successful) * 100,
                    'low': len(low_quality) / len(successful) * 100
                }
            }
            
            # Métodos de extração
            methods = {}
            for c in successful:
                method = c.get('extraction_strategy', 'unknown')
                methods[method] = methods.get(method, 0) + 1
            
            analysis['extraction_methods'] = methods
        
        return analysis
    
    def _extract_domain(self, url: str) -> str:
        """Extrai domínio de URL"""
        
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.lower().replace('www.', '')
        except:
            return 'unknown'
    
    def _calculate_avg_quality(self, extracted_content: List[Dict[str, Any]]) -> float:
        """Calcula qualidade média"""
        
        quality_scores = []
        
        for content in extracted_content:
            if content.get('success'):
                score = content.get('content_stats', {}).get('quality_score', 0)
                if score > 0:
                    quality_scores.append(score)
        
        return sum(quality_scores) / len(quality_scores) if quality_scores else 0
    
    def _analyze_quality_distribution(self, successful_extractions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analisa distribuição de qualidade"""
        
        distribution = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        
        for content in successful_extractions:
            quality_score = content.get('content_stats', {}).get('quality_score', 0)
            
            if quality_score >= 90:
                distribution['excellent'] += 1
            elif quality_score >= 75:
                distribution['good'] += 1
            elif quality_score >= 60:
                distribution['fair'] += 1
            else:
                distribution['poor'] += 1
        
        return distribution
    
    def _queries_too_similar(self, query1: str, query2: str) -> bool:
        """Verifica se duas queries são muito similares"""
        
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        
        # Se mais de 70% das palavras são iguais, considera similar
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union) if union else 0
        return similarity > 0.7

# Instância global
advanced_search_orchestrator = AdvancedSearchOrchestrator()