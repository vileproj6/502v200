#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Pre-Pitch Architect
Versão corrigida e aprimorada do arquiteto de pré-pitch
"""

import time
import logging
import json
from typing import Dict, List, Any, Optional
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class EnhancedPrePitchArchitect:
    """Arquiteto de Pré-Pitch Aprimorado com correções robustas"""
    
    def __init__(self):
        """Inicializa o arquiteto aprimorado"""
        # Prompt especializado para busca e síntese
        self.search_specialist_prompt = """
        You are a search specialist expert at finding and synthesizing information from the web.
        
        Focus Areas:
        - Advanced search query formulation
        - Domain-specific searching and filtering
        - Result quality evaluation and ranking
        - Information synthesis across sources
        - Fact verification and cross-referencing
        - Historical and trend analysis
        
        Query Optimization:
        - Use specific phrases in quotes for exact matches
        - Exclude irrelevant terms with negative keywords
        - Target specific timeframes for recent/historical data
        - Formulate multiple query variations
        
        Domain Filtering:
        - allowed_domains for trusted sources
        - blocked_domains to exclude unreliable sites
        - Target specific sites for authoritative content
        - Academic sources for research topics
        
        Approach:
        1. Understand the research objective clearly
        2. Create 3-5 query variations for coverage
        3. Search broadly first, then refine
        4. Verify key facts across multiple sources
        5. Track contradictions and consensus
        6. Focus on actionable insights
        7. Always provide direct quotes for important claims
        """
        
        self.psychological_phases = self._load_enhanced_phases()
        self.transition_templates = self._load_enhanced_transitions()
        self.validation_rules = self._load_validation_rules()
        self.orquestracao_completa = self._load_orquestracao_completa_anexos()
        
        logger.info("Enhanced Pre-Pitch Architect inicializado")
    
    def _load_orquestracao_completa_anexos(self) -> Dict[str, Dict[str, Any]]:
        """Carrega orquestração completa dos anexos"""
        return {
            'sequencia_psicologica_anexos': [
                {
                    'fase': 'quebra',
                    'objetivo': 'Destruir a ilusão confortável',
                    'duracao': '3-5 minutos',
                    'intensidade': 'Alta',
                    'drivers_ideais': ['Diagnóstico Brutal', 'Ferida Exposta'],
                    'resultado_esperado': 'Desconforto produtivo',
                    'tecnicas': ['Confronto direto', 'Pergunta desconfortável', 'Estatística chocante']
                },
                {
                    'fase': 'exposicao',
                    'objetivo': 'Revelar a ferida real',
                    'duracao': '4-6 minutos',
                    'intensidade': 'Crescente',
                    'drivers_ideais': ['Custo Invisível', 'Ambiente Vampiro'],
                    'resultado_esperado': 'Consciência da dor',
                    'tecnicas': ['Cálculo de perdas', 'Visualização da dor', 'Comparação cruel']
                },
                {
                    'fase': 'indignacao',
                    'objetivo': 'Criar revolta produtiva',
                    'duracao': '3-4 minutos',
                    'intensidade': 'Máxima',
                    'drivers_ideais': ['Relógio Psicológico', 'Inveja Produtiva'],
                    'resultado_esperado': 'Urgência de mudança',
                    'tecnicas': ['Urgência temporal', 'Comparação social', 'Consequências futuras']
                },
                {
                    'fase': 'vislumbre',
                    'objetivo': 'Mostrar o possível',
                    'duracao': '5-7 minutos',
                    'intensidade': 'Esperançosa',
                    'drivers_ideais': ['Ambição Expandida', 'Troféu Secreto'],
                    'resultado_esperado': 'Desejo amplificado',
                    'tecnicas': ['Visualização do sucesso', 'Casos de transformação', 'Possibilidades expandidas']
                },
                {
                    'fase': 'tensao',
                    'objetivo': 'Amplificar o gap',
                    'duracao': '2-3 minutos',
                    'intensidade': 'Crescente',
                    'drivers_ideais': ['Identidade Aprisionada', 'Oportunidade Oculta'],
                    'resultado_esperado': 'Tensão máxima',
                    'tecnicas': ['Gap atual vs ideal', 'Identidade limitante', 'Oportunidade única']
                },
                {
                    'fase': 'necessidade',
                    'objetivo': 'Tornar a mudança inevitável',
                    'duracao': '3-4 minutos',
                    'intensidade': 'Definitiva',
                    'drivers_ideais': ['Método vs Sorte', 'Mentor Salvador'],
                    'resultado_esperado': 'Necessidade de solução',
                    'tecnicas': ['Caminho claro', 'Mentor necessário', 'Método vs caos']
                }
            ],
            'transicoes_anexos': {
                'quebra_para_exposicao': "Eu sei que isso dói ouvir... Mas sabe o que dói mais?",
                'exposicao_para_indignacao': "E o pior de tudo é que isso não precisa ser assim...",
                'indignacao_para_vislumbre': "Mas calma, não vim aqui só para abrir feridas...",
                'vislumbre_para_tensao': "Agora você vê a diferença entre onde está e onde poderia estar...",
                'tensao_para_necessidade': "A pergunta não é SE você vai mudar, é COMO...",
                'necessidade_para_logica': "Eu sei que você está sentindo isso agora... Mas seu cérebro racional está gritando: 'Será que funciona mesmo?' Então deixa eu te mostrar os números..."
            }
        }
    
    def _load_enhanced_phases(self) -> Dict[str, Dict[str, Any]]:
        """Carrega fases psicológicas aprimoradas"""
        return {
            'despertar': {
                'objetivo': 'Quebrar padrão mental e despertar consciência',
                'duracao': '2-4 minutos',
                'intensidade': 'Crescente',
                'tecnicas': ['Pergunta disruptiva', 'Estatística chocante', 'Realidade brutal'],
                'resultado_esperado': 'Atenção total e desconforto produtivo'
            },
            'amplificacao': {
                'objetivo': 'Amplificar dor e urgência',
                'duracao': '3-5 minutos',
                'intensidade': 'Alta',
                'tecnicas': ['Cálculo de perdas', 'Comparação social', 'Consequências futuras'],
                'resultado_esperado': 'Dor emocional e urgência de mudança'
            },
            'vislumbre': {
                'objetivo': 'Mostrar possibilidade de transformação',
                'duracao': '4-6 minutos',
                'intensidade': 'Esperançosa',
                'tecnicas': ['Casos de sucesso', 'Visualização do futuro', 'Prova de possibilidade'],
                'resultado_esperado': 'Esperança e desejo amplificado'
            },
            'tensao': {
                'objetivo': 'Criar tensão entre atual e possível',
                'duracao': '2-3 minutos',
                'intensidade': 'Máxima',
                'tecnicas': ['Gap emocional', 'Identidade limitante', 'Escolha binária'],
                'resultado_esperado': 'Tensão máxima e necessidade de resolução'
            },
            'preparacao': {
                'objetivo': 'Preparar para receber solução',
                'duracao': '1-2 minutos',
                'intensidade': 'Expectante',
                'tecnicas': ['Abertura mental', 'Receptividade', 'Antecipação'],
                'resultado_esperado': 'Estado mental ideal para oferta'
            }
        }
    
    def _load_enhanced_transitions(self) -> Dict[str, str]:
        """Carrega transições aprimoradas"""
        return {
            'despertar_para_amplificacao': "Agora que você viu isso... deixa eu te mostrar o que isso realmente significa...",
            'amplificacao_para_vislumbre': "Mas calma, não vim aqui só para abrir feridas. Vim te mostrar que existe uma saída...",
            'vislumbre_para_tensao': "Agora você vê a diferença entre onde está e onde poderia estar. E isso dói, não é?",
            'tensao_para_preparacao': "A pergunta não é SE você vai mudar. A pergunta é COMO e QUANDO...",
            'preparacao_para_oferta': "E é exatamente isso que eu vou te mostrar agora..."
        }
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Carrega regras de validação"""
        return {
            'min_phases': 3,
            'min_total_duration': 10,  # minutos
            'max_total_duration': 25,  # minutos
            'required_elements': ['objetivo', 'tecnicas', 'resultado_esperado'],
            'min_script_length': 100,
            'max_script_length': 2000
        }
    
    def generate_enhanced_pre_pitch_system(
        self, 
        drivers_data: Dict[str, Any], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera sistema de pré-pitch aprimorado com validação robusta"""
        
        # Validação de entrada mais robusta
        validation_result = self._validate_input_data(drivers_data, avatar_data, context_data)
        if not validation_result['valid']:
            logger.error(f"❌ Dados de entrada inválidos: {validation_result['errors']}")
            return self._generate_emergency_pre_pitch(context_data, validation_result['errors'])
        
        try:
            logger.info("🎯 Gerando pré-pitch aprimorado...")
            
            # Salva dados de entrada
            salvar_etapa("pre_pitch_entrada_enhanced", {
                "drivers_data": drivers_data,
                "avatar_data": avatar_data,
                "context_data": context_data,
                "validation": validation_result
            }, categoria="pre_pitch")
            
            # Extrai drivers utilizáveis
            usable_drivers = self._extract_usable_drivers(drivers_data)
            
            if not usable_drivers:
                logger.warning("⚠️ Nenhum driver utilizável encontrado")
                usable_drivers = self._create_basic_drivers(context_data)
            
            # Cria orquestração emocional robusta
            emotional_orchestration = self._create_robust_emotional_orchestration(
                usable_drivers, avatar_data, context_data
            )
            
            # Valida orquestração
            if not self._validate_orchestration(emotional_orchestration):
                logger.error("❌ Orquestração emocional inválida")
                emotional_orchestration = self._create_fallback_orchestration(context_data)
            
            # Salva orquestração
            salvar_etapa("orquestracao_enhanced", emotional_orchestration, categoria="pre_pitch")
            
            # Gera roteiros específicos
            scripts = self._generate_enhanced_scripts(emotional_orchestration, avatar_data, context_data)
            
            # Valida roteiros
            if not self._validate_scripts(scripts):
                logger.error("❌ Roteiros inválidos")
                scripts = self._create_fallback_scripts(context_data)
            
            # Salva roteiros
            salvar_etapa("scripts_enhanced", scripts, categoria="pre_pitch")
            
            # Cria sistema completo
            complete_system = {
                'orquestracao_emocional': emotional_orchestration,
                'roteiros_detalhados': scripts,
                'drivers_utilizados': [d['nome'] for d in usable_drivers],
                'fases_implementadas': list(emotional_orchestration.get('sequencia_fases', {}).keys()),
                'duracao_total_estimada': self._calculate_total_duration(emotional_orchestration),
                'nivel_intensidade': self._calculate_intensity_level(emotional_orchestration),
                'metricas_eficacia': self._create_effectiveness_metrics(),
                'validacao_status': 'ENHANCED_VALID',
                'generation_timestamp': time.time(),
                'version': '2.0_enhanced'
            }
            
            # Validação final
            final_validation = self._validate_complete_system(complete_system)
            complete_system['final_validation'] = final_validation
            
            if not final_validation['valid']:
                logger.error(f"❌ Sistema final inválido: {final_validation['errors']}")
                return self._generate_emergency_pre_pitch(context_data, final_validation['errors'])
            
            # Salva sistema completo
            salvar_etapa("pre_pitch_completo_enhanced", complete_system, categoria="pre_pitch")
            
            logger.info("✅ Pré-pitch aprimorado gerado com sucesso")
            return complete_system
            
        except Exception as e:
            logger.error(f"❌ Erro crítico no pré-pitch aprimorado: {str(e)}")
            salvar_erro("pre_pitch_enhanced_erro", e, contexto=context_data)
            # NÃO RETORNA FALLBACK - FALHA EXPLICITAMENTE
            raise Exception(f"PRÉ-PITCH APRIMORADO FALHOU: {str(e)}")
    
    def _create_robust_emotional_orchestration_from_annexes(
        self, 
        drivers: List[Dict[str, Any]], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria orquestração emocional robusta usando sequência dos anexos"""
        
        try:
            # Usa sequência psicológica dos anexos como base
            base_sequence = self.orquestracao_completa['sequencia_psicologica_anexos']
            
            # Mapeia drivers para fases dos anexos
            phase_mapping = self._map_drivers_to_annexes_phases(drivers)
            
            # Cria sequência baseada nos anexos
            sequence = {}
            
            for phase_data in base_sequence:
                phase_name = phase_data['fase']
                assigned_drivers = phase_mapping.get(phase_name, [])
                
                sequence[phase_name] = {
                    'configuracao': phase_data,
                    'drivers_atribuidos': assigned_drivers,
                    'tecnicas_especificas': phase_data['tecnicas'],
                    'transicao_proxima': self._get_transition_from_annexes(phase_name),
                    'indicadores_sucesso': self._get_phase_success_indicators_annexes(phase_name),
                    'intensidade_anexos': phase_data['intensidade'],
                    'resultado_esperado_anexos': phase_data['resultado_esperado']
                }
            
            orchestration = {
                'sequencia_fases': sequence,
                'fluxo_emocional': self._create_emotional_flow_annexes(sequence),
                'pontos_criticos': self._identify_critical_points_annexes(sequence),
                'mecanismos_recuperacao': self._create_recovery_mechanisms_annexes(sequence),
                'adaptacoes_contexto': self._create_context_adaptations_annexes(sequence, context_data),
                'escalada_emocional_anexos': 'Crescente até o clímax da oferta conforme anexos'
            }
            
            return orchestration
            
        except Exception as e:
            logger.error(f"❌ Erro na orquestração robusta dos anexos: {e}")
            return self._create_fallback_orchestration(context_data)
    
    def _map_drivers_to_annexes_phases(self, drivers: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Mapeia drivers para fases dos anexos"""
        
        mapping = {}
        
        for driver in drivers:
            driver_name = driver.get('nome', '').lower()
            
            # Mapeamento baseado nos anexos
            if any(keyword in driver_name for keyword in ['diagnóstico', 'brutal', 'ferida', 'realidade']):
                mapping.setdefault('quebra', []).append(driver)
            elif any(keyword in driver_name for keyword in ['custo', 'invisível', 'ambiente', 'vampiro']):
                mapping.setdefault('exposicao', []).append(driver)
            elif any(keyword in driver_name for keyword in ['relógio', 'urgência', 'inveja', 'tempo']):
                mapping.setdefault('indignacao', []).append(driver)
            elif any(keyword in driver_name for keyword in ['ambição', 'expandida', 'troféu', 'secreto']):
                mapping.setdefault('vislumbre', []).append(driver)
            elif any(keyword in driver_name for keyword in ['identidade', 'aprisionada', 'oportunidade']):
                mapping.setdefault('tensao', []).append(driver)
            elif any(keyword in driver_name for keyword in ['método', 'sorte', 'mentor', 'salvador']):
                mapping.setdefault('necessidade', []).append(driver)
            else:
                # Distribui drivers não categorizados baseado na intensidade
                mapping.setdefault('quebra', []).append(driver)
        
        return mapping
    
    def _get_transition_from_annexes(self, current_phase: str) -> str:
        """Obtém transição dos anexos"""
        
        transitions = self.orquestracao_completa['transicoes_anexos']
        
        if current_phase == 'quebra':
            return transitions.get('quebra_para_exposicao', 'Transição para exposição')
        elif current_phase == 'exposicao':
            return transitions.get('exposicao_para_indignacao', 'Transição para indignação')
        elif current_phase == 'indignacao':
            return transitions.get('indignacao_para_vislumbre', 'Transição para vislumbre')
        elif current_phase == 'vislumbre':
            return transitions.get('vislumbre_para_tensao', 'Transição para tensão')
        elif current_phase == 'tensao':
            return transitions.get('tensao_para_necessidade', 'Transição para necessidade')
        elif current_phase == 'necessidade':
            return transitions.get('necessidade_para_logica', 'Transição para lógica')
        else:
            return 'Transição padrão'
    
    def _generate_enhanced_scripts_with_specialist(
        self, 
        orchestration: Dict[str, Any], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera roteiros aprimorados usando prompt especialista em busca"""
        
        try:
            segmento = context_data.get('segmento', 'negócios')
            
            # Extrai informações do avatar
            dores = avatar_data.get('dores_viscerais', [])[:5]
            desejos = avatar_data.get('desejos_secretos', [])[:5]
            linguagem = avatar_data.get('linguagem_interna', {})
            
            prompt = f"""
            {self.search_specialist_prompt}
            
            Como especialista em busca e síntese de informações, crie roteiros detalhados de pré-pitch para o segmento {segmento}.
            
            Use a sequência psicológica dos anexos:
            1. QUEBRA - Destruir ilusão confortável
            2. EXPOSIÇÃO - Revelar ferida real  
            3. INDIGNAÇÃO - Criar revolta produtiva
            4. VISLUMBRE - Mostrar o possível
            5. TENSÃO - Amplificar o gap
            6. NECESSIDADE - Tornar mudança inevitável

            ORQUESTRAÇÃO EMOCIONAL:
            {json.dumps(orchestration, indent=2, ensure_ascii=False)[:3000]}

            AVATAR - DORES PRINCIPAIS:
            {json.dumps(dores, ensure_ascii=False)}

            AVATAR - DESEJOS PRINCIPAIS:
            {json.dumps(desejos, ensure_ascii=False)}

            LINGUAGEM INTERNA:
            {json.dumps(linguagem, ensure_ascii=False)}

            INSTRUÇÕES:
            1. Crie roteiros específicos para cada fase dos anexos
            2. Use linguagem que ressoe com o avatar
            3. Inclua elementos emocionais específicos
            4. Seja específico para o segmento {segmento}
            5. NUNCA use placeholders genéricos
            6. Focus on actionable insights
            7. Always provide direct quotes for important claims

            RETORNE APENAS JSON VÁLIDO:

            ```json
            {{
              "fase_quebra": {{
                "duracao": "3-5 minutos",
                "objetivo": "Destruir a ilusão confortável",
                "roteiro_principal": "Roteiro detalhado específico para {segmento}",
                "elementos_chave": ["Elemento 1", "Elemento 2", "Elemento 3"],
                "frases_impacto": ["Frase 1", "Frase 2", "Frase 3"],
                "transicao": "Frase de transição específica dos anexos"
              }},
              "fase_exposicao": {{
                "duracao": "4-6 minutos",
                "objetivo": "Revelar a ferida real",
                "roteiro_principal": "Roteiro detalhado específico para {segmento}",
                "calculos_perda": ["Cálculo 1", "Cálculo 2"],
                "comparacoes_crueis": ["Comparação 1", "Comparação 2"],
                "transicao": "Frase de transição específica dos anexos"
              }},
              "fase_indignacao": {{
                "duracao": "3-4 minutos",
                "objetivo": "Criar revolta produtiva",
                "roteiro_principal": "Roteiro detalhado específico para {segmento}",
                "urgencia_temporal": ["Urgência 1", "Urgência 2"],
                "comparacao_social": ["Comparação 1", "Comparação 2"],
                "transicao": "Frase de transição específica dos anexos"
              }},
              "fase_vislumbre": {{
                "duracao": "5-7 minutos",
                "objetivo": "Mostrar o possível",
                "roteiro_principal": "Roteiro detalhado específico para {segmento}",
                "casos_transformacao": ["Caso 1", "Caso 2"],
                "visualizacoes": ["Visualização 1", "Visualização 2"],
                "transicao": "Frase de transição específica dos anexos"
              }},
              "fase_tensao": {{
                "duracao": "2-3 minutos",
                "objetivo": "Amplificar o gap",
                "roteiro_principal": "Roteiro detalhado específico para {segmento}",
                "gap_emocional": "Descrição do gap específico",
                "identidade_limitante": "Identidade que precisa ser quebrada",
                "transicao": "Frase de transição específica dos anexos"
              }},
              "fase_necessidade": {{
                "duracao": "3-4 minutos",
                "objetivo": "Tornar mudança inevitável",
                "roteiro_principal": "Roteiro detalhado específico para {segmento}",
                "caminho_claro": "Como o método resolve tudo",
                "mentor_necessario": "Por que precisam de orientação",
                "ponte_oferta": "Frase de ponte para oferta dos anexos"
              }}
            }}
            ```
            """
            
            response = ai_manager.generate_analysis(prompt, max_tokens=4000)
            
            if response:
                clean_response = response.strip()
                if "```json" in clean_response:
                    start = clean_response.find("```json") + 7
                    end = clean_response.rfind("```")
                    clean_response = clean_response[start:end].strip()
                
                try:
                    scripts = json.loads(clean_response)
                    
                    # Valida estrutura dos scripts
                    if self._validate_scripts_structure_annexes(scripts):
                        logger.info("✅ Roteiros aprimorados gerados com especialista em busca")
                        return scripts
                    else:
                        logger.warning("⚠️ Estrutura de scripts inválida")
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ JSON inválido da IA: {e}")
            
            # Fallback para scripts básicos
            return self._create_fallback_scripts_annexes(context_data)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar scripts aprimorados: {e}")
            return self._create_fallback_scripts_annexes(context_data)
    
    def _validate_scripts_structure_annexes(self, scripts: Dict[str, Any]) -> bool:
        """Valida estrutura dos scripts baseada nos anexos"""
        
        required_phases = ['fase_quebra', 'fase_exposicao', 'fase_vislumbre', 'fase_necessidade']
        
        for phase in required_phases:
            if phase not in scripts:
                logger.error(f"❌ Fase obrigatória dos anexos ausente: {phase}")
                return False
            
            phase_data = scripts[phase]
            if not isinstance(phase_data, dict):
                logger.error(f"❌ Dados da fase {phase} não são um dicionário")
                return False
            
            if not phase_data.get('roteiro_principal'):
                logger.error(f"❌ Roteiro principal ausente na fase {phase}")
                return False
            
            if len(phase_data['roteiro_principal']) < 100:
                logger.error(f"❌ Roteiro muito curto na fase {phase}")
                return False
        
        return True
    
    def _create_fallback_scripts_annexes(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria scripts de fallback baseados nos anexos"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return {
            'fase_quebra': {
                'duracao': '3-5 minutos',
                'objetivo': 'Destruir a ilusão confortável',
                'roteiro_principal': f"Deixa eu te fazer uma pergunta difícil sobre {segmento}... Há quanto tempo você está no mesmo nível? A maioria dos profissionais trabalha muito mas não sai do lugar. E sabe por quê? Porque estão fazendo as mesmas coisas que todo mundo faz. Isso dói ouvir, mas é a verdade que ninguém te conta sobre {segmento}.",
                'elementos_chave': ['Pergunta disruptiva', 'Realidade brutal', 'Padrão quebrado'],
                'frases_impacto': [
                    f"A verdade sobre {segmento} que ninguém te conta",
                    "Isso vai doer, mas precisa ser dito",
                    "Você está fazendo tudo errado"
                ],
                'transicao': "Eu sei que isso dói ouvir... Mas sabe o que dói mais?"
            },
            'fase_exposicao': {
                'duracao': '4-6 minutos',
                'objetivo': 'Revelar a ferida real',
                'roteiro_principal': f"Cada dia que passa sem otimizar {segmento} é dinheiro saindo do seu bolso. Enquanto você está 'pensando', seus concorrentes estão agindo. Cada mês de atraso custa oportunidades que não voltam mais. E o pior de tudo é que isso não precisa ser assim...",
                'calculos_perda': [
                    f"Cada mês sem sistema em {segmento} = R$ 10.000 perdidos",
                    f"Concorrentes ganham 20% de market share por ano"
                ],
                'comparacoes_crueis': [
                    f"Outros profissionais de {segmento} já estão na frente",
                    "Quem não age agora fica para trás permanentemente"
                ],
                'transicao': "E o pior de tudo é que isso não precisa ser assim..."
            },
            'fase_vislumbre': {
                'duracao': '5-7 minutos',
                'objetivo': 'Mostrar o possível',
                'roteiro_principal': f"Mas calma, não vim aqui só para abrir feridas. Imagine se você pudesse dominar {segmento} de forma que seus concorrentes nem conseguissem acompanhar. Imagine ter um sistema que funciona enquanto você dorme. Isso não é fantasia, é realidade para quem sabe como fazer.",
                'casos_transformacao': [
                    f"Cliente em {segmento} triplicou receita em 6 meses",
                    f"Profissional saiu de R$ 5K para R$ 50K mensais"
                ],
                'visualizacoes': [
                    f"Você como autoridade reconhecida em {segmento}",
                    "Liberdade financeira e de tempo total"
                ],
                'transicao': "Agora você vê a diferença entre onde está e onde poderia estar..."
            },
            'fase_necessidade': {
                'duracao': '3-4 minutos',
                'objetivo': 'Tornar mudança inevitável',
                'roteiro_principal': f"A pergunta não é SE você vai mudar em {segmento}. A pergunta é COMO e QUANDO. Eu vou te mostrar exatamente como sair dessa situação. Como transformar tudo isso que você viu em realidade. Mas antes, preciso saber se você está realmente pronto para isso.",
                'caminho_claro': f"Método específico para dominar {segmento}",
                'mentor_necessario': "Orientação especializada para acelerar resultados",
                'ponte_oferta': "Agora que você está pronto, deixa eu te mostrar como..."
            },
            'fallback_mode': True,
            'baseado_anexos': True
        }
    
    def _validate_input_data(self, drivers_data: Dict[str, Any], avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validação robusta dos dados de entrada"""
        
        errors = []
        warnings = []
        
        # Valida context_data
        if not context_data or not context_data.get('segmento'):
            errors.append("Segmento obrigatório ausente")
        
        # Valida avatar_data
        if not avatar_data:
            warnings.append("Dados do avatar ausentes - será criado avatar básico")
        else:
            if not avatar_data.get('dores_viscerais'):
                warnings.append("Dores viscerais ausentes no avatar")
            if not avatar_data.get('desejos_secretos'):
                warnings.append("Desejos secretos ausentes no avatar")
        
        # Valida drivers_data
        if not drivers_data:
            warnings.append("Dados de drivers ausentes - será criado sistema básico")
        else:
            if isinstance(drivers_data, dict):
                drivers_list = drivers_data.get('drivers_customizados', [])
                if not drivers_list or len(drivers_list) < 2:
                    warnings.append("Poucos drivers disponíveis")
            elif isinstance(drivers_data, list):
                if len(drivers_data) < 2:
                    warnings.append("Poucos drivers na lista")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'can_proceed': len(errors) == 0
        }
    
    def _extract_usable_drivers(self, drivers_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai drivers utilizáveis dos dados"""
        
        usable_drivers = []
        
        try:
            if isinstance(drivers_data, dict):
                # Formato padrão com drivers_customizados
                if 'drivers_customizados' in drivers_data:
                    drivers_list = drivers_data['drivers_customizados']
                    if isinstance(drivers_list, list):
                        usable_drivers = drivers_list
                
                # Formato alternativo direto
                elif 'nome' in drivers_data:
                    usable_drivers = [drivers_data]
                
                # Busca em outras chaves possíveis
                else:
                    for key, value in drivers_data.items():
                        if isinstance(value, list) and value:
                            if all(isinstance(item, dict) and 'nome' in item for item in value):
                                usable_drivers = value
                                break
            
            elif isinstance(drivers_data, list):
                usable_drivers = drivers_data
            
            # Filtra drivers válidos
            valid_drivers = []
            for driver in usable_drivers:
                if isinstance(driver, dict) and driver.get('nome'):
                    valid_drivers.append(driver)
            
            logger.info(f"📊 Drivers extraídos: {len(valid_drivers)} válidos de {len(usable_drivers)} totais")
            return valid_drivers
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair drivers: {e}")
            return []
    
    def _create_basic_drivers(self, context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Cria drivers básicos quando não há dados suficientes"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return [
            {
                'nome': 'Diagnóstico de Realidade',
                'gatilho_central': f'Situação atual em {segmento}',
                'objetivo': 'Despertar consciência da situação real',
                'intensidade': 'Alta'
            },
            {
                'nome': 'Custo da Inação',
                'gatilho_central': f'Preço de não agir em {segmento}',
                'objetivo': 'Amplificar urgência através do custo',
                'intensidade': 'Máxima'
            },
            {
                'nome': 'Visão do Possível',
                'gatilho_central': f'Potencial real em {segmento}',
                'objetivo': 'Mostrar possibilidades de transformação',
                'intensidade': 'Esperançosa'
            },
            {
                'nome': 'Momento de Decisão',
                'gatilho_central': 'Escolha entre status quo e mudança',
                'objetivo': 'Criar necessidade de decisão',
                'intensidade': 'Definitiva'
            }
        ]
    
    def _create_robust_emotional_orchestration(
        self, 
        drivers: List[Dict[str, Any]], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria orquestração emocional robusta"""
        
        try:
            # Mapeia drivers para fases
            phase_mapping = self._map_drivers_to_phases_enhanced(drivers)
            
            # Cria sequência de fases
            sequence = {}
            
            for phase_name, phase_config in self.psychological_phases.items():
                assigned_drivers = phase_mapping.get(phase_name, [])
                
                if assigned_drivers or phase_name in ['despertar', 'preparacao']:  # Fases essenciais sempre incluídas
                    sequence[phase_name] = {
                        'configuracao': phase_config,
                        'drivers_atribuidos': assigned_drivers,
                        'tecnicas_especificas': self._get_phase_specific_techniques(phase_name, assigned_drivers, context_data),
                        'transicao_proxima': self._get_transition_to_next_phase(phase_name),
                        'indicadores_sucesso': self._get_phase_success_indicators(phase_name)
                    }
            
            # Valida sequência mínima
            if len(sequence) < self.validation_rules['min_phases']:
                logger.warning(f"⚠️ Sequência muito curta: {len(sequence)} fases")
                sequence = self._ensure_minimum_sequence(sequence, context_data)
            
            orchestration = {
                'sequencia_fases': sequence,
                'fluxo_emocional': self._create_emotional_flow(sequence),
                'pontos_criticos': self._identify_critical_points(sequence),
                'mecanismos_recuperacao': self._create_recovery_mechanisms(sequence),
                'adaptacoes_contexto': self._create_context_adaptations(sequence, context_data)
            }
            
            return orchestration
            
        except Exception as e:
            logger.error(f"❌ Erro na orquestração robusta: {e}")
            return self._create_fallback_orchestration(context_data)
    
    def _map_drivers_to_phases_enhanced(self, drivers: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Mapeia drivers para fases de forma aprimorada"""
        
        mapping = {}
        
        for driver in drivers:
            driver_name = driver.get('nome', '').lower()
            driver_objetivo = driver.get('objetivo', '').lower()
            driver_intensidade = driver.get('intensidade', '').lower()
            
            # Mapeamento baseado em múltiplos critérios
            if any(keyword in driver_name for keyword in ['diagnóstico', 'realidade', 'despertar', 'consciência']):
                mapping.setdefault('despertar', []).append(driver)
            elif any(keyword in driver_name for keyword in ['custo', 'perda', 'urgência', 'tempo']):
                mapping.setdefault('amplificacao', []).append(driver)
            elif any(keyword in driver_name for keyword in ['visão', 'possível', 'futuro', 'transformação']):
                mapping.setdefault('vislumbre', []).append(driver)
            elif any(keyword in driver_name for keyword in ['decisão', 'escolha', 'momento', 'tensão']):
                mapping.setdefault('tensao', []).append(driver)
            elif any(keyword in driver_name for keyword in ['preparação', 'abertura', 'receptividade']):
                mapping.setdefault('preparacao', []).append(driver)
            else:
                # Distribui drivers não categorizados
                if 'alta' in driver_intensidade or 'máxima' in driver_intensidade:
                    mapping.setdefault('amplificacao', []).append(driver)
                elif 'esperançosa' in driver_intensidade:
                    mapping.setdefault('vislumbre', []).append(driver)
                else:
                    mapping.setdefault('despertar', []).append(driver)
        
        return mapping
    
    def _get_phase_specific_techniques(self, phase_name: str, drivers: List[Dict[str, Any]], context_data: Dict[str, Any]) -> List[str]:
        """Obtém técnicas específicas para cada fase"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        base_techniques = self.psychological_phases[phase_name]['tecnicas']
        
        # Personaliza técnicas baseado no segmento
        personalized_techniques = []
        
        for technique in base_techniques:
            if phase_name == 'despertar':
                personalized_techniques.append(f"{technique} específica para {segmento}")
            elif phase_name == 'amplificacao':
                personalized_techniques.append(f"{technique} no contexto de {segmento}")
            elif phase_name == 'vislumbre':
                personalized_techniques.append(f"{technique} de sucesso em {segmento}")
            elif phase_name == 'tensao':
                personalized_techniques.append(f"{technique} entre situação atual e potencial em {segmento}")
            elif phase_name == 'preparacao':
                personalized_techniques.append(f"{technique} para receber solução em {segmento}")
        
        # Adiciona técnicas dos drivers
        for driver in drivers:
            if driver.get('tecnicas'):
                personalized_techniques.extend(driver['tecnicas'])
        
        return personalized_techniques
    
    def _get_transition_to_next_phase(self, current_phase: str) -> str:
        """Obtém transição para próxima fase"""
        
        phase_order = list(self.psychological_phases.keys())
        
        try:
            current_index = phase_order.index(current_phase)
            if current_index < len(phase_order) - 1:
                next_phase = phase_order[current_index + 1]
                transition_key = f"{current_phase}_para_{next_phase}"
                return self.transition_templates.get(transition_key, f"Transição de {current_phase} para {next_phase}")
            else:
                return "Transição para apresentação da solução"
        except ValueError:
            return "Transição padrão"
    
    def _get_phase_success_indicators(self, phase_name: str) -> List[str]:
        """Obtém indicadores de sucesso para cada fase"""
        
        indicators = {
            'despertar': [
                'Silêncio absoluto na audiência',
                'Expressões de surpresa ou choque',
                'Comentários de reconhecimento da situação',
                'Linguagem corporal de atenção total'
            ],
            'amplificacao': [
                'Sinais de desconforto emocional',
                'Comentários sobre urgência',
                'Perguntas sobre consequências',
                'Expressões de preocupação'
            ],
            'vislumbre': [
                'Mudança na linguagem corporal (abertura)',
                'Comentários esperançosos',
                'Perguntas sobre possibilidades',
                'Interesse visível aumentado'
            ],
            'tensao': [
                'Ansiedade visível',
                'Perguntas sobre próximos passos',
                'Comentários sobre necessidade de mudança',
                'Linguagem corporal de urgência'
            ],
            'preparacao': [
                'Atenção total focada',
                'Perguntas sobre solução',
                'Comentários sobre estar pronto',
                'Expectativa visível'
            ]
        }
        
        return indicators.get(phase_name, ['Engajamento geral da audiência'])
    
    def _generate_enhanced_scripts(
        self, 
        orchestration: Dict[str, Any], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera roteiros aprimorados usando IA com validação"""
        
        try:
            segmento = context_data.get('segmento', 'negócios')
            
            # Extrai informações do avatar
            dores = avatar_data.get('dores_viscerais', [])[:5]
            desejos = avatar_data.get('desejos_secretos', [])[:5]
            linguagem = avatar_data.get('linguagem_interna', {})
            
            prompt = f"""
Crie roteiros detalhados de pré-pitch para o segmento {segmento}.

ORQUESTRAÇÃO EMOCIONAL:
{json.dumps(orchestration, indent=2, ensure_ascii=False)[:3000]}

AVATAR - DORES PRINCIPAIS:
{json.dumps(dores, ensure_ascii=False)}

AVATAR - DESEJOS PRINCIPAIS:
{json.dumps(desejos, ensure_ascii=False)}

LINGUAGEM INTERNA:
{json.dumps(linguagem, ensure_ascii=False)}

INSTRUÇÕES:
1. Crie roteiros específicos para cada fase
2. Use linguagem que ressoe com o avatar
3. Inclua elementos emocionais específicos
4. Seja específico para o segmento {segmento}
5. NUNCA use placeholders genéricos

RETORNE APENAS JSON VÁLIDO:

```json
{{
  "fase_despertar": {{
    "duracao": "2-4 minutos",
    "objetivo": "Quebrar padrão e despertar consciência",
    "roteiro_principal": "Roteiro detalhado específico para {segmento}",
    "elementos_chave": ["Elemento 1", "Elemento 2", "Elemento 3"],
    "frases_impacto": ["Frase 1", "Frase 2", "Frase 3"],
    "transicao": "Frase de transição específica"
  }},
  "fase_amplificacao": {{
    "duracao": "3-5 minutos",
    "objetivo": "Amplificar dor e urgência",
    "roteiro_principal": "Roteiro detalhado específico para {segmento}",
    "calculos_perda": ["Cálculo 1", "Cálculo 2"],
    "comparacoes_sociais": ["Comparação 1", "Comparação 2"],
    "transicao": "Frase de transição específica"
  }},
  "fase_vislumbre": {{
    "duracao": "4-6 minutos",
    "objetivo": "Mostrar possibilidade de transformação",
    "roteiro_principal": "Roteiro detalhado específico para {segmento}",
    "casos_sucesso": ["Caso 1", "Caso 2"],
    "visualizacoes": ["Visualização 1", "Visualização 2"],
    "transicao": "Frase de transição específica"
  }},
  "fase_tensao": {{
    "duracao": "2-3 minutos",
    "objetivo": "Criar tensão máxima",
    "roteiro_principal": "Roteiro detalhado específico para {segmento}",
    "gap_emocional": "Descrição do gap específico",
    "escolha_binaria": "Apresentação da escolha",
    "transicao": "Frase de transição específica"
  }},
  "fase_preparacao": {{
    "duracao": "1-2 minutos",
    "objetivo": "Preparar para solução",
    "roteiro_principal": "Roteiro detalhado específico para {segmento}",
    "abertura_mental": "Como abrir a mente",
    "ponte_oferta": "Frase de ponte para oferta",
    "estado_ideal": "Estado mental ideal criado"
  }}
}}
```
"""
            
            response = ai_manager.generate_analysis(prompt, max_tokens=3000)
            
            if response:
                clean_response = response.strip()
                if "```json" in clean_response:
                    start = clean_response.find("```json") + 7
                    end = clean_response.rfind("```")
                    clean_response = clean_response[start:end].strip()
                
                try:
                    scripts = json.loads(clean_response)
                    
                    # Valida estrutura dos scripts
                    if self._validate_scripts_structure(scripts):
                        logger.info("✅ Roteiros aprimorados gerados com IA")
                        return scripts
                    else:
                        logger.warning("⚠️ Estrutura de scripts inválida")
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ JSON inválido da IA: {e}")
            
            # Fallback para scripts básicos
            return self._create_fallback_scripts(context_data)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar scripts aprimorados: {e}")
            return self._create_fallback_scripts(context_data)
    
    def _validate_scripts_structure(self, scripts: Dict[str, Any]) -> bool:
        """Valida estrutura dos scripts gerados"""
        
        required_phases = ['fase_despertar', 'fase_amplificacao', 'fase_vislumbre']
        
        for phase in required_phases:
            if phase not in scripts:
                logger.error(f"❌ Fase obrigatória ausente: {phase}")
                return False
            
            phase_data = scripts[phase]
            if not isinstance(phase_data, dict):
                logger.error(f"❌ Dados da fase {phase} não são um dicionário")
                return False
            
            if not phase_data.get('roteiro_principal'):
                logger.error(f"❌ Roteiro principal ausente na fase {phase}")
                return False
            
            if len(phase_data['roteiro_principal']) < self.validation_rules['min_script_length']:
                logger.error(f"❌ Roteiro muito curto na fase {phase}")
                return False
        
        return True
    
    def _validate_scripts(self, scripts: Dict[str, Any]) -> bool:
        """Valida qualidade dos scripts"""
        
        if not scripts or not isinstance(scripts, dict):
            return False
        
        # Verifica se tem pelo menos 3 fases
        if len(scripts) < 3:
            return False
        
        # Verifica cada script
        for phase_name, phase_data in scripts.items():
            if not isinstance(phase_data, dict):
                return False
            
            roteiro = phase_data.get('roteiro_principal', '')
            if not roteiro or len(roteiro) < 50:
                return False
            
            # Verifica se não é genérico
            if any(placeholder in roteiro.lower() for placeholder in [
                'customizado para', 'específico para', 'baseado em', 'exemplo de'
            ]):
                return False
        
        return True
    
    def _create_fallback_orchestration(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria orquestração de fallback"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return {
            'sequencia_fases': {
                'despertar': {
                    'configuracao': self.psychological_phases['despertar'],
                    'drivers_atribuidos': [{'nome': 'Diagnóstico de Realidade'}],
                    'tecnicas_especificas': [f'Diagnóstico brutal da situação em {segmento}'],
                    'transicao_proxima': 'Agora que você viu a realidade...',
                    'indicadores_sucesso': ['Atenção total', 'Desconforto visível']
                },
                'amplificacao': {
                    'configuracao': self.psychological_phases['amplificacao'],
                    'drivers_atribuidos': [{'nome': 'Custo da Inação'}],
                    'tecnicas_especificas': [f'Cálculo de perdas em {segmento}'],
                    'transicao_proxima': 'Mas existe uma saída...',
                    'indicadores_sucesso': ['Urgência emocional', 'Preocupação visível']
                },
                'vislumbre': {
                    'configuracao': self.psychological_phases['vislumbre'],
                    'drivers_atribuidos': [{'nome': 'Visão do Possível'}],
                    'tecnicas_especificas': [f'Casos de transformação em {segmento}'],
                    'transicao_proxima': 'Agora você tem uma escolha...',
                    'indicadores_sucesso': ['Esperança renovada', 'Interesse aumentado']
                }
            },
            'fluxo_emocional': ['Despertar → Amplificar → Vislumbrar'],
            'pontos_criticos': ['Momento do diagnóstico', 'Cálculo de perdas', 'Apresentação da possibilidade'],
            'fallback_mode': True
        }
    
    def _create_fallback_scripts(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria scripts de fallback"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return {
            'fase_despertar': {
                'duracao': '2-4 minutos',
                'objetivo': 'Quebrar padrão e despertar consciência',
                'roteiro_principal': f"Deixa eu te fazer uma pergunta sobre {segmento}... Há quanto tempo você está no mesmo nível? A maioria dos profissionais trabalha muito mas não sai do lugar. E sabe por quê? Porque estão fazendo as mesmas coisas que todo mundo faz.",
                'elementos_chave': ['Pergunta disruptiva', 'Realidade brutal', 'Padrão quebrado'],
                'frases_impacto': [
                    f"A verdade sobre {segmento} que ninguém te conta",
                    "Isso vai doer, mas precisa ser dito",
                    "Você está fazendo tudo errado"
                ],
                'transicao': "E sabe o que isso está custando para você?"
            },
            'fase_amplificacao': {
                'duracao': '3-5 minutos',
                'objetivo': 'Amplificar dor e urgência',
                'roteiro_principal': f"Cada dia que passa sem otimizar {segmento} é dinheiro saindo do seu bolso. Enquanto você está 'pensando', seus concorrentes estão agindo. Cada mês de atraso custa oportunidades que não voltam mais.",
                'calculos_perda': [
                    f"Cada mês sem sistema = R$ 10.000 perdidos em {segmento}",
                    f"Concorrentes ganham 20% de market share por ano"
                ],
                'comparacoes_sociais': [
                    f"Outros profissionais de {segmento} já estão na frente",
                    "Quem não age agora fica para trás permanentemente"
                ],
                'transicao': "Mas existe um caminho diferente..."
            },
            'fase_vislumbre': {
                'duracao': '4-6 minutos',
                'objetivo': 'Mostrar possibilidade de transformação',
                'roteiro_principal': f"Imagine se você pudesse dominar {segmento} de forma que seus concorrentes nem conseguissem acompanhar. Imagine ter um sistema que funciona enquanto você dorme. Isso não é fantasia, é realidade para quem sabe como fazer.",
                'casos_sucesso': [
                    f"Cliente em {segmento} triplicou receita em 6 meses",
                    f"Profissional saiu de R$ 5K para R$ 50K mensais"
                ],
                'visualizacoes': [
                    f"Você como autoridade reconhecida em {segmento}",
                    "Liberdade financeira e de tempo total"
                ],
                'transicao': "Agora você tem duas escolhas..."
            },
            'fase_tensao': {
                'duracao': '2-3 minutos',
                'objetivo': 'Criar tensão máxima',
                'roteiro_principal': f"Você pode continuar como está, trabalhando muito em {segmento} e vendo outros crescerem mais rápido. Ou pode decidir que chegou a hora de mudar de verdade. Mas não dá para ficar em cima do muro para sempre.",
                'gap_emocional': f"A diferença entre onde você está e onde poderia estar em {segmento}",
                'escolha_binaria': "Continuar igual ou transformar de verdade",
                'transicao': "E é exatamente isso que eu vou te mostrar agora..."
            },
            'fase_preparacao': {
                'duracao': '1-2 minutos',
                'objetivo': 'Preparar para solução',
                'roteiro_principal': f"Eu vou te mostrar exatamente como sair dessa situação em {segmento}. Como transformar tudo isso que você viu em realidade. Mas antes, preciso saber se você está realmente pronto para isso.",
                'abertura_mental': "Preparação psicológica para receber a solução",
                'ponte_oferta': "Agora que você está pronto, deixa eu te mostrar como...",
                'estado_ideal': "Ansioso pela solução, mentalmente aberto, emocionalmente engajado"
            },
            'fallback_mode': True
        }
    
    def _validate_orchestration(self, orchestration: Dict[str, Any]) -> bool:
        """Valida orquestração emocional"""
        
        if not orchestration or not isinstance(orchestration, dict):
            return False
        
        sequencia = orchestration.get('sequencia_fases', {})
        if not sequencia or len(sequencia) < 3:
            return False
        
        # Verifica se cada fase tem configuração válida
        for phase_name, phase_data in sequencia.items():
            if not isinstance(phase_data, dict):
                return False
            
            if not phase_data.get('configuracao'):
                return False
        
        return True
    
    def _validate_complete_system(self, system: Dict[str, Any]) -> Dict[str, Any]:
        """Validação final do sistema completo"""
        
        errors = []
        warnings = []
        
        # Verifica componentes obrigatórios
        required_components = ['orquestracao_emocional', 'roteiros_detalhados']
        
        for component in required_components:
            if component not in system:
                errors.append(f"Componente obrigatório ausente: {component}")
        
        # Verifica orquestração
        orchestration = system.get('orquestracao_emocional', {})
        if not self._validate_orchestration(orchestration):
            errors.append("Orquestração emocional inválida")
        
        # Verifica roteiros
        scripts = system.get('roteiros_detalhados', {})
        if not self._validate_scripts(scripts):
            errors.append("Roteiros detalhados inválidos")
        
        # Verifica duração total
        duracao_total = system.get('duracao_total_estimada', '')
        if not duracao_total or 'minutos' not in duracao_total:
            warnings.append("Duração total não calculada")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'quality_score': 100 - (len(errors) * 25) - (len(warnings) * 5)
        }
    
    def _generate_emergency_pre_pitch(self, context_data: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
        """Gera pré-pitch de emergência quando tudo falha"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        logger.warning(f"🚨 Gerando pré-pitch de emergência para {segmento}")
        
        emergency_system = {
            'orquestracao_emocional': {
                'sequencia_fases': {
                    'despertar_emergencia': {
                        'configuracao': {
                            'objetivo': 'Despertar consciência básica',
                            'duracao': '3-5 minutos',
                            'intensidade': 'Moderada'
                        },
                        'roteiro': f"Vamos falar sobre a realidade do mercado de {segmento}. A maioria dos profissionais está estagnada, trabalhando muito mas não crescendo proporcionalmente."
                    },
                    'amplificacao_emergencia': {
                        'configuracao': {
                            'objetivo': 'Mostrar custo da inação',
                            'duracao': '4-6 minutos',
                            'intensidade': 'Alta'
                        },
                        'roteiro': f"Cada mês sem otimizar {segmento} representa oportunidades perdidas. Enquanto você hesita, outros profissionais estão avançando."
                    },
                    'solucao_emergencia': {
                        'configuracao': {
                            'objetivo': 'Preparar para apresentar solução',
                            'duracao': '2-3 minutos',
                            'intensidade': 'Esperançosa'
                        },
                        'roteiro': f"Mas existe um caminho comprovado para dominar {segmento}. E é isso que vou te mostrar agora."
                    }
                }
            },
            'roteiros_detalhados': self._create_fallback_scripts(context_data),
            'status': 'EMERGENCY_MODE',
            'errors_original': errors,
            'generation_timestamp': time.time(),
            'duracao_total_estimada': '9-14 minutos',
            'nivel_intensidade': 'Moderado a Alto',
            'observacoes': [
                'Sistema em modo de emergência',
                'Funcionalidade limitada mas operacional',
                'Recomenda-se configurar APIs para versão completa'
            ]
        }
        
        # Salva sistema de emergência
        salvar_etapa("pre_pitch_emergencia", emergency_system, categoria="pre_pitch")
        
        return emergency_system
    
    def _ensure_minimum_sequence(self, sequence: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Garante sequência mínima de fases"""
        
        essential_phases = ['despertar', 'amplificacao', 'vislumbre']
        
        for phase in essential_phases:
            if phase not in sequence:
                sequence[phase] = {
                    'configuracao': self.psychological_phases[phase],
                    'drivers_atribuidos': [],
                    'tecnicas_especificas': [f"Técnica básica para {phase}"],
                    'transicao_proxima': f"Transição de {phase}",
                    'indicadores_sucesso': [f"Indicador básico de {phase}"]
                }
        
        return sequence
    
    def _create_emotional_flow(self, sequence: Dict[str, Any]) -> List[str]:
        """Cria fluxo emocional"""
        
        flow = []
        for phase_name in sequence.keys():
            phase_config = sequence[phase_name]['configuracao']
            flow.append(f"{phase_name}: {phase_config['objetivo']}")
        
        return flow
    
    def _identify_critical_points(self, sequence: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica pontos críticos"""
        
        critical_points = []
        
        for phase_name, phase_data in sequence.items():
            intensidade = phase_data['configuracao'].get('intensidade', 'Baixa')
            
            if intensidade in ['Alta', 'Máxima']:
                critical_points.append({
                    'fase': phase_name,
                    'intensidade': intensidade,
                    'risco': 'Perda de audiência se muito intenso',
                    'oportunidade': 'Máximo impacto emocional',
                    'gestao': 'Monitorar reações e ajustar'
                })
        
        return critical_points
    
    def _create_recovery_mechanisms(self, sequence: Dict[str, Any]) -> Dict[str, Any]:
        """Cria mecanismos de recuperação"""
        
        return {
            'sinais_resistencia': [
                'Questionamentos técnicos excessivos',
                'Mudança de assunto',
                'Linguagem corporal fechada',
                'Objeções imediatas'
            ],
            'estrategias_recuperacao': [
                'Reduzir intensidade temporariamente',
                'Usar prova social para validar',
                'Fazer pergunta para reengajar',
                'Contar história pessoal'
            ],
            'pontos_saida': [
                'Se resistência muito alta, pular para vislumbre',
                'Se desengajamento, usar pergunta direta',
                'Se objeções, usar validação social'
            ]
        }
    
    def _create_context_adaptations(self, sequence: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria adaptações por contexto"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return {
            'adaptacoes_segmento': {
                'linguagem': f"Vocabulário específico de {segmento}",
                'exemplos': f"Cases e exemplos de {segmento}",
                'metricas': f"KPIs relevantes para {segmento}",
                'dores': f"Dores específicas de profissionais de {segmento}"
            },
            'adaptacoes_formato': {
                'webinar': 'Usar chat para engajamento',
                'presencial': 'Interação direta com audiência',
                'video': 'Pausas estratégicas para reflexão',
                'audio': 'Ênfase na entonação e ritmo'
            }
        }
    
    def _calculate_total_duration(self, orchestration: Dict[str, Any]) -> str:
        """Calcula duração total"""
        
        sequence = orchestration.get('sequencia_fases', {})
        
        total_min = 0
        total_max = 0
        
        for phase_data in sequence.values():
            duracao = phase_data['configuracao'].get('duracao', '3-4 minutos')
            
            # Extrai números
            import re
            numbers = re.findall(r'\d+', duracao)
            if len(numbers) >= 2:
                total_min += int(numbers[0])
                total_max += int(numbers[1])
            elif len(numbers) == 1:
                num = int(numbers[0])
                total_min += num
                total_max += num + 1
        
        return f"{total_min}-{total_max} minutos"
    
    def _calculate_intensity_level(self, orchestration: Dict[str, Any]) -> str:
        """Calcula nível de intensidade"""
        
        sequence = orchestration.get('sequencia_fases', {})
        
        intensities = []
        for phase_data in sequence.values():
            intensidade = phase_data['configuracao'].get('intensidade', 'Baixa')
            intensities.append(intensidade)
        
        if 'Máxima' in intensities:
            return 'Muito Alto'
        elif 'Alta' in intensities:
            return 'Alto'
        elif 'Crescente' in intensities:
            return 'Progressivo'
        else:
            return 'Moderado'
    
    def _create_effectiveness_metrics(self) -> Dict[str, Any]:
        """Cria métricas de eficácia"""
        
        return {
            'indicadores_durante_apresentacao': [
                'Nível de atenção da audiência',
                'Reações emocionais visíveis',
                'Engajamento no chat/comentários',
                'Linguagem corporal receptiva'
            ],
            'indicadores_pos_apresentacao': [
                'Perguntas sobre próximos passos',
                'Comentários sobre identificação',
                'Solicitações de mais informações',
                'Redução de objeções iniciais'
            ],
            'metricas_conversao': [
                'Taxa de permanência até o final',
                'Engajamento durante apresentação',
                'Perguntas qualificadas geradas',
                'Interesse demonstrado na oferta'
            ]
        }

# Instância global aprimorada
enhanced_pre_pitch_architect = EnhancedPrePitchArchitect()