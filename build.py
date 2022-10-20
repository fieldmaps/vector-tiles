import subprocess
import shutil
import json
from pathlib import Path

styles = ['osm-liberty', 'basic', 'bright', 'dark-matter', 'positron']

if __name__ == '__main__':
    Path('config/styles').mkdir(parents=True, exist_ok=True)
    shutil.copy('styles/config.json', 'config/config.json')
    for style in styles:
        Path(f'config/styles/{style}').mkdir(parents=True, exist_ok=True)
        with open(f'styles/{style}/style.json') as f:
            data = json.load(f)
        with open(f'config/styles/{style}/style.json', 'w') as f:
            json.dump(data, f, separators=(',', ':'))
        subprocess.run(['spreet', '--minify-index-file',
                       f'styles/{style}/icons', f'config/styles/{style}/sprite'])
        subprocess.run(['spreet', '--minify-index-file', '--retina',
                       f'styles/{style}/icons', f'config/styles/{style}/sprite@2x'])
