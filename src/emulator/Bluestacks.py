import subprocess
import time
import os

def encontrar_executavel_hd_manager(caminho_bluestacks):
    hd_manager_executavel = os.path.join(caminho_bluestacks, 'HD-MultiInstanceManager.exe')
    
    if os.path.isfile(hd_manager_executavel):
        return hd_manager_executavel
    else:
        return None

def contar_instancias_em_execucao():
    # Comando para listar os processos relacionados ao BlueStacks
    comando_listar_processos = ['tasklist', '/FI', 'IMAGENAME eq HD-MultiInstanceManager.exe']
    resultado = subprocess.run(comando_listar_processos, capture_output=True, text=True)
    
    # Conta o número de instâncias em execução
    instancias_em_execucao = resultado.stdout.count('HD-MultiInstanceManager.exe')
    return instancias_em_execucao

def executar_hd_multi_instance_manager(caminho_bluestacks):
    caminho_hd_manager = encontrar_executavel_hd_manager(caminho_bluestacks)

    if caminho_hd_manager is None:
        print("Erro: O executável HD-MultiInstanceManager.exe não foi encontrado.")
        return False

    try:
        # Verifica o número de instâncias do HD-MultiInstanceManager em execução
        instancias_em_execucao = contar_instancias_em_execucao()
        
        if instancias_em_execucao > 0:
            print("O HD-MultiInstanceManager já está em execução.")
            return False

        # Comando para executar o HD-MultiInstanceManager
        comando_executar = [caminho_hd_manager]
        subprocess.Popen(comando_executar, cwd=caminho_bluestacks)
        
        # Aguarda alguns segundos para garantir que o HD-MultiInstanceManager seja iniciado
        time.sleep(10)  # Ajuste o tempo conforme necessário
        
        print("HD-MultiInstanceManager foi executado.")
        return True
    except Exception as e:
        print(f"Erro ao executar o HD-MultiInstanceManager: {e}")
        return False

# Substitua 'c:\Program Files\BlueStacks_nxt' pelo caminho real para o diretório do BlueStacks em seu sistema
caminho_bluestacks = r'c:\Program Files\BlueStacks_nxt'

# Executa o HD-MultiInstanceManager se ainda não estiver em execução
executar_hd_multi_instance_manager(caminho_bluestacks)
