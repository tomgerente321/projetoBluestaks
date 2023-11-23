import subprocess
import time
import random

class ProfilePhoto:
    def __init__(self, adb_host):
        self.adb_host = adb_host
        #self.step = 0

    def add_profile_photo_from_user(self):
        self.step += 1
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 457 1514']
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 454 412']
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 253 1560'] #choose gallery
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        if self.step == 2:
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 320 1530'] #tap continue gallery
            subprocess.run(adb_command, check=True)
            time.sleep(3)
            adb_command = ['adb', '-s', self.adb_host, 'shell', 'input tap 785 868'] #allow gallery
            subprocess.run(adb_command, check=True)
            time.sleep(3)
        print("========= Selecting Photo from Gallery =========")
        start_x, start_y = 115, 530
        num_cols, num_rows = 3, 5
        num_fotos = num_cols * num_rows
        largura_foto, altura_foto = 300, 300
        posicao_foto = random.randint(4, num_fotos)
        coluna_foto = (posicao_foto - 1) % num_cols
        linha_foto = (posicao_foto - 1) // num_cols
        x_foto = start_x + (coluna_foto * largura_foto)
        y_foto = start_y + (linha_foto * altura_foto)
        adb_command = ['adb', '-s', self.adb_host, 'shell', 'input', f'tap {x_foto} {y_foto}']
        subprocess.run(adb_command, check=True)
        time.sleep(3)
        print("========= Validating Photo =========")
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input', 'tap 852 70'])
        time.sleep(10)
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input', 'tap 845 412'])
        time.sleep(2)
        subprocess.run(['adb', '-s', self.adb_host, 'shell', 'input', 'tap 456 514'])
        time.sleep(5)
        self.appImage.take_screenshot('validate_user_profile_photo_completed')
        time.sleep(3)
        action = self.appImage.get_app_action_from_image('validate_user_profile_photo_completed', (25, 121, 821, 651))
        print("========= Setting Way Decision from ActionText  =========")
        self._set_way_decision_from_action(action, 'validate_user_profile_photo_completed', self.step)

    def _set_way_decision_from_action(self, action, screenshot_name, step):
        # Your code for setting way decision goes here
        pass
