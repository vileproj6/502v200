#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Content Synthesis Engine
Motor de síntese de conteúdo que processa dados brutos em insights estruturados
"""

import logging
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import Counter

logger = logging.getLogger(__name__)

class ContentSynthesisEngine:
    """Motor de síntese que transforma dados brutos em insights estruturados"""
    
    def __init__(self):
        """Inicializa motor de síntese"""
        self.synthesis_patterns = self._load_synthesis_patterns()
        self.insight_categories = self._load_insight_categories()
        self.data_extractors = self._load_data_extractors()
        
        logger.info("Content Synthesis Engine inicializado")
    
    def _load_synthesis_patterns(self) -> Dict[str, List[str]]:
        """Carrega padrões para síntese de conteúdo"""
        return {
            'market_size': [
                r'mercado de R\$ ([\d,\.]+)',
                r'faturamento de R\$ ([\d,\.]+)',
                r'receita de R\$ ([\d,\.]+)',
                r'movimenta R\$ ([\d,\.]+)',
                r'valor de R\$ ([\d,\.]+)'
            ],
            'growth_rates': [
                r'crescimento de (\d+(?:\.\d+)?%)',
                r'cresceu (\d+(?:\.\d+)?%)',
                r'aumento de (\d+(?:\.\d+)?%)',
                r'expansão de (\d+(?:\.\d+)?%)',
                r'alta de (\d+(?:\.\d+)?%)'
            ],
            'market_share': [
                r'(\d+(?:\.\d+)?%) do mercado',
                r'participação de (\d+(?:\.\d+)?%)',
                r'fatia de (\d+(?:\.\d+)?%)',
                r'representa (\d+(?:\.\d+)?%)',
                r'corresponde a (\d+(?:\.\d+)?%)'
            ],
            'consumer_behavior': [
                r'(\d+(?:\.\d+)?%) dos consumidores',
                r'(\d+(?:\.\d+)?%) dos brasileiros',
                r'(\d+(?:\.\d+)?%) da população',
                r'(\d+(?:\.\d+)?%) dos usuários',
                r'(\d+(?:\.\d+)?%) dos clientes'
            ],
            'trends': [
                r'tendência de (\w+)',
                r'crescimento em (\w+)',
                r'aumento na (\w+)',
                r'expansão do (\w+)',
                r'evolução da (\w+)'
            ]
        }
    
    def _load_insight_categories(self) -> Dict[str, Dict[str, Any]]:
        """Carrega categorias de insights"""
        return {
            'market_opportunity': {
                'keywords': ['oportunidade', 'potencial', 'crescimento', 'expansão', 'demanda'],
                'priority': 10,
                'template': 'Oportunidade identificada: {content}'
            },
            'competitive_advantage': {
                'keywords': ['vantagem', 'diferencial', 'único', 'exclusivo', 'inovador'],
                'priority': 9,
                'template': 'Vantagem competitiva: {content}'
            },
            'market_threat': {
                'keywords': ['ameaça', 'risco', 'desafio', 'problema', 'barreira'],
                'priority': 8,
                'template': 'Ameaça ao mercado: {content}'
            },
            'consumer_insight': {
                'keywords': ['consumidor', 'cliente', 'usuário', 'comportamento', 'preferência'],
                'priority': 7,
                'template': 'Insight do consumidor: {content}'
            },
            'technology_trend': {
                'keywords': ['tecnologia', 'inovação', 'digital', 'automação', 'IA'],
                'priority': 6,
                'template': 'Tendência tecnológica: {content}'
            },
            'regulatory_change': {
                'keywords': ['regulamentação', 'lei', 'norma', 'compliance', 'legal'],
                'priority': 5,
                'template': 'Mudança regulatória: {content}'
            }
        }
    
    def _load_data_extractors(self) -> Dict[str, callable]:
        """Carrega extratores de dados específicos"""
        return {
            'financial_data': self._extract_financial_data,
            'percentage_data': self._extract_percentage_data,
            'company_names': self._extract_company_names,
            'market_trends': self._extract_market_trends,
            'geographic_data': self._extract_geographic_data,
            'temporal_data': self._extract_temporal_data
        }
    
    def synthesize_research_content(
        self, 
        raw_content_list: List[Dict[str, Any]], 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Sintetiza conteúdo bruto em insights estruturados"""
        
        logger.info(f"🔄 Sintetizando {len(raw_content_list)} fontes de conteúdo")
        
        # Combina todo o conteúdo
        combined_content = self._combine_content_sources(raw_content_list)
        
        # Extrai dados estruturados
        structured_data = self._extract_structured_data(combined_content, context)
        
        # Gera insights categorizados
        categorized_insights = self._generate_categorized_insights(combined_content, context)
        
        # Identifica padrões e tendências
        patterns = self._identify_content_patterns(combined_content, context)
        
        # Cria síntese final
        synthesis_result = {
            'content_sources_analyzed': len(raw_content_list),
            'total_content_length': len(combined_content),
            'structured_data': structured_data,
            'categorized_insights': categorized_insights,
            'identified_patterns': patterns,
            'synthesis_metadata': {
                'generated_at': datetime.now().isoformat(),
                'synthesis_engine': 'ARQV30_v2.0',
                'quality_score': self._calculate_synthesis_quality(structured_data, categorized_insights),
                'data_sources': len(raw_content_list),
                'unique_insights': len(categorized_insights.get('all_insights', []))
            }
        }
        
        logger.info(f"✅ Síntese concluída: {len(categorized_insights.get('all_insights', []))} insights gerados")
        
        return synthesis_result
    
    def _combine_content_sources(self, content_list: List[Dict[str, Any]]) -> str:
        """Combina múltiplas fontes de conteúdo"""
        
        combined = ""
        
        for i, content_item in enumerate(content_list, 1):
            if content_item.get('success') and content_item.get('content'):
                content = content_item['content']
                title = content_item.get('title', f'Fonte {i}')
                url = content_item.get('url', '')
                
                # Adiciona cabeçalho da fonte (sem URL completa)
                domain = self._extract_domain(url) if url else 'fonte_desconhecida'
                combined += f"\n=== FONTE {i}: {title} ({domain}) ===\n"
                combined += content[:2000]  # Limita tamanho por fonte
                combined += "\n\n"
        
        return combined
    
    def _extract_structured_data(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados estruturados do conteúdo"""
        
        structured_data = {}
        
        # Executa todos os extratores
        for extractor_name, extractor_func in self.data_extractors.items():
            try:
                extracted = extractor_func(content, context)
                if extracted:
                    structured_data[extractor_name] = extracted
            except Exception as e:
                logger.warning(f"⚠️ Extrator {extractor_name} falhou: {e}")
                continue
        
        return structured_data
    
    def _extract_financial_data(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados financeiros"""
        
        financial_data = {
            'market_values': [],
            'revenue_figures': [],
            'investment_amounts': [],
            'growth_rates': []
        }
        
        # Valores de mercado
        market_patterns = self.synthesis_patterns['market_size']
        for pattern in market_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                financial_data['market_values'].append(f"R$ {match}")
        
        # Taxas de crescimento
        growth_patterns = self.synthesis_patterns['growth_rates']
        for pattern in growth_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            financial_data['growth_rates'].extend(matches)
        
        # Remove duplicatas
        for key in financial_data:
            financial_data[key] = list(set(financial_data[key]))
        
        return financial_data
    
    def _extract_percentage_data(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados percentuais"""
        
        percentage_data = {
            'market_shares': [],
            'consumer_percentages': [],
            'adoption_rates': []
        }
        
        # Participação de mercado
        share_patterns = self.synthesis_patterns['market_share']
        for pattern in share_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            percentage_data['market_shares'].extend(matches)
        
        # Comportamento do consumidor
        consumer_patterns = self.synthesis_patterns['consumer_behavior']
        for pattern in consumer_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            percentage_data['consumer_percentages'].extend(matches)
        
        # Taxas de adoção
        adoption_patterns = [
            r'adoção de (\d+(?:\.\d+)?%)',
            r'penetração de (\d+(?:\.\d+)?%)',
            r'uso de (\d+(?:\.\d+)?%)'
        ]
        
        for pattern in adoption_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            percentage_data['adoption_rates'].extend(matches)
        
        return percentage_data
    
    def _extract_company_names(self, content: str, context: Dict[str, Any]) -> List[str]:
        """Extrai nomes de empresas"""
        
        # Padrões para identificar empresas
        company_patterns = [
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',  # Nome Sobrenome (empresas)
            r'\b([A-Z]{2,})\b',  # Siglas
            r'\b([A-Z][a-z]+(?:Tech|Lab|Corp|Inc|Ltd|SA|Ltda))\b'  # Sufixos empresariais
        ]
        
        companies = []
        
        for pattern in company_patterns:
            matches = re.findall(pattern, content)
            companies.extend(matches)
        
        # Filtra empresas conhecidas brasileiras
        known_companies = [
            'Magazine Luiza', 'Nubank', 'Stone', 'PagSeguro', 'Mercado Livre',
            'B2W', 'Via Varejo', 'Americanas', 'Submarino', 'Shopee',
            'iFood', 'Rappi', 'Uber', '99', 'Loggi', 'Petrobras', 'Vale'
        ]
        
        relevant_companies = []
        for company in companies:
            if (len(company) > 2 and 
                (company in known_companies or 
                 any(known in company for known in known_companies))):
                relevant_companies.append(company)
        
        return list(set(relevant_companies))[:10]  # Top 10 empresas únicas
    
    def _extract_market_trends(self, content: str, context: Dict[str, Any]) -> List[str]:
        """Extrai tendências de mercado"""
        
        trends = []
        
        # Padrões de tendências
        trend_patterns = self.synthesis_patterns['trends']
        for pattern in trend_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            trends.extend(matches)
        
        # Tendências específicas por contexto
        trend_keywords = [
            'inteligência artificial', 'automação', 'digitalização',
            'sustentabilidade', 'ESG', 'experiência cliente',
            'personalização', 'omnichannel', 'mobile first',
            'cloud computing', 'big data', 'analytics'
        ]
        
        for keyword in trend_keywords:
            if keyword.lower() in content.lower():
                # Busca contexto ao redor da palavra-chave
                pattern = rf'.{{0,100}}{re.escape(keyword)}.{{0,100}}'
                matches = re.findall(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    if len(match.strip()) > 50:
                        trends.append(f"Tendência: {match.strip()[:150]}...")
        
        return list(set(trends))[:8]  # Top 8 tendências únicas
    
    def _extract_geographic_data(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados geográficos"""
        
        geographic_data = {
            'regions': [],
            'cities': [],
            'states': []
        }
        
        # Regiões brasileiras
        regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
        for region in regions:
            if region.lower() in content.lower():
                geographic_data['regions'].append(region)
        
        # Estados principais
        states = [
            'São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Paraná', 'Bahia',
            'Rio Grande do Sul', 'Pernambuco', 'Ceará', 'Pará', 'Santa Catarina'
        ]
        
        for state in states:
            if state.lower() in content.lower():
                geographic_data['states'].append(state)
        
        # Cidades principais
        cities = [
            'São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza',
            'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre'
        ]
        
        for city in cities:
            if city.lower() in content.lower():
                geographic_data['cities'].append(city)
        
        return geographic_data
    
    def _extract_temporal_data(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados temporais"""
        
        temporal_data = {
            'years_mentioned': [],
            'periods': [],
            'forecasts': []
        }
        
        # Anos mencionados
        year_pattern = r'\b(20\d{2})\b'
        years = re.findall(year_pattern, content)
        temporal_data['years_mentioned'] = list(set(years))
        
        # Períodos
        period_patterns = [
            r'últimos (\d+) (?:anos|meses)',
            r'próximos (\d+) (?:anos|meses)',
            r'até (\d{4})',
            r'desde (\d{4})'
        ]
        
        for pattern in period_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            temporal_data['periods'].extend(matches)
        
        # Previsões
        forecast_patterns = [
            r'previsão (?:de|para) (\d{4})',
            r'projeção (?:de|para) (\d{4})',
            r'estimativa (?:de|para) (\d{4})'
        ]
        
        for pattern in forecast_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            temporal_data['forecasts'].extend(matches)
        
        return temporal_data
    
    def _generate_categorized_insights(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gera insights categorizados"""
        
        categorized = {
            'all_insights': [],
            'by_category': {},
            'priority_insights': []
        }
        
        # Divide conteúdo em sentenças
        sentences = self._extract_meaningful_sentences(content)
        
        # Categoriza cada sentença
        for sentence in sentences:
            category = self._categorize_sentence(sentence)
            
            if category:
                insight = self._format_insight(sentence, category)
                
                categorized['all_insights'].append(insight)
                
                if category not in categorized['by_category']:
                    categorized['by_category'][category] = []
                
                categorized['by_category'][category].append(insight)
        
        # Seleciona insights prioritários
        categorized['priority_insights'] = self._select_priority_insights(categorized['by_category'])
        
        return categorized
    
    def _extract_meaningful_sentences(self, content: str) -> List[str]:
        """Extrai sentenças significativas do conteúdo"""
        
        # Divide em sentenças
        sentences = re.split(r'[.!?]+', content)
        
        meaningful = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            # Filtra sentenças significativas
            if (len(sentence) > 50 and  # Tamanho mínimo
                len(sentence) < 300 and  # Tamanho máximo
                self._is_meaningful_sentence(sentence)):
                meaningful.append(sentence)
        
        return meaningful[:100]  # Top 100 sentenças
    
    def _is_meaningful_sentence(self, sentence: str) -> bool:
        """Verifica se sentença é significativa"""
        
        sentence_lower = sentence.lower()
        
        # Deve conter pelo menos um indicador de valor
        value_indicators = [
            r'\d+%', r'R\$', r'\d+(?:\.\d+)? (?:mil|milhão|bilhão)',
            r'crescimento', r'aumento', r'redução', r'queda',
            r'oportunidade', r'tendência', r'inovação', r'mercado'
        ]
        
        has_value = any(re.search(pattern, sentence_lower) for pattern in value_indicators)
        
        # Não deve ser navegação ou conteúdo irrelevante
        irrelevant_indicators = [
            'clique aqui', 'saiba mais', 'leia mais', 'veja também',
            'entre em contato', 'fale conosco', 'sobre nós',
            'termos de uso', 'política de privacidade'
        ]
        
        is_irrelevant = any(indicator in sentence_lower for indicator in irrelevant_indicators)
        
        return has_value and not is_irrelevant
    
    def _categorize_sentence(self, sentence: str) -> Optional[str]:
        """Categoriza sentença por tipo de insight"""
        
        sentence_lower = sentence.lower()
        
        # Encontra categoria com maior score
        best_category = None
        best_score = 0
        
        for category, config in self.insight_categories.items():
            score = 0
            
            # Conta palavras-chave da categoria
            for keyword in config['keywords']:
                if keyword in sentence_lower:
                    score += 1
            
            # Adiciona prioridade da categoria
            if score > 0:
                score += config['priority'] * 0.1
            
            if score > best_score:
                best_score = score
                best_category = category
        
        return best_category if best_score > 0 else None
    
    def _format_insight(self, sentence: str, category: str) -> str:
        """Formata insight baseado na categoria"""
        
        if category in self.insight_categories:
            template = self.insight_categories[category]['template']
            return template.format(content=sentence.strip())
        
        return sentence.strip()
    
    def _select_priority_insights(self, categorized_insights: Dict[str, List[str]]) -> List[str]:
        """Seleciona insights prioritários"""
        
        priority_insights = []
        
        # Ordena categorias por prioridade
        sorted_categories = sorted(
            categorized_insights.keys(),
            key=lambda cat: self.insight_categories.get(cat, {}).get('priority', 0),
            reverse=True
        )
        
        # Seleciona top insights de cada categoria
        for category in sorted_categories:
            insights = categorized_insights[category]
            
            # Ordena insights da categoria por qualidade
            quality_sorted = sorted(insights, key=len, reverse=True)
            
            # Adiciona top 3 da categoria
            priority_insights.extend(quality_sorted[:3])
        
        return priority_insights[:20]  # Top 20 insights prioritários
    
    def _identify_content_patterns(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Identifica padrões no conteúdo"""
        
        patterns = {
            'recurring_themes': [],
            'data_patterns': [],
            'trend_patterns': [],
            'competitive_patterns': []
        }
        
        # Temas recorrentes
        words = re.findall(r'\b[a-záêçõ]{4,}\b', content.lower())
        word_freq = Counter(words)
        
        # Filtra palavras relevantes
        relevant_words = [
            word for word, freq in word_freq.most_common(50)
            if freq >= 3 and word not in ['brasil', 'mercado', 'empresa', 'dados', 'anos']
        ]
        
        patterns['recurring_themes'] = relevant_words[:10]
        
        # Padrões de dados
        data_patterns_found = []
        
        # Busca padrões de crescimento
        growth_mentions = len(re.findall(r'crescimento|aumento|expansão', content, re.IGNORECASE))
        if growth_mentions > 5:
            data_patterns_found.append(f"Forte ênfase em crescimento ({growth_mentions} menções)")
        
        # Busca padrões de inovação
        innovation_mentions = len(re.findall(r'inovação|tecnologia|digital', content, re.IGNORECASE))
        if innovation_mentions > 5:
            data_patterns_found.append(f"Foco em inovação tecnológica ({innovation_mentions} menções)")
        
        patterns['data_patterns'] = data_patterns_found
        
        return patterns
    
    def _calculate_synthesis_quality(self, structured_data: Dict[str, Any], insights: Dict[str, Any]) -> float:
        """Calcula qualidade da síntese"""
        
        score = 0.0
        
        # Score por dados estruturados
        if structured_data:
            score += len(structured_data) * 10  # 10 pontos por tipo de dado
        
        # Score por insights categorizados
        all_insights = insights.get('all_insights', [])
        if all_insights:
            score += min(len(all_insights) * 2, 40)  # Máximo 40 pontos
        
        # Score por diversidade de categorias
        categories = len(insights.get('by_category', {}))
        score += categories * 5  # 5 pontos por categoria
        
        # Score por insights prioritários
        priority_insights = insights.get('priority_insights', [])
        score += len(priority_insights) * 1  # 1 ponto por insight prioritário
        
        return min(score, 100.0)
    
    def _extract_domain(self, url: str) -> str:
        """Extrai domínio de URL"""
        
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.replace('www.', '')
        except:
            return 'unknown'
    
    def create_synthesis_summary(self, synthesis_result: Dict[str, Any]) -> str:
        """Cria resumo da síntese"""
        
        summary = []
        summary.append("=== SÍNTESE DE CONTEÚDO ===\n")
        
        metadata = synthesis_result.get('synthesis_metadata', {})
        summary.append(f"Fontes analisadas: {metadata.get('data_sources', 0)}")
        summary.append(f"Insights únicos gerados: {metadata.get('unique_insights', 0)}")
        summary.append(f"Qualidade da síntese: {metadata.get('quality_score', 0):.1f}%\n")
        
        # Dados estruturados
        structured = synthesis_result.get('structured_data', {})
        if structured:
            summary.append("DADOS ESTRUTURADOS EXTRAÍDOS:")
            for data_type, data_content in structured.items():
                if isinstance(data_content, dict):
                    total_items = sum(len(v) if isinstance(v, list) else 1 for v in data_content.values())
                    summary.append(f"• {data_type}: {total_items} itens")
                elif isinstance(data_content, list):
                    summary.append(f"• {data_type}: {len(data_content)} itens")
            summary.append("")
        
        # Insights prioritários
        insights = synthesis_result.get('categorized_insights', {})
        priority_insights = insights.get('priority_insights', [])
        
        if priority_insights:
            summary.append("INSIGHTS PRIORITÁRIOS:")
            for i, insight in enumerate(priority_insights[:10], 1):
                summary.append(f"{i}. {insight}")
            summary.append("")
        
        # Padrões identificados
        patterns = synthesis_result.get('identified_patterns', {})
        if patterns:
            summary.append("PADRÕES IDENTIFICADOS:")
            
            themes = patterns.get('recurring_themes', [])
            if themes:
                summary.append(f"• Temas recorrentes: {', '.join(themes[:5])}")
            
            data_patterns = patterns.get('data_patterns', [])
            for pattern in data_patterns:
                summary.append(f"• {pattern}")
        
        return '\n'.join(summary)

# Instância global
content_synthesis_engine = ContentSynthesisEngine()