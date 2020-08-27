# import the smtplib module. It should be included in Python by default
import smtplib
# set up the SMTP server
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from private.keys import FLASK_MAIL_PASSWORD

MY_ADDRESS = 'eri_portal@eprojecttrackers.com'


def send_eri_mail(recipient, message_, subject="This is TEST", message_type='html'):
    msg = MIMEMultipart()  # create a message
    # setup the parameters of the message
    # msg['From'] = MY_ADDRESS
    msg['From'] = str(Header(f'algo102 scripts <{MY_ADDRESS}>'))
    msg['To'] = recipient
    msg['Subject'] = subject
    # add in the message body
    msg.attach(MIMEText(message_, message_type))
    # send
    with smtplib.SMTP_SSL(host='mail.eprojecttrackers.com', port=465) as s:
        s.login(MY_ADDRESS, FLASK_MAIL_PASSWORD)
        s.send_message(msg, MY_ADDRESS, recipient)


if __name__ == '__main__':

    message = """
        <table style="width:100%">
          <tr>
            <th>Firstname</th>
            <th>Lastname</th>
            <th>Age</th>
          </tr>
          <tr>
            <td>Jill</td>
            <td>Smith</td>
            <td>50</td>
          </tr>
          <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
          </tr>
        </table>
        """

    send_eri_mail('phanveehuen@gmail.com', message)
