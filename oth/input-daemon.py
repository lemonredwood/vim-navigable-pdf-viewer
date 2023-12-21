import subprocess
proc = subprocess.Popen(["sudo","python3","keybinds.py"])
take = input();
if input=="end":
    proc.terminate()
