#!/usr/bin/python2

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os, sys
from optparse import OptionParser

gmail_user = "foo@miempresa.com"
gmail_pwd = "foobar"

def mailAttach(to, subject, text, attach):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(text))
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
        'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)
    
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.quit()
    mailServer.close()

def mail(to, subject, text):
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.set_debuglevel(1)
    mailServer.ehlo()
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:'+subject+' \n'
    msg = header + '\n '+text+' \n\n'
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    
    print mailServer.sendmail(gmail_user, to, msg)
    # Should be mailServer.quit(), but that crashes...
    mailServer.quit()
    mailServer.close()

parser = OptionParser()
parser.add_option("-f", "--file",
                  action="store", type="string", dest="filename")
parser.add_option("-s", "--subject",
                  action="store", type="string", dest="subject")
parser.add_option("-b", "--body",
                  action="store", type="string", dest="body")
parser.add_option("-r", "--receipt",
                  action="store", type="string", dest="receipt")

(opts, args) = parser.parse_args()


if opts.filename == None:
    mail(opts.receipt, opts.subject, opts.body)
else:
    filetosend = opts.filename
    if filetosend[-3:] == 'gsm':
        filetosend = "/tmp/%s.mp3" % (os.path.basename(filetosend)[:-4])
        os.system("sox -v 2 %s -r 8000 -c 1 %s >/dev/null 2>&1"%(opts.filename,filetosend))
    mailAttach(opts.receipt, opts.subject, opts.body, filetosend)
    if filetosend[-3:] == 'mp3':
        try: os.remove(filetosend)
        except: pass

sys.exit(0)
