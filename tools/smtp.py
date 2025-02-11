import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from db import get_users, update_user_pass
from passlib.context import CryptContext
from .pass_generator import gerador_senha_super_seguro

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Carregar variáveis do .env
load_dotenv()

# Obter credenciais do .env
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

def enviar_mensagem(mensagem_texto: str,
                    sender: str,
                    assunto: str,
                    senha_pass_sv: str,
                    destinatario: str) -> bool | None:
    try:
        print("Iniciando Envio...")
        print(f"Destinatário: {destinatario}")

        # Criar o e-mail
        mensagem = EmailMessage()
        mensagem.set_content(mensagem_texto)
        mensagem["Subject"] = assunto
        mensagem["From"] = sender
        mensagem["To"] = destinatario

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, senha_pass_sv)
            server.send_message(mensagem)

        print("E-mail enviado com sucesso!")
        return True

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def enviar_mensagem_admin() -> bool | None:
    users = get_users()
    for index, user in enumerate(users):
        if index == 0:  
            username = user.username
            destinatario = user.email
            

            nova_senha = gerador_senha_super_seguro() 

            mensagem_texto = (
                f"Olá, {username}!\n\n"
                "Este é um teste de envio de e-mail.\n"
                f"Sua nova senha temporária é: {nova_senha}\n"
                "Por favor, altere sua senha após o login."
            )
            assunto = "Nova Senha Temporária"
            sender = EMAIL
            senha_pass_sv = SENHA
            
            update_user_pass(user_id=user.id, new_password=nova_senha)
            
            status = enviar_mensagem(mensagem_texto=mensagem_texto,
                            sender=sender,
                            assunto=assunto,
                            senha_pass_sv=senha_pass_sv,
                            destinatario=destinatario
            )
            return status
                            