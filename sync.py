import subprocess
from pathlib import Path

cwd = Path(__file__).parent


def upload(src, dest):
    subprocess.run(
        [
            "rclone",
            "sync",
            "--progress",
            "--include={adm.pmtiles,adm0.pmtiles,adm1.pmtiles,adm2.pmtiles,adm3.pmtiles,adm4.pmtiles}",
            "--s3-no-check-bucket",
            "--s3-chunk-size=256M",
            src,
            dest,
        ]
    )


if __name__ == "__main__":
    upload(cwd / "dist/data", "r2://fieldmaps-tiles")
