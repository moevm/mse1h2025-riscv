import random
import networkx as nx
import matplotlib.pyplot as plt


def generate_random_values(student_id):
    random.seed(student_id)
    t1 = random.randint(0, 0xFFFF)
    t2 = random.randint(0, 0xFFFF)
    return t1, t2


def generate_graph(max_depth=5, max_nodes=10):
    G = nx.DiGraph()
    G.add_node(0)

    # список доступных для соединения узлов
    available_nodes = {0: 0}  # {узел: глубина}
    out_degree = {0: 0}  # {узел: количество исходящих рёбер}

    for i in range(1, max_nodes):
        # выбираем случайного родителя, у которого меньше двух детей
        parent = random.choice([node for node in available_nodes if out_degree[node] < 2])

        # добавляем новое ребро
        G.add_edge(parent, i)
        out_degree[parent] += 1
        out_degree[i] = 0

        # обновляем глубину нового узла
        depth = available_nodes[parent] + 1
        available_nodes[i] = depth

        # удаляем узлы, которые достигли лимита исходящих рёбер
        if out_degree[parent] == 2:
            del available_nodes[parent]

        if depth >= max_depth:
            del available_nodes[i]

    return G


def add_operations_and_conditions(G, student_id):
    # добавляет операции и условия для каждой вершины графа
    random.seed(student_id)

    operations = ["add", "sub", "xor", "and", "or", "sll", "srl"]
    registers = ["t1", "t2", "t3", "t5", "t6"]

    for node in G.nodes():
        # выбираем операцию
        op = random.choice(operations[:-1])
        flag_use_t = 0

        # с вероятностью 50% выбираем t3 как целевой регистр
        if random.random() < 0.5:
            target_reg = "t3"
        else:
            target_reg = random.choice([reg for reg in registers if reg != "t3"])  # Выбираем любой регистр, кроме t3

        source_reg = random.choice(registers)  # Источник может быть любым регистром
        if source_reg in ["t5", "t6"]:
            init_value = random.randint(0, 0xFFFF)
            G.nodes[node]["init"] = f"li {source_reg}, {init_value}"

        if random.random() < 0.5:
            imm = random.randint(1, 15) if "sll" in op or "srl" in op else random.randint(0, 0xFFFF)
        else:
            imm = random.choice(registers)
            flag_use_t = imm
            if imm in ["t5", "t6"]:
                init_value = random.randint(0, 0xFFFF)
                G.nodes[node]["init"] = f"li {imm}, {init_value}"

        G.nodes[node]["op"] = f"{op} {target_reg}, {source_reg}, {imm}"

        # добавляем условие перехода
        if G.out_degree(node) > 1:
            condition = random.choice(["beqz", "bnez", "blt", "bge", "je", "jne", "ja", "jae", "jb", "jbe"])
            if condition in ["beqz", "bnez", "blt", "bge"]:
                G.nodes[node]["condition"] = f"{condition} {target_reg},"
            else:
                if flag_use_t != 0:
                    G.nodes[node][
                        "condition"] = f"cmp {target_reg}, {random.choice([flag_use_t, random.randint(0, 0xFFFF)])}\n    {condition}"
                else:
                    G.nodes[node]["condition"] = f"cmp {target_reg}, {random.randint(0, 0xFFFF)}\n    {condition}"
        else:
            G.nodes[node]["condition"] = "j"  # безусловный переход


def do_operation(registers, target_reg, source_reg, op, operand):
    # определяем операнд (число или регистр)
    if operand in registers:
        imm = registers[operand]
    else:
        imm = int(operand, 0)

    # применяем операцию к целевому регистру
    if op == "add":
        registers[target_reg] = registers[source_reg] + imm
    elif op == "sub":
        registers[target_reg] = registers[source_reg] - imm
    elif op == "xor":
        registers[target_reg] = registers[source_reg] ^ imm
    elif op == "and":
        registers[target_reg] = registers[source_reg] & imm
    elif op == "or":
        registers[target_reg] = registers[source_reg] | imm
    elif op == "sll":
        registers[target_reg] = (registers[source_reg] << imm) & 0xFFFFFFFF
    elif op == "srl":
        registers[target_reg] = (registers[source_reg] >> imm) & 0xFFFFFFFF
    return registers


def calculate_t4(G, t1, t2):
    # эмулирует выполнение графа и вычисляет конечное значение t3 (t4)
    registers = {'t1': t1, 't2': t2, 't3': 0, 't4': 0, 't5': 0, 't6': 0}
    current_node = 0

    while True:
        # получаем операцию в узле
        op_str = G.nodes[current_node]["op"]
        op_parts = op_str.split()
        op = op_parts[0]
        target_reg = op_parts[1][:-1]
        source_reg = op_parts[2][:-1]
        operand = op_parts[-1]
        if "init" in G.nodes[current_node]:
            init = G.nodes[current_node]["init"].split()
            registers[init[1][:-1]] = int(init[2])

        registers = do_operation(registers, target_reg, source_reg, op,operand)

        # получаем список исходящих рёбер
        successors = list(G.successors(current_node))

        if not successors:
            break  # если нет исходящих рёбер, завершаем выполнение

        # проверяем условие перехода
        condition = G.nodes[current_node]["condition"].split()
        if condition[0] == "j":
            current_node = successors[0]  # Безусловный переход
        elif condition[0] == "beqz" and registers[target_reg] == 0:
            current_node = successors[0]
        elif condition[0] == "bnez" and registers[target_reg] != 0:
            current_node = successors[0]
        elif condition[0] == "blt" and registers[target_reg] < 0:
            current_node = successors[0]
        elif condition[0] == "bge" and registers[target_reg] >= 0:
            current_node = successors[0]
        elif condition[0] == "cmp":
            if condition[2] in registers:
                cond_num = registers[condition[2]]
            else:
                cond_num = int(condition[2])
            if condition[-1] == 'je' and registers[target_reg] == cond_num:
                current_node = successors[0]
            elif condition[-1] == 'jne' and registers[target_reg] != cond_num:
                current_node = successors[0]
            elif condition[-1] == 'ja' and registers[target_reg] > cond_num:
                current_node = successors[0]
            elif condition[-1] == 'jae' and registers[target_reg] >= cond_num:
                current_node = successors[0]
            elif condition[-1] == 'jb' and registers[target_reg] < cond_num:
                current_node = successors[0]
            elif condition[-1] == 'jbe' and registers[target_reg] <= cond_num:
                current_node = successors[0]
        else:
            current_node = successors[1]  # иначе идём по второму пути

    # добавляем секретное действие (+1 функция) которое нужно будет восстановить студенту
    operations = ["add", "sub", "xor", "and", "or", "sll", "srl"]
    op_secret = random.choice(operations[:-1])
    if random.random() < 0.5:
        imm_secret = random.randint(1, 15) if "sll" in op or "srl" in op else random.randint(0, 0xFFFF)
    else:
        imm_secret = random.choice(list(registers.keys()))
        if imm_secret in ["t5", "t6"] and registers[imm_secret] == 0:
            registers[imm_secret] = random.randint(0, 0xFFFF)
    registers = do_operation(registers, 't3', 't3', op_secret, imm_secret)
    return registers['t3'], [op_secret, imm_secret]


def generate_code_from_graph(G, t1, t2, t4):
    # генерирует RISC-V код на основе графа
    asm_code = ".data\n"
    asm_code += '    error: .asciz "Access denied!"\n'
    asm_code += '    flag: .asciz "SUCCESS"\n\n'
    asm_code += ".text\n.globl _start\n_start:\n"

    asm_code += f"    li t1, {hex(t1)}\n"
    asm_code += f"    li t2, {hex(t2)}\n"
    asm_code += f"    li t4, {hex(t4)}  # ожидаемое значение t4\n"

    for node in sorted(G.nodes()):  # обход узлов в порядке возрастания
        op = G.nodes[node]["op"]
        condition = G.nodes[node]["condition"]

        asm_code += f"node_{node}:\n"
        if "init" in G.nodes[node]:
            asm_code += f"    {G.nodes[node]['init']}\n"
        asm_code += f"    {op}\n"

        # получаем список исходящих рёбер
        successors = list(G.successors(node))

        if not successors:  # если нет исходящих рёбер
            asm_code += "    j final\n"
        elif condition == "j":  # безусловный переход
            asm_code += f"    j node_{successors[0]}\n"
        else:  # Условный переход
            asm_code += f"    {condition} node_{successors[0]}\n"
            if len(successors) > 1:  # если есть второй переход
                asm_code += f"    j node_{successors[1]}\n"

    # проверка на успех
    asm_code += "final:\n    bne t3, t4, fail  # если t3 != t4 fail\n    j success  # если t3 == t4 success\n"

    asm_code += "fail:\n    li a0, 1\n    la a1, error\n    li a2, 13\n    li a7, 64\n    ecall\n    j exit\n"

    asm_code += "success:\n    li a0, 1\n    la a1, flag\n    li a2, 13\n    li a7, 64\n    ecall\n"

    asm_code += "exit:\n    li a7, 93\n    li a0, 0\n    ecall\n"
    return asm_code


def visualize_graph(G):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, k=2, iterations=50)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=12,
            font_weight='bold')
    plt.title("Сгенерированный граф кода")
    plt.show()


def generate_file(file_name, student_id=123456):
    # создаём структуру графа
    G = generate_graph(max_nodes=10, max_depth=5)

    # добавляем операции и условия
    add_operations_and_conditions(G, student_id)

    # генерируем RISC-V код
    t1, t2 = generate_random_values(student_id)
    t4, secret = calculate_t4(G, t1, t2)
    asm_code = generate_code_from_graph(G, t1, t2, t4=0)

    # сохраняем код в файл
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(asm_code)


if __name__ == '__main__':
    # создаём структуру графа
    G = generate_graph(max_nodes=10, max_depth=5)

    student_id = 123456

    # добавляем операции и условия
    add_operations_and_conditions(G, student_id)

    # генерируем RISC-V код
    t1, t2 = generate_random_values(student_id)
    t4, secret = calculate_t4(G, t1, t2)
    asm_code = generate_code_from_graph(G, t1, t2, t4=0)

    # сохраняем код в файл
    with open("lab1.S", "w", encoding="utf-8") as f:
        f.write(asm_code)

    # print("Файл с RISC-V кодом сгенерирован: generated_task.s")
    visualize_graph(G)
