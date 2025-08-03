#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Local Storage Client
Cliente de armazenamento local (substitui Supabase)
"""

import os
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class LocalStorageClient:
    """Cliente de armazenamento local (substitui Supabase)"""
    
    def __init__(self):
        """Inicializa cliente de armazenamento local"""
        self.storage_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'local_storage')
        os.makedirs(self.storage_dir, exist_ok=True)
        
        logger.info("✅ Local Storage client inicializado")
    
    def is_connected(self) -> bool:
        """Verifica se o armazenamento local está disponível"""
        return os.path.exists(self.storage_dir) and os.access(self.storage_dir, os.W_OK)
    
    def test_connection(self) -> bool:
        """Testa conexão com armazenamento local"""
        try:
            test_file = os.path.join(self.storage_dir, 'test.json')
            with open(test_file, 'w') as f:
                json.dump({'test': True}, f)
            os.remove(test_file)
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao testar armazenamento local: {str(e)}")
            return False
    
    def create_analysis(self, analysis_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria nova análise no armazenamento local"""
        try:
            analysis_id = f"analysis_{int(time.time())}_{os.urandom(4).hex()}"
            
            # Prepara dados para armazenamento
            storage_data = {
                'id': analysis_id,
                'segmento': analysis_data.get('segmento', ''),
                'produto': analysis_data.get('produto', ''),
                'publico': analysis_data.get('publico', ''),
                'preco': analysis_data.get('preco'),
                'objetivo_receita': analysis_data.get('objetivo_receita'),
                'orcamento_marketing': analysis_data.get('orcamento_marketing'),
                'prazo_lancamento': analysis_data.get('prazo_lancamento', ''),
                'concorrentes': analysis_data.get('concorrentes', ''),
                'dados_adicionais': analysis_data.get('dados_adicionais', ''),
                'query': analysis_data.get('query', ''),
                'status': analysis_data.get('status', 'completed'),
                'comprehensive_analysis': analysis_data,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Salva arquivo
            file_path = os.path.join(self.storage_dir, f"{analysis_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Análise criada no armazenamento local: {analysis_id}")
            return storage_data
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar análise local: {str(e)}")
            return None
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Busca análise por ID"""
        try:
            file_path = os.path.join(self.storage_dir, f"{analysis_id}.json")
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar análise {analysis_id}: {str(e)}")
            return None
    
    def list_analyses(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista análises com paginação"""
        try:
            analyses = []
            
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.storage_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            analysis = json.load(f)
                            # Retorna apenas metadados básicos
                            analyses.append({
                                'id': analysis.get('id'),
                                'segmento': analysis.get('segmento'),
                                'produto': analysis.get('produto'),
                                'status': analysis.get('status'),
                                'created_at': analysis.get('created_at'),
                                'updated_at': analysis.get('updated_at')
                            })
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao ler arquivo {filename}: {e}")
                        continue
            
            # Ordena por data de criação
            analyses.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            # Aplica paginação
            start = offset
            end = offset + limit
            
            return analyses[start:end]
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar análises: {str(e)}")
            return []
    
    def update_analysis(self, analysis_id: str, update_data: Dict[str, Any]) -> bool:
        """Atualiza análise existente"""
        try:
            file_path = os.path.join(self.storage_dir, f"{analysis_id}.json")
            
            if os.path.exists(file_path):
                # Carrega dados existentes
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                # Atualiza dados
                existing_data.update(update_data)
                existing_data['updated_at'] = datetime.now().isoformat()
                
                # Salva de volta
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
                logger.info(f"✅ Análise {analysis_id} atualizada")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar análise {analysis_id}: {str(e)}")
            return False
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """Remove análise do armazenamento local"""
        try:
            file_path = os.path.join(self.storage_dir, f"{analysis_id}.json")
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"✅ Análise {analysis_id} removida")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover análise {analysis_id}: {str(e)}")
            return False
    
    def save_analysis_file(self, analysis_id: str, file_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Salva informações de arquivo (não implementado para local)"""
        logger.info(f"📁 Informações de arquivo registradas para {analysis_id}")
        return {'id': f"file_{int(time.time())}", **file_data}
    
    def get_analysis_files(self, analysis_id: str) -> List[Dict[str, Any]]:
        """Busca arquivos de uma análise (retorna lista vazia para local)"""
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do armazenamento local"""
        try:
            analyses = self.list_analyses(1000)  # Carrega todas para estatísticas
            
            # Conta por status
            status_counts = {}
            for analysis in analyses:
                status = analysis.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Análises recentes (últimos 7 dias)
            from datetime import timedelta
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            recent_count = len([a for a in analyses if a.get('created_at', '') > week_ago])
            
            return {
                'total_analyses': len(analyses),
                'status_counts': status_counts,
                'recent_analyses': recent_count,
                'storage_type': 'local_files',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
            return {
                'total_analyses': 0,
                'status_counts': {},
                'recent_analyses': 0,
                'storage_type': 'local_files',
                'error': str(e)
            }

# Instância global (compatibilidade)
supabase_client = LocalStorageClient()