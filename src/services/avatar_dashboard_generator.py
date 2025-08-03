#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Avatar Dashboard Generator
Gerador do Dashboard Arqueológico do Avatar baseado nos anexos
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class AvatarDashboardGenerator:
    """Gerador do Dashboard Arqueológico do Avatar baseado nos anexos"""
    
    def __init__(self):
        """Inicializa gerador do dashboard"""
        # Prompt especializado para marketing de conteúdo
        self.content_marketer_prompt = """
        You are a content marketer specializing in engaging, SEO-optimized content.
        
        Focus Areas:
        - Blog posts with keyword optimization
        - Social media content (Twitter/X, LinkedIn, etc.)
        - Email newsletter campaigns
        - SEO meta descriptions and titles
        - Content calendar planning
        - Call-to-action optimization
        
        Approach:
        1. Start with audience pain points
        2. Use data to support claims
        3. Include relevant keywords naturally
        4. Write scannable content with headers
        5. Always include a clear CTA
        6. Focus on value-first content
        7. Include hooks and storytelling elements
        """
        
        self.dashboard_structure = self._load_dashboard_structure()
        self.analysis_framework = self._load_analysis_framework()
        self.dashboard_completo_anexos = self._load_dashboard_completo_anexos()
        
        logger.info("Avatar Dashboard Generator inicializado com metodologia dos anexos")
    
    def _load_dashboard_completo_anexos(self) -> Dict[str, Any]:
        """Carrega dashboard completo dos anexos MASI"""
        return {
            'visao_geral_anexos': {
                'publico_analisado': 'Total de 28 empresas/alunos avaliados',
                'distribuicao_faturamento': {
                    '64_porcento_acima_5mi': 'Empresas consolidadas buscando próximo salto estratégico',
                    '32_porcento_1_a_5mi': 'Empresas em zona de transição, maior necessidade de estruturação',
                    '20_porcento_abaixo_1mi': 'Empresas em estágio inicial com desafios básicos'
                },
                'principais_desafios': [
                    '87% relatam estar presos no nível operacional',
                    '92% possuem faturamento entre R$ 1-10 milhões',
                    '100% apresentam problemas de gestão de pessoas'
                ]
            },
            'analise_dores_anexos': {
                'top_10_dores_estruturadas': [
                    {
                        'dor': 'Desenvolvimento de Liderança e Gestão de Pessoas',
                        'mencoes': '5 (20%)',
                        'contexto': 'Dificuldade em formar líderes internos capazes'
                    },
                    {
                        'dor': 'Construção de uma Cultura Organizacional Forte',
                        'mencoes': '4 (16%)',
                        'contexto': 'Falta de cultura consistente que sustente crescimento'
                    },
                    {
                        'dor': 'Fortalecimento da Operação e Processos',
                        'mencoes': '4 (16%)',
                        'contexto': 'Operações dependentes do fundador, processos frágeis'
                    },
                    {
                        'dor': 'Clareza e Comunicação da Proposta de Valor',
                        'mencoes': '3 (12%)',
                        'contexto': 'Dificuldade em definir e comunicar valor único'
                    },
                    {
                        'dor': 'Acompanhamento de Indicadores e Tomada de Decisão com Dados',
                        'mencoes': '3 (12%)',
                        'contexto': 'Carência de gestão orientada por métricas'
                    }
                ],
                'convergencia_principal': 'Gestão de Pessoas aparece como dor mais crítica',
                'descoberta_relevante': 'Cultura Organizacional tem destaque quando estruturada',
                'gap_identificado': 'Gestão Financeira é necessidade latente'
            },
            'desejos_motivacoes_anexos': {
                'sonhos_profundos': [
                    'Ausência Produtiva: desejo de se afastar da operação',
                    'Máquina Empresarial Perfeita: processos totalmente automatizados',
                    'Multiplicação Acelerada: objetivo de triplicar o faturamento',
                    'Reconhecimento no Mercado: ser o empresário que revolucionou o segmento'
                ],
                'desejos_expressos': [
                    'Escalar o negócio para novos patamares',
                    'Criar uma máquina de vendas que funcione de forma consistente',
                    'Fazer com que a equipe trabalhe para a empresa e não para o fundador',
                    'Romper a barreira de faturamento de R$ 5 milhões/ano'
                ],
                'gatilhos_emocionais': [
                    'Liberdade: construir empresa que cresce sem depender do fundador',
                    'Controle: transformar o caos em previsibilidade com processos claros',
                    'Legado: criar algo que impacte o mercado e seja maior que o próprio fundador',
                    'Velocidade: crescer de forma exponencial, com resultados concretos em até 12 meses'
                ]
            },
            'comportamento_anexos': {
                'arquetipos_dominantes': {
                    'tecnico_aprisionado': {
                        'percentual': '30%',
                        'descricao': 'Profissional de origem técnica preso à execução',
                        'caracteristicas': 'Deveria atuar na estratégia mas continua na operação'
                    },
                    'escalador_frustrado': {
                        'percentual': '40%',
                        'descricao': 'Empresário estagnado há anos no mesmo nível',
                        'caracteristicas': 'Trabalha duro, custos sobem, lucros diminuem'
                    },
                    'visionario_sufocado': {
                        'percentual': '30%',
                        'descricao': 'Líder com visão clara mas equipe que não acompanha',
                        'caracteristicas': 'Frustrado porque equipe não tem mentalidade de crescimento'
                    }
                },
                'medos_paralisantes': [
                    'Terror da Irrelevância: medo de ter produto bom mas não conseguir reconhecimento',
                    'Pânico da Dependência Eterna: receio de nunca se desvincular da operação',
                    'Medo da Traição: insegurança em delegar por medo de traição ou incompetência',
                    'Pavor do Modelo Errado: desconfiança de que empresa foi construída sobre bases frágeis'
                ],
                'objecoes_reais': [
                    '"Já tentei de tudo, nada funciona": ceticismo após experiências frustradas',
                    '"Meu negócio é muito específico": resistência a soluções padronizadas',
                    '"Não tenho tempo para implementar": paradoxo onde precisa de ajuda mas não consegue parar'
                ]
            },
            'arsenal_tatico_anexos': {
                'estruturacao_mentoria_modulos': [
                    {
                        'modulo': 'Libertação do Operacional (Gestão de Pessoas/Time)',
                        'framework': 'Framework de delegação progressiva',
                        'sistema': 'Sistema de formação de líderes internos',
                        'protocolo': 'Protocolo de autonomia para times que pensam como donos',
                        'estudo_caso': 'Redução de carga operacional de 80h/semana para 20h/semana'
                    },
                    {
                        'modulo': 'Máquina de Vendas Previsível (Vendas e Comercial)',
                        'framework': 'Blueprint para vendas recorrentes B2B',
                        'sistema': 'Sistema de qualificação de leads com conversão 3x maior',
                        'protocolo': 'Automação comercial desde primeiro contato até LTV',
                        'estudo_caso': 'Workshop prático para construção de playbook de vendas'
                    },
                    {
                        'modulo': 'Processos que Escalam (Processos e Gestão)',
                        'framework': 'Documentação de SOPs utilizados pela equipe',
                        'sistema': 'Dashboard com os 5 KPIs críticos para controle operacional',
                        'protocolo': 'Adaptação de metodologias ágeis para PMEs',
                        'estudo_caso': 'Ferramentas para controle e estruturação em 30 dias'
                    },
                    {
                        'modulo': 'Escala Inteligente (Modelo de Negócio e Estratégia)',
                        'framework': 'Análise de unit economics para decisões sobre escala',
                        'sistema': 'Pivotagem estratégica com cases de sucesso',
                        'protocolo': 'Transição de serviço para produto para aumento de margens',
                        'estudo_caso': 'Comparação entre expansão geográfica e digital'
                    },
                    {
                        'modulo': 'Cultura de Alta Performance (Cultura e Liderança)',
                        'framework': 'Framework para transformar cultura organizacional em prática',
                        'sistema': 'Sistema de feedback contínuo para evolução da equipe',
                        'protocolo': 'Estrutura de reuniões curtas e eficazes (15min)',
                        'estudo_caso': 'Caso prático: empresa que funciona sem o fundador'
                    }
                ],
                'linguagem_recomendada': {
                    'substituir_processo_comercial_por': 'máquina de vendas',
                    'substituir_crescer_gradualmente_por': 'romper barreiras',
                    'substituir_delegar_tarefas_por': 'time autônomo',
                    'substituir_work_life_balance_por': 'liberdade',
                    'substituir_melhorar_processos_por': 'revolucionar operação',
                    'substituir_aumentar_vendas_por': 'dominar mercado',
                    'substituir_contratar_pessoas_por': 'formar líderes',
                    'substituir_organizar_empresa_por': 'construir império'
                }
            }
        }
    
    def _load_dashboard_structure(self) -> Dict[str, Any]:
        """Carrega estrutura do dashboard dos anexos"""
        return {
            'visao_geral': {
                'publico_analisado': 'Total de empresas/alunos avaliados',
                'distribuicao_faturamento': 'Categorização por faturamento anual',
                'principais_desafios': 'Desafios identificados no grupo'
            },
            'analise_dores': {
                'top_10_dores_estruturadas': 'Dores com frequência e contexto',
                'analise_comparativa': 'Convergência entre dores abertas e estruturadas',
                'gap_identificado': 'Necessidades latentes descobertas'
            },
            'desejos_motivacoes': {
                'sonhos_profundos': 'Sonhos mais profundos identificados',
                'desejos_expressos': 'Desejos de maneira direta',
                'gatilhos_emocionais': 'Gatilhos mais eficazes'
            },
            'comportamento': {
                'arquetipos_dominantes': 'Técnico Aprisionado, Escalador Frustrado, Visionário Sufocado',
                'medos_paralisantes': 'Medos que paralisam decisões',
                'objecoes_reais': 'Objeções ao buscar soluções externas'
            },
            'insights_ocultos': {
                'gatilhos_eficazes': 'Gatilhos emocionais mais eficazes',
                'abordagens_impacto': 'Abordagens que geram maior impacto'
            },
            'arsenal_tatico': {
                'estruturacao_mentoria': 'Estruturação da mentoria em módulos',
                'formatos_entrega': 'Formatos e ferramentas de entrega',
                'estrutura_ideal': 'Estrutura ideal da mentoria'
            }
        }
    
    def _load_analysis_framework(self) -> Dict[str, Any]:
        """Carrega framework de análise dos anexos"""
        return {
            'distribuicao_faturamento': {
                'alto_faturamento': {
                    'percentual': '64%',
                    'faixa': 'Acima de R$ 5 milhões/ano',
                    'perfil': 'Empresas consolidadas buscando próximo salto estratégico'
                },
                'medio_faturamento': {
                    'percentual': '32%',
                    'faixa': 'Entre R$ 1 milhão e R$ 5 milhões/ano',
                    'perfil': 'Empresas em zona de transição, maior necessidade de estruturação'
                },
                'baixo_faturamento': {
                    'percentual': '20%',
                    'faixa': 'Menos de R$ 1 milhão/ano',
                    'perfil': 'Empresas em estágio inicial com desafios básicos'
                }
            },
            'arquetipos_empresariais': {
                'tecnico_aprisionado': {
                    'percentual': '30%',
                    'descricao': 'Profissional de origem técnica preso à execução',
                    'caracteristicas': 'Deveria atuar na estratégia mas continua na operação'
                },
                'escalador_frustrado': {
                    'percentual': '40%',
                    'descricao': 'Empresário estagnado há anos no mesmo nível',
                    'caracteristicas': 'Trabalha duro, custos sobem, lucros diminuem'
                },
                'visionario_sufocado': {
                    'percentual': '30%',
                    'descricao': 'Líder com visão clara mas equipe que não acompanha',
                    'caracteristicas': 'Frustrado porque equipe não tem mentalidade de crescimento'
                }
            },
            'top_10_dores_masi': [
                {
                    'dor': 'Desenvolvimento de Liderança e Gestão de Pessoas',
                    'mencoes': '5 (20%)',
                    'contexto': 'Dificuldade em formar líderes internos capazes'
                },
                {
                    'dor': 'Construção de uma Cultura Organizacional Forte',
                    'mencoes': '4 (16%)',
                    'contexto': 'Falta de cultura consistente que sustente crescimento'
                },
                {
                    'dor': 'Fortalecimento da Operação e Processos',
                    'mencoes': '4 (16%)',
                    'contexto': 'Operações dependentes do fundador, processos frágeis'
                },
                {
                    'dor': 'Clareza e Comunicação da Proposta de Valor',
                    'mencoes': '3 (12%)',
                    'contexto': 'Dificuldade em definir e comunicar valor único'
                },
                {
                    'dor': 'Acompanhamento de Indicadores e Tomada de Decisão com Dados',
                    'mencoes': '3 (12%)',
                    'contexto': 'Carência de gestão orientada por métricas'
                }
            ]
        }
    
    def generate_archaeological_avatar_dashboard(
        self, 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera dashboard arqueológico completo baseado nos anexos"""
        
        try:
            logger.info("📊 Gerando Dashboard Arqueológico do Avatar")
            
            # Salva dados de entrada
            salvar_etapa("dashboard_entrada", {
                "avatar_data": avatar_data,
                "context_data": context_data
            }, categoria="avatar")
            
            # 1. VISÃO GERAL
            visao_geral = self._create_overview_section(avatar_data, context_data)
            
            # 2. ANÁLISE DE DORES
            analise_dores = self._create_pain_analysis_section(avatar_data, context_data)
            
            # 3. DESEJOS E MOTIVAÇÕES
            desejos_motivacoes = self._create_desires_section(avatar_data, context_data)
            
            # 4. COMPORTAMENTO
            comportamento = self._create_behavior_section(avatar_data, context_data)
            
            # 5. INSIGHTS OCULTOS
            insights_ocultos = self._create_hidden_insights_section(avatar_data, context_data)
            
            # 6. ARSENAL TÁTICO
            arsenal_tatico = self._create_tactical_arsenal_section(avatar_data, context_data)
            
            # 7. LINGUAGEM RECOMENDADA
            linguagem_recomendada = self._create_language_recommendations(avatar_data, context_data)
            
            dashboard = {
                'titulo': 'DASHBOARD ARQUEOLÓGICO DO AVATAR',
                'subtitulo': f'Análise profunda - Visão completa do perfil {context_data.get("segmento", "empresarial")}',
                'visao_geral': visao_geral,
                'analise_dores': analise_dores,
                'desejos_motivacoes': desejos_motivacoes,
                'comportamento': comportamento,
                'insights_ocultos': insights_ocultos,
                'arsenal_tatico': arsenal_tatico,
                'linguagem_recomendada': linguagem_recomendada,
                 'dashboard_anexos_completo': self.dashboard_completo_anexos,
                 'metodologia_masi': {
                     'base_analise': '28 empresas/alunos avaliados',
                     'distribuicao_faturamento': 'Análise por faixas de receita',
                     'arquetipos_identificados': 'Técnico Aprisionado, Escalador Frustrado, Visionário Sufocado',
                     'top_10_dores_estruturadas': 'Baseado em frequência e contexto real',
                     'gatilhos_emocionais_eficazes': 'Liberdade, Controle, Legado, Velocidade'
                 },
                'metadata': {
                    'gerado_em': datetime.now().isoformat(),
                    'baseado_em': 'Metodologia Dashboard MASI dos anexos',
                    'versao': '2.0_enhanced_with_annexes',
                    'fonte_dados': 'Análise de 28 empresas MASI'
                }
            }
            
            # Salva dashboard completo
            salvar_etapa("dashboard_completo", dashboard, categoria="avatar")
            
            logger.info("✅ Dashboard Arqueológico do Avatar gerado com sucesso")
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar dashboard: {e}")
            salvar_erro("dashboard_avatar", e, contexto=context_data)
            return self._create_fallback_dashboard(context_data)
    
    def _create_overview_section_annexes(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de visão geral baseada nos anexos MASI"""
        
        segmento = context_data.get('segmento', 'negócios')
        objetivo_receita = context_data.get('objetivo_receita', 0)
        
        # Determina categoria de faturamento baseada nos anexos
        if objetivo_receita > 5000000:
            categoria_faturamento = {
                'faixa': 'Acima de R$ 5 milhões/ano',
                'percentual': '64%',
                'perfil': 'Empresas consolidadas buscando próximo salto estratégico'
            }
        elif objetivo_receita > 1000000:
            categoria_faturamento = {
                'faixa': 'Entre R$ 1 milhão e R$ 5 milhões/ano',
                'percentual': '32%',
                'perfil': 'Empresas em zona de transição, maior necessidade de estruturação'
            }
        else:
            categoria_faturamento = {
                'faixa': 'Menos de R$ 1 milhão/ano',
                'percentual': '20%',
                'perfil': 'Empresas em estágio inicial com desafios básicos'
            }
        
        return {
            'publico_analisado': f'Avatar para {segmento} baseado em metodologia MASI',
            'distribuicao_faturamento': categoria_faturamento,
            'principais_desafios': self.dashboard_completo_anexos['visao_geral_anexos']['principais_desafios'],
            'base_metodologica': 'Análise de 28 empresas/alunos MASI',
            'aplicacao_segmento': f'Adaptado especificamente para {segmento}'
        }
    
    def _create_pain_analysis_section_annexes(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de análise de dores baseada no top 10 dos anexos"""
        
        dores_avatar = avatar_data.get('dores_viscerais', [])
        
        # Usa top 10 dores estruturadas dos anexos
        top_10_anexos = self.dashboard_completo_anexos['analise_dores_anexos']['top_10_dores_estruturadas']
        
        # Mapeia dores do avatar para estrutura MASI
        dores_mapeadas = []
        
        for i, dor_masi in enumerate(top_10_anexos, 1):
            # Verifica se alguma dor do avatar se relaciona
            dor_relacionada = self._find_related_pain_annexes(dor_masi['dor'], dores_avatar)
            
            dores_mapeadas.append({
                'posicao': i,
                'dor_estruturada': dor_masi['dor'],
                'mencoes_masi': dor_masi['mencoes'],
                'contexto_masi': dor_masi['contexto'],
                'dor_avatar_relacionada': dor_relacionada,
                'intensidade': 'Alta' if i <= 3 else 'Média' if i <= 7 else 'Baixa',
                'aplicacao_segmento': f"Como se manifesta em {context_data.get('segmento', 'negócios')}"
            })
        
        return {
            'top_10_dores_estruturadas_masi': dores_mapeadas,
            'analise_comparativa': self.dashboard_completo_anexos['analise_dores_anexos'],
            'dores_avatar_originais': dores_avatar[:10],
            'mapeamento_intensidade': self._map_pain_intensity_annexes(dores_avatar),
            'convergencia_principal': 'Gestão de Pessoas como dor mais crítica (baseado em MASI)',
            'gap_identificado': 'Gestão Financeira como necessidade latente'
        }
    
    def _create_desires_section_annexes(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de desejos baseada nos anexos"""
        
        desejos_avatar = avatar_data.get('desejos_profundos', [])
        desejos_anexos = self.dashboard_completo_anexos['desejos_motivacoes_anexos']
        
        return {
            'sonhos_profundos_masi': desejos_anexos['sonhos_profundos'],
            'desejos_expressos_masi': desejos_anexos['desejos_expressos'],
            'desejos_avatar_mapeados': desejos_avatar,
            'gatilhos_emocionais_eficazes': desejos_anexos['gatilhos_emocionais'],
            'aplicacao_segmento': f"Desejos específicos para {context_data.get('segmento', 'negócios')}"
        }
    
    def _create_behavior_section_annexes(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de comportamento baseada nos arquétipos dos anexos"""
        
        # Determina arquétipo dominante baseado no avatar
        arquetipo = self._determine_dominant_archetype_annexes(avatar_data, context_data)
        comportamento_anexos = self.dashboard_completo_anexos['comportamento_anexos']
        
        return {
            'arquetipos_dominantes_masi': comportamento_anexos['arquetipos_dominantes'],
            'arquetipo_identificado': arquetipo,
            'medos_paralisantes_masi': comportamento_anexos['medos_paralisantes'],
            'objecoes_reais_masi': comportamento_anexos['objecoes_reais'],
            'padroes_comportamentais': self._identify_behavioral_patterns_annexes(avatar_data),
            'aplicacao_avatar': f"Comportamento específico do avatar em {context_data.get('segmento', 'negócios')}"
        }
    
    def _create_tactical_arsenal_section_annexes(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de arsenal tático baseada nos anexos"""
        
        arsenal_anexos = self.dashboard_completo_anexos['arsenal_tatico_anexos']
        
        return {
            'estruturacao_mentoria_modulos_masi': arsenal_anexos['estruturacao_mentoria_modulos'],
            'formatos_ferramentas_entrega': [
                'Lives semanais com análise de casos reais',
                'Templates prontos para uso imediato (planilhas, dashboards e SOPs)',
                'Simulações e role-playing para treinar situações críticas',
                'Táticas rápidas de implementação com resultados em até 24h'
            ],
            'estrutura_ideal_mentoria': [
                'Diagnóstico profundo e direto, sem filtros',
                'Quick Wins imediatos para gerar resultados rápidos',
                'Roadmap estratégico de 90 dias com métricas claras',
                'Sistema de accountability intensivo para garantir execução'
            ],
            'aplicacao_segmento': f"Arsenal adaptado para {context_data.get('segmento', 'negócios')}"
        }
    
    def _create_language_recommendations_annexes(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, str]:
        """Cria recomendações de linguagem dos anexos"""
        
        return self.dashboard_completo_anexos['arsenal_tatico_anexos']['linguagem_recomendada']
    
    def _determine_dominant_archetype_annexes(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> str:
        """Determina arquétipo dominante baseado nos anexos"""
        
        dores = avatar_data.get('dores_viscerais', [])
        segmento = context_data.get('segmento', '').lower()
        
        # Análise baseada nas dores e segmento conforme anexos
        if any('técnico' in dor.lower() or 'operacional' in dor.lower() for dor in dores):
            return 'Técnico Aprisionado (30%) - Profissional de origem técnica preso à execução'
        elif any('estagnado' in dor.lower() or 'mesmo nível' in dor.lower() for dor in dores):
            return 'Escalador Frustrado (40%) - Empresário estagnado há anos no mesmo nível'
        elif any('equipe' in dor.lower() or 'liderança' in dor.lower() for dor in dores):
            return 'Visionário Sufocado (30%) - Líder com visão clara mas equipe que não acompanha'
        else:
            # Default baseado no segmento
            if 'tecnologia' in segmento or 'consultoria' in segmento:
                return 'Técnico Aprisionado (30%) - Profissional de origem técnica preso à execução'
            else:
                return 'Escalador Frustrado (40%) - Empresário estagnado há anos no mesmo nível'
    
    def _find_related_pain_annexes(self, pain_masi: str, avatar_pains: List[str]) -> Optional[str]:
        """Encontra dor do avatar relacionada à dor MASI dos anexos"""
        
        pain_keywords = {
            'Desenvolvimento de Liderança': ['liderança', 'gestão', 'equipe', 'pessoas'],
            'Cultura Organizacional': ['cultura', 'valores', 'ambiente', 'clima'],
            'Operação e Processos': ['processo', 'operação', 'sistema', 'procedimento'],
            'Proposta de Valor': ['valor', 'diferencial', 'posicionamento', 'proposta'],
            'Indicadores e Dados': ['dados', 'métricas', 'indicadores', 'kpi']
        }
        
        for keyword_group in pain_keywords.values():
            for keyword in keyword_group:
                if keyword in pain_masi.lower():
                    # Busca dor relacionada no avatar
                    for avatar_pain in avatar_pains:
                        if any(kw in avatar_pain.lower() for kw in keyword_group):
                            return avatar_pain
        
        return None
    
    def _map_pain_intensity_annexes(self, dores: List[str]) -> Dict[str, List[str]]:
        """Mapeia intensidade das dores baseado nos anexos"""
        
        alta_intensidade = []
        media_intensidade = []
        baixa_intensidade = []
        
        for dor in dores:
            if any(word in dor.lower() for word in ['excessivamente', 'sempre', 'nunca', 'constantemente']):
                alta_intensidade.append(dor)
            elif any(word in dor.lower() for word in ['frequentemente', 'muitas vezes', 'geralmente']):
                media_intensidade.append(dor)
            else:
                baixa_intensidade.append(dor)
        
        return {
            'alta_intensidade': alta_intensidade,
            'media_intensidade': media_intensidade,
            'baixa_intensidade': baixa_intensidade,
            'metodologia': 'Baseada em análise de frequência de palavras-chave MASI'
        }
    
    def _identify_behavioral_patterns_annexes(self, avatar_data: Dict[str, Any]) -> List[str]:
        """Identifica padrões comportamentais baseados nos anexos"""
        
        patterns = []
        
        # Análise baseada nas objeções dos anexos
        objecoes = avatar_data.get('objecoes_reais', [])
        
        if any('já tentei' in obj.lower() for obj in objecoes):
            patterns.append('Padrão de múltiplas tentativas frustradas (identificado em MASI)')
        
        if any('tempo' in obj.lower() for obj in objecoes):
            patterns.append('Padrão de sobrecarga operacional (87% dos casos MASI)')
        
        if any('específico' in obj.lower() for obj in objecoes):
            patterns.append('Padrão de resistência a soluções padronizadas (comum em MASI)')
        
        # Análise baseada nos medos dos anexos
        medos = avatar_data.get('medos_paralisantes', [])
        
        if medos:
            patterns.append('Padrão de paralisia por análise excessiva (Terror da Irrelevância)')
            patterns.append('Padrão de medo de mudança estrutural (Pânico da Dependência Eterna)')
        
        return patterns
    
    def _create_overview_section(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de visão geral"""
        
        segmento = context_data.get('segmento', 'negócios')
        objetivo_receita = context_data.get('objetivo_receita', 0)
        
        # Determina categoria de faturamento
        if objetivo_receita > 5000000:
            categoria_faturamento = self.analysis_framework['distribuicao_faturamento']['alto_faturamento']
        elif objetivo_receita > 1000000:
            categoria_faturamento = self.analysis_framework['distribuicao_faturamento']['medio_faturamento']
        else:
            categoria_faturamento = self.analysis_framework['distribuicao_faturamento']['baixo_faturamento']
        
        return {
            'publico_analisado': f'Avatar para {segmento}',
            'distribuicao_faturamento': {
                'categoria': categoria_faturamento['faixa'],
                'percentual': categoria_faturamento['percentual'],
                'perfil': categoria_faturamento['perfil']
            },
            'principais_desafios': [
                '87% relatam estar presos no nível operacional',
                '92% possuem faturamento entre R$ 1-10 milhões',
                '100% apresentam problemas de gestão de pessoas'
            ]
        }
    
    def _create_pain_analysis_section(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de análise de dores"""
        
        dores_avatar = avatar_data.get('dores_viscerais', [])
        
        # Mapeia dores do avatar para estrutura MASI
        dores_estruturadas = []
        
        for i, dor_masi in enumerate(self.analysis_framework['top_10_dores_masi'][:10], 1):
            # Verifica se alguma dor do avatar se relaciona
            dor_relacionada = self._find_related_pain(dor_masi['dor'], dores_avatar)
            
            dores_estruturadas.append({
                'posicao': i,
                'dor': dor_masi['dor'],
                'mencoes': dor_masi['mencoes'],
                'contexto': dor_masi['contexto'],
                'dor_avatar_relacionada': dor_relacionada,
                'intensidade': 'Alta' if i <= 3 else 'Média' if i <= 7 else 'Baixa'
            })
        
        return {
            'top_10_dores_estruturadas': dores_estruturadas,
            'analise_comparativa': {
                'convergencia_principal': 'Gestão de Pessoas aparece como dor mais crítica',
                'descoberta_relevante': 'Cultura Organizacional tem destaque quando estruturada',
                'gap_identificado': 'Gestão Financeira é necessidade latente'
            },
            'dores_avatar_originais': dores_avatar[:10],
            'mapeamento_intensidade': self._map_pain_intensity(dores_avatar)
        }
    
    def _create_desires_section(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de desejos e motivações"""
        
        desejos_avatar = avatar_data.get('desejos_profundos', [])
        
        return {
            'sonhos_profundos_identificados': [
                'Ausência Produtiva: desejo de se afastar da operação',
                'Máquina Empresarial Perfeita: processos totalmente automatizados',
                'Multiplicação Acelerada: objetivo de triplicar o faturamento',
                'Reconhecimento no Mercado: ser o empresário que revolucionou o segmento'
            ],
            'desejos_expressos_diretamente': [
                'Escalar o negócio para novos patamares',
                'Criar uma máquina de vendas que funcione de forma consistente',
                'Fazer com que a equipe trabalhe para a empresa e não para o fundador',
                'Romper a barreira de faturamento de R$ 5 milhões/ano'
            ],
            'desejos_avatar_mapeados': desejos_avatar,
            'gatilhos_emocionais_eficazes': [
                'Liberdade: construir empresa que cresce sem depender do fundador',
                'Controle: transformar o caos em previsibilidade com processos claros',
                'Legado: criar algo que impacte o mercado e seja maior que o próprio fundador',
                'Velocidade: crescer de forma exponencial, com resultados concretos em até 12 meses'
            ]
        }
    
    def _create_behavior_section(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de comportamento"""
        
        # Determina arquétipo dominante baseado no avatar
        arquetipo = self._determine_dominant_archetype(avatar_data, context_data)
        
        return {
            'arquetipos_dominantes': {
                'arquetipo_identificado': arquetipo,
                'distribuicao_geral': self.analysis_framework['arquetipos_empresariais']
            },
            'medos_paralisantes': [
                'Terror da Irrelevância: medo de ter produto bom mas não conseguir reconhecimento',
                'Pânico da Dependência Eterna: receio de nunca se desvincular da operação',
                'Medo da Traição: insegurança em delegar por medo de traição ou incompetência',
                'Pavor do Modelo Errado: desconfiança de que empresa foi construída sobre bases frágeis'
            ],
            'objecoes_reais_buscar_solucoes': [
                '"Já tentei de tudo, nada funciona": ceticismo após experiências frustradas',
                '"Meu negócio é muito específico": resistência a soluções padronizadas',
                '"Não tenho tempo para implementar": paradoxo onde precisa de ajuda mas não consegue parar'
            ],
            'padroes_comportamentais': self._identify_behavioral_patterns(avatar_data)
        }
    
    def _create_hidden_insights_section(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de insights ocultos"""
        
        return {
            'gatilhos_emocionais_eficazes': [
                'Liberdade: construir uma empresa que cresce sem depender do fundador',
                'Controle: transformar o caos em previsibilidade com processos claros',
                'Legado: criar algo que impacte o mercado e seja maior que o próprio fundador',
                'Velocidade: crescer de forma exponencial, com resultados concretos em até 12 meses'
            ],
            'abordagens_maior_impacto': [
                'Honestidade brutal: empresários estão cansados de abordagens superficiais',
                'Casos reais: preferem ver exemplos concretos e resultados palpáveis',
                'Métodos práticos: valorizam o "como fazer" acima de teorias motivacionais',
                'Quick Wins: precisam de resultados rápidos para manter o engajamento'
            ],
            'descobertas_comportamentais': self._extract_behavioral_discoveries(avatar_data),
            'oportunidades_ocultas': self._identify_hidden_opportunities(avatar_data, context_data)
        }
    
    def _create_tactical_arsenal_section(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de arsenal tático"""
        
        return {
            'estruturacao_mentoria_modulos': [
                {
                    'modulo': 'Libertação do Operacional (Gestão de Pessoas/Time)',
                    'framework': 'Framework de delegação progressiva',
                    'sistema': 'Sistema de formação de líderes internos',
                    'protocolo': 'Protocolo de autonomia para times que pensam como donos',
                    'estudo_caso': 'Redução de carga operacional de 80h/semana para 20h/semana'
                },
                {
                    'modulo': 'Máquina de Vendas Previsível (Vendas e Comercial)',
                    'framework': 'Blueprint para vendas recorrentes B2B',
                    'sistema': 'Sistema de qualificação de leads com conversão 3x maior',
                    'protocolo': 'Automação comercial desde primeiro contato até LTV',
                    'estudo_caso': 'Workshop prático para construção de playbook de vendas'
                },
                {
                    'modulo': 'Processos que Escalam (Processos e Gestão)',
                    'framework': 'Documentação de SOPs utilizados pela equipe',
                    'sistema': 'Dashboard com os 5 KPIs críticos para controle operacional',
                    'protocolo': 'Adaptação de metodologias ágeis para PMEs',
                    'estudo_caso': 'Ferramentas para controle e estruturação em 30 dias'
                },
                {
                    'modulo': 'Escala Inteligente (Modelo de Negócio e Estratégia)',
                    'framework': 'Análise de unit economics para decisões sobre escala',
                    'sistema': 'Pivotagem estratégica com cases de sucesso',
                    'protocolo': 'Transição de serviço para produto para aumento de margens',
                    'estudo_caso': 'Comparação entre expansão geográfica e digital'
                },
                {
                    'modulo': 'Cultura de Alta Performance (Cultura e Liderança)',
                    'framework': 'Framework para transformar cultura organizacional em prática',
                    'sistema': 'Sistema de feedback contínuo para evolução da equipe',
                    'protocolo': 'Estrutura de reuniões curtas e eficazes (15min)',
                    'estudo_caso': 'Caso prático: empresa que funciona sem o fundador'
                }
            ],
            'formatos_ferramentas_entrega': [
                'Lives semanais com análise de casos reais',
                'Templates prontos para uso imediato (planilhas, dashboards e SOPs)',
                'Simulações e role-playing para treinar situações críticas',
                'Táticas rápidas de implementação com resultados em até 24h'
            ],
            'estrutura_ideal_mentoria': [
                'Diagnóstico profundo e direto, sem filtros',
                'Quick Wins imediatos para gerar resultados rápidos',
                'Roadmap estratégico de 90 dias com métricas claras',
                'Sistema de accountability intensivo para garantir execução'
            ]
        }
    
    def _create_language_recommendations(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, str]:
        """Cria recomendações de linguagem dos anexos"""
        
        return {
            'substituir_processo_comercial_por': 'máquina de vendas',
            'substituir_crescer_gradualmente_por': 'romper barreiras',
            'substituir_delegar_tarefas_por': 'time autônomo',
            'substituir_work_life_balance_por': 'liberdade',
            'substituir_melhorar_processos_por': 'revolucionar operação',
            'substituir_aumentar_vendas_por': 'dominar mercado',
            'substituir_contratar_pessoas_por': 'formar líderes',
            'substituir_organizar_empresa_por': 'construir império'
        }
    
    def _determine_dominant_archetype(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> str:
        """Determina arquétipo dominante"""
        
        dores = avatar_data.get('dores_viscerais', [])
        segmento = context_data.get('segmento', '').lower()
        
        # Análise baseada nas dores e segmento
        if any('técnico' in dor.lower() or 'operacional' in dor.lower() for dor in dores):
            return 'Técnico Aprisionado'
        elif any('estagnado' in dor.lower() or 'mesmo nível' in dor.lower() for dor in dores):
            return 'Escalador Frustrado'
        elif any('equipe' in dor.lower() or 'liderança' in dor.lower() for dor in dores):
            return 'Visionário Sufocado'
        else:
            # Default baseado no segmento
            if 'tecnologia' in segmento or 'consultoria' in segmento:
                return 'Técnico Aprisionado'
            else:
                return 'Escalador Frustrado'
    
    def _find_related_pain(self, pain_masi: str, avatar_pains: List[str]) -> Optional[str]:
        """Encontra dor do avatar relacionada à dor MASI"""
        
        pain_keywords = {
            'Desenvolvimento de Liderança': ['liderança', 'gestão', 'equipe', 'pessoas'],
            'Cultura Organizacional': ['cultura', 'valores', 'ambiente', 'clima'],
            'Operação e Processos': ['processo', 'operação', 'sistema', 'procedimento'],
            'Proposta de Valor': ['valor', 'diferencial', 'posicionamento', 'proposta'],
            'Indicadores e Dados': ['dados', 'métricas', 'indicadores', 'kpi']
        }
        
        for keyword_group in pain_keywords.values():
            for keyword in keyword_group:
                if keyword in pain_masi.lower():
                    # Busca dor relacionada no avatar
                    for avatar_pain in avatar_pains:
                        if any(kw in avatar_pain.lower() for kw in keyword_group):
                            return avatar_pain
        
        return None
    
    def _map_pain_intensity(self, dores: List[str]) -> Dict[str, List[str]]:
        """Mapeia intensidade das dores"""
        
        alta_intensidade = []
        media_intensidade = []
        baixa_intensidade = []
        
        for dor in dores:
            if any(word in dor.lower() for word in ['excessivamente', 'sempre', 'nunca', 'constantemente']):
                alta_intensidade.append(dor)
            elif any(word in dor.lower() for word in ['frequentemente', 'muitas vezes', 'geralmente']):
                media_intensidade.append(dor)
            else:
                baixa_intensidade.append(dor)
        
        return {
            'alta_intensidade': alta_intensidade,
            'media_intensidade': media_intensidade,
            'baixa_intensidade': baixa_intensidade
        }
    
    def _identify_behavioral_patterns(self, avatar_data: Dict[str, Any]) -> List[str]:
        """Identifica padrões comportamentais"""
        
        patterns = []
        
        # Análise baseada nas objeções
        objecoes = avatar_data.get('objecoes_reais', [])
        
        if any('já tentei' in obj.lower() for obj in objecoes):
            patterns.append('Padrão de múltiplas tentativas frustradas')
        
        if any('tempo' in obj.lower() for obj in objecoes):
            patterns.append('Padrão de sobrecarga operacional')
        
        if any('específico' in obj.lower() for obj in objecoes):
            patterns.append('Padrão de resistência a soluções padronizadas')
        
        # Análise baseada nos medos
        medos = avatar_data.get('medos_paralisantes', [])
        
        if medos:
            patterns.append('Padrão de paralisia por análise excessiva')
            patterns.append('Padrão de medo de mudança estrutural')
        
        return patterns
    
    def _extract_behavioral_discoveries(self, avatar_data: Dict[str, Any]) -> List[str]:
        """Extrai descobertas comportamentais"""
        
        return [
            'Empresários valorizam honestidade brutal sobre diplomacia',
            'Preferem casos reais a teorias motivacionais',
            'Precisam de quick wins para manter engajamento',
            'Resistem a soluções que parecem "receita de bolo"',
            'Valorizam metodologias que podem personalizar'
        ]
    
    def _identify_hidden_opportunities(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> List[str]:
        """Identifica oportunidades ocultas"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return [
            f'Mercado de {segmento} carente de soluções práticas',
            'Demanda reprimida por mentoria especializada',
            'Oportunidade em metodologias proprietárias',
            'Nicho de empresários frustrados com consultorias genéricas',
            'Potencial em comunidades de alta performance'
        ]
    
    def _create_fallback_dashboard(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria dashboard de fallback"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return {
            'titulo': 'DASHBOARD ARQUEOLÓGICO DO AVATAR - MODO BÁSICO',
            'visao_geral': {
                'publico_analisado': f'Avatar básico para {segmento}',
                'principais_desafios': ['Gestão de pessoas', 'Processos', 'Crescimento']
            },
            'analise_dores': {
                'dores_principais': [
                    f'Dificuldades operacionais em {segmento}',
                    'Falta de sistemas estruturados',
                    'Dependência excessiva do fundador'
                ]
            },
            'fallback_mode': True,
            'recomendacao': 'Configure sistema completo para dashboard detalhado'
        }

# Instância global
avatar_dashboard_generator = AvatarDashboardGenerator()