#!/usr/bin/env python3
import os, sys, subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / "venv"
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"

IS_WINDOWS = sys.platform == "win32"
PIP = VENV / ("Scripts" if IS_WINDOWS else "bin") / "pip"
PYTHON = VENV / ("Scripts" if IS_WINDOWS else "bin") / "python"
SCRIPT = ROOT / "colorful"

def run(cmd, cwd=None):
    print(f"  $ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd or ROOT)

def step(msg):
    print(f"\n  \x1b[38;2;97;114;133m\u2501\u2501\u2501\x1b[0m  {msg}")

def prompt(text, default=""):
    val = input(f"  \x1b[38;2;177;211;254m?\x1b[0m  {text} \x1b[38;2;97;114;133m[{default}]\x1b[0m \x1b[38;2;97;114;133m\u203a\x1b[0m ").strip()
    return val or default

print()
print(f"  \x1b[38;2;163;241;203m\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\x1b[0m")
print(f"  \x1b[38;2;177;211;254m  colorful\x1b[0m  \x1b[38;2;97;114;133minstall\x1b[0m")
print(f"  \x1b[38;2;163;241;203m\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\x1b[0m")

step("creating virtual environment")
if VENV.exists():
    print(f"  venv already exists at {VENV}")
else:
    run([sys.executable, "-m", "venv", str(VENV)])

step("installing dependencies")
run([str(PIP), "install", "-r", str(ROOT / "requirements.txt")])

step("setting up .env")
if not ENV_EXAMPLE.exists():
    ENV_EXAMPLE.write_text("# OPENROUTER_API_KEY=sk-or-v1-...\n# COLORFUL_MODEL=\n# COLORFUL_TEXT_MODEL=\n# COLORFUL_OUTPUT_DIR=\n")
if not ENV_FILE.exists():
    shutil.copy(str(ENV_EXAMPLE), str(ENV_FILE))
    print(f"  created {ENV_FILE}")
key = os.environ.get("OPENROUTER_API_KEY")
if not key:
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY=") and "sk-or-" in line:
            key = line.split("=", 1)[1].strip()
if not key or key.startswith("sk-or-v1-") is False:
    new_key = prompt("OpenRouter API key (sk-or-v1-...)", "")
    if new_key:
        lines = ENV_FILE.read_text().splitlines()
        found = False
        for i, line in enumerate(lines):
            if line.startswith("OPENROUTER_API_KEY="):
                lines[i] = f"OPENROUTER_API_KEY={new_key}"
                found = True
                break
        if not found:
            lines.append(f"OPENROUTER_API_KEY={new_key}")
        ENV_FILE.write_text("\n".join(lines) + "\n")

step("adding to PATH")
SHELL = os.environ.get("SHELL", "")
if IS_WINDOWS:
    bin_dir = Path.home() / ".local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    bat = bin_dir / "colorful.bat"
    bat.write_text(f'@"{PYTHON}" "{SCRIPT}" %*\n')
    print(f"  created {bat}")
    path_var = str(bin_dir)
    if path_var not in os.environ.get("PATH", ""):
        print(f"  add {path_var} to your PATH manually, or run:")
        print(f'    [Environment]::SetEnvironmentVariable("Path", '
              f'[Environment]::GetEnvironmentVariable("Path","User") + ";{path_var}", "User")')
elif "zsh" in SHELL:
    rc = Path.home() / ".zshrc"
    alias_line = f'alias colorful="{PYTHON} {SCRIPT}"'
    if rc.exists() and alias_line in rc.read_text():
        print(f"  alias already in {rc}")
    else:
        with open(str(rc), "a") as f:
            f.write(f"\n{alias_line}\n")
        print(f"  added alias to {rc}")
else:
    rc = Path.home() / ".bashrc"
    alias_line = f'alias colorful="{PYTHON} {SCRIPT}"'
    if rc.exists() and alias_line in rc.read_text():
        print(f"  alias already in {rc}")
    else:
        with open(str(rc), "a") as f:
            f.write(f"\n{alias_line}\n")
        print(f"  added alias to {rc}")

print()
print(f"  \x1b[38;2;163;241;203m\u2714\x1b[0m  \x1b[38;2;177;211;254mcolorful\x1b[0m installed")
print(f"  \x1b[38;2;97;114;133mrestart your terminal or run: source ~/.zshrc (or ~/.bashrc)\x1b[0m")
print()
print(f"  \x1b[38;2;223;184;255mquick start\x1b[0m")
print(f"    \x1b[38;2;97;114;133mcolorful\x1b[0m")
print(f"    \x1b[38;2;97;114;133mcolorful -p \"hello\"\x1b[0m")
print(f"    \x1b[38;2;97;114;133mcolorful -i photo.jpg -p \"make it a painting\"\x1b[0m")
print(f"    \x1b[38;2;97;114;133mcolorful -h\x1b[0m")
print()
