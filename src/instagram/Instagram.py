import subprocess
import time
from instagram.WayFactory import WayFactory
from paths import ConfigPathFinder
from app_image.AppImage import AppImage

class InstagramApp:
    def __init__(self, adb_config) -> None:
        self.path_finder = ConfigPathFinder()
        self.adb_config = adb_config
        self.adb_host = self._get_agb_config()
        self.screenshots_path = self.path_finder.get_path_by_name('general', 'screenshots_path')
        self.wayFactory = WayFactory()
        self.appImage = AppImage(self.adb_host, self.screenshots_path)

    def start(self):
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'am start -n com.instagram.lite/com.facebook.lite.MainActivity']
        subprocess.run(adb_command, check=True)
    
    def startRegister(self):
        print("========= Checking create account button has disabled  =========")
        self.appImage.take_screenshot('create_account_button')
        time.sleep(3)
        button_color = self.appImage.get_image_color('create_account_button', (97, 817, 205, 865))
        if button_color == '178 223 252 255' or button_color == '128 128 128 255':
            raise Exception("Failed to create account, restarting bot for trying again =(")
        else:
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 445 841']
            subprocess.run(adb_command, check=True)
            time.sleep(2)
            self.appImage.take_screenshot('1st_register_step')
            time.sleep(3)
            print("========= Getting App Action From Image  =========")
            action = self.appImage.get_app_action_from_image('1st_register_step', (205, 735, 680, 830))
            print("========= Setting Way Decision from ActionText  =========")
        self._set_way_decision_from_action(action, 'sign_up_button')

    def _set_way_decision_from_action(self, action, step):
        if "error" in action:
            if step == 'sign_up_button':
                print("========= Error On SignUp Button Trying SignupWithLogin =========")
                adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 454 875']
                subprocess.run(adb_command, check=True)
                way = self.wayFactory.set_way('signupWithLogin', self.adb_host)
                way.execute()
        else:
            print("========= Success On SignUp Button Going to DefaultSignUp =========")
            way = self.wayFactory.set_way('defaultSignUp', self.adb_host)
            way.execute()

    def _get_agb_config(self) -> str:
        return f"{self.adb_config['hostname']}:{str(self.adb_config['port'])}"





