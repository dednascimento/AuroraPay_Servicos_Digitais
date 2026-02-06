from datetime import date
from typing import List
from src.core.domain import Invoice, BillingAction
from src.infrastructure.log_adapter import LogAdapter
from src.infrastructure.email_adapter import EmailAdapter
from src.utils.debug_logger import log_debug

class BillingManager:
    def __init__(self, excel_adapter, email_adapter, log_adapter):
        self.excel_adapter = excel_adapter
        self.email_adapter = email_adapter
        self.log_adapter = log_adapter

    def process_billing(self, force_test: bool = False, target_rule: str = None):
        invoices = self.excel_adapter.read_invoices()
        today = date.today()

        for invoice in invoices:
            self._process_single_invoice(invoice, today, force_test, target_rule)

    def _process_single_invoice(self, invoice: Invoice, today: date, force_test: bool, target_rule: str = None):
        rule = self._determine_rule(invoice.due_date, today)
        
        if not rule:
            return # No action needed for this day

        # Filter by Target Rule (if specified)
        if target_rule and rule != target_rule:
             return


        # Check Idempotency ONLY if NOT in test mode
        if not force_test:
            if self.log_adapter.has_action_been_performed(invoice.invoice_id, rule):
                print(f"Skipping {invoice.invoice_id} for rule {rule}: Already performed today.")
                return
        else:
             print(f"[TEST MODE] Forcing execution for {invoice.invoice_id} rule {rule}")

        # Execute Action
        if invoice.accepts_communication:
            success = self.email_adapter.send_template_email(invoice, rule, is_test_mode=force_test)
            action_status = "SUCCESS" if success else "FAILED"
            self.log_adapter.log_action(invoice.invoice_id, rule, action_status)
        else:
            self.log_adapter.log_action(invoice.invoice_id, rule, "SKIPPED_OPT_OUT")

    def _determine_rule(self, due_date: date, today: date) -> str:
        delta = (today - due_date).days
        log_debug(f"[BillingManager] Vencimento: {due_date} | Hoje: {today} | Delta: {delta} dias")
        
        # Mapping Delta to Rules (Files in templates/email/)
        # D-5: 5 days before due date -> due_date - today = 5 -> delta = -5
        # D0: Due date -> delta = 0
        # D+3: 3 days after -> delta = 3
        # D+7: 7 days after -> delta = 7
        
        if delta == -5:
            return "D-5"
        elif delta == 0:
            return "D0"
        elif delta == 3:
            return "D+3"
        elif delta == 7:
            return "D+7"
        
        return "" 
