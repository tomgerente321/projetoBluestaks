from abc import ABC, abstractmethod
import configparser
import os
from dotenv import load_dotenv
load_dotenv()

class Paths:
    """Gerencia caminhos relativos a um diretório base."""

    def __init__(self, base_path):
        """Inicializa a instância com o diretório base."""
        self.base_path = base_path

    def get_path(self, path):
        """Retorna o caminho absoluto a partir de um caminho relativo."""
        return os.path.join(self.base_path, path)

class PathFinder(ABC):
    """Classe abstrata para buscar caminhos a partir de um nome."""

    @abstractmethod
    def get_path_by_name(self, section_name, path_name):
        """Retorna o caminho correspondente ao nome dado."""

    @abstractmethod
    def get_value_by_name(self, section_name, path_name):
        """Retorna o valor correspondente ao nome dado."""

class ConfigPathFinder(PathFinder):
    """Busca caminhos a partir de um arquivo INI de configuração."""

    def __init__(self, config_path=os.path.dirname(os.path.abspath(__file__)) + '/../' + os.getenv('SETTINGS_PATH')):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.paths = Paths(os.path.dirname(config_path))

    def get_path_by_name(self, section, path_name):
        try:
            path = self.config.get(section, path_name)
            return self.paths.get_path(path)
        except configparser.NoOptionError:
            raise ValueError('Path not found: {}'.format(path_name))
        
    def get_value_by_name(self, section, path_name):
        value = self.config.get(section, path_name)
        return value

