import subprocess
from pathlib import Path

cwd = Path(__file__).parent

if __name__ == '__main__':
    subprocess.run([
        's3cmd', 'sync',
        '--acl-public',
        '--delete-removed',
        '--rexclude', '\/\.',
        '--multipart-chunk-size-mb=5120',
        cwd / 'dist/config.json',
        f's3://data.fieldmaps.io/tileserver_gl/config.json',
    ])
    subprocess.run([
        's3cmd', 'sync',
        '--acl-public',
        '--delete-removed',
        '--rexclude', '\/\.',
        '--multipart-chunk-size-mb=5120',
        cwd / 'dist/styles',
        f's3://data.fieldmaps.io/tileserver_gl/',
    ])
    subprocess.run([
        's3cmd', 'sync',
        '--acl-public',
        '--delete-removed',
        '--rexclude', '\/\.',
        '--multipart-chunk-size-mb=5120',
        cwd / 'dist/data/adm.mbtiles',
        f's3://data.fieldmaps.io/tileserver_gl/data/adm.mbtiles',
    ])
    for l in range(0, 2):
        subprocess.run([
            's3cmd', 'sync',
            '--acl-public',
            '--delete-removed',
            '--rexclude', '\/\.',
            '--multipart-chunk-size-mb=5120',
            cwd / f'dist/data/adm{l}.mbtiles',
            f's3://data.fieldmaps.io/tileserver_gl/data/adm{l}.mbtiles',
        ])
