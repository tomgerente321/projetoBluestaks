from mailtm import Email

class MailTMAdapter:
    inbox = None
    def __init__(self) -> None:
        self.mail_box: Email = Email()

    def getEmailAddress(self):
        self.mail_box.register()
        return self.mail_box.address
    
    def start(self):
        self.mail_box.start(self.listener)
        pass

    def stop(self):
        self.mail_box.stop()
    
    def getMessages(self):
        return self.inbox
    
    def getMessageSubject(self):
        return self.inbox.subject
    
    def getMessageText(self):
        return self.inbox.body


    def listener(self, message):
        if(message['subject']):
            self.inbox = Inbox(message['subject'], message['text'])

class Inbox:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
    
    def __repr__(self) -> str:
        return f"<MailTM; subject='{self.subject}', body='{self.body}'>"


