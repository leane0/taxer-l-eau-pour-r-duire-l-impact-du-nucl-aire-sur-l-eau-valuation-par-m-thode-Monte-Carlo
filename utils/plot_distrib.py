import os
import pickle
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PARAMETRES
# ============================================================

RESULTS_DIR = "results"

SCENARIOS = [
    "S_REF",
    "S_HARM",
    "S_RENF",
    "S_RENF_FORT"
]

GROUP_1 = [
    "Tricastin",
    "Bugey",
    "Saint-Alban"
]

GROUP_2 = [
    "Golfech",
    "Nogent"
]

SCENARIOS_NOGENT=[
    "S_REF",
    "S_RENF_FORT",
    "S_1",
    "S_2"
]


# ============================================================
# CHARGEMENT
# ============================================================

def load_results(CNPE, scenario):

    filepath = os.path.join(
        RESULTS_DIR,
        CNPE,
        scenario,
        "monte_carlo_results.pkl"
    )

    with open(filepath, "rb") as f:
        return pickle.load(f)


# ============================================================
# FONCTION DE REPARTITION EMPIRIQUE
# ============================================================

def empirical_cdf(data):

    x = np.sort(data)

    n = len(x)

    F = np.arange(1, n + 1) / n

    return x, F


# ============================================================
# PLOT CDF
# ============================================================

def plot_cdf(cnpe_group, scenario, variable):

    plt.figure(figsize=(8, 5))

    for CNPE in cnpe_group:

        try:
            data = load_results(CNPE, scenario)

        except FileNotFoundError:
            print(
                f"Fichier introuvable : "
                f"{CNPE} / {scenario}"
            )
            continue

        # ----------------------------------------------------
        # Récupération de la variable
        # ----------------------------------------------------

        values = np.asarray(data[variable])

        # ----------------------------------------------------
        # Conversion des unités
        # ----------------------------------------------------

        if variable == "NPV":

            # €
            values = values / 1e6

            xlabel = "NPV (M€)"

        elif variable == "ROI":

            # fraction -> %
            values = values * 100

            xlabel = "ROI (%)"

        else:

            raise ValueError(
                "variable doit être 'NPV' ou 'ROI'"
            )

        # ----------------------------------------------------
        # CDF
        # ----------------------------------------------------

        x, F = empirical_cdf(values)
        plt.plot(
            x,
            F,
            label=CNPE
        )

    # --------------------------------------------------------
    # Ligne x = 0
    # --------------------------------------------------------

    plt.axvline(
        x=0,
        linestyle="--",
        linewidth=1
    )

    # Médiane
    plt.axhline(
        y=0.5,
        linestyle=":",
        linewidth=1
    )

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    plt.xlabel(xlabel)

    plt.ylabel(
        f"P({xlabel.split()[0]} ≤ x)"
    )

    plt.title(
        f"Empirical CDF of {variable} — {scenario}"
    )

    plt.ylim(0, 1)

    plt.grid(
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    # --------------------------------------------------------
    # SAUVEGARDE
    # --------------------------------------------------------

    output_dir = os.path.join(
        RESULTS_DIR,
        "CDF"
    )

    os.makedirs(output_dir, exist_ok=True)

    group_name = "_".join(cnpe_group)

    filepath = os.path.join(
        output_dir,
        f"CDF_{variable}_{scenario}_{group_name}.png"
    )

    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches="tight"
    )

    #plt.show()
    plt.close()

    print(f"Figure saved : {filepath}")


# ============================================================
# GENERATION DE TOUTES LES FIGURES
# ============================================================

for scenario in ["S_THER_1","S_THER_2"]:
    
    print("\n========================================")
    print(f"Scenario : {scenario}")
    print("========================================")

    plot_cdf( GROUP_1, scenario, "NPV")
    plot_cdf( GROUP_2, scenario, "NPV")

    plot_cdf( GROUP_1, scenario, "ROI" )

    plot_cdf(GROUP_2, scenario, "ROI")


def plot_cdf_nogent( scenarios, variable):
    
    plt.figure(figsize=(8, 5))
    CNPE="Nogent"

    for scenario in scenarios:

        try:
            data = load_results(CNPE, scenario)

        except FileNotFoundError:
            print(
                f"Fichier introuvable : "
                f"{CNPE} / {scenario}"
            )
            continue

        values = np.asarray(data[variable])

        if variable == "NPV":
            # €
            values = values / 1e6
            xlabel = "NPV (M€)"

        elif variable == "ROI":
            # fraction -> %
            values = values * 100
            xlabel = "ROI (%)"

        else:
            raise ValueError(
                "variable doit être 'NPV' ou 'ROI'"
            )
        # ----------------------------------------------------
        # CDF
        # ----------------------------------------------------

        x, F = empirical_cdf(values)
        label={"S_REF":"Scénario de référence","S_RENF_FORT":"Redevance thermique x10 (reforcement 2)","S_1":"Redevance thermique x 100","S_2":"Redevance thermique x 1000"}

        plt.plot(
            x,
            F,
            label=label[scenario]
        )

    # --------------------------------------------------------
    # Ligne x = 0
    # --------------------------------------------------------

    plt.axvline(
        x=0,
        linestyle="--",
        linewidth=1
    )

    # Médiane
    plt.axhline(
        y=0.5,
        linestyle=":",
        linewidth=1
    )

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    plt.xlabel(xlabel)

    plt.ylabel(
        f"P({xlabel.split()[0]} ≤ x)"
    )

    plt.title(
        f"Empirical CDF of {variable} — {scenario}"
    )

    plt.ylim(0, 1)

    plt.grid(
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    # --------------------------------------------------------
    # SAUVEGARDE
    # --------------------------------------------------------

    output_dir = os.path.join(
        RESULTS_DIR,
        "CDF"
    )

    os.makedirs(output_dir, exist_ok=True)

    group_name = "_".join(["Nogent"])

    filepath = os.path.join(
        output_dir,
        f"CDF_{variable}_{CNPE}.png"
    )

    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches="tight"
    )

    #plt.show()
    plt.close()

    print(f"Figure saved : {filepath}")



#plot_cdf_nogent( SCENARIOS_NOGENT, "NPV")
#plot_cdf_nogent( SCENARIOS_NOGENT, "ROI" )