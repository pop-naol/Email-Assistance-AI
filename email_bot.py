#made by @naolsime



import os
import smtplib
import cohere
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

load_dotenv()

class EmailAssistant:
    def __init__(self):
        
        self.co = cohere.Client(os.getenv("CO_API_KEY"))
        
        
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GMAIL_ADDRESS")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD")
        
        if not all([self.sender_email, self.sender_password]):
            raise ValueError("Missing email credentials in .env file")

    def generate_reply(self, original_email: str) -> str:
        """Generate professional email reply using Cohere"""
        prompt = f"""Write a concise, professional email reply to this message:
        {original_email}
        
        Reply:"""
        
        response = self.co.chat(
            model="command",
            message=prompt,
            temperature=0.7,
            preamble="You are a professional email assistant"
        )
        return response.text.split("---")[0].strip()

    def send_email(self, recipient: str, subject: str, body: str):
        """Send email using SMTP"""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)

def main():
    print("=== Email Assistant ===")
    print("----------------------\n")
    
    try:
        assistant = EmailAssistant()
        
        
        recipient = input("Recipient email address: ")
        subject = input("Email subject: ")
        print("\nPaste the original email (press twice  Enter when done):")
        original_email = '\n'.join(iter(input, ''))
        
        if not all([recipient, subject, original_email]):
            raise ValueError("Missing required information")
        
        print("\nGenerating reply...")
        reply_body = assistant.generate_reply(original_email)
     
        print("\n=== Generated Reply ===")
        print(reply_body)
        print("----------------------")
        
        if input("\nSend this reply? (y/n): ").lower() == 'y':
            assistant.send_email(recipient, subject, reply_body)
            print("\nEmail sent successfully!")
        else:
            print("\nReply not sent.")
            
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
