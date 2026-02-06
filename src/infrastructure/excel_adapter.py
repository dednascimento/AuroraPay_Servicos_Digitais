import pandas as pd
from typing import List
from datetime import datetime, date
from src.core.domain import Invoice, InvoiceItem
from src.utils.debug_logger import log_debug

class ExcelAdapter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_invoices(self) -> List[Invoice]:
        try:
            # Read 3 sheets
            xls = pd.ExcelFile(self.file_path)
            df_clientes = pd.read_excel(xls, 'Clientes')
            df_faturas = pd.read_excel(xls, 'Faturas')
            df_itens = pd.read_excel(xls, 'Itens')

            # Normalize columns
            df_clientes.columns = [str(c).lower().strip() for c in df_clientes.columns]
            df_faturas.columns = [str(c).lower().strip() for c in df_faturas.columns]
            df_itens.columns = [str(c).lower().strip() for c in df_itens.columns]

            log_debug(f"[ExcelAdapter] Loaded {len(df_clientes)} clients, {len(df_faturas)} invoices, {len(df_itens)} items")

            invoices = []
            
            # Iterate over Invoices (Main Entity)
            for _, row_fat in df_faturas.iterrows():
                invoice_id = str(row_fat.get('fatura_id'))
                client_id = str(row_fat.get('cliente_id'))
                
                # Find Client
                client_data = df_clientes[df_clientes['cliente_id'].astype(str) == client_id]
                if client_data.empty:
                    log_debug(f"[ExcelAdapter] Warning: Client {client_id} not found for Invoice {invoice_id}")
                    continue
                row_cli = client_data.iloc[0]

                # Find Items
                items_data = df_itens[df_itens['fatura_id'].astype(str) == invoice_id]
                invoice_items = []
                for _, row_item in items_data.iterrows():
                    invoice_items.append(InvoiceItem(
                        description=str(row_item.get('descricao')),
                        amount=float(row_item.get('valor'))
                    ))

                # Parse Date
                raw_date = row_fat.get('data_vencimento')
                if isinstance(raw_date, (str, datetime, date)):
                    if isinstance(raw_date, str):
                        due_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                    elif isinstance(raw_date, datetime):
                        due_date = raw_date.date()
                    else:
                        due_date = raw_date
                else:
                    due_date = datetime.now().date()

                invoice = Invoice(
                    invoice_id=invoice_id,
                    customer_name=str(row_cli.get('nome')),
                    amount=invoice_items[0].amount if not invoice_items else sum(i.amount for i in invoice_items), # Recalculate or use total? Using sum of items is safer.
                    due_date=due_date,
                    email=str(row_cli.get('email')),
                    accepts_communication=True, # Assuming true for now
                    items=invoice_items
                )
                invoices.append(invoice)
                
            return invoices
        except Exception as e:
            print(f"Error reading Excel V2: {e}")
            log_debug(f"[ExcelAdapter] ERROR: {e}")
            return []
