import subprocess, time
from app_image.AppImage import AppImage
from paths import ConfigPathFinder
from instagram.CreateUser import CreateUser
from instagram.SaveUser import SaveUser

class UserProfile:
    def __init__(self, adb_host, step, flag = None) -> None:
        self.adb_host = adb_host
        self.step = step
        self.path_finder = ConfigPathFinder()
        self.screenshots_path = self.path_finder.get_path_by_name('general', 'screenshots_path')
        self.appImage = AppImage(self.adb_host, self.screenshots_path)
        self.createUser = CreateUser(self.adb_host)
        self.flag = flag

    def profile(self):
        print("========= Checking Last Pre Saved User  =========")
        if self.flag is None:
            saveUser = SaveUser()
            current_new_user = saveUser.get_last_user_pre_saved()
            print(current_new_user)
            self.save_new_current_user(current_new_user)
        print("========= User Profile  =========")
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input touchscreen swipe 811 1561 811 1562 1500']
        subprocess.run(adb_command, check=True)
        time.sleep(5)
        self.create_new_user_from_profile()
    
    def create_new_user_from_profile(self):
        print("========= Creating New User From Profile  =========")
        print('ACTUAL STEP: ' + str(self.step))
        self.manage_steps_from_create_user(self.step)
        time.sleep(3)
        self.createUser.gerenate_new_user()
        self.createUser.set_username_from_profile()
        self.createUser.set_password_from_profile()
    
    def manage_steps_from_create_user(self, step):
        if (step == 1):
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 840 1556']
            subprocess.run(adb_command, check=True)
        elif (step == 2):
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 840 1465']
            subprocess.run(adb_command, check=True)
            time.sleep(2)
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 320 1530'] #tap create account
            subprocess.run(adb_command, check=True)
        elif (step == 3):
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 840 1375']
            subprocess.run(adb_command, check=True)
            time.sleep(2)
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 320 1530'] #tap create account
            subprocess.run(adb_command, check=True)
        elif (step == 4):
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 840 1265']
            subprocess.run(adb_command, check=True)
            time.sleep(2)
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 320 1530'] #tap create account
            subprocess.run(adb_command, check=True)
        elif (step == 5):
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 840 1175']
            subprocess.run(adb_command, check=True)
            time.sleep(2)
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 320 1530'] #tap create account
            subprocess.run(adb_command, check=True)
        elif (step == 6):
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 840 1100']
            subprocess.run(adb_command, check=True)
            time.sleep(2)
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 320 1530'] #tap create account
            subprocess.run(adb_command, check=True)
        else:
            raise Exception(f"Process Finished on STEP: {self.step} Restarting BOT for Create New Accounts!!!!!")
        
    def save_new_current_user(self, current_new_user):
        if len(current_new_user) > 0:
            _current_new_user = {
                'username': current_new_user.split()[0],
                'password': current_new_user.split()[1]
            }
            saveUser = SaveUser(_current_new_user)
            saveUser.save_new_user(int(self.step))
        else:
            raise Exception("Error while saving user restarting process :(")
