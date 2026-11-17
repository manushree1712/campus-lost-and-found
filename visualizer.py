from typing import Dict

def generate_charts(summary: Dict, output_file: str = "campus_summary_charts.png") -> bool:
    """Generates a side-by-side category bar chart and status pie chart."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[Visualizer Warning] Matplotlib not installed. Run 'pip install matplotlib' to export charts.")
        return False

    if summary["total"] == 0:
        print("[Visualizer] No records available to plot.")
        return False

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Chart 1: Items by Category
    categories = list(summary["by_category"].keys())
    counts = list(summary["by_category"].values())
    ax1.bar(categories, counts, color="#2b5c8f")
    ax1.set_title("Items Reported by Category")
    ax1.set_ylabel("Count")
    ax1.tick_params(axis="x", rotation=30)

    # Chart 2: Open vs. Claimed Status
    labels = ["Open", "Claimed"]
    sizes = [summary["open"], summary["claimed"]]
    ax2.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["#e07a5f", "#81b29a"], startangle=90)
    ax2.set_title("Resolution Status Breakdown")

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    return True