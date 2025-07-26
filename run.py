import subprocess

if __name__ == "__main__":
    subprocess.run(["python", "-m", "adm"], check=False)
    subprocess.run(["python", "-m", "admx"], check=False)
    subprocess.run(["python", "sync.py"], check=False)
