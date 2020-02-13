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
		<link href="https://fonts.googleapis.com/css?family=Fondamento|Shadows+Into+Light&display=swap" rel="stylesheet">
		<style>
			p {
				text-align: center;
				font-family: 'Fondamento', cursive;
			}
			#main-card {
				box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
				padding: 10px;
			}
			#descriptive-text {
				line-height: 25px;
				text-align: center;
			}
		</style>
		<div id='main-card'>
			<body style='padding: 20px;'>
				<h1 style="text-align: center; font-family: 'Fondamento', cursive;">%s</h1>
				<hr>
				<div id='main-card>'
					<img style="display: block; margin-left: auto; margin-right: auto;" src="%s" width="405" height="256" />
					<hr>
					<p><em><strong>Directed by: </strong></em><span style="text-decoration: underline; style="font-family: 'Shadows Into Light', cursive;">%s</span></p>
					<p><strong>Genre: </strong><em style="font-family: 'Shadows Into Light', cursive;">%s</em>
					<p><strong>Country: </strong><span style="font-family: 'Shadows Into Light', cursive;">%s</span></p>
					<p><strong> Year:</strong><span style="font-family: 'Shadows Into Light', cursive;"><em> %s</em></span></p>
					<hr>
					<div id='descriptive text'>
						<p><strong>Sypnosis</strong></p>
						<p style="font-family: 'Shadows Into Light', cursive;">%s</p>
						<p><strong>Focus / MUBI Take</strong></p>
						<p style="font-family: 'Shadows Into Light', cursive;">%s</p>
					</div>
				</div>
			</body>
		</div>
	</html>
	""" % (info[1], info[0], info[2], info[7], info[3], info[4], info[5], info[6])
	return content