import smtplib


mailserver = smtplib.SMTP('smtp.office365.com',587)
mailserver.ehlo()
mailserver.starttls()
mailserver.login('cnascimento@dermage.com.br', '#')
mailserver.sendmail('cnascimento@dermage.com.br','cesarfnt@gmail.com','\npython email')
mailserver.quit()