from email.message import EmailMessage
import os
import smtplib

def test(body):
	msg = EmailMessage()
	msg.set_content(body)
	msg['Subject'] = "Testing sending an email message."
	msg['From'] = 'don@donaldbales.com'
	msg['To'] = 'donaldbales@mac.com'
	# creates SMTP session
	s = smtplib.SMTP('netsol-smtp-oxcs.hostingplatform.com', 587)
	# start TLS for security
	s.starttls()
	# Authentication
	password = os.getenv('EMAIL_PASSWORD', '')
	print(password)
	s.login("don@donaldbales.com", password)
	# sending the mail
	s.sendmail("don@donaldbales.com", "donaldbales@mac.com", msg.as_string())
	# terminating the session
	s.quit()
	return True

test("Did this work?")
