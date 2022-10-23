import subprocess
from pathlib import Path

cwd = Path(__file__).parent

if __name__ == '__main__':
    subprocess.run([
        'ansible-playbook',
        cwd / 'planetiler/playbook.yml',
        '-i', cwd / 'planetiler/inventory.ini'
    ])
