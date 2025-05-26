import random
import networkx as nx

OPERATIONS = ["add", "sub", "xor", "and", "or", "sll", "srl"]
CONDITIONS = ["beqz", "bnez", "blt", "bge", "beq", "bne", "bltu", "bgeu"]
REGISTERS = ["t1", "t2", "t3", "t5", "t6"]

def parse_instruction(line: str):
    parts = line.strip().split()

    if parts[0] == 'j':
        return ('j', parts[1])

    if parts[0] == 'li':
        reg = parts[1].strip(',')
        val_str = parts[2]
    
        if val_str.startswith("0x"):
            val = int(val_str, 16)
        else:
            val = int(val_str)
    
        return ('li', (reg, val))

    if parts[0] in OPERATIONS:
        r1 = parts[1].strip(',')
        r2 = parts[2].strip(',')
        r3 = parts[3]
        return ('op', (parts[0], r1, r2, r3))

    if parts[0] in CONDITIONS:
        cond = parts
        if cond[0] in ["beqz", "bnez"]:
            reg = parts[1].strip(",")
            label = parts[2]
            return ('cond', (cond[0], reg, None, label))

        else:
            reg1 = parts[1].strip(",")
            reg2 = parts[2].strip(",")
            label = parts[3]
            return ('cond', (cond[0], reg1, reg2, label))



def find_solution(asm_code: str) -> str:
    def cacl_operations(oper):
        op, r1, r2, r3 = oper
        if op == "add":
            registers[r1] = registers[r2] + registers[r3]
        elif op == "sub":
            registers[r1] = registers[r2] - registers[r3]
        elif op == "or":
            registers[r1] = registers[r2] | registers[r3]
        elif op == "and":
            registers[r1] = registers[r2] & registers[r3]
        elif op == "xor":
            registers[r1] = registers[r2] ^ registers[r3]
        elif op == "sll":
            registers[r1] = registers[r2] << registers[r3]


    def calc_cond(oper):
        cond, r1, r2, node = oper
        v1 = registers[r1] if r1 in registers else 0
        v2 = registers[r2] if r2 and r2 in registers else 0  # для beqz/bnez r2 может быть None

        if cond == "beqz":
            return node if v1 == 0 else None
        elif cond == "bnez":
            return node if v1 != 0 else None
        elif cond == "beq":
            return node if v1 == v2 else None
        elif cond == "bne":
            return node if v1 != v2 else None
        elif cond == "blt":
            return node if v1 < v2 else None
        elif cond == "bge":
            return node if v1 >= v2 else None
        elif cond == "bltu":
            return node if (v1 & 0xFFFFFFFF) < (v2 & 0xFFFFFFFF) else None
        elif cond == "bgeu":
            return node if (v1 & 0xFFFFFFFF) >= (v2 & 0xFFFFFFFF) else None

    last_t3 = 9
    num_of_line = 7
    lines = (asm_code.split('final:')[0]).split('_start:')[1]
    lines = [line.strip() for line in lines.splitlines() if line.strip() and not line.strip().startswith(".")]
    registers = dict()

    for reg in REGISTERS:
        registers[reg] = 0

    for i in range(4):
        reg, val = parse_instruction(lines[i])[1]
        registers[reg] = val

    next_node = None
    curr_node = None

    i = 4
    while next_node != 'final':
        if lines[i].startswith('node'):
            curr_node = lines[i][0:(len(lines[i])-1)]
            i += 1
            continue
        elif (next_node != None) and (curr_node != next_node):
            i += 1
            continue
        else:
            oper = parse_instruction(lines[i])
            if oper[0] == 'li':
                if oper[1][0] == 't3':
                    last_t3 = i + num_of_line
                registers[oper[1][0]] = oper[1][1]

            elif oper[0] == 'op':
                if oper[1][1] == 't3':
                    last_t3 = i + num_of_line
                cacl_operations(oper[1])

            elif oper[0] == 'cond':
                res = calc_cond(oper[1])
                if res:
                    next_node = res

            elif oper[0] == 'j':
                next_node = oper[1]
            i += 1

    return last_t3


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

def init_temp_reg(G, node, k, n):
    if k == 7:
        temp_registers = 'a7'
        k = 0
    else:
        temp_registers = f"a{k}"
        k += 1
    if "init" in G.nodes[node]:
        G.nodes[node]["init"] += f"\n    li {temp_registers}, {n}"
    else:
        G.nodes[node]["init"] = f"li {temp_registers}, {n}"
    return G, k, temp_registers


def add_operations_and_conditions(G):
    # добавляет операции и условия для каждой вершины графа
    T3_FLAG = True
    k = 0

    for node in G.nodes():
        # выбираем операцию
        op = random.choice(OPERATIONS[:-1])
        flag_use_t = 0


        if T3_FLAG:
            target_reg = "t3"
            T3_FLAG = False
        elif random.random() < 0.5:
            target_reg = "t3"
        else:
            target_reg = random.choice([reg for reg in REGISTERS if reg != "t3"])  # Выбираем любой регистр, кроме t3

        source_reg = random.choice(REGISTERS)  # Источник может быть любым регистром
        if source_reg in ["t5", "t6"]:
            init_value = random.randint(0, 0xFFFF)
            G.nodes[node]["init"] = f"li {source_reg}, {init_value}"

        if random.random() < 0.5:
            imm = random.randint(1, 15) if "sll" in op or "srl" in op else random.randint(0, 0xFFFF)
            G, k, imm = init_temp_reg(G, node, k, imm)
        else:
            imm = random.choice(REGISTERS)
            flag_use_t = imm
            if imm in ["t5", "t6"]:
                init_value = random.randint(0, 0xFFFF)
                G.nodes[node]["init"] = f"li {imm}, {init_value}"

        G.nodes[node]["op"] = f"{op} {target_reg}, {source_reg}, {imm}"

        # добавляем условие перехода
        if G.out_degree(node) > 1:
            condition = random.choice(CONDITIONS)
            if condition in ["beqz", "bnez"]:
                G.nodes[node]["condition"] = f"{condition} {target_reg},"
            else:
                num = random.randint(0, 0xFFFF)
                if flag_use_t != 0:
                    choice = random.choice([flag_use_t, num])
                    if not isinstance(choice, str):
                        G, k, choice = init_temp_reg(G, node, k, num)
                    G.nodes[node]["condition"] = f"{condition} {target_reg}, {choice},"
                else:
                    G, k, num = init_temp_reg(G, node, k, num)
                    G.nodes[node]["condition"] = f"{condition} {target_reg}, {num},"
        else:
            G.nodes[node]["condition"] = "j"  # безусловный переход


def generate_code_from_graph(G):
    # генерирует RISC-V код на основе графа
    asm_code = ".data\n"
    asm_code += '    error: .asciz "Access denied!"\n'
    asm_code += '    flag: .asciz "SUCCESS"\n'
    asm_code += ".text\n.globl _start\n_start:\n"

    asm_code += f"    li t1, {hex(random.randint(0, 0xFFFF))}\n"
    asm_code += f"    li t2, {hex(random.randint(0, 0xFFFF))}\n"
    asm_code += f"    li t3, {hex(random.randint(0, 0xFFFF))}\n"
    asm_code += f"    li t4, {0}\n"

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

    # проверка на успех
    return asm_code

def generate_file(file_name, student_id=123456):
    # создаём структуру графа
    G = generate_graph(max_nodes=10, max_depth=5)

    # добавляем операции и условия
    add_operations_and_conditions(G)

    asm_code = generate_code_from_graph(G)

    # сохраняем код в файл
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(asm_code)

def start_gen(n: int, deep: int, student_id: int):
    random.seed(student_id)
    G = generate_graph(max_nodes=n, max_depth=deep)

    # добавляем операции и условия
    add_operations_and_conditions(G)

    asm_code = generate_code_from_graph(G)
    ans = find_solution(asm_code)
    return asm_code, ans