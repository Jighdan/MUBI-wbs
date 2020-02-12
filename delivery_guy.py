import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_to_email(sender_email, sender_passwd, receiver_email, content): 
	try:
		# prepares email #
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Film of the Week'
		msg['From'] = sender_email
		msg['To'] = receiver_email

		msg_parts = MIMEText(content, 'html')
		msg.attach(msg_parts)
		# connecs to gmail servers #
		smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
		smtpObj.starttls()
		# logs in the bot email account #
		smtpObj.login(sender_email, sender_passwd)
		# sends the email #
		smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
		# disconnects from the server #
		smtpObj.quit()
		print('Email sent')
	except SMTPException:
		print('Error sending email')

def content_generator(info):
	content = """\
	<html>
		<style>
			p {
				text-align: center
			}
		<h1 style="text-align: center;">%s</h1>
		<body>
			<p><img style="display: block; margin-left: auto; margin-right: auto;" src="%s" width="405" height="256" /></p>
			<p><em>Directed by: </em><span style="text-decoration: underline;">%s</span></p>
			<p><strong>Genre: </strong><em>%s</em>
			<p><strong>Country: </strong>%s<strong> Year:</strong><em> %s</em></p>
			<p><strong>	Sypnosis</strong></p>
			<p>%s</p>
			<p><strong>Focus / MUBI Take</strong></p>
			<p>%s</p>
		</body>
	</html>
	""" % (info[1], info[0], info[2], info[7], info[3], info[4], info[5], info[6])
	return content