import random, subprocess, time
from app_image.AppImage import AppImage
from paths import ConfigPathFinder
from instagram.EmailValidator import EmailValidator
from instagram.UsernameChecker import UsernameChecker
from instagram.UserProfile import UserProfile

class SignupWithLogin:
    user_registred_credentials = {
        'username': None,
        'password': None
    }
    def __init__(self, adb_host) -> None:
        self.path_finder = ConfigPathFinder()
        self.adb_host = adb_host
        self.screenshots_path = self.path_finder.get_path_by_name('general', 'screenshots_path')
        self.users_path = self.path_finder.get_path_by_name('instagram', 'users_path')
        self.mail_provider = self.path_finder.get_value_by_name('mail', 'mail_provider')
        self.appImage = AppImage(self.adb_host, self.screenshots_path)
        self.usernameChecker = UsernameChecker()
        self.step = 2
        self.count_feedback = 0

    def execute(self):
        self._signup_from_login()

    def _get_login_from_users(self):
        with open(f'{self.users_path}/sign_up_users.txt', 'r') as file:
            lines = file.readlines()
        line = random.choice(lines)
        username, password = line.strip().split(' ')
        self.user_registred_credentials['username'] = username
        self.user_registred_credentials['password'] = password
        return self.user_registred_credentials
    
    def _remove_user_from_signup_list(self):
        with open(f'{self.users_path}/sign_up_users.txt', 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if self.user_registred_credentials['username'] in line and self.user_registred_credentials['password'] in line:
                del lines[i]
                break
        with open(f'{self.users_path}/sign_up_users.txt', 'w') as file:
            file.writelines(lines)

    def _dump_pre_registred_user(self):
        with open(f'{self.users_path}/pre_register_user.txt', 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if len(line):
                del lines[i]
                break
        with open(f'{self.users_path}/pre_register_user.txt', 'w') as file:
            file.writelines(lines)

    def _signup_from_login(self):
        login = self._get_login_from_users()
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 447 924']
        subprocess.run(adb_command, check=True)
        time.sleep(5)
        self._login(login)
        time.sleep(5)
        self._submit_login()
        self.appImage.take_screenshot('register_on_login_button_step')
        time.sleep(3)
        print("========= Getting App Action From Image  =========")
        action = self.appImage.get_app_action_from_image('register_on_login_button_step', (162, 685, 752, 958))
        print("========= Setting Way Decision from ActionText  =========")
        self._set_way_decision_from_action(action, 'sign_up_on_login_button')

    def _login(self, login: str):
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 854 416 840 416 300']
        subprocess.run(adb_command, check=True)
        time.sleep(2.5)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 80 391']
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input text ' + login['password']]
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 80 290']
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input text ' + login['username']]
        subprocess.run(adb_command, check=True)

    
    def _submit_login(self):
        print("========= Loging into User  =========")
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 440 474']
        subprocess.run(adb_command, check=True)
        time.sleep(10)
    
    def _new_user_register(self):
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 450 919']
        subprocess.run(adb_command, check=True)
        time.sleep(5)
        print("========= Success on Login  =========")
        self.appImage.take_screenshot('instagram_feed')
        time.sleep(3)
        action = self.appImage.get_app_action_from_image('instagram_feed', (5, 45, 610, 310))
        print("========= Setting Way Decision from ActionText  =========")
        self._set_way_decision_from_action(action, 'register_new_user_instagram_feed')
    
    def _complete_sign_up(self):
        if self.step == 2:
            self._register_user_with_email()
        elif self.step > 2:
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 458 776 456 776 300']
            subprocess.run(adb_command, check=True)
            time.sleep(1.5)
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 458 776']
            subprocess.run(adb_command, check=True)
        print("========= Validating User Please Wait =========")
        time.sleep(20)
        self.appImage.take_screenshot('validate_user_from_welcome')
        time.sleep(3)
        action = self.appImage.get_app_action_from_image('validate_user_from_welcome', (30, 55, 870, 1090))
        print("========= Setting Way Decision from ActionText  =========")
        self._set_way_decision_from_action(action, 'validate_user_from_welcome')
    
    def _register_user_with_email(self):
        emailValidator = EmailValidator(self.adb_host, self.mail_provider)
        emailValidator.generate_user_email()

    def _manage_feedback(self, step):
        self.count_feedback += 1
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input keyevent KEYCODE_BACK']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input keyevent KEYCODE_BACK']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input keyevent KEYCODE_BACK']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 852 247']
        subprocess.run(adb_command, check=True)
        time.sleep(2)
        print(f"========= New Attempt For Create New User After Feedback ({str(self.count_feedback)}) =========")
        self.userProfile = UserProfile(self.adb_host, step)
        self.userProfile.create_new_user_from_profile()
        if(self.count_feedback > 3):
            raise Exception("Error for complete register Restarting Process")

    def _set_way_decision_from_action(self, action, way, step=1):
        print(action)
        if "error" in action:
            self._dump_pre_registred_user()
            if way == 'sign_up_on_login_button':
                raise Exception("Error On SignUp in Login Button Restarting Process")
            elif way == 'register_new_user_instagram_feed':
                raise Exception("Error On SignUp From Instagram Feed Restarting Process")
            elif way == 'validate_user_from_profile' or way == 'validate_user_from_welcome':
                raise Exception("Error On SignUp in Profile User Restarting Process")
        elif "remember" in action: 
            self._new_user_register()
        elif ("your" in action and "story" in action) or ("welcome" in action and "to" in action and "instagram" in action and "follow" in action and "people" in action):
            if way == 'register_new_user_instagram_feed':
                self.userProfile = UserProfile(self.adb_host, self.step, 'SKIP_SAVE_USER')
                self.userProfile.profile()
            else:
                self.userProfile = UserProfile(self.adb_host, self.step)
                self.userProfile.profile()
            self.appImage.take_screenshot('new_user_from_profile_' + str(self.step))
            action = self.appImage.get_app_action_from_image('new_user_from_profile_' + str(self.step), (5, 45, 853, 1191))
            print("========= Setting Way Decision from ActionText  =========")
            self._set_way_decision_from_action(action, 'validate_user_from_profile')
        elif ("welcome" in action and "to" in action and "instagram" in action and "add" in action) and ("feedbacklrequired" not in action or "feedback" not in action or "required" not in action) and ("failed" not in action or "form" not in action or "validation" not in action):
            print("========= User Pre-Registered With Sucessfull =========")
            time.sleep(2)
            self._complete_sign_up()
        elif "extra" in action and "security" in action and "required" in action:
            self._remove_user_from_signup_list()
            self._dump_pre_registred_user()
            raise Exception("User Extra Security Detected Restarting Process")
        elif "add" in action and "profile" in action and "photo" in action and "skip" in action:
            print("========= Add Profile Photo =========")
            self.step += 1
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 450 490 448 490 300']
            subprocess.run(adb_command, check=True)
            time.sleep(3)
            self.appImage.take_screenshot('validate_user_profile_photo_completed')
            time.sleep(1.5)
            action = self.appImage.get_app_action_from_image('validate_user_profile_photo_completed', (25, 121, 821, 651))
            print("========= Setting Way Decision from ActionText  =========")
            self._set_way_decision_from_action(action, 'validate_user_profile_photo_completed', self.step)
        elif "add" in action and "profile" in action and "photo" in action:
            self.step += 1
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 450 1560 448 1560 300']
            subprocess.run(adb_command, check=True)
            time.sleep(3)
            self.appImage.take_screenshot('validate_user_profile_photo_completed')
            time.sleep(1.5)
            action = self.appImage.get_app_action_from_image('validate_user_profile_photo_completed', (25, 121, 821, 651))
            self._set_way_decision_from_action(action, 'validate_user_profile_photo_completed', self.step)           
        elif "or" in action and "have" in action and "sign" in action:
            self._dump_pre_registred_user()
            raise Exception("Error On Login Restarting Process")
        elif "feedbackrequired" in action or "feedbacklrequired" in action or "feedback" in action or "required" in action:
            raise Exception("Error for complete register Restarting Process")
        else:
            self._dump_pre_registred_user()
            raise Exception("No Action Found Restarting Process")

