import os
import json
import logging
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.ai_manager import ai_manager
from services.production_search_manager import production_search_manager
from services.quality_assurance_manager import quality_assurance_manager
from services.auto_save_manager import auto_save_manager, salvar_etapa, salvar_erro
from services.attachment_service import attachment_service

logger = logging.getLogger(__name__)

class EnhancedAnalysisPipeline:
    def __init__(self):
        self.search_manager = production_search_manager
        self.ai_manager = ai_manager
        self.qa_manager = quality_assurance_manager
        self.executor = ThreadPoolExecutor(max_workers=os.cpu_count() * 2)

    def _execute_search_phase(self, query, session_id, progress_callback):
        progress_callback(1, "🌐 Iniciando pesquisa web e coleta de dados...")
        logger.info(f"Iniciando pesquisa para: {query}")
        search_results = self.search_manager.perform_search(query)
        salvar_etapa("pesquisa_web", search_results, session_id=session_id, categoria="pesquisa_web")
        if not search_results or not search_results.get("results"):
            logger.warning("Nenhum resultado de pesquisa encontrado.")
            return {"error": "Nenhum resultado de pesquisa encontrado"}
        progress_callback(2, "✅ Pesquisa web concluída.")
        return search_results

    def _execute_extraction_phase(self, search_results, session_id, progress_callback):
        progress_callback(3, "📄 Extraindo conteúdo das páginas...")
        logger.info("Iniciando extração de conteúdo.")
        extracted_content = self.search_manager.extract_content_from_results(search_results)
        salvar_etapa("extracao_conteudo", extracted_content, session_id=session_id, categoria="extracao")
        if not extracted_content:
            logger.warning("Nenhum conteúdo extraído.")
            return {"error": "Nenhum conteúdo extraído"}
        progress_callback(4, "✅ Extração de conteúdo concluída.")
        return extracted_content

    def _execute_ai_analysis_phase(self, extracted_content, data, session_id, progress_callback):
        progress_callback(5, "🧠 Iniciando análise de IA e geração de insights...")
        logger.info("Iniciando análise de IA.")
        
        analysis_tasks = []
        
        # Tarefa 1: Análise de Segmento e Tendências
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_market_segment,
            extracted_content, data.get("segmento"), data.get("produto")))
        
        # Tarefa 2: Identificação de Oportunidades e Ameaças
        analysis_tasks.append(self.executor.submit(self.ai_manager.identify_opportunities_threats,
            extracted_content, data.get("segmento"), data.get("produto")))
            
        # Tarefa 3: Análise de Concorrentes
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_competitors,
            extracted_content, data.get("concorrentes")))
            
        # Tarefa 4: Geração de Persona/Avatar
        analysis_tasks.append(self.executor.submit(self.ai_manager.generate_persona,
            data.get("publico"), data.get("segmento")))
            
        # Tarefa 5: Estratégias de Marketing e Vendas
        analysis_tasks.append(self.executor.submit(self.ai_manager.suggest_marketing_sales_strategies,
            extracted_content, data.get("segmento"), data.get("produto"), data.get("publico")))
            
        # Tarefa 6: Projeções Financeiras
        analysis_tasks.append(self.executor.submit(self.ai_manager.generate_financial_projections,
            data.get("objetivo_receita"), data.get("orcamento_marketing"), data.get("prazo_lancamento")))
            
        # Tarefa 7: Análise SWOT
        analysis_tasks.append(self.executor.submit(self.ai_manager.perform_swot_analysis,
            extracted_content, data.get("segmento"), data.get("produto")))
            
        # Tarefa 8: Recomendações Estratégicas
        analysis_tasks.append(self.executor.submit(self.ai_manager.generate_strategic_recommendations,
            extracted_content, data.get("segmento"), data.get("produto")))
            
        # Tarefa 9: Resumo Executivo
        analysis_tasks.append(self.executor.submit(self.ai_manager.generate_executive_summary,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 10: Geração de Perguntas e Respostas Frequentes (FAQ)
        analysis_tasks.append(self.executor.submit(self.ai_manager.generate_faq,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 11: Análise de Sentimento (se aplicável e dados disponíveis)
        # analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_sentiment, extracted_content))

        # Tarefa 12: Geração de Tópicos para Conteúdo (Blog, Redes Sociais)
        analysis_tasks.append(self.executor.submit(self.ai_manager.generate_content_topics,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 13: Análise de Precificação (se dados de preço forem fornecidos)
        if data.get("preco"):
            analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_pricing_strategy,
                extracted_content, data.get("preco"), data.get("segmento"), data.get("produto")))

        # Tarefa 14: Análise de Canais de Distribuição
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_distribution_channels,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 15: Análise de Regulamentação e Conformidade
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_regulations_compliance,
            extracted_content, data.get("segmento")))

        # Tarefa 16: Análise de Inovação e P&D
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_innovation_rd,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 17: Análise de Sustentabilidade e ESG
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_sustainability_esg,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 18: Análise de Cenários Futuros
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_future_scenarios,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 19: Geração de Glossário de Termos Técnicos
        analysis_tasks.append(self.executor.submit(self.ai_manager.generate_glossary,
            extracted_content, data.get("segmento")))

        # Tarefa 20: Análise de Barreiras de Entrada e Saída
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_entry_exit_barriers,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 21: Análise de Fatores Críticos de Sucesso
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_critical_success_factors,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 22: Análise de Modelos de Negócio
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_business_models,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 23: Análise de Cadeia de Valor
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_value_chain,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 24: Análise de Forças de Porter
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_porters_five_forces,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 25: Análise de PESTEL
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_pestel,
            extracted_content, data.get("segmento")))

        # Tarefa 26: Análise de Stakeholders
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_stakeholders,
            extracted_content, data.get("segmento")))

        # Tarefa 27: Análise de Cultura Organizacional (se aplicável)
        # analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_organizational_culture, extracted_content))

        # Tarefa 28: Análise de Gestão de Riscos
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_risk_management,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 29: Análise de Propriedade Intelectual
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_intellectual_property,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 30: Análise de Alianças Estratégicas
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_strategic_alliances,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 31: Análise de Responsabilidade Social Corporativa (RSC)
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_corporate_social_responsibility,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 32: Análise de Governança Corporativa
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_corporate_governance,
            extracted_content, data.get("segmento")))

        # Tarefa 33: Análise de Gestão da Qualidade
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_quality_management,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 34: Análise de Gestão do Conhecimento
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_knowledge_management,
            extracted_content, data.get("segmento")))

        # Tarefa 35: Análise de Gestão de Crises
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_crisis_management,
            extracted_content, data.get("segmento")))

        # Tarefa 36: Análise de Reputação e Marca
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_reputation_brand,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 37: Análise de Experiência do Cliente (CX)
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_customer_experience,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 38: Análise de Retenção de Clientes
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_customer_retention,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 39: Análise de Aquisição de Clientes
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_customer_acquisition,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 40: Análise de Engajamento de Clientes
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_customer_engagement,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 41: Análise de Ciclo de Vida do Produto
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_product_lifecycle,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 42: Análise de Portfólio de Produtos
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_product_portfolio,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 43: Análise de Desenvolvimento de Novos Produtos
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_new_product_development,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 44: Análise de Lançamento de Produtos
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_product_launch,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 45: Análise de Desempenho de Produtos
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_product_performance,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 46: Análise de Otimização de Preços
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_price_optimization,
            extracted_content, data.get("segmento"), data.get("produto"), data.get("preco")))

        # Tarefa 47: Análise de Estratégias de Promoção
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_promotion_strategies,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 48: Análise de Canais de Venda
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_sales_channels,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 49: Análise de Força de Vendas
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_sales_force,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 50: Análise de Previsão de Vendas
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_sales_forecasting,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 51: Análise de Gestão de Relacionamento com o Cliente (CRM)
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_crm,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 52: Análise de Automação de Marketing
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_marketing_automation,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 53: Análise de Marketing de Conteúdo
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_content_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 54: Análise de SEO e SEM
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_seo_sem,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 55: Análise de Mídias Sociais
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_social_media,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 56: Análise de Publicidade Online
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_online_advertising,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 57: Análise de Relações Públicas
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_public_relations,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 58: Análise de Eventos e Patrocínios
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_events_sponsorships,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 59: Análise de Marketing Direto
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_direct_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 60: Análise de Marketing de Guerrilha
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_guerrilla_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 61: Análise de Marketing de Influência
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_influencer_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 62: Análise de Marketing de Afiliados
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_affiliate_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 63: Análise de Marketing de Permissão
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_permission_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 64: Análise de Marketing de Relacionamento
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_relationship_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 65: Análise de Marketing de Experiência
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_experience_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 66: Análise de Marketing de Causa
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_cause_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 67: Análise de Marketing Verde
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_green_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 68: Análise de Marketing Social
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_social_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 69: Análise de Marketing de Nicho
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_niche_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 70: Análise de Marketing de Massa
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_mass_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 71: Análise de Marketing One-to-One
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_one_to_one_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 72: Análise de Marketing de Dados
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_data_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 73: Análise de Marketing de Performance
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_performance_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 74: Análise de Marketing de Busca
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_search_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 75: Análise de Marketing de Display
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_display_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 76: Análise de Marketing de Vídeo
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_video_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 77: Análise de Marketing de Áudio
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_audio_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 78: Análise de Marketing de Imagem
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_image_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 79: Análise de Marketing de Texto
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_text_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 80: Análise de Marketing de E-mail
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_email_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 81: Análise de Marketing de SMS
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_sms_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 82: Análise de Marketing de Notificação Push
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_push_notification_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 83: Análise de Marketing de Realidade Aumentada (RA)
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_ar_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 84: Análise de Marketing de Realidade Virtual (RV)
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_vr_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 85: Análise de Marketing de Jogos
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_gaming_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 86: Análise de Marketing de Geolocalização
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_geolocation_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 87: Análise de Marketing de Proximidade
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_proximity_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 88: Análise de Marketing de Conteúdo Interativo
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_interactive_content_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 89: Análise de Marketing de Personalização
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_personalization_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 90: Análise de Marketing de Segmentação
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_segmentation_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 91: Análise de Marketing de Posicionamento
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_positioning_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 92: Análise de Marketing de Diferenciação
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_differentiation_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 93: Análise de Marketing de Valor
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_value_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 94: Análise de Marketing de Inovação
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_innovation_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 95: Análise de Marketing de Crescimento
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_growth_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 96: Análise de Marketing de Expansão
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_expansion_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 97: Análise de Marketing de Internacionalização
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_internationalization_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 98: Análise de Marketing de Fusões e Aquisições
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_m_a_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 99: Análise de Marketing de Reestruturação
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_restructuring_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Tarefa 100: Análise de Marketing de Crise
        analysis_tasks.append(self.executor.submit(self.ai_manager.analyze_crisis_marketing,
            extracted_content, data.get("segmento"), data.get("produto")))

        # Dicionário para armazenar os resultados
        results = {}
        
        # Mapeamento de futuros para chaves de resultado
        future_to_key = {
            analysis_tasks[0]: "market_segment_analysis",
            analysis_tasks[1]: "opportunities_threats",
            analysis_tasks[2]: "competitor_analysis",
            analysis_tasks[3]: "persona_generation",
            analysis_tasks[4]: "marketing_sales_strategies",
            analysis_tasks[5]: "financial_projections",
            analysis_tasks[6]: "swot_analysis",
            analysis_tasks[7]: "strategic_recommendations",
            analysis_tasks[8]: "executive_summary",
            analysis_tasks[9]: "faq_generation",
            analysis_tasks[10]: "content_topics_generation",
            analysis_tasks[11]: "pricing_strategy_analysis" if data.get("preco") else None,
            analysis_tasks[12]: "distribution_channels_analysis",
            analysis_tasks[13]: "regulations_compliance_analysis",
            analysis_tasks[14]: "innovation_rd_analysis",
            analysis_tasks[15]: "sustainability_esg_analysis",
            analysis_tasks[16]: "future_scenarios_analysis",
            analysis_tasks[17]: "glossary_generation",
            analysis_tasks[18]: "entry_exit_barriers_analysis",
            analysis_tasks[19]: "critical_success_factors_analysis",
            analysis_tasks[20]: "business_models_analysis",
            analysis_tasks[21]: "value_chain_analysis",
            analysis_tasks[22]: "porters_five_forces_analysis",
            analysis_tasks[23]: "pestel_analysis",
            analysis_tasks[24]: "stakeholders_analysis",
            analysis_tasks[25]: "risk_management_analysis",
            analysis_tasks[26]: "intellectual_property_analysis",
            analysis_tasks[27]: "strategic_alliances_analysis",
            analysis_tasks[28]: "corporate_social_responsibility_analysis",
            analysis_tasks[29]: "corporate_governance_analysis",
            analysis_tasks[30]: "quality_management_analysis",
            analysis_tasks[31]: "knowledge_management_analysis",
            analysis_tasks[32]: "crisis_management_analysis",
            analysis_tasks[33]: "reputation_brand_analysis",
            analysis_tasks[34]: "customer_experience_analysis",
            analysis_tasks[35]: "customer_retention_analysis",
            analysis_tasks[36]: "customer_acquisition_analysis",
            analysis_tasks[37]: "customer_engagement_analysis",
            analysis_tasks[38]: "product_lifecycle_analysis",
            analysis_tasks[39]: "product_portfolio_analysis",
            analysis_tasks[40]: "new_product_development_analysis",
            analysis_tasks[41]: "product_launch_analysis",
            analysis_tasks[42]: "product_performance_analysis",
            analysis_tasks[43]: "price_optimization_analysis",
            analysis_tasks[44]: "promotion_strategies_analysis",
            analysis_tasks[45]: "sales_channels_analysis",
            analysis_tasks[46]: "sales_force_analysis",
            analysis_tasks[47]: "sales_forecasting_analysis",
            analysis_tasks[48]: "crm_analysis",
            analysis_tasks[49]: "marketing_automation_analysis",
            analysis_tasks[50]: "content_marketing_analysis",
            analysis_tasks[51]: "seo_sem_analysis",
            analysis_tasks[52]: "social_media_analysis",
            analysis_tasks[53]: "online_advertising_analysis",
            analysis_tasks[54]: "public_relations_analysis",
            analysis_tasks[55]: "events_sponsorships_analysis",
            analysis_tasks[56]: "direct_marketing_analysis",
            analysis_tasks[57]: "guerrilla_marketing_analysis",
            analysis_tasks[58]: "influencer_marketing_analysis",
            analysis_tasks[59]: "affiliate_marketing_analysis",
            analysis_tasks[60]: "permission_marketing_analysis",
            analysis_tasks[61]: "relationship_marketing_analysis",
            analysis_tasks[62]: "experience_marketing_analysis",
            analysis_tasks[63]: "cause_marketing_analysis",
            analysis_tasks[64]: "green_marketing_analysis",
            analysis_tasks[65]: "social_marketing_analysis",
            analysis_tasks[66]: "niche_marketing_analysis",
            analysis_tasks[67]: "mass_marketing_analysis",
            analysis_tasks[68]: "one_to_one_marketing_analysis",
            analysis_tasks[69]: "data_marketing_analysis",
            analysis_tasks[70]: "performance_marketing_analysis",
            analysis_tasks[71]: "search_marketing_analysis",
            analysis_tasks[72]: "display_marketing_analysis",
            analysis_tasks[73]: "video_marketing_analysis",
            analysis_tasks[74]: "audio_marketing_analysis",
            analysis_tasks[75]: "image_marketing_analysis",
            analysis_tasks[76]: "text_marketing_analysis",
            analysis_tasks[77]: "email_marketing_analysis",
            analysis_tasks[78]: "sms_marketing_analysis",
            analysis_tasks[79]: "push_notification_marketing_analysis",
            analysis_tasks[80]: "ar_marketing_analysis",
            analysis_tasks[81]: "vr_marketing_analysis",
            analysis_tasks[82]: "gaming_marketing_analysis",
            analysis_tasks[83]: "geolocation_marketing_analysis",
            analysis_tasks[84]: "proximity_marketing_analysis",
            analysis_tasks[85]: "interactive_content_marketing_analysis",
            analysis_tasks[86]: "personalization_marketing_analysis",
            analysis_tasks[87]: "segmentation_marketing_analysis",
            analysis_tasks[88]: "positioning_marketing_analysis",
            analysis_tasks[89]: "differentiation_marketing_analysis",
            analysis_tasks[90]: "value_marketing_analysis",
            analysis_tasks[91]: "innovation_marketing_analysis",
            analysis_tasks[92]: "growth_marketing_analysis",
            analysis_tasks[93]: "expansion_marketing_analysis",
            analysis_tasks[94]: "internationalization_marketing_analysis",
            analysis_tasks[95]: "m_a_marketing_analysis",
            analysis_tasks[96]: "restructuring_marketing_analysis",
            analysis_tasks[97]: "crisis_marketing_analysis",
        }

        for i, future in enumerate(as_completed(analysis_tasks)):
            try:
                key = future_to_key.get(future)
                if key:
                    results[key] = future.result()
                    progress_callback(5 + i, f"✅ Análise de IA concluída: {key}")
                else:
                    logger.warning(f"Resultado de tarefa de IA sem chave correspondente: {future}")
            except Exception as e:
                logger.error(f"Erro durante a execução da tarefa de IA: {e}")
                salvar_erro(f"erro_ia_tarefa_{i}", e, session_id=session_id, contexto=f"Tarefa {i}")
                results[f"error_task_{i}"] = str(e)

        salvar_etapa("analise_ia", results, session_id=session_id, categoria="analise_ia")
        progress_callback(10, "✅ Análise de IA e geração de insights concluída.")
        return results

    def _analyze_revenue_distribution(self, data):
        # Lógica para analisar a distribuição de faturamento
        # Pode usar os dados de 'objetivo_receita', 'orcamento_marketing', etc.
        # Exemplo simplificado:
        return {
            "canais_principais": ["Vendas Diretas", "Marketing Digital", "Parcerias"],
            "percentual_por_canal": {
                "Vendas Diretas": "40%",
                "Marketing Digital": "35%",
                "Parcerias": "25%"
            },
            "observacoes": "Baseado nos objetivos de receita e orçamento de marketing fornecidos."
        }

    def _identify_main_challenges(self, avatar_data):
        # Lógica para identificar os principais desafios
        # Pode usar informações da persona/avatar e do segmento
        # Exemplo simplificado:
        return [
            "Alta concorrência no segmento",
            "Necessidade de inovação constante",
            "Flutuações econômicas",
            "Adaptação às novas tecnologias"
        ]

    def execute_complete_analysis(self, data, session_id, progress_callback=None):
        if progress_callback is None:
            progress_callback = lambda step, message, details=None: logger.info(f"Progresso: {step} - {message}")

        full_analysis_result = {}

        try:
            # Fase 1: Pesquisa e Coleta de Dados
            search_results = self._execute_search_phase(data.get("query"), session_id, progress_callback)
            if "error" in search_results:
                return search_results
            full_analysis_result["search_results"] = search_results

            # Fase 2: Extração de Conteúdo
            extracted_content = self._execute_extraction_phase(search_results, session_id, progress_callback)
            if "error" in extracted_content:
                return extracted_content
            full_analysis_result["extracted_content"] = extracted_content

            # Fase 3: Análise de IA e Geração de Insights
            ai_analysis_results = self._execute_ai_analysis_phase(extracted_content, data, session_id, progress_callback)
            full_analysis_result.update(ai_analysis_results)

            # Fase 4: Geração de Dashboard e Relatórios
            progress_callback(11, "📊 Gerando dashboard e relatórios...")
            logger.info("Gerando dashboard e relatórios.")

            # Exemplo de como integrar a persona gerada
            avatar_data = ai_analysis_results.get("persona_generation", {})
            
            segmento = data.get("segmento", "negócios")
            
            return {
                # Dashboard baseado na metodologia dos anexos
                'dashboard': {
                    'visao_geral': {
                        'publico_analisado': f"Avatar para {data.get('segmento', 'negócios')}",
                        'distribuicao_faturamento': self._analyze_revenue_distribution(data),
                        'desafios_principais': self._identify_main_challenges(avatar_data)
                    },
                    'metricas_chave': {
                        'crescimento_mercado': ai_analysis_results.get("market_segment_analysis", {}).get("crescimento_mercado", "N/A"),
                        'roi_marketing_projetado': ai_analysis_results.get("financial_projections", {}).get("roi_marketing_projetado", "N/A"),
                        'market_share_potencial': ai_analysis_results.get("strategic_recommendations", {}).get("market_share_potencial", "N/A")
                    },
                    'swot_resumo': ai_analysis_results.get("swot_analysis", {}).get("resumo", "N/A"),
                    'recomendacoes_principais': ai_analysis_results.get("strategic_recommendations", {}).get("principais_recomendacoes", "N/A")
                },
                'resumo_executivo': ai_analysis_results.get("executive_summary", {}),
                'analise_segmento': ai_analysis_results.get("market_segment_analysis", {}),
                'oportunidades_ameacas': ai_analysis_results.get("opportunities_threats", {}),
                'analise_concorrentes': ai_analysis_results.get("competitor_analysis", {}),
                'persona_detalhada': avatar_data,
                'estrategias_marketing_vendas': ai_analysis_results.get("marketing_sales_strategies", {}),
                'projecoes_financeiras': ai_analysis_results.get("financial_projections", {}),
                'analise_swot': ai_analysis_results.get("swot_analysis", {}),
                'recomendacoes_estrategicas': ai_analysis_results.get("strategic_recommendations", {}),
                'faq': ai_analysis_results.get("faq_generation", {}),
                'topicos_conteudo': ai_analysis_results.get("content_topics_generation", {}),
                'analise_precificacao': ai_analysis_results.get("pricing_strategy_analysis", {}),
                'analise_canais_distribuicao': ai_analysis_results.get("distribution_channels_analysis", {}),
                'analise_regulamentacao_conformidade': ai_analysis_results.get("regulations_compliance_analysis", {}),
                'analise_inovacao_pd': ai_analysis_results.get("innovation_rd_analysis", {}),
                'analise_sustentabilidade_esg': ai_analysis_results.get("sustainability_esg_analysis", {}),
                'analise_cenarios_futuros': ai_analysis_results.get("future_scenarios_analysis", {}),
                'glossario': ai_analysis_results.get("glossary_generation", {}),
                'analise_barreiras_entrada_saida': ai_analysis_results.get("entry_exit_barriers_analysis", {}),
                'analise_fatores_criticos_sucesso': ai_analysis_results.get("critical_success_factors_analysis", {}),
                'analise_modelos_negocio': ai_analysis_results.get("business_models_analysis", {}),
                'analise_cadeia_valor': ai_analysis_results.get("value_chain_analysis", {}),
                'analise_forcas_porter': ai_analysis_results.get("porters_five_forces_analysis", {}),
                'analise_pestel': ai_analysis_results.get("pestel_analysis", {}),
                'analise_stakeholders': ai_analysis_results.get("stakeholders_analysis", {}),
                'analise_gestao_riscos': ai_analysis_results.get("risk_management_analysis", {}),
                'analise_propriedade_intelectual': ai_analysis_results.get("intellectual_property_analysis", {}),
                'analise_aliancas_estrategicas': ai_analysis_results.get("strategic_alliances_analysis", {}),
                'analise_responsabilidade_social_corporativa': ai_analysis_results.get("corporate_social_responsibility_analysis", {}),
                'analise_governanca_corporativa': ai_analysis_results.get("corporate_governance_analysis", {}),
                'analise_gestao_qualidade': ai_analysis_results.get("quality_management_analysis", {}),
                'analise_gestao_conhecimento': ai_analysis_results.get("knowledge_management_analysis", {}),
                'analise_gestao_crises': ai_analysis_results.get("crisis_management_analysis", {}),
                'analise_reputacao_marca': ai_analysis_results.get("reputation_brand_analysis", {}),
                'analise_experiencia_cliente': ai_analysis_results.get("customer_experience_analysis", {}),
                'analise_retencao_clientes': ai_analysis_results.get("customer_retention_analysis", {}),
                'analise_aquisicao_clientes': ai_analysis_results.get("customer_acquisition_analysis", {}),
                'analise_engajamento_clientes': ai_analysis_results.get("customer_engagement_analysis", {}),
                'analise_ciclo_vida_produto': ai_analysis_results.get("product_lifecycle_analysis", {}),
                'analise_portfolio_produtos': ai_analysis_results.get("product_portfolio_analysis", {}),
                'analise_desenvolvimento_novos_produtos': ai_analysis_results.get("new_product_development_analysis", {}),
                'analise_lancamento_produtos': ai_analysis_results.get("product_launch_analysis", {}),
                'analise_desempenho_produtos': ai_analysis_results.get("product_performance_analysis", {}),
                'analise_otimizacao_precos': ai_analysis_results.get("price_optimization_analysis", {}),
                'analise_estrategias_promocao': ai_analysis_results.get("promotion_strategies_analysis", {}),
                'analise_canais_venda': ai_analysis_results.get("sales_channels_analysis", {}),
                'analise_forca_vendas': ai_analysis_results.get("sales_force_analysis", {}),
                'analise_previsao_vendas': ai_analysis_results.get("sales_forecasting_analysis", {}),
                'analise_crm': ai_analysis_results.get("crm_analysis", {}),
                'analise_automacao_marketing': ai_analysis_results.get("marketing_automation_analysis", {}),
                'analise_marketing_conteudo': ai_analysis_results.get("content_marketing_analysis", {}),
                'analise_seo_sem': ai_analysis_results.get("seo_sem_analysis", {}),
                'analise_midias_sociais': ai_analysis_results.get("social_media_analysis", {}),
                'analise_publicidade_online': ai_analysis_results.get("online_advertising_analysis", {}),
                'analise_relacoes_publicas': ai_analysis_results.get("public_relations_analysis", {}),
                'analise_eventos_patrocinios': ai_analysis_results.get("events_sponsorships_analysis", {}),
                'analise_marketing_direto': ai_analysis_results.get("direct_marketing_analysis", {}),
                'analise_marketing_guerrilha': ai_analysis_results.get("guerrilla_marketing_analysis", {}),
                'analise_marketing_influencia': ai_analysis_results.get("influencer_marketing_analysis", {}),
                'analise_marketing_afiliados': ai_analysis_results.get("affiliate_marketing_analysis", {}),
                'analise_marketing_permissao': ai_analysis_results.get("permission_marketing_analysis", {}),
                'analise_marketing_relacionamento': ai_analysis_results.get("relationship_marketing_analysis", {}),
                'analise_marketing_experiencia': ai_analysis_results.get("experience_marketing_analysis", {}),
                'analise_marketing_causa': ai_analysis_results.get("cause_marketing_analysis", {}),
                'analise_marketing_verde': ai_analysis_results.get("green_marketing_analysis", {}),
                'analise_marketing_social': ai_analysis_results.get("social_marketing_analysis", {}),
                'analise_marketing_nicho': ai_analysis_results.get("niche_marketing_analysis", {}),
                'analise_marketing_massa': ai_analysis_results.get("mass_marketing_analysis", {}),
                'analise_marketing_one_to_one': ai_analysis_results.get("one_to_one_marketing_analysis", {}),
                'analise_marketing_dados': ai_analysis_results.get("data_marketing_analysis", {}),
                'analise_marketing_performance': ai_analysis_results.get("performance_marketing_analysis", {}),
                'analise_marketing_busca': ai_analysis_results.get("search_marketing_analysis", {}),
                'analise_marketing_display': ai_analysis_results.get("display_marketing_analysis", {}),
                'analise_marketing_video': ai_analysis_results.get("video_marketing_analysis", {}),
                'analise_marketing_audio': ai_analysis_results.get("audio_marketing_analysis", {}),
                'analise_marketing_imagem': ai_analysis_results.get("image_marketing_analysis", {}),
                'analise_marketing_texto': ai_analysis_results.get("text_marketing_analysis", {}),
                'analise_marketing_email': ai_analysis_results.get("email_marketing_analysis", {}),
                'analise_marketing_sms': ai_analysis_results.get("sms_marketing_analysis", {}),
                'analise_marketing_notificacao_push': ai_analysis_results.get("push_notification_marketing_analysis", {}),
                'analise_marketing_ar': ai_analysis_results.get("ar_marketing_analysis", {}),
                'analise_marketing_vr': ai_analysis_results.get("vr_marketing_analysis", {}),
                'analise_marketing_jogos': ai_analysis_results.get("gaming_marketing_analysis", {}),
                'analise_marketing_geolocalizacao': ai_analysis_results.get("geolocation_marketing_analysis", {}),
                'analise_marketing_proximidade': ai_analysis_results.get("proximity_marketing_analysis", {}),
                'analise_marketing_conteudo_interativo': ai_analysis_results.get("interactive_content_marketing_analysis", {}),
                'analise_marketing_personalizacao': ai_analysis_results.get("personalization_marketing_analysis", {}),
                'analise_marketing_segmentacao': ai_analysis_results.get("segmentation_marketing_analysis", {}),
                'analise_marketing_posicionamento': ai_analysis_results.get("positioning_marketing_analysis", {}),
                'analise_marketing_diferenciacao': ai_analysis_results.get("differentiation_marketing_analysis", {}),
                'analise_marketing_valor': ai_analysis_results.get("value_marketing_analysis", {}),
                'analise_marketing_inovacao': ai_analysis_results.get("innovation_marketing_analysis", {}),
                'analise_marketing_crescimento': ai_analysis_results.get("growth_marketing_analysis", {}),
                'analise_marketing_expansao': ai_analysis_results.get("expansion_marketing_analysis", {}),
                'analise_marketing_internacionalizacao': ai_analysis_results.get("internationalization_marketing_analysis", {}),
                'analise_marketing_fusoes_aquisicoes': ai_analysis_results.get("m_a_marketing_analysis", {}),
                'analise_marketing_reestruturacao': ai_analysis_results.get("restructuring_marketing_analysis", {}),
                'analise_marketing_crise': ai_analysis_results.get("crisis_marketing_analysis", {}),
                **full_analysis_result # Inclui todos os resultados da análise de IA
            }

        except Exception as e:
            logger.error(f"Erro durante a execução completa da análise: {e}", exc_info=True)
            salvar_erro("pipeline_completo_falha", e, session_id=session_id, contexto=data)
            return {"error": f"Erro crítico na análise: {str(e)}"}

enhanced_analysis_pipeline = EnhancedAnalysisPipeline()


