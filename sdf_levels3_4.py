def generate_sdf(G, sdf_cell="multi_level_circuit", sdf_instance="/uut", timescale="1ns"):
    codev = []
    codev.append("(DELAYFILE")
    codev.append(f"  (SDFVERSION \"3.0\")")
    codev.append(f"  (TIMESCALE {timescale})")
    codev.append(f"  (CELL")
    codev.append(f"    (CELLTYPE \"{sdf_cell}\")")
    codev.append(f"    (INSTANCE {sdf_instance})")

    # Interconnect Delays 
    codev.append("    ;; Interconnect delays")
    for u, v, attrs in G.edges(data=True):
        delay = attrs.get("delay", 0.2)
        codev.append(f"    (DELAY (ABSOLUTE (IOPATH {u} {v} ({delay}:{delay}:{delay}))))")

    # Gate Delays 
    codev.append("    ;; Gate-level delays (from specify blocks)")

    for node, attrs in G.nodes(data=True):
        ntype = attrs["type"]

        if ntype == "and":
            preds = list(G.predecessors(node))
            for p in preds:
                codev.append(f"    (DELAY (ABSOLUTE (IOPATH {p}_q {node}_q (0.7:0.7:0.7))))")

        elif ntype == "dff":
            codev.append(f"    (DELAY (ABSOLUTE (IOPATH clk {node}_q (1.5:1.5:1.5))))")
            codev.append(f"    ($SETUP d {node}_q (1.0))")
            codev.append(f"    ($HOLD d {node}_q (0.3))")

    codev.append("  )")
    codev.append(")")
    return "\n".join(codev)



with open("multi_level_circuit.sdf", "w") as f:
    f.write(generate_sdf(G))
