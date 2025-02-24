from typing import Optional
import random
import numpy as np
from ..base_module import BaseTaskClass, TestItem

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
Напишите программу на ассемблере, которая складывает два числа, переданных в регистрах a2 и a3, и результат сохраняет в регистр a0. Программа должна завершаться командой ret.

Шаблон программы для подготовки решения:

```
.globl solution
solution:
    # a0 = result
    ret
```

"""

MAIN_S = r"""
.globl main
.text
main:
    la a0, x
    la a1, y
    call read_data
    ld a2, x
    ld a3, y
    call solution
    call print_result
    addi a0, x0, 0
    addi a7, x0, 93
    ecall

.data
x: .dword 0
y: .dword 0
"""

PRINT_RESULT_C = r"""
#include<stdio.h>
#include<stdint.h>

void print_result(int64_t result){
    fprintf(stderr, "%ld\n", result);
}

void read_data(int64_t *a, int64_t *b){
    scanf("%ld %ld", a, b);
}
"""


class Lab10Test(BaseTaskClass):

    def __init__(
            self, *args,
            a2_class: str = DEFAULT_TYPE, a3_class: str = DEFAULT_TYPE,
            a2_min: Optional[int] = 1, a2_max: Optional[int] = 10,
            a3_min: Optional[int] = 1, a3_max: Optional[int] = 10,
            **kwself
    ):
        super().__init__(*args, **kwself)
        self.a2_class = INT_TYPES.get(a2_class)
        self.a3_class = INT_TYPES.get(a3_class)
        self.a2_min = a2_min if a2_min is not None else 1
        self.a3_min = a3_min if a3_min is not None else 1
        self.a2_max = a2_max if a2_max is not None else 10
        self.a3_max = a3_max if a3_max is not None else 10

        self.check_files = {
            "main.s": MAIN_S,
            "print_result.c": PRINT_RESULT_C,
        }

    def generate_task(self) -> str:
        return TASK_DESCRIPTION

    def _generate_tests(self):
        random.seed(42)
        self.tests = []

        for _ in range(self.tests_num):
            a2 = random.randint(self.a2_min, self.a2_max)
            a3 = random.randint(self.a3_min, self.a3_max)
            print(a2)
            print(a3)
            result = a2 + a3

            self.tests.append(TestItem(
                input_str=f"{a2} {a3}",
                showed_input=f"a2={a2} a3={a3}",
                expected=str(result),
                compare_func=self._compare_default
            ))

    def check_sol_prereq(self) -> Optional[str]:
        error = super().check_sol_prereq()
        if error is not None:
            return error

        if self.solution.find("ecall") != -1:
            return "Ошибка: Системные вызовы запрещены."
