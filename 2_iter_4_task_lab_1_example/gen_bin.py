import subprocess
import sys
import os
from generation_1lab import generate_file


LINKER_FILE = 'link.ld'


def assemble_to_binary(asm_filename, link_script):
    obj_filename = asm_filename.replace('.S', '.o')
    elf_filename = asm_filename.replace('.S', '.elf')
    bin_filename = asm_filename.replace('.S', '.bin')

    try:
        subprocess.run(
            ['riscv64-unknown-elf-gcc', '-nostdlib', '-o', bin_filename, asm_filename]
        )
        # Ассемблирование
        # subprocess.run(
        #     [
        #         'riscv64-unknown-elf-as',
        #         '-march=rv64gc',
        #         asm_filename,
        #         '-o', obj_filename
        #     ],
        #     check=True
        # )

        # Линковка с явным указанием прав
        # subprocess.run(
        #     [
        #         'riscv64-unknown-elf-ld',
        #         '-T', link_script,
        #         '-Map=output.map',
        #         obj_filename,
        #         '-o', elf_filename
        #     ],
        #     check=True
        # )

        # Генерация бинарника
        # subprocess.run(
        #     [
        #         'riscv64-unknown-elf-objcopy',
        #         '-O', 'binary',
        #         elf_filename,
        #         bin_filename
        #     ],
        #     check=True
        # )

        # subprocess.run(['rm', '-f', obj_filename, elf_filename], check=True)

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
    assemble_to_binary(file_name, LINKER_FILE)


if __name__ == "__main__":
    make_bin()
