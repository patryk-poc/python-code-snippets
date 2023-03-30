#!/usr/bin/env python3
"""Get e-mail from the Gmail user."""
import email
import imaplib


class GmailClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.mail = None

    def login(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.email, self.password)

    def logout(self):
        self.mail.logout()

    def get_email_list(self):
        self.mail.select('inbox')
        _, data = self.mail.search(None, 'ALL')
        email_ids = data[0].split()
        email_list = []
        for email_id in email_ids:
            _, data = self.mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            email_list.append({
                'subject': msg['Subject'],
                'from': msg['From'],
                'to': msg['To'],
                'date': msg['Date'],
                'size': len(data[0][1])
            })
        return email_list

    def sort_emails_by_size(self, email_list):
        return sorted(email_list, key=lambda k: k['size'], reverse=True)

    def display_top_n_largest_emails(self, email_list, n):
        sorted_email_list = self.sort_emails_by_size(email_list)
        print(f'Top {n} largest emails by size:')
        for i in range(n):
            email = sorted_email_list[i]
            print(f"{i + 1}. Subject: {email['subject']} | From: {email['from']} | To: {email['to']} | Date: {email['date']} | Size: {email['size']} bytes")


if __name__ == '__main__':
    email_address = input('Enter your email address: ')
    password = input('Enter your password: ')
    gmail_client = GmailClient(email_address, password)
    gmail_client.login()
    email_list = gmail_client.get_email_list()
    gmail_client.display_top_n_largest_emails(email_list, 5)
    gmail_client.logout()
