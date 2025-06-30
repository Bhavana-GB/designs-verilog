import networkx as nx
from tb_wrapped_cir import generate_wrapped_testbench
# from sdf_wrapped_cir import generate_wrapped_sdf

def build_graph(levels=3, width=3):
    G = nx.DiGraph()

    # Add input pins
    for i in range(width):
        G.add_node(f"d{i}", type="input")

    # Add DFFs and wiring
    for lvl in range(1, levels + 1):
        for i in range(width):
            ff = f"q{lvl}_{i}"
            G.add_node(ff, type="dff", level=lvl)
            if lvl == 1:
                G.add_edge(f"d{i}", ff)

    # Add AND gates between levels
    for lvl in range(1, levels):
        for i in range(width):
            a_idx = i
            b_idx = (i + 1) % width
            and_name = f"and{lvl}_{i}"
            G.add_node(and_name, type="and", inputs=[f"q{lvl}_{a_idx}", f"q{lvl}_{b_idx}"])

            # Connect inputs to AND
            G.add_edge(f"q{lvl}_{a_idx}", and_name)
            G.add_edge(f"q{lvl}_{b_idx}", and_name)

            # Connect AND output to next level FF
            G.add_edge(and_name, f"q{lvl+1}_{i}")

    # Add output pins
    for i in range(width):
        G.add_node(f"q{i}", type="output")
        G.add_edge(f"q{levels}_{i}", f"q{i}")

    return G

def generate_v_wrapped(G, levels=3, width=3):
    codev = []
    inputs = [f"d{i}" for i in range(width)]
    outputs = [f"q{i}" for i in range(width)]
    wires = [n for n in G.nodes if G.nodes[n].get("type") in ["dff", "and"]]

    codev.append("module wrapped_and_circuit (")
    codev.append(f"    input clk, {', '.join(inputs)},")
    codev.append(f"    output {', '.join(outputs)}")
    codev.append(");")

    if wires:
        codev.append(f"    wire {', '.join(wires)};")

    # DFF
    for node in G.nodes:
        if G.nodes[node].get("type") == "dff":
            d_src = list(G.predecessors(node))[0]
            codev.append(f"    dff_spec {node}_inst (.clk(clk), .d({d_src}), .q({node}));")

    # AND gates (2 inputs)
    for node in G.nodes:
        if G.nodes[node].get("type") == "and":
            a, b = G.nodes[node]["inputs"]
            codev.append(f"    and_gate_2 {node}_inst (.a({a}), .b({b}), .y({node}));")

    # Output assigns
    for node in G.nodes:
        if G.nodes[node].get("type") == "output":
            src = list(G.predecessors(node))[0]
            codev.append(f"    assign {node} = {src};")

    codev.append("endmodule")
    return "\n".join(codev)

def and_gate_2_module():
    return """\
`celldefine
module and_gate_2 (
    input a, b,
    output y
);
    assign y = a & b;
    specify
        (a => y) = 1;
        (b => y) = 1;
    endspecify
endmodule
`endcelldefine
"""

def dff_spec_module():
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

def main():
    # levels = 3
    # width = 3
    levels = int(input("Enter number of levels: "))
    width = int(input("Enter number of FFs per level (rows): "))

    G = build_graph(levels, width)

    with open("wrapped_cir.v", "w") as f:
        f.write("//Python Generated\n")
        f.write(dff_spec_module())
        f.write("\n")
        f.write(and_gate_2_module())
        f.write("\n")
        f.write(generate_v_wrapped(G, levels, width))
        print("Output written to wrapped_cir.v")
    
    tb_code = generate_wrapped_testbench(G)
    with open("tb_wrapped_cir.v",'w') as f :
        f.write("//Python Generated\n")
        f.write(tb_code)
        print("Output written to tb_wrapped_cir.v")

    sdf_code = generate_wrapped_testbench(G)
    with open("tb_wrapped_cir.v",'w') as f :
        f.write("//Python Generated\n")
        f.write(tb_code)
        print("Output written to tb_wrapped_cir.v")
if __name__ == "__main__":
    main()
