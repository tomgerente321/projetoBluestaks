from onesecmail import OneSecMail
from onesecmail.validators import FromAddressValidator

class OneSecMailAdapter:
    mail_box: OneSecMail = None

    def __init__(self) -> None:
        self.mail_box: OneSecMail = OneSecMail.get_random_mailbox()

    def getEmailAddress(self):
        return self.mail_box.address
    
    def getMessages(self):
        return self.mail_box.get_messages()
    
    def getMessagesFromEMailAddress(self, email_address):
        from_validator = FromAddressValidator(email_address)
        inbox = self.mail_box.get_messages(validators=[from_validator])
        return inbox[0] if inbox else None
    
    #TODO: TRATAR OS CODIGOS PARA O INSTAGRAM

# onesecmail_adapter = OneSecMailAdapter()
# email_address = onesecmail_adapter.getEmailAddress()
# print(email_address)
# while True:
#     inbox = onesecmail_adapter.getMessagesFromEMailAddress('matheusduarte.developer@gmail.com')
#     if(len(inbox)):
#         print(inbox[0].subject)
#     time.sleep(5)
    


