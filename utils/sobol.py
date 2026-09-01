import numpy as np
import matplotlib.pyplot as plt

from SALib.sample import saltelli
from SALib.analyze import sobol
from param import CNPE_PARAMETERS
from utils.montecarlo_utils import compute_NPV

def calc_sobol(CNPE, scenario):
    
    param = CNPE_PARAMETERS[CNPE]

    capex_min = param["CAPEX_MIN"]
    capex_max = param["CAPEX_MAX"]

    loss_2030_min = param["PERTE_PROD_2030_MIN"]
    loss_2030_max = param["PERTE_PROD_2030_MAX"]

    loss_2050_min = param["PERTE_PROD_2050_MIN"]
    loss_2050_max = param["PERTE_PROD_2050_MAX"]

    power = param["PUISSANCE"]

    # 1 MWh = 3600 MJ
    hours_year = 365 * 24

    # Probleme de Sobol

    if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:
        # OPEX = perte_OPEX × production × FC × prix elec

        opex_min = param["PERTE_OPEX_MIN"]
        opex_max = param["PERTE_OPEX_MAX"]

        problem = {
            "num_vars": 8,

            "names": [
                "Lifetime",
                "CAPEX",
                "Production loss OPEX",
                "Capacity factor",
                "Production loss 2030",
                "Production loss 2050",
                "WACC",
                "Electricity price"
            ],

            "bounds": [
                [min(param["L"]), max(param["L"])],
                [capex_min, capex_max],
                [opex_min, opex_max],
                [0, 1],
                [loss_2030_min, loss_2030_max],
                [loss_2050_min, loss_2050_max],
                [0, 0.1],
                [40, 100]
            ]
        }

    else:

        # OPEX = CAPEX × k_OPEX

        k_opex_min = param["K_OPEX_MIN"]
        k_opex_max = param["K_OPEX_MAX"]

        problem = {
            "num_vars": 7,

            "names": [
                "Lifetime",
                "CAPEX",
                "K_OPEX",
                "Production loss 2030",
                "Production loss 2050",
                "WACC",
                "Electricity price"
            ],

            "bounds": [
                [min(param["L"]), max(param["L"])],
                [capex_min, capex_max],
                [k_opex_min, k_opex_max],
                [loss_2030_min, loss_2030_max],
                [loss_2050_min, loss_2050_max],
                [0, 0.01],
                [40, 100]
            ]
        }
    # échantillonnage par méthode de Saltelli

    param_values = saltelli.sample(problem, 2048,calc_second_order=False)
    Y = np.zeros(len(param_values))

    # VAN

    for i, X in enumerate(param_values):

        lifetime = X[0]
        capex = X[1]

        if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:

            loss_opex = X[2]
            FC = X[3]
            loss_2030 = X[4]
            loss_2050 = X[5]
            wacc = X[6]
            electricity_price = X[7]

            opex = ( loss_opex* (power * hours_year)* FC* electricity_price )

            gain_redevance = (param["TAUX_REDEVANCE_PREL"][scenario] * param["V_PREL_OUVERT"]*1e4+9.1*param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST_OUVERT"])

        else:

            k_opex = X[2]
            loss_2030 = X[3]
            loss_2050 = X[4]
            wacc = X[5]
            electricity_price = X[6]

            opex = capex * k_opex
            gain_redevance = (10* param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST"] )

        # cash flow
        production = power * hours_year
        CF_2030 = (-opex + loss_2030* electricity_price * production+ gain_redevance   )
        CF_2050 = ( -opex + loss_2050 * electricity_price * production + gain_redevance )

        # VAN
        Y[i] = compute_NPV(
            lifetime,
            capex,
            wacc,
            CF_2030,
            CF_2050
        )[0]

    # calcul indices sobol
    Si = sobol.analyze( problem,Y, calc_second_order=False )

    # enregristrement

    print("--------------------------------")
    print(f"Sobol indices - {CNPE} - {scenario}")
    print("--------------------------------")

    for name, s1, st in zip( problem["names"], Si["S1"], Si["ST"]  ):
        print(f"{name:25s}"f"S1={s1:.3f} "f"ST={st:.3f}" )


    plt.figure(figsize=(10, 6))

    x = np.arange(len(problem["names"]))

    plt.bar( x - 0.2, Si["S1"],width=0.4,   label="First order" )
    plt.bar( x + 0.2, Si["ST"], width=0.4, label="Total" )
    plt.xticks( x,problem["names"],  rotation=45, ha="right" )
    plt.ylabel("Sobol index")
    plt.title( f"Sobol sensitivity analysis – {CNPE} – {scenario}")
    plt.legend()
    plt.tight_layout()

    return Si