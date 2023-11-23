import subprocess, time, random
from unidecode import unidecode
from instagram.UsernameChecker import UsernameChecker
from faker import Faker
from paths import ConfigPathFinder
from instagram.SaveUser import SaveUser

class CreateUser:
    def __init__(self, adb_host) -> None:
        self.path_finder = ConfigPathFinder()
        self.usernameChecker = UsernameChecker()
        self.fake = Faker('pt_BR')
        self.adb_host = adb_host
        self.count_feedback = 0

    
    def gerenate_new_user(self):
        self.new_user_credentials = {
            'username': self._generate_username(f'{self.fake.unique.first_name_female().lower()}.{self.fake.unique.last_name_female().lower()}'),
            'first_name': self.fake.unique.first_name_female(),
            'last_name': self.fake.unique.last_name_female(),
            'password': self.fake.pystr()
        }
        mail_domain = ['gmail.com', 'outlook.com.br', 'outlook.com', 'hotmail.com', 'hotmail.com.br', 'aol.com', 'yahoo.com']
        self.new_user_credentials['email'] = f"{unidecode(self.new_user_credentials['first_name'])}.{unidecode(self.new_user_credentials['last_name'])}{str(random.randint(1, 2004))}@{random.choice(mail_domain)}".lower()
        return self.new_user_credentials
    
    def _generate_username(self, fullname: str) -> str:
        return f'{unidecode(fullname.replace(" ", "_"))}{unidecode(self._generate_alphanumeric())}'
    
    def _generate_alphanumeric(self) -> str:
        letters = 'abcdefghijklmnopqrstuvwxyz'
        numbers = str(random.randint(1, 9999))
        for i in range(random.randint(1, 2)):
            numbers += random.choice(letters)
        return numbers


    def set_username_from_profile(self):
        print("========= Setting Username  =========")
        payload = {
            'username': self.new_user_credentials['username'],
            'email': self.new_user_credentials['email'],
            'first_name': self.new_user_credentials['first_name']
        }
        print("========= Checking Username  =========")
        username = self.usernameChecker.check(payload)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input text ' + username]
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        print(username)
        self.new_user_credentials['username'] = username
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 380 325']
        subprocess.run(adb_command, check=True)
        time.sleep(5)
    
    def set_password_from_profile(self):
        print("========= Setting Password  =========")
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input text ' + self.new_user_credentials['password']]
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 304 378']
        subprocess.run(adb_command, check=True)
        print(self.new_user_credentials)
        saveUser = SaveUser(self.new_user_credentials)
        saveUser.pre_save_new_user()
        time.sleep(5)