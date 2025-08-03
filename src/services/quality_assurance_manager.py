#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Quality Assurance Manager
Gerenciador de garantia de qualidade com zero tolerância a simulações
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class QualityAssuranceManager:
    """Gerenciador de garantia de qualidade ultra-rigoroso"""
    
    def __init__(self):
        """Inicializa gerenciador de qualidade"""
        self.simulation_patterns = [
            r'simulado',
            r'genérico',
            r'template'
        ]
        
        self.quality_requirements = {
            'min_avatar_dores': 8,
            'min_avatar_desejos': 8,
            'min_insights': 15,
            'min_content_specificity': 0.8,
            'min_component_success_rate': 0.6,
            'zero_simulation_tolerance': True
        }
        
        self.content_filters = {
            'remove_raw_data': True,
            'remove_urls': True,
            'remove_html': True,
            'remove_debug_info': True,
            'keep_statistics_only': True
        }
        
        logger.info("Quality Assurance Manager inicializado com tolerância zero")
    
    def validate_complete_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida análise completa com critérios ultra-rigorosos"""
        
        validation_result = {
            'valid': False,
            'quality_score': 0.0,
            'errors': [],
            'warnings': [],
            'simulation_detected': False,
            'component_validation': {},
            'content_quality': {},
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            logger.info("🔍 Iniciando validação ultra-rigorosa")
            
            # 1. Detecta simulações (ZERO TOLERÂNCIA)
            simulation_check = self._detect_simulations_comprehensive(analysis)
            validation_result['simulation_detected'] = simulation_check['has_simulation']
            
            if simulation_check['has_simulation']:
                validation_result['errors'].extend(simulation_check['simulation_errors'])
                logger.error(f"❌ SIMULAÇÕES DETECTADAS: {simulation_check['simulation_errors']}")
                return validation_result
            
            # 2. Valida estrutura obrigatória
            structure_validation = self._validate_required_structure(analysis)
            validation_result['component_validation']['structure'] = structure_validation
            
            if not structure_validation['valid']:
                validation_result['errors'].extend(structure_validation['errors'])
            
            # 3. Valida qualidade do conteúdo
            content_validation = self._validate_content_quality(analysis)
            validation_result['content_quality'] = content_validation
            
            if not content_validation['valid']:
                validation_result['errors'].extend(content_validation['errors'])
            
            # 4. Valida componentes individuais
            component_validations = self._validate_individual_components(analysis)
            validation_result['component_validation'].update(component_validations)
            
            # 5. Calcula score de qualidade
            quality_score = self._calculate_comprehensive_quality_score(
                structure_validation, content_validation, component_validations
            )
            validation_result['quality_score'] = quality_score
            
            # 6. Determina se é válida
            validation_result['valid'] = (
                len(validation_result['errors']) == 0 and
                quality_score >= 70.0 and
                not validation_result['simulation_detected']
            )
            
            # 7. Gera recomendações
            validation_result['recommendations'] = self._generate_quality_recommendations(validation_result)
            
            status = "✅ VÁLIDA" if validation_result['valid'] else "❌ INVÁLIDA"
            logger.info(f"{status} Análise validada - Score: {quality_score:.1f}%")
            
            return validation_result
            
        except Exception as e:
            validation_result['errors'].append(f"Erro crítico na validação: {str(e)}")
            logger.error(f"❌ Erro crítico na validação: {str(e)}")
            return validation_result
    
    def _detect_simulations_comprehensive(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Detecta simulações de forma abrangente"""
        
        result = {
            'has_simulation': False,
            'simulation_errors': [],
            'simulation_count': 0,
            'affected_components': []
        }
        
        # Converte análise para string
        analysis_str = json.dumps(analysis, ensure_ascii=False).lower()
        
        # Verifica padrões de simulação
        for pattern in self.simulation_patterns:
            matches = len(re.findall(pattern, analysis_str))
            if matches > 0:
                result['simulation_count'] += matches
                result['simulation_errors'].append(f"Padrão '{pattern}' encontrado {matches} vezes")
        
        # Verifica componentes específicos
        components_to_check = [
            'avatar_ultra_detalhado',
            'posicionamento_estrategico', 
            'analise_concorrencia_avancada',
            'insights_exclusivos'
        ]
        
        for component_name in components_to_check:
            if component_name in analysis:
                component_simulation = self._check_component_simulation(
                    component_name, analysis[component_name]
                )
                
                if component_simulation['has_simulation']:
                    result['affected_components'].append(component_name)
                    result['simulation_errors'].extend(component_simulation['errors'])
        
        # Determina se tem simulação
        result['has_simulation'] = (
            result['simulation_count'] > 0 or 
            len(result['affected_components']) > 0
        )
        
        return result
    
    def _check_component_simulation(self, component_name: str, component_data: Any) -> Dict[str, Any]:
        """Verifica simulação em componente específico"""
        
        result = {
            'has_simulation': False,
            'errors': []
        }
        
        if not component_data:
            return result
        
        component_str = json.dumps(component_data, ensure_ascii=False).lower()
        
        # Padrões específicos por componente
        if component_name == 'avatar_ultra_detalhado':
            # Avatar não pode ter dados genéricos
            if isinstance(component_data, dict):
                dores = component_data.get('dores_viscerais', [])
                for dor in dores:
                    if any(pattern in str(dor).lower() for pattern in self.simulation_patterns):
                        result['has_simulation'] = True
                        result['errors'].append(f"Dor simulada detectada: {str(dor)[:50]}...")
        
        elif component_name == 'insights_exclusivos':
            # Insights devem ser específicos
            if isinstance(component_data, list):
                for insight in component_data:
                    if any(pattern in str(insight).lower() for pattern in self.simulation_patterns):
                        result['has_simulation'] = True
                        result['errors'].append(f"Insight simulado detectado: {str(insight)[:50]}...")
        
        # Verifica padrões gerais
        for pattern in self.simulation_patterns:
            if pattern in component_str:
                result['has_simulation'] = True
                result['errors'].append(f"Padrão '{pattern}' em {component_name}")
        
        return result
    
    def _validate_required_structure(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida estrutura obrigatória"""
        
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Componentes obrigatórios
        required_components = [
            'projeto_dados',
            'avatar_ultra_detalhado',
            'posicionamento_estrategico',
            'insights_exclusivos'
        ]
        
        for component in required_components:
            if component not in analysis:
                result['errors'].append(f"Componente obrigatório ausente: {component}")
                result['valid'] = False
            elif not analysis[component]:
                result['errors'].append(f"Componente obrigatório vazio: {component}")
                result['valid'] = False
        
        # Validações específicas
        if 'avatar_ultra_detalhado' in analysis:
            avatar = analysis['avatar_ultra_detalhado']
            
            if not avatar.get('perfil_demografico'):
                result['errors'].append("Perfil demográfico ausente no avatar")
                result['valid'] = False
            
            if not avatar.get('dores_viscerais') or len(avatar['dores_viscerais']) < 8:
                result['errors'].append("Dores viscerais insuficientes (mínimo 8)")
                result['valid'] = False
            
            if not avatar.get('desejos_secretos') or len(avatar['desejos_secretos']) < 8:
                result['errors'].append("Desejos secretos insuficientes (mínimo 8)")
                result['valid'] = False
        
        return result
    
    def _validate_content_quality(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida qualidade do conteúdo"""
        
        result = {
            'valid': True,
            'errors': [],
            'quality_metrics': {}
        }
        
        # Verifica especificidade do conteúdo
        specificity_score = self._calculate_content_specificity(analysis)
        result['quality_metrics']['specificity_score'] = specificity_score
        
        if specificity_score < self.quality_requirements['min_content_specificity']:
            result['errors'].append(f"Conteúdo muito genérico: {specificity_score:.2f} < {self.quality_requirements['min_content_specificity']}")
            result['valid'] = False
        
        # Verifica insights
        insights = analysis.get('insights_exclusivos', [])
        if isinstance(insights, list):
            valid_insights = [i for i in insights if self._is_valid_insight(i)]
            result['quality_metrics']['valid_insights_count'] = len(valid_insights)
            
            if len(valid_insights) < self.quality_requirements['min_insights']:
                result['errors'].append(f"Insights válidos insuficientes: {len(valid_insights)} < {self.quality_requirements['min_insights']}")
                result['valid'] = False
        
        return result
    
    def _validate_individual_components(self, analysis: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Valida componentes individuais"""
        
        validations = {}
        
        # Lista de componentes para validar
        components_to_validate = [
            'drivers_mentais_customizados',
            'provas_visuais_instantaneas',
            'sistema_anti_objecao',
            'pre_pitch_invisivel',
            'predicoes_futuro_completas'
        ]
        
        for component_name in components_to_validate:
            if component_name in analysis:
                validations[component_name] = self._validate_single_component(
                    component_name, analysis[component_name]
                )
            else:
                validations[component_name] = {
                    'valid': False,
                    'error': 'Componente ausente',
                    'quality_score': 0
                }
        
        return validations
    
    def _validate_single_component(self, component_name: str, component_data: Any) -> Dict[str, Any]:
        """Valida componente individual"""
        
        result = {
            'valid': True,
            'error': None,
            'quality_score': 100,
            'warnings': []
        }
        
        if not component_data:
            result['valid'] = False
            result['error'] = 'Componente vazio'
            result['quality_score'] = 0
            return result
        
        # Rejeita fallbacks
        if isinstance(component_data, dict) and component_data.get('fallback_mode'):
            result['valid'] = False
            result['error'] = 'Componente em modo fallback - rejeitado'
            result['quality_score'] = 0
            return result
        
        # Validações específicas por componente
        if component_name == 'drivers_mentais_customizados':
            drivers = component_data.get('drivers_customizados', [])
            if len(drivers) < 3:
                result['valid'] = False
                result['error'] = f'Drivers insuficientes: {len(drivers)} < 3'
                result['quality_score'] = 0
            else:
                # Verifica qualidade dos drivers
                valid_drivers = 0
                for driver in drivers:
                    if (driver.get('nome') and 
                        driver.get('roteiro_ativacao', {}).get('historia_analogia') and
                        len(driver['roteiro_ativacao']['historia_analogia']) > 100):
                        valid_drivers += 1
                
                if valid_drivers < len(drivers) * 0.8:
                    result['quality_score'] = 50
                    result['warnings'].append('Alguns drivers de baixa qualidade')
        
        elif component_name == 'provas_visuais_instantaneas':
            if isinstance(component_data, list):
                if len(component_data) < 3:
                    result['valid'] = False
                    result['error'] = f'Provas visuais insuficientes: {len(component_data)} < 3'
                    result['quality_score'] = 0
                else:
                    # Verifica qualidade das provas
                    valid_proofs = 0
                    for proof in component_data:
                        if (proof.get('nome') and 
                            proof.get('experimento') and
                            len(proof.get('experimento', '')) > 50):
                            valid_proofs += 1
                    
                    if valid_proofs < len(component_data) * 0.8:
                        result['quality_score'] = 60
                        result['warnings'].append('Algumas provas de baixa qualidade')
        
        elif component_name == 'insights_exclusivos':
            if isinstance(component_data, list):
                valid_insights = [i for i in component_data if self._is_valid_insight(i)]
                
                if len(valid_insights) < 10:
                    result['valid'] = False
                    result['error'] = f'Insights válidos insuficientes: {len(valid_insights)} < 10'
                    result['quality_score'] = 0
                else:
                    result['quality_score'] = min(100, (len(valid_insights) / 20) * 100)
        
        return result
    
    def _calculate_content_specificity(self, analysis: Dict[str, Any]) -> float:
        """Calcula especificidade do conteúdo"""
        
        analysis_str = json.dumps(analysis, ensure_ascii=False)
        
        # Padrões que indicam especificidade
        specificity_patterns = [
            r'\d+%',  # Percentuais
            r'R\$\s*\d+',  # Valores monetários
            r'\d+\s*(mil|milhão|bilhão)',  # Quantidades
            r'20(23|24|25)',  # Anos recentes
            r'\d+\s*(dias|meses|anos)',  # Períodos
            r'[A-Z][a-z]+\s+[A-Z][a-z]+',  # Nomes próprios
            r'\d+\.\d+',  # Números decimais
            r'\d+\s*(clientes|usuários|empresas)',  # Quantidades específicas
        ]
        
        specificity_count = 0
        for pattern in specificity_patterns:
            matches = len(re.findall(pattern, analysis_str))
            specificity_count += matches
        
        # Normaliza baseado no tamanho do conteúdo
        content_length = len(analysis_str)
        specificity_ratio = specificity_count / (content_length / 1000) if content_length > 0 else 0
        
        return min(specificity_ratio, 1.0)
    
    def _is_valid_insight(self, insight: str) -> bool:
        """Verifica se insight é válido (não simulado)"""
        
        if not insight or len(insight) < 40:
            return False
        
        insight_lower = insight.lower()
        
        # Rejeita insights com padrões de simulação
        for pattern in self.simulation_patterns:
            if pattern in insight_lower:
                return False
        
        # Verifica se tem elementos específicos
        has_specifics = (
            re.search(r'\d+%', insight) or  # Percentuais
            re.search(r'R\$\s*\d+', insight) or  # Valores
            re.search(r'\d+\s*(mil|milhão|bilhão)', insight) or  # Quantidades
            re.search(r'20(23|24|25)', insight) or  # Anos
            len(insight.split()) > 15  # Insights substanciais
        )
        
        return has_specifics
    
    def _calculate_comprehensive_quality_score(
        self, 
        structure_validation: Dict[str, Any],
        content_validation: Dict[str, Any],
        component_validations: Dict[str, Dict[str, Any]]
    ) -> float:
        """Calcula score abrangente de qualidade"""
        
        score = 0.0
        
        # Estrutura (30 pontos)
        if structure_validation['valid']:
            score += 30
        
        # Qualidade do conteúdo (40 pontos)
        if content_validation['valid']:
            score += 30
            
            # Bonus por especificidade
            specificity = content_validation.get('quality_metrics', {}).get('specificity_score', 0)
            score += specificity * 10
        
        # Componentes individuais (30 pontos)
        valid_components = sum(1 for v in component_validations.values() if v['valid'])
        total_components = len(component_validations)
        
        if total_components > 0:
            component_score = (valid_components / total_components) * 30
            score += component_score
        
        return min(score, 100.0)
    
    def _generate_quality_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Gera recomendações de qualidade"""
        
        recommendations = []
        
        if validation_result['simulation_detected']:
            recommendations.append("🚨 CRÍTICO: Remova todas as simulações e dados genéricos")
            recommendations.append("🔧 Configure todas as APIs para dados reais")
        
        if validation_result['errors']:
            recommendations.append("❌ Corrija os erros listados antes de usar a análise")
        
        quality_score = validation_result['quality_score']
        
        if quality_score < 50:
            recommendations.append("🔧 URGENTE: Configure mais APIs para melhorar qualidade")
        elif quality_score < 70:
            recommendations.append("🔧 MELHORIA: Configure APIs adicionais para qualidade premium")
        elif quality_score < 90:
            recommendations.append("✨ OTIMIZAÇÃO: Pequenos ajustes podem elevar a qualidade")
        else:
            recommendations.append("🎉 EXCELENTE: Análise de qualidade premium")
        
        # Recomendações específicas por componente
        component_validations = validation_result.get('component_validation', {})
        failed_components = [name for name, val in component_validations.items() if not val.get('valid')]
        
        if failed_components:
            recommendations.append(f"🔧 COMPONENTES: Configure APIs para: {', '.join(failed_components)}")
        
        return recommendations
    
    def filter_raw_data_comprehensive(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Remove dados brutos de forma abrangente"""
        
        if not self.content_filters['remove_raw_data']:
            return analysis
        
        logger.info("🧹 Removendo dados brutos do relatório final")
        
        # Campos que contêm dados brutos
        raw_data_fields = [
            'extracted_content', 'raw_content', 'page_content', 'html_content',
            'search_results', 'urls_found', 'links_extracted', 'raw_response',
            'full_content', 'content_preview', 'detailed_results', 'sources_raw',
            'extraction_details', 'raw_data', 'content_raw', 'html_raw',
            'search_results_raw', 'content_full', 'page_html', 'response_raw',
            'debug_info', 'extraction_log', 'search_log', 'processing_log'
        ]
        
        return self._filter_recursive(analysis, raw_data_fields)
    
    def _filter_recursive(self, data: Any, fields_to_remove: List[str]) -> Any:
        """Filtra dados recursivamente"""
        
        if isinstance(data, dict):
            filtered = {}
            
            for key, value in data.items():
                # Remove campos de dados brutos
                if key.lower() in [field.lower() for field in fields_to_remove]:
                    # Mantém apenas estatísticas
                    if isinstance(value, list):
                        filtered[f"{key}_count"] = len(value)
                    elif isinstance(value, str):
                        filtered[f"{key}_length"] = len(value)
                    # Não inclui o conteúdo bruto
                else:
                    # Filtra recursivamente
                    filtered[key] = self._filter_recursive(value, fields_to_remove)
            
            return filtered
        
        elif isinstance(data, list):
            return [self._filter_recursive(item, fields_to_remove) for item in data]
        
        else:
            return data
    
    def create_quality_report(self, validation_result: Dict[str, Any]) -> str:
        """Cria relatório de qualidade detalhado"""
        
        report = []
        report.append("=" * 80)
        report.append("📊 RELATÓRIO DE GARANTIA DE QUALIDADE")
        report.append("=" * 80)
        
        # Status geral
        status_icon = "✅" if validation_result['valid'] else "❌"
        status_text = "APROVADA" if validation_result['valid'] else "REJEITADA"
        report.append(f"{status_icon} STATUS GERAL: {status_text}")
        report.append(f"📈 SCORE DE QUALIDADE: {validation_result['quality_score']:.1f}%")
        
        # Simulações
        if validation_result['simulation_detected']:
            report.append(f"\n🚨 SIMULAÇÕES DETECTADAS:")
            for error in validation_result.get('simulation_errors', [])[:5]:
                report.append(f"   • {error}")
        else:
            report.append(f"\n✅ ZERO SIMULAÇÕES: Conteúdo 100% real")
        
        # Componentes
        component_validations = validation_result.get('component_validation', {})
        if component_validations:
            report.append(f"\n🔧 STATUS DOS COMPONENTES:")
            for component, validation in component_validations.items():
                icon = "✅" if validation.get('valid', False) else "❌"
                score = validation.get('quality_score', 0)
                report.append(f"   {icon} {component}: {score:.1f}%")
        
        # Qualidade do conteúdo
        content_quality = validation_result.get('content_quality', {})
        if content_quality:
            report.append(f"\n📝 QUALIDADE DO CONTEÚDO:")
            metrics = content_quality.get('quality_metrics', {})
            
            if 'specificity_score' in metrics:
                report.append(f"   • Especificidade: {metrics['specificity_score']:.2f}")
            
            if 'valid_insights_count' in metrics:
                report.append(f"   • Insights válidos: {metrics['valid_insights_count']}")
        
        # Erros
        if validation_result['errors']:
            report.append(f"\n❌ ERROS CRÍTICOS:")
            for error in validation_result['errors']:
                report.append(f"   • {error}")
        
        # Recomendações
        if validation_result['recommendations']:
            report.append(f"\n💡 RECOMENDAÇÕES:")
            for rec in validation_result['recommendations']:
                report.append(f"   • {rec}")
        
        report.append("=" * 80)
        
        return '\n'.join(report)
    
    def should_generate_pdf(self, analysis: Dict[str, Any]) -> Tuple[bool, str]:
        """Determina se deve gerar PDF baseado na qualidade"""
        
        validation = self.validate_complete_analysis(analysis)
        
        # Critérios para PDF
        if validation['simulation_detected']:
            return False, "PDF rejeitado: Simulações detectadas"
        
        # Critérios mais flexíveis para PDF
        if validation['quality_score'] < 50:
            return False, f"PDF rejeitado: Qualidade muito baixa ({validation['quality_score']:.1f}% < 50%)"
        
        # Verifica se tem componentes essenciais
        essential_components = ['avatar_ultra_detalhado', 'insights_exclusivos']
        missing_essential = [comp for comp in essential_components if comp not in analysis or not analysis[comp]]
        
        if missing_essential:
            return False, f"PDF rejeitado: Componentes essenciais ausentes: {missing_essential}"
        
        # Verifica se tem conteúdo suficiente
        insights = analysis.get('insights_exclusivos', [])
        if len(insights) < 8:
            return False, f"PDF rejeitado: Insights insuficientes ({len(insights)} < 8)"
        
        return True, f"PDF aprovado: Qualidade adequada ({validation['quality_score']:.1f}%)"

# Instância global
quality_assurance_manager = QualityAssuranceManager()
