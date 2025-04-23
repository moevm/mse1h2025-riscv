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

n = 7
deep = 6

lab_checker = riscv_course.lab9_first.Lab9First(
    n=n,
    deep=deep,
    student_id=user_id,
)

task_raw = lab_checker.init_task()

if "```" not in task_raw:
    formatted_task = task_raw.replace("\n", "<br>")
else:
    ridx1 = task_raw.rfind("```")
    ridx2 = task_raw[:ridx1].rfind("```")

    before_code = task_raw[:ridx2].strip().replace("\n", "<br>")
    code_block = task_raw[ridx2 + 3:ridx1].strip()
    after_code = task_raw[ridx1 + 3:].strip().replace("\n", "<br>")

    formatted_task = f"{before_code}<pre>{code_block}</pre>{after_code}"

data = {
    "task": formatted_task,
    "task_seed": user_id,
}

print(json.dumps(data, ensure_ascii=False))
