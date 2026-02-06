import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from src.core.domain import Invoice
from datetime import date
from src.utils.debug_logger import log_debug

# Load environment variables
load_dotenv()

class EmailAdapter:
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SMTP_EMAIL")
        _password = os.getenv("SMTP_PASSWORD")
        self.sender_password = _password.replace(" ", "") if _password else None

    def send_template_email(self, invoice: Invoice, rule: str, is_test_mode: bool = False) -> bool:
        if not self.sender_email or "seu_email" in self.sender_email:
            print("[EmailAdapter] ERRO: Credenciais de e-mail não configuradas no arquivo .env")
            return False

        # Try to find HTML template first
        template_path = os.path.join(self.templates_dir, "email", f"{rule}.html")
        is_html = True
        
        if not os.path.exists(template_path):
            # Fallback to MD
            template_path = os.path.join(self.templates_dir, "email", f"{rule}.md")
            is_html = False
        
        if not os.path.exists(template_path):
            print(f"[EmailAdapter] Error: Template not found at {template_path}")
            return False

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Placeholder substitution
            subject = f"Notificação AuroraPay: {rule}"
            if rule == "D0": subject = "Sua fatura vence hoje!"
            elif rule == "D-5": subject = "Lembrete: Fatura próxima do vencimento"
            elif rule == "D+3": subject = "Aviso: Fatura em atraso"
            
            if is_test_mode:
                subject = f"[TESTE] {subject}"

            # Generate Items Table HTML
            items_html = self._generate_items_table(invoice.items)

            # Calculate days delta
            today = date.today()
            delta = (invoice.due_date - today).days
            
            dias_para_vencer = delta if delta > 0 else 0
            dias_atraso = abs(delta) if delta < 0 else 0
            
            body_content = content.replace("{{ nome }}", invoice.customer_name)\
                                      .replace("{{ valor }}", f"R$ {invoice.amount:.2f}")\
                                      .replace("{{ vencimento }}", invoice.due_date.strftime("%d/%m/%Y"))\
                                      .replace("{{ link_boleto }}", f"http://fatura.com/{invoice.invoice_id}")\
                                      .replace("{{ invoice_id }}", invoice.invoice_id)\
                                      .replace("{{ items_table }}", items_html)\
                                      .replace("{{ dias_para_vencer }}", str(dias_para_vencer))\
                                      .replace("{{ dias_atraso }}", str(dias_atraso))


            # Create Message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = invoice.email
            msg['Subject'] = subject
            
            # Attach plain text version (simplified from html or raw md)
            text_part = MIMEText("Por favor, visualize este e-mail em um cliente que suporte HTML.", 'plain')
            msg.attach(text_part)
            
            # Attach HTML version
            if is_html:
                html_part = MIMEText(body_content, 'html')
                msg.attach(html_part)
            else:
                # If using old MD, send as plain text
                msg.attach(MIMEText(body_content, 'plain'))

            # Connect and Send
            try:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, invoice.email, msg.as_string())
                server.quit()
                
                log_debug(f"[EmailAdapter] SUCESSO envindo para {invoice.email} | Assunto: {subject}")
                print(f"--- [REAL] EMAIL ENVIADO PARA {invoice.email} ---")
                return True
            except Exception as smtp_err:
                log_debug(f"[EmailAdapter] ERRO SMTP: {smtp_err}")
                print(f"[EmailAdapter] SMTP Connection Error: {smtp_err}")
                return False

        except Exception as e:
            print(f"[EmailAdapter] Failed to prepare email: {e}")
            return False

    def _generate_items_table(self, items) -> str:
        if not items:
            return "<p><em>Sem detalhes disponíveis</em></p>"
        
        html = '<table class="items-table" width="100%"><thead><tr><th>Descrição</th><th style="text-align:right;">Valor</th></tr></thead><tbody>'
        
        for item in items:
            html += f'<tr><td>{item.description}</td><td class="price">R$ {item.amount:.2f}</td></tr>'
            
        html += '</tbody></table>'
        return html
