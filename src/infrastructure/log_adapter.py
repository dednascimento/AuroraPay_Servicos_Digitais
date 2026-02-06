import csv
import os
from datetime import date
from typing import List, Dict
from src.core.domain import Invoice, BillingAction

class LogAdapter:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'invoice_id', 'rule', 'action', 'details'])

    def log_action(self, invoice_id: str, rule: str, action: str, details: str = ""):
        with open(self.log_file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([date.today().isoformat(), invoice_id, rule, action, details])

    def get_todays_actions(self) -> List[Dict]:
        """Returns a list of actions performed TODAY to avoid duplicates."""
        actions = []
        today_str = date.today().isoformat()
        if not os.path.exists(self.log_file_path):
            return []
            
        with open(self.log_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('timestamp') == today_str:
                    actions.append(row)
        return actions

    def has_action_been_performed(self, invoice_id: str, rule: str) -> bool:
        """Checks if a specific rule was already applied to an invoice TODAY."""
        # Note: Depending on requirements, idempotency might be 'ever' or 'today'.
        # For a billing ruler, usually it is 'once per cycle' but since we run daily, 'today' check prevents double run on same day.
        # However, we must ensure we don't send D+3 twice if script runs on D+3 and D+4 (wait, D+3 is a specific day).
        # So 'today' check is sufficient if the rule is strictly "Day == X".
        
        todays = self.get_todays_actions()
        for action in todays:
            if action['invoice_id'] == str(invoice_id) and action['rule'] == rule:
                return True
        return False
