from paths import ConfigPathFinder
import subprocess

class OpenVPN:
    def __init__(self) -> None:
        self.path_finder = ConfigPathFinder()
        self.openvpn_file_exec = self.path_finder.get_path_by_name('openvpn', 'vpn_file_exec')

    def connect(self, client: str):
        subprocess.Popen(['cmd', '/c', 'start', self.openvpn_file_exec, client], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def disconnect(self):
        subprocess.run(["taskkill", "/F", "/IM", "openvpn.exe"], shell=True)
        subprocess.run(["taskkill", "/F", "/IM", "cmd.exe"], shell=True)


