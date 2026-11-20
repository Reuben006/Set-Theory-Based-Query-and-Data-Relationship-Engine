import base64
from io import BytesIO

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib_venn import venn2


OPERATION_LABELS = {
    "union": "Union: A ∪ B",
    "intersection": "Intersection: A ∩ B",
    "difference": "Difference: A − B",
    "symmetric_difference": "Symmetric difference: A △ B",
}

SET_A_COLOR = "#0969da"
SET_B_COLOR = "#e36209"
INTERSECTION_COLOR = "#8e44ad"
NEUTRAL_COLOR = "#eaeef2"


def make_venn_diagram(list_a, list_b, operation):
    set_a, set_b = set(list_a), set(list_b)
    counts = (len(set_a - set_b), len(set_b - set_a), len(set_a & set_b))
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="white")
    diagram = venn2(subsets=counts, set_labels=("Set A", "Set B"), ax=ax)

    selected_regions = {
        "union": {"10", "01", "11"},
        "intersection": {"11"},
        "difference": {"10"},
        "symmetric_difference": {"10", "01"},
    }.get(operation, set())
    region_colors = {"10": SET_A_COLOR, "01": SET_B_COLOR, "11": INTERSECTION_COLOR}
    for region_id in ("10", "01", "11"):
        patch = diagram.get_patch_by_id(region_id)
        if patch is not None:
            patch.set_color(region_colors[region_id] if region_id in selected_regions else NEUTRAL_COLOR)
            patch.set_alpha(0.82 if region_id in selected_regions else 0.5)
            patch.set_edgecolor("#24292f")
    for label in diagram.set_labels:
        if label is not None:
            label.set_color("#24292f")
            label.set_fontsize(11)
    for label in diagram.subset_labels:
        if label is not None:
            label.set_color("#24292f")
            label.set_fontsize(10)

    ax.set_title(OPERATION_LABELS.get(operation, "Set operation"), color="#24292f", fontsize=13, pad=14)
    ax.set_axis_off()
    fig.tight_layout()
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    image = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{image}"
