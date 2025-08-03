#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Configuração do Banco de Dados Local
Sistema de armazenamento local sem dependência do Supabase
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from services.local_file_manager import local_file_manager
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de dados local sem Supabase"""
    
    def __init__(self):
        """Inicializa gerenciador com arquivos locais apenas"""
        self.local_files = local_file_manager
        
        logger.info("✅ Database Manager inicializado com armazenamento local")
    
    def test_connection(self) -> bool:
        """Testa conexão com o sistema de arquivos local"""
        try:
            # Verifica se pode escrever no diretório
            test_file = os.path.join(self.local_files.base_dir, 'test_connection.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except Exception as e:
            logger.error(f"❌ Erro no teste de conexão local: {e}")
            return False
    
    def create_analysis(self, analysis_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria nova análise em arquivos locais"""
        try:
            logger.info("💾 Salvando análise em arquivos locais...")
            local_result = self.local_files.save_analysis_locally(analysis_data)
            
            if not local_result['success']:
                logger.error(f"❌ Falha ao salvar localmente: {local_result.get('error')}")
                return None
            
            logger.info(f"✅ Análise criada: {len(local_result['files'])} arquivos locais")
            
            # Retorna dados com ID local
            return {
                'id': local_result['analysis_id'],
                'local_only': True,
                'local_files': local_result,
                **analysis_data
            }
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar análise: {str(e)}")
            return None
    
    def update_analysis(self, analysis_id: str, update_data: Dict[str, Any]) -> bool:
        """Atualiza análise existente (não implementado para arquivos locais)"""
        logger.warning("⚠️ Atualização de análise não implementada para armazenamento local")
        return False
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Busca análise por ID nos arquivos locais"""
        try:
            # Busca nos arquivos de metadata
            analyses = self.local_files.list_local_analyses()
            
            for analysis in analyses:
                if analysis['analysis_id'] == analysis_id:
                    # Carrega análise completa
                    complete_file = None
                    for root, dirs, files in os.walk(self.local_files.base_dir):
                        for file in files:
                            if analysis_id[:8] in file and file.endswith('_completa.json'):
                                complete_file = os.path.join(root, file)
                                break
                        if complete_file:
                            break
                    
                    if complete_file:
                        with open(complete_file, 'r', encoding='utf-8') as f:
                            return json.load(f)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar análise {analysis_id}: {e}")
            return None
    
    def list_analyses(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista análises locais com paginação"""
        try:
            analyses = self.local_files.list_local_analyses()
            
            # Aplica paginação
            start = offset
            end = offset + limit
            
            return analyses[start:end]
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar análises: {e}")
            return []
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """Remove análise dos arquivos locais"""
        return self.local_files.delete_local_analysis(analysis_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do armazenamento local"""
        try:
            local_analyses = self.local_files.list_local_analyses()
            storage_stats = self.local_files.get_storage_stats()
            
            return {
                'total_analyses': len(local_analyses),
                'recent_analyses': len([a for a in local_analyses if a.get('created_at', '') > (datetime.now().isoformat()[:10])]),
                'storage_stats': storage_stats,
                'local_analyses': local_analyses[:10],  # Últimas 10
                'storage_type': 'local_files_only'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {e}")
            return {
                'total_analyses': 0,
                'recent_analyses': 0,
                'storage_stats': {},
                'local_analyses': [],
                'storage_type': 'local_files_only',
                'error': str(e)
            }
    
    def get_analysis_files(self, analysis_id: str) -> List[Dict[str, Any]]:
        """Busca arquivos de uma análise"""
        return self.local_files.get_analysis_files(analysis_id)
    
    def list_local_analyses(self) -> List[Dict[str, Any]]:
        """Lista análises salvas localmente"""
        return self.local_files.list_local_analyses()

# Instância global do gerenciador
db_manager = DatabaseManager()