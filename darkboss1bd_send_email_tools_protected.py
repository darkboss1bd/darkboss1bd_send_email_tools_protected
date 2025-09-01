#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 DARKBOSS1BD - Protected Email Sender Tool
🔐 Version: 1.0 | Protected Code
⚠️ Unauthorized copying/distribution prohibited
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
import hashlib
import getpass
import json
import os
import sys

# 🛡️ Anti-Debugging System
def anti_debug():
    start_time = time.time()
    while True:
        if time.time() - start_time > 1000:
            messagebox.showerror("Security Alert", "Debugger detected! Application terminated.")
            sys.exit()
        time.sleep(5)

# 🔒 License & Authentication System
class LicenseManager:
    def __init__(self):
        self.license_file = "license.dat"
        self.machine_id = self.get_machine_id()
    
    def get_machine_id(self):
        username = getpass.getuser()
        return hashlib.md5(username.encode()).hexdigest()[:12]
    
    def generate_license_key(self):
        return hashlib.sha256(self.machine_id.encode()).hexdigest()[:16].upper()
    
    def create_license(self):
        license_data = {
            "machine_id": self.machine_id,
            "license_key": self.generate_license_key(),
            "created": time.ctime(),
            "version": "1.0"
        }
        with open(self.license_file, "w") as f:
            json.dump(license_data, f)
        return license_data
    
    def verify_license(self):
        if not os.path.exists(self.license_file):
            return self.setup_new_license()
        
        try:
            with open(self.license_file, "r") as f:
                data = json.load(f)
            
            if data.get("machine_id") == self.machine_id:
                expected_key = self.generate_license_key()
                if data.get("license_key") == expected_key:
                    return True
        except:
            pass
        
        messagebox.showerror("License Error", "Invalid or corrupted license!")
        return False
    
    def setup_new_license(self):
        license_data = self.create_license()
        messagebox.showinfo("License Setup", 
                          f"New license created!\nKey: {license_data['license_key']}\nKeep this safe.")
        return True

# 🔐 Access Control
def verify_access():
    password = "darkboss123"  # In real app, this should be encrypted
    try:
        user_input = simpledialog.askstring("🔒 Access Required", 
                                          "Enter Tool Password:", show='*')
        if user_input != password:
            messagebox.showerror("❌ Access Denied", "Invalid Password!")
            return False
        return True
    except:
        return False

# 🎨 ASCII Art Animation
def computer_animation(banner_label):
    frames = [
        """
  ╔══════════════════════════════════════╗
  ║  ┌────────────────────────────────┐  ║
  ║  │    DARKBOSS1BD - PROTECTED     │  ║
  ║  │      Email Sender v1.0         │  ║
  ║  │    🔐 Code Protection Active   │  ║
  ║  └────────────────────────────────┘  ║
  ╚══════════════════════════════════════╝
        ████████████████████████
        """,
        """
  ╔══════════════════════════════════════╗
  ║  ┌────────────────────────────────┐  ║
  ║  │    DARKBOSS1BD - PROTECTED     │  ║
  ║  │      Sending Emails...         │  ║
  ║  │    ⚡ Processing Requests       │  ║
  ║  └────────────────────────────────┘  ║
  ╚══════════════════════════════════════╝
        ████████████████████████
        """,
        """
  ╔══════════════════════════════════════╗
  ║  ┌────────────────────────────────┐  ║
  ║  │    DARKBOSS1BD - PROTECTED     │  ║
  ║  │      ✅ Emails Sent!           │  ║
  ║  │    🛡️ Protected Session        │  ║
  ║  └────────────────────────────────┘  ║
  ╚══════════════════════════════════════╝
        ████████████████████████
        """
    ]
    for frame in frames:
        try:
            banner_label.config(text=frame)
            banner_label.update()
            time.sleep(1)
        except:
            break

# 📧 Email Sending Function
def send_emails(smtp_server, smtp_port, sender_email, sender_password, 
                subject, body, recipients, banner_label):
    
    if not all([smtp_server, sender_email, sender_password, subject, body]) or not recipients:
        messagebox.showerror("Error", "Please fill all fields and recipients!")
        return

    def send_process():
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            for recipient in recipients:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                server.sendmail(sender_email, recipient, msg.as_string())

            server.quit()
            messagebox.showinfo("Success", "✅ Emails sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to send emails:\n{str(e)}")

    # Start animation and send process
    threading.Thread(target=computer_animation, args=(banner_label,), daemon=True).start()
    threading.Thread(target=send_process, daemon=True).start()

# 🖥️ Main GUI Application
class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📧 DARKBOSS1BD - Protected Email Sender")
        self.root.geometry("750x700")
        self.root.configure(bg="#0d0d0d")
        self.root.resizable(True, True)
        
        # 🛡️ Start anti-debugging
        threading.Thread(target=anti_debug, daemon=True).start()
        
        # 🔐 License check
        self.license_manager = LicenseManager()
        if not self.license_manager.verify_license():
            sys.exit()
        
        # 🔒 Access verification
        if not verify_access():
            sys.exit()
        
        self.create_widgets()
    
    def create_widgets(self):
        # 🎨 Banner
        self.banner_label = tk.Label(self.root, text="", font=("Courier", 10), 
                                   bg="#0d0d0d", fg="#00ff00")
        self.banner_label.pack(pady=10)
        
        # ⚙️ SMTP Settings Frame
        smtp_frame = tk.LabelFrame(self.root, text="⚙️ SMTP Settings", 
                                 bg="#1a1a1a", fg="#00ff00", font=("Arial", 10, "bold"))
        smtp_frame.pack(fill="x", padx=15, pady=10)
        
        # SMTP Server
        tk.Label(smtp_frame, text="SMTP Server:", bg="#1a1a1a", fg="white").grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        self.smtp_entry = tk.Entry(smtp_frame, width=25, bg="#2d2d2d", fg="white")
        self.smtp_entry.grid(row=0, column=1, padx=5, pady=5)
        self.smtp_entry.insert(0, "smtp.gmail.com")
        
        # Port
        tk.Label(smtp_frame, text="Port:", bg="#1a1a1a", fg="white").grid(
            row=0, column=2, sticky="w", padx=10, pady=5)
        self.port_entry = tk.Entry(smtp_frame, width=10, bg="#2d2d2d", fg="white")
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)
        self.port_entry.insert(0, "587")
        
        # Email
        tk.Label(smtp_frame, text="Email:", bg="#1a1a1a", fg="white").grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(smtp_frame, width=25, bg="#2d2d2d", fg="white")
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(smtp_frame, text="Password:", bg="#1a1a1a", fg="white").grid(
            row=1, column=2, sticky="w", padx=10, pady=5)
        self.password_entry = tk.Entry(smtp_frame, show="*", width=20, bg="#2d2d2d", fg="white")
        self.password_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # ✉️ Email Content Frame
        content_frame = tk.LabelFrame(self.root, text="✉️ Email Content", 
                                    bg="#1a1a1a", fg="#00ff00", font=("Arial", 10, "bold"))
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Subject
        tk.Label(content_frame, text="Subject:", bg="#1a1a1a", fg="white").grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        self.subject_entry = tk.Entry(content_frame, width=60, bg="#2d2d2d", fg="white")
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Body
        tk.Label(content_frame, text="Body:", bg="#1a1a1a", fg="white").grid(
            row=1, column=0, sticky="nw", padx=10, pady=5)
        self.body_text = scrolledtext.ScrolledText(content_frame, width=60, height=8,
                                                 bg="#2d2d2d", fg="white")
        self.body_text.grid(row=1, column=1, padx=5, pady=5)
        
        # 👥 Recipients Frame
        recipients_frame = tk.LabelFrame(self.root, text="👥 Recipients (One per line)", 
                                       bg="#1a1a1a", fg="#00ff00", font=("Arial", 10, "bold"))
        recipients_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.recipient_text = scrolledtext.ScrolledText(recipients_frame, width=60, height=8,
                                                      bg="#2d2d2d", fg="white")
        self.recipient_text.pack(padx=10, pady=10)
        
        # 🚀 Send Button
        self.send_button = tk.Button(self.root, text="🚀 SEND PROTECTED EMAILS", 
                                   command=self.process_emails,
                                   bg="#006600", fg="white", font=("Arial", 12, "bold"),
                                   padx=20, pady=10)
        self.send_button.pack(pady=15)
        
        # © Watermark
        watermark = tk.Label(self.root, 
                           text="© 2024 DARKBOSS1BD | 🔐 PROTECTED CODE | UNAUTHORIZED COPYING PROHIBITED",
                           bg="#0d0d0d", fg="#ff0000", font=("Arial", 8))
        watermark.pack(side="bottom", pady=5)
        
        # Start initial animation
        threading.Thread(target=computer_animation, args=(self.banner_label,), daemon=True).start()
    
    def process_emails(self):
        try:
            smtp_server = self.smtp_entry.get()
            smtp_port = int(self.port_entry.get())
            sender_email = self.email_entry.get()
            sender_password = self.password_entry.get()
            subject = self.subject_entry.get()
            body = self.body_text.get("1.0", tk.END)
            recipients = [r.strip() for r in self.recipient_text.get("1.0", tk.END).strip().split("\n") if r.strip()]
            
            send_emails(smtp_server, smtp_port, sender_email, sender_password,
                       subject, body, recipients, self.banner_label)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

# 🚀 Application Entry Point
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = EmailSenderApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application Error: {e}")