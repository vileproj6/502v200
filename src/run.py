#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Aplicação Flask Principal
Análise Ultra-Detalhada de Mercado com IA Avançada
"""

import os
import sys
import logging
import locale
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import traceback
import signal
import atexit

# Carrega variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

# Cria diretório de logs se necessário
if os.getenv('LOG_FILE_ENABLED', 'true').lower() == 'true':
    os.makedirs('logs', exist_ok=True)

# Configura locale para UTF-8
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except locale.Error:
        pass  # Usa locale padrão

# Configuração de logging
log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper())
log_format = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Prepara handlers de logging
handlers = [logging.StreamHandler(sys.stdout)]

if os.getenv('LOG_FILE_ENABLED', 'true').lower() == 'true':
    handlers.append(logging.FileHandler('logs/arqv30.log', encoding='utf-8'))

logging.basicConfig(
    level=log_level,
    format=log_format,
    handlers=handlers
)

logger = logging.getLogger(__name__)

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)

    # Força encoding UTF-8
    app.config['JSON_AS_ASCII'] = False

    # Configurações básicas
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year cache for static files

    # Cria diretório de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Configuração de produção
    if os.getenv('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = False
    else:
        app.config['DEBUG'] = True

    # Configuração CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))

    # Headers de segurança para produção
    if os.getenv('SECURE_HEADERS_ENABLED', 'true').lower() == 'true':
        @app.after_request
        def add_security_headers(response):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            return response

    # Compressão GZIP
    if os.getenv('GZIP_ENABLED', 'true').lower() == 'true':
        try:
            from flask_compress import Compress
            Compress(app)
        except ImportError:
            logger.warning("⚠️ Flask-Compress não instalado - compressão desabilitada")

    # Importa e registra blueprints
    try:
        from routes.analysis import analysis_bp
        app.register_blueprint(analysis_bp, url_prefix='/api')
        logger.info("✅ Blueprint analysis registrado")
    except ImportError as e:
        logger.error(f"❌ Erro ao importar analysis blueprint: {e}")

    try:
        from routes.pdf_generator import pdf_bp
        app.register_blueprint(pdf_bp, url_prefix='/api')
        logger.info("✅ Blueprint pdf_generator registrado")
    except ImportError as e:
        logger.warning(f"⚠️ PDF generator não disponível: {e}")

    try:
        from routes.monitoring import monitoring_bp
        app.register_blueprint(monitoring_bp, url_prefix='/api')
        logger.info("✅ Blueprint monitoring registrado")
    except ImportError as e:
        logger.warning(f"⚠️ Monitoring não disponível: {e}")

    try:
        from routes.user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api')
        logger.info("✅ Blueprint user registrado")
    except ImportError as e:
        logger.warning(f"⚠️ User routes não disponível: {e}")

    try:
        from routes.progress import progress_bp
        app.register_blueprint(progress_bp, url_prefix='/api')
        logger.info("✅ Blueprint progress registrado")
    except ImportError as e:
        logger.warning(f"⚠️ Progress routes não disponível: {e}")

    try:
        from routes.files import files_bp
        app.register_blueprint(files_bp, url_prefix='/api')
        logger.info("✅ Blueprint files registrado")
    except ImportError as e:
        logger.warning(f"⚠️ Files routes não disponível: {e}")

    # Service Worker route
    @app.route('/sw.js')
    def service_worker():
        """Serve o service worker"""
        try:
            return send_file(os.path.join(app.static_folder, 'sw.js'), mimetype='application/javascript')
        except FileNotFoundError:
            return "// Service worker não encontrado", 404, {'Content-Type': 'application/javascript'}

    # Rota para compatibilidade com PDF
    @app.route('/generate-pdf', methods=['POST'])
    def generate_pdf_compat():
        """Rota de compatibilidade para geração de PDF"""
        try:
            from routes.pdf_generator import generate_pdf
            return generate_pdf()
        except ImportError:
            return jsonify({
                'error': 'Gerador de PDF não disponível',
                'message': 'Módulo pdf_generator não foi carregado'
            }), 501

    # Rota principal
    @app.route('/')
    def index():
        """Página principal da aplicação"""
        try:
            return render_template('enhanced_index.html')
        except Exception as e:
            logger.error(f"Erro ao carregar template: {e}")
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ARQV30 Enhanced v2.0</title>
                <meta charset="UTF-8">
            </head>
            <body>
                <h1>ARQV30 Enhanced v2.0</h1>
                <p>Sistema de Análise de Mercado</p>
                <p>Status: Operacional</p>
                <p>Timestamp: {datetime.now().isoformat()}</p>
                <a href="/api/health">Health Check</a>
            </body>
            </html>
            """

    # Health check
    @app.route('/api/health')
    def health_check():
        """Verifica status da aplicação"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        })

    # Status da aplicação
    @app.route('/api/app_status')
    def app_status():
        """Retorna status detalhado dos serviços"""
        try:
            # Importa serviços dinamicamente para evitar erros
            search_status = {}
            try:
                from services.production_search_manager import production_search_manager
                search_status = production_search_manager.get_provider_status()
            except ImportError as e:
                logger.warning(f"Search manager não disponível: {e}")
                search_status = {'error': 'Não disponível'}

            # Conta provedores disponíveis
            if isinstance(search_status, dict) and 'error' not in search_status:
                available_search = len([p for p in search_status.values() if p.get('enabled', False)])
                total_search = len(search_status)
            else:
                available_search = 0
                total_search = 0

            return jsonify({
                'app_name': 'ARQV30 Enhanced',
                'version': '2.0.0',
                'status': 'production' if os.getenv('FLASK_ENV') == 'production' else 'development',
                'timestamp': datetime.now().isoformat(),
                'encoding': 'UTF-8',
                'locale': locale.getlocale(),
                'services': {
                    'search_providers': {
                        'available': available_search,
                        'total': total_search,
                        'details': search_status
                    },
                    'content_extraction': {'available': True},
                    'cache': {'enabled': os.getenv('CACHE_ENABLED', 'true').lower() == 'true'},
                    'database': {'available': bool(os.getenv('SUPABASE_URL'))}
                },
                'environment': {
                    'python_version': sys.version,
                    'flask_env': os.getenv('FLASK_ENV', 'production'),
                    'debug_mode': app.config.get('DEBUG', False),
                    'max_content_length': app.config.get('MAX_CONTENT_LENGTH'),
                    'upload_folder': app.config.get('UPLOAD_FOLDER')
                }
            })
        except Exception as e:
            logger.error(f"Erro ao verificar status: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500

    # Rota para limpar caches
    @app.route('/api/clear_cache', methods=['POST'])
    def clear_cache():
        """Limpa todos os caches do sistema"""
        try:
            cleared_services = []
            
            try:
                from services.production_search_manager import production_search_manager
                production_search_manager.clear_cache()
                cleared_services.append('search_manager')
            except ImportError:
                pass
            
            try:
                from services.production_content_extractor import production_content_extractor
                production_content_extractor.clear_cache()
                cleared_services.append('content_extractor')
            except ImportError:
                pass

            return jsonify({
                'success': True,
                'message': 'Caches limpos com sucesso',
                'cleared_services': cleared_services,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {str(e)}")
            return jsonify({
                'error': 'Erro ao limpar cache',
                'message': str(e)
            }), 500

    # Rota para reset de provedores
    @app.route('/api/reset_providers', methods=['POST'])
    def reset_providers():
        """Reset contadores de erro dos provedores"""
        try:
            data = request.get_json() or {}
            provider_name = data.get('provider')
            reset_services = []

            try:
                from services.production_search_manager import production_search_manager
                production_search_manager.reset_provider_errors(provider_name)
                reset_services.append('search_providers')
            except ImportError:
                pass

            message = f"Reset erros do provedor: {provider_name}" if provider_name else "Reset erros de todos os provedores"

            return jsonify({
                'success': True,
                'message': message,
                'reset_services': reset_services,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Erro ao resetar provedores: {str(e)}")
            return jsonify({
                'error': 'Erro ao resetar provedores',
                'message': str(e)
            }), 500

    # Handler de erro global
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handler global para exceções"""
        logger.error(f"Erro não tratado: {str(e)}")
        logger.error(traceback.format_exc())

        # Em produção, não expõe detalhes do erro
        if os.getenv('FLASK_ENV') == 'production':
            error_message = 'Erro interno do servidor'
        else:
            error_message = str(e)

        return jsonify({
            'error': 'Erro interno do servidor',
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }), 500

    # Handler para 404
    @app.errorhandler(404)
    def not_found(e):
        """Handler para páginas não encontradas"""
        return jsonify({
            'error': 'Recurso não encontrado',
            'message': 'O endpoint solicitado não existe',
            'timestamp': datetime.now().isoformat()
        }), 404

    # Handler para 413 (arquivo muito grande)
    @app.errorhandler(413)
    def file_too_large(e):
        """Handler para arquivos muito grandes"""
        return jsonify({
            'error': 'Arquivo muito grande',
            'message': 'O arquivo enviado excede o limite de 16MB',
            'timestamp': datetime.now().isoformat()
        }), 413

    return app

def setup_signal_handlers():
    """Configura handlers para sinais do sistema"""
    def signal_handler(signum, frame):
        logger.info(f"🛑 Recebido sinal {signum}, encerrando aplicação...")
        # Cleanup aqui se necessário
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def cleanup_on_exit():
    """Função de limpeza executada na saída"""
    logger.info("🧹 Executando limpeza final...")
    try:
        # Importa e executa limpeza dos serviços se disponíveis
        try:
            from services.production_search_manager import production_search_manager
            production_search_manager.clear_cache()
        except ImportError:
            pass
        
        try:
            from services.production_content_extractor import production_content_extractor
            production_content_extractor.clear_cache()
        except ImportError:
            pass
            
    except Exception as e:
        logger.error(f"Erro na limpeza final: {e}")

def main():
    """Função principal para executar a aplicação"""
    try:
        # Configura handlers de sinal
        setup_signal_handlers()
        atexit.register(cleanup_on_exit)

        app = create_app()

        # Configurações do servidor
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV') != 'production'

        # Configurações de produção
        if os.getenv('FLASK_ENV') == 'production':
            logger.info("🚀 Iniciando ARQV30 Enhanced v2.0 em MODO PRODUÇÃO")
            logger.info("🔒 Debug desabilitado, headers de segurança habilitados")
        else:
            logger.info("🔧 Iniciando ARQV30 Enhanced v2.0 em MODO DESENVOLVIMENTO")

        logger.info(f"Servidor: http://{host}:{port}")
        logger.info(f"Encoding: UTF-8")
        logger.info(f"Locale: {locale.getlocale()}")

        # Verifica configurações críticas
        critical_configs = [
            'SUPABASE_URL', 'SUPABASE_ANON_KEY', 'GEMINI_API_KEY'
        ]

        missing_configs = [config for config in critical_configs if not os.getenv(config)]
        if missing_configs:
            logger.warning(f"⚠️ Configurações ausentes: {', '.join(missing_configs)}")

        # Log de provedores de busca
        try:
            from services.production_search_manager import production_search_manager
            search_status = production_search_manager.get_provider_status()
            enabled_providers = [name for name, status in search_status.items() if status.get('enabled', False)]
            logger.info(f"🔍 Provedores de busca ativos: {', '.join(enabled_providers)}")
        except ImportError:
            logger.warning("⚠️ Production search manager não disponível")

        # Inicia o servidor
        if os.getenv('FLASK_ENV') == 'production':
            # Produção com Gunicorn seria ideal, mas para compatibilidade:
            app.run(
                host=host,
                port=port,
                debug=False,
                threaded=True,
                use_reloader=False
            )
        else:
            app.run(
                host=host,
                port=port,
                debug=debug,
                threaded=True
            )

    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
