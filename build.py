import json
import subprocess
from pathlib import Path

cwd = Path(__file__).parent


def build_config():
    with open('src/config.json') as f:
        data = json.load(f)
    with open(f'dist/config.json', 'w') as f:
        json.dump(data, f, separators=(',', ':'))


def build_style(style):
    with open(cwd / f'src/styles/{style}/style.json') as f:
        data = json.load(f)
    layers = []
    for layer in data['layers']:
        if isinstance(layer, str):
            with open(cwd / f'src/layers/{layer}.json') as f:
                layer = json.load(f)
        if not isinstance(layer, list):
            layer = [layer]
        layers.extend(layer)
    data['layers'] = layers
    variables = data.get('metadata', {}).get('variables')
    datas = json.dumps(data, separators=(',', ':'))
    if variables:
        for key in variables:
            datas = datas.replace(f'"{{{key}}}"', json.dumps(variables[key]))
    with open(cwd / f'dist/styles/{style}/style.json', 'w') as f:
        f.write(datas)


def build_sprites(style):
    subprocess.run(['spreet', '--minify-index-file',
                    cwd / f'src/styles/{style}/icons',
                    cwd / f'dist/styles/{style}/sprite'])
    subprocess.run(['spreet', '--minify-index-file', '--retina',
                    cwd / f'src/styles/{style}/icons',
                    cwd / f'dist/styles/{style}/sprite@2x'])


if __name__ == '__main__':
    (cwd / 'dist/styles').mkdir(parents=True, exist_ok=True)
    build_config()
    styles = [x.name for x in (cwd / 'src/styles').iterdir() if x.is_dir()]
    for style in styles:
        (cwd / f'dist/styles/{style}').mkdir(parents=True, exist_ok=True)
        build_style(style)
        build_sprites(style)
