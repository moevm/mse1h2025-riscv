import subprocess
import sys
import os

def assemble_to_binary(asm_filename, bin_filename, link_script):
    obj_filename = asm_filename.replace('.S', '.o')
    elf_filename = asm_filename.replace('.S', '.elf')

    try:
        # Ассемблирование
        subprocess.run(
            [
                'riscv64-unknown-elf-as',
                '-march=rv64gc',
                asm_filename,
                '-o', obj_filename
            ],
            check=True
        )

        # Линковка с явным указанием прав
        subprocess.run(
            [
                'riscv64-unknown-elf-ld',
                '-T', link_script,
                '-Map=output.map',
                obj_filename,
                '-o', elf_filename
            ],
            check=True
        )

        # Генерация бинарника
        subprocess.run(
            [
                'riscv64-unknown-elf-objcopy',
                '-O', 'binary',
                elf_filename,
                bin_filename
            ],
            check=True
        )

        subprocess.run(['rm', '-f', obj_filename, elf_filename], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Требуется RISC-V toolchain!", file=sys.stderr)
        print("Установите: sudo apt install gcc-riscv64-unknown-elf", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asm_file = "lab_1_template.S"     
    bin_file = "lab_1_template.bin"   
    linker_script = "link.ld"  

    # Генерация ассемблерного кода 
    # ...

    assemble_to_binary(asm_file, bin_file, linker_script)