import random
from mail.OneSecMailAdapter import OneSecMailAdapter
from mail.MailTMAdapter import MailTMAdapter
from mail.MailoAdapter import MailoAdapter

class MailFactory:
    def __init__(self, provider=None):
        self.provider = provider or random.choice(['OneSecMailAdapter', 'MailTMAdapter'])
    
    def create_adapter(self):
        print(self.provider)
        if self.provider == 'OneSecMailAdapter':
            return OneSecMailAdapter()
        elif self.provider == 'MailTMAdapter':
            return MailTMAdapter()
        elif self.provider == 'MailoAdapter':
            return MailoAdapter()
        else:
            raise ValueError('Invalid provider specified')