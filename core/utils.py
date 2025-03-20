import subprocess
from sys import platform

def ping(host):
    """
    Ping une machine pour vérifier si elle est en ligne.
    Retourne True si la machine répond, False sinon.
    """
    try:
        # Utiliser la commande ping (Windows ou Linux)
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except Exception as e:
        print(f"Erreur lors du ping : {e}")
        return False