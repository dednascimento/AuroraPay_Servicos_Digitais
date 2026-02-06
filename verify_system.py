import pandas as pd
from datetime import date, timedelta
import os
import sys

# Setup path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.excel_adapter import ExcelAdapter
from src.infrastructure.email_adapter import EmailAdapter
from src.infrastructure.log_adapter import LogAdapter
from src.services.billing_manager import BillingManager

def verify():
    print("--- INICIANDO VERIFICAÇÃO AUTOMATIZADA ---")
    
    # 1. Create Mock Data
    today = date.today()
    data = [
        {"cliente_id": "TEST_01", "nome_cliente": "Cliente D-5", "valor": 100.0, "vencimento": today + timedelta(days=5), "email": "d5@test.com", "aceita_comunicacao": True},
        {"cliente_id": "TEST_02", "nome_cliente": "Cliente D0", "valor": 200.0, "vencimento": today, "email": "d0@test.com", "aceita_comunicacao": True},
        {"cliente_id": "TEST_03", "nome_cliente": "Cliente D+3", "valor": 300.0, "vencimento": today - timedelta(days=3), "email": "d3@test.com", "aceita_comunicacao": True},
        {"cliente_id": "TEST_04", "nome_cliente": "Cliente Ignorado", "valor": 400.0, "vencimento": today - timedelta(days=10), "email": "ignore@test.com", "aceita_comunicacao": True},
        {"cliente_id": "TEST_USER_01", "nome_cliente": "Deivid (Corp)", "valor": 1250.0, "vencimento": today, "email": "deividnascimento.corporativo@gmail.com", "aceita_comunicacao": True},
        {"cliente_id": "TEST_USER_02", "nome_cliente": "ACS Legendados", "valor": 75.90, "vencimento": today + timedelta(days=5), "email": "acslegendados16@gmail.com", "aceita_comunicacao": True},
        {"cliente_id": "TEST_05", "nome_cliente": "Cliente OptOut", "valor": 500.0, "vencimento": today, "email": "optout@test.com", "aceita_comunicacao": False},
    ]
    
    test_input = "data/input/test_sample.xlsx"
    pd.DataFrame(data).to_excel(test_input, index=False)
    print(f"[OK] Arquivo de teste criado: {test_input}")
    
    # 2. Setup Adapters with Test files
    test_log = "data/output/test_log.csv"
    if os.path.exists(test_log):
        os.remove(test_log)
        
    excel = ExcelAdapter(test_input)
    # email adapter pointing to real templates
    email = EmailAdapter("templates") 
    log = LogAdapter(test_log)
    
    # 3. Process
    manager = BillingManager(excel, email, log)
    manager.process_billing()
    
    # 4. Verify Output
    print("\n--- VRERIFICANDO LOGS ---")
    df_log = pd.read_csv(test_log)
    print(df_log[['invoice_id', 'rule', 'action']])
    
    # Assertions
    assert not df_log[df_log['invoice_id'] == 'TEST_01'].empty, "TEST_01 (D-5) deveria ter sido processado"
    assert not df_log[df_log['invoice_id'] == 'TEST_02'].empty, "TEST_02 (D0) deveria ter sido processado"
    assert not df_log[df_log['invoice_id'] == 'TEST_03'].empty, "TEST_03 (D+3) deveria ter sido processado"
    assert df_log[df_log['invoice_id'] == 'TEST_04'].empty, "TEST_04 (D-10) NÃO deveria ter sido processado"
    
    # Verify New Users
    assert not df_log[df_log['invoice_id'] == 'TEST_USER_01'].empty, "Deivid (D0) deve receber email"
    assert not df_log[df_log['invoice_id'] == 'TEST_USER_02'].empty, "ACS (D-5) deve receber email"

    opt_out = df_log[df_log['invoice_id'] == 'TEST_05'].iloc[0]
    assert opt_out['action'] == 'SKIPPED_OPT_OUT', "TEST_05 deveria ter sido SKIPPED"

    print("\n[SUCESSO] Todos os testes passaram!")

if __name__ == "__main__":
    verify()
