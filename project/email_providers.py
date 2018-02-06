import sendgrid
import os
from sendgrid.helpers.mail import *
from sparkpost import SparkPost
from flask import Response

class SparkPostEmail:
    """class object for creating and sending a email through SparkPost"""
    sp = SparkPost('b52095de67842daa5a5a3b1cfd951d9790f6eb02')

    def __init__(self, from_email, to_email_list, cc_email_list=[], bcc_email_list=[], 
        subject="no subject", content="empty body"):

        self.from_email = from_email
        self.to_email_list = to_email_list
        self.cc_email_list = cc_email_list
        self.bcc_email_list = bcc_email_list
        self.subject = subject
        self.content = content

    def send_email(self):
        try:
            res = self.sp.transmissions.send(
                recipients = self.to_email_list,
                cc = self.cc_email_list,
                bcc = self.bcc_email_list,
                text = self.content,
                from_email = self.from_email,
                subject = self.content,
                track_opens=True,
                track_clicks=True
            )
            return Response(json.dumps({'response': res}), mimetype='application/json; charset=utf-8')
        except:
            res = Response(status=400)
            return res


class SendGridEmail:
    """class object for creating and sending a email through SendGrid"""
    sg = sendgrid.SendGridAPIClient(apikey='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')

    def __init__(self, from_email, to_email_list, cc_email_list=[], bcc_email_list=[], 
        subject="no subject", content="empty body"):

        self.from_email = from_email
        # Sendgrid cannot handle duplicate email in multiple lists or listed twice
        self.to_email_list = to_email_list
        self.cc_email_list = cc_email_list
        self.bcc_email_list = bcc_email_list
        self.subject = subject
        # Sendgrid requires one char in the body or will not send
        self.content = content

    def send_email(self):
        mail = Mail()
        personalization = Personalization()
        personalization.subject = self.subject
        for to_addr in self.to_email_list:
            personalization.add_to(Email(to_addr))
        for cc_addr in self.cc_email_list:
            personalization.add_cc(Email(cc_addr))
        for bcc_addr in self.bcc_email_list:
            personalization.add_bcc(Email(bcc_addr))
        mail.from_email = Email(self.from_email)
        mail.subject = self.subject
        mail.add_personalization(personalization)
        mail.add_content(Content("text/plain", self.content))
        try:
            res = self.sg.client.mail.send.post(request_body=mail.get())
            return res
        except:
            res = Response(status=400)
            return res

        email = SendGridEmail(
            from_email='anewtest@nowhere.com',
            to_email_list=['aaron.manley@juno.com'],
            cc_email_list=['aaron.m.manley@gmail.com'],
            bcc_email_list=['ammaney@ucdavis.edu'],
            subject='a stupid subject line',
            content=''
            )