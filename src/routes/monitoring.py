
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Monitoring Routes
Endpoints para monitoramento do sistema de extração
"""
from flask import Blueprint, jsonify, request
import logging

# Importação condicional
try:
    from services.robust_content_extractor import robust_content_extractor
    HAS_ROBUST_EXTRACTOR = True
except ImportError:
    HAS_ROBUST_EXTRACTOR = False
    robust_content_extractor = None
logger = logging.getLogger(__name__)

monitoring_bp = Blueprint('monitoring', __name__)


@monitoring_bp.route('/api/extractor_stats', methods=['GET'])
def get_extractor_stats():
    """Retorna estatísticas dos extratores"""
    try:
        if HAS_ROBUST_EXTRACTOR and robust_content_extractor:
            stats = robust_content_extractor.get_extractor_stats()
        else:
            stats = {'error': 'Robust Content Extractor não disponível'}
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoring_bp.route('/api/test_extraction', methods=['GET'])
def test_extraction():
    """Testa extração para uma URL específica"""
    url = request.args.get('url')
    
    if not url:
        return jsonify({
            'success': False,
            'error': 'URL é obrigatória'
        }), 400
    
    try:
        # Testa extração com detalhes
        if HAS_ROBUST_EXTRACTOR and robust_content_extractor:
            content = robust_content_extractor.extract_content(url)
        else:
            return jsonify({
                'success': False,
                'error': 'Robust Content Extractor não disponível'
            }), 500
        
        if content:
            # Valida qualidade do conteúdo
            try:
                from services.content_quality_validator import content_quality_validator
                validation = content_quality_validator.validate_content(content, url)
            except ImportError:
                validation = {
                    'valid': len(content) > 200,
                    'score': min(100, len(content) / 10),
                    'reason': 'Validação básica'
                }
            
            result = {
                'success': True,
                'url': url,
                'content_length': len(content),
                'content_preview': content[:500] + '...' if len(content) > 500 else content,
                'validation': validation,
                'extractor_stats': robust_content_extractor.get_extractor_stats() if HAS_ROBUST_EXTRACTOR else {}
            }
        else:
            result = {
                'success': False,
                'url': url,
                'error': 'Falha na extração de conteúdo',
                'extractor_stats': robust_content_extractor.get_extractor_stats() if HAS_ROBUST_EXTRACTOR else {}
            }
        
        return jsonify({
            'success': result['success'],
            **result
        })
    except Exception as e:
        logger.error(f"❌ Erro ao testar extração: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'extractor_stats': robust_content_extractor.get_extractor_stats()
        }), 500


@monitoring_bp.route('/api/health', methods=['GET'])
def health_check():
    """Verifica saúde do sistema"""
    try:
        # Testa extração com URL brasileira real
        test_url = "https://g1.globo.com/"
        
        if HAS_ROBUST_EXTRACTOR and robust_content_extractor:
            content = robust_content_extractor.extract_content(test_url)
            extraction_success = content is not None and len(content) > 100
        else:
            extraction_success = False
        
        stats = robust_content_extractor.get_extractor_stats() if HAS_ROBUST_EXTRACTOR else {}
        global_stats = stats.get('global', {})
        available_extractors = sum(1 for name, data in stats.items() 
                                 if name != 'global' and data.get('available', False))
        
        # Verifica status das APIs de IA
        try:
            from services.ai_manager import ai_manager
            ai_status = ai_manager.get_provider_status()
            available_ai = sum(1 for provider in ai_status.values() if provider.get('available', False))
        except ImportError:
            ai_status = {}
            available_ai = 0
        
        # Verifica status de busca
        try:
            from services.production_search_manager import production_search_manager
            search_status = production_search_manager.get_provider_status()
            available_search = sum(1 for provider in search_status.values() if provider.get('enabled', False))
        except ImportError:
            search_status = {}
            available_search = 0
        
        overall_health = 'healthy'
        if available_extractors == 0 or available_ai == 0:
            overall_health = 'critical'
        elif available_extractors < 2 or available_search == 0:
            overall_health = 'degraded'
        
        return jsonify({
            'success': True,
            'status': overall_health,
            'available_extractors': available_extractors,
            'available_ai_providers': available_ai,
            'available_search_providers': available_search,
            'test_extraction': extraction_success,
            'extraction_stats': global_stats,
            'ai_status': ai_status,
            'search_status': search_status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"❌ Erro no health check: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'critical',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
