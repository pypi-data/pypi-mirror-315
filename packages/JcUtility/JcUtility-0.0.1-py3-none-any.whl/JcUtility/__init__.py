import email
from email.header import decode_header
from bs4 import BeautifulSoup

__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '0.0.1'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/python-pkg/JcUtil'
__all__ = ['JcFile', 'JcMailText', 'JcString']

class JcFile:
    def __init__(self):
        pass
    def read_all_text(self, path):
        file = open(path, "rt")
        content = file.read()
        file.close()
        return content
    def write_all_text(self, path, content):
        file = open(path, "wb")
        jcstr = JcString()
        #file.write(content.replace("\r\n", "\n").replace("\r", "\n").encode())
        file.write(jcstr.adjust_new_line(content).encode())
        file.close()

class JcMailText:
    def __init__(self):
        pass
    def get_mail_text(self, raw_email, with_subject = False):
        try:
          raw_email = raw_email.decode()
        except (UnicodeDecodeError, AttributeError):
           pass
        b = email.message_from_string(raw_email)
        body = ""
        if b.is_multipart():
            for part in b.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                #print(f"ctype: {ctype} cdispo: {cdispo}")
                if (ctype == 'text/plain' or ctype == 'text/html') and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
        else:
            body = b.get_payload(decode=True)
        if not isinstance(body, str):
            body = body.decode("utf-8")
        if body.startswith('<html'):
            soup = BeautifulSoup(body, features="html.parser")
            body = soup.get_text('\n')
        if with_subject:
            #print (email.utils.parseaddr(b['From']))
            mail_to = b['To']
            mail_from = b['From']
            subject = decode_header(b['Subject'])
            subject = subject[0][0].decode(subject[0][1])
            body = f"JcMailText-From: {mail_from}\nJcMailText-To: {mail_to}\nJcMailText-Subject: {subject}\n{body}" 
        return body

class JcString:
    def __init__(self):
        pass
    def adjust_new_line(self, str):
        return str.replace("\r\n", "\n").replace("\r", "\n")
