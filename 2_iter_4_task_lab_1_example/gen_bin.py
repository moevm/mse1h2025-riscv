import subprocess
import sys
from generation_1lab import generate_file


def assemble_to_binary(asm_filename):
    bin_filename = asm_filename.replace('.S', '.bin')

    try:
        subprocess.run(
            ['riscv64-unknown-elf-gcc', '-nostdlib', '-o', bin_filename, asm_filename]
        )

    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Требуется RISC-V toolchain!", file=sys.stderr)
        print("Установите: sudo apt install gcc-riscv64-unknown-elf", file=sys.stderr)
        sys.exit(1)


def make_bin(student_id=123456):
    file_name = 'file.S'

    generate_file(file_name, student_id)
    assemble_to_binary(file_name)


if __name__ == "__main__":
    make_bin()
