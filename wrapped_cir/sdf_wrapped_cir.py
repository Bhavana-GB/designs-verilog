# def generate_wrapped_sdf(G, sdf_cell="multi_level_circuit", sdf_instance="/uut", timescale="1ns"):
#     codev = []
#     codev.append("(DELAYFILE")
#     codev.append(f"  (SDFVERSION \"3.0\")")
#     codev.append(f"  (TIMESCALE {timescale})")
#     codev.append(f"  (CELL")
#     codev.append(f"    (CELLTYPE \"{sdf_cell}\")")
#     codev.append(f"    (INSTANCE {sdf_instance})")

#     #AND Delays
#     codev.append("    ;; AND gate IOPATH delays")
#     for node, data in G.nodes(data=True):
#         if data["type"] == "and":
#             preds = list(G.predecessors(node))
#             for pred in preds:
#                 codev.append(f"    (DELAY (ABSOLUTE (IOPATH {pred}_q {node}_q (1:1:1))))")

#     # DFF Delays
#     codev.append("    ;; DFF IOPATHs and timing checks")
#     for node, data in G.nodes(data=True):
#         if data["type"] == "dff":
#             codev.append(f"    (DELAY (ABSOLUTE (IOPATH clk {node}_q (2:2:2))))")
#             codev.append(f"    ($SETUP d {node}_q (1))")
#             codev.append(f"    ($HOLD d {node}_q (1))")
     # Interconnect Delays
#     codev.append("    ;; Interconnect delays from graph edges")
#     for u, v, attrs in G.edges(data=True):
#         delay = attrs.get("delay", 0.2)
#         codev.append(f"    (DELAY (ABSOLUTE (INTERCONNECT {u} {v} ({delay}))))")


#     codev.append("  )")
#     codev.append(")")
#     return "\n".join(codev)
