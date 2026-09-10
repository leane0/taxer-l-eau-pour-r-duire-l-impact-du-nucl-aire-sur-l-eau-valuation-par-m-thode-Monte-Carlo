from main import *
import numpy as np
from utils.montecarlo_utils import *
from utils.plot import *
import os
import pandas as pd
import pickle
from plot_param import *
from utils.sobol import *
from utils.tornado import *

# pour tracer le graphique avec la proba de VAN positive en fonction du taux de redevance en chaleur


if __name__ == "__main__":
    
    print("--------------------------------")
    print("Monte Carlo - All CNPE / scenarios")
    print("--------------------------------")

    n_sim = 10000

    # Tous les scénarios
    scenarios = [
        "S_REF","S_1","S_2","S_3"
    ]

    CNPEs = ["Nogent"]

    # Dossier principal de sortie
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    redevance_Q = range (60,46060,500)

    results={}
    for CNPE in CNPEs:
        print(CNPE)
        results[CNPE] = {}

        for r_Q in redevance_Q:
            data = montecarlo_parameters(n_sim,CNPE,"S_REF",r_Q)
            results[CNPE][str(r_Q)] = {
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
            print(f"Scenario  : {str(r_Q)}")
            print("--------------------------------")

            # Dossier de sortie
            #scenario_dir = os.path.join(output_dir, CNPE,str(r_Q))
            #os.makedirs(scenario_dir, exist_ok=True)

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

            #with open(os.path.join(scenario_dir, "monte_carlo_results.pkl"), "wb" ) as f:
            #    pickle.dump(data, f)

            # Stockage des résultats
            all_results.append({
                "CNPE": CNPE,
                "Taux_redevance": r_Q,
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

            #print_results(mean,median,std,q025,q975,probability_positive,mean_roi,std_roi)
            #plot_NPV(NPV_results,CNPE,scenario,os,scenario_dir)
            #plot_ROI(ROI_results,CNPE,scenario,os,scenario_dir)
            #plot_convergence(NPV_results,n_sim,CNPE,scenario,os,scenario_dir)

            #tornado_plot(NPV_results,CNPE,scenario)
            #plt.savefig(os.path.join(scenario_dir,"tornado.png"),dpi=300,bbox_inches="tight")
            #plt.close()

            #calc_sobol(CNPE,scenario)
            #plt.savefig(os.path.join(scenario_dir,"sobol.png"),dpi=300,bbox_inches="tight")
            #plt.close()

    # CSV final

    results_df = pd.DataFrame(all_results)
    csv_path = os.path.join(output_dir,"results_rQ.csv")
    results_df.to_csv( csv_path, index=False, sep=";")

    print("\n================================")
    print("ALL SIMULATIONS FINISHED")
    print("================================")
    print(f"Results saved to : {csv_path}")
    print("\nSummary:")
    print(results_df)