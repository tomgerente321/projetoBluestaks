import os
import random
import subprocess
import time
import re
import datetime

from faker import Faker
fake = Faker('pt_BR')

file_path = './routines/mail_settings.txt'
file_path_users = './users/users.txt'

with open('./routines/instance_number.txt', 'r') as file:
    count_instances = int(file.read())

dir_path = "./screenshots/"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

def init():
    if os.path.exists("C:\ProgramData\BlueStacks_bgp64_hyperv\Logs\Player.log"):
        # Delete the file
        os.remove("C:\ProgramData\BlueStacks_bgp64_hyperv\Logs\Player.log")
    global count_instances
    count_instances += 1
    with open('./routines/instance_number.txt', 'w') as file:
        file.write(str(count_instances))
    #create_instance
    command_create_instance = r'"C:\Program Files\BlueStacks_bgp64_hyperv\HD-VmManager.exe" createinstance clone Android_'+str(count_instances)+' Android {"cpu":2,"ram":2048,"dpi":"240","abi":15,"resolutionwidth":1600,"resolutionheight":900}'
    subprocess.run(command_create_instance, shell=True)
    time.sleep(5)
    #execute_instance
    command_execute_instance = r'"C:\Program Files\BlueStacks_bgp64_hyperv\Bluestacks.exe" -vmname Android_'+str(count_instances)+''
    process_instance_execute = subprocess.Popen(command_execute_instance, shell=True)
    print('pid instance: ' + str(process_instance_execute.pid))
    time.sleep(5)
    print('========= Scanning Bluestacks adbport =========')
    with open("C:\ProgramData\BlueStacks_bgp64_hyperv\Logs\Player.log") as f:
        data = f.read()
        match = re.search(r"INFO: 5555 --> (\d{5})", data)
        if match:
            adb_port = match.group(1)
    time.sleep(2)
    if os.path.exists("C:\ProgramData\BlueStacks_bgp64_hyperv\Logs\Player.log"):
        # Delete the file
        os.remove("C:\ProgramData\BlueStacks_bgp64_hyperv\Logs\Player.log")
    print('========= Starting Bluestacks instance =========')
    initBluestacks(adb_port, process_instance_execute)

def initBluestacks(adb_port, process_instance_execute):
    print('adb_port: ' + adb_port)
    subprocess.run(['adb', 'kill-server'])
    subprocess.run(['adb', 'start-server'])
    time.sleep(5)
    connectInstace(adb_port, process_instance_execute)

def connectInstace(adb_port, process_instance_execute):
    subprocess.run(['adb', 'connect', 'localhost:'+str(adb_port)+''])
    time.sleep(2)
    print('========= Installing apks =========')
    installApks(adb_port)
    startInstaApp(adb_port, process_instance_execute)

def installApks(adb_port):
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'install', './apks/LITE[LeyoutModerno]-281.0.0.13.111.apk'])
    

    

def startInstaApp(adb_port, process_instance_execute):
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'am start -n com.instagram.lite/com.facebook.lite.MainActivity'])
    process = subprocess.Popen(['python', 'tempmail.py'])
    time.sleep(10)
    print(r'========= Waiting app initiazation =========')
    startRegister(process, adb_port, process_instance_execute)

def startRegister(process, adb_port, process_instance_execute):
    print(r'========= Starting register =========')
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 459 854']) #clicar no botão cadastrar-se
    time.sleep(2)

    print(r'========= Selecting e-mail option =========')
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 675 195']) #ir para aba e-mail
    time.sleep(2)

    print(r'========= Writing e-mail =========')
    with open(file_path, 'r') as file:
        file_content = file.read()
        email_address = file_content
        subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', r"input text " + email_address])

    print(r'========= Sending code confirmation, check your inbox and wait 15 seconds =========')
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 450 400'])
    time.sleep(15)

    with open(file_path, 'r') as file:
        file_content = file.read()
        if(len(file_content.split()) > 1):
            instagram_code = file_content.split()[1]
            print(r'========= Writing code confirmation =========')
            time.sleep(2)
            subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', r"input text " + instagram_code])
    # Check if the file exists before deleting it
    print(r'========= Deleting temp mail settings =========')
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")
    #STOP Temp Mail Service    
    process.kill()
    time.sleep(5)

    print(r'========= Validating Email =========')
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 450 360'])
    time.sleep(5)

    print(r'========= Writing full name and password =========')
    user_profile = fake.simple_profile()
    full_name = user_profile["name"].replace(" ", "%s")
    time.sleep(2)
    username = user_profile["username"].replace("-", "_") + str(random.randint(1, 9999))
    time.sleep(2)
    password = fake.pystr()
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 330 190'])
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', r"input text " + full_name])
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 330 290'])
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', r"input text " + password])
    time.sleep(2)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 450 550'])
    time.sleep(2)

    print(r'========= Setting date of birthday =========')
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 445 1560'])
    time.sleep(2)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 445 888'])
    time.sleep(2)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 445 1560'])
    time.sleep(2)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 360 290'])
    rand_age = random.randint(18, 59)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', r"input text " + str(rand_age)])
    time.sleep(1)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 450 383'])
    time.sleep(3)

    print(r'========= Setting username =========')
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 450 1560'])
    time.sleep(2)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 860 245'])
    time.sleep(2)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 270 250'])
    time.sleep(3)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', r"input text " + username])
    time.sleep(2)
    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 445 450'])
    print(r'========= Saving username and password, please wait... =========')
    with open(file_path_users, 'a') as file:
            file.write(username + ' ' + password + '\n')
    time.sleep(30)

    subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 450 488'])
    time.sleep(2)
    print(r'========= Finished =========')
    #TODO
    # print(r'========= Setting profile photo... =========')
    # subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 550 415'])
    # time.sleep(2)
    # subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 360 1565'])
    # time.sleep(3)
    # subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 460 1535'])
    # time.sleep(1)
    # subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 787 869']) #allow gallery
    # time.sleep(2)
    # subprocess.run(['adb', '-s', 'localhost:'+str(adb_port)+'', 'shell', 'input tap 451 1535'])
    # time.sleep(3)

    # Define o nome do arquivo com a data e hora atual concatenada
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    # Captura a captura de tela e salva no diretório de destino com o nome do arquivo definido
    subprocess.run(["adb", '-s', 'localhost:'+str(adb_port)+'', "shell", "screencap", "-p", "/sdcard/screen.png"])
    subprocess.run(["adb",  '-s', 'localhost:'+str(adb_port)+'', "pull", "/sdcard/screen.png", os.path.join(dir_path, file_name)])

    subprocess.run(["taskkill", "/F", "/IM", "Bluestacks.exe"], shell=True)

    time.sleep(3)
    print(r'========= Restarting Process =========')
    init()
init()