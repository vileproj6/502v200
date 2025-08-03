#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Anti Objection System
Sistema de Engenharia Psicológica Anti-Objeção baseado nos anexos
"""

import time
import random
import logging
import json
from typing import Dict, List, Any, Optional
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class AntiObjectionSystem:
    """Sistema de Engenharia Psicológica Anti-Objeção"""
    
    def __init__(self):
        """Inicializa o sistema anti-objeção"""
        # Prompt especializado para análise de negócios
        self.business_analyst_prompt = """
        You are a business analyst specializing in actionable insights and growth metrics.
        
        Focus Areas:
        - KPI tracking and reporting
        - Revenue analysis and projections
        - Customer acquisition cost (CAC)
        - Lifetime value (LTV) calculations
        - Churn analysis and cohort retention
        - Market sizing and TAM analysis
        
        Approach:
        1. Focus on metrics that drive decisions
        2. Use visualizations for clarity
        3. Compare against benchmarks
        4. Identify trends and anomalies
        5. Recommend specific actions
        """
        
        self.objecoes_universais = self._load_objecoes_universais()
        self.objecoes_ocultas = self._load_objecoes_ocultas()
        self.tecnicas_neutralizacao = self._load_tecnicas_neutralizacao()
        self.arsenal_emergencia = self._load_arsenal_emergencia()
        
        logger.info("Anti Objection System inicializado com engenharia psicológica dos anexos")
    
    def _load_objecoes_universais(self) -> Dict[str, Dict[str, Any]]:
        """Carrega as 3 objeções universais dos anexos"""
        return {
            'tempo': {
                'objecao': 'Isso não é prioridade para mim',
                'raiz_emocional': 'Medo de comprometimento e mudança',
                'contra_ataque': 'Prioridade é sobre importância, não sobre tempo disponível',
                'drives_mentais': ['Custo Invisível', 'Relógio Psicológico'],
                'historias_consequencia': [
                    'Cliente que adiou por 2 anos e perdeu R$ 500 mil em oportunidades',
                    'Empresário que priorizou urgente sobre importante e faliu'
                ],
                'reformulacao': 'Tempo não é sobre ter, é sobre fazer'
            },
            'dinheiro': {
                'objecao': 'Minha vida não está tão ruim que precise investir',
                'raiz_emocional': 'Negação da realidade e conformismo',
                'contra_ataque': 'Comparação cruel entre gastos supérfluos e investimento em evolução',
                'drives_mentais': ['Diagnóstico Brutal', 'Comparação Cruel'],
                'tecnica_piorar_vida': 'Mostrar como situação atual vai deteriorar sem ação',
                'calculo_oportunidade': 'ROI de não agir vs custo de agir'
            },
            'confianca': {
                'objecao': 'Me dê uma razão para acreditar',
                'raiz_emocional': 'Medo de mais um fracasso ou decepção',
                'contra_ataque': 'Provas sociais qualificadas + garantias agressivas',
                'drives_mentais': ['Prova Social Qualificada', 'Autoridade Técnica'],
                'validacao_preocupacoes': 'Suas preocupações são legítimas e inteligentes',
                'remocao_risco': 'Assumir todo o risco da decisão'
            }
        }
    
    def _load_objecoes_ocultas(self) -> Dict[str, Dict[str, Any]]:
        """Carrega as 5 objeções ocultas críticas dos anexos"""
        return {
            'autossuficiencia': {
                'objecao_oculta': 'Acho que consigo sozinho',
                'perfil_tipico': 'Pessoas com formação superior, experiência na área, ego profissional',
                'raiz_emocional': 'Orgulho/individualismo - medo de parecer incompetente',
                'sinais_detectacao': [
                    'Menções de "tentar sozinho"',
                    'Resistência a ajuda',
                    'Linguagem técnica excessiva',
                    'Minimização de dificuldades'
                ],
                'contra_ataque': 'Histórias de outros "experts" que precisaram de mentoria para dar salto quântico',
                'reframe': 'Buscar ajuda é sinal de inteligência, não fraqueza'
            },
            'sinal_fraqueza': {
                'objecao_oculta': 'Aceitar ajuda é admitir fracasso',
                'perfil_tipico': 'Principalmente homens, líderes, pessoas com imagem a zelar',
                'raiz_emocional': 'Medo de julgamento, perda de status, humilhação',
                'sinais_detectacao': [
                    'Minimização de problemas',
                    '"Está tudo bem"',
                    'Resistência a expor vulnerabilidade',
                    'Linguagem defensiva'
                ],
                'contra_ataque': 'Reposicionamento de ajuda como "aceleração" e "otimização"',
                'exemplos_herois': 'Os maiores CEOs do mundo têm coaches. Coincidência?'
            },
            'medo_novo': {
                'objecao_oculta': 'Não tenho pressa',
                'perfil_tipico': 'Pessoas estagnadas mas "confortáveis", medo do desconhecido',
                'raiz_emocional': 'Conforto com mediocridade/medo de mudança',
                'sinais_detectacao': [
                    '"Quando for a hora certa"',
                    'Procrastinação disfarçada',
                    'Conformismo',
                    'Evitação de compromissos'
                ],
                'contra_ataque': 'Histórias de arrependimento por não agir + consequências futuras',
                'amplificacao_dor': 'A única coisa pior que a dor da mudança é a dor do arrependimento'
            },
            'prioridades_desequilibradas': {
                'objecao_oculta': 'Não é dinheiro',
                'perfil_tipico': 'Pessoas que gastam em lazer/consumo mas "não têm dinheiro" para evolução',
                'raiz_emocional': 'Não reconhece educação como prioridade, vício em gratificação imediata',
                'sinais_detectacao': [
                    'Menções de gastos em outras áreas',
                    'Justificativas financeiras contraditórias',
                    'Priorização de consumo sobre investimento'
                ],
                'contra_ataque': 'Comparação cruel entre investimentos + cálculo de oportunidade perdida',
                'reformulacao_valores': 'Hierarquia de valores precisa ser reorganizada'
            },
            'autoestima_destruida': {
                'objecao_oculta': 'Não confio em mim',
                'perfil_tipico': 'Pessoas com múltiplas tentativas fracassadas, baixa confiança pessoal',
                'raiz_emocional': '"Sou eu o problema", medo de mais um fracasso',
                'sinais_detectacao': [
                    '"Já tentei antes"',
                    'Histórico de fracassos',
                    'Vitimização',
                    'Autodesqualificação'
                ],
                'contra_ataque': 'Casos de pessoas "piores" que conseguiram + diferencial do método',
                'reconstrucao_confianca': 'Não é você, é o método que estava errado'
            }
        }
    
    def _load_tecnicas_neutralizacao(self) -> Dict[str, str]:
        """Carrega técnicas de neutralização dos anexos"""
        return {
            'concordar_valorizar_apresentar': 'Você tem razão... Por isso criei...',
            'inversao_perspectiva': 'Na verdade é o oposto do que você imagina...',
            'memorias_reviravolta': 'Lembre de quando você decidiu sem certeza...',
            'confronto_controlado': 'Quantas vezes você perdeu oportunidade por isso?',
            'nova_crenca': 'Isso é uma crença limitante, vou te mostrar outro ângulo...'
        }
    
    def _load_arsenal_emergencia(self) -> List[str]:
        """Carrega arsenal de emergência dos anexos"""
        return [
            'Vamos ser honestos: você vai continuar adiando até quando?',
            'A única diferença entre você e quem já conseguiu é a decisão de agir',
            'Quantas oportunidades você já perdeu por "pensar demais"?',
            'Seu futuro está sendo decidido agora, não quando você "estiver pronto"',
            'Condições perfeitas são mito. Decisões corajosas são realidade.'
        ]
    
    def generate_complete_anti_objection_system(
        self, 
        objections_list: List[str], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera sistema completo de engenharia psicológica anti-objeção"""
        
        # Validação crítica de entrada
        if not objections_list:
            logger.error("❌ Lista de objeções vazia")
            # Gera objeções básicas em vez de falhar
            segmento = context_data.get('segmento', 'negócios')
            objections_list = [
                "Não tenho tempo para implementar isso agora",
                "Preciso pensar melhor sobre o investimento",
                "Meu caso é diferente, isso pode não funcionar",
                "Já tentei outras coisas e não deram certo",
                "Preciso de mais garantias de que funciona"
            ]
            logger.warning("⚠️ Usando objeções básicas para sistema anti-objeção")
        
        if not context_data.get('segmento'):
            logger.error("❌ Segmento não informado")
            raise ValueError("SISTEMA ANTI-OBJEÇÃO FALHOU: Segmento obrigatório")
        
        try:
            logger.info(f"🛡️ Gerando sistema anti-objeção para {len(objections_list)} objeções")
            
            # Salva dados de entrada imediatamente
            salvar_etapa("anti_objecao_entrada", {
                "objections_list": objections_list,
                "avatar_data": avatar_data,
                "context_data": context_data
            }, categoria="anti_objecao")
            
            # Analisa e categoriza objeções
            categorized_objections = self._analyze_and_categorize_objections(objections_list, avatar_data)
            
            # Gera sistema de neutralização
            neutralization_system = self._create_neutralization_system(categorized_objections, avatar_data, context_data)
            
            # Cria scripts personalizados
            personalized_scripts = self._create_personalized_scripts(categorized_objections, context_data)
            
            # Gera arsenal de emergência customizado
            emergency_arsenal = self._create_emergency_arsenal(avatar_data, context_data)
            
            result = {
                'objecoes_universais': self._map_to_universal_objections(categorized_objections),
                'objecoes_ocultas': self._identify_hidden_objections(avatar_data, context_data),
                'sistema_neutralizacao': neutralization_system,
                'scripts_personalizados': personalized_scripts,
                'arsenal_emergencia': emergency_arsenal,
                'engenharia_psicologica': self._create_psychological_engineering(objections_list, avatar_data, context_data),
                'mapeamento_por_perfil': self._create_profile_mapping(avatar_data),
                'cronograma_implementacao': self._create_implementation_timeline(),
                'metricas_eficacia': self._create_effectiveness_metrics(),
                'validation_status': 'VALID',
                'generation_timestamp': time.time()
            }
            
            # Salva resultado final imediatamente
            salvar_etapa("anti_objecao_final", result, categoria="anti_objecao")
            
            logger.info("✅ Sistema anti-objeção gerado com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar sistema anti-objeção: {str(e)}")
            salvar_erro("anti_objecao_sistema", e, contexto={"segmento": context_data.get('segmento')})
            
            # Fallback para sistema básico em caso de erro
            logger.warning("🔄 Gerando sistema anti-objeção básico como fallback...")
            return self._generate_fallback_anti_objection_system(context_data)
    
    def _analyze_and_categorize_objections(self, objections: List[str], avatar_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analisa e categoriza objeções usando IA especializada"""
        
        try:
            prompt = f"""
            {self.business_analyst_prompt}
            
            Como especialista em análise de objeções e psicologia de vendas, analise e categorize as seguintes objeções:
            
            OBJEÇÕES IDENTIFICADAS:
            {json.dumps(objections, indent=2, ensure_ascii=False)}
            
            AVATAR:
            {json.dumps(avatar_data, indent=2, ensure_ascii=False)[:1500]}
            
            Categorize cada objeção nas 3 categorias universais:
            1. TEMPO - "Isso não é prioridade para mim"
            2. DINHEIRO - "Minha vida não está tão ruim que precise investir"
            3. CONFIANÇA - "Me dê uma razão para acreditar"
            
            E identifique objeções ocultas:
            1. AUTOSSUFICIÊNCIA - "Acho que consigo sozinho"
            2. SINAL DE FRAQUEZA - "Aceitar ajuda é admitir fracasso"
            3. MEDO DO NOVO - "Não tenho pressa"
            4. PRIORIDADES DESEQUILIBRADAS - "Não é dinheiro"
            5. AUTOESTIMA DESTRUÍDA - "Não confio em mim"
            
            RETORNE APENAS JSON VÁLIDO:
            
            ```json
            {{
              "tempo": ["objeções relacionadas a tempo/prioridade"],
              "dinheiro": ["objeções relacionadas a investimento/valor"],
              "confianca": ["objeções relacionadas a credibilidade/risco"],
              "autossuficiencia": ["objeções de independência"],
              "sinal_fraqueza": ["objeções de imagem/status"],
              "medo_novo": ["objeções de mudança"],
              "prioridades_desequilibradas": ["objeções de valor"],
              "autoestima_destruida": ["objeções de capacidade pessoal"]
            }}
            ```
            """
            
            response = ai_manager.generate_analysis(prompt, max_tokens=1500)
            
            if response:
                clean_response = response.strip()
                if "```json" in clean_response:
                    start = clean_response.find("```json") + 7
                    end = clean_response.rfind("```")
                    clean_response = clean_response[start:end].strip()
                
                try:
                    categorized = json.loads(clean_response)
                    logger.info("✅ Objeções categorizadas com IA")
                    return categorized
                except json.JSONDecodeError:
                    logger.warning("⚠️ IA retornou JSON inválido para categorização")
            
            # Fallback para categorização básica
            return self._basic_categorization(objections)
            
        except Exception as e:
            logger.error(f"❌ Erro ao categorizar objeções: {str(e)}")
            return self._basic_categorization(objections)
    
    def _create_neutralization_system(
        self, 
        categorized_objections: Dict[str, List[str]], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria sistema de neutralização baseado nos anexos"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        neutralization = {}
        
        # Para cada categoria de objeção universal
        for categoria, objecoes in categorized_objections.items():
            if categoria in self.objecoes_universais and objecoes:
                universal_data = self.objecoes_universais[categoria]
                
                neutralization[categoria] = {
                    'objecoes_identificadas': objecoes,
                    'raiz_emocional': universal_data['raiz_emocional'],
                    'estrategia_principal': universal_data['contra_ataque'],
                    'drives_recomendados': universal_data['drives_mentais'],
                    'scripts_neutralizacao': self._create_neutralization_scripts(categoria, objecoes, segmento),
                    'provas_necessarias': self._identify_required_proofs(categoria, avatar_data),
                    'momento_ideal_abordagem': self._determine_ideal_moment(categoria),
                    'intensidade_recomendada': self._calculate_intensity(categoria, avatar_data)
                }
        
        return neutralization
    
    def _create_psychological_engineering(
        self, 
        objections: List[str], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria engenharia psicológica dos anexos"""
        
        return {
            'objecoes_universais_mapeadas': {
                'tempo': 'Isso não é prioridade para mim',
                'dinheiro': 'Minha vida não está tão ruim que precise investir',
                'confianca': 'Me dê uma razão para acreditar'
            },
            'objecoes_ocultas_criticas': {
                'autossuficiencia': 'Acho que consigo sozinho',
                'sinal_fraqueza': 'Aceitar ajuda é admitir fracasso',
                'medo_novo': 'Não tenho pressa',
                'prioridades_desequilibradas': 'Não é dinheiro',
                'autoestima_destruida': 'Não confio em mim'
            },
            'tecnicas_neutralizacao': [
                'Concordar + Valorizar + Apresentar',
                'Inversão de Perspectiva',
                'Memórias de Reviravolta',
                'Confronto Controlado',
                'Nova Crença'
            ],
            'arsenal_emergencia': self.arsenal_emergencia,
            'sequencia_psicologica': [
                'Identificar objeção real (não a verbalizada)',
                'Validar preocupação como legítima',
                'Apresentar perspectiva alternativa',
                'Oferecer prova irrefutável',
                'Criar urgência de decisão'
            ]
        }
    
    def _create_personalized_scripts(
        self, 
        categorized_objections: Dict[str, List[str]], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Dict[str, str]]:
        """Cria scripts personalizados para cada categoria"""
        
        segmento = context_data.get('segmento', 'negócios')
        scripts = {}
        
        for categoria, objecoes in categorized_objections.items():
            if categoria in self.objecoes_universais and objecoes:
                scripts[categoria] = {
                    'abertura': f'Entendo perfeitamente sua preocupação com {categoria}...',
                    'validacao': f'Na verdade, pessoas inteligentes como você sempre pensam nisso...',
                    'reframe': f'E é exatamente por isso que criei este sistema para {segmento}...',
                    'prova': f'Deixe-me mostrar como outros profissionais de {segmento} superaram isso...',
                    'fechamento': f'A pergunta não é SE você vai resolver isso, é QUANDO...'
                }
        
        return scripts
    
    def _create_emergency_arsenal(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> List[str]:
        """Cria arsenal de emergência customizado"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return [
            f'Vamos ser honestos sobre {segmento}: você vai continuar adiando até quando?',
            f'A única diferença entre você e quem já domina {segmento} é a decisão de agir',
            f'Quantas oportunidades em {segmento} você já perdeu por "pensar demais"?',
            f'Seu futuro em {segmento} está sendo decidido agora, não quando você "estiver pronto"',
            f'Condições perfeitas em {segmento} são mito. Decisões corajosas são realidade.'
        ]
    
    def _generate_fallback_anti_objection_system(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sistema anti-objeção básico como fallback"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return {
            'objecoes_universais': {
                'tempo': {
                    'objecao': 'Não tenho tempo',
                    'contra_ataque': f'Tempo não é sobre ter, é sobre priorizar {segmento}',
                    'script': f'Entendo que {segmento} parece não ser prioridade agora...'
                },
                'dinheiro': {
                    'objecao': 'Não tenho orçamento',
                    'contra_ataque': f'Investimento em {segmento} se paga sozinho',
                    'script': f'Vamos calcular o ROI real de dominar {segmento}...'
                },
                'confianca': {
                    'objecao': 'Preciso de garantias',
                    'contra_ataque': f'Resultados em {segmento} falam por si',
                    'script': f'Deixe-me mostrar casos reais de {segmento}...'
                }
            },
            'arsenal_emergencia': self._create_emergency_arsenal({}, context_data),
            'validation_status': 'FALLBACK_VALID',
            'generation_timestamp': time.time(),
            'fallback_mode': True
        }
    
    def _basic_categorization(self, objections: List[str]) -> Dict[str, List[str]]:
        """Categorização básica de objeções"""
        
        categorized = {
            'tempo': [],
            'dinheiro': [],
            'confianca': [],
            'autossuficiencia': [],
            'sinal_fraqueza': [],
            'medo_novo': [],
            'prioridades_desequilibradas': [],
            'autoestima_destruida': []
        }
        
        for objection in objections:
            objection_lower = objection.lower()
            
            if any(word in objection_lower for word in ['tempo', 'prioridade', 'ocupado', 'agenda']):
                categorized['tempo'].append(objection)
            elif any(word in objection_lower for word in ['dinheiro', 'caro', 'investimento', 'orçamento']):
                categorized['dinheiro'].append(objection)
            elif any(word in objection_lower for word in ['confiança', 'garantia', 'prova', 'funciona']):
                categorized['confianca'].append(objection)
            elif any(word in objection_lower for word in ['sozinho', 'conseguir', 'tentar']):
                categorized['autossuficiencia'].append(objection)
            else:
                categorized['confianca'].append(objection)  # Default
        
        return categorized
    
    def _create_neutralization_scripts(self, categoria: str, objecoes: List[str], segmento: str) -> List[str]:
        """Cria scripts de neutralização específicos"""
        
        if categoria == 'tempo':
            return [
                f'Entendo que {segmento} parece não ser prioridade agora. Na verdade, pessoas inteligentes como você sempre avaliam prioridades. E é exatamente por isso que criei um sistema que funciona mesmo com agenda apertada...',
                f'Tempo não é sobre ter, é sobre priorizar. E {segmento} deveria ser sua prioridade número 1 porque...',
                f'Cada dia sem otimizar {segmento} custa mais tempo no futuro. É investimento de tempo, não gasto.'
            ]
        elif categoria == 'dinheiro':
            return [
                f'Vamos ser honestos sobre {segmento}: quanto você já perdeu NÃO investindo na solução certa?',
                f'O custo de não dominar {segmento} é muito maior que o investimento para dominar.',
                f'Pessoas inteligentes investem em {segmento} porque sabem que se paga sozinho.'
            ]
        elif categoria == 'confianca':
            return [
                f'Suas preocupações sobre {segmento} são legítimas e inteligentes. Por isso vou te mostrar provas irrefutáveis...',
                f'Não precisa confiar em mim. Precisa confiar nos resultados que vou te mostrar em {segmento}.',
                f'Assumo todo o risco: se não funcionar em {segmento}, você não paga nada.'
            ]
        else:
            return [f'Script personalizado para {categoria} em {segmento}']

# Instância global
anti_objection_system = AntiObjectionSystem()