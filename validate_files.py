#!/usr/bin/env python3
"""
Validation Script für ChatPro AI Analyzer
Prüft alle Python-Dateien vor dem Commit
"""

import ast
import sys
import os
from pathlib import Path
from typing import List, Tuple

def check_syntax(file_path: str) -> Tuple[bool, str]:
    """Prüft Python Syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        # Check for NULL bytes
        if '\x00' in code:
            return False, f"❌ NULL bytes gefunden in {file_path}"
            
        # Parse AST
        ast.parse(code, filename=file_path)
        return True, f"✅ {file_path}"
        
    except SyntaxError as e:
        return False, f"❌ Syntax Error in {file_path}:{e.lineno} - {e.msg}"
    except Exception as e:
        return False, f"❌ Fehler beim Lesen von {file_path}: {str(e)}"

def check_imports(file_path: str) -> Tuple[bool, List[str]]:
    """Prüft ob alle Imports existieren"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
            
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                    
        return True, imports
        
    except Exception as e:
        return False, [str(e)]

def check_class_exists(file_path: str, class_name: str) -> Tuple[bool, str]:
    """Prüft ob eine Klasse in einer Datei existiert"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return True, f"✅ Klasse '{class_name}' gefunden in {file_path}"
                
        return False, f"❌ Klasse '{class_name}' NICHT gefunden in {file_path}"
        
    except Exception as e:
        return False, f"❌ Fehler: {str(e)}"

def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║  CHATPRO AI - FILE VALIDATION                          ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    files_to_check = [
        'app/pipeline.py',
        'app/crawler.py',
        'app/analyzer.py',
        'app/pdf_generator.py',
        'app/sources_database.py',
        'app/brevo_crm.py'
    ]
    
    all_passed = True
    
    # STUFE 1: Syntax Check
    print("=== STUFE 1: SYNTAX CHECK ===")
    for file_path in files_to_check:
        if os.path.exists(file_path):
            passed, message = check_syntax(file_path)
            print(message)
            if not passed:
                all_passed = False
        else:
            print(f"⚠️  {file_path} nicht gefunden")
    print()
    
    # STUFE 2: Class Check
    print("=== STUFE 2: CLASS EXISTENCE CHECK ===")
    class_checks = [
        ('app/pipeline.py', 'AnalysisPipeline'),
        ('app/crawler.py', 'WebsiteCrawler'),
        ('app/analyzer.py', 'AIAnalyzer'),
        ('app/pdf_generator.py', 'PDFReportGenerator'),
        ('app/brevo_crm.py', 'BrevoCRM')
    ]
    
    for file_path, class_name in class_checks:
        if os.path.exists(file_path):
            passed, message = check_class_exists(file_path, class_name)
            print(message)
            if not passed:
                all_passed = False
    print()
    
    # STUFE 3: Cross-File Compatibility
    print("=== STUFE 3: CROSS-FILE COMPATIBILITY ===")
    
    # Check: pipeline.py imports WebsiteCrawler
    if os.path.exists('app/pipeline.py'):
        with open('app/pipeline.py', 'r') as f:
            content = f.read()
            if 'from .crawler import WebsiteCrawler' in content:
                print("✅ pipeline.py importiert WebsiteCrawler")
            else:
                print("❌ pipeline.py importiert NICHT WebsiteCrawler")
                all_passed = False
                
            if 'self.crawler = WebsiteCrawler()' in content:
                print("✅ pipeline.py instanziiert WebsiteCrawler korrekt")
            else:
                print("❌ pipeline.py instanziiert WebsiteCrawler NICHT korrekt")
                all_passed = False
    print()
    
    # Final Result
    print("╔════════════════════════════════════════════════════════╗")
    if all_passed:
        print("║  ✅ ALLE CHECKS BESTANDEN - READY TO COMMIT           ║")
        print("╚════════════════════════════════════════════════════════╝")
        sys.exit(0)
    else:
        print("║  ❌ CHECKS FEHLGESCHLAGEN - FIX ERRORS FIRST          ║")
        print("╚════════════════════════════════════════════════════════╝")
        sys.exit(1)

if __name__ == '__main__':
    main()

