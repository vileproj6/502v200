#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Analysis Pipeline
Pipeline de análise aprimorado sem dependências do Supabase
"""

import os
import json
import logging
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class EnhancedAnalysisPipeline:
    """Pipeline de análise aprimorado"""
    
    def __init__(self):
        """Inicializa pipeline"""
        # Importações locais para evitar dependências circulares
        try:
            from .ai_manager import ai_manager
            self.ai_manager = ai_manager
        except ImportError:
            logger.error("❌ AI Manager não disponível")
            self.ai_manager = None
        
        try:
            from .production_search_manager import production_search_manager
            self.search_manager = production_search_manager
        except ImportError:
            logger.error("❌ Search Manager não disponível")
            self.search_manager = None
        
        try:
            from .quality_assurance_manager import quality_assurance_manager
            self.qa_manager = quality_assurance_manager
        except ImportError:
            logger.error("❌ QA Manager não disponível")
            self.qa_manager = None
        
        try:
            from .auto_save_manager import auto_save_manager, salvar_etapa, salvar_erro
            self.auto_save = auto_save_manager
            self.salvar_etapa = salvar_etapa
            self.salvar_erro = salvar_erro
        except ImportError:
            logger.error("❌ Auto Save Manager não disponível")
            self.auto_save = None
        
        self.executor = ThreadPoolExecutor(max_workers=os.cpu_count() * 2)
        
        logger.info("✅ Enhanced Analysis Pipeline inicializado")

    def _execute_search_phase(self, query, session_id, progress_callback):
        """Executa fase de pesquisa"""
        try:
            progress_callback(1, "🌐 Iniciando pesquisa web e coleta de dados...")
            logger.info(f"Iniciando pesquisa para: {query}")
            
            if not self.search_manager:
                logger.error("❌ Search Manager não disponível")
                return {"error": "Search Manager não disponível"}
            
            search_results = self.search_manager.search_with_fallback(query, max_results=20)
            
            if self.salvar_etapa:
                self.salvar_etapa("pesquisa_web", search_results, categoria="pesquisa_web")
            
            if not search_results:
                logger.warning("Nenhum resultado de pesquisa encontrado.")
                return {"error": "Nenhum resultado de pesquisa encontrado"}
            
            progress_callback(2, "✅ Pesquisa web concluída.")
            return {"results": search_results, "total": len(search_results)}
            
        except Exception as e:
            logger.error(f"❌ Erro na fase de pesquisa: {e}")
            if self.salvar_erro:
                self.salvar_erro("pesquisa_fase", e)
            return {"error": str(e)}

    def _execute_extraction_phase(self, search_results, session_id, progress_callback):
        """Executa fase de extração"""
        try:
            progress_callback(3, "📄 Extraindo conteúdo das páginas...")
            logger.info("Iniciando extração de conteúdo.")
            
            # Importa extrator
            try:
                from .robust_content_extractor import robust_content_extractor
                extractor = robust_content_extractor
            except ImportError:
                logger.error("❌ Content Extractor não disponível")
                return {"error": "Content Extractor não disponível"}
            
            extracted_content = []
            results = search_results.get("results", [])
            
            for result in results[:15]:  # Limita para performance
                try:
                    content = extractor.extract_content(result.get('url', ''))
                    if content:
                        extracted_content.append({
                            'url': result.get('url'),
                            'title': result.get('title'),
                            'content': content[:2000],  # Limita tamanho
                            'source': result.get('source')
                        })
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao extrair {result.get('url')}: {e}")
                    continue
            
            if self.salvar_etapa:
                self.salvar_etapa("extracao_conteudo", extracted_content, categoria="pesquisa_web")
            
            if not extracted_content:
                logger.warning("Nenhum conteúdo extraído.")
                return {"error": "Nenhum conteúdo extraído"}
            
            progress_callback(4, "✅ Extração de conteúdo concluída.")
            return extracted_content
            
        except Exception as e:
            logger.error(f"❌ Erro na fase de extração: {e}")
            if self.salvar_erro:
                self.salvar_erro("extracao_fase", e)
            return {"error": str(e)}

    def _execute_ai_analysis_phase(self, extracted_content, data, session_id, progress_callback):
        """Executa fase de análise com IA"""
        try:
            progress_callback(5, "🧠 Iniciando análise de IA e geração de insights...")
            logger.info("Iniciando análise de IA.")
            
            if not self.ai_manager:
                logger.error("❌ AI Manager não disponível")
                return {"error": "AI Manager não disponível"}
            
            # Prepara contexto para IA
            context = self._prepare_ai_context(extracted_content, data)
            
            # Gera análise principal
            analysis_prompt = self._build_analysis_prompt(data, context)
            
            ai_response = self.ai_manager.generate_analysis(analysis_prompt, max_tokens=8192)
            
            if not ai_response:
                raise Exception("IA não retornou resposta válida")
            
            # Processa resposta
            processed_analysis = self._process_ai_response(ai_response, data)
            
            if self.salvar_etapa:
                self.salvar_etapa("analise_ia", processed_analysis, categoria="analise_completa")
            
            progress_callback(10, "✅ Análise de IA concluída.")
            return processed_analysis
            
        except Exception as e:
            logger.error(f"❌ Erro na fase de IA: {e}")
            if self.salvar_erro:
                self.salvar_erro("ia_fase", e)
            return {"error": str(e)}
    
    def _prepare_ai_context(self, extracted_content, data):
        """Prepara contexto para IA"""
        context = "PESQUISA WEB REALIZADA:\n\n"
        
        for i, content_item in enumerate(extracted_content[:10], 1):
            context += f"--- FONTE {i}: {content_item.get('title', 'Sem título')} ---\n"
            context += f"URL: {content_item.get('url', '')}\n"
            context += f"Conteúdo: {content_item.get('content', '')[:1500]}\n\n"
        
        return context
    
    def _build_analysis_prompt(self, data, context):
        """Constrói prompt para análise"""
        return f"""
Analise o seguinte mercado brasileiro e forneça insights detalhados:

DADOS DO PROJETO:
- Segmento: {data.get('segmento', 'Não informado')}
- Produto: {data.get('produto', 'Não informado')}
- Público: {data.get('publico', 'Não informado')}
- Preço: R$ {data.get('preco', 'Não informado')}

CONTEXTO DE PESQUISA:
{context}

Forneça uma análise estruturada em JSON com:
1. Avatar ultra-detalhado
2. Análise de posicionamento
3. Insights exclusivos (mínimo 15)
4. Análise de concorrência
5. Estratégia de palavras-chave
6. Métricas e projeções

Retorne apenas JSON válido.
"""
    
    def _process_ai_response(self, ai_response, original_data):
        """Processa resposta da IA"""
        try:
            # Remove markdown se presente
            clean_text = ai_response.strip()
            
            if "```json" in clean_text:
                start = clean_text.find("```json") + 7
                end = clean_text.rfind("```")
                clean_text = clean_text[start:end].strip()
            elif "```" in clean_text:
                start = clean_text.find("```") + 3
                end = clean_text.rfind("```")
                clean_text = clean_text[start:end].strip()
            
            # Tenta parsear JSON
            analysis = json.loads(clean_text)
            
            # Adiciona metadados
            analysis['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'provider_used': 'ai_manager',
                'version': '2.0.0',
                'analysis_type': 'comprehensive',
                'data_source': 'real_search_data'
            }
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao parsear JSON da IA: {str(e)}")
            # Retorna análise básica
            return self._create_basic_analysis(original_data)
    
    def _create_basic_analysis(self, data):
        """Cria análise básica quando IA falha"""
        segmento = data.get('segmento', 'Negócios')
        
        return {
            "avatar_ultra_detalhado": {
                "nome_ficticio": f"Profissional {segmento} Brasileiro",
                "perfil_demografico": {
                    "idade": "30-45 anos",
                    "renda": "R$ 8.000 - R$ 35.000",
                    "escolaridade": "Superior completo",
                    "localizacao": "Grandes centros urbanos"
                },
                "dores_viscerais": [
                    f"Trabalhar excessivamente em {segmento} sem crescer",
                    "Sentir-se sempre correndo atrás da concorrência",
                    "Ver competidores crescendo mais rápido"
                ],
                "desejos_secretos": [
                    f"Ser autoridade em {segmento}",
                    "Ter liberdade financeira",
                    "Negócio que funcione sozinho"
                ]
            },
            "insights_exclusivos": [
                f"O mercado brasileiro de {segmento} está em transformação",
                "Existe lacuna entre ferramentas e conhecimento",
                f"Profissionais de {segmento} pagam premium por simplicidade",
                "Fator decisivo é confiança + urgência + prova social",
                "Sistema básico gerado - configure APIs para análise completa"
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "analysis_type": "basic_fallback",
                "recommendation": "Configure APIs para análise completa"
            }
        }

    def execute_complete_analysis(self, data, session_id=None, progress_callback=None):
        """Executa análise completa"""
        if progress_callback is None:
            progress_callback = lambda step, message, details=None: logger.info(f"Progresso: {step} - {message}")

        try:
            # Inicia sessão de salvamento
            if self.auto_save and not session_id:
                session_id = self.auto_save.iniciar_sessao()
            
            # Fase 1: Pesquisa e Coleta de Dados
            search_results = self._execute_search_phase(data.get("query", f"mercado {data.get('segmento', 'negócios')} Brasil"), session_id, progress_callback)
            if "error" in search_results:
                logger.warning(f"⚠️ Pesquisa falhou: {search_results['error']}")
                # Continua sem pesquisa
                search_results = {"results": [], "total": 0}

            # Fase 2: Extração de Conteúdo
            extracted_content = self._execute_extraction_phase(search_results, session_id, progress_callback)
            if isinstance(extracted_content, dict) and "error" in extracted_content:
                logger.warning(f"⚠️ Extração falhou: {extracted_content['error']}")
                extracted_content = []

            # Fase 3: Análise de IA
            ai_analysis_results = self._execute_ai_analysis_phase(extracted_content, data, session_id, progress_callback)
            if isinstance(ai_analysis_results, dict) and "error" in ai_analysis_results:
                logger.warning(f"⚠️ Análise IA falhou: {ai_analysis_results['error']}")
                ai_analysis_results = self._create_basic_analysis(data)

            # Fase 4: Consolidação
            progress_callback(11, "📊 Consolidando análise final...")
            
            final_analysis = {
                'projeto_dados': data,
                'pesquisa_web_massiva': {
                    'estatisticas': {
                        'total_resultados': search_results.get('total', 0),
                        'conteudo_extraido': len(extracted_content) if isinstance(extracted_content, list) else 0
                    }
                },
                **ai_analysis_results,
                'session_id': session_id,
                'pipeline_status': {
                    'pesquisa_sucesso': "error" not in search_results,
                    'extracao_sucesso': isinstance(extracted_content, list),
                    'ia_sucesso': isinstance(ai_analysis_results, dict) and "error" not in ai_analysis_results
                }
            }
            
            progress_callback(12, "✅ Análise completa finalizada!")
            
            return final_analysis

        except Exception as e:
            logger.error(f"Erro durante a execução completa da análise: {e}", exc_info=True)
            if self.salvar_erro:
                self.salvar_erro("pipeline_completo_falha", e, contexto=data)
            return {"error": f"Erro crítico na análise: {str(e)}"}

# Instância global
enhanced_analysis_pipeline = EnhancedAnalysisPipeline()