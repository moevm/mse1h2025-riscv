import random
import networkx as nx
import matplotlib.pyplot as plt
import math

# -------------------------------------------------
n = 7  # количество функций
deep = 0.6  # глубина основного пути (0.3–0.9)
# -------------------------------------------------

a4_val = random.randint(5, 15) # в идеале эти значения должны рассчитываться на основе id студента но пока так
a5_val = random.randint(2, 10)
a6_val = random.randint(10, 30)

step1 = a4_val + a5_val
step2 = a6_val // a5_val
final_flag = step1 + step2  # будет в a5

# Генерация связного графа
G = nx.DiGraph()
vertices = list(range(n))
G.add_nodes_from(vertices)

min_path_len = max(3, int(n * deep))
main_path = random.sample(vertices, min_path_len)
for i in range(len(main_path) - 1):
    G.add_edge(main_path[i], main_path[i + 1], color='black')
print(main_path)
used = set(main_path)
free = [v for v in vertices if v not in used]
print(free)
for v in free:
    u = random.choice(main_path[:-1])
    G.add_edge(u, v, color='red')

#поиск последней функции
final_func = 0
for v in range(1, len(main_path)):
    if not G.adj[main_path[v-1]]:
        continue
    temp = max(G.adj[main_path[v-1]])
    temp2 = main_path[v]
    if max(G.adj[main_path[v-1]]) > main_path[v]:
        final_func = max(final_func, max(G.adj[main_path[v-1]]))
        break



remaining_funcs = [v for v in vertices if v != final_func]
op_funcs_sample = random.sample(remaining_funcs, 2)

ops_map = {
    op_funcs_sample[0]: '\tadd a4, a4, a5',
    op_funcs_sample[1]: '\tdiv a6, a6, a5',
    final_func:         '\tadd a5, a4, a6'  # всегда в последней
}


def gen_noise():
    regs = ['a1', 'a2', 'a3']
    ops = ['add', 'sub', 'xor', 'or', 'and', 'mul']
    lines = []
    for _ in range(random.randint(1, 3)):
        dst = random.choice(regs)
        r1 = random.choice(regs)
        r2 = random.choice(regs)
        op = random.choice(ops)
        lines.append(f'\t{op} {dst}, {r1}, {r2}')
    return lines

def gen_func(idx, neighbors):
    lines = [f'func_{idx}:']
    lines += gen_noise()

    if idx in ops_map:
        lines.append(ops_map[idx])

    for n in neighbors:
        lines += [
            '\taddi sp, sp, -4',
            '\tsw ra, 0(sp)',
            f'\tcall func_{n}',
            '\tlw ra, 0(sp)',
            '\taddi sp, sp, 4'
        ]
    lines.append('\tret\n')
    return lines

#a1, a2, a3 - будут рандомными
#От самой начальной программы требуется только задать a1 - a6 регистры и вызвать начальуню функцию
# это пока для тестов
asm_code = f"""
.global _start

_start:
\tli a1, 5  
\tli a2, 10 
\tli a3, 15   
\tli a4, {a4_val}
\tli a5, {a5_val}
\tli a6, {a6_val}
\tcall func_{main_path[0]}
\t# Флаг находится в a5
\tli a0, 0        
\tli a7, 93       
\tecall   
"""

visited = set()
stack = [main_path[0]]
while stack:
    v = stack.pop()
    if v in visited:
        continue
    visited.add(v)
    u = dict(sorted(G.adj[v].items()))
    stack.extend(u)
    asm_code += '\n'.join(gen_func(v, u)) + '\n'



print(f"Флаг (в a5): {final_flag}")
print(f"Начальные значения: a4 = {a4_val}, a5 = {a5_val}, a6 = {a6_val}")
print(f"Инструкции распределены по функциям: {op_funcs_sample}")
print("Ассемблер сохранён в: generated_program.s")

with open("generated_program.s", "w") as f:
    f.write(asm_code)


# plt.figure(figsize=(8, 6))
# edge_colors = [G[u][v]['color'] for u, v in G.edges()]
# nx.draw(G, with_labels=True, node_color="lightblue", edge_color=edge_colors)
# plt.title("Граф вызовов функций")
# plt.show()


