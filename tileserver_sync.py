import subprocess
from pathlib import Path

cwd = Path(__file__).parent

if __name__ == '__main__':
    subprocess.run([
        'ansible-playbook',
        cwd / 'tileserver/playbook-sync.yml',
        '-i', cwd / 'tileserver/inventory.ini'
    ])
