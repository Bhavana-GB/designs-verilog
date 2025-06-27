import networkx as nx

def build_basic_logic_graph():
    G = nx.DiGraph()

    # Pins (Inputs)
    G.add_node("a", type="input")
    G.add_node("b", type="input")
    G.add_node("c", type="input")

    # AND Gate
    G.add_node("and1", type="and", inputs=["a", "b"])
    G.add_edge("a", "and1")
    G.add_edge("b", "and1")

    # OR Gate
    G.add_node("or1", type="or", inputs=["and1", "c"])
    G.add_edge("and1", "or1")
    G.add_edge("c", "or1")

    # Output pin
    G.add_node("y", type="output")
    G.add_edge("or1", "y")

    return G

def generate_logic_verilog(G):
    codev = []
    inputs = [n for n in G.nodes if G.nodes[n].get("type") == "input"]
    outputs = [n for n in G.nodes if G.nodes[n].get("type") == "output"]
    wires = [n for n in G.nodes if G.nodes[n].get("type") in ["and", "or"]]

    # Header
    codev.append("module logic_gate_test (")
    codev.append(f"    input {', '.join(inputs)},")
    codev.append(f"    output {', '.join(outputs)}")
    codev.append(");")

    # Wire declarations
    if wires:
        codev.append(f"    wire {', '.join(wires)};")

    # AND gate
    for node in G.nodes:
        if G.nodes[node].get("type") == "and":
            a, b = G.nodes[node]["inputs"]
            codev.append(f"    and_gate_2 {node}_inst (.a({a}), .b({b}), .y({node}));")

    # OR gate
    for node in G.nodes:
        if G.nodes[node].get("type") == "or":
            a, b = G.nodes[node]["inputs"]
            codev.append(f"    or_gate_2 {node}_inst (.a({a}), .b({b}), .y({node}));")
    
     # Output assignments
    for node in G.nodes:
        if G.nodes[node].get("type") == "output":
            src = list(G.predecessors(node))[0]
            codev.append(f"    assign {node} = {src};")

    codev.append("endmodule")
    return "\n".join(codev)


def generate_celldefine_and2():
    return """\
`celldefine
module and_gate_2 (
    input a, b,
    output y
);
    assign y = a & b;

    specify
        (a => y) = (1:1:1);
        (b => y) = (1:1:1);
    endspecify
endmodule
`endcelldefine
"""

def generate_celldefine_or2():
    return """\
`celldefine
module or_gate_2 (
    input a, b,
    output y
);
    assign y = a | b;

    specify
        (a => y) = (1:1:1);
        (b => y) = (1:1:1);
    endspecify
endmodule
`endcelldefine
"""

def main():
    G = build_basic_logic_graph()

    with open("Python_Generated/basic_cir.v", "w") as f:
        f.write("// Auto-generated logic circuit: AND followed by OR\n\n")
        f.write(generate_celldefine_and2())
        f.write("\n\n")
        f.write(generate_celldefine_or2())
        f.write("\n\n")
        f.write(generate_logic_verilog(G))

if __name__ == "__main__":
    main()
