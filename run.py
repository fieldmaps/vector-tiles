import subprocess

if __name__ == "__main__":
    subprocess.run(["python", "-m", "adm"])
    subprocess.run(["python", "-m", "admx"])
    subprocess.run(["python", "sync.py"])
