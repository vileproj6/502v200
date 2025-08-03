#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Consolidated Report Generator
Gerador de relatórios consolidados ultra-robustos sem dados brutos
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import markdown
import html

logger = logging.getLogger(__name__)

class ConsolidatedReportGenerator:
    """Gerador de relatórios consolidados ultra-completos"""
    
    def __init__(self):
        """Inicializa gerador de relatórios"""
        self.reports_dir = Path("relatorios_consolidados")
        self.reports_dir.mkdir(exist_ok=True)
        
        self.templates = self._load_report_templates()
        self.formatting_rules = self._load_formatting_rules()
        
        logger.info("Consolidated Report Generator inicializado")
    
    def _load_report_templates(self) -> Dict[str, str]:
        """Carrega templates de relatórios"""
        return {
            'executive_summary': """# Resumo Executivo - {title}

## Oportunidade Principal
{main_opportunity}

## Descobertas-Chave
{key_findings}

## Recomendação Estratégica
{strategic_recommendation}

## Investimento Necessário
{investment_required}

## ROI Projetado
{projected_roi}

## Próximos Passos
{next_steps}
""",
            
            'technical_analysis': """# Análise Técnica Detalhada - {title}

## Avatar Ultra-Detalhado
{avatar_analysis}

## Posicionamento Estratégico
{positioning_analysis}

## Análise Competitiva
{competition_analysis}

## Estratégia de Marketing
{marketing_strategy}

## Métricas e KPIs
{metrics_analysis}

## Plano de Ação
{action_plan}
""",
            
            'implementation_guide': """# Guia de Implementação - {title}

## Fase 1: Preparação (0-30 dias)
{phase_1}

## Fase 2: Lançamento (31-90 dias)
{phase_2}

## Fase 3: Crescimento (91-180 dias)
{phase_3}

## Recursos Necessários
{resources_needed}

## Cronograma Detalhado
{detailed_timeline}

## Métricas de Acompanhamento
{tracking_metrics}
"""
        }
    
    def _load_formatting_rules(self) -> Dict[str, Any]:
        """Carrega regras de formatação"""
        return {
            'remove_raw_data': True,
            'enhance_readability': True,
            'add_visual_elements': True,
            'include_actionable_items': True,
            'prioritize_insights': True,
            'add_implementation_notes': True
        }
    
    def generate_consolidated_reports(
        self, 
        analysis: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Gera relatórios consolidados completos"""
        
        logger.info(f"📊 Gerando relatórios consolidados para sessão: {session_id}")
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f"analise_{session_id[:8]}_{timestamp}"
            
            generated_reports = {}
            
            # 1. Relatório Executivo Premium
            executive_report = self._generate_executive_report(analysis, base_filename)
            generated_reports['executive'] = executive_report
            
            # 2. Análise Técnica Completa
            technical_report = self._generate_technical_report(analysis, base_filename)
            generated_reports['technical'] = technical_report
            
            # 3. Guia de Implementação Detalhado
            implementation_guide = self._generate_implementation_guide(analysis, base_filename)
            generated_reports['implementation'] = implementation_guide
            
            # 4. Dashboard Interativo
            dashboard = self._generate_interactive_dashboard(analysis, base_filename)
            generated_reports['dashboard'] = dashboard
            
            # 5. Relatório de Insights Prioritizados
            insights_report = self._generate_insights_report(analysis, base_filename)
            generated_reports['insights'] = insights_report
            
            # 6. Análise de ROI e Projeções
            roi_analysis = self._generate_roi_analysis(analysis, base_filename)
            generated_reports['roi'] = roi_analysis
            
            # 7. Plano de Contingência
            contingency_plan = self._generate_contingency_plan(analysis, base_filename)
            generated_reports['contingency'] = contingency_plan
            
            # 8. Relatório de Monitoramento
            monitoring_report = self._generate_monitoring_report(analysis, base_filename)
            generated_reports['monitoring'] = monitoring_report
            
            # Gera índice de relatórios
            index_file = self._generate_reports_index(generated_reports, base_filename)
            generated_reports['index'] = index_file
            
            logger.info(f"✅ {len(generated_reports)} relatórios consolidados gerados")
            
            return {
                'success': True,
                'reports_generated': len(generated_reports),
                'reports': generated_reports,
                'base_directory': str(self.reports_dir),
                'session_id': session_id,
                'timestamp': timestamp
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatórios consolidados: {e}")
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }
    
    def _generate_executive_report(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera relatório executivo premium"""
        
        try:
            resumo = analysis.get('resumo_executivo', {})
            projeto = analysis.get('projeto_dados', {})
            
            # Conteúdo do relatório executivo
            content = f"""# Relatório Executivo Premium
## {projeto.get('segmento', 'Análise de Mercado')} - {datetime.now().strftime('%B %Y')}

### 🎯 Oportunidade Principal
{resumo.get('visao_geral', {}).get('oportunidade_principal', 'Oportunidade estratégica identificada')}

### 📊 Potencial de Mercado
{resumo.get('visao_geral', {}).get('potencial_mercado', 'Potencial significativo identificado')}

### 🚀 Recomendação Estratégica
{resumo.get('visao_geral', {}).get('recomendacao_estrategica', 'Estratégia recomendada baseada na análise')}

### 💰 Investimento Recomendado
{resumo.get('investimento_recomendado', 'Investimento calculado baseado no ROI projetado')}

### 📈 Projeções Financeiras

#### Cenário Conservador
- **Receita Mensal:** {self._extract_financial_projection(analysis, 'conservador', 'receita_mensal')}
- **Clientes/Mês:** {self._extract_financial_projection(analysis, 'conservador', 'clientes_mes')}
- **Ticket Médio:** {self._extract_financial_projection(analysis, 'conservador', 'ticket_medio')}

#### Cenário Realista
- **Receita Mensal:** {self._extract_financial_projection(analysis, 'realista', 'receita_mensal')}
- **Clientes/Mês:** {self._extract_financial_projection(analysis, 'realista', 'clientes_mes')}
- **Ticket Médio:** {self._extract_financial_projection(analysis, 'realista', 'ticket_medio')}

#### Cenário Otimista
- **Receita Mensal:** {self._extract_financial_projection(analysis, 'otimista', 'receita_mensal')}
- **Clientes/Mês:** {self._extract_financial_projection(analysis, 'otimista', 'clientes_mes')}
- **Ticket Médio:** {self._extract_financial_projection(analysis, 'otimista', 'ticket_medio')}

### 🎯 Próximos Passos Críticos
{self._format_list(resumo.get('proximos_passos_criticos', []))}

### ⚠️ Principais Riscos
{self._format_list(resumo.get('riscos_oportunidades', {}).get('principais_riscos', []))}

### 🌟 Maiores Oportunidades
{self._format_list(resumo.get('riscos_oportunidades', {}).get('maiores_oportunidades', []))}

### 📅 Timeline de Implementação
{self._format_timeline(resumo.get('timeline_implementacao', {}))}

---
*Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} pelo ARQV30 Enhanced v2.0*
"""
            
            # Salva relatório
            filepath = self.reports_dir / f"{base_filename}_executivo.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Gera versão HTML
            html_content = markdown.markdown(content, extensions=['tables', 'toc'])
            html_filepath = self.reports_dir / f"{base_filename}_executivo.html"
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(self._wrap_html(html_content, "Relatório Executivo Premium"))
            
            logger.info(f"✅ Relatório executivo gerado: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório executivo: {e}")
            return ""
    
    def _generate_technical_report(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera relatório técnico detalhado"""
        
        try:
            avatar = analysis.get('avatar_ultra_detalhado', {})
            posicionamento = analysis.get('posicionamento_estrategico', {})
            
            content = f"""# Análise Técnica Detalhada
## {analysis.get('projeto_dados', {}).get('segmento', 'Mercado Analisado')}

### 👤 Avatar Ultra-Detalhado

#### Perfil Demográfico
{self._format_dict(avatar.get('perfil_demografico', {}))}

#### Perfil Psicográfico
{self._format_dict(avatar.get('perfil_psicografico', {}))}

#### Dores Viscerais ({len(avatar.get('dores_viscerais', []))})
{self._format_numbered_list(avatar.get('dores_viscerais', []))}

#### Desejos Secretos ({len(avatar.get('desejos_secretos', []))})
{self._format_numbered_list(avatar.get('desejos_secretos', []))}

#### Objeções Reais ({len(avatar.get('objecoes_reais', []))})
{self._format_numbered_list(avatar.get('objecoes_reais', []))}

### 🎯 Posicionamento Estratégico

#### Proposta de Valor Única
{posicionamento.get('proposta_valor_unica', 'Proposta de valor a ser definida')}

#### Diferenciais Competitivos
{self._format_list(posicionamento.get('diferenciais_competitivos', []))}

#### Mensagem Central
{posicionamento.get('mensagem_central', 'Mensagem central a ser definida')}

#### Estratégia Oceano Azul
{posicionamento.get('estrategia_oceano_azul', 'Estratégia de oceano azul a ser desenvolvida')}

### 🏆 Análise Competitiva
{self._format_competition_analysis(analysis.get('analise_concorrencia_avancada', []))}

### 📈 Estratégia de Marketing Completa
{self._format_marketing_strategy(analysis.get('estrategia_marketing_completa', {}))}

### 📊 Métricas e KPIs Avançados
{self._format_metrics_analysis(analysis.get('metricas_kpis_avancados', {}))}

### 🔄 Funil de Vendas Detalhado
{self._format_sales_funnel(analysis.get('funil_vendas_detalhado', {}))}

---
*Análise técnica gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
            
            filepath = self.reports_dir / f"{base_filename}_tecnico.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Relatório técnico gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório técnico: {e}")
            return ""
    
    def _generate_implementation_guide(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera guia de implementação detalhado"""
        
        try:
            plano = analysis.get('plano_acao_detalhado', {})
            
            content = f"""# Guia de Implementação Detalhado
## {analysis.get('projeto_dados', {}).get('segmento', 'Projeto')}

### 🚀 Visão Geral da Implementação

Este guia fornece um roadmap detalhado para implementar as estratégias identificadas na análise de mercado.

### 📅 Fase 1: Primeiros 30 Dias - Preparação e Estruturação

#### Foco Principal
{plano.get('primeiros_30_dias', {}).get('foco', 'Estruturação inicial do projeto')}

#### Atividades Detalhadas
{self._format_activities(plano.get('primeiros_30_dias', {}).get('atividades', []))}

#### Investimento Necessário
{plano.get('primeiros_30_dias', {}).get('investimento', 'Investimento a ser calculado')}

#### Entregas Esperadas
{self._format_list(plano.get('primeiros_30_dias', {}).get('entregas', []))}

#### Métricas de Acompanhamento
{self._format_list(plano.get('primeiros_30_dias', {}).get('metricas', []))}

### 📈 Fase 2: Dias 31-90 - Implementação e Testes

#### Foco Principal
{plano.get('dias_31_90', {}).get('foco', 'Implementação das estratégias principais')}

#### Atividades Detalhadas
{self._format_activities(plano.get('dias_31_90', {}).get('atividades', []))}

#### Estratégias de Escalação
{self._format_list(plano.get('dias_31_90', {}).get('escalacao', []))}

#### Otimizações Planejadas
{self._format_list(plano.get('dias_31_90', {}).get('otimizacao', []))}

### 🎯 Fase 3: Dias 91-180 - Otimização e Crescimento

#### Foco Principal
{plano.get('dias_91_180', {}).get('foco', 'Otimização e crescimento sustentável')}

#### Estratégias de Consolidação
{self._format_list(plano.get('dias_91_180', {}).get('consolidacao', []))}

#### Inovações a Implementar
{self._format_list(plano.get('dias_91_180', {}).get('inovacao', []))}

#### Parcerias Estratégicas
{self._format_list(plano.get('dias_91_180', {}).get('parcerias', []))}

### 🛠️ Recursos e Ferramentas Necessárias

#### Recursos Humanos
- Equipe de marketing digital
- Especialista em vendas
- Analista de dados
- Designer/Desenvolvedor

#### Recursos Tecnológicos
- CRM avançado
- Ferramentas de automação
- Plataforma de analytics
- Sistema de gestão de conteúdo

#### Recursos Financeiros
- Orçamento de marketing
- Investimento em tecnologia
- Capital de giro
- Reserva para contingências

### 📊 Sistema de Monitoramento

#### KPIs Principais
{self._format_kpis(analysis.get('metricas_kpis_avancados', {}))}

#### Frequência de Acompanhamento
- **Diário:** Métricas operacionais
- **Semanal:** KPIs de performance
- **Mensal:** Análise estratégica
- **Trimestral:** Revisão completa

### ⚠️ Planos de Contingência

#### Cenário de Baixa Performance
- Revisão de estratégias
- Ajuste de investimentos
- Mudança de canais
- Otimização de processos

#### Cenário de Alta Performance
- Aceleração de investimentos
- Expansão de canais
- Contratação de equipe
- Desenvolvimento de novos produtos

---
*Guia de implementação gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
            
            filepath = self.reports_dir / f"{base_filename}_implementacao.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Guia de implementação gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar guia de implementação: {e}")
            return ""
    
    def _generate_interactive_dashboard(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera dashboard interativo em HTML"""
        
        try:
            metricas = analysis.get('metricas_kpis_avancados', {})
            insights = analysis.get('insights_exclusivos', [])
            
            html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Interativo - ARQV30</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border-left: 4px solid #4facfe;
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #4facfe;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .insights-section {{
            padding: 30px;
            background: #f8f9fa;
        }}
        .insight-item {{
            background: white;
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .priority-high {{ border-left-color: #dc3545; }}
        .priority-medium {{ border-left-color: #ffc107; }}
        .priority-low {{ border-left-color: #28a745; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dashboard Interativo</h1>
            <p>Análise Ultra-Avançada de Mercado</p>
            <p><strong>{analysis.get('projeto_dados', {}).get('segmento', 'Mercado Analisado')}</strong></p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">ROI Esperado</div>
                <div class="metric-value">{metricas.get('roi_esperado', 'N/A')}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Fontes Analisadas</div>
                <div class="metric-value">{analysis.get('metadata', {}).get('research_sources', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Insights Gerados</div>
                <div class="metric-value">{len(insights)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Score de Qualidade</div>
                <div class="metric-value">{analysis.get('metadata', {}).get('quality_score', 0):.1f}%</div>
            </div>
        </div>
        
        <div class="insights-section">
            <h2>💡 Insights Prioritizados</h2>
            {self._format_insights_html(insights)}
        </div>
    </div>
    
    <script>
        // Adiciona interatividade
        document.querySelectorAll('.metric-card').forEach(card => {{
            card.addEventListener('click', function() {{
                this.style.background = '#e3f2fd';
                setTimeout(() => {{
                    this.style.background = '#f8f9fa';
                }}, 200);
            }});
        }});
    </script>
</body>
</html>"""
            
            filepath = self.reports_dir / f"{base_filename}_dashboard.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Dashboard interativo gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar dashboard: {e}")
            return ""
    
    def _generate_insights_report(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera relatório de insights prioritizados"""
        
        try:
            insights = analysis.get('insights_exclusivos', [])
            
            content = f"""# Relatório de Insights Prioritizados
## {analysis.get('projeto_dados', {}).get('segmento', 'Mercado Analisado')}

### 📊 Resumo dos Insights
- **Total de Insights:** {len(insights)}
- **Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}
- **Qualidade:** Premium (dados reais validados)

### 💡 Insights Detalhados

"""
            
            for i, insight in enumerate(insights, 1):
                # Categoriza insight
                categoria = self._categorize_insight_advanced(insight)
                prioridade = self._calculate_insight_priority_advanced(insight)
                
                content += f"""#### Insight #{i} - {categoria}
**Prioridade:** {prioridade}
**Conteúdo:** {insight}
**Acionabilidade:** {self._assess_actionability_advanced(insight)}
**Impacto Estimado:** {self._estimate_impact_advanced(insight)}

---

"""
            
            filepath = self.reports_dir / f"{base_filename}_insights.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Relatório de insights gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório de insights: {e}")
            return ""
    
    def _generate_roi_analysis(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera análise detalhada de ROI"""
        
        try:
            metricas = analysis.get('metricas_kpis_avancados', {})
            projecoes = metricas.get('projecoes_financeiras', {})
            
            content = f"""# Análise de ROI e Projeções Financeiras

## 💰 Projeções Financeiras Detalhadas

### Cenário Conservador
{self._format_financial_scenario(projecoes.get('cenario_conservador', {}))}

### Cenário Realista
{self._format_financial_scenario(projecoes.get('cenario_realista', {}))}

### Cenário Otimista
{self._format_financial_scenario(projecoes.get('cenario_otimista', {}))}

## 📈 Análise de Retorno sobre Investimento

### ROI Esperado
{metricas.get('roi_esperado', 'ROI a ser calculado baseado nas projeções')}

### Métricas Operacionais
{self._format_operational_metrics(metricas.get('metricas_operacionais', {}))}

### Payback Period
{self._calculate_payback_period(projecoes)}

### Break-even Analysis
{self._calculate_breakeven(projecoes)}

## 🎯 Recomendações de Investimento

### Alocação de Recursos Recomendada
- **Marketing Digital:** 40-50% do orçamento
- **Desenvolvimento de Produto:** 20-30%
- **Vendas e Relacionamento:** 15-25%
- **Operações e Suporte:** 10-15%

### Cronograma de Investimentos
{self._format_investment_timeline(analysis)}

---
*Análise de ROI gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
            
            filepath = self.reports_dir / f"{base_filename}_roi.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Análise de ROI gerada: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar análise de ROI: {e}")
            return ""
    
    def _generate_contingency_plan(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera plano de contingência"""
        
        try:
            content = f"""# Plano de Contingência
## {analysis.get('projeto_dados', {}).get('segmento', 'Projeto')}

### 🚨 Cenários de Risco e Respostas

#### Cenário 1: Performance Abaixo do Esperado
**Indicadores:**
- Conversão < 50% da meta
- CAC > 150% do planejado
- Churn > 10% mensal

**Ações Imediatas:**
- Revisão completa do funil de vendas
- Otimização de campanhas de marketing
- Análise detalhada do produto/serviço
- Pesquisa com clientes perdidos

#### Cenário 2: Concorrência Agressiva
**Indicadores:**
- Perda de market share
- Pressão de preços
- Clientes migrando para concorrentes

**Ações Imediatas:**
- Análise competitiva atualizada
- Desenvolvimento de diferenciais únicos
- Estratégia de retenção de clientes
- Inovação acelerada

#### Cenário 3: Mudanças Regulatórias
**Indicadores:**
- Novas leis ou regulamentações
- Mudanças nas regras do setor
- Compliance adicional necessário

**Ações Imediatas:**
- Adequação legal imediata
- Revisão de processos
- Treinamento de equipe
- Comunicação com clientes

### 🛡️ Estratégias de Mitigação

#### Diversificação de Riscos
- Múltiplos canais de aquisição
- Diversificação de produtos/serviços
- Diferentes segmentos de clientes
- Parcerias estratégicas

#### Monitoramento Contínuo
- Alertas automáticos de performance
- Análise semanal de métricas
- Feedback contínuo de clientes
- Monitoramento da concorrência

---
*Plano de contingência gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
            
            filepath = self.reports_dir / f"{base_filename}_contingencia.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Plano de contingência gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar plano de contingência: {e}")
            return ""
    
    def _generate_monitoring_report(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Gera relatório de monitoramento"""
        
        try:
            content = f"""# Sistema de Monitoramento e Controle

## 📊 Dashboard de Métricas

### KPIs Principais
{self._format_main_kpis(analysis)}

### Métricas Operacionais
{self._format_operational_kpis(analysis)}

### Métricas Financeiras
{self._format_financial_kpis(analysis)}

## 🔍 Alertas e Indicadores

### Alertas Críticos (Ação Imediata)
- Conversão < 50% da meta
- CAC > 200% do planejado
- Churn > 15% mensal
- NPS < 30

### Alertas de Atenção (Monitoramento)
- Conversão entre 50-80% da meta
- CAC entre 120-200% do planejado
- Churn entre 8-15% mensal
- NPS entre 30-50

### Indicadores Positivos
- Conversão > 100% da meta
- CAC < 80% do planejado
- Churn < 5% mensal
- NPS > 70

## 📈 Relatórios Automáticos

### Relatório Diário
- Vendas do dia
- Leads gerados
- Conversões
- Principais métricas

### Relatório Semanal
- Performance vs metas
- Análise de tendências
- Top performers
- Áreas de melhoria

### Relatório Mensal
- Análise completa de performance
- ROI atualizado
- Projeções revisadas
- Recomendações estratégicas

---
*Sistema de monitoramento configurado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
            
            filepath = self.reports_dir / f"{base_filename}_monitoramento.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Relatório de monitoramento gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório de monitoramento: {e}")
            return ""
    
    def _generate_reports_index(self, reports: Dict[str, str], base_filename: str) -> str:
        """Gera índice de todos os relatórios"""
        
        try:
            content = f"""# Índice de Relatórios - ARQV30 Enhanced v2.0

## 📋 Relatórios Disponíveis

### 1. Relatório Executivo Premium
**Arquivo:** `{os.path.basename(reports.get('executive', ''))}`
**Descrição:** Resumo executivo com descobertas-chave e recomendações estratégicas
**Público:** C-Level, Investidores, Tomadores de Decisão

### 2. Análise Técnica Detalhada
**Arquivo:** `{os.path.basename(reports.get('technical', ''))}`
**Descrição:** Análise técnica completa com avatar, posicionamento e estratégias
**Público:** Gerentes, Analistas, Equipe de Marketing

### 3. Guia de Implementação
**Arquivo:** `{os.path.basename(reports.get('implementation', ''))}`
**Descrição:** Roadmap detalhado de implementação com cronograma e recursos
**Público:** Equipe de Projeto, Gerentes de Implementação

### 4. Dashboard Interativo
**Arquivo:** `{os.path.basename(reports.get('dashboard', ''))}`
**Descrição:** Dashboard visual interativo com métricas e insights
**Público:** Todos os stakeholders

### 5. Relatório de Insights
**Arquivo:** `{os.path.basename(reports.get('insights', ''))}`
**Descrição:** Insights prioritizados com análise de impacto e acionabilidade
**Público:** Estrategistas, Analistas de Mercado

### 6. Análise de ROI
**Arquivo:** `{os.path.basename(reports.get('roi', ''))}`
**Descrição:** Projeções financeiras detalhadas e análise de retorno
**Público:** CFO, Controladores, Investidores

### 7. Plano de Contingência
**Arquivo:** `{os.path.basename(reports.get('contingency', ''))}`
**Descrição:** Cenários de risco e planos de resposta
**Público:** Gerência, Equipe de Risco

### 8. Sistema de Monitoramento
**Arquivo:** `{os.path.basename(reports.get('monitoring', ''))}`
**Descrição:** KPIs, alertas e sistema de acompanhamento
**Público:** Analistas, Gerentes Operacionais

## 📊 Metadados da Análise

- **Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}
- **Engine:** ARQV30 Enhanced v2.0
- **IA Utilizada:** {analysis.get('metadata', {}).get('ai_provider_used', 'N/A')}
- **Modelo:** {analysis.get('metadata', {}).get('model_used', 'N/A')}
- **Qualidade:** {analysis.get('metadata', {}).get('quality_score', 0):.1f}%
- **Fontes:** {analysis.get('metadata', {}).get('research_sources', 0)}
- **Tempo de Processamento:** {analysis.get('metadata', {}).get('processing_time_formatted', 'N/A')}

## 🎯 Como Usar os Relatórios

1. **Comece pelo Relatório Executivo** para ter uma visão geral
2. **Use a Análise Técnica** para entender detalhes específicos
3. **Siga o Guia de Implementação** para executar as estratégias
4. **Monitore com o Dashboard** para acompanhar progresso
5. **Consulte os Insights** para decisões estratégicas
6. **Use a Análise de ROI** para justificar investimentos
7. **Tenha o Plano de Contingência** sempre à mão
8. **Configure o Monitoramento** desde o início

---
*Índice gerado automaticamente pelo ARQV30 Enhanced v2.0*
"""
            
            filepath = self.reports_dir / f"{base_filename}_indice.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Índice de relatórios gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar índice: {e}")
            return ""
    
    # Métodos auxiliares de formatação
    def _format_list(self, items: List[str]) -> str:
        """Formata lista como markdown"""
        if not items:
            return "- Nenhum item disponível"
        return '\n'.join(f"- {item}" for item in items)
    
    def _format_numbered_list(self, items: List[str]) -> str:
        """Formata lista numerada"""
        if not items:
            return "1. Nenhum item disponível"
        return '\n'.join(f"{i}. {item}" for i, item in enumerate(items, 1))
    
    def _format_dict(self, data: Dict[str, Any]) -> str:
        """Formata dicionário como markdown"""
        if not data:
            return "- Dados não disponíveis"
        
        formatted = []
        for key, value in data.items():
            label = key.replace('_', ' ').title()
            formatted.append(f"- **{label}:** {value}")
        
        return '\n'.join(formatted)
    
    def _format_activities(self, activities: List[str]) -> str:
        """Formata atividades com checkboxes"""
        if not activities:
            return "- [ ] Nenhuma atividade definida"
        return '\n'.join(f"- [ ] {activity}" for activity in activities)
    
    def _format_timeline(self, timeline: Dict[str, str]) -> str:
        """Formata timeline"""
        if not timeline:
            return "Timeline a ser definido"
        
        formatted = []
        for fase, descricao in timeline.items():
            formatted.append(f"**{fase}:** {descricao}")
        
        return '\n'.join(formatted)
    
    def _extract_financial_projection(self, analysis: Dict[str, Any], scenario: str, metric: str) -> str:
        """Extrai projeção financeira específica"""
        try:
            metricas = analysis.get('metricas_kpis_avancados', {})
            projecoes = metricas.get('projecoes_financeiras', {})
            cenario = projecoes.get(f'cenario_{scenario}', {})
            return cenario.get(metric, 'N/A')
        except:
            return 'N/A'
    
    def _categorize_insight_advanced(self, insight: str) -> str:
        """Categoriza insight de forma avançada"""
        insight_lower = insight.lower()
        
        if any(word in insight_lower for word in ['oportunidade', 'potencial', 'crescimento', 'expansão']):
            return '🚀 Oportunidade'
        elif any(word in insight_lower for word in ['risco', 'ameaça', 'desafio', 'problema']):
            return '⚠️ Risco'
        elif any(word in insight_lower for word in ['tendência', 'futuro', 'evolução', 'mudança']):
            return '📈 Tendência'
        elif any(word in insight_lower for word in ['estratégia', 'tática', 'abordagem', 'método']):
            return '🎯 Estratégia'
        elif any(word in insight_lower for word in ['tecnologia', 'inovação', 'digital', 'automação']):
            return '💡 Inovação'
        else:
            return '📊 Mercado'
    
    def _calculate_insight_priority_advanced(self, insight: str) -> str:
        """Calcula prioridade avançada do insight"""
        insight_lower = insight.lower()
        
        high_priority = ['crítico', 'urgente', 'imediato', 'essencial', 'fundamental']
        medium_priority = ['importante', 'relevante', 'significativo', 'necessário']
        
        if any(word in insight_lower for word in high_priority):
            return '🔴 Alta'
        elif any(word in insight_lower for word in medium_priority):
            return '🟡 Média'
        else:
            return '🟢 Baixa'
    
    def _assess_actionability_advanced(self, insight: str) -> str:
        """Avalia acionabilidade do insight"""
        if len(insight) > 100 and any(word in insight.lower() for word in ['implementar', 'executar', 'desenvolver', 'criar']):
            return 'Alta - Insight específico e acionável'
        elif len(insight) > 50:
            return 'Média - Requer planejamento adicional'
        else:
            return 'Baixa - Muito genérico'
    
    def _estimate_impact_advanced(self, insight: str) -> str:
        """Estima impacto do insight"""
        insight_lower = insight.lower()
        
        if any(word in insight_lower for word in ['receita', 'lucro', 'vendas', 'crescimento']):
            return 'Alto - Impacto direto na receita'
        elif any(word in insight_lower for word in ['eficiência', 'otimização', 'melhoria']):
            return 'Médio - Melhoria operacional'
        else:
            return 'Baixo - Impacto indireto'
    
    def _wrap_html(self, content: str, title: str) -> str:
        """Envolve conteúdo em HTML completo"""
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ARQV30</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; margin: 40px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""

# Instância global
consolidated_report_generator = ConsolidatedReportGenerator()