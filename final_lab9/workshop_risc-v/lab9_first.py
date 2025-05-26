from typing import Optional
import os
import numpy as np
from ..base_module import BaseTaskClass, TestItem
from .lab9_gen import start_gen

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
Вам предоставлена сломанная программа которая, ваша задача найти в чем ошибка в коде, и исправить его, чтобы программа выводила SUCCESS.
Для решения требуется чтобы условие t3 == t4 было истинно. Изначально t4 = 0.  Загрузите исправленный код для проверки.

Ваша функция с ошибкой:   

"""

PRINT_RESULT_C = r"""
#include<stdio.h>
#include<stdint.h>

void print_result(int64_t result){
    fprintf(stderr, "%ld\n", result);
}
"""

DEFAULT_START_LEN = 11
DEFAULT_DEEP = 6

class Lab9First(BaseTaskClass):
    def __init__(
            self, *args,
            n: int = DEFAULT_START_LEN,
            deep: int = DEFAULT_DEEP,
            answer: str = "",
            interactive: bool = False, print_task_when_i: bool = True,
            **kwself
    ):
        super().__init__(*args, **kwself)
        self.deep = deep
        self.asm_code, self.expected_result = start_gen(n=n, deep=self.deep, student_id=self.seed)
        self.answer = answer
        self.interactive = interactive
        self.print_task_when_i = print_task_when_i
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
        return TASK_DESCRIPTION + self.asm_code


    # def init_task(self) -> str:
    #     task_descp = super().init_task()
    #     if self.interactive:
    #         if self.print_task_when_i:
    #             print(task_descp)
    #         os.system("rm -rf main.py pyproject.toml requirements.txt src sol.s main.s print_result.c")
    #         os.execlp("bash", "-c")
    #     return task_descp


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