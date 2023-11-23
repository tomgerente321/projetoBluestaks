import subprocess, time
from paths import ConfigPathFinder 
from app_image.AppImage import AppImage
from mail.MailTMAdapter import MailTMAdapter
from mail.OneSecMailAdapter import OneSecMailAdapter
from mail.MailFactory import MailFactory

MAX_ATTEMPTS_READ_INBOX_TEMPMAIL = 10
INTAGRAM_MAIL = 'no-reply@mail.instagram.com'

class EmailValidator:
    def __init__(self, adb_host, temp_mail_provider: str):
        self.path_finder = ConfigPathFinder()
        self.adb_host = adb_host
        self.screenshots_path = self.path_finder.get_path_by_name('general', 'screenshots_path')
        self.mailFactory = MailFactory(temp_mail_provider)
        self.temp_mail_adapter = self.mailFactory.create_adapter()
        self.appImage = AppImage(self.adb_host, self.screenshots_path)
        self.mail_box_read_attempts = 0

    def generate_user_email(self):
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 458 841 456 841 300']
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 670 160 673 160 300']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        email_address = self._get_tempmail_address()
        self._set_mail_box_on_input_and_confirm(email_address)
        self._read_inbox()
    
    def _get_tempmail_address(self):
        print("========= Getting Temp Mail Please Wait  =========")
        email_address = self.temp_mail_adapter.getEmailAddress()
        if isinstance(self.temp_mail_adapter, MailTMAdapter):
            self.temp_mail_adapter.start()
        time.sleep(2)
        return email_address

    def _set_mail_box_on_input_and_confirm(self, email_address):
        print(email_address)
        for char in email_address:
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input text ' + str(char)]
            subprocess.run(adb_command, check=True)
            time.sleep(0.5)
        time.sleep(2)
        print("========= Confirming Mail User Please Wait =========")
        subprocess.run(['adb', '-s',  self.adb_host, 'shell', 'input tap 450 365'])
        time.sleep(10)

    def _read_inbox(self):
        while self.mail_box_read_attempts < MAX_ATTEMPTS_READ_INBOX_TEMPMAIL:
            self.mail_box_read_attempts += 1
            if (self.mail_box_read_attempts + 1 > MAX_ATTEMPTS_READ_INBOX_TEMPMAIL):
                raise Exception("Error On Obtain The Instagram Code [1] :( Restarting Proccess")
            print(f"========= Reading MailBox Attempt: [{self.mail_box_read_attempts}/{MAX_ATTEMPTS_READ_INBOX_TEMPMAIL}] =========")
            inbox = self.temp_mail_adapter.getMessagesFromEMailAddress(INTAGRAM_MAIL) if isinstance(self.temp_mail_adapter, OneSecMailAdapter) else self.temp_mail_adapter.getMessages()
            if inbox is not None:
                instagram_code = inbox.subject.split()[0]
                if(len(instagram_code) > 0):
                    print('========= Writing Code Confirmation =========')
                    print(instagram_code)
                    adb_command = ['adb', '-s', self.adb_host, 'shell', f'input text {instagram_code}']
                    subprocess.run(adb_command, check=True)
                    self.mail_box_read_attempts = MAX_ATTEMPTS_READ_INBOX_TEMPMAIL
                    if isinstance(self.temp_mail_adapter, MailTMAdapter):
                        self.temp_mail_adapter.stop()
                    self._validate_mail_user()
                else:
                    raise Exception("Error On Obtain The Instagram Code [2] :( Restarting Proccess")
            time.sleep(10)

    def _validate_mail_user(self):
        print('========= Validating Email Please Wait =========')
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 450 360']
        subprocess.run(adb_command, check=True)
        time.sleep(15)
