import networkx as nx
from tb_cascade_and import generate_tb_cascade
# from sdf_cascade_and import generate_sdf_cascade

def build_graph(levels, rows):
    G = nx.DiGraph()

    # Level 1 FFs
    for i in range(rows):
        d = f"d{i}"
        ff = f"q1_{i}"
        G.add_node(d, type="input")
        G.add_node(ff, type="dff")
        G.add_edge(d, ff, delay=2)

    # Intermediate levels with AND gates
    for lvl in range(1, levels):
        for i in range(rows):
            and_gate = f"and{lvl}_{i}"
            next_ff = f"q{lvl+1}_{i}"
            G.add_node(and_gate, type="and")
            G.add_node(next_ff, type="dff")

            for j in range(i + 1):
                src = f"q{lvl}_{j}"
                G.add_edge(src, and_gate, delay=2)

            G.add_edge(and_gate, next_ff, delay=3)

    # Outputs
    for i in range(rows):
        G.add_node(f"q{i}", type="output")
        G.add_edge(f"q{levels}_{i}", f"q{i}")
    return G

def generate_v_cascade(G, levels, rows, module_name="cascade_and"):
    codev = []

    inputs = [f"d{i}" for i in range(rows)]
    outputs = [f"q{i}" for i in range(rows)]

    codev.append(f"module {module_name} (")
    codev.append(f"    input clk,")
    codev.append(f"    input {', '.join(inputs)},")
    codev.append(f"    output {', '.join(outputs)}")
    codev.append(");")

    # Wire declarations
    for lvl in range(1, levels + 1):
        wires = [f"q{lvl}_{i}" for i in range(rows)]
        codev.append(f"    wire {', '.join(wires)};")
    for lvl in range(1, levels):
        wires = [f"and{lvl}_{i}" for i in range(rows)]
        codev.append(f"    wire {', '.join(wires)};")

    # FF instantiations
    for lvl in range(1, levels + 1):
        for i in range(rows):
            # ff = f"ff{lvl}_{i}"
            ff = f"q{lvl}_{i}"
            preds = list(G.predecessors(ff))
            if preds:
                src = preds[0]
                d_src = f"{src}_q" if G.nodes[src]["type"] in {"dff", "and"} else src
            else:
                d_src = "1'b0"
            codev.append(f"    dff_spec {ff} (.clk(clk), .d({d_src}), .q({ff}));")

    # AND gate instantiations
    for lvl in range(1, levels):
        for i in range(rows):
            and_gate = f"and{lvl}_{i}"
            in_ports = [f".in{j}(ff{lvl}_{j}_q)" for j in range(i + 1)]
            port_str = ", ".join(in_ports) + f", .q({and_gate}_q)"
            codev.append(f"    and_spec #{i+1} {and_gate} ({port_str});")

    # Output assignments
    for i in range(rows):
        codev.append(f"    assign q{i} = q{levels}_{i};")

    codev.append("endmodule")
    return "\n".join(codev)

def main():

    levels = int(input("Enter number of levels: "))
    rows = int(input("Enter number of FFs per level (rows): "))

    G = build_graph(levels, rows)
    verilog_code = generate_v_cascade(G, levels, rows)
    test_bench_code = generate_tb_cascade( rows)
    # sdf_code = generate_sdf_cascade(G)

    with open("cascade_and.v", "w") as f:
        f.write(verilog_code)
    print(f"\n Verilog code written to cascade_and.v")
    
    with open("tb_cascade_and.v", "w") as f:
        f.write(test_bench_code)
    print(f"Testbench written to tb_cascade_and.v")

    # with open("sdf+cascade_and.v", "w") as f:
    #     f.write(sdf_code)
    # print(f"SDF file written to sdf+cascade_and.v")


if __name__ == "__main__":
    main()
