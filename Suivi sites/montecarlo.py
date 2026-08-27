import numpy as np
import matplotlib.pyplot as plt
from capex_opex import *
from montecarlo_utils import tornado_plot,calc_sobol,compute_NPV
from param import CNPE_PARAMETERS

# PARAMETERS

ELECTRICITY_PRICE_MU = 66.7
ELECTRICITY_PRICE_SIGMA = 11.4
WACC_VALUES = [0.02,0.06,0.1]




def montecarlo_simulation(n_sim,cnpe_choice,scenario):

    NPV_results = []
    ROI_results = []
    param = CNPE_PARAMETERS[cnpe_choice]


    for i in range(n_sim):
    
        lifetime = np.random.choice(param["L"])
        capex = np.random.triangular(param["CAPEX_MIN"],param["CAPEX_MODE"],param["CAPEX_MAX"])
        loss_2030 = np.random.triangular(param["PERTE_PROD_2030_MIN"],param["PERTE_PROD_2030_MODE"],param["PERTE_PROD_2030_MAX"])
        loss_2050 = np.random.triangular(param["PERTE_PROD_2050_MIN"],param["PERTE_PROD_2050_MODE"],param["PERTE_PROD_2050_MAX"])
        wacc = np.random.choice(WACC_VALUES)
        electricity_price = np.random.normal(ELECTRICITY_PRICE_MU,ELECTRICITY_PRICE_SIGMA)
        power = param["PUISSANCE"]

        if cnpe_choice in ["Tricastin", "Saint-Alban", "Bugey"]:
            loss_opex = np.random.triangular(param["PERTE_OPEX_MIN"],param["PERTE_OPEX_MODE"],param["PERTE_OPEX_MAX"])
            FC = np.random.beta(param["FC_ALPHA"],param["FC_BETA"])
            opex = loss_opex * (power*365*24) * FC * electricity_price
            gain_redevance = param["TAUX_REDEVANCE_PREL"][scenario] * param["V_PREL_OUVERT"]*1e4+9.1*param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST_OUVERT"]
        else :
            k = np.random.triangular(param["K_OPEX_MIN"],param["K_OPEX_MODE"],param["K_OPEX_MAX"])
            opex = capex * k
            gain_redevance = 5*param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST"]

        CF_2030 = - opex + loss_2030*electricity_price* (power*365*24) + gain_redevance
        CF_2050 = - opex + loss_2050*electricity_price* (power*365*24) + gain_redevance
        NPV, ROI = compute_NPV(lifetime,capex,wacc,CF_2030,CF_2050)

        NPV_results.append(NPV)
        ROI_results.append(ROI)

    NPV_results=np.array(NPV_results)
    ROI_results=np.array(ROI_results)

    return NPV_results,ROI_results


if __name__=="__main__":

    print("--------------------------------")
    print("Monte Carlo results")
    print("--------------------------------")
    n_sim = 100000
    scenario = "S_REF" #S_REF, S_HARM, S_RENF, S_RENF_FORT
    CNPE = 'Tricastin'

    NPV_results,ROI_results = montecarlo_simulation(n_sim,CNPE,scenario)

    mean=np.mean(NPV_results)
    median=np.median(NPV_results)


    std=np.std(NPV_results,ddof=1)
    SE=std/np.sqrt(n_sim)
    q025 = np.percentile(NPV_results, 2.5)
    q975 = np.percentile(NPV_results, 97.5)

    print(f"Mean NPV : {mean/1e6:.1f} M€")
    print(f"Median NPV : {median/1e6:.1f} M€")
    print(
            f"NPV standard deviation : "
            f"{np.std(NPV_results)/1e6:.1f} M€"
        )
    print(f"Intervalle à 95 % : [{q025/1e6:.1f} ; {q975/1e6:.1f}] M€")
    print(
        f"Probability NPV > 0 : "
        f"{np.mean(NPV_results>0)*100:.1f}%"
    )
    print(
        f"Mean ROI : "
        f"{np.mean(ROI_results)*100:.1f}%"
    )
    print(
        f"ROI standard deviation : "
        f"{np.std(ROI_results)*100:.1f}%"
    )



    plt.figure(figsize=(8,5))

    plt.hist( NPV_results/1e6, bins=100 )

    plt.xlabel("NPV (M€)")
    plt.ylabel("Frequency")
    plt.title("Monte Carlo distribution of NPV")

    plt.show()

    plt.figure(figsize=(8,5))
    plt.hist(  ROI_results*100,  bins=100 )
    plt.xlabel("ROI (%)")
    plt.ylabel("Frequency")
    plt.title("Monte Carlo distribution of ROI")
    plt.show()

    #Convergence
    cum_mean = ( np.cumsum(NPV_results) /  np.arange(1,n_sim+1))
    plt.figure(figsize=(8,5))
    plt.plot(cum_mean/1e6)
    plt.xlabel("Number of simulations")
    plt.ylabel("Mean NPV (M€)")
    plt.title("Monte Carlo convergence")
    plt.show()

    tornado_plot(NPV_results,CNPE,scenario)
    calc_sobol(CNPE,scenario)


