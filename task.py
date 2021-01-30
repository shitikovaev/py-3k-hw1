from sklearn.tree import export_graphviz
# from typing import List
from functools import cmp_to_key
from itertools import permutations


class Node:
    elements: (int, int)


def generate_lists(n: int):
    perms = [list(enumerate(perm)) for perm in list(permutations(range(n)))]
    res = []
    for perm in perms:
        order = []
        res_perm = []
        for item in perm:
            res_perm.append([item[0], item[1], order])
        res.append(res_perm)
    return res


def compare(x: list[int, int, list], y: list[int, int, list]):
    x[2].append((x[0], y[0], x[1] > y[1]))
    return x[1] - y[1]


def main_event(sorting, n: int):
    lists = generate_lists(n)
    results = []
    for l in lists:
        new_l = sorting(l, key=cmp_to_key(compare))
        results.append(new_l[0][2])

    # # tree = DecisionTreeClassifier()
    # tree = tree.fit()
    print(results)
    print()
    return results


def get_name(depth, seq):
    if depth == 0:
        return "depth0_" + str(seq[depth][0]) + "_" + str(seq[depth][1])
    return get_name(depth - 1, seq) + str(seq[depth - 1][2]) + f"_depth{depth}_" + str(seq[depth][0]) + "_" + str(seq[depth][1])


def createTree(lists, n):
    i = 0
    layers = []
    notOver = True
    while i <= n * n and notOver:
        notOver = False
        layer = {}
        for l in lists:
            if len(l) <= i:
                continue
            notOver = True
            name = get_name(i, l)
            if name in layer:
                layer[name]["val"] += 1
            else:
                layer[name] = {"val": 1}
                layer[name]["items"] = (l[i][0], l[i][1])
                if i == 0:
                    layer[name]["parent"] = None
                else:
                    # layer[name]["cond"] = l[i-1][2]
                    layer[name]["parent"] = get_name(i - 1, l)
        layers.append(layer)
        i += 1
    return layers


def export_to_dotfile(layers, n, sorting):
    f = open(f"{sorting.__name__}_{n}.dot", "w")
    f.write("digraph G {\n")
    elements = []
    for layer in layers:
        if not layer:
            continue
        for item in layer.items():
            els = item[1]["items"]
            f.write(f" {item[0]} [label = \"el{els[0]}>el{els[1]}\"];\n")
            parent = item[1]["parent"]
            if parent:
                val = item[1]["val"]
                f.write(f"  {parent}->{item[0]} [label = \"{val}\"];\n")
            #     f.write(
            #         f"\"el{parent[0]}>el{parent[1]}\" -> \"el{item[0][0]}>el{item[0][1]}\" [label = \"{parent[2]}\"];\n")
            # if (item[0][0], item[0][1]) not in elements:
            #     elements.append((item[0][0], item[0][1]))
            #     f.write(f"  \"el{item[0][0]}>el{item[0][1]}\";\n")

    f.write("}")


export_to_dotfile(createTree(main_event(sorted, 3), 3), 3, sorted)
