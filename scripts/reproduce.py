from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parents[1]
for script in ['analyze.py','figures.py','validate.py']:
    subprocess.run([sys.executable,str(root/'scripts'/script)],cwd=root,check=True)
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root,check=True)
