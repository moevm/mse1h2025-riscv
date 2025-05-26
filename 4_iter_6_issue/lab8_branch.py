from typing import Optional
import subprocess
import shlex
import urllib.request
import hashlib
import hmac
import datetime
import numpy as np
from ..base_module import BaseTaskClass, TestItem
from .lab8_gen import GenerateLab8

DEFAULT_TYPE = "int64"
INT_TYPES = {
    "int64":  np.int64,
    "int32":  np.int32,
    "int16":  np.int16,
    "int8":   np.int8,
    "uint64": np.uint64,
    "uint32": np.uint32,
    "uint16": np.uint16,
    "uint8":  np.uint8
}

TASK_DESCRIPTION = """
Проанализируйте программу на ассемблере RISC-V, которая создает граф вызовов функций и вычисляет итоговое значение в соответствии с вашим вариантом.

Исходный код программы будет сгенерирован автоматически на основе вашего ID. 
Ваша задача - проанализировать последовательность вызовов функций и операции с регистрами, чтобы определить итоговое значение, которое должно быть записано в регистр a5.

Сгенерированная программа для анализа:
"""

PRINT_RESULT_C = r"""
#include<stdio.h>
#include<stdint.h>

void print_result(int64_t result){
    fprintf(stderr, "%ld\n", result);
}
"""

DEFAULT_START_LEN = 12
DEFAULT_DEEP = 0.5

access_key = 'YCAJEFio4CdAZohHoafHTpJBA'
secret_key = 'YCPud0aAiVCnU-37dUEWm9lgzEfUB5_tCfczz1QE'
bucket = 'mse1h2025v2'


def hmac_sha256(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def sha256_hash(data):
    return hashlib.sha256(data).hexdigest()


class Lab8Branch(BaseTaskClass):
    def __init__(
        self, *args,
        n: int = DEFAULT_START_LEN,
        deep: float = DEFAULT_DEEP,
        answer: str = "",
        **kwself
    ):
        super().__init__(*args, **kwself)
        self.generator = GenerateLab8(n=n, deep=deep, id=self.seed).generate_asm()
        self.expected_result = self.generator[0]
        self.asm_code = self.generator[1]
        self.answer = answer
        self.n = n
        self.deep = deep
        self.check_files = {
            "print_result.c": PRINT_RESULT_C,
        }
    
    def load_student_solution(
    self, solfile: Optional[str] = None, solcode: Optional[str] = None):
        self.answer = solcode
    # Do nothing, pass solution (answer) as argument
        pass


    def generate_task(self) -> str:
        main_s = self.asm_code
        if (err := self.__compile_binary(main_s)) is not None:
            return err

        temp_filename = 'temp_filename.s'
        with open(temp_filename, "w", encoding="utf-8") as f:
            f.write(self.asm_code)

        # compile_command = f'riscv64-unknown-linux-gnu-gcc -c -nostdlib -static -g {temp_filename} -o {self.seed}.bin'
        emulator = 'qemu-riscv64'
        if self.jail_path != "":
            emulator = "/" + emulator
        compile_command = f'{self.jail_exec} {self.jail_path}'
        subprocess.run(shlex.split(compile_command))

        filename_upload = f'{self.seed}.bin'

        url = self.upload_file(filename_upload)

        return TASK_DESCRIPTION + url

    def upload_file(self, filename: str) -> str:
        object_key = filename  # Имя файла в хранилище
        file_path = filename  # Локальный файл

        with open(file_path, 'rb') as f:
            content = f.read()

        # Временные метки
        now = datetime.datetime.utcnow()
        amz_date = now.strftime('%Y%m%dT%H%M%SZ')
        date_scope = now.strftime('%Y%m%d')

        # Настройки доступа
        acl_header = 'public-read'
        content_hash = sha256_hash(content)

        # Формирование запроса
        canonical_headers = (
            f'host:{bucket}.storage.yandexcloud.net\n'
            f'x-amz-acl:{acl_header}\n'
            f'x-amz-content-sha256:{content_hash}\n'
            f'x-amz-date:{amz_date}\n'
        )

        canonical_request = (
            'PUT\n'
            f'/{object_key}\n'
            '\n'
            f'{canonical_headers}\n'
            'host;x-amz-acl;x-amz-content-sha256;x-amz-date\n'
            f'{content_hash}'
        )

        # Подпись
        string_to_sign = (
            f'AWS4-HMAC-SHA256\n'
            f'{amz_date}\n'
            f'{date_scope}/ru-central1/s3/aws4_request\n'
            f'{sha256_hash(canonical_request.encode("utf-8"))}'
        )

        signing_key = hmac_sha256(hmac_sha256(hmac_sha256(
            hmac_sha256(f'AWS4{secret_key}'.encode('utf-8'), date_scope),
            'ru-central1'),
            's3'),
            'aws4_request'
        )
        signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

        # Заголовки запроса
        authorization_header = (
            'AWS4-HMAC-SHA256 Credential={}/{}, '
            'SignedHeaders=host;x-amz-acl;x-amz-content-sha256;x-amz-date, '
            'Signature={}'
        ).format(access_key, f'{date_scope}/ru-central1/s3/aws4_request', signature)

        url = f'https://{bucket}.storage.yandexcloud.net/{object_key}'
        headers = {
            'Host': f'{bucket}.storage.yandexcloud.net',
            'x-amz-acl': acl_header,
            'x-amz-date': amz_date,
            'x-amz-content-sha256': content_hash,
            'Authorization': authorization_header,
            'Content-Type': 'application/octet-stream'  # MIME-тип для бинарных файлов
        }

        # Отправка
        req = urllib.request.Request(url, data=content, headers=headers, method='PUT')
        try:
            with urllib.request.urlopen(req) as response:
                public_url = f'https://storage.yandexcloud.net/{bucket}/{object_key}'
        except urllib.error.HTTPError as e:
            print(f'Ошибка: {e.code} {e.reason}')

        return public_url

    def check_sol_prereq(self) -> Optional[str]:
        return None


    def compile(self) -> Optional[str]:
        return None


    def __compile_binary(self, src: str) -> Optional[str]:
        t_files = self.check_files
        self.check_files = {"main.s": src}
        self.solution = ""
        if (err := self._compile_internal(compile_args="-nostdlib -static -g")) is not None:
            return f"Bad source code generated. Error: {err}.\n" \
                    "Contact to the authors to solve the problem"
        self.check_files = t_files
        return None
    
    def run_tests(self) -> tuple[bool, str]:
        self.check_files["main.s"] = self.asm_code.replace("_start", "main")
        self.solution = ""
        if (err := self._compile_internal(compile_args="-static")) is not None:
            return (False, f"Bad source code generated. Error: {err}.\n"
                            "Contact to the authors to solve the problem"
                    )

        dummy_test = TestItem(
            input_str="", showed_input="",
            expected="text", compare_func=self._compare_default
        )
        res = self._run_solution_internal(dummy_test)
        if res is None:
            return (False, "Bad source code generated.\n"
                            "Contact to the authors to solve the problem"
                    )

        if self.answer.strip() == str(self.expected_result).strip():
            return True, "OK"
        return False, f"Wrong answer"

    def _generate_tests(self):
        pass
