"""
The really trivial trigger: just prints debug output to the log.
"""

import smtplib

SMTPSERVER='mail.openbase.co.kr'
SMTPAUTH=0
SMTPUSER='hwlee@openbase.co.kr'
SMTPPASSWD='12dlgusdnr@@'
SMTPRECIPIENTS= [ 'hwlee@openbase.co.kr' ]
SMTPSENDER = 'hwlee@openbase.co.kr'

class Trigger(HostTrigger):
    def sendemail(self, msg):
        session = smtplib.SMTP(SMTPSERVER)
        if SMTPAUTH:
            session.login(SMTPUSER, SMTPPASSWD)
            
        msg = "From: %s\r\nTo: %s\r\nSubject: Host Trigger Alert for %s\r\n\r\n%s" % (SMTPSENDER, ",".join(SMTPRECIPIENTS), self.ip, msg)

        smtpresult = session.sendmail(SMTPSENDER, SMTPRECIPIENTS, msg)
        session.quit()

        if smtpresult:
            errstr = ""
            for recip in smtpresult.keys():
                print "Could not deliver mail to: %s"
                errstr = """Could not delivery mail to: %s

Server said: %s
%s

%s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
            raise smtplib.SMTPException, errstr
        return

    def trigger(self):
        self.sendemail("""%s matched trigger:
                       Bytes: %s
                       Speed: %s
                       Bytes (fwd): %s
                       Speed (fwd): %s
                       Connections: %s
                       CPS: %s
                       Connection Prot: %s
        return

    def reset(self):
        self.sendemail("% ip matched trigger Outbound Traffic 20Mbps Over" % self.ip)
        return

