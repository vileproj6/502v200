#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Rotas de Análise
Endpoints para análise de mercado ultra-detalhada
"""

import os
import logging
import time
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, session, send_file
from services.enhanced_analysis_pipeline import enhanced_analysis_pipeline
from services.quality_assurance_manager import quality_assurance_manager
from services.ai_manager import ai_manager
from services.production_search_manager import production_search_manager
from services.attachment_service import attachment_service
from database import db_manager
from routes.progress import get_progress_tracker, update_analysis_progress
from services.auto_save_manager import auto_save_manager, salvar_etapa, salvar_erro
from services.consolidated_report_generator import consolidated_report_generator
from services.gemini_2_5_client import gemini_25_client

logger = logging.getLogger(__name__)

# Cria blueprint
analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
    """Endpoint principal para análise de mercado"""
    
    try:
        start_time = time.time()
        logger.info("🚀 Iniciando análise de mercado aprimorada")
        
        # Coleta dados da requisição
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Dados não fornecidos',
                'message': 'Envie os dados da análise no corpo da requisição'
            }), 400
        
        # Validação básica
        if not data.get('segmento'):
            return jsonify({
                'error': 'Segmento obrigatório',
                'message': 'O campo "segmento" é obrigatório para análise'
            }), 400
        
        # Adiciona session_id se não fornecido
        if not data.get('session_id'):
            data['session_id'] = f"session_{int(time.time())}_{os.urandom(4).hex()}"
        
        # Inicia sessão de salvamento automático
        session_id = data['session_id']
        auto_save_manager.iniciar_sessao(session_id)
        
        # Salva dados de entrada imediatamente
        salvar_etapa("requisicao_analise", {
            "input_data": data,
            "timestamp": datetime.now().isoformat(),
            "ip_address": request.remote_addr,
            "user_agent": request.headers.get('User-Agent', '')
        }, categoria="analise_completa")
        
        # Inicia rastreamento de progresso
        progress_tracker = get_progress_tracker(session_id)
        
        # Função de callback para progresso
        def progress_callback(step: int, message: str, details: str = None):
            update_analysis_progress(session_id, step, message, details)
            # Salva progresso também
            salvar_etapa("progresso", {
                "step": step,
                "message": message,
                "details": details
            }, categoria="logs")
        
        # Log dos dados recebidos
        logger.info(f"📊 Dados recebidos: Segmento={data.get('segmento')}, Produto={data.get('produto')}")
        
        # Prepara query de pesquisa se não fornecida
        if not data.get('query'):
            segmento = data.get('segmento', '')
            produto = data.get('produto', '')
            if produto:
                data['query'] = f"mercado {segmento} {produto} Brasil tendências oportunidades 2024"
            else:
                data['query'] = f"análise mercado {segmento} Brasil dados estatísticas crescimento"
        
        logger.info(f"🔍 Query de pesquisa: {data['query']}")
        
        # Salva query preparada
        salvar_etapa("query_preparada", {"query": data['query']}, categoria="pesquisa_web")
        
        # Executa análise aprimorada com pipeline
        logger.info("🚀 Executando análise aprimorada...")
        try:
            # Usa o pipeline aprimorado com Gemini 2.5 Pro
            analysis_result = enhanced_analysis_pipeline.execute_complete_analysis(
                data,
                session_id=session_id,
                progress_callback=progress_callback
            )
            
            # Salva resultado da análise imediatamente
            salvar_etapa("analise_resultado", analysis_result, categoria="analise_completa")
            
            # Gera relatórios consolidados
            if progress_callback:
                progress_callback(11, "📊 Gerando relatórios consolidados...")
            
            consolidated_reports = consolidated_report_generator.generate_consolidated_reports(
                analysis_result, session_id
            )
            
            # Adiciona informações dos relatórios ao resultado
            analysis_result['relatorios_consolidados'] = consolidated_reports
            
            # Validação de qualidade ultra-rigorosa
            logger.info("🔍 Executando garantia de qualidade...")
            quality_validation = quality_assurance_manager.validate_complete_analysis(analysis_result)
            
            # Salva validação
            salvar_etapa("validacao_qualidade", quality_validation, categoria="analise_completa")
            
            if not quality_validation['valid']:
                logger.error(f"❌ Análise rejeitada: {quality_validation['errors']}")
                salvar_erro("validacao_falha", Exception("Análise rejeitada por baixa qualidade"), contexto=quality_validation)
                
                # Consolida dados parciais
                dados_parciais = auto_save_manager.consolidar_sessao(session_id)
                
                return jsonify({
                    'error': 'Análise de baixa qualidade rejeitada',
                    'message': 'Análise não atende critérios de qualidade ultra-rigorosos',
                    'quality_report': quality_validation,
                    'recommendations': quality_validation['recommendations'],
                    'dados_parciais': dados_parciais,
                    'session_id': session_id,
                    'timestamp': datetime.now().isoformat()
                }), 422
            
            # Remove dados brutos do relatório final
            clean_analysis = quality_assurance_manager.filter_raw_data_comprehensive(analysis_result)
            
            # Adiciona informações dos relatórios consolidados
            clean_analysis['relatorios_consolidados'] = analysis_result.get('relatorios_consolidados', {})
            
            # Salva análise limpa
            salvar_etapa("analise_limpa", clean_analysis, categoria="analise_completa")
            
            logger.info(f"✅ Análise validada com score {quality_validation['quality_score']:.1f}%")
            
        except Exception as e:
            logger.error(f"❌ Pipeline de análise falhou: {str(e)}")
            salvar_erro("pipeline_analise", e, contexto=data)
            
            # Recupera dados salvos automaticamente
            try:
                dados_recuperados = auto_save_manager.consolidar_sessao(session_id)
                logger.info(f"🔄 Dados recuperados automaticamente: {dados_recuperados}")
                
                return jsonify({
                    'error': 'Pipeline falhou mas dados preservados',
                    'message': str(e),
                    'dados_preservados': True,
                    'session_id': session_id,
                    'relatorio_parcial': dados_recuperados,
                    'timestamp': datetime.now().isoformat(),
                    'recommendation': 'Dados preservados - configure APIs e tente novamente'
                }), 206  # Partial Content
                
            except Exception as recovery_error:
                logger.error(f"❌ Falha na recuperação automática: {recovery_error}")
            
            return jsonify({
                'error': 'Falha crítica na análise',
                'message': str(e),
                'timestamp': datetime.now().isoformat(),
                'recommendation': 'Configure APIs e execute novamente',
                'session_id': session_id,
                'dados_preservados': f'Verifique relatorios_intermediarios/{session_id}',
                'debug_info': {
                    'input_data': {
                        'segmento': data.get('segmento'),
                        'produto': data.get('produto'),
                        'query': data.get('query')
                    },
                    'ai_status': ai_manager.get_provider_status(),
                    'search_status': production_search_manager.get_provider_status()
                }
            }), 500
        
        # Verifica se a análise foi bem-sucedida
        if not clean_analysis or not isinstance(clean_analysis, dict):
            logger.error("❌ Análise limpa inválida")
            salvar_erro("analise_limpa_invalida", Exception("Análise limpa inválida"))
            return jsonify({
                'error': 'Análise final inválida',
                'message': 'Falha na limpeza da análise',
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'recommendation': 'Verifique logs e tente novamente'
            }), 500
        
        # Marca progresso como completo
        progress_tracker.complete()
        
        # Salva no banco de dados
        try:
            logger.info("💾 Salvando análise no banco de dados...")
            db_record = db_manager.create_analysis({
                'segmento': data.get('segmento'),
                'produto': data.get('produto'),
                'publico': data.get('publico'),
                'preco': data.get('preco'),
                'objetivo_receita': data.get('objetivo_receita'),
                'orcamento_marketing': data.get('orcamento_marketing'),
                'prazo_lancamento': data.get('prazo_lancamento'),
                'concorrentes': data.get('concorrentes'),
                'dados_adicionais': data.get('dados_adicionais'),
                'query': data.get('query'),
                'status': 'completed',
                'session_id': session_id,
                **clean_analysis  # Inclui análise limpa
            })
            
            if db_record:
                if db_record.get('local_only'):
                    clean_analysis['local_only'] = True
                    clean_analysis['local_files'] = db_record.get('local_files')
                    logger.info(f"✅ Análise salva localmente: {len(db_record['local_files']['files'])} arquivos")
                else:
                    clean_analysis['database_id'] = db_record['id']
                    clean_analysis['local_files'] = db_record.get('local_files')
                    logger.info(f"✅ Análise salva: Supabase ID {db_record['id']} + arquivos locais")
                
                # Salva confirmação do banco
                salvar_etapa("banco_salvo", {
                    "database_id": db_record.get('id'),
                    "local_files": db_record.get('local_files', {})
                }, categoria="analise_completa")
            else:
                logger.warning("⚠️ Falha ao salvar análise")
                salvar_erro("banco_falha", Exception("Falha ao salvar no banco"))
                clean_analysis['database_warning'] = "Falha ao salvar no banco"
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar no banco: {str(e)}")
            salvar_erro("banco_erro", e)
            clean_analysis['database_warning'] = f"Erro no banco: {str(e)}"
        
        # Consolida sessão final
        try:
            relatorio_consolidado = auto_save_manager.consolidar_sessao(session_id)
            clean_analysis['relatorio_consolidado'] = relatorio_consolidado
            logger.info(f"📋 Relatório consolidado gerado: {relatorio_consolidado}")
        except Exception as e:
            logger.error(f"❌ Erro ao consolidar sessão: {e}")
        
        # Calcula tempo de processamento
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Adiciona metadados finais
        if 'metadata' not in clean_analysis:
            clean_analysis['metadata'] = {}
        
        clean_analysis['metadata'].update({
            'processing_time_seconds': processing_time,
            'processing_time_formatted': f"{int(processing_time // 60)}m {int(processing_time % 60)}s",
            'request_timestamp': datetime.now().isoformat(),
            'session_id': data.get('session_id'),
            'pipeline_version': '2.0_enhanced',
            'quality_assured': True,
            'raw_data_filtered': True,
            'simulation_free': True,
            'input_data': {
                'segmento': data.get('segmento'),
                'produto': data.get('produto'),
                'query': data.get('query')
            },
            'quality_score': quality_validation.get('quality_score', 0)
        })
        
        # Salva resposta final
        salvar_etapa("resposta_final", clean_analysis, categoria="analise_completa")
        
        logger.info(f"✅ Análise concluída em {processing_time:.2f} segundos")
        
        return jsonify(clean_analysis)
        
    except Exception as e:
        logger.error(f"❌ Erro crítico na análise: {str(e)}", exc_info=True)
        
        # Remove progresso em caso de erro
        try:
            if 'session_id' in locals() and session_id in get_progress_tracker.__globals__.get('progress_sessions', {}):
                del get_progress_tracker.__globals__['progress_sessions'][session_id]
        except:
            pass  # Ignora erros de limpeza
        
        return jsonify({
            'error': 'Erro na análise',
            'message': str(e),
            'timestamp': datetime.now().isoformat(),
            'recommendation': 'Configure todas as APIs necessárias antes de tentar novamente',
            'session_id': locals().get('session_id', 'unknown'),
            'debug_info': {
                'input_data': {
                    'segmento': data.get('segmento') if 'data' in locals() else 'unknown',
                    'produto': data.get('produto') if 'data' in locals() else 'unknown'
                },
                'ai_status': ai_manager.get_provider_status(),
                'search_status': production_search_manager.get_provider_status()
            }
        }), 500

@analysis_bp.route('/status', methods=['GET'])
def get_analysis_status():
    """Retorna status dos sistemas de análise"""
    
    try:
        # Status dos provedores de IA
        ai_status = ai_manager.get_provider_status()
        
        # Status dos provedores de busca
        search_status = production_search_manager.get_provider_status()
        
        # Status do banco de dados
        db_status = db_manager.test_connection()
        
        # Status geral
        total_ai_available = len([p for p in ai_status.values() if p['available']])
        total_search_available = len([p for p in search_status.values() if p['available']])
        
        overall_status = "healthy" if (total_ai_available > 0 and total_search_available > 0 and db_status) else "degraded"
        
        return jsonify({
            'status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'systems': {
                'ai_providers': {
                    'status': 'healthy' if total_ai_available > 0 else 'error',
                    'available_count': total_ai_available,
                    'total_count': len(ai_status),
                    'providers': ai_status
                },
                'search_providers': {
                    'status': 'healthy' if total_search_available > 0 else 'error',
                    'available_count': total_search_available,
                    'total_count': len(search_status),
                    'providers': search_status
                },
                'database': {
                    'status': 'healthy' if db_status else 'error',
                    'connected': db_status
                },
                'content_extraction': {
                    'status': 'healthy',
                    'available': True
                }
            },
            'capabilities': {
                'multi_ai_fallback': total_ai_available > 1,
                'multi_search_fallback': total_search_available > 1,
                'real_time_search': total_search_available > 0,
                'content_extraction': True,
                'database_storage': db_status
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar status: {str(e)}")
        return jsonify({
            'error': 'Erro ao verificar status',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@analysis_bp.route('/progress/<session_id>', methods=['GET'])
def get_analysis_progress(session_id):
    """Retorna progresso da análise em tempo real"""
    
    try:
        progress_tracker = get_progress_tracker(session_id)
        
        return jsonify({
            'session_id': session_id,
            'progress': progress_tracker.get_progress(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter progresso: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter progresso',
            'message': str(e),
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        }), 500

@analysis_bp.route('/cancel/<session_id>', methods=['POST'])
def cancel_analysis(session_id):
    """Cancela análise em andamento"""
    
    try:
        # Remove progresso
        if session_id in get_progress_tracker.__globals__.get('progress_sessions', {}):
            del get_progress_tracker.__globals__['progress_sessions'][session_id]
        
        # Salva cancelamento
        salvar_etapa("analise_cancelada", {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "reason": "Cancelada pelo usuário"
        }, categoria="logs")
        
        return jsonify({
            'success': True,
            'message': 'Análise cancelada com sucesso',
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao cancelar análise: {str(e)}")
        return jsonify({
            'error': 'Erro ao cancelar análise',
            'message': str(e),
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        }), 500

@analysis_bp.route('/history', methods=['GET'])
def get_analysis_history():
    """Retorna histórico de análises"""
    
    try:
        # Parâmetros de paginação
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 10)), 50)  # Máximo 50
        
        # Busca histórico no banco
        history = db_manager.get_analysis_history(page=page, limit=limit)
        
        return jsonify({
            'success': True,
            'history': history,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': len(history)
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter histórico: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter histórico',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@analysis_bp.route('/download/<analysis_id>', methods=['GET'])
def download_analysis(analysis_id):
    """Download de análise específica"""
    
    try:
        # Busca análise no banco
        analysis = db_manager.get_analysis(analysis_id)
        
        if not analysis:
            return jsonify({
                'error': 'Análise não encontrada',
                'analysis_id': analysis_id
            }), 404
        
        # Gera arquivo temporário
        import tempfile
        import json
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
            temp_path = f.name
        
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f"analise_{analysis_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mimetype='application/json'
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao fazer download: {str(e)}")
        return jsonify({
            'error': 'Erro ao fazer download',
            'message': str(e),
            'analysis_id': analysis_id,
            'timestamp': datetime.now().isoformat()
        }), 500

