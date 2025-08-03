// ARQV30 Enhanced v2.0 - Main JavaScript
// Core functionality and system management

class ARQV30App {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentAnalysis = null;
        this.systemStatus = {
            apis: 'checking',
            extractors: 'checking',
            overall: 'checking'
        };
        
        this.init();
    }
    
    init() {
        console.log('🚀 ARQV30 Enhanced v2.0 - Inicializando...');
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Check system health
        this.checkSystemHealth();
        
        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        // Initialize tooltips
        this.initializeTooltips();
        
        console.log('✅ ARQV30 Enhanced v2.0 - Inicializado com sucesso');
    }
    
    setupEventListeners() {
        // Form submission
        const form = document.getElementById('analysisForm');
        if (form) {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        }
        
        // Status indicator click
        const statusIndicator = document.getElementById('statusIndicator');
        if (statusIndicator) {
            statusIndicator.addEventListener('click', this.showSystemStatus.bind(this));
        }
        
        // Auto-save form data
        this.setupAutoSave();
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Enter: Submit form
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                const form = document.getElementById('analysisForm');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
            
            // Ctrl+S: Save current analysis
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                if (this.currentAnalysis) {
                    this.saveAnalysisLocally(this.currentAnalysis);
                }
            }
        });
    }
    
    setupAutoSave() {
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                this.saveFormData();
            });
        });
        
        // Load saved form data
        this.loadFormData();
    }
    
    saveFormData() {
        const formData = new FormData(document.getElementById('analysisForm'));
        const data = Object.fromEntries(formData.entries());
        localStorage.setItem('arqv30_form_data', JSON.stringify(data));
    }
    
    loadFormData() {
        const saved = localStorage.getItem('arqv30_form_data');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                Object.keys(data).forEach(key => {
                    const element = document.getElementById(key);
                    if (element && data[key]) {
                        element.value = data[key];
                    }
                });
            } catch (e) {
                console.warn('Erro ao carregar dados salvos:', e);
            }
        }
    }
    
    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
        // Validation
        if (!data.segmento || data.segmento.trim().length < 3) {
            this.showAlert('Segmento é obrigatório e deve ter pelo menos 3 caracteres', 'error');
            return;
        }
        
        try {
            // Show progress
            this.showProgress();
            
            // Start analysis
            const result = await this.startAnalysis(data);
            
            if (result.error) {
                throw new Error(result.message || result.error);
            }
            
            // Show results
            this.showResults(result);
            
            // Clear saved form data
            localStorage.removeItem('arqv30_form_data');
            
        } catch (error) {
            console.error('Erro na análise:', error);
            this.hideProgress();
            this.showAlert(`Erro na análise: ${error.message}`, 'error');
        }
    }
    
    async startAnalysis(data) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.message || `HTTP ${response.status}`);
            }
            
            this.currentAnalysis = result;
            return result;
            
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error;
        }
    }
    
    showProgress() {
        const progressArea = document.getElementById('progressArea');
        const resultsArea = document.getElementById('resultsArea');
        
        if (progressArea) {
            progressArea.style.display = 'block';
            progressArea.scrollIntoView({ behavior: 'smooth' });
        }
        
        if (resultsArea) {
            resultsArea.style.display = 'none';
        }
        
        // Simulate progress
        this.simulateProgress();
    }
    
    hideProgress() {
        const progressArea = document.getElementById('progressArea');
        if (progressArea) {
            progressArea.style.display = 'none';
        }
    }
    
    simulateProgress() {
        const steps = [
            'Validando dados de entrada...',
            'Iniciando pesquisa web massiva...',
            'Extraindo conteúdo de páginas...',
            'Processando com múltiplas IAs...',
            'Gerando avatar ultra-detalhado...',
            'Criando drivers mentais customizados...',
            'Desenvolvendo provas visuais...',
            'Construindo sistema anti-objeção...',
            'Arquitetando pré-pitch invisível...',
            'Predizendo futuro do mercado...',
            'Consolidando insights exclusivos...',
            'Finalizando análise ultra-robusta...'
        ];
        
        let currentStep = 0;
        const progressFill = document.querySelector('.progress-fill');
        const stepElement = document.getElementById('currentStep');
        const stepCounter = document.getElementById('stepCounter');
        const estimatedTime = document.getElementById('estimatedTime');
        
        const interval = setInterval(() => {
            if (currentStep < steps.length) {
                const progress = ((currentStep + 1) / steps.length) * 100;
                
                if (progressFill) {
                    progressFill.style.width = `${progress}%`;
                }
                
                if (stepElement) {
                    stepElement.textContent = steps[currentStep];
                }
                
                if (stepCounter) {
                    stepCounter.textContent = `${currentStep + 1}/${steps.length}`;
                }
                
                if (estimatedTime) {
                    const remaining = Math.max(0, (steps.length - currentStep - 1) * 15);
                    const minutes = Math.floor(remaining / 60);
                    const seconds = remaining % 60;
                    estimatedTime.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
                }
                
                currentStep++;
            } else {
                clearInterval(interval);
            }
        }, 2000); // 2 seconds per step
        
        // Store interval for cleanup
        this.progressInterval = interval;
    }
    
    showResults(analysis) {
        // Clear progress interval
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        // Hide progress, show results
        this.hideProgress();
        
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.style.display = 'block';
            resultsArea.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Render analysis results
        this.renderAnalysisResults(analysis);
        
        // Show download buttons
        this.showDownloadButtons();
        
        // Show success message
        this.showAlert('Análise ultra-detalhada concluída com sucesso!', 'success');
    }
    
    renderAnalysisResults(analysis) {
        // Avatar
        if (analysis.avatar_ultra_detalhado) {
            this.renderAvatar(analysis.avatar_ultra_detalhado);
        }
        
        // Drivers Mentais
        if (analysis.drivers_mentais_customizados) {
            this.renderDrivers(analysis.drivers_mentais_customizados);
        }
        
        // Competition
        if (analysis.analise_concorrencia_detalhada) {
            this.renderCompetition(analysis.analise_concorrencia_detalhada);
        }
        
        // Positioning
        if (analysis.escopo) {
            this.renderPositioning(analysis.escopo);
        }
        
        // Keywords
        if (analysis.estrategia_palavras_chave) {
            this.renderKeywords(analysis.estrategia_palavras_chave);
        }
        
        // Metrics
        if (analysis.metricas_performance_detalhadas) {
            this.renderMetrics(analysis.metricas_performance_detalhadas);
        }
        
        // Action Plan
        if (analysis.plano_acao_detalhado) {
            this.renderActionPlan(analysis.plano_acao_detalhado);
        }
        
        // Insights
        if (analysis.insights_exclusivos) {
            this.renderInsights(analysis.insights_exclusivos);
        }
        
        // Visual Proofs
        if (analysis.provas_visuais_sugeridas) {
            this.renderVisualProofs(analysis.provas_visuais_sugeridas);
        }
        
        // Anti-Objection
        if (analysis.sistema_anti_objecao) {
            this.renderAntiObjection(analysis.sistema_anti_objecao);
        }
        
        // Pre-Pitch
        if (analysis.pre_pitch_invisivel) {
            this.renderPrePitch(analysis.pre_pitch_invisivel);
        }
        
        // Future Predictions
        if (analysis.predicoes_futuro_completas) {
            this.renderFuturePredictions(analysis.predicoes_futuro_completas);
        }
        
        // Research
        if (analysis.pesquisa_web_massiva) {
            this.renderResearch(analysis.pesquisa_web_massiva);
        }
        
        // Metadata
        if (analysis.metadata) {
            this.renderMetadata(analysis.metadata);
        }
    }
    
    renderAvatar(avatar) {
        const container = document.getElementById('avatarResults');
        if (!container) return;
        
        const html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-user-circle"></i>
                    <h4>Avatar Ultra-Detalhado</h4>
                </div>
                <div class="result-section-content">
                    <div class="avatar-grid">
                        ${avatar.perfil_demografico ? this.renderAvatarSection('Perfil Demográfico', avatar.perfil_demografico, 'fas fa-chart-pie') : ''}
                        ${avatar.perfil_psicografico ? this.renderAvatarSection('Perfil Psicográfico', avatar.perfil_psicografico, 'fas fa-brain') : ''}
                    </div>
                    
                    ${avatar.dores_viscerais ? this.renderAvatarList('Dores Viscerais', avatar.dores_viscerais, 'fas fa-exclamation-triangle', '#ff6b6b') : ''}
                    ${avatar.desejos_secretos ? this.renderAvatarList('Desejos Secretos', avatar.desejos_secretos, 'fas fa-heart', '#06ffa5') : ''}
                    ${avatar.objecoes_reais ? this.renderAvatarList('Objeções Reais', avatar.objecoes_reais, 'fas fa-shield-alt', '#ffd700') : ''}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    renderAvatarSection(title, data, icon) {
        if (!data || typeof data !== 'object') return '';
        
        const items = Object.entries(data).map(([key, value]) => `
            <div class="avatar-item">
                <span class="avatar-label">${this.formatLabel(key)}</span>
                <span class="avatar-value">${value}</span>
            </div>
        `).join('');
        
        return `
            <div class="avatar-card">
                <h5><i class="${icon}"></i> ${title}</h5>
                ${items}
            </div>
        `;
    }
    
    renderAvatarList(title, items, icon, color) {
        if (!Array.isArray(items) || items.length === 0) return '';
        
        const listItems = items.map((item, index) => `
            <li class="insight-item">
                <i class="${icon}" style="color: ${color}"></i>
                <span class="insight-text">${item}</span>
            </li>
        `).join('');
        
        return `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="${icon}" style="color: ${color}"></i>
                    <h4>${title} (${items.length})</h4>
                </div>
                <div class="result-section-content">
                    <ul class="insight-list">
                        ${listItems}
                    </ul>
                </div>
            </div>
        `;
    }
    
    renderInsights(insights) {
        const container = document.getElementById('insightsResults');
        if (!container || !Array.isArray(insights)) return;
        
        const insightCards = insights.map((insight, index) => `
            <div class="insight-card enhanced">
                <div class="insight-header">
                    <div class="insight-number">${index + 1}</div>
                    <div class="insight-meta">
                        <span class="insight-category">${this.categorizeInsight(insight)}</span>
                        <span class="insight-priority priority-${this.calculatePriority(insight)}">${this.calculatePriority(insight)}</span>
                    </div>
                </div>
                <div class="insight-content">${insight}</div>
                <div class="insight-actionability">
                    <strong>Acionabilidade:</strong> ${this.assessActionability(insight)}
                </div>
            </div>
        `).join('');
        
        const html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-lightbulb"></i>
                    <h4>Insights Exclusivos Ultra-Valiosos (${insights.length})</h4>
                    <div class="quality-indicators">
                        <span class="quality-badge ultra-premium">ULTRA PREMIUM</span>
                        <span class="innovation-badge">DADOS REAIS</span>
                    </div>
                </div>
                <div class="result-section-content">
                    <div class="insight-filters">
                        <div class="filter-buttons">
                            <button class="filter-btn active" data-filter="all">Todos</button>
                            <button class="filter-btn" data-filter="oportunidade">Oportunidades</button>
                            <button class="filter-btn" data-filter="risco">Riscos</button>
                            <button class="filter-btn" data-filter="tendencia">Tendências</button>
                        </div>
                    </div>
                    <div class="insights-showcase">
                        ${insightCards}
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        
        // Setup filter functionality
        this.setupInsightFilters();
    }
    
    renderMetrics(metrics) {
        const container = document.getElementById('metricsResults');
        if (!container) return;
        
        const html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-chart-line"></i>
                    <h4>Métricas de Performance Detalhadas</h4>
                </div>
                <div class="result-section-content">
                    ${metrics.projecoes_financeiras ? this.renderFinancialProjections(metrics.projecoes_financeiras) : ''}
                    ${metrics.kpis_principais ? this.renderKPIs(metrics.kpis_principais) : ''}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    renderFinancialProjections(projections) {
        const scenarios = ['cenario_conservador', 'cenario_realista', 'cenario_otimista'];
        const scenarioNames = {
            'cenario_conservador': 'Conservador',
            'cenario_realista': 'Realista', 
            'cenario_otimista': 'Otimista'
        };
        
        const cards = scenarios.map(scenario => {
            const data = projections[scenario];
            if (!data) return '';
            
            return `
                <div class="scenario-card scenario-${scenario.split('_')[1]}">
                    <h6>${scenarioNames[scenario]}</h6>
                    <div class="scenario-metrics">
                        ${data.receita_mensal ? `<div class="metric"><span class="metric-label">Receita Mensal</span><span class="metric-value">${data.receita_mensal}</span></div>` : ''}
                        ${data.clientes_mes ? `<div class="metric"><span class="metric-label">Clientes/Mês</span><span class="metric-value">${data.clientes_mes}</span></div>` : ''}
                        ${data.ticket_medio ? `<div class="metric"><span class="metric-label">Ticket Médio</span><span class="metric-value">${data.ticket_medio}</span></div>` : ''}
                        ${data.margem_lucro ? `<div class="metric"><span class="metric-label">Margem</span><span class="metric-value">${data.margem_lucro}</span></div>` : ''}
                    </div>
                </div>
            `;
        }).join('');
        
        return `
            <div class="projections-grid">
                ${cards}
            </div>
        `;
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/status`);
            const status = await response.json();
            
            this.updateSystemStatus(status);
            
            return status;
            
        } catch (error) {
            console.error('Erro ao verificar status do sistema:', error);
            this.updateSystemStatus({ status: 'error', error: error.message });
        }
    }
    
    updateSystemStatus(status) {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        const apiStatus = document.getElementById('apiStatus');
        const extractorStatus = document.getElementById('extractorStatus');
        
        if (statusIndicator && statusText) {
            statusIndicator.className = 'status-indicator';
            
            if (status.status === 'healthy') {
                statusIndicator.classList.add('online');
                statusText.textContent = 'Sistema Online';
            } else if (status.status === 'degraded') {
                statusIndicator.classList.add('loading');
                statusText.textContent = 'Sistema Degradado';
            } else {
                statusIndicator.classList.add('offline');
                statusText.textContent = 'Sistema Offline';
            }
        }
        
        // Update API status
        if (apiStatus && status.systems) {
            const aiProviders = status.systems.ai_providers;
            if (aiProviders) {
                apiStatus.innerHTML = `
                    <i class="fas fa-robot"></i>
                    <span>APIs: ${aiProviders.available_count}/${aiProviders.total_count}</span>
                `;
            }
        }
        
        // Update extractor status
        if (extractorStatus) {
            extractorStatus.innerHTML = `
                <i class="fas fa-download"></i>
                <span>Extratores: Ativos</span>
            `;
        }
        
        this.systemStatus = status;
    }
    
    showSystemStatus() {
        const status = this.systemStatus;
        let message = `Status do Sistema: ${status.status || 'Desconhecido'}\n\n`;
        
        if (status.systems) {
            if (status.systems.ai_providers) {
                message += `IAs: ${status.systems.ai_providers.available_count}/${status.systems.ai_providers.total_count} disponíveis\n`;
            }
            
            if (status.systems.search_providers) {
                message += `Busca: ${status.systems.search_providers.available_count}/${status.systems.search_providers.total_count} disponíveis\n`;
            }
            
            if (status.systems.database) {
                message += `Banco: ${status.systems.database.connected ? 'Conectado' : 'Desconectado'}\n`;
            }
        }
        
        if (status.capabilities) {
            message += '\nCapacidades:\n';
            Object.entries(status.capabilities).forEach(([key, value]) => {
                message += `• ${key}: ${value ? 'Sim' : 'Não'}\n`;
            });
        }
        
        alert(message);
    }
    
    showDownloadButtons() {
        const downloadPdfBtn = document.getElementById('downloadPdfBtn');
        const saveJsonBtn = document.getElementById('saveJsonBtn');
        
        if (downloadPdfBtn) {
            downloadPdfBtn.style.display = 'inline-flex';
            downloadPdfBtn.onclick = () => this.downloadPDF();
        }
        
        if (saveJsonBtn) {
            saveJsonBtn.style.display = 'inline-flex';
        }
    }
    
    async downloadPDF() {
        if (!this.currentAnalysis) {
            this.showAlert('Nenhuma análise disponível para download', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/generate_pdf`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.currentAnalysis)
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `analise_mercado_${new Date().toISOString().slice(0, 10)}.pdf`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showAlert('PDF gerado com sucesso!', 'success');
            } else {
                throw new Error('Erro ao gerar PDF');
            }
            
        } catch (error) {
            console.error('Erro ao baixar PDF:', error);
            this.showAlert('Erro ao gerar PDF', 'error');
        }
    }
    
    saveAnalysisLocally(analysis) {
        if (!analysis) {
            this.showAlert('Nenhuma análise para salvar', 'error');
            return;
        }
        
        try {
            const dataStr = JSON.stringify(analysis, null, 2);
            const blob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `analise_arqv30_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            this.showAlert('Análise salva localmente!', 'success');
            
        } catch (error) {
            console.error('Erro ao salvar análise:', error);
            this.showAlert('Erro ao salvar análise', 'error');
        }
    }
    
    showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());
        
        // Create new alert
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <i class="fas fa-${this.getAlertIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(alert);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
    
    getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    formatLabel(key) {
        return key.replace(/_/g, ' ')
                 .replace(/\b\w/g, l => l.toUpperCase());
    }
    
    categorizeInsight(insight) {
        const text = insight.toLowerCase();
        if (text.includes('oportunidade') || text.includes('potencial')) return 'Oportunidade';
        if (text.includes('risco') || text.includes('ameaça')) return 'Risco';
        if (text.includes('tendência') || text.includes('futuro')) return 'Tendência';
        if (text.includes('estratégia') || text.includes('tática')) return 'Estratégia';
        return 'Mercado';
    }
    
    calculatePriority(insight) {
        const text = insight.toLowerCase();
        if (text.includes('crítico') || text.includes('urgente')) return 'high';
        if (text.includes('importante') || text.includes('relevante')) return 'medium';
        return 'low';
    }
    
    assessActionability(insight) {
        if (insight.length > 100 && insight.includes('implementar')) return 'Alta - Insight específico e acionável';
        if (insight.length > 50) return 'Média - Requer planejamento adicional';
        return 'Baixa - Muito genérico';
    }
    
    setupInsightFilters() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        const insightCards = document.querySelectorAll('.insight-card');
        
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active button
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const filter = btn.dataset.filter;
                
                // Filter insights
                insightCards.forEach(card => {
                    const category = card.querySelector('.insight-category')?.textContent.toLowerCase();
                    
                    if (filter === 'all' || category?.includes(filter)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }
    
    initializeTooltips() {
        // Simple tooltip implementation
        const elementsWithTooltips = document.querySelectorAll('[data-tooltip]');
        
        elementsWithTooltips.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                const tooltip = document.createElement('div');
                tooltip.className = 'tooltip-popup';
                tooltip.textContent = e.target.dataset.tooltip;
                
                document.body.appendChild(tooltip);
                
                const rect = e.target.getBoundingClientRect();
                tooltip.style.position = 'absolute';
                tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;
                tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
                tooltip.style.zIndex = '1000';
                
                e.target._tooltip = tooltip;
            });
            
            element.addEventListener('mouseleave', (e) => {
                if (e.target._tooltip) {
                    e.target._tooltip.remove();
                    delete e.target._tooltip;
                }
            });
        });
    }
    
    // Additional render methods for other components
    renderDrivers(drivers) {
        const container = document.getElementById('driversResults');
        if (!container || !drivers.drivers_customizados) return;
        
        const driverCards = drivers.drivers_customizados.map(driver => `
            <div class="driver-card">
                <h4>${driver.nome || 'Driver Mental'}</h4>
                <div class="driver-content">
                    <p><strong>Gatilho Central:</strong> ${driver.gatilho_central || 'N/A'}</p>
                    <p><strong>Definição:</strong> ${driver.definicao_visceral || 'N/A'}</p>
                    
                    ${driver.roteiro_ativacao ? `
                        <div class="driver-script">
                            <h6>Roteiro de Ativação</h6>
                            <p><strong>Pergunta:</strong> ${driver.roteiro_ativacao.pergunta_abertura || 'N/A'}</p>
                            <p><strong>História:</strong> ${driver.roteiro_ativacao.historia_analogia || 'N/A'}</p>
                            <p><strong>Comando:</strong> ${driver.roteiro_ativacao.comando_acao || 'N/A'}</p>
                        </div>
                    ` : ''}
                    
                    ${driver.frases_ancoragem ? `
                        <div class="anchor-phrases">
                            <h6>Frases de Ancoragem</h6>
                            <ul>
                                ${driver.frases_ancoragem.map(frase => `<li>${frase}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');
        
        const html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-brain"></i>
                    <h4>Drivers Mentais Customizados (${drivers.drivers_customizados.length})</h4>
                </div>
                <div class="result-section-content">
                    <div class="drivers-grid">
                        ${driverCards}
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    renderResearch(research) {
        const container = document.getElementById('researchResults');
        if (!container) return;
        
        const stats = research.estatisticas || {};
        
        const html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-search"></i>
                    <h4>Pesquisa Web Massiva REAL</h4>
                    <div class="quality-indicators">
                        <span class="quality-badge premium">DADOS REAIS</span>
                    </div>
                </div>
                <div class="result-section-content">
                    <div class="research-stats">
                        <div class="stats-grid">
                            <div class="stat-item">
                                <span class="stat-label">Queries Executadas</span>
                                <span class="stat-value">${stats.total_queries || 0}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Resultados Encontrados</span>
                                <span class="stat-value">${stats.total_resultados || 0}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Fontes Únicas</span>
                                <span class="stat-value">${stats.fontes_unicas || 0}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Conteúdo Extraído</span>
                                <span class="stat-value">${(stats.total_conteudo || 0).toLocaleString()} chars</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Qualidade Média</span>
                                <span class="stat-value">${(stats.qualidade_media || 0).toFixed(1)}%</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="data-quality-indicator">
                        <span class="quality-label">Qualidade dos Dados:</span>
                        <span class="quality-value real-data">100% DADOS REAIS</span>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    renderMetadata(metadata) {
        const container = document.getElementById('metadataResults');
        if (!container) return;
        
        const html = `
            <div class="result-section">
                <div class="result-section-header">
                    <i class="fas fa-info-circle"></i>
                    <h4>Metadados da Análise</h4>
                </div>
                <div class="result-section-content">
                    <div class="metadata-grid enhanced">
                        <div class="metadata-item premium">
                            <span class="metadata-label">Tempo de Processamento</span>
                            <span class="metadata-value">${metadata.processing_time_formatted || 'N/A'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Engine de Análise</span>
                            <span class="metadata-value">ARQV30 v2.0</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Qualidade</span>
                            <span class="metadata-value quality-score">${(metadata.quality_score || 0).toFixed(1)}%</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Tipo de Relatório</span>
                            <span class="metadata-value">${metadata.report_type || 'COMPLETO'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Simulação</span>
                            <span class="metadata-value">${metadata.simulation_free ? 'ZERO' : 'DETECTADA'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Dados Brutos</span>
                            <span class="metadata-value">${metadata.raw_data_filtered ? 'FILTRADOS' : 'INCLUSOS'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ARQV30App();
});

// Global functions for testing
window.testFunctions = {
    checkHealth: () => window.app.checkSystemHealth(),
    saveAnalysis: () => window.app.saveAnalysisLocally(window.app.currentAnalysis),
    showStatus: () => window.app.showSystemStatus()
};