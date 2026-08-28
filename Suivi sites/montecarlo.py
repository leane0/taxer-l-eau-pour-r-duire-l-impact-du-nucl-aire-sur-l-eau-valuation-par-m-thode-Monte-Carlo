import numpy as np
import matplotlib.pyplot as plt
from montecarlo_utils import tornado_plot,calc_sobol,compute_NPV
from param import CNPE_PARAMETERS
from plot import *
import os
import pandas as pd
import pickle
from plot_param import *
from sobol import *
from tornado import *



# PARAMETERS

ELECTRICITY_PRICE_MU = 66.7
ELECTRICITY_PRICE_SIGMA = 11.4
WACC_VALUES = [0.02,0.06,0.1]




def montecarlo_parameters(n_sim, cnpe_choice, scenario):
    
    param = CNPE_PARAMETERS[cnpe_choice]

    capex_results = []
    opex_results = []
    redevance_results = []
    loss_prod_results = []
    npv_results = []
    roi_results =[]

    for i in range(n_sim):

        lifetime = np.random.choice(param["L"])
        capex = np.random.triangular(
            param["CAPEX_MIN"],
            param["CAPEX_MODE"],
            param["CAPEX_MAX"]
        )
        loss_2030 = np.random.triangular(
            param["PERTE_PROD_2030_MIN"],
            param["PERTE_PROD_2030_MODE"],
            param["PERTE_PROD_2030_MAX"]
        )
        loss_2050 = np.random.triangular(
            param["PERTE_PROD_2050_MIN"],
            param["PERTE_PROD_2050_MODE"],
            param["PERTE_PROD_2050_MAX"]
        )
        power = param["PUISSANCE"]
        wacc=np.random.triangular(WACC_VALUES[0],WACC_VALUES[1],WACC_VALUES[2])

        # OPEX
        if cnpe_choice in ["Tricastin", "Saint-Alban", "Bugey"]:
            loss_opex = np.random.triangular(
                param["PERTE_OPEX_MIN"],
                param["PERTE_OPEX_MODE"],
                param["PERTE_OPEX_MAX"]
            )
            FC = np.random.beta(
                param["FC_ALPHA"],
                param["FC_BETA"]
            )
            electricity_price = np.random.normal(
                ELECTRICITY_PRICE_MU,
                ELECTRICITY_PRICE_SIGMA
            )
            opex = (loss_opex
                * (power * 365 * 24)* FC* electricity_price)

            gain_redevance = (
                param["TAUX_REDEVANCE_PREL"][scenario]* param["V_PREL_OUVERT"] * 1e4
                + 9.1* param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST_OUVERT"])

        else:

            k = np.random.triangular(
                param["K_OPEX_MIN"],
                param["K_OPEX_MODE"],
                param["K_OPEX_MAX"]
            )
            opex = capex * k
            gain_redevance = (5
                * param["TAUX_REDEVANCE_Q"][scenario]
                * param["V_REST"])

        # Perte de production moyenne
        loss_prod_mean = (loss_2030 + loss_2050) / 2
        CF_2030 = -opex + gain_redevance + loss_2030
        CF_2050 = -opex + gain_redevance + loss_2050

        capex_results.append(capex)
        opex_results.append(opex)
        redevance_results.append(gain_redevance)
        loss_prod_results.append(loss_prod_mean)
        NPV,ROI = compute_NPV(lifetime,capex,wacc,CF_2030,CF_2050)
    return {
        "NPV" : np.array(NPV),
        "ROI" : np.array(ROI),
        "CAPEX": np.array(capex_results),
        "OPEX": np.array(opex_results),
        "REDEVANCE": np.array(redevance_results),
        "LOSS_PROD": np.array(loss_prod_results)
    }

if __name__ == "__main__":
    
    print("--------------------------------")
    print("Monte Carlo - All CNPE / scenarios")
    print("--------------------------------")

    n_sim = 100000

    # Tous les scénarios
    scenarios = [
        "S_REF",
        "S_HARM",
        "S_RENF",
        "S_RENF_FORT"
    ]

    CNPEs = list(CNPE_PARAMETERS.keys())

    # Dossier principal de sortie
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    all_results = []


    # ============================================================
    # BOUCLE CNPE / SCENARIO
    # ============================================================
    results={}
    for CNPE in CNPEs:
        print(CNPE)
        results[CNPE] = {}

        for scenario in scenarios:
            data = montecarlo_parameters(n_sim,CNPE,scenario)
            results[CNPE][scenario] = {
                "NPV" : np.mean(data["NPV"])/1e6,
                "ROI" : np.mean(data["ROI"])/1e6,
                "CAPEX": np.mean(data["CAPEX"]) / 1e6,
                "OPEX": np.mean(data["OPEX"]) / 1e6,
                "REDEVANCE": np.mean(data["REDEVANCE"]) / 1e6,
                "LOSS_PROD": np.mean(data["LOSS_PROD"]) * 100
            }

            #plot_param (CNPE,scenarios,results)

            print("\n--------------------------------")
            print(f"CNPE      : {CNPE}")
            print(f"Scenario  : {scenario}")
            print("--------------------------------")

            # Dossier de sortie
            scenario_dir = os.path.join(output_dir, CNPE,scenario)
            os.makedirs(scenario_dir, exist_ok=True)

            # Monte Carlo

            NPV_results, ROI_results = data["NPV"],data["ROI"]

            mean = np.mean(NPV_results)
            median = np.median(NPV_results)
            std = np.std(NPV_results, ddof=1)
            SE = std / np.sqrt(n_sim)
            q025 = np.percentile(NPV_results, 2.5)
            q975 = np.percentile(NPV_results, 97.5)
            probability_positive = np.mean(NPV_results > 0)
            mean_roi = np.mean(ROI_results)
            std_roi = np.std(ROI_results, ddof=1)

            with open(os.path.join(scenario_dir, "monte_carlo_results.pkl"), "wb" ) as f:
                pickle.dump(data, f)

            # Stockage des résultats
            all_results.append({
                "CNPE": CNPE,
                "Scenario": scenario,
                "N_sim": n_sim,
                "NPV_mean_M€": mean / 1e6,
                "NPV_median_M€": median / 1e6,
                "NPV_std_M€": std / 1e6,
                "NPV_SE_M€": SE / 1e6,
                "NPV_2.5_percentile_M€": q025 / 1e6,
                "NPV_97.5_percentile_M€": q975 / 1e6,
                "Probability_NPV_positive": probability_positive,
                "ROI_mean": mean_roi,
                "ROI_std": std_roi,
                "CAPEX": np.mean(data["CAPEX"]) / 1e6,
                "OPEX": np.mean(data["OPEX"]) / 1e6,
                "REDEVANCE": np.mean(data["REDEVANCE"]) / 1e6,
                "LOSS_PROD": np.mean(data["LOSS_PROD"]) * 100

            })

            # AFFICHAGE

            print_results(mean,median,std,q025,q975,probability_positive,mean_roi,std_roi)
            plot_NPV(NPV_results,CNPE,scenario,os,scenario_dir)
            plot_ROI(ROI_results,CNPE,scenario,os,scenario_dir)
            plot_convergence(NPV_results,n_sim,CNPE,scenario,os,scenario_dir)

            tornado_plot(NPV_results,CNPE,scenario)
            plt.savefig(os.path.join(scenario_dir,"tornado.png"),dpi=300,bbox_inches="tight")
            plt.close()

            calc_sobol(CNPE,scenario)
            plt.savefig(os.path.join(scenario_dir,"sobol.png"),dpi=300,bbox_inches="tight")
            plt.close()

    # CSV FINAL

    results_df = pd.DataFrame(all_results)
    csv_path = os.path.join(output_dir,"results.csv")
    results_df.to_csv( csv_path, index=False, sep=";")

    print("\n================================")
    print("ALL SIMULATIONS FINISHED")
    print("================================")
    print(f"Results saved to : {csv_path}")
    print("\nSummary:")
    print(results_df)


