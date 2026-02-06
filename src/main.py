import os
import sys

# Ensure project root is in pythonpath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.excel_adapter import ExcelAdapter
from src.infrastructure.email_adapter import EmailAdapter
from src.infrastructure.log_adapter import LogAdapter
from src.services.billing_manager import BillingManager

import argparse

def main():
    parser = argparse.ArgumentParser(description="AuroraPay Billing System")
    parser.add_argument("--test", action="store_true", help="Run in Test Mode (Force execution and mark emails as [TESTE])")
    parser.add_argument("--rule", type=str, help="Filter by specific rule (e.g., D-5, D0, D+3)")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "input", "Regua_Cobranca_V2.xlsx")
    log_file = os.path.join(base_dir, "data", "output", "execution_log.csv")
    templates_dir = os.path.join(base_dir, "templates")

    print(f"Iniciando Sistema de Cobrança AuroraPay...")
    if args.test:
        print("⚠️  MODO DE TESTE ATIVADO: Ignorando idempotência e marcando e-mails como [TESTE]")
    if args.rule:
        print(f"🎯 FILTRO ATIVO: Executando apenas regra '{args.rule}'")
        
    print(f"Lendo dados de: {input_file}")
    
    # Initialize Adapters
    excel_adapter = ExcelAdapter(input_file)
    log_adapter = LogAdapter(log_file)
    email_adapter = EmailAdapter(templates_dir)
    
    # Initialize Service
    manager = BillingManager(excel_adapter, email_adapter, log_adapter)
    
    # Run
    manager.process_billing(force_test=args.test, target_rule=args.rule) 
    print("Processamento concluído. Verifique o log em data/output/.")

if __name__ == "__main__":
    main()
