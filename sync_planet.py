from datetime import date, timedelta
from pathlib import Path
from subprocess import run

cwd = Path(__file__).parent

if __name__ == "__main__":
    today = date.today()
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    run(
        [
            "rclone",
            "copyurl",
            "--progress",
            "--s3-no-check-bucket",
            "--s3-chunk-size=256M",
            f"https://build.protomaps.com/{yesterday_str}.pmtiles",
            "r2://fieldmaps-tiles/planet.pmtiles",
        ]
    )
