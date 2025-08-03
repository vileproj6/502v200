#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Gemini 2.5 Pro Client
Cliente otimizado para Gemini 2.5 Pro com configurações avançadas
"""

import os
import logging
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

logger = logging.getLogger(__name__)

class Gemini25ProClient:
    """Cliente otimizado para Gemini 2.5 Pro"""
    
    def __init__(self):
        """Inicializa cliente Gemini 2.5 Pro"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            logger.error("❌ GEMINI_API_KEY não configurada")
            self.available = False
            return
        
        if not HAS_GEMINI:
            logger.error("❌ Biblioteca google-generativeai não instalada")
            self.available = False
            return
        
        try:
            # Configura API
            genai.configure(api_key=self.api_key)
            
            # Modelo mais avançado disponível
            self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
            
            # Configurações otimizadas para análises ultra-detalhadas
            self.generation_config = {
                'temperature': 0.9,  # Máxima criatividade
                'top_p': 0.95,
                'top_k': 64,
                'max_output_tokens': 8192,  # Máximo permitido
                'candidate_count': 1,
                'response_mime_type': 'text/plain'
            }
            
            # Configurações de segurança mínimas
            self.safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            self.available = True
            self.stats = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'total_tokens_used': 0,
                'avg_response_time': 0.0
            }
            
            logger.info("✅ Gemini 2.5 Pro Client inicializado com configurações avançadas")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Gemini 2.5 Pro: {e}")
            self.available = False
    
    def is_available(self) -> bool:
        """Verifica se o cliente está disponível"""
        return self.available
    
    def generate_ultra_analysis(
        self, 
        prompt: str, 
        max_tokens: int = 8192,
        temperature: float = 0.9,
        context: Dict[str, Any] = None
    ) -> Optional[str]:
        """Gera análise ultra-detalhada com Gemini 2.5 Pro"""
        
        if not self.available:
            raise Exception("Gemini 2.5 Pro não está disponível")
        
        self.stats['total_requests'] += 1
        start_time = time.time()
        
        try:
            # Configuração personalizada para esta requisição
            custom_config = self.generation_config.copy()
            custom_config['temperature'] = temperature
            custom_config['max_output_tokens'] = min(max_tokens, 8192)
            
            # Adiciona contexto ao prompt se fornecido
            if context:
                enhanced_prompt = self._enhance_prompt_with_context(prompt, context)
            else:
                enhanced_prompt = prompt
            
            logger.info("🚀 Gerando análise ultra-detalhada com Gemini 2.5 Pro...")
            
            # Gera conteúdo
            response = self.model.generate_content(
                enhanced_prompt,
                generation_config=custom_config,
                safety_settings=self.safety_settings
            )
            
            response_time = time.time() - start_time
            
            if response.text:
                # Atualiza estatísticas
                self.stats['successful_requests'] += 1
                self.stats['avg_response_time'] = (
                    (self.stats['avg_response_time'] * (self.stats['successful_requests'] - 1) + response_time) 
                    / self.stats['successful_requests']
                )
                
                # Estima tokens usados (aproximação)
                estimated_tokens = len(enhanced_prompt.split()) + len(response.text.split())
                self.stats['total_tokens_used'] += estimated_tokens
                
                logger.info(f"✅ Gemini 2.5 Pro: {len(response.text)} chars em {response_time:.2f}s")
                
                return response.text
            else:
                raise Exception("Resposta vazia do Gemini 2.5 Pro")
                
        except Exception as e:
            self.stats['failed_requests'] += 1
            response_time = time.time() - start_time
            
            logger.error(f"❌ Erro no Gemini 2.5 Pro após {response_time:.2f}s: {e}")
            raise Exception(f"Gemini 2.5 Pro falhou: {str(e)}")
    
    def _enhance_prompt_with_context(self, prompt: str, context: Dict[str, Any]) -> str:
        """Aprimora prompt com contexto adicional"""
        
        enhanced = f"""CONTEXTO ADICIONAL:
- Análise solicitada em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
- Nível de detalhamento: ULTRA-AVANÇADO
- Qualidade esperada: CONSULTORIA PREMIUM
- Público-alvo: {context.get('publico', 'Profissionais')}
- Segmento: {context.get('segmento', 'Negócios')}

{prompt}

INSTRUÇÕES ADICIONAIS:
- Use dados específicos e mensuráveis
- Evite generalidades e clichês
- Foque em insights acionáveis
- Mantenha tom profissional e autoritativo
- Estruture informações de forma clara e lógica"""
        
        return enhanced
    
    def test_connection(self) -> bool:
        """Testa conexão com Gemini 2.5 Pro"""
        
        if not self.available:
            return False
        
        try:
            test_prompt = "Responda apenas: GEMINI_2_5_PRO_OK"
            response = self.generate_ultra_analysis(test_prompt, max_tokens=50)
            
            return response and "GEMINI_2_5_PRO_OK" in response
            
        except Exception as e:
            logger.error(f"❌ Teste de conexão falhou: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cliente"""
        
        success_rate = 0.0
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
        
        return {
            **self.stats,
            'success_rate': success_rate,
            'available': self.available,
            'model': "gemini-2.0-flash-exp",
            'last_updated': datetime.now().isoformat()
        }
    
    def reset_stats(self):
        """Reset estatísticas"""
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_tokens_used': 0,
            'avg_response_time': 0.0
        }
        logger.info("🔄 Estatísticas do Gemini 2.5 Pro resetadas")
    
    def analyze_market_comprehensive(self, market_data: Dict[str, Any]) -> Optional[str]:
        """Análise de mercado abrangente específica"""
        
        prompt = f"""Como especialista em análise de mercado de elite, analise o seguinte mercado brasileiro:

DADOS DO MERCADO:
- Segmento: {market_data.get('segmento', 'N/A')}
- Produto/Serviço: {market_data.get('produto', 'N/A')}
- Público-Alvo: {market_data.get('publico', 'N/A')}
- Preço: R$ {market_data.get('preco', 'N/A')}
- Objetivo de Receita: R$ {market_data.get('objetivo_receita', 'N/A')}

FORNEÇA:
1. Análise SWOT ultra-detalhada
2. Oportunidades ocultas específicas
3. Ameaças não óbvias
4. Estratégias de diferenciação inovadoras
5. Projeções financeiras realistas
6. Roadmap de implementação detalhado
7. KPIs críticos para monitoramento
8. Cenários futuros prováveis

Seja ultra-específico para o mercado brasileiro. Cada insight deve ser imediatamente acionável."""
        
        return self.generate_ultra_analysis(prompt, max_tokens=8192, context=market_data)

# Instância global
gemini_25_client = Gemini25ProClient()