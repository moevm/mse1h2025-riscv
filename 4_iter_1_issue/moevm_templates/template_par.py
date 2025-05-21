import json
import sys
import subprocess
import os

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

user_id = int(sys.argv[2].split("=")[1])
user_id = (((user_id ** 2) << 10) * 43) >> 5

def fake_compile(self, *args, **kwargs):
    return None
riscv_course.lab2_debug.Lab2Debug._Lab2Debug__compile_binary = fake_compile

lab_checker = riscv_course.lab2_debug.Lab2Debug(seed=user_id)
task = lab_checker.init_task()

parts = task.split("```")
if len(parts) >= 3:
    description = parts[0].strip()
    asm_code = parts[1].strip()
    rest = parts[2].strip()
else:
    description = task
    asm_code = ""
    rest = ""

task_html = (
    description.replace("\n", "<br>") +
    f"<pre>{asm_code}</pre>" +
    "<br>" + rest.replace("\n", "<br>")
)

print(json.dumps({
    "task_seed": user_id,
    "task": task_html
}))
