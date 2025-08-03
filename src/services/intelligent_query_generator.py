#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Intelligent Query Generator
Gerador inteligente de queries para pesquisa aprimorada
"""

import logging
import re
from typing import Dict, List, Any, Set
from datetime import datetime

logger = logging.getLogger(__name__)

class IntelligentQueryGenerator:
    """Gerador inteligente de queries para pesquisa abrangente"""
    
    def __init__(self):
        """Inicializa gerador de queries"""
        self.query_templates = self._load_query_templates()
        self.segment_keywords = self._load_segment_keywords()
        self.market_intelligence_terms = self._load_market_intelligence_terms()
        
        logger.info("Intelligent Query Generator inicializado")
    
    def _load_query_templates(self) -> Dict[str, List[str]]:
        """Carrega templates de queries por categoria"""
        return {
            'market_analysis': [
                "mercado {segmento} Brasil 2024 tamanho crescimento dados",
                "análise {segmento} estatísticas IBGE consumo demanda",
                "setor {segmento} brasileiro faturamento receita participação",
                "indústria {segmento} Brasil números dados oficiais",
                "economia {segmento} PIB contribuição impacto econômico"
            ],
            'competition': [
                "principais empresas {segmento} Brasil líderes mercado",
                "concorrência {segmento} market share participação",
                "ranking empresas {segmento} brasileiras maiores",
                "competição {segmento} análise competitiva SWOT",
                "players {segmento} Brasil unicórnios startups"
            ],
            'trends_innovation': [
                "tendências {segmento} 2024 2025 futuro inovação",
                "inovação {segmento} tecnologia disrupção mudanças",
                "futuro {segmento} predições especialistas consultoria",
                "transformação digital {segmento} automação IA",
                "evolução {segmento} próximos anos cenários"
            ],
            'investment_funding': [
                "investimentos {segmento} venture capital funding rodadas",
                "aportes {segmento} startups unicórnios valuations",
                "fusões aquisições {segmento} M&A consolidação",
                "IPO {segmento} bolsa valores B3 abertura capital",
                "private equity {segmento} investidores fundos"
            ],
            'regulation_compliance': [
                "regulamentação {segmento} leis normas compliance",
                "legislação {segmento} mudanças legais impacto",
                "normas {segmento} ANVISA ANATEL reguladores",
                "compliance {segmento} adequação legal requisitos",
                "marco legal {segmento} PL projetos lei"
            ],
            'consumer_behavior': [
                "comportamento consumidor {segmento} pesquisa hábitos",
                "perfil consumidor {segmento} demográfico psicográfico",
                "jornada compra {segmento} processo decisão fatores",
                "preferências consumidor {segmento} tendências consumo",
                "experiência cliente {segmento} satisfação NPS"
            ],
            'pricing_economics': [
                "preços {segmento} ticket médio benchmarks mercado",
                "precificação {segmento} estratégias modelos negócio",
                "elasticidade preço {segmento} sensibilidade consumidor",
                "margens {segmento} rentabilidade lucratividade",
                "custos {segmento} estrutura despesas operacionais"
            ],
            'distribution_channels': [
                "canais distribuição {segmento} vendas marketplace",
                "e-commerce {segmento} vendas online digital",
                "varejo {segmento} pontos venda distribuição",
                "logística {segmento} supply chain distribuição",
                "parcerias {segmento} canais indiretos revendas"
            ]
        }
    
    def _load_segment_keywords(self) -> Dict[str, List[str]]:
        """Carrega palavras-chave específicas por segmento"""
        return {
            'tecnologia': [
                'software', 'hardware', 'SaaS', 'cloud', 'IA', 'machine learning',
                'blockchain', 'IoT', 'big data', 'analytics', 'cybersecurity',
                'fintech', 'healthtech', 'edtech', 'proptech', 'agtech'
            ],
            'saude': [
                'medicina', 'hospitais', 'clínicas', 'telemedicina', 'farmácia',
                'biotecnologia', 'dispositivos médicos', 'diagnóstico', 'terapia',
                'SUS', 'planos saúde', 'ANS', 'ANVISA', 'CFM'
            ],
            'educacao': [
                'ensino', 'universidades', 'escolas', 'cursos', 'treinamento',
                'capacitação', 'EAD', 'e-learning', 'MEC', 'INEP',
                'educação básica', 'ensino superior', 'pós-graduação'
            ],
            'financeiro': [
                'bancos', 'fintechs', 'pagamentos', 'crédito', 'investimentos',
                'seguros', 'previdência', 'Bacen', 'CVM', 'Susep',
                'PIX', 'open banking', 'DeFi', 'criptomoedas'
            ],
            'varejo': [
                'e-commerce', 'marketplace', 'omnichannel', 'retail',
                'consumo', 'FMCG', 'moda', 'alimentação', 'casa',
                'shopping centers', 'franquias', 'atacado', 'distribuição'
            ],
            'agronegocio': [
                'agricultura', 'pecuária', 'agtech', 'commodities',
                'exportação', 'soja', 'milho', 'café', 'carne',
                'sustentabilidade', 'ESG', 'rastreabilidade'
            ]
        }
    
    def _load_market_intelligence_terms(self) -> List[str]:
        """Carrega termos de inteligência de mercado"""
        return [
            'dados', 'estatísticas', 'pesquisa', 'relatório', 'estudo',
            'análise', 'insights', 'tendências', 'projeções', 'cenários',
            'benchmarks', 'KPIs', 'métricas', 'indicadores', 'performance',
            'crescimento', 'expansão', 'oportunidades', 'ameaças', 'riscos',
            'inovação', 'disrupção', 'transformação', 'evolução', 'mudanças'
        ]
    
    def generate_comprehensive_queries(
        self, 
        base_query: str, 
        context: Dict[str, Any],
        max_queries: int = 20
    ) -> List[str]:
        """Gera queries abrangentes para pesquisa"""
        
        segmento = context.get('segmento', '').lower()
        produto = context.get('produto', '')
        publico = context.get('publico', '')
        
        logger.info(f"🧠 Gerando queries inteligentes para: {segmento}")
        
        all_queries = [base_query]  # Inclui query original
        
        # 1. Queries baseadas em templates
        template_queries = self._generate_from_templates(segmento, produto, publico)
        all_queries.extend(template_queries)
        
        # 2. Queries específicas do segmento
        segment_queries = self._generate_segment_specific_queries(segmento, produto)
        all_queries.extend(segment_queries)
        
        # 3. Queries de inteligência de mercado
        intelligence_queries = self._generate_market_intelligence_queries(segmento, context)
        all_queries.extend(intelligence_queries)
        
        # 4. Queries temporais (tendências)
        temporal_queries = self._generate_temporal_queries(segmento, produto)
        all_queries.extend(temporal_queries)
        
        # 5. Queries geográficas (Brasil específico)
        geographic_queries = self._generate_geographic_queries(segmento, produto)
        all_queries.extend(geographic_queries)
        
        # Remove duplicatas e queries muito similares
        unique_queries = self._deduplicate_and_rank_queries(all_queries, context)
        
        # Retorna top queries
        final_queries = unique_queries[:max_queries]
        
        logger.info(f"✅ {len(final_queries)} queries inteligentes geradas")
        
        return final_queries
    
    def _generate_from_templates(self, segmento: str, produto: str, publico: str) -> List[str]:
        """Gera queries a partir de templates"""
        
        queries = []
        
        for category, templates in self.query_templates.items():
            for template in templates:
                # Substitui placeholders
                query = template.format(segmento=segmento)
                
                # Adiciona produto se disponível
                if produto and '{produto}' not in template:
                    query = query.replace(segmento, f"{segmento} {produto}")
                
                queries.append(query)
        
        return queries
    
    def _generate_segment_specific_queries(self, segmento: str, produto: str) -> List[str]:
        """Gera queries específicas do segmento"""
        
        queries = []
        
        # Identifica segmento principal
        segment_key = self._identify_segment_category(segmento)
        
        if segment_key in self.segment_keywords:
            keywords = self.segment_keywords[segment_key]
            
            # Combina segmento com palavras-chave específicas
            for keyword in keywords[:10]:  # Top 10 keywords
                queries.extend([
                    f"{segmento} {keyword} Brasil mercado dados",
                    f"análise {keyword} {segmento} oportunidades",
                    f"tendências {keyword} {segmento} 2024"
                ])
        
        # Queries específicas por produto
        if produto:
            queries.extend([
                f"demanda {produto} {segmento} Brasil consumo",
                f"concorrentes {produto} {segmento} análise",
                f"preço {produto} {segmento} benchmarks",
                f"inovação {produto} {segmento} tecnologia"
            ])
        
        return queries
    
    def _generate_market_intelligence_queries(self, segmento: str, context: Dict[str, Any]) -> List[str]:
        """Gera queries de inteligência de mercado"""
        
        queries = []
        
        # Combina segmento com termos de inteligência
        for term in self.market_intelligence_terms[:15]:
            queries.append(f"{term} {segmento} Brasil 2024")
        
        # Queries de fontes específicas
        intelligence_sources = [
            'McKinsey', 'BCG', 'Deloitte', 'PwC', 'KPMG',
            'Bain', 'Accenture', 'EY', 'Oliver Wyman'
        ]
        
        for source in intelligence_sources[:5]:
            queries.append(f"{source} relatório {segmento} Brasil")
        
        # Queries de institutos brasileiros
        brazilian_institutes = [
            'IBGE', 'FGV', 'IPEA', 'CNI', 'FIESP',
            'Sebrae', 'BNDES', 'Banco Central'
        ]
        
        for institute in brazilian_institutes[:5]:
            queries.append(f"{institute} dados {segmento} Brasil")
        
        return queries
    
    def _generate_temporal_queries(self, segmento: str, produto: str) -> List[str]:
        """Gera queries temporais para capturar tendências"""
        
        queries = []
        
        # Queries por período
        time_periods = [
            '2024', '2025', 'últimos 12 meses', 'próximos anos',
            'pós-pandemia', 'atual cenário', 'nova era'
        ]
        
        for period in time_periods:
            queries.extend([
                f"{segmento} {period} crescimento tendências",
                f"mercado {segmento} {period} oportunidades",
                f"futuro {segmento} {period} predições"
            ])
        
        # Queries de evolução
        evolution_terms = [
            'evolução', 'transformação', 'mudanças', 'revolução',
            'disrupção', 'inovação', 'modernização'
        ]
        
        for term in evolution_terms:
            queries.append(f"{term} {segmento} Brasil impacto")
        
        return queries
    
    def _generate_geographic_queries(self, segmento: str, produto: str) -> List[str]:
        """Gera queries geográficas específicas do Brasil"""
        
        queries = []
        
        # Regiões brasileiras
        regions = [
            'Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte',
            'São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Paraná', 'Bahia'
        ]
        
        for region in regions[:8]:
            queries.extend([
                f"{segmento} {region} mercado regional",
                f"empresas {segmento} {region} principais"
            ])
        
        # Contexto brasileiro específico
        brazilian_context = [
            'economia brasileira', 'mercado interno', 'consumidor brasileiro',
            'empresas nacionais', 'indústria nacional', 'setor privado',
            'políticas públicas', 'ambiente regulatório'
        ]
        
        for context_term in brazilian_context:
            queries.append(f"{segmento} {context_term} impacto")
        
        return queries
    
    def _identify_segment_category(self, segmento: str) -> str:
        """Identifica categoria do segmento"""
        
        segmento_lower = segmento.lower()
        
        # Mapeia segmento para categoria
        segment_mapping = {
            'tecnologia': ['tecnologia', 'software', 'digital', 'tech', 'TI', 'sistemas'],
            'saude': ['saúde', 'medicina', 'médico', 'hospital', 'clínica', 'farmácia'],
            'educacao': ['educação', 'ensino', 'escola', 'curso', 'treinamento'],
            'financeiro': ['financeiro', 'banco', 'fintech', 'pagamento', 'crédito'],
            'varejo': ['varejo', 'comércio', 'loja', 'e-commerce', 'marketplace'],
            'agronegocio': ['agro', 'agricultura', 'pecuária', 'rural', 'campo']
        }
        
        for category, keywords in segment_mapping.items():
            if any(keyword in segmento_lower for keyword in keywords):
                return category
        
        return 'tecnologia'  # Default
    
    def _deduplicate_and_rank_queries(self, queries: List[str], context: Dict[str, Any]) -> List[str]:
        """Remove duplicatas e ranqueia queries por relevância"""
        
        # Remove duplicatas exatas
        unique_queries = list(dict.fromkeys(queries))
        
        # Remove queries muito similares
        filtered_queries = []
        
        for query in unique_queries:
            if not any(self._queries_too_similar(query, existing) for existing in filtered_queries):
                filtered_queries.append(query)
        
        # Ranqueia por relevância
        ranked_queries = self._rank_queries_by_relevance(filtered_queries, context)
        
        return ranked_queries
    
    def _queries_too_similar(self, query1: str, query2: str, threshold: float = 0.7) -> bool:
        """Verifica se duas queries são muito similares"""
        
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        
        # Calcula similaridade Jaccard
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union) if union else 0
        return similarity > threshold
    
    def _rank_queries_by_relevance(self, queries: List[str], context: Dict[str, Any]) -> List[str]:
        """Ranqueia queries por relevância"""
        
        segmento = context.get('segmento', '').lower()
        produto = context.get('produto', '').lower()
        publico = context.get('publico', '').lower()
        
        scored_queries = []
        
        for query in queries:
            score = self._calculate_query_relevance_score(query, segmento, produto, publico)
            scored_queries.append((query, score))
        
        # Ordena por score (maior primeiro)
        scored_queries.sort(key=lambda x: x[1], reverse=True)
        
        return [query for query, score in scored_queries]
    
    def _calculate_query_relevance_score(
        self, 
        query: str, 
        segmento: str, 
        produto: str, 
        publico: str
    ) -> float:
        """Calcula score de relevância da query"""
        
        score = 0.0
        query_lower = query.lower()
        
        # Score por menção do segmento
        if segmento in query_lower:
            score += 3.0
        
        # Score por menção do produto
        if produto and produto in query_lower:
            score += 2.0
        
        # Score por menção do público
        if publico and any(word in query_lower for word in publico.lower().split()):
            score += 1.5
        
        # Score por termos de alta qualidade
        high_quality_terms = [
            'dados', 'estatísticas', 'análise', 'pesquisa', 'relatório',
            'brasil', '2024', 'mercado', 'crescimento', 'oportunidades'
        ]
        
        for term in high_quality_terms:
            if term in query_lower:
                score += 0.5
        
        # Score por especificidade (queries mais longas são melhores)
        word_count = len(query.split())
        if word_count >= 6:
            score += 1.0
        elif word_count >= 4:
            score += 0.5
        
        # Penalty por termos muito genéricos
        generic_terms = ['geral', 'básico', 'simples', 'comum']
        for term in generic_terms:
            if term in query_lower:
                score -= 1.0
        
        return score
    
    def generate_follow_up_queries(
        self, 
        initial_results: List[Dict[str, Any]], 
        context: Dict[str, Any]
    ) -> List[str]:
        """Gera queries de follow-up baseadas nos resultados iniciais"""
        
        follow_up_queries = []
        
        # Analisa títulos dos resultados para identificar temas
        themes = self._extract_themes_from_results(initial_results)
        
        # Gera queries baseadas nos temas encontrados
        for theme in themes[:5]:
            follow_up_queries.extend([
                f"{theme} {context.get('segmento', '')} aprofundamento",
                f"detalhes {theme} {context.get('segmento', '')} Brasil",
                f"análise {theme} impacto {context.get('segmento', '')}"
            ])
        
        # Queries para preencher lacunas
        gap_queries = self._generate_gap_filling_queries(initial_results, context)
        follow_up_queries.extend(gap_queries)
        
        return follow_up_queries[:10]  # Top 10 follow-ups
    
    def _extract_themes_from_results(self, results: List[Dict[str, Any]]) -> List[str]:
        """Extrai temas dos resultados de busca"""
        
        themes = []
        
        # Analisa títulos e snippets
        all_text = ""
        for result in results:
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            all_text += f" {title} {snippet}"
        
        # Extrai palavras-chave relevantes
        words = re.findall(r'\b[a-záêçõ]{4,}\b', all_text.lower())
        
        # Conta frequência
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Filtra palavras relevantes
        relevant_words = [
            word for word, freq in word_freq.items() 
            if freq >= 2 and word not in ['brasil', 'mercado', 'empresa', 'dados']
        ]
        
        # Ordena por frequência
        relevant_words.sort(key=lambda x: word_freq[x], reverse=True)
        
        return relevant_words[:10]
    
    def _generate_gap_filling_queries(
        self, 
        initial_results: List[Dict[str, Any]], 
        context: Dict[str, Any]
    ) -> List[str]:
        """Gera queries para preencher lacunas de informação"""
        
        gap_queries = []
        segmento = context.get('segmento', '')
        
        # Identifica lacunas comuns
        common_gaps = [
            'custos operacionais', 'margens lucro', 'barreiras entrada',
            'cadeia valor', 'fornecedores', 'distribuidores',
            'regulamentação específica', 'certificações necessárias',
            'sazonalidade mercado', 'ciclos econômicos'
        ]
        
        for gap in common_gaps:
            gap_queries.append(f"{gap} {segmento} Brasil análise")
        
        # Queries para aspectos não cobertos
        if not any('preço' in r.get('title', '').lower() for r in initial_results):
            gap_queries.append(f"preços {segmento} Brasil benchmarks")
        
        if not any('regulament' in r.get('title', '').lower() for r in initial_results):
            gap_queries.append(f"regulamentação {segmento} Brasil normas")
        
        if not any('invest' in r.get('title', '').lower() for r in initial_results):
            gap_queries.append(f"investimentos {segmento} Brasil funding")
        
        return gap_queries
    
    def optimize_query_for_search_engine(self, query: str, search_engine: str) -> str:
        """Otimiza query para motor de busca específico"""
        
        optimized = query
        
        if search_engine == 'google':
            # Google responde bem a queries específicas
            optimized = f'"{query}" OR ({query.replace(" ", " AND ")})'
        
        elif search_engine == 'bing':
            # Bing prefere queries naturais
            optimized = query + " site:*.com.br OR site:*.org.br"
        
        elif search_engine == 'duckduckgo':
            # DuckDuckGo funciona bem com operadores simples
            optimized = query + " !br"
        
        elif search_engine == 'academic':
            # Fontes acadêmicas
            optimized = query + " filetype:pdf OR site:*.edu.br"
        
        return optimized
    
    def generate_negative_keywords(self, context: Dict[str, Any]) -> List[str]:
        """Gera palavras-chave negativas para filtrar resultados irrelevantes"""
        
        negative_keywords = [
            # Termos genéricos irrelevantes
            'login', 'cadastro', 'entrar', 'registrar', 'conta',
            'download', 'baixar', 'instalar', 'app', 'aplicativo',
            'contato', 'sobre', 'quem somos', 'história', 'missão',
            'vagas', 'trabalhe conosco', 'carreiras', 'jobs',
            'termos uso', 'privacidade', 'cookies', 'política',
            
            # Termos de e-commerce irrelevantes
            'comprar', 'preço', 'oferta', 'promoção', 'desconto',
            'carrinho', 'checkout', 'pagamento', 'frete',
            
            # Termos de redes sociais
            'instagram', 'facebook', 'twitter', 'linkedin',
            'youtube', 'tiktok', 'whatsapp', 'telegram',
            
            # Termos técnicos irrelevantes
            'tutorial', 'como fazer', 'passo a passo', 'dicas',
            'truques', 'hacks', 'review', 'análise produto'
        ]
        
        return negative_keywords

# Instância global
intelligent_query_generator = IntelligentQueryGenerator()