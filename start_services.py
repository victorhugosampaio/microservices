import os
import subprocess

def executar_scripts_em_cmd(pasta):
    arquivos_py = [f for f in os.listdir(pasta) if f.endswith("_service.py")]

    for arquivo in arquivos_py:
        caminho_completo = os.path.join(pasta, arquivo)
        subprocess.Popen(f'start cmd /k python "{caminho_completo}"', shell=True)

if __name__ == "__main__":
    pasta = "build"
    executar_scripts_em_cmd(pasta)