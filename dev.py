import subprocess
from pathlib import Path

cwd = Path(__file__).parent

if __name__ == '__main__':
    subprocess.run(['python3', cwd / 'build.py'])
    subprocess.run(['tileserver-gl-light', '--config',
                   cwd / 'dist/config.json'])
