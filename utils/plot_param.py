import numpy as np
import matplotlib.pyplot as plt

# trace redevance, opex, capex, pertes moyennes pour chaque scenario, centrale (obsolete)


def plot_param (CNPE,SCENARIOS,results):
    x = np.arange(len(CNPE))
    width = 0.25

    fig, axes = plt.subplots(4, 1, figsize=(12, 16))

    # CAPEX
    # print(results[CNPE][SCENARIOS])
    for j, scenario in enumerate(SCENARIOS):
        values = [
            results[cnpe][scenario]["CAPEX"]
            for cnpe in CNPE
        ]

        axes[0].bar(
            x + (j - 1) * width,
            values,
            width,
            label=scenario
        )

    axes[0].set_ylabel("CAPEX (M€)")
    axes[0].set_title("CAPEX moyen selon la centrale et le scénario")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(CNPE)
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    # OPEX

    for j, scenario in enumerate(SCENARIOS):

        values = [
            results[cnpe][scenario]["OPEX"]
            for cnpe in CNPE
        ]

        axes[1].bar(
            x + (j - 1) * width,
            values,
            width,
            label=scenario
        )

    axes[1].set_ylabel("OPEX (M€/an)")
    axes[1].set_title("OPEX moyen selon la centrale et le scénario")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(CNPE)
    axes[1].grid(axis="y", alpha=0.3)

    # gain redevance

    for j, scenario in enumerate(SCENARIOS):

        values = [
            results[cnpe][scenario]["REDEVANCE"]
            for cnpe in CNPE
        ]

        axes[2].bar(
            x + (j - 1) * width,
            values,
            width,
            label=scenario
        )

    axes[2].set_ylabel("Gain de redevance (M€/an)")
    axes[2].set_title("Gain de redevance moyen selon la centrale et le scénario")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(CNPE)
    axes[2].grid(axis="y", alpha=0.3)

    # perte de production

    for j, scenario in enumerate(SCENARIOS):

        values = [
            results[cnpe][scenario]["LOSS_PROD"]
            for cnpe in CNPE
        ]

        axes[3].bar(
            x + (j - 1) * width,
            values,
            width,
            label=scenario
        )

    axes[3].set_ylabel("Perte de production (%)")
    axes[3].set_title("Perte de production moyenne selon la centrale et le scénario")
    axes[3].set_xticks(x)
    axes[3].set_xticklabels(CNPE)
    axes[3].grid(axis="y", alpha=0.3)


    plt.tight_layout()
    plt.show()