import random, subprocess, time
from app_image.AppImage import AppImage
from paths import ConfigPathFinder
from random_username.generate import generate_username
from instagram.EmailValidator import EmailValidator
from instagram.UsernameChecker import UsernameChecker
from instagram.SaveUser import SaveUser
from instagram.UserProfile import UserProfile
from instagram.CreateUser import CreateUser

class DefaultSignUp:
    def __init__(self, adb_host) -> None:
        self.path_finder = ConfigPathFinder()
        self.adb_host = adb_host
        self.screenshots_path = self.path_finder.get_path_by_name('general', 'screenshots_path')
        self.users_path = self.path_finder.get_path_by_name('instagram', 'users_path')
        self.mail_provider = self.path_finder.get_value_by_name('mail', 'mail_provider')
        self.appImage = AppImage(self.adb_host, self.screenshots_path)
        self.usernameChecker = UsernameChecker()
        self.userCreate = CreateUser(self.adb_host)
        self.step = 1
        self.count_feedback = 0
        self.new_user_credentials = {}
        self.add_profile_photos_possibilites = 'up'


    def execute(self):
        self.start_register()

    def start_register(self):
        print('========= Starting Register =========')
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 459 854']
        subprocess.run(adb_command, check=True) #clicar no botão cadastrar-se
        time.sleep(2)
        print('========= Selecting E-mail Option =========')
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 675 195']
        subprocess.run(adb_command, check=True) #ir para aba e-mail
        time.sleep(2)
        self.new_user_credentials = self.userCreate.gerenate_new_user()
        time.sleep(2)
        self._register_new_user_with_email()
        self._set_full_name_from_new_user()
        self._set_password_from_new_user()
        self._set_date_of_birthday_from_new_user()
        self._set_username_from_new_user()
        saveUser = SaveUser(self.new_user_credentials)
        saveUser.pre_save_new_user()
        self._validate_new_user_credentials()
        self.appImage.take_screenshot('validate_user_from_welcome')
        time.sleep(3)
        action = self.appImage.get_app_action_from_image('validate_user_from_welcome', (30, 55, 870, 1090))
        print("========= Setting Way Decision from ActionText  =========")
        self._set_way_decision_from_action(action, 'validate_user_from_welcome')
       
    
    def _register_new_user_with_email(self):
        emailValidator = EmailValidator(self.adb_host, self.mail_provider)
        emailValidator.generate_user_email()
    
    def _set_full_name_from_new_user(self):
        print("========= Setting Fullname  =========")
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 330 190 350 190 300']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        full_name = f"{self.new_user_credentials['first_name']} {self.new_user_credentials['last_name']}".replace(" ", "%s")
        adb_command = ['adb', '-s', self.adb_host, 'shell', f"input text {full_name}"]
        subprocess.run(adb_command, shell=True)

    def _set_password_from_new_user(self):
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 890 300 880 300 300']
        subprocess.run(adb_command, check=True)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 230 305']
        subprocess.run(adb_command, check=True)
        print("========= Setting Password  =========")
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input text ' + self.new_user_credentials['password']]
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 450 555']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
    
    def _set_date_of_birthday_from_new_user(self):
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input tap 445 1560'])
        time.sleep(2)
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input tap 445 888'])
        time.sleep(2)
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input tap 445 1560'])
        time.sleep(2)
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input tap 360 290'])
        rand_age = random.randint(18, 29)
        subprocess.run(['adb', '-s', self.adb_host, 'shell', f"input text {str(rand_age)}"])
        time.sleep(1)
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input tap 450 383'])
        time.sleep(3)
    
    def _set_username_from_new_user(self):
        print("========= Setting Username  =========")
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 450 1560']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 860 245']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 270 250']
        subprocess.run(adb_command, check=True)
        payload = {
            'username': self.new_user_credentials['username'],
            'email': self.new_user_credentials['email'],
            'first_name': self.new_user_credentials['first_name']
        }
        print("========= Checking Username  =========")
        username = self.usernameChecker.check(payload)
        time.sleep(2)
        self.new_user_credentials['username'] = username
        print(self.new_user_credentials['username'])
        time.sleep(5)
        for char in self.new_user_credentials['username']:
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input text ' + str(char)]
            subprocess.run(adb_command, check=True)
            time.sleep(0.5)
        time.sleep(3)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 445 450']
        subprocess.run(adb_command, check=True)
        time.sleep(5)
    
    def _validate_new_user_credentials(self):
        print('========= Validating New User Please Wait... =========')
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 450 488']
        subprocess.run(adb_command, shell=True)
        time.sleep(20)
        print('========= Finished =========')
    
    def _complete_sign_up(self):
        if self.step == 1:
            emailValidator = EmailValidator(self.adb_host, self.mail_provider)
            emailValidator.generate_user_email()
        else:
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 458 776']
            subprocess.run(adb_command, check=True)
        print("========= Validating User Please Wait =========")
        time.sleep(15)
        self.appImage.take_screenshot('validate_user_from_welcome')
        time.sleep(1.5)
        action = self.appImage.get_app_action_from_image('validate_user_from_welcome', (30, 55, 870, 1090))
        print("========= Setting Way Decision from ActionText  =========")
        self._set_way_decision_from_action(action, 'validate_user_from_welcome')
    
    def _set_way_decision_from_action(self, action, way, step=1):
        print(action)
        if "error" in action:
            raise Exception("Error On SignUp in Login Button Restarting Process")
        elif "extra" in action and "security" in action and "required" in action:
            raise Exception("User Extra Security Detected Restarting Process")
        elif "add" in action and "profile" in action and "photo" in action and "skip" in action:
            print("========= Add Profile Photo =========")
            self.step += 1
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 450 490']
            subprocess.run(adb_command, check=True)
            time.sleep(3)
            self.appImage.take_screenshot('validate_user_profile_photo_completed')
            time.sleep(3)
            action = self.appImage.get_app_action_from_image('validate_user_profile_photo_completed', (25, 121, 821, 651))
            print("========= Setting Way Decision from ActionText  =========")
            self._set_way_decision_from_action(action, 'validate_user_profile_photo_completed', self.step)
        elif "add" in action and "profile" in action and "photo" in action:
            self.step += 1
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 450 1560']
            subprocess.run(adb_command, check=True)
            time.sleep(3)
            self.appImage.take_screenshot('validate_user_profile_photo_completed')
            time.sleep(3)
            action = self.appImage.get_app_action_from_image('validate_user_profile_photo_completed', (25, 121, 821, 651))
            self._set_way_decision_from_action(action, 'validate_user_profile_photo_completed', self.step)           
        elif "welcome" in action and "follow" in action and "people" in action and "start" in action:
            self.userProfile = UserProfile(self.adb_host, step)
            self.userProfile.profile()
            self.appImage.take_screenshot('new_user_from_profile_' + str(self.step))
            action = self.appImage.get_app_action_from_image('new_user_from_profile_' + str(self.step), (5, 45, 853, 1191))
            print("========= Setting Way Decision from ActionText  =========")
            self._set_way_decision_from_action(action, 'validate_user_from_profile')
        elif "welcome" in action and "to" in action and "instagram" in action and "add" in action and ("feedbacklrequired" not in action or "feedbackrequired" not in action or "feedback" not in action or "required" not in action or "failed" not in action or "form" not in action or "validation" not in action):
            print("========= User Pre-Registered With Sucessfull =========")
            time.sleep(5)
            self._complete_sign_up()
        elif "feedbacklrequired" in action or "feedbackrequired" in action or "feedback" in action or "required" in action or "failed" in action or "form" in action or "validation" in action:
            raise Exception("Error for complete register Restarting Process")
        else:
            raise Exception("No Action Found Restarting Process")
