import numpy as np
import matplotlib.pyplot as plt

from SALib.sample import saltelli
from SALib.analyze import sobol
from param import CNPE_PARAMETERS

def calc_base (capex_param,opex_param,loss_param,power,hours_year,redevance):
    _,capex_mode,_ = capex_param
    _,opex_mode,_ = opex_param
    _,loss_mode,_ = loss_param
    return {"lifetime":20,
            "power" : power,
            "hours_year":hours_year,
            "capex":capex_mode,
            "opex":opex_mode, 
            "loss":loss_mode,
            "wacc":0.04,
            "electricity_price":70,
            "redevance":redevance
            }

def compute_NPV(
    lifetime,
    capex,
    wacc,
    CF_2030,
    CF_2050,
):

    discounted_cashflows = 0

    for year in range(1,int(lifetime)+1):
        if year <= 10 : discounted_cashflows += ( CF_2030 /(1+wacc)**year)
        else : discounted_cashflows += ( CF_2050 /(1+wacc)**year)

    NPV = (-capex + discounted_cashflows)
    ROI = ( discounted_cashflows-capex ) / capex

    return NPV, ROI

def npv_dict(d):
    
    CNPE = d["CNPE"]
    scenario = d["scenario"]

    param = CNPE_PARAMETERS[CNPE]

    lifetime = d["lifetime"]
    capex = d["capex"]
    loss_2030 = d["loss_2030"]
    loss_2050 = d["loss_2050"]
    electricity_price = d["electricity_price"]
    wacc = d["wacc"]
    power = d["power"]

    # CALCUL DE L'OPEX

    if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:
        loss_opex = d["loss_opex"]
        FC = d["FC"]
        opex = (loss_opex* (power * 365 * 24 * 3600)* FC* electricity_price)
        gain_redevance = (9.1* param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST_OUVERT"])

    else:
        k = d["k_opex"]
        opex = capex * k
        gain_redevance = ( 5* param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST"])

    # FLUX DE TRÉSORERIE 2030 ET 2050

    production = power * 365 * 24 * 3600
    CF_2030 = (-opex + loss_2030 * electricity_price * production + gain_redevance)
    CF_2050 = ( -opex + loss_2050 * electricity_price * production+ gain_redevance )

    # VAN

    npv = -capex
    for t in range(1, int(lifetime) + 1):
        if t < lifetime / 2:
            CF = CF_2030
        else:
            CF = CF_2050
        npv += CF / (1 + wacc) ** t

    return npv

def tornado_plot(NPV_results, CNPE, scenario):
    
    param = CNPE_PARAMETERS[CNPE]

    # 1. PARAMÈTRES COMMUNS

    capex_bounds = [param["CAPEX_MIN"],param["CAPEX_MAX"]]
    lifetime_bounds = [ min(param["L"]), max(param["L"]) ]
    loss_2030_bounds = [param["PERTE_PROD_2030_MIN"], param["PERTE_PROD_2030_MAX"] ]
    loss_2050_bounds = [ param["PERTE_PROD_2050_MIN"], param["PERTE_PROD_2050_MAX"]]
    power = param["PUISSANCE"]

    # 2. PARAMÈTRES SPÉCIFIQUES AU CNPE

    if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:

        # OPEX dépend de loss_opex × puissance × heures × FC × prix électricité
        loss_opex_bounds = [param["PERTE_OPEX_MIN"],param["PERTE_OPEX_MAX"]]

        # FC ~ Beta(alpha, beta):on utilise  les bornes théoriques[0,1].
        FC_bounds = [0, 1]

        # Redevance
        taux_redevance = param["TAUX_REDEVANCE_Q"][scenario]
        V_REST = param["V_REST_OUVERT"]

        # Variables spécifiques
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

    # 3. GOLFECH / NOGENT

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

    # 4. VALEURS DE BASE

    base = {
        "lifetime": np.mean(param["L"]),
        "capex": param["CAPEX_MODE"],
        "loss_2030": param["PERTE_PROD_2030_MODE"],
        "loss_2050": param["PERTE_PROD_2050_MODE"],
        "electricity_price": 70,
        "wacc": 0.04,
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

    # 5. CALCUL DES EFFETS

    effects = []
    for name, (key, bounds) in variables.items():
        low = base.copy()
        high = base.copy()
        low[key] = bounds[0]
        high[key] = bounds[1]
        # Calcul NPV
        npv_low = npv_dict(low)
        npv_high = npv_dict(high)

        effects.append([name, npv_low, npv_high, abs(npv_high - npv_low)])

    # 6. TRI DES VARIABLES

    effects.sort(key=lambda x: x[3], reverse=True)
    labels = []
    low = []
    high = []

    for effect in effects:
        labels.append(effect[0])
        low.append(effect[1] / 1e6 )
        high.append( effect[2] / 1e6 )

    # 7. TORNADO PLOT

    y = np.arange(len(labels))
    plt.figure(figsize=(9, 7))
    plt.hlines(y, low, high, linewidth=8 )

    plt.plot(low, y, "o" )

    plt.plot( high, y, "o" )

    plt.yticks( y, labels )

    # NPV moyenne Monte Carlo
    plt.axvline( np.mean(NPV_results) / 1e6,linestyle="--",label="NPV moyenne")

    plt.xlabel("NPV (M€)")
    plt.ylabel("Variable")
    plt.title(f"Tornado plot – sensibilité de la NPV\n" f"{CNPE} – scénario {scenario}")

    plt.legend()
    plt.tight_layout()
    plt.show()
def calc_sobol(CNPE, scenario):
    
    param = CNPE_PARAMETERS[CNPE]

    # ============================================================
    # PARAMÈTRES COMMUNS
    # ============================================================

    capex_min = param["CAPEX_MIN"]
    capex_max = param["CAPEX_MAX"]

    loss_2030_min = param["PERTE_PROD_2030_MIN"]
    loss_2030_max = param["PERTE_PROD_2030_MAX"]

    loss_2050_min = param["PERTE_PROD_2050_MIN"]
    loss_2050_max = param["PERTE_PROD_2050_MAX"]

    power = param["PUISSANCE"]

    # 1 MWh = 3600 MJ
    # Si power est en MW :
    hours_year = 365 * 24

    # ============================================================
    # PROBLÈME SOBOL
    # ============================================================

    if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:

        # --------------------------------------------------------
        # OPEX = PERTE_OPEX × production × FC × prix électricité
        # --------------------------------------------------------

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
                [0, 0.07],
                [45, 120]
            ]
        }

    else:

        # --------------------------------------------------------
        # OPEX = CAPEX × K_OPEX
        # --------------------------------------------------------

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
                [0, 0.07],
                [45, 120]
            ]
        }

    # ============================================================
    # SALTELLI SAMPLING
    # ============================================================

    param_values = saltelli.sample(
        problem,
        2048,
        calc_second_order=False
    )

    Y = np.zeros(len(param_values))

    # ============================================================
    # CALCUL DU NPV
    # ============================================================

    for i, X in enumerate(param_values):

        # --------------------------------------------------------
        # Paramètres communs
        # --------------------------------------------------------

        lifetime = X[0]
        capex = X[1]

        # --------------------------------------------------------
        # TRICASTIN / SAINT-ALBAN / BUGEY
        # --------------------------------------------------------

        if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:

            loss_opex = X[2]
            FC = X[3]

            loss_2030 = X[4]
            loss_2050 = X[5]

            wacc = X[6]
            electricity_price = X[7]

            # OPEX
            opex = (
                loss_opex
                * (power * hours_year)
                * FC
                * electricity_price
            )

            # Redevance économisée
            gain_redevance = (
                9.1
                * param["TAUX_REDEVANCE_Q"][scenario]
                * param["V_REST_OUVERT"]
            )

        # --------------------------------------------------------
        # GOLFECH / NOGENT
        # --------------------------------------------------------

        else:

            k_opex = X[2]

            loss_2030 = X[3]
            loss_2050 = X[4]

            wacc = X[5]
            electricity_price = X[6]

            # OPEX
            opex = capex * k_opex

            # Redevance économisée
            gain_redevance = (
                5
                * param["TAUX_REDEVANCE_Q"][scenario]
                * param["V_REST"]
            )

        # ========================================================
        # CASH-FLOWS
        # ========================================================

        production = power * hours_year

        CF_2030 = (
            -opex
            + loss_2030
            * electricity_price
            * production
            + gain_redevance
        )

        CF_2050 = (
            -opex
            + loss_2050
            * electricity_price
            * production
            + gain_redevance
        )

        # ========================================================
        # NPV
        # ========================================================

        Y[i] = compute_NPV(
            lifetime,
            capex,
            wacc,
            CF_2030,
            CF_2050
        )[0]

    # ============================================================
    # SOBOL INDICES
    # ============================================================

    Si = sobol.analyze(
        problem,
        Y,
        calc_second_order=False
    )

    # ============================================================
    # AFFICHAGE
    # ============================================================

    print("--------------------------------")
    print(f"Sobol indices - {CNPE} - {scenario}")
    print("--------------------------------")

    for name, s1, st in zip(
        problem["names"],
        Si["S1"],
        Si["ST"]
    ):
        print(
            f"{name:25s}"
            f"S1={s1:.3f} "
            f"ST={st:.3f}"
        )

    # ============================================================
    # SOBOL PLOT
    # ============================================================

    plt.figure(figsize=(10, 6))

    x = np.arange(len(problem["names"]))

    plt.bar(
        x - 0.2,
        Si["S1"],
        width=0.4,
        label="First order"
    )

    plt.bar(
        x + 0.2,
        Si["ST"],
        width=0.4,
        label="Total"
    )

    plt.xticks(
        x,
        problem["names"],
        rotation=45,
        ha="right"
    )

    plt.ylabel("Sobol index")

    plt.title(
        f"Sobol sensitivity analysis – {CNPE} – {scenario}"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()

    return Si