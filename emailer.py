import smtplib
from email.mime.text import MIMEText

def errorEmail():
	content = """From: Raspberry Pi <tonyraspberrypi19@gmail.com>
	To: Tony <athomps@sas.upenn.edu>
	Subject: Error in torrenter caused crash
	
	"""
	try:
		mail = smtplib.SMTP('smtp.gmail.com',587)
		mail.ehlo()
		mail.starttls()
		mail.login('tonyraspberrypi19@gmail.com','penislolol')
		mail.sendmail('tonyraspberrypi19@gmail.com','athomps@sas.upenn.edu',content) 
		mail.close()
		print("Sent")
	except:
		print "Error: unable to send email"
def showUpdateEmail(fileNames):

	content = "The following files were added to the library: \n" 
	for fileName in fileNames:
		content += fileName + "\n"
	msg = MIMEText(content)
	msg['Subject'] = "Library Update"
	msg['From'] = "tonyraspberrypi19@gmail.com"
	msg['To'] = "athomps@sas.upenn.edu"
	try:
		mail = smtplib.SMTP('smtp.gmail.com',587)
		mail.ehlo()
		mail.starttls()
		mail.login('tonyraspberrypi19@gmail.com','penislolol')
		mail.sendmail('tonyraspberrypi19@gmail.com','athomps@sas.upenn.edu',msg.as_string()) 
		mail.close()
		print("Sent")
	except:
		print "Error: unable to send email"
