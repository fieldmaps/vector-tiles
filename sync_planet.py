import subprocess
from datetime import date
from pathlib import Path

cwd = Path(__file__).parent

if __name__ == "__main__":
    today = date.today().strftime("%Y%m%d")
    subprocess.run(
        [
            "rclone",
            "copyurl",
            "--progress",
            "--s3-no-check-bucket",
            "--s3-chunk-size=256M",
            f"https://build.protomaps.com/{today}.pmtiles",
            "r2://fieldmaps-tiles/planet.pmtiles",
        ]
    )
