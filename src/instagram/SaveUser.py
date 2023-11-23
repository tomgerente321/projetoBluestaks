import time
from paths import ConfigPathFinder


class SaveUser:
    def __init__(self, new_user_credentials = {}) -> None:
        self.path_finder = ConfigPathFinder()
        self.users_path = self.path_finder.get_path_by_name('instagram', 'users_path')
        self.new_user_credentials = new_user_credentials

    def save_new_user(self, step):
        if not self.new_user_credentials['username'] == None and not self.new_user_credentials['password'] == None:
            print(f"========= Saving User =========")
            with open(f'{self.users_path}/users.txt', 'a') as file:
                file.write(f"{self.new_user_credentials['username']} {self.new_user_credentials['password']}" + '\n')
            time.sleep(2)
            if step <= 3:
                with open(f'{self.users_path}/sign_up_users.txt', 'a') as file:
                    file.write(f"{self.new_user_credentials['username']} {self.new_user_credentials['password']}" + '\n')
            self.new_user_credentials = {}
            print(f"========= Success on process creating next user: {step} =========")
        else: 
            raise Exception(f"Failed to save user: {self.new_user_credentials}")
    
    def pre_save_new_user(self):
        with open(f'{self.users_path}/pre_register_user.txt', 'w') as file:
            file.write(f"{self.new_user_credentials['username']} {self.new_user_credentials['password']}" + '\n')
    
    def get_last_user_pre_saved(self):
        with open(f'{self.users_path}/pre_register_user.txt', 'r') as file:
            return file.read()