import json
import sys
import subprocess
import os
import warnings

repo_url = "https://github.com/MarieLukyanova/workshop_risc-v.git"
repo_dir = "workshop_risc-v"
requirements_path = os.path.join(repo_dir, "requirements.txt")

if not os.path.exists(repo_dir):
    subprocess.run(["git", "clone", repo_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    subprocess.run(["git", "-C", repo_dir, "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

src_path = os.path.join(repo_dir, "src")
sys.path.insert(0, os.path.abspath(src_path))

subprocess.run(["pip", "install", "-r", requirements_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import riscv_course

task_seed = """{{ task_seed }}"""
task_seed = int(task_seed.strip())

lab_checker = riscv_course.lab2_debug.Lab2Debug(
    seed=task_seed,
    jail_path="./jail",
    jail_exec="fakechroot chroot"
)

os.environ["PATH"] += ":/opt/riscv/bin"
warnings.filterwarnings("ignore", category=RuntimeWarning)

if os.system("cp -r /jail_template_riscv ./jail") != 0:
    print(json.dumps({"fraction": 0.0, "prologuehtml": "Ошибка окружения"}))
    exit(1)

student_answer = """{{ STUDENT_ANSWER | e('py') }}"""
student_answer = student_answer.strip()
lab_checker.load_student_solution(solcode=student_answer)
passed, msg = lab_checker.check()

print(msg)