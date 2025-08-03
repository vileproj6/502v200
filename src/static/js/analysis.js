// ARQV30 Enhanced v2.0 - Analysis Manager
// Advanced analysis management and testing functions

class AnalysisManager {
    constructor() {
        this.currentAnalysis = null;
        this.testResults = {};
        this.extractorStats = null;
        
        console.log('🔬 Analysis Manager inicializado');
    }
    
    // Test extraction functionality
    async testExtraction() {
        const testUrl = prompt('Digite uma URL para testar extração:', 'https://g1.globo.com/');
        
        if (!testUrl) return;
        
        try {
            console.log('🧪 Testando extração para:', testUrl);
            
            const response = await fetch('/api/test_extraction?' + new URLSearchParams({
                url: testUrl
            }));
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Teste de extração bem-sucedido:', result);
                
                const message = `
Teste de Extração - SUCESSO

URL: ${testUrl}
Conteúdo: ${result.content_length} caracteres
Tempo: ${(result.extraction_time || 0).toFixed(2)}s
Extrator: ${result.extractor_used || 'N/A'}

Preview: ${result.content_preview ? result.content_preview.substring(0, 200) + '...' : 'N/A'}
                `.trim();
                
                alert(message);
                
                if (window.app) {
                    window.app.showAlert('Teste de extração bem-sucedido!', 'success');
                }
            } else {
                throw new Error(result.error || 'Teste falhou');
            }
            
        } catch (error) {
            console.error('❌ Erro no teste de extração:', error);
            alert(`Erro no teste de extração: ${error.message}`);
            
            if (window.app) {
                window.app.showAlert(`Erro no teste: ${error.message}`, 'error');
            }
        }
    }
    
    // Test search functionality
    async testSearch() {
        const testQuery = prompt('Digite uma query para testar busca:', 'mercado digital Brasil 2024');
        
        if (!testQuery) return;
        
        try {
            console.log('🔍 Testando busca para:', testQuery);
            
            const response = await fetch('/api/test_search?' + new URLSearchParams({
                query: testQuery,
                max_results: '5'
            }));
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Teste de busca bem-sucedido:', result);
                
                const message = `
Teste de Busca - SUCESSO

Query: ${testQuery}
Resultados: ${result.results_count || 0}
Provedores: ${result.providers_used || 'N/A'}
Tempo: ${(result.search_time || 0).toFixed(2)}s

Primeiros resultados:
${result.results ? result.results.slice(0, 3).map(r => `• ${r.title}`).join('\n') : 'Nenhum'}
                `.trim();
                
                alert(message);
                
                if (window.app) {
                    window.app.showAlert('Teste de busca bem-sucedido!', 'success');
                }
            } else {
                throw new Error(result.error || 'Teste falhou');
            }
            
        } catch (error) {
            console.error('❌ Erro no teste de busca:', error);
            alert(`Erro no teste de busca: ${error.message}`);
            
            if (window.app) {
                window.app.showAlert(`Erro no teste: ${error.message}`, 'error');
            }
        }
    }
    
    // Show extractor statistics
    async showExtractorStats() {
        try {
            console.log('📊 Obtendo estatísticas dos extratores...');
            
            const response = await fetch('/api/extractor_stats');
            const result = await response.json();
            
            if (result.success) {
                this.extractorStats = result.stats;
                console.log('📊 Estatísticas dos extratores:', this.extractorStats);
                
                this.displayExtractorStats(this.extractorStats);
                
                if (window.app) {
                    window.app.showAlert('Estatísticas carregadas!', 'info');
                }
            } else {
                throw new Error(result.error || 'Erro ao obter estatísticas');
            }
            
        } catch (error) {
            console.error('❌ Erro ao obter estatísticas:', error);
            alert(`Erro ao obter estatísticas: ${error.message}`);
        }
    }
    
    displayExtractorStats(stats) {
        let message = 'ESTATÍSTICAS DOS EXTRATORES\n\n';
        
        // Global stats
        if (stats.global) {
            const global = stats.global;
            message += `GLOBAL:\n`;
            message += `• Total de extrações: ${global.total_extractions || 0}\n`;
            message += `• Sucessos: ${global.total_successes || 0}\n`;
            message += `• Falhas: ${global.total_failures || 0}\n`;
            message += `• Taxa de sucesso: ${(global.success_rate || 0).toFixed(1)}%\n\n`;
        }
        
        // Individual extractors
        Object.entries(stats).forEach(([name, data]) => {
            if (name === 'global') return;
            
            message += `${name.toUpperCase()}:\n`;
            message += `• Disponível: ${data.available ? 'Sim' : 'Não'}\n`;
            
            if (data.available) {
                message += `• Sucessos: ${data.success || 0}\n`;
                message += `• Falhas: ${data.failed || 0}\n`;
                message += `• Uso: ${data.usage_count || 0}x\n`;
                
                if (data.success_rate !== undefined) {
                    message += `• Taxa: ${data.success_rate.toFixed(1)}%\n`;
                }
                
                if (data.avg_response_time !== undefined) {
                    message += `• Tempo médio: ${data.avg_response_time.toFixed(2)}s\n`;
                }
            } else if (data.reason) {
                message += `• Motivo: ${data.reason}\n`;
            }
            
            message += '\n';
        });
        
        // Show in modal or alert
        if (message.length > 1000) {
            // Create modal for large content
            this.showStatsModal(message);
        } else {
            alert(message);
        }
    }
    
    showStatsModal(content) {
        // Create modal
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;
        
        modal.innerHTML = `
            <div style="
                background: var(--bg-elevated);
                border-radius: 16px;
                padding: 32px;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: var(--shadow-floating);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                    <h3 style="color: var(--accent-primary); margin: 0;">📊 Estatísticas dos Extratores</h3>
                    <button onclick="this.closest('.modal').remove()" style="
                        background: var(--bg-surface);
                        border: none;
                        border-radius: 8px;
                        padding: 8px 12px;
                        color: var(--text-secondary);
                        cursor: pointer;
                    ">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <pre style="
                    background: var(--bg-surface);
                    padding: 20px;
                    border-radius: 12px;
                    color: var(--text-primary);
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 12px;
                    line-height: 1.4;
                    white-space: pre-wrap;
                    box-shadow: var(--shadow-inset);
                ">${content}</pre>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close on click outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }
    
    // Reset extractor statistics
    async resetExtractors() {
        if (!confirm('Resetar estatísticas de todos os extratores?')) {
            return;
        }
        
        try {
            console.log('🔄 Resetando extratores...');
            
            const response = await fetch('/api/reset_extractors', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Extratores resetados');
                alert('Estatísticas dos extratores resetadas com sucesso!');
                
                if (window.app) {
                    window.app.showAlert('Extratores resetados!', 'success');
                }
            } else {
                throw new Error(result.error || 'Erro ao resetar');
            }
            
        } catch (error) {
            console.error('❌ Erro ao resetar extratores:', error);
            alert(`Erro ao resetar extratores: ${error.message}`);
        }
    }
    
    // Save analysis locally
    saveAnalysisLocally(analysis) {
        if (!analysis) {
            alert('Nenhuma análise para salvar');
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
            
            console.log('💾 Análise salva localmente');
            
            if (window.app) {
                window.app.showAlert('Análise salva localmente!', 'success');
            }
            
        } catch (error) {
            console.error('❌ Erro ao salvar análise:', error);
            alert(`Erro ao salvar: ${error.message}`);
        }
    }
    
    // Load analysis from file
    loadAnalysisFromFile() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const analysis = JSON.parse(e.target.result);
                    this.currentAnalysis = analysis;
                    
                    if (window.app) {
                        window.app.currentAnalysis = analysis;
                        window.app.showResults(analysis);
                        window.app.showAlert('Análise carregada com sucesso!', 'success');
                    }
                    
                    console.log('📂 Análise carregada:', analysis);
                    
                } catch (error) {
                    console.error('❌ Erro ao carregar análise:', error);
                    alert('Erro ao carregar arquivo: formato inválido');
                }
            };
            
            reader.readAsText(file);
        };
        
        input.click();
    }
    
    // Export analysis in different formats
    async exportAnalysis(format = 'json') {
        if (!this.currentAnalysis) {
            alert('Nenhuma análise para exportar');
            return;
        }
        
        try {
            let blob, filename, mimeType;
            
            switch (format) {
                case 'json':
                    const jsonData = JSON.stringify(this.currentAnalysis, null, 2);
                    blob = new Blob([jsonData], { type: 'application/json' });
                    filename = `analise_${Date.now()}.json`;
                    break;
                    
                case 'csv':
                    const csvData = this.convertToCSV(this.currentAnalysis);
                    blob = new Blob([csvData], { type: 'text/csv' });
                    filename = `analise_${Date.now()}.csv`;
                    break;
                    
                case 'txt':
                    const txtData = this.convertToText(this.currentAnalysis);
                    blob = new Blob([txtData], { type: 'text/plain' });
                    filename = `analise_${Date.now()}.txt`;
                    break;
                    
                default:
                    throw new Error('Formato não suportado');
            }
            
            // Download
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            console.log(`📤 Análise exportada em ${format.toUpperCase()}`);
            
            if (window.app) {
                window.app.showAlert(`Análise exportada em ${format.toUpperCase()}!`, 'success');
            }
            
        } catch (error) {
            console.error('❌ Erro ao exportar:', error);
            alert(`Erro ao exportar: ${error.message}`);
        }
    }
    
    convertToCSV(analysis) {
        let csv = 'Campo,Valor\n';
        
        // Basic info
        if (analysis.projeto_dados) {
            Object.entries(analysis.projeto_dados).forEach(([key, value]) => {
                csv += `"${key}","${String(value).replace(/"/g, '""')}"\n`;
            });
        }
        
        // Insights
        if (analysis.insights_exclusivos) {
            analysis.insights_exclusivos.forEach((insight, index) => {
                csv += `"Insight ${index + 1}","${String(insight).replace(/"/g, '""')}"\n`;
            });
        }
        
        return csv;
    }
    
    convertToText(analysis) {
        let text = 'ANÁLISE ULTRA-DETALHADA - ARQV30 Enhanced v2.0\n';
        text += '='.repeat(60) + '\n\n';
        
        // Basic info
        if (analysis.projeto_dados) {
            text += 'DADOS DO PROJETO:\n';
            Object.entries(analysis.projeto_dados).forEach(([key, value]) => {
                text += `${key}: ${value}\n`;
            });
            text += '\n';
        }
        
        // Avatar
        if (analysis.avatar_ultra_detalhado) {
            text += 'AVATAR ULTRA-DETALHADO:\n';
            
            if (analysis.avatar_ultra_detalhado.dores_viscerais) {
                text += '\nDores Viscerais:\n';
                analysis.avatar_ultra_detalhado.dores_viscerais.forEach((dor, i) => {
                    text += `${i + 1}. ${dor}\n`;
                });
            }
            
            if (analysis.avatar_ultra_detalhado.desejos_secretos) {
                text += '\nDesejos Secretos:\n';
                analysis.avatar_ultra_detalhado.desejos_secretos.forEach((desejo, i) => {
                    text += `${i + 1}. ${desejo}\n`;
                });
            }
            
            text += '\n';
        }
        
        // Insights
        if (analysis.insights_exclusivos) {
            text += 'INSIGHTS EXCLUSIVOS:\n';
            analysis.insights_exclusivos.forEach((insight, i) => {
                text += `${i + 1}. ${insight}\n`;
            });
            text += '\n';
        }
        
        // Metadata
        if (analysis.metadata) {
            text += 'METADADOS:\n';
            Object.entries(analysis.metadata).forEach(([key, value]) => {
                text += `${key}: ${value}\n`;
            });
        }
        
        return text;
    }
    
    // Compare analyses
    compareAnalyses(analysis1, analysis2) {
        const comparison = {
            insights_diff: this.compareInsights(
                analysis1.insights_exclusivos || [],
                analysis2.insights_exclusivos || []
            ),
            quality_diff: {
                analysis1: analysis1.metadata?.quality_score || 0,
                analysis2: analysis2.metadata?.quality_score || 0
            },
            processing_time_diff: {
                analysis1: analysis1.metadata?.processing_time_seconds || 0,
                analysis2: analysis2.metadata?.processing_time_seconds || 0
            }
        };
        
        console.log('🔍 Comparação de análises:', comparison);
        return comparison;
    }
    
    compareInsights(insights1, insights2) {
        const set1 = new Set(insights1.map(i => i.toLowerCase()));
        const set2 = new Set(insights2.map(i => i.toLowerCase()));
        
        const common = [...set1].filter(i => set2.has(i));
        const unique1 = [...set1].filter(i => !set2.has(i));
        const unique2 = [...set2].filter(i => !set1.has(i));
        
        return {
            common_count: common.length,
            unique_to_first: unique1.length,
            unique_to_second: unique2.length,
            similarity_score: common.length / Math.max(set1.size, set2.size)
        };
    }
    
    // Performance monitoring
    startPerformanceMonitoring() {
        this.performanceData = {
            startTime: performance.now(),
            memoryStart: performance.memory ? performance.memory.usedJSHeapSize : 0,
            networkRequests: 0,
            errors: 0
        };
        
        // Monitor network requests
        const originalFetch = window.fetch;
        window.fetch = (...args) => {
            this.performanceData.networkRequests++;
            return originalFetch.apply(this, args);
        };
        
        // Monitor errors
        window.addEventListener('error', () => {
            this.performanceData.errors++;
        });
        
        console.log('📈 Monitoramento de performance iniciado');
    }
    
    getPerformanceReport() {
        if (!this.performanceData) {
            return 'Monitoramento não iniciado';
        }
        
        const endTime = performance.now();
        const duration = endTime - this.performanceData.startTime;
        const memoryEnd = performance.memory ? performance.memory.usedJSHeapSize : 0;
        const memoryUsed = memoryEnd - this.performanceData.memoryStart;
        
        return {
            duration_ms: duration,
            memory_used_mb: memoryUsed / (1024 * 1024),
            network_requests: this.performanceData.networkRequests,
            errors: this.performanceData.errors,
            requests_per_second: this.performanceData.networkRequests / (duration / 1000)
        };
    }
    
    // Debug utilities
    debugAnalysis(analysis = this.currentAnalysis) {
        if (!analysis) {
            console.log('❌ Nenhuma análise para debug');
            return;
        }
        
        console.group('🐛 DEBUG - Análise ARQV30');
        
        // Structure analysis
        console.log('📋 Estrutura da análise:');
        console.log('Seções principais:', Object.keys(analysis));
        
        // Quality metrics
        if (analysis.metadata) {
            console.log('📊 Métricas de qualidade:');
            console.log('Score:', analysis.metadata.quality_score);
            console.log('Tempo:', analysis.metadata.processing_time_formatted);
            console.log('Simulação:', analysis.metadata.simulation_free ? 'Não' : 'Sim');
        }
        
        // Content analysis
        if (analysis.insights_exclusivos) {
            console.log('💡 Insights:');
            console.log('Total:', analysis.insights_exclusivos.length);
            console.log('Média de caracteres:', 
                analysis.insights_exclusivos.reduce((acc, i) => acc + i.length, 0) / analysis.insights_exclusivos.length
            );
        }
        
        // Research data
        if (analysis.pesquisa_web_massiva) {
            console.log('🔍 Pesquisa:');
            console.log('Estatísticas:', analysis.pesquisa_web_massiva.estatisticas);
        }
        
        console.groupEnd();
        
        return {
            structure: Object.keys(analysis),
            insights_count: analysis.insights_exclusivos?.length || 0,
            quality_score: analysis.metadata?.quality_score || 0,
            has_research: !!analysis.pesquisa_web_massiva,
            has_avatar: !!analysis.avatar_ultra_detalhado
        };
    }
    
    // Validate analysis completeness
    validateAnalysis(analysis = this.currentAnalysis) {
        if (!analysis) {
            return { valid: false, errors: ['Nenhuma análise fornecida'] };
        }
        
        const errors = [];
        const warnings = [];
        
        // Required sections
        const requiredSections = [
            'projeto_dados',
            'avatar_ultra_detalhado', 
            'insights_exclusivos'
        ];
        
        requiredSections.forEach(section => {
            if (!analysis[section]) {
                errors.push(`Seção obrigatória ausente: ${section}`);
            }
        });
        
        // Quality checks
        if (analysis.insights_exclusivos) {
            if (analysis.insights_exclusivos.length < 5) {
                warnings.push(`Poucos insights: ${analysis.insights_exclusivos.length} < 5`);
            }
            
            const shortInsights = analysis.insights_exclusivos.filter(i => i.length < 50);
            if (shortInsights.length > 0) {
                warnings.push(`${shortInsights.length} insights muito curtos`);
            }
        }
        
        // Metadata checks
        if (analysis.metadata) {
            if (analysis.metadata.quality_score < 70) {
                warnings.push(`Score de qualidade baixo: ${analysis.metadata.quality_score}%`);
            }
            
            if (!analysis.metadata.simulation_free) {
                errors.push('Análise contém simulações');
            }
        }
        
        const result = {
            valid: errors.length === 0,
            errors,
            warnings,
            score: this.calculateValidationScore(analysis, errors, warnings)
        };
        
        console.log('✅ Validação da análise:', result);
        return result;
    }
    
    calculateValidationScore(analysis, errors, warnings) {
        let score = 100;
        
        // Penalize errors heavily
        score -= errors.length * 25;
        
        // Penalize warnings lightly
        score -= warnings.length * 5;
        
        // Bonus for completeness
        const sections = Object.keys(analysis);
        if (sections.length > 10) score += 10;
        if (sections.length > 15) score += 10;
        
        return Math.max(0, Math.min(100, score));
    }
}

// Initialize analysis manager
document.addEventListener('DOMContentLoaded', () => {
    window.analysisManager = new AnalysisManager();
    
    // Start performance monitoring
    window.analysisManager.startPerformanceMonitoring();
});

// Global utility functions
window.arqv30Utils = {
    formatCurrency: (value) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    },
    
    formatNumber: (value) => {
        return new Intl.NumberFormat('pt-BR').format(value);
    },
    
    formatDate: (date) => {
        return new Intl.DateTimeFormat('pt-BR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    },
    
    copyToClipboard: async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            if (window.app) {
                window.app.showAlert('Copiado para área de transferência!', 'success');
            }
        } catch (error) {
            console.error('Erro ao copiar:', error);
        }
    },
    
    downloadText: (text, filename) => {
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
};

// Console helpers for development
if (typeof window !== 'undefined') {
    window.arqv30Debug = {
        getCurrentAnalysis: () => window.analysisManager?.currentAnalysis,
        getUploadedFiles: () => window.uploadManager?.getUploadedFiles(),
        getSystemStatus: () => window.app?.systemStatus,
        validateCurrent: () => window.analysisManager?.validateAnalysis(),
        debugCurrent: () => window.analysisManager?.debugAnalysis(),
        getPerformance: () => window.analysisManager?.getPerformanceReport()
    };
    
    console.log('🛠️ Debug utilities available at window.arqv30Debug');
}