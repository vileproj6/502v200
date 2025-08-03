#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Visual Proofs Generator
Gerador de Provas Visuais Instantâneas - Sistema Completo dos Anexos
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

class VisualProofsGenerator:
    """Gerador de Provas Visuais Instantâneas - Sistema Completo dos Anexos"""
    
    def __init__(self):
        """Inicializa o gerador de provas visuais"""
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
        
        self.proof_types = self._load_proof_types()
        self.visual_elements = self._load_visual_elements()
        self.proof_categories = self._load_proof_categories()
        self.arsenal_techniques = self._load_arsenal_techniques()
        self.complete_arsenal = self._load_complete_arsenal_from_attachments()
        
        logger.info("Visual Proofs Generator inicializado com sistema completo dos anexos")
    
    def _load_complete_arsenal_from_attachments(self) -> Dict[str, Dict[str, Any]]:
        """Carrega arsenal completo das provas visuais dos anexos"""
        return {
            'destruidoras_objecao': {
                'contra_tempo': {
                    'ampulheta_dinheiro': {
                        'nome': 'Ampulheta do Tempo Perdido',
                        'objetivo': 'Mostrar que tempo "perdido" é dinheiro escapando',
                        'descricao': 'Ampulheta com dinheiro (moedas) caindo em vez de areia',
                        'analogia': 'Assim como o dinheiro escapa da ampulheta → Oportunidades escapam da sua vida',
                        'materiais': ['Ampulheta grande', 'Moedas douradas', 'Calculadora'],
                        'roteiro': {
                            'setup': 'Apresentar ampulheta cheia de moedas',
                            'execucao': [
                                'Virar ampulheta e mostrar moedas caindo',
                                'Contar quantas moedas caem em 1 minuto',
                                'Multiplicar por horas/dias/meses de procrastinação'
                            ],
                            'climax': 'Revelar que cada moeda representa R$ 100 de oportunidade perdida'
                        }
                    },
                    'celular_distracao': {
                        'nome': 'Celular com 47 Apps de Distração',
                        'objetivo': 'Mostrar como tempo é desperdiçado inconscientemente',
                        'descricao': 'Demonstração de tempo gasto em apps vs tempo produtivo',
                        'materiais': ['Smartphone', 'Cronômetro', 'Lista de apps']
                    }
                },
                'contra_dinheiro': {
                    'calculadora_gastos': {
                        'nome': 'Calculadora de Gastos Invisíveis',
                        'objetivo': 'Revelar onde o dinheiro realmente vai',
                        'descricao': 'Cálculo em tempo real de gastos "pequenos" que viram fortunas',
                        'materiais': ['Calculadora', 'Lista de gastos', 'Projeção anual']
                    },
                    'cofrinho_furado': {
                        'nome': 'Cofrinho Furado vs Investimento',
                        'objetivo': 'Contrastar poupança passiva com investimento ativo',
                        'descricao': 'Dois cofrinhos: um furado (gastos) e um sólido (investimentos)',
                        'materiais': ['2 cofrinhos', 'Moedas', 'Furos visíveis']
                    }
                }
            },
            'criadoras_urgencia': {
                'vela_oportunidade': {
                    'nome': 'Vela da Oportunidade',
                    'objetivo': 'Criar pressão temporal visual',
                    'descricao': 'Vela acesa que representa janela de oportunidade',
                    'analogia': 'Assim como a vela se apaga → Oportunidades têm prazo de validade',
                    'materiais': ['Vela grande', 'Isqueiro', 'Prato de segurança'],
                    'roteiro': {
                        'setup': 'Acender vela no início da apresentação',
                        'execucao': [
                            'Mostrar vela queimando durante apresentação',
                            'Apontar como diminuiu durante o tempo',
                            'Soprar vela no momento da oferta'
                        ],
                        'climax': 'Vela apagada = oportunidade perdida para sempre'
                    }
                },
                'trem_partindo': {
                    'nome': 'Trem Partindo da Estação',
                    'objetivo': 'Urgência de embarcar antes que seja tarde',
                    'descricao': 'Simulação de trem partindo com últimas vagas',
                    'materiais': ['Som de trem', 'Cronômetro', 'Apito']
                }
            },
            'instaladoras_crenca': {
                'metamorfose_lagarta': {
                    'nome': 'Metamorfose da Lagarta',
                    'objetivo': 'Mostrar potencial de transformação',
                    'descricao': 'Demonstração visual da metamorfose lagarta → borboleta',
                    'analogia': 'Assim como a lagarta vira borboleta → Você pode se transformar completamente',
                    'materiais': ['Imagens HD', 'Objetos representativos', 'Casulo real (opcional)'],
                    'roteiro': {
                        'setup': 'Mostrar imagem/objeto de lagarta',
                        'execucao': [
                            'Mostrar lagarta (estado atual)',
                            'Explicar processo de metamorfose (método)',
                            'Revelar borboleta (resultado final)'
                        ],
                        'climax': 'Borboleta emergindo - transformação completa'
                    }
                },
                'semente_arvore': {
                    'nome': 'Semente → Árvore (Potencial)',
                    'objetivo': 'Demonstrar crescimento exponencial',
                    'descricao': 'Evolução de semente para árvore frondosa',
                    'materiais': ['Semente real', 'Imagens de crescimento', 'Vaso com terra']
                }
            },
            'provas_metodo': {
                'quebra_cabeca_metodo': {
                    'nome': 'Quebra-cabeça do Método',
                    'objetivo': 'Demonstrar sistema vs caos',
                    'descricao': 'Quebra-cabeça montado com/sem imagem de referência',
                    'analogia': 'Assim como o quebra-cabeça precisa da imagem → Você precisa do método',
                    'materiais': ['2 quebra-cabeças iguais', 'Cronômetro', 'Mesa visível'],
                    'roteiro': {
                        'setup': 'Duas pessoas, dois quebra-cabeças iguais',
                        'execucao': [
                            'Uma pessoa monta com imagem, outra sem',
                            'Mostrar diferença de velocidade e precisão',
                            'Revelar resultado final de cada um'
                        ],
                        'climax': 'Diferença gritante entre ter método vs tentar na sorte'
                    }
                },
                'receita_ingredientes': {
                    'nome': 'Receita vs Ingredientes Soltos',
                    'objetivo': 'Mostrar importância da sequência e método',
                    'descricao': 'Comparação entre seguir receita e improvisar',
                    'materiais': ['Ingredientes', 'Receita impressa', 'Resultado final']
                }
            }
        }
    
    def _load_proof_types(self) -> Dict[str, Dict[str, Any]]:
        """Carrega tipos de provas visuais"""
        return {
            'destruidoras_objecao': {
                'nome': 'Destruidoras de Objeção',
                'objetivo': 'Neutralizar objeções específicas',
                'impacto': 'Alto',
                'facilidade': 'Média',
                'arsenal': ['Ampulheta com dinheiro', 'Calculadora de gastos', 'GPS vs mapa rasgado']
            },
            'criadoras_urgencia': {
                'nome': 'Criadoras de Urgência',
                'objetivo': 'Instalar pressão temporal',
                'impacto': 'Alto',
                'facilidade': 'Alta',
                'arsenal': ['Vela se apagando', 'Trem partindo', 'Porta se fechando', 'Maré subindo']
            },
            'instaladoras_crenca': {
                'nome': 'Instaladoras de Crença',
                'objetivo': 'Transformar mentalidade',
                'impacto': 'Alto',
                'facilidade': 'Média',
                'arsenal': ['Lagarta → Borboleta', 'Semente → Árvore', 'Carvão → Diamante']
            },
            'provas_metodo': {
                'nome': 'Provas de Método',
                'objetivo': 'Demonstrar sistema vs caos',
                'impacto': 'Alto',
                'facilidade': 'Média',
                'arsenal': ['Quebra-cabeça com/sem imagem', 'Receita vs ingredientes', 'Orquestra com/sem maestro']
            }
        }
    
    def _load_proof_categories(self) -> Dict[str, List[str]]:
        """Carrega categorias de provas dos anexos"""
        return {
            'contra_tempo': [
                'Ampulheta com dinheiro escapando',
                'Celular com 47 apps de distração',
                'Agenda com 80% de "nada importante"'
            ],
            'contra_dinheiro': [
                'Calculadora de gastos invisíveis',
                'Cofrinho furado vs investimento',
                'Pilha de "economias" que são perdas'
            ],
            'contra_tentativas': [
                'GPS vs mapa rasgado',
                'Chave certa vs molho de erradas',
                'Receita completa vs ingredientes soltos'
            ],
            'criadoras_urgencia': [
                'Vela se apagando',
                'Trem partindo da estação',
                'Porta se fechando automaticamente',
                'Maré subindo em castelo de areia'
            ],
            'instaladoras_crenca': [
                'Lagarta → Borboleta (metamorfose)',
                'Semente → Árvore (potencial)',
                'Carvão → Diamante (pressão certa)',
                'Água → Gelo → Vapor (estados)'
            ],
            'provas_metodo': [
                'Quebra-cabeça com/sem imagem',
                'Ingredientes vs receita pronta',
                'Ferramentas vs blueprint',
                'Orquestra com/sem maestro'
            ]
        }
    
    def _load_arsenal_techniques(self) -> Dict[str, Dict[str, Any]]:
        """Carrega técnicas do arsenal dos anexos"""
        return {
            'elementos_sensoriais': {
                'som': 'O que faz barulho?',
                'visual': 'O que muda de cor/forma?',
                'tatil': 'O que podem tocar/sentir?',
                'olfativo': 'Que cheiro evoca memória?'
            },
            'fisica_cotidiano': {
                'gravidade': 'Queda, peso',
                'temperatura': 'Calor/frio',
                'pressao': 'Expansão/compressão',
                'tempo': 'Deterioração/crescimento'
            },
            'emocoes_primarias': {
                'medo': 'Perda, escuridão',
                'desejo': 'Brilho, atração',
                'surpresa': 'Revelação',
                'alivio': 'Solução'
            }
        }
    
    def _load_visual_elements(self) -> Dict[str, List[str]]:
        """Carrega elementos visuais disponíveis"""
        return {
            'graficos': ['Barras', 'Linhas', 'Pizza', 'Área', 'Dispersão'],
            'comparacoes': ['Lado a lado', 'Sobreposição', 'Timeline', 'Tabela'],
            'depoimentos': ['Vídeo', 'Texto', 'Áudio', 'Screenshot'],
            'demonstracoes': ['Screencast', 'Fotos', 'Infográfico', 'Animação'],
            'dados': ['Números', 'Percentuais', 'Valores', 'Métricas']
        }
    
    def generate_complete_proofs_system(
        self, 
        concepts_to_prove: List[str], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gera sistema completo de provas visuais baseado nos anexos"""
        
        # Validação crítica de entrada
        if not concepts_to_prove:
            logger.error("❌ Nenhum conceito para provar")
            # Gera conceitos básicos em vez de falhar
            segmento = context_data.get('segmento', 'negócios')
            concepts_to_prove = [
                f"Eficácia comprovada em {segmento}",
                f"Resultados mensuráveis em {segmento}",
                f"Metodologia diferenciada para {segmento}",
                f"Transformação real de profissionais",
                f"Superioridade competitiva demonstrada"
            ]
            logger.warning("⚠️ Usando conceitos básicos para provas visuais")
        
        if not context_data.get('segmento'):
            logger.error("❌ Segmento não informado")
            raise ValueError("PROVAS VISUAIS FALHARAM: Segmento obrigatório")
        
        try:
            logger.info(f"🎭 Gerando provas visuais para {len(concepts_to_prove)} conceitos")
            
            # Salva dados de entrada imediatamente
            salvar_etapa("provas_entrada", {
                "concepts_to_prove": concepts_to_prove,
                "avatar_data": avatar_data,
                "context_data": context_data
            }, categoria="provas_visuais")
            
            # FASE 1: ESCANEAMENTO PROFUNDO (dos anexos)
            scanned_concepts = self._deep_scan_concepts(concepts_to_prove, avatar_data, context_data)
            
            # FASE 2: CRIAÇÃO MASSIVA DE PROVIS (dos anexos)
            visual_proofs = self._create_massive_provis(scanned_concepts, avatar_data, context_data)
            
            # FASE 3: ORQUESTRAÇÃO ESTRATÉGICA (dos anexos)
            orchestrated_proofs = self._orchestrate_proofs_strategically(visual_proofs, context_data)
            
            # Salva provas visuais finais
            salvar_etapa("provas_finais", orchestrated_proofs, categoria="provas_visuais")
            
            logger.info(f"✅ {len(orchestrated_proofs)} provas visuais geradas com sistema completo dos anexos")
            return orchestrated_proofs
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar provas visuais: {str(e)}")
            salvar_erro("provas_sistema", e, contexto={"segmento": context_data.get('segmento')})
            
            # Gera provas básicas como último recurso
            return self._get_default_visual_proofs(context_data)
    
    def _deep_scan_concepts(self, concepts: List[str], avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """FASE 1: Escaneamento profundo dos anexos"""
        
        scanned = {
            'conceitos_abstratos': [],
            'objecoes_destruir': [],
            'principios_metodo': [],
            'transformacoes_prometidas': [],
            'crencas_quebrar': [],
            'urgencias_criar': []
        }
        
        # Extrai conceitos abstratos
        for concept in concepts:
            if any(word in concept.lower() for word in ['eficácia', 'metodologia', 'sistema']):
                scanned['principios_metodo'].append(concept)
            elif any(word in concept.lower() for word in ['transformação', 'resultado', 'mudança']):
                scanned['transformacoes_prometidas'].append(concept)
            elif any(word in concept.lower() for word in ['tempo', 'urgente', 'rápido']):
                scanned['urgencias_criar'].append(concept)
            else:
                scanned['conceitos_abstratos'].append(concept)
        
        # Adiciona objeções do avatar
        objecoes = avatar_data.get('objecoes_reais', [])
        scanned['objecoes_destruir'].extend(objecoes)
        
        # Categoriza por prioridade
        scanned['prioridade_critica'] = scanned['objecoes_destruir'][:3]
        scanned['prioridade_alta'] = scanned['transformacoes_prometidas'][:3]
        scanned['prioridade_media'] = scanned['principios_metodo'][:3]
        
        return scanned
    
    def _create_massive_provis(self, scanned_concepts: Dict[str, Any], avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FASE 2: Criação massiva de PROVIs dos anexos"""
        
        provis = []
        provi_counter = 1
        
        # Cria PROVIs para conceitos críticos
        for concept in scanned_concepts.get('prioridade_critica', []):
            provi = self._create_complete_provi(concept, 'destruidoras_objecao', provi_counter, avatar_data, context_data)
            provis.append(provi)
            provi_counter += 1
        
        # Cria PROVIs para transformações
        for concept in scanned_concepts.get('prioridade_alta', []):
            provi = self._create_complete_provi(concept, 'instaladoras_crenca', provi_counter, avatar_data, context_data)
            provis.append(provi)
            provi_counter += 1
        
        # Cria PROVIs para método
        for concept in scanned_concepts.get('prioridade_media', []):
            provi = self._create_complete_provi(concept, 'provas_metodo', provi_counter, avatar_data, context_data)
            provis.append(provi)
            provi_counter += 1
        
        # Adiciona PROVIs de urgência
        urgency_provi = self._create_urgency_provi(provi_counter, context_data)
        provis.append(urgency_provi)
        
        return provis
    
    def _create_complete_provi(self, concept: str, category: str, number: int, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria PROVI completo baseado no formato dos anexos"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        # Seleciona experimento baseado na categoria
        experiment = self._select_experiment_from_arsenal(category, concept)
        
        provi = {
            'nome': f'PROVI #{number}: {experiment["nome"]}',
            'conceito_alvo': concept,
            'categoria': category,
            'prioridade': 'Crítica' if number <= 3 else 'Alta' if number <= 6 else 'Média',
            'momento_ideal': self._determine_ideal_moment(category),
            
            'objetivo_psicologico': experiment['objetivo'],
            'experimento_escolhido': experiment['descricao'],
            'analogia_perfeita': experiment['analogia'],
            
            'roteiro_completo': {
                'setup': {
                    'duracao': '30s',
                    'acao': experiment['setup'],
                     'expectativa': f'Criar expectativa sobre {concept}'
                 },
                 'execucao': {
                     'duracao': '30-90s',
                     'passo_1': experiment.get('roteiro', {}).get('execucao', ['Primeiro passo da demonstração'])[0] if experiment.get('roteiro', {}).get('execucao') else 'Primeiro passo da demonstração',
                     'passo_2': experiment.get('roteiro', {}).get('execucao', ['', 'Segundo passo da demonstração'])[1] if len(experiment.get('roteiro', {}).get('execucao', [])) > 1 else 'Segundo passo da demonstração',
                     'passo_3': experiment.get('roteiro', {}).get('execucao', ['', '', 'Terceiro passo da demonstração'])[2] if len(experiment.get('roteiro', {}).get('execucao', [])) > 2 else 'Terceiro passo da demonstração'
                 },
                 'climax': {
                     'duracao': '15s',
                     'momento_aha': experiment.get('roteiro', {}).get('climax', f'Revelação sobre {concept}'),
                     'reacao_esperada': 'Compreensão súbita e impacto emocional'
                 },
                 'bridge': {
                     'duracao': '30s',
                     'conexao_vida': f'Assim como {experiment["nome"].lower()}, em {segmento}...',
                     'pergunta_retorica': f'Você quer continuar {concept.lower()} ou está pronto para mudar?',
                     'comando_subliminar': f'Aceite a transformação em {segmento}'
                 }
             },
             
             'materiais': experiment.get('materiais', ['Material visual', 'Objeto demonstrativo', 'Suporte técnico']),
             
             'variacoes': {
                 'online': f'Versão digital da demonstração {experiment["nome"]}',
                 'grande_publico': f'Versão amplificada para grandes audiências',
                 'intimista': f'Versão simplificada para grupos pequenos'
             },
             
             'gestao_riscos': {
                 'pode_falhar_se': [f'Material falhar', f'Audiência não conectar', f'Timing inadequado'],
                 'plano_b': f'Usar analogia verbal se material falhar',
                 'transformar_erro': f'Usar falha como exemplo de imprevisibilidade'
             },
             
             'frases_impacto': {
                 'durante': f'Vejam como {concept.lower()} funciona na prática...',
                 'revelacao': f'Isso é exatamente o que acontece com {concept}',
                 'ancoragem': f'{concept} não é teoria, é realidade demonstrável'
             },
             
             'dramatizacao_extra': f'Elementos teatrais para amplificar impacto de {concept}',
             
             # Elementos específicos dos anexos
             'elementos_sensoriais': {
                 'som': f'Som que reforça {concept}',
                 'visual': f'Mudança visual que representa {concept}',
                 'tatil': f'Elemento tátil para {concept}',
                 'olfativo': f'Aroma que evoca memória de {concept}'
             },
             
             'fisica_cotidiano': {
                 'gravidade': f'Como gravidade se relaciona com {concept}',
                 'temperatura': f'Variação de temperatura para demonstrar {concept}',
                 'pressao': f'Pressão como metáfora para {concept}',
                 'tempo': f'Elemento temporal em {concept}'
             }
                    'expectativa': f'Criar expectativa sobre {concept}'
                },
                'execucao': {
                    'duracao': '30-90s',
                    'passo_1': experiment['execucao']['passo_1'],
                    'passo_2': experiment['execucao']['passo_2'],
                    'passo_3': experiment['execucao']['passo_3']
                },
                'climax': {
                    'duracao': '15s',
                    'momento_aha': experiment['climax'],
                    'reacao_esperada': 'Compreensão súbita e impacto emocional'
                },
                'bridge': {
                    'duracao': '30s',
                    'conexao_vida': f'Assim como {experiment["nome"].lower()}, em {segmento}...',
                    'pergunta_retorica': experiment['pergunta'],
                    'comando_subliminar': experiment['comando']
                }
            },
            
            'materiais': experiment['materiais'],
            
            'variacoes': {
                'online': experiment['variacoes']['online'],
                'grande_publico': experiment['variacoes']['grande_publico'],
                'intimista': experiment['variacoes']['intimista']
            },
            
            'gestao_riscos': {
                'pode_falhar_se': experiment['riscos']['pode_falhar'],
                'plano_b': experiment['riscos']['plano_b'],
                'transformar_erro': experiment['riscos']['transformar_erro']
            },
            
            'frases_impacto': {
                'durante': experiment['frases']['durante'],
                'revelacao': experiment['frases']['revelacao'],
                'ancoragem': experiment['frases']['ancoragem']
            },
            
            'dramatizacao_extra': experiment.get('dramatizacao', 'Elementos teatrais para amplificar impacto')
        }
        
        return provi
    
    def _select_experiment_from_complete_arsenal(self, category: str, concept: str, segmento: str) -> Dict[str, Any]:
        """Seleciona experimento do arsenal completo dos anexos"""
        
        # Mapeia categoria para arsenal específico
        if category == 'destruidoras_objecao':
            if 'tempo' in concept.lower():
                return self.complete_arsenal['destruidoras_objecao']['contra_tempo']['ampulheta_dinheiro']
            elif 'dinheiro' in concept.lower() or 'investimento' in concept.lower():
                return self.complete_arsenal['destruidoras_objecao']['contra_dinheiro']['calculadora_gastos']
            else:
                return self.complete_arsenal['destruidoras_objecao']['contra_tempo']['ampulheta_dinheiro']
        
        elif category == 'criadoras_urgencia':
            return self.complete_arsenal['criadoras_urgencia']['vela_oportunidade']
        
        elif category == 'instaladoras_crenca':
            return self.complete_arsenal['instaladoras_crenca']['metamorfose_lagarta']
        
        elif category == 'provas_metodo':
            return self.complete_arsenal['provas_metodo']['quebra_cabeca_metodo']
        
        else:
            # Fallback para experimento genérico
            return {
                'nome': f'Demonstração {concept}',
                'objetivo': f'Provar {concept} visualmente',
                'descricao': f'Demonstração visual específica para {concept} em {segmento}',
                'materiais': ['Material visual', 'Objeto demonstrativo'],
                'roteiro': {
                    'setup': f'Preparar demonstração de {concept}',
                    'execucao': [f'Mostrar {concept} na prática'],
                    'climax': f'Revelação sobre {concept}'
                }
            }
    
    def _select_experiment_from_arsenal(self, category: str, concept: str) -> Dict[str, Any]:
        """Seleciona experimento do arsenal dos anexos"""
        
        # Arsenal baseado nos anexos
        arsenal = {
            'destruidoras_objecao': {
                'nome': 'Ampulheta do Tempo Perdido',
                'objetivo': 'Mostrar que tempo "perdido" é dinheiro escapando',
                'descricao': 'Ampulheta com dinheiro (moedas) caindo em vez de areia',
                'analogia': 'Assim como o dinheiro escapa da ampulheta → Oportunidades escapam da sua vida',
                'setup': 'Apresentar ampulheta cheia de moedas',
                'execucao': {
                    'passo_1': 'Virar ampulheta e mostrar moedas caindo',
                    'passo_2': 'Contar quantas moedas caem em 1 minuto',
                    'passo_3': 'Multiplicar por horas/dias/meses de procrastinação'
                },
                'climax': 'Revelar que cada moeda representa R$ 100 de oportunidade perdida',
                'pergunta': 'Quantas moedas você já deixou cair?',
                'comando': 'Pare de deixar seu futuro escorrer pelos dedos',
                'materiais': ['Ampulheta grande', 'Moedas douradas', 'Calculadora'],
                'variacoes': {
                    'online': 'Ampulheta digital com contador de dinheiro',
                    'grande_publico': 'Ampulheta gigante no palco',
                    'intimista': 'Ampulheta pequena na mesa'
                },
                'riscos': {
                    'pode_falhar': 'Ampulheta emperrar',
                    'plano_b': 'Cronômetro com som de moedas caindo',
                    'transformar_erro': 'Usar falha como exemplo de imprevisibilidade'
                },
                'frases': {
                    'durante': 'Olhem como o tempo escorre...',
                    'revelacao': 'Cada segundo que passou = R$ X perdidos',
                    'ancoragem': 'Tempo não volta, oportunidade não espera'
                }
            },
            'criadoras_urgencia': {
                'nome': 'Vela da Oportunidade',
                'objetivo': 'Criar pressão temporal visual',
                'descricao': 'Vela acesa que representa janela de oportunidade',
                'analogia': 'Assim como a vela se apaga → Oportunidades têm prazo de validade',
                'setup': 'Acender vela no início da apresentação',
                'execucao': {
                    'passo_1': 'Mostrar vela queimando durante apresentação',
                    'passo_2': 'Apontar como diminuiu durante o tempo',
                    'passo_3': 'Soprar vela no momento da oferta'
                },
                'climax': 'Vela apagada = oportunidade perdida para sempre',
                'pergunta': 'Quantas velas você já deixou apagar?',
                'comando': 'Aja antes que sua vela se apague',
                'materiais': ['Vela grande', 'Isqueiro', 'Prato de segurança'],
                'variacoes': {
                    'online': 'Timer visual com chama diminuindo',
                    'grande_publico': 'Múltiplas velas no palco',
                    'intimista': 'Vela aromática na mesa'
                },
                'riscos': {
                    'pode_falhar': 'Vela apagar antes da hora',
                    'plano_b': 'Cronômetro regressivo',
                    'transformar_erro': 'Usar como exemplo de imprevisibilidade da vida'
                },
                'frases': {
                    'durante': 'Vejam como o tempo está passando...',
                    'revelacao': 'Quando a chama se apaga, acabou',
                    'ancoragem': 'Oportunidades são como velas: têm prazo de validade'
                }
            },
            'instaladoras_crenca': {
                'nome': 'Metamorfose da Lagarta',
                'objetivo': 'Mostrar potencial de transformação',
                'descricao': 'Demonstração visual da metamorfose lagarta → borboleta',
                'analogia': 'Assim como a lagarta vira borboleta → Você pode se transformar completamente',
                'setup': 'Mostrar imagem/objeto de lagarta',
                'execucao': {
                    'passo_1': 'Mostrar lagarta (estado atual)',
                    'passo_2': 'Explicar processo de metamorfose (método)',
                    'passo_3': 'Revelar borboleta (resultado final)'
                },
                'climax': 'Borboleta emergindo - transformação completa',
                'pergunta': 'Você quer continuar rastejando ou está pronto para voar?',
                'comando': 'Aceite sua metamorfose',
                'materiais': ['Imagens HD', 'Objetos representativos', 'Casulo real (opcional)'],
                'variacoes': {
                    'online': 'Animação da metamorfose',
                    'grande_publico': 'Vídeo em telão',
                    'intimista': 'Objetos físicos pequenos'
                },
                'riscos': {
                    'pode_falhar': 'Analogia não conectar',
                    'plano_b': 'Usar semente → árvore',
                    'transformar_erro': 'Falar sobre resistência natural à mudança'
                },
                'frases': {
                    'durante': 'A natureza nos ensina sobre transformação...',
                    'revelacao': 'Isso é o que acontece quando você aceita mudar',
                    'ancoragem': 'Metamorfose não é opcional, é inevitável'
                }
            },
            'provas_metodo': {
                'nome': 'Quebra-cabeça do Método',
                'objetivo': 'Demonstrar sistema vs caos',
                'descricao': 'Quebra-cabeça montado com/sem imagem de referência',
                'analogia': 'Assim como o quebra-cabeça precisa da imagem → Você precisa do método',
                'setup': 'Duas pessoas, dois quebra-cabeças iguais',
                'execucao': {
                    'passo_1': 'Uma pessoa monta com imagem, outra sem',
                    'passo_2': 'Mostrar diferença de velocidade e precisão',
                    'passo_3': 'Revelar resultado final de cada um'
                },
                'climax': 'Diferença gritante entre ter método vs tentar na sorte',
                'pergunta': 'Você quer montar sua vida com ou sem a imagem?',
                'comando': 'Pare de tentar na sorte, use o método',
                'materiais': ['2 quebra-cabeças iguais', 'Cronômetro', 'Mesa visível'],
                'variacoes': {
                    'online': 'Simulação digital do quebra-cabeça',
                    'grande_publico': 'Quebra-cabeça gigante no palco',
                    'intimista': 'Quebra-cabeça pequeno na mesa'
                },
                'riscos': {
                    'pode_falhar': 'Pessoa sem método montar rápido por sorte',
                    'plano_b': 'Usar receita de bolo vs ingredientes soltos',
                    'transformar_erro': 'Mostrar que sorte não é sustentável'
                },
                'frases': {
                    'durante': 'Vejam a diferença...',
                    'revelacao': 'Método sempre vence tentativa',
                    'ancoragem': 'Sucesso não é sorte, é sistema'
                }
            }
        }
        
        return arsenal.get(category, arsenal['destruidoras_objecao'])
    
    def _orchestrate_proofs_strategically(self, visual_proofs: List[Dict[str, Any]], context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FASE 3: Orquestração estratégica dos anexos"""
        
        # Ordena por prioridade e momento ideal
        orchestrated = sorted(visual_proofs, key=lambda x: (
            0 if x['prioridade'] == 'Crítica' else 1 if x['prioridade'] == 'Alta' else 2,
            x['momento_ideal']
        ))
        
        # Adiciona sequência otimizada
        for i, proof in enumerate(orchestrated):
            proof['sequencia_otimizada'] = {
                'posicao': i + 1,
                'momento_apresentacao': self._calculate_presentation_moment(i, len(orchestrated)),
                'conexao_anterior': self._create_connection_to_previous(i, orchestrated),
                'preparacao_proxima': self._create_preparation_for_next(i, orchestrated)
            }
            
            # Adiciona narrativa conectora
            proof['narrativa_conectora'] = self._create_connecting_narrative(proof, context_data)
        
        # Adiciona kit de implementação
        orchestrated.append(self._create_implementation_kit(orchestrated, context_data))
        
        return orchestrated
    
    def _create_urgency_provi(self, number: int, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria PROVI específico de urgência"""
        
        return {
            'nome': f'PROVI #{number}: Vela da Oportunidade',
            'conceito_alvo': 'Urgência temporal',
            'categoria': 'criadoras_urgencia',
            'prioridade': 'Crítica',
            'momento_ideal': 'Pré-fechamento',
            'objetivo_psicologico': 'Instalar pressão temporal visceral',
            'experimento_escolhido': 'Vela acesa que representa janela de oportunidade',
            'roteiro_completo': {
                'setup': {
                    'duracao': '30s',
                    'acao': 'Acender vela no início da apresentação',
                    'expectativa': 'Criar consciência temporal'
                },
                'execucao': {
                    'duracao': '60s',
                    'passo_1': 'Mostrar vela queimando durante apresentação',
                    'passo_2': 'Apontar como diminuiu durante o tempo',
                    'passo_3': 'Soprar vela no momento da oferta'
                },
                'climax': {
                    'duracao': '15s',
                    'momento_aha': 'Vela apagada = oportunidade perdida para sempre',
                    'reacao_esperada': 'Urgência visceral'
                }
            },
            'materiais': ['Vela grande', 'Isqueiro', 'Prato de segurança'],
            'frases_impacto': {
                'durante': 'Vejam como o tempo está passando...',
                'revelacao': 'Quando a chama se apaga, acabou',
                'ancoragem': 'Oportunidades são como velas: têm prazo de validade'
            }
        }
    
    def _determine_ideal_moment(self, category: str) -> str:
        """Determina momento ideal baseado na categoria"""
        moments = {
            'destruidoras_objecao': 'Durante objeções',
            'criadoras_urgencia': 'Pré-fechamento',
            'instaladoras_crenca': 'Desenvolvimento',
            'provas_metodo': 'Apresentação do método'
        }
        return moments.get(category, 'Desenvolvimento')
    
    def _calculate_presentation_moment(self, index: int, total: int) -> str:
        """Calcula momento de apresentação"""
        percentage = (index + 1) / total
        
        if percentage <= 0.3:
            return 'Abertura (primeiros 30%)'
        elif percentage <= 0.7:
            return 'Desenvolvimento (30-70%)'
        else:
            return 'Fechamento (últimos 30%)'
    
    def _create_connection_to_previous(self, index: int, proofs: List[Dict[str, Any]]) -> str:
        """Cria conexão com PROVI anterior"""
        if index == 0:
            return 'Primeira demonstração - criar impacto inicial'
        
        previous_proof = proofs[index - 1]
        return f'Conectar com {previous_proof["nome"]} através de callback'
    
    def _create_preparation_for_next(self, index: int, proofs: List[Dict[str, Any]]) -> str:
        """Cria preparação para próximo PROVI"""
        if index >= len(proofs) - 1:
            return 'Última demonstração - preparar para oferta'
        
        next_proof = proofs[index + 1]
        return f'Preparar terreno para {next_proof["nome"]}'
    
    def _create_connecting_narrative(self, proof: Dict[str, Any], context_data: Dict[str, Any]) -> str:
        """Cria narrativa conectora"""
        return f'Esta demonstração conecta com {context_data.get("segmento", "seu negócio")} porque mostra a importância de {proof["conceito_alvo"]}'
    
    def _create_implementation_kit(self, proofs: List[Dict[str, Any]], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria kit de implementação dos anexos"""
        
        return {
            'tipo': 'kit_implementacao',
            'nome': 'KIT DE IMPLEMENTAÇÃO COMPLETO',
            'checklist_preparacao': [
                'Listar todos os materiais necessários',
                'Ensaiar cada demonstração 3x',
                'Preparar planos B para cada PROVI',
                'Testar equipamentos e backup'
            ],
            'timeline_execucao': [
                'Semana -2: Comprar materiais',
                'Semana -1: Ensaios completos',
                'Dia -1: Setup e teste final',
                'Dia 0: Execução'
            ],
            'script_transicoes': [
                'Entre PROVIs: "Assim como vocês viram..."',
                'Para oferta: "Agora que vocês entenderam..."',
                'Pós-demonstração: "Quem aqui se identificou?"'
            ],
            'plano_contingencia_geral': [
                'Se material falhar: usar analogia verbal',
                'Se audiência resistir: intensificar dramatização',
                'Se tempo acabar: focar nos 3 PROVIs críticos'
            ],
            'metricas_sucesso': [
                'Silêncio absoluto durante demonstração',
                'Comentários emocionais pós-PROVI',
                'Perguntas sobre implementação',
                'Redução de objeções na oferta'
            ]
        }
            
    def _get_default_visual_proofs(self, context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retorna provas visuais padrão baseadas nos anexos"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return [
            {
                'nome': f'PROVI 1: Ampulheta do {segmento}',
                'conceito_alvo': f'Urgência temporal em {segmento}',
                'categoria': 'criadoras_urgencia',
                'experimento_escolhido': f'Demonstração de tempo perdido em {segmento}',
                'materiais': ['Ampulheta', 'Moedas', 'Calculadora'],
                'roteiro_completo': {
                    'setup': {'acao': 'Preparar ampulheta com moedas'},
                    'execucao': {'passo_1': 'Virar ampulheta', 'passo_2': 'Contar moedas caindo'},
                    'climax': {'momento_aha': 'Cada moeda = oportunidade perdida'}
                },
                'fallback_mode': True
            },
            {
                'nome': f'PROVI 2: Metamorfose {segmento}',
                'conceito_alvo': f'Transformação possível em {segmento}',
                'categoria': 'instaladoras_crenca',
                'experimento_escolhido': f'Demonstração de potencial em {segmento}',
                'materiais': ['Imagens de transformação', 'Objetos representativos'],
                'roteiro_completo': {
                    'setup': {'acao': 'Mostrar estado atual'},
                    'execucao': {'passo_1': 'Processo de mudança', 'passo_2': 'Resultado final'},
                    'climax': {'momento_aha': 'Transformação é possível'}
                },
                'fallback_mode': True
            }
        ]
            
# Instância global atualizada
visual_proofs_generator = VisualProofsGenerator()
    
    def _prioritize_concepts(self, concepts: List[str], avatar_data: Dict[str, Any]) -> List[str]:
        """Prioriza conceitos baseado no avatar"""
        
        # Dores têm prioridade alta
        dores = avatar_data.get('dores_viscerais', [])
        desejos = avatar_data.get('desejos_secretos', [])
        
        prioritized = []
        
        # Adiciona dores primeiro
        for concept in concepts:
            if any(concept.lower() in dor.lower() for dor in dores):
                prioritized.append(concept)
        
        # Adiciona desejos
        for concept in concepts:
            if concept not in prioritized and any(concept.lower() in desejo.lower() for desejo in desejos):
                prioritized.append(concept)
        
        # Adiciona conceitos restantes
        for concept in concepts:
            if concept not in prioritized:
                prioritized.append(concept)
        
        return prioritized
    
    def _generate_visual_proof_for_concept(
        self, 
        concept: str, 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any],
        proof_number: int
    ) -> Optional[Dict[str, Any]]:
        """Gera prova visual para um conceito específico"""
        
        try:
            segmento = context_data.get('segmento', 'negócios')
            
            # Seleciona tipo de prova mais adequado
            proof_type = self._select_best_proof_type(concept, avatar_data)
            
            # Gera prova usando IA
            prompt = f"""
Crie uma prova visual específica para o conceito: "{concept}"

SEGMENTO: {segmento}
TIPO DE PROVA: {proof_type['nome']}
OBJETIVO: {proof_type['objetivo']}

RETORNE APENAS JSON VÁLIDO:

```json
{{
  "nome": "PROVI {proof_number}: Nome específico da prova",
  "conceito_alvo": "{concept}",
  "tipo_prova": "{proof_type['nome']}",
  "experimento": "Descrição detalhada do experimento visual",
  "materiais": [
    "Material 1 específico",
    "Material 2 específico",
    "Material 3 específico"
  ],
  "roteiro_completo": {{
    "preparacao": "Como preparar a prova",
    "execucao": "Como executar a demonstração",
    "impacto_esperado": "Qual reação esperar"
  }},
  "metricas_sucesso": [
    "Métrica 1 de sucesso",
    "Métrica 2 de sucesso"
  ]
}}
```
"""
            
            response = ai_manager.generate_analysis(prompt, max_tokens=800)
            
            if response:
                clean_response = response.strip()
                if "```json" in clean_response:
                    start = clean_response.find("```json") + 7
                    end = clean_response.rfind("```")
                    clean_response = clean_response[start:end].strip()
                
                try:
                    proof = json.loads(clean_response)
                    logger.info(f"✅ Prova visual {proof_number} gerada com IA")
                    return proof
                except json.JSONDecodeError:
                    logger.warning(f"⚠️ IA retornou JSON inválido para prova {proof_number}")
            
            # Fallback para prova básica
            return self._create_basic_proof(concept, proof_type, proof_number, context_data)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar prova visual: {str(e)}")
            return self._create_basic_proof(concept, proof_type, proof_number, context_data)
    
    def _select_best_proof_type(self, concept: str, avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Seleciona melhor tipo de prova para o conceito"""
        
        concept_lower = concept.lower()
        
        # Mapeia conceitos para tipos de prova
        if any(word in concept_lower for word in ['resultado', 'crescimento', 'melhoria']):
            return self.proof_types['antes_depois']
        elif any(word in concept_lower for word in ['concorrente', 'melhor', 'superior']):
            return self.proof_types['comparacao_competitiva']
        elif any(word in concept_lower for word in ['tempo', 'rapidez', 'velocidade']):
            return self.proof_types['timeline_resultados']
        elif any(word in concept_lower for word in ['outros', 'clientes', 'pessoas']):
            return self.proof_types['social_proof_visual']
        else:
            return self.proof_types['demonstracao_processo']
    
    def _create_basic_proof(
        self, 
        concept: str, 
        proof_type: Dict[str, Any], 
        proof_number: int, 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria prova visual básica"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return {
            'nome': f'PROVI {proof_number}: {proof_type["nome"]} para {segmento}',
            'conceito_alvo': concept,
            'tipo_prova': proof_type['nome'],
            'experimento': f'Demonstração visual do conceito "{concept}" através de {proof_type["nome"].lower()} específica para {segmento}',
            'materiais': [
                'Gráficos comparativos',
                'Dados numéricos',
                'Screenshots de resultados',
                'Depoimentos visuais'
            ],
            'roteiro_completo': {
                'preparacao': f'Prepare materiais visuais que demonstrem {concept} no contexto de {segmento}',
                'execucao': f'Apresente a prova visual de forma clara e impactante',
                'impacto_esperado': 'Redução de ceticismo e aumento de confiança'
            },
            'metricas_sucesso': [
                'Redução de objeções relacionadas ao conceito',
                'Aumento de interesse e engajamento',
                'Aceleração do processo de decisão'
            ],
            'fallback_mode': True
        }
    
    def _get_default_visual_proofs(self, context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retorna provas visuais padrão como fallback"""
        
        segmento = context_data.get('segmento', 'negócios')
        
        return [
            {
                'nome': f'PROVI 1: Resultados Comprovados em {segmento}',
                'conceito_alvo': f'Eficácia da metodologia em {segmento}',
                'tipo_prova': 'Antes/Depois',
                'experimento': f'Comparação visual de resultados antes e depois da aplicação da metodologia em {segmento}',
                'materiais': ['Gráficos de crescimento', 'Dados de performance', 'Screenshots de métricas'],
                'roteiro_completo': {
                    'preparacao': 'Organize dados de clientes que aplicaram a metodologia',
                    'execucao': 'Mostre transformação clara com números específicos',
                    'impacto_esperado': 'Convencimento através de evidência visual'
                },
                'metricas_sucesso': ['Redução de ceticismo', 'Aumento de interesse']
            },
            {
                'nome': f'PROVI 2: Comparação com Mercado em {segmento}',
                'conceito_alvo': f'Superioridade da abordagem em {segmento}',
                'tipo_prova': 'Comparação Competitiva',
                'experimento': f'Comparação visual entre abordagem tradicional e metodologia específica para {segmento}',
                'materiais': ['Tabelas comparativas', 'Gráficos de performance', 'Benchmarks do setor'],
                'roteiro_completo': {
                    'preparacao': 'Colete dados de mercado e benchmarks',
                    'execucao': 'Apresente comparação lado a lado',
                    'impacto_esperado': 'Demonstração clara de vantagem competitiva'
                },
                'metricas_sucesso': ['Compreensão do diferencial', 'Justificativa de preço premium']
            },
            {
                'nome': f'PROVI 3: Depoimentos Visuais {segmento}',
                'conceito_alvo': f'Validação social no {segmento}',
                'tipo_prova': 'Prova Social Visual',
                'experimento': f'Compilação visual de depoimentos de profissionais de {segmento}',
                'materiais': ['Vídeos de depoimento', 'Screenshots de resultados', 'Fotos de clientes'],
                'roteiro_completo': {
                    'preparacao': 'Selecione melhores depoimentos com resultados',
                    'execucao': 'Apresente sequência de validações sociais',
                    'impacto_esperado': 'Redução de risco percebido'
                },
                'metricas_sucesso': ['Aumento de confiança', 'Redução de objeções']
            }
        ]

# Instância global
visual_proofs_generator = VisualProofsGenerator()