import numpy as np
import matplotlib.pyplot as plt

from param import CNPE_PARAMETERS
from utils.montecarlo_utils import *

def tornado_plot(NPV_results, CNPE, scenario):
    
    param = CNPE_PARAMETERS[CNPE]

    capex_bounds = [param["CAPEX_MIN"],param["CAPEX_MAX"]]
    lifetime_bounds = [ min(param["L"]), max(param["L"]) ]
    loss_2030_bounds = [param["PERTE_PROD_2030_MIN"], param["PERTE_PROD_2030_MAX"] ]
    loss_2050_bounds = [ param["PERTE_PROD_2050_MIN"], param["PERTE_PROD_2050_MAX"]]
    power = param["PUISSANCE"]

    if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:

        # OPEX  = loss_opex × puissance × heures × FC × prix elec
        loss_opex_bounds = [param["PERTE_OPEX_MIN"],param["PERTE_OPEX_MAX"]]

        # FC ~ Beta(alpha, beta):on utilise  les bornes théoriques[0,1]
        FC_bounds = [0, 1]

        # Redevance
        taux_redevance = param["TAUX_REDEVANCE_Q"][scenario]
        V_REST = param["V_REST_OUVERT"]

        variables = {
            "Lifetime": ("lifetime", lifetime_bounds),
            "CAPEX": ("capex", capex_bounds),
            "OPEX loss": ("loss_opex", loss_opex_bounds),
            "Capacity factor": ("FC", FC_bounds),
            "Production loss 2030": (
                "loss_2030",
                loss_2030_bounds
            ),
            "Production loss 2050": (
                "loss_2050",
                loss_2050_bounds
            ),
            "Electricity price": (
                "electricity_price",
                [45, 120]
            ),
            "WACC": (
                "wacc",
                [0, 0.07]
            )
        }

    # golfech et nogent
    else:
        # OPEX = CAPEX × k
        k_opex_bounds = [
            param["K_OPEX_MIN"],
            param["K_OPEX_MAX"]
        ]

        variables = {
            "Lifetime": ("lifetime", lifetime_bounds),
            "CAPEX": ("capex", capex_bounds),
            "OPEX coefficient": (
                "k_opex",
                k_opex_bounds
            ),
            "Production loss 2030": (
                "loss_2030",
                loss_2030_bounds
            ),
            "Production loss 2050": (
                "loss_2050",
                loss_2050_bounds
            ),
            "Electricity price": (
                "electricity_price",
                [45, 120]
            ),
            "WACC": (
                "wacc",
                [0, 0.07]
            )
        }

    # valeurs de référence

    base = {
        "lifetime": np.mean(param["L"]),
        "capex": param["CAPEX_MODE"],
        "loss_2030": param["PERTE_PROD_2030_MODE"],
        "loss_2050": param["PERTE_PROD_2050_MODE"],
        "electricity_price": 70,
        "wacc": 0.06,
        "power": power,
        "scenario": scenario,
        "CNPE": CNPE
    }

    # Paramètres spécifiques
    if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:
        base["loss_opex"] = param["PERTE_OPEX_MODE"]
        # Pour une Beta, valeur moyenne = alpha/(alpha+beta)
        base["FC"] = (
            param["FC_ALPHA"]
            / (param["FC_ALPHA"] + param["FC_BETA"])
        )
    else:
        base["k_opex"] = param["K_OPEX_MODE"]

    # effets (calcul VAN sur les bornes)

    effects = []

    for name, (key, bounds) in variables.items():

        low_param = base.copy()
        high_param = base.copy()

        low_param[key] = bounds[0]
        high_param[key] = bounds[1]

        npv_low = npv_dict(low_param)
        npv_high = npv_dict(high_param)

        effects.append([
            name,
            npv_low,
            npv_high,
            abs(npv_high - npv_low)
        ])


    # Tri
    effects.sort(key=lambda x: x[3], reverse=True)
    labels = [e[0] for e in effects]
    npv_low = [e[1] / 1e6 for e in effects]
    npv_high = [e[2] / 1e6 for e in effects]
    y = np.arange(len(labels))
    plt.figure(figsize=(9,7))

    # Barres
    plt.hlines(
        y,
        np.minimum(npv_low, npv_high),
        np.maximum(npv_low, npv_high),
        linewidth=8
    )

    # Points des min/max
    plt.scatter(npv_low, y, zorder=3, label="Valeur min du paramètre")
    plt.scatter(npv_high, y, zorder=3, label="Valeur max du paramètre")

    # rentabilité
    plt.axvline(
        0,
        linestyle="-",
        linewidth=1,
        label="VAN = 0"
    )

    # VAN de référence
    npv_mean = np.mean(NPV_results)

    plt.axvline(
        npv_mean / 1e6,
        linestyle="--",
        label="VAN moyenne")

    plt.yticks(y, labels)
    plt.xlabel("VAN (M€)")
    plt.ylabel("Variable")
    plt.title(
        f"Tornado plot – sensibilité de la VAN\n"
        f"{CNPE} – scénario {scenario}"
    )

    plt.legend()
    plt.tight_layout()