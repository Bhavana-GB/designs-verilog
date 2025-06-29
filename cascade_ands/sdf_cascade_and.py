def generate_sdf_cascade(G):
    codev = []
    codev.append("(DELAYFILE\n")
    codev.append("    (SDFVERSION \"2.1\")")
    codev.append("    (TIMESCALE 1ns)")
    codev.append("    (DESIGN cascade_and)")
    codev.append("    (DATE \"Generated by Python\")\n")

    for node in G.nodes:
        cell_type = G.nodes[node]["type"]
        if cell_type not in {"dff", "and"}:
            continue

        codev.append(f"    (CELL")
        codev.append(f"        (CELLTYPE \"{cell_type}_spec\")")
        codev.append(f"        (INSTANCE {node})")

        codev.append("        (DELAY")
        if cell_type == "and":
            # Multi-input AND
            num_inputs = int(node.split("_")[-1]) + 1  # e.g., and2_2 → 3-input
            for i in range(num_inputs):
                codev.append(f"            (IOPATH in{i} q (0.3:0.3:0.3))")
        elif cell_type == "dff":
            # DFF has IOPATH d → q and timing checks
            codev.append("            (IOPATH clk q (0.5:0.5:0.5))")
        codev.append("        )")

        # Timing Check Block for DFFs
        if cell_type == "dff":
            codev.append("        (TIMINGCHECK")
            codev.append("            (SETUP d (posedge clk) (0.2:0.2:0.2))")
            codev.append("            (HOLD d (posedge clk) (0.1:0.1:0.1))")
            codev.append("            (WIDTH (posedge clk) (1.0:1.0:1.0))")
            codev.append("        )")

        codev.append("    )\n")

    # INTERCONNECTS — from graph edges
    codev.append("    (INTERCONNECT")
    for u, v, attr in G.edges(data=True):
        delay = attr.get("delay", 0.2)
        codev.append(f"        (INTERCONNECT {u}* → {v}* ({delay}:{delay}:{delay}))")
    codev.append("    )")

    codev.append(")")
    return "\n".join(codev)
