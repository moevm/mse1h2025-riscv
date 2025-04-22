import difflib
import os
import pytest

# Фикстуры для подготовки тестовых данных
@pytest.fixture
def original_path():
    return os.path.join(os.path.dirname(__file__), '..', 'lab9.s')

@pytest.fixture
def student_path():
    return os.path.join(os.path.dirname(__file__), '..', 'solution', 'student_lab9.s')

def read_lines(path):
    # Чтение строк из файла, игнорируя пустые строки
    with open(path) as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def test_line_count(student_path, original_path):
    # Проверка, что количество строк не уменьшилось и не увеличилось
    original = read_lines(original_path)
    student = read_lines(student_path)
    assert abs(len(original) - len(student)) == 0, f"Количество строк отличается: {len(student)} != {len(original)}"

def test_ecall_count(student_path, original_path):
    # Проверка, что количество вызовов ecall не увеличилось
    original = read_lines(original_path)
    student = read_lines(student_path)
    assert student.count("ecall") <= original.count("ecall"), f"Добавлены лишние ecall! Ожидалось: {original.count('ecall')}, Получено: {student.count('ecall')}"

def test_registers_usage(student_path, original_path):
    # Проверка, что использованы те же регистры, что и в исходном файле
    def extract_regs(lines):
        regs = []
        for line in lines:
            regs.extend([token for token in line.split() if token.startswith(("t", "a"))])  # Выбираем регистры
        return set(regs)

    original = extract_regs(read_lines(original_path))
    student = extract_regs(read_lines(student_path))
    assert original <= student, f"Некоторые оригинальные регистры не используются. Ожидались: {original}, Получены: {student}"

def test_data_section_unchanged(student_path, original_path):
    # Проверка, что секция .data осталась без изменений
    def extract_data(lines):
        in_data = False
        section = []
        for line in lines:
            if ".data" in line:
                in_data = True
                continue
            if in_data:
                if ".text" in line:
                    break
                section.append(line)
        return section

    original = extract_data(read_lines(original_path))
    student = extract_data(read_lines(student_path))
    assert original == student, f".data секция была изменена!"

def test_only_one_line_changed(student_path, original_path):
    # Проверка, что изменена только одна строка
    original = read_lines(original_path)
    student = read_lines(student_path)

    # Сравниваем файлы с помощью difflib
    diff = list(difflib.unified_diff(original, student))
    changed_lines = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]

    # Проверка, что изменена только одна строка
    assert len(changed_lines) != 0, "Изменения не были внесены"
    assert len(changed_lines) <= 2, f"Изменено больше одной строки! Изменения: {changed_lines}"
