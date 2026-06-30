import os
import imaplib
import email
import json
import datetime
import google.generativeai as genai
from email.header import decode_header

# 🛰️ SYNAPSE EMAIL HARVESTER: SOBERANIA DE COMUNICAÇÃO
# Sincroniza emails do servidor IMAP (ex: USP) e gera insights no Vault.

VAULT_EMAIL_DIR = "/opt/synapse_vault/email_sync"
MODEL_NAME = "gemini-1.5-flash"

def get_config():
    config = {}
    vault_env = "/opt/synapse_vault/.env"
    if os.path.exists(vault_env):
        with open(vault_env, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip().strip('"').strip("'")
    return config

def fetch_emails(user, password, server="imap.usp.br"):
    print(f"📡 Conectando ao servidor IMAP: {server}...")
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, password)
        mail.select("inbox")
        
        # Buscar emails de hoje
        date = (datetime.date.today()).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{date}")')
        
        email_list = []
        for num in messages[0].split():
            status, data = mail.fetch(num, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    
                    sender = msg.get("From")
                    date_str = msg.get("Date")
                    
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    email_list.append({
                        "subject": subject,
                        "from": sender,
                        "date": date_str,
                        "body": body[:2000] # Limite para o prompt
                    })
        
        mail.logout()
        return email_list
    except Exception as e:
        print(f"❌ Erro ao buscar emails: {e}")
        return []

def summarize_emails(email_list, api_key):
    if not email_list:
        return "Nenhum email novo hoje."
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = f"""
    Atue como o Synapse Intelligence Harvester. 
    Analise os seguintes emails recebidos hoje e gere um resumo executivo soberano para o Maestro.
    Extraia Action Items, Prazos e Insights Estratégicos.
    
    EMAILS:
    {json.dumps(email_list, indent=2)}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro na sumarização: {e}"

def main():
    config = get_config()
    api_key = config.get("GEMINI_API_KEY")
    user = config.get("EMAIL_USER")
    password = config.get("EMAIL_PASS")
    server = config.get("EMAIL_IMAP_SERVER", "imap.usp.br")

    if not api_key or not user or not password:
        print("⚠️  Credenciais de email ou API Key ausentes no Vault.")
        print("💡 Adicione EMAIL_USER, EMAIL_PASS e EMAIL_IMAP_SERVER ao /opt/synapse_vault/.env")
        return

    emails = fetch_emails(user, password, server)
    if emails:
        summary = summarize_emails(emails, api_key)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists(VAULT_EMAIL_DIR):
            os.makedirs(VAULT_EMAIL_DIR)
            
        report_path = os.path.join(VAULT_EMAIL_DIR, f"email_report_{timestamp}.md")
        with open(report_path, "w") as f:
            f.write(f"# 📬 RESUMO SOBERANO DE EMAILS - {datetime.date.today()}\n\n")
            f.write(summary)
            
        print(f"✅ Relatório de emails gerado: {report_path}")
    else:
        print("📭 Nenhum email novo para processar.")

if __name__ == "__main__":
    main()
