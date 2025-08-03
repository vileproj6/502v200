#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Mental Drivers Architect
Arquiteto de Drivers Mentais Customizados
"""

import time
import random
import logging
import json
import json
from typing import Dict, List, Any, Optional
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class MentalDriversArchitect:
    """Arquiteto de Drivers Mentais Customizados"""
    
    def __init__(self):
        """Inicializa o arquiteto de drivers mentais"""
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
        
        self.universal_drivers = self._load_universal_drivers()
        self.driver_templates = self._load_driver_templates()
        self.arsenal_completo = self._load_arsenal_completo()
        
        logger.info("Mental Drivers Architect inicializado")
    
    def _load_arsenal_completo(self) -> Dict[str, Dict[str, Any]]:
        """Carrega arsenal completo dos 19 drivers universais dos anexos"""
        return {
            # DRIVERS EMOCIONAIS PRIMÁRIOS
            'ferida_exposta': {
                'nome': 'Ferida Exposta',
                'gatilho_central': 'Dor não resolvida',
                'mecanica': 'Trazer à consciência o que foi reprimido',
                'ativacao': 'Você ainda [comportamento doloroso] mesmo sabendo que [consequência]?',
                'categoria': 'emocional_primario'
            },
            'trofeu_secreto': {
                'nome': 'Troféu Secreto',
                'gatilho_central': 'Desejo inconfessável',
                'mecanica': 'Validar ambições "proibidas"',
                'ativacao': 'Não é sobre dinheiro, é sobre [desejo real oculto]',
                'categoria': 'emocional_primario'
            },
            'inveja_produtiva': {
                'nome': 'Inveja Produtiva',
                'gatilho_central': 'Comparação com pares',
                'mecanica': 'Transformar inveja em combustível',
                'ativacao': 'Enquanto você [situação atual], outros como você [resultado desejado]',
                'categoria': 'emocional_primario'
            },
            'relogio_psicologico': {
                'nome': 'Relógio Psicológico',
                'gatilho_central': 'Urgência existencial',
                'mecanica': 'Tempo como recurso finito',
                'ativacao': 'Quantos [período] você ainda vai [desperdício]?',
                'categoria': 'emocional_primario'
            },
            'identidade_aprisionada': {
                'nome': 'Identidade Aprisionada',
                'gatilho_central': 'Conflito entre quem é e quem poderia ser',
                'mecanica': 'Expor a máscara social',
                'ativacao': 'Você não é [rótulo limitante], você é [potencial real]',
                'categoria': 'emocional_primario'
            },
            'custo_invisivel': {
                'nome': 'Custo Invisível',
                'gatilho_central': 'Perda não percebida',
                'mecanica': 'Quantificar o preço da inação',
                'ativacao': 'Cada dia sem [solução] custa [perda específica]',
                'categoria': 'emocional_primario'
            },
            'ambicao_expandida': {
                'nome': 'Ambição Expandida',
                'gatilho_central': 'Sonhos pequenos demais',
                'mecanica': 'Elevar o teto mental de possibilidades',
                'ativacao': 'Se o esforço é o mesmo, por que você está pedindo tão pouco?',
                'categoria': 'emocional_primario'
            },
            'diagnostico_brutal': {
                'nome': 'Diagnóstico Brutal',
                'gatilho_central': 'Confronto com a realidade atual',
                'mecanica': 'Criar indignação produtiva com status quo',
                'ativacao': 'Olhe seus números/situação. Até quando você vai aceitar isso?',
                'categoria': 'emocional_primario'
            },
            'ambiente_vampiro': {
                'nome': 'Ambiente Vampiro',
                'gatilho_central': 'Consciência do entorno tóxico',
                'mecanica': 'Revelar como ambiente atual suga energia/potencial',
                'ativacao': 'Seu ambiente te impulsiona ou te mantém pequeno?',
                'categoria': 'emocional_primario'
            },
            'mentor_salvador': {
                'nome': 'Mentor Salvador',
                'gatilho_central': 'Necessidade de orientação externa',
                'mecanica': 'Ativar desejo por figura de autoridade que acredita neles',
                'ativacao': 'Você precisa de alguém que veja seu potencial quando você não consegue',
                'categoria': 'emocional_primario'
            },
            'coragem_necessaria': {
                'nome': 'Coragem Necessária',
                'gatilho_central': 'Medo paralisante disfarçado',
                'mecanica': 'Transformar desculpas em decisões corajosas',
                'ativacao': 'Não é sobre condições perfeitas, é sobre decidir apesar do medo',
                'categoria': 'emocional_primario'
            },
            # DRIVERS RACIONAIS COMPLEMENTARES
            'mecanismo_revelado': {
                'nome': 'Mecanismo Revelado',
                'gatilho_central': 'Compreensão do "como"',
                'mecanica': 'Desmistificar o complexo',
                'ativacao': 'É simplesmente [analogia simples], não [complicação percebida]',
                'categoria': 'racional_complementar'
            },
            'prova_matematica': {
                'nome': 'Prova Matemática',
                'gatilho_central': 'Certeza numérica',
                'mecanica': 'Equação irrefutável',
                'ativacao': 'Se você fizer X por Y dias = Resultado Z garantido',
                'categoria': 'racional_complementar'
            },
            'padrao_oculto': {
                'nome': 'Padrão Oculto',
                'gatilho_central': 'Insight revelador',
                'mecanica': 'Mostrar o que sempre esteve lá',
                'ativacao': 'Todos que conseguiram [resultado] fizeram [padrão específico]',
                'categoria': 'racional_complementar'
            },
            'excecao_possivel': {
                'nome': 'Exceção Possível',
                'gatilho_central': 'Quebra de limitação',
                'mecanica': 'Provar que regras podem ser quebradas',
                'ativacao': 'Diziam que [limitação], mas [prova contrária]',
                'categoria': 'racional_complementar'
            },
            'atalho_etico': {
                'nome': 'Atalho Ético',
                'gatilho_central': 'Eficiência sem culpa',
                'mecanica': 'Validar o caminho mais rápido',
                'ativacao': 'Por que sofrer [tempo longo] se existe [atalho comprovado]?',
                'categoria': 'racional_complementar'
            },
            'decisao_binaria': {
                'nome': 'Decisão Binária',
                'gatilho_central': 'Simplificação radical',
                'mecanica': 'Eliminar zona cinzenta',
                'ativacao': 'Ou você [ação desejada] ou aceita [consequência dolorosa]',
                'categoria': 'racional_complementar'
            },
            'oportunidade_oculta': {
                'nome': 'Oportunidade Oculta',
                'gatilho_central': 'Vantagem não percebida',
                'mecanica': 'Revelar demanda/chance óbvia mas ignorada',
                'ativacao': 'O mercado está gritando por [solução] e ninguém está ouvindo',
                'categoria': 'racional_complementar'
            },
            'metodo_vs_sorte': {
                'nome': 'Método vs Sorte',
                'gatilho_central': 'Caos vs sistema',
                'mecanica': 'Contrastar tentativa aleatória com caminho estruturado',
                'ativacao': 'Sem método você está cortando mata com foice. Com método, está na autoestrada',
                'categoria': 'racional_complementar'
            }
        }
    
    def _load_universal_drivers(self) -> Dict[str, Dict[str, Any]]:
        """Carrega drivers mentais universais"""
        return {
            'urgencia_temporal': {
                'nome': 'Urgência Temporal',
                'gatilho_central': 'Tempo limitado para agir',
                'definicao_visceral': 'Criar pressão temporal que força decisão imediata',
                'aplicacao': 'Quando prospect está procrastinando'
            },
            'escassez_oportunidade': {
                'nome': 'Escassez de Oportunidade',
                'gatilho_central': 'Oportunidade única e limitada',
                'definicao_visceral': 'Amplificar valor através da raridade',
                'aplicacao': 'Para aumentar percepção de valor'
            },
            'prova_social': {
                'nome': 'Prova Social Qualificada',
                'gatilho_central': 'Outros como ele já conseguiram',
                'definicao_visceral': 'Reduzir risco através de validação social',
                'aplicacao': 'Para superar objeções de confiança'
            },
            'autoridade_tecnica': {
                'nome': 'Autoridade Técnica',
                'gatilho_central': 'Expertise comprovada',
                'definicao_visceral': 'Estabelecer credibilidade através de conhecimento',
                'aplicacao': 'Para construir confiança inicial'
            },
            'reciprocidade': {
                'nome': 'Reciprocidade Estratégica',
                'gatilho_central': 'Valor entregue antecipadamente',
                'definicao_visceral': 'Criar obrigação psicológica de retribuição',
                'aplicacao': 'Para gerar compromisso'
            }
        }
    
    def _load_driver_templates(self) -> Dict[str, str]:
        """Carrega templates de drivers"""
        return {
            'historia_analogia': 'Era uma vez {personagem} que enfrentava {problema_similar}. Depois de {tentativas_fracassadas}, descobriu que {solucao_especifica} e conseguiu {resultado_transformador}.',
            'metafora_visual': 'Imagine {situacao_atual} como {metafora_visual}. Agora visualize {situacao_ideal} como {metafora_transformada}.',
            'comando_acao': 'Agora que você {compreensao_adquirida}, a única ação lógica é {acao_especifica} porque {consequencia_inevitavel}.'
        }
    
    def generate_complete_drivers_system(
        self, 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera sistema completo de drivers mentais customizados"""
        
        # Validação crítica de entrada
        if not avatar_data:
            logger.error("❌ Dados do avatar ausentes")
            # Cria avatar básico em vez de falhar
            segmento = context_data.get('segmento', 'negócios')
            avatar_data = {
                'dores_viscerais': [
                    f"Trabalhar excessivamente em {segmento} sem crescer",
                    "Sentir-se sempre correndo atrás da concorrência",
                    "Ver competidores crescendo mais rápido"
                ],
                'desejos_secretos': [
                    f"Ser autoridade em {segmento}",
                    "Ter liberdade financeira",
                    "Negócio que funcione sozinho"
                ]
            }
            logger.warning("⚠️ Usando avatar básico para drivers mentais")
        
        if not context_data.get('segmento'):
            logger.error("❌ Segmento não informado")
            raise ValueError("DRIVERS MENTAIS FALHARAM: Segmento obrigatório")
        
        try:
            logger.info("🧠 Gerando drivers mentais customizados...")
            
            # Salva dados de entrada imediatamente
            salvar_etapa("drivers_entrada", {
                "avatar_data": avatar_data,
                "context_data": context_data
            }, categoria="drivers_mentais")
            
            # Analisa avatar para identificar drivers ideais
            ideal_drivers = self._identify_ideal_drivers(avatar_data, context_data)
            
            # Gera drivers customizados
            customized_drivers = self._generate_customized_drivers(ideal_drivers, avatar_data, context_data)
            
            if not customized_drivers:
                logger.error("❌ Falha na geração de drivers customizados")
                # Usa fallback em vez de falhar
                logger.warning("🔄 Usando drivers básicos como fallback")
                customized_drivers = self._generate_fallback_drivers_system(context_data)
            
            # Salva drivers customizados
            salvar_etapa("drivers_customizados", customized_drivers, categoria="drivers_mentais")
            
            # Cria roteiros de ativação
            activation_scripts = self._create_activation_scripts(customized_drivers, avatar_data)
            
            # Gera frases de ancoragem
            anchor_phrases = self._generate_anchor_phrases(customized_drivers, avatar_data)
            
            result = {
                'drivers_customizados': customized_drivers,
                'roteiros_ativacao': activation_scripts,
                'frases_ancoragem': anchor_phrases,
                'drivers_universais_utilizados': [d['nome'] for d in ideal_drivers],
                'personalizacao_nivel': self._calculate_personalization_level(customized_drivers),
                'validation_status': 'VALID',
                'generation_timestamp': time.time()
            }
            
            # Salva resultado final imediatamente
            salvar_etapa("drivers_final", result, categoria="drivers_mentais")
            
            logger.info("✅ Drivers mentais customizados gerados com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar drivers mentais: {str(e)}")
            salvar_erro("drivers_sistema", e, contexto={"segmento": context_data.get('segmento')})
            
            # Fallback para sistema básico em caso de erro
            logger.warning("🔄 Gerando drivers básicos como fallback...")
            return self._generate_fallback_drivers_system(context_data)
    
    def _generate_customized_drivers_from_arsenal(
        self, 
        ideal_drivers: List[Dict[str, Any]], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gera drivers customizados usando arsenal completo dos anexos"""
        
        try:
            segmento = context_data.get('segmento', 'negócios')
            
            # Prompt aprimorado com especialização em análise de negócios
            prompt = f"""
            {self.business_analyst_prompt}
            
            Como especialista em drivers mentais e análise de negócios, crie drivers mentais customizados para o segmento {segmento}.
            
            Use o arsenal completo dos 19 drivers universais dos anexos:
            
            DRIVERS EMOCIONAIS PRIMÁRIOS:
            1. Ferida Exposta - Dor não resolvida
            2. Troféu Secreto - Desejo inconfessável  
            3. Inveja Produtiva - Comparação com pares
            4. Relógio Psicológico - Urgência existencial
            5. Identidade Aprisionada - Conflito identitário
            6. Custo Invisível - Perda não percebida
            7. Ambição Expandida - Sonhos pequenos demais
            8. Diagnóstico Brutal - Confronto com realidade
            9. Ambiente Vampiro - Entorno tóxico
            10. Mentor Salvador - Necessidade de orientação
            11. Coragem Necessária - Medo paralisante
            
            DRIVERS RACIONAIS COMPLEMENTARES:
            12. Mecanismo Revelado - Compreensão do "como"
            13. Prova Matemática - Certeza numérica
            14. Padrão Oculto - Insight revelador
            15. Exceção Possível - Quebra de limitação
            16. Atalho Ético - Eficiência sem culpa
            17. Decisão Binária - Simplificação radical
            18. Oportunidade Oculta - Vantagem não percebida
            19. Método vs Sorte - Caos vs sistema

            AVATAR:
            {json.dumps(avatar_data, indent=2, ensure_ascii=False)[:2000]}

            DRIVERS IDEAIS IDENTIFICADOS:
            {json.dumps(ideal_drivers, indent=2, ensure_ascii=False)[:1000]}

            RETORNE APENAS JSON VÁLIDO com drivers customizados baseados no arsenal dos anexos:

            ```json
            [
              {{
                "nome": "Nome específico do driver baseado no arsenal",
                "driver_base": "Nome do driver universal usado como base",
                "gatilho_central": "Gatilho psicológico principal",
                "definicao_visceral": "Definição que gera impacto emocional",
                "mecanica_psicologica": "Como funciona no cérebro",
                "momento_instalacao": "Quando plantar durante a jornada",
                "roteiro_ativacao": {{
                  "pergunta_abertura": "Pergunta que ativa o driver",
                  "historia_analogia": "História específica de 150+ palavras",
                  "metafora_visual": "Metáfora visual poderosa",
                  "comando_acao": "Comando específico de ação"
                }},
                "frases_ancoragem": [
                  "Frase 1 de ancoragem psicológica",
                  "Frase 2 de ancoragem psicológica",
                  "Frase 3 de ancoragem psicológica"
                ],
                "prova_logica": "Prova lógica que sustenta o driver",
                "loop_reforco": "Como reativar em momentos posteriores",
                "categoria": "emocional_primario ou racional_complementar"
              }}
            ]
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
                    drivers = json.loads(clean_response)
                    if isinstance(drivers, list) and len(drivers) > 0:
                        logger.info("✅ Drivers customizados gerados com arsenal dos anexos")
                        return drivers
                    else:
                        logger.warning("⚠️ IA retornou formato inválido")
                except json.JSONDecodeError:
                    logger.warning("⚠️ IA retornou JSON inválido")
            
            # Fallback para drivers básicos
            return self._create_basic_drivers_from_arsenal(context_data)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar drivers customizados: {str(e)}")
            # NÃO RETORNA FALLBACK - FALHA EXPLICITAMENTE
            raise Exception(f"DRIVERS CUSTOMIZADOS FALHARAM: {str(e)}")
    
    def _create_basic_drivers_from_arsenal(self, context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Cria drivers básicos usando arsenal dos anexos"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return [
            {
                'nome': f'Diagnóstico Brutal {segmento}',
                'driver_base': 'diagnostico_brutal',
                'gatilho_central': f'Confronto com realidade atual em {segmento}',
                'definicao_visceral': f'Criar indignação produtiva com status quo em {segmento}',
                'mecanica_psicologica': 'Quebra padrão mental de conformismo',
                'momento_instalacao': 'Abertura - primeira quebra de padrão',
                'roteiro_ativacao': {
                    'pergunta_abertura': f'Olhe seus números em {segmento}. Até quando você vai aceitar isso?',
                    'historia_analogia': f'Conheci um profissional de {segmento} que estava estagnado há 3 anos. Trabalhava 12 horas por dia mas não saía do lugar. Quando implementou um sistema específico para {segmento}, em 6 meses triplicou os resultados. A diferença não foi trabalhar mais, foi trabalhar com método.',
                    'metafora_visual': f'Imagine {segmento} como uma corrida. Você está correndo no lugar enquanto outros avançam.',
                    'comando_acao': f'Pare de aceitar mediocridade em {segmento} e exija excelência de si mesmo'
                },
                'frases_ancoragem': [
                    f'Mediocridade em {segmento} é escolha, não destino',
                    f'Seus números em {segmento} refletem suas decisões',
                    f'Status quo em {segmento} é zona de conforto disfarçada'
                ],
                'prova_logica': f'Profissionais que aplicaram diagnóstico brutal em {segmento} cresceram 300% mais rápido',
                'loop_reforco': f'Toda vez que ver números estagnados, lembrar: diagnóstico brutal é primeiro passo',
                'categoria': 'emocional_primario'
            },
            {
                'nome': f'Ambição Expandida {segmento}',
                'driver_base': 'ambicao_expandida',
                'gatilho_central': f'Sonhos pequenos demais em {segmento}',
                'definicao_visceral': f'Elevar o teto mental de possibilidades em {segmento}',
                'mecanica_psicologica': 'Expande visão de potencial realizável',
                'momento_instalacao': 'Desenvolvimento - após diagnóstico',
                'roteiro_ativacao': {
                    'pergunta_abertura': f'Se o esforço é o mesmo, por que você está pedindo tão pouco em {segmento}?',
                    'historia_analogia': f'Um cliente meu em {segmento} queria ganhar R$ 10 mil por mês. Perguntei: por que não R$ 50 mil? Ele disse que era impossível. Em 8 meses estava faturando R$ 80 mil mensais. O limite estava na mente, não no mercado.',
                    'metafora_visual': f'Ambição em {segmento} é como músculo - quanto mais exercita, mais forte fica',
                    'comando_acao': f'Multiplique sua meta em {segmento} por 5 e descubra como chegar lá'
                },
                'frases_ancoragem': [
                    f'Pequenos sonhos em {segmento} geram pequenos resultados',
                    f'Mercado de {segmento} premia quem pensa grande',
                    f'Ambição expandida em {segmento} atrai oportunidades maiores'
                ],
                'prova_logica': f'Profissionais com metas 5x maiores em {segmento} alcançam resultados 3x superiores',
                'loop_reforco': f'Sempre que definir meta em {segmento}, perguntar: posso multiplicar por 5?',
                'categoria': 'emocional_primario'
            },
            {
                'nome': f'Método vs Sorte {segmento}',
                'driver_base': 'metodo_vs_sorte',
                'gatilho_central': 'Diferença entre método e tentativa',
                'definicao_visceral': f'Parar de tentar e começar a aplicar método em {segmento}',
                'mecanica_psicologica': 'Contrasta caos com sistema estruturado',
                'momento_instalacao': 'Pré-fechamento - antes da oferta',
                'roteiro_ativacao': {
                    'pergunta_abertura': f'Você está tentando ou aplicando método em {segmento}?',
                    'historia_analogia': f'Dois profissionais de {segmento} começaram juntos. Um ficou tentando estratégias aleatórias, outro seguiu um método específico. Após 1 ano: o primeiro ainda lutava para crescer, o segundo já era referência no mercado. A diferença não foi talento, foi método.',
                    'metafora_visual': f'Tentar em {segmento} é como atirar no escuro. Método é como ter mira laser.',
                    'comando_acao': f'Pare de tentar e comece a aplicar método comprovado em {segmento}'
                },
                'frases_ancoragem': [
                    f'Método em {segmento} elimina tentativa e erro',
                    f'Profissionais com método crescem 10x mais rápido',
                    f'Sorte é para quem não tem método em {segmento}'
                ],
                'prova_logica': f'Metodologia específica para {segmento} reduz tempo de resultado em 80%',
                'loop_reforco': f'Sempre que enfrentar desafio em {segmento}, perguntar: qual o método?',
                'categoria': 'racional_complementar'
            }
        ]
    
    def _create_psychological_anchoring_system(
        self, 
        drivers: List[Dict[str, Any]], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria sistema de ancoragem psicológica dos anexos"""
        
        return {
            'tecnicas_ancoragem': [
                'Repetição estratégica de frases-chave',
                'Associação com experiências emocionais',
                'Reforço através de múltiplos canais',
                'Ancoragem visual e auditiva'
            ],
            'momentos_reativacao': [
                'Início de cada interação',
                'Momentos de objeção',
                'Pré-fechamento',
                'Pós-venda'
            ],
            'frases_ancora': [
                f"Lembre-se: {drivers[0].get('nome', 'método')} funciona",
                "Você já decidiu mudar, agora é só escolher como",
                "Cada dia sem ação é uma oportunidade perdida"
            ],
            'sequencia_psicologica_otimizada': self._create_psychological_sequence(drivers),
            'arsenal_emergencia': [
                'Vamos ser honestos: você vai continuar adiando até quando?',
                'A única diferença entre você e quem já conseguiu é a decisão de agir',
                'Quantas oportunidades você já perdeu por "pensar demais"?'
            ]
        }
    
    def _get_complete_arsenal_usage(self, customized_drivers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mapeia uso do arsenal completo dos 19 drivers"""
        
        return {
            'drivers_emocionais_utilizados': [
                d for d in customized_drivers 
                if d.get('categoria') == 'emocional_primario'
            ],
            'drivers_racionais_utilizados': [
                d for d in customized_drivers 
                if d.get('categoria') == 'racional_complementar'
            ],
            'sequencia_recomendada': [
                'Fase 1 - Despertar: Oportunidade Oculta, Diagnóstico Brutal',
                'Fase 2 - Desejo: Ambição Expandida, Troféu Secreto',
                'Fase 3 - Decisão: Relógio Psicológico, Decisão Binária',
                'Fase 4 - Direção: Método vs Sorte, Mentor Salvador'
            ],
            'drivers_complementares_disponiveis': [
                nome for nome, driver in self.arsenal_completo.items()
                if not any(d.get('driver_base') == nome for d in customized_drivers)
            ]
        }
    
    def _create_optimized_sequence(self, drivers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cria sequência otimizada baseada nos anexos"""
        
        return {
            'ordem_psicologica': [
                {
                    'posicao': i + 1,
                    'driver': driver['nome'],
                    'momento_ideal': driver.get('momento_instalacao', 'Desenvolvimento'),
                    'intensidade': 'Alta' if i < 2 else 'Média' if i < 4 else 'Baixa',
                    'transicao_proxima': f"Conecta com {drivers[i+1]['nome'] if i+1 < len(drivers) else 'oferta'}"
                }
                for i, driver in enumerate(drivers)
            ],
            'escalada_emocional': 'Crescente até o clímax da oferta',
            'pontos_criticos': [
                'Momento do diagnóstico brutal',
                'Revelação da ambição expandida',
                'Urgência do relógio psicológico',
                'Decisão binária final'
            ]
        }
    
    def _create_psychological_sequence(self, drivers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cria sequência psicológica dos anexos"""
        
        return [
            {
                'fase': 'quebra',
                'objetivo': 'Destruir a ilusão confortável',
                'duracao': '3-5 minutos',
                'drivers_utilizados': [d['nome'] for d in drivers if 'diagnóstico' in d['nome'].lower()],
                'resultado_esperado': 'Desconforto produtivo'
            },
            {
                'fase': 'exposicao',
                'objetivo': 'Revelar a ferida real',
                'duracao': '4-6 minutos',
                'drivers_utilizados': [d['nome'] for d in drivers if 'custo' in d['nome'].lower()],
                'resultado_esperado': 'Consciência da dor'
            },
            {
                'fase': 'vislumbre',
                'objetivo': 'Mostrar o possível',
                'duracao': '5-7 minutos',
                'drivers_utilizados': [d['nome'] for d in drivers if 'ambição' in d['nome'].lower()],
                'resultado_esperado': 'Desejo amplificado'
            },
            {
                'fase': 'necessidade',
                'objetivo': 'Tornar mudança inevitável',
                'duracao': '3-4 minutos',
                'drivers_utilizados': [d['nome'] for d in drivers if 'método' in d['nome'].lower()],
                'resultado_esperado': 'Necessidade de solução'
            }
        ]
    
    def _identify_ideal_drivers(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica drivers ideais baseado no avatar"""
        
        ideal_drivers = []
        
        # Analisa dores para identificar drivers
        dores = avatar_data.get('dores_viscerais', [])
        
        # Mapeia dores para drivers
        if any('tempo' in dor.lower() for dor in dores):
            ideal_drivers.append(self.universal_drivers['urgencia_temporal'])
        
        if any('concorrência' in dor.lower() or 'competidor' in dor.lower() for dor in dores):
            ideal_drivers.append(self.universal_drivers['escassez_oportunidade'])
        
        if any('resultado' in dor.lower() or 'crescimento' in dor.lower() for dor in dores):
            ideal_drivers.append(self.universal_drivers['prova_social'])
        
        # Sempre inclui autoridade técnica
        ideal_drivers.append(self.universal_drivers['autoridade_tecnica'])
        
        # Sempre inclui reciprocidade
        ideal_drivers.append(self.universal_drivers['reciprocidade'])
        
        return ideal_drivers[:5]  # Máximo 5 drivers
    
    def _generate_customized_drivers(
        self, 
        ideal_drivers: List[Dict[str, Any]], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gera drivers customizados usando IA"""
        
        try:
            segmento = context_data.get('segmento', 'negócios')
            
            prompt = f"""
Crie drivers mentais customizados para o segmento {segmento}.

AVATAR:
{json.dumps(avatar_data, indent=2, ensure_ascii=False)[:2000]}

DRIVERS IDEAIS:
{json.dumps(ideal_drivers, indent=2, ensure_ascii=False)[:1000]}

RETORNE APENAS JSON VÁLIDO:

```json
[
  {{
    "nome": "Nome específico do driver",
    "gatilho_central": "Gatilho psicológico principal",
    "definicao_visceral": "Definição que gera impacto emocional",
    "roteiro_ativacao": {{
      "pergunta_abertura": "Pergunta que ativa o driver",
      "historia_analogia": "História específica de 150+ palavras",
      "metafora_visual": "Metáfora visual poderosa",
      "comando_acao": "Comando específico de ação"
    }},
    "frases_ancoragem": [
      "Frase 1 de ancoragem",
      "Frase 2 de ancoragem",
      "Frase 3 de ancoragem"
    ],
    "prova_logica": "Prova lógica que sustenta o driver"
  }}
]
```
"""
            
            response = ai_manager.generate_analysis(prompt, max_tokens=2000)
            
            if response:
                clean_response = response.strip()
                if "```json" in clean_response:
                    start = clean_response.find("```json") + 7
                    end = clean_response.rfind("```")
                    clean_response = clean_response[start:end].strip()
                
                try:
                    drivers = json.loads(clean_response)
                    if isinstance(drivers, list) and len(drivers) > 0:
                        logger.info("✅ Drivers customizados gerados com IA")
                        return drivers
                    else:
                        logger.warning("⚠️ IA retornou formato inválido")
                except json.JSONDecodeError:
                    logger.warning("⚠️ IA retornou JSON inválido")
            
            # Fallback para drivers básicos
            return self._create_basic_drivers(context_data)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar drivers customizados: {str(e)}")
            # NÃO RETORNA FALLBACK - FALHA EXPLICITAMENTE
            raise Exception(f"DRIVERS CUSTOMIZADOS FALHARAM: {str(e)}")
    
    def _create_basic_drivers(self, context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Cria drivers básicos como fallback"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return [
            {
                'nome': f'Urgência {segmento}',
                'gatilho_central': f'Tempo limitado para dominar {segmento}',
                'definicao_visceral': f'Cada dia sem otimizar {segmento} é oportunidade perdida',
                'roteiro_ativacao': {
                    'pergunta_abertura': f'Há quanto tempo você está no mesmo nível em {segmento}?',
                    'historia_analogia': f'Conheci um profissional de {segmento} que estava estagnado há 3 anos. Trabalhava 12 horas por dia mas não saía do lugar. Quando implementou um sistema específico para {segmento}, em 6 meses triplicou os resultados. A diferença não foi trabalhar mais, foi trabalhar com método.',
                    'metafora_visual': f'Imagine {segmento} como uma corrida. Você está correndo no lugar enquanto outros avançam.',
                    'comando_acao': f'Pare de correr no lugar em {segmento} e comece a usar um método comprovado'
                },
                'frases_ancoragem': [
                    f'Cada mês sem otimizar {segmento} custa oportunidades',
                    f'Seus concorrentes em {segmento} não estão esperando',
                    f'O tempo perdido em {segmento} não volta mais'
                ],
                'prova_logica': f'Profissionais que aplicaram métodos específicos em {segmento} cresceram 300% mais rápido'
            },
            {
                'nome': f'Autoridade {segmento}',
                'gatilho_central': f'Expertise comprovada em {segmento}',
                'definicao_visceral': f'Ser reconhecido como autoridade em {segmento}',
                'roteiro_ativacao': {
                    'pergunta_abertura': f'O que falta para você ser visto como autoridade em {segmento}?',
                    'historia_analogia': f'Um cliente meu em {segmento} era invisível no mercado. Aplicou nossa metodologia e em 8 meses estava palestrando em eventos do setor. A diferença foi posicionamento estratégico e execução consistente.',
                    'metafora_visual': f'Autoridade em {segmento} é como um farol - todos veem e confiam',
                    'comando_acao': f'Construa sua autoridade em {segmento} com método comprovado'
                },
                'frases_ancoragem': [
                    f'Autoridade em {segmento} atrai clientes automaticamente',
                    f'Especialistas em {segmento} cobram 5x mais',
                    f'Reconhecimento em {segmento} gera oportunidades únicas'
                ],
                'prova_logica': f'Autoridades em {segmento} têm 500% mais oportunidades de negócio'
            },
            {
                'nome': f'Método vs Sorte',
                'gatilho_central': 'Diferença entre método e tentativa',
                'definicao_visceral': f'Parar de tentar e começar a aplicar método em {segmento}',
                'roteiro_ativacao': {
                    'pergunta_abertura': f'Você está tentando ou aplicando método em {segmento}?',
                    'historia_analogia': f'Dois profissionais de {segmento} começaram juntos. Um ficou tentando estratégias aleatórias, outro seguiu um método específico. Após 1 ano: o primeiro ainda lutava para crescer, o segundo já era referência no mercado. A diferença não foi talento, foi método.',
                    'metafora_visual': f'Tentar em {segmento} é como atirar no escuro. Método é como ter mira laser.',
                    'comando_acao': f'Pare de tentar e comece a aplicar método comprovado em {segmento}'
                },
                'frases_ancoragem': [
                    f'Método em {segmento} elimina tentativa e erro',
                    f'Profissionais com método crescem 10x mais rápido',
                    f'Sorte é para quem não tem método'
                ],
                'prova_logica': f'Metodologia específica para {segmento} reduz tempo de resultado em 80%'
            }
        ]
    
    def _create_activation_scripts(self, drivers: List[Dict[str, Any]], avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria roteiros de ativação para cada driver"""
        
        scripts = {}
        
        for driver in drivers:
            driver_name = driver.get('nome', 'Driver')
            roteiro = driver.get('roteiro_ativacao', {})
            
            scripts[driver_name] = {
                'abertura': roteiro.get('pergunta_abertura', ''),
                'desenvolvimento': roteiro.get('historia_analogia', ''),
                'fechamento': roteiro.get('comando_acao', ''),
                'tempo_estimado': '3-5 minutos',
                'intensidade': 'Alta'
            }
        
        return scripts
    
    def _generate_anchor_phrases(self, drivers: List[Dict[str, Any]], avatar_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Gera frases de ancoragem para cada driver"""
        
        anchor_phrases = {}
        
        for driver in drivers:
            driver_name = driver.get('nome', 'Driver')
            frases = driver.get('frases_ancoragem', [])
            
            if frases:
                anchor_phrases[driver_name] = frases
            else:
                # Frases padrão
                anchor_phrases[driver_name] = [
                    f"Este é o momento de ativar {driver_name}",
                    f"Você sente o impacto de {driver_name}",
                    f"Agora {driver_name} faz sentido para você"
                ]
        
        return anchor_phrases
    
    def _calculate_personalization_level(self, drivers: List[Dict[str, Any]]) -> str:
        """Calcula nível de personalização dos drivers"""
        
        if not drivers:
            return "Baixo"
        
        # Verifica se tem histórias específicas
        has_stories = sum(1 for d in drivers if len(d.get('roteiro_ativacao', {}).get('historia_analogia', '')) > 100)
        
        # Verifica se tem frases de ancoragem
        has_anchors = sum(1 for d in drivers if len(d.get('frases_ancoragem', [])) >= 3)
        
        personalization_score = (has_stories + has_anchors) / (len(drivers) * 2)
        
        if personalization_score >= 0.8:
            return "Alto"
        elif personalization_score >= 0.5:
            return "Médio"
        else:
            return "Baixo"
    
    def _generate_fallback_drivers_system(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sistema de drivers básico como fallback"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        fallback_drivers = self._create_basic_drivers(context_data)
        
        return {
            'drivers_customizados': fallback_drivers,
            'roteiros_ativacao': {
                driver['nome']: {
                    'abertura': driver['roteiro_ativacao']['pergunta_abertura'],
                    'desenvolvimento': driver['roteiro_ativacao']['historia_analogia'],
                    'fechamento': driver['roteiro_ativacao']['comando_acao'],
                    'tempo_estimado': '3-5 minutos'
                } for driver in fallback_drivers
            },
            'frases_ancoragem': {
                driver['nome']: driver['frases_ancoragem'] for driver in fallback_drivers
            },
            'validation_status': 'FALLBACK_VALID',
            'generation_timestamp': time.time(),
            'fallback_mode': True
        }

# Instância global
mental_drivers_architect = MentalDriversArchitect()