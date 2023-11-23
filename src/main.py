from emulator.Bluestacks import BluestacksInstance
import time
import psutil

class Main:
    def __init__(self) -> None:
        self.bluestacks = BluestacksInstance()

    def startBot(self):
        while True:
            try:
                if self.check_program_running('Bluestacks.exe'):
                    raise Exception("Bluestacks is Already Running canceling operation. Please Restart your computer or Reinstall your Bluestacks if that happening again")
                self.bluestacks.execute()
            except Exception as e:
                print('========= An Error ocorred  =========')
                print(f"{e.__traceback__}: {e}")
                self.bluestacks.stopInstance()
                time.sleep(5)

    def check_program_running(self, program_name):
        for process in psutil.process_iter(['name']):
            if process.info['name'] == program_name:
                return True
        return False
    

main = Main()
main.startBot()