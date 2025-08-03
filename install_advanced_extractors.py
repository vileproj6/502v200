#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Instalador de Extratores Avançados
Instala Playwright e Selenium para extração de páginas dinâmicas
"""

import subprocess
import sys
import logging
import os

logger = logging.getLogger(__name__)

def install_package(package_name):
    """Instala um pacote Python"""
    try:
        logger.info(f"📦 Instalando {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logger.info(f"✅ {package_name} instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erro ao instalar {package_name}: {e}")
        return False

def install_playwright_browsers():
    """Instala browsers do Playwright"""
    try:
        logger.info("🌐 Instalando browsers do Playwright...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        logger.info("✅ Browsers do Playwright instalados")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erro ao instalar browsers: {e}")
        return False

def main():
    """Instala todos os extratores avançados"""
    
    print("🚀 ARQV30 - Instalando extratores avançados...")
    print("📋 Pacotes a instalar:")
    print("   • Playwright (para páginas dinâmicas)")
    print("   • Selenium (para páginas JavaScript pesadas)")
    print("   • WebDriver Manager (gerenciamento automático)")
    
    # Lista de pacotes necessários
    packages = [
        "playwright==1.40.0",
        "selenium==4.16.2", 
        "webdriver-manager==4.0.1"
    ]
    
    failed_packages = []
    
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Falha ao instalar: {', '.join(failed_packages)}")
        print("⚠️ Alguns extratores podem não funcionar")
        return False
    
    # Instala browsers do Playwright
    if not install_playwright_browsers():
        print("\n❌ Falha ao instalar browsers do Playwright")
        print("⚠️ Execute manualmente: playwright install chromium")
        return False
    
    print("\n✅ Todos os extratores avançados instalados!")
    print("\n🎉 RECURSOS ATIVADOS:")
    print("   • ✅ Playwright: Páginas React, Angular, Vue.js")
    print("   • ✅ Selenium: Páginas JavaScript pesadas")
    print("   • ✅ WebDriver Manager: Gerenciamento automático")
    print("   • ✅ Extração de páginas do Workday, LinkedIn, etc.")
    print("   • ✅ Suporte a SPAs (Single Page Applications)")
    print("   • ✅ Páginas com autenticação (detecção)")
    
    print("\n🚀 SISTEMA AGORA PODE EXTRAIR:")
    print("   • Páginas estáticas tradicionais")
    print("   • Páginas dinâmicas (React/Angular/Vue)")
    print("   • Páginas JavaScript pesadas")
    print("   • PDFs complexos")
    print("   • Páginas com carregamento assíncrono")
    print("   • Sites de vagas (Workday, etc.)")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. ✅ Execute uma análise para testar os novos extratores")
        print("2. 📊 Monitore logs para ver qual extrator é usado")
        print("3. 🔧 Ajuste configurações se necessário")
        
    else:
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. ❌ Verifique conexão com internet")
        print("2. 🔧 Execute: pip install --upgrade pip")
        print("3. 🧪 Tente instalar pacotes individualmente")
        print("4. 📞 Consulte logs para detalhes específicos")
    
    sys.exit(0 if success else 1)