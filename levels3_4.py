import networkx as nx

def build_multi_level_ff_graph(levels=3, width=3):
    G = nx.DiGraph()

    # Inputs
    for i in range(width):
        G.add_node(f"d{i}", type="input")

    # DFFs per level
    for lvl in range(1, levels + 1):
        for i in range(width):
            ff = f"q{lvl}_{i}"
            G.add_node(ff, type="dff", level=lvl)
            if lvl == 1:
                G.add_edge(f"d{i}", ff)
            else:
                and_node = f"and{lvl - 1}"
                G.add_edge(and_node, ff)

    # AND gates between levels
    for lvl in range(1, levels):
        and_node = f"and{lvl}"
        G.add_node(and_node, type="and", inputs=[f"q{lvl}_{i}" for i in range(width)])
        for i in range(width):
            G.add_edge(f"q{lvl}_{i}", and_node)

    # Outputs
    for i in range(width):
        G.add_node(f"q{i}", type="output")
        G.add_edge(f"q{levels}_{i}", f"q{i}")

    return G


def generate_multi_level_verilog(G, levels=3, width=3):
    codev = []
    inputs = [f"d{i}" for i in range(width)]
    outputs = [f"q{i}" for i in range(width)]
    wires = [n for n in G.nodes if G.nodes[n].get("type") in ["dff", "and"]]

    # Header
    codev.append("module multi_level_ff_chain (")
    codev.append(f"    input clk, {', '.join(inputs)},")
    codev.append(f"    output {', '.join(outputs)}")
    codev.append(");")

    if wires:
        codev.append(f"    wire {', '.join(wires)};")

    # DFFs
    for node in G.nodes:
        if G.nodes[node].get("type") == "dff":
            d_src = list(G.predecessors(node))[0]
            codev.append(f"    dff_spec {node}_inst (.clk(clk), .d({d_src}), .q({node}));")

    # ANDs
    for node in G.nodes:
        if G.nodes[node].get("type") == "and":
            ins = G.nodes[node]["inputs"]
            if len(ins) == 3:
                a, b, c = ins
                codev.append(f"    and_gate_3 {node}_inst (.a({a}), .b({b}), .c({c}), .y({node}));")
            else:
                codev.append(f"    // {node}: Unsupported input count")

    # Output assignments
    for node in G.nodes:
        if G.nodes[node].get("type") == "output":
            src = list(G.predecessors(node))[0]
            codev.append(f"    assign {node} = {src};")

    codev.append("endmodule")
    return "\n".join(codev)

def dff_module():
    return """\
module dff_spec (
    input clk,
    input d,
    output reg q
);
    always @(posedge clk)
        q <= d;

    specify
        (posedge clk => (q : d)) = (3:3:3);
        $setup(d, posedge clk, 2);
        $hold(d, posedge clk, 1);
    endspecify
endmodule
"""

# def and_gate_3_module():
#     return """\
# `celldefine
# module and_gate_3 (
#     input a, b, c,
#     output y
# );
#     assign y = a & b & c;

#     specify
#         (a => y) = (1:1:1);
#         (b => y) = (1:1:1);
#         (c => y) = (1:1:1);
#     endspecify
# endmodule
# `endcelldefine
# """

def generate_and_gate_module(input_count=3):
    assert input_count >= 2, "AND gate needs at least 2 inputs"
    inputs = ", ".join([f"in{i}" for i in range(input_count)])
    delays = "\n    ".join([f"({f'in{i}'} => y) = (1:1:1);" for i in range(input_count)])
    and_expr = " & ".join([f"in{i}" for i in range(input_count)])

    return f"""\
`celldefine
module and_gate_{input_count} (
    input {inputs},
    output y
);
    assign y = {and_expr};

    specify
        {delays}
    endspecify
endmodule
`endcelldefine
"""
def main():
    levels = 3
    width = 3
    G = build_multi_level_ff_graph(levels, width)

    with open("Python_Generated/levels3_4.v", "w") as f:
        f.write("// Auto-generated 3-level FF chain with AND gates\n\n")
        f.write(dff_module())
        f.write("\n\n")
        f.write(generate_and_gate_module(levels))
        f.write("\n\n")
        f.write(generate_multi_level_verilog(G, levels, width))

if __name__ == "__main__":
    main()
