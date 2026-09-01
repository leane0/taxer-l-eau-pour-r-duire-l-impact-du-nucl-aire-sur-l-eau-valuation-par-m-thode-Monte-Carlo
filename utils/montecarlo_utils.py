import numpy as np
import matplotlib.pyplot as plt

from SALib.sample import saltelli
from SALib.analyze import sobol
from param import CNPE_PARAMETERS

# retourne le cas moyen (cas de base)
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

# calcule la VAN et le ROI pour chaque set de paramètres tirés au hasard
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


# calcul van pour tornado plot
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
    

    # calcul OPEX

    if CNPE in ["Tricastin", "Saint-Alban", "Bugey"]:
        loss_opex = d["loss_opex"]
        FC = d["FC"]
        opex = (loss_opex* (power * 365 * 24)* FC* electricity_price)
        gain_redevance = param["TAUX_REDEVANCE_PREL"][scenario] * param["V_PREL_OUVERT"]*1e4+9.1*param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST_OUVERT"]

    else:
        k = d["k_opex"]
        opex = capex * k
        gain_redevance = ( 10* param["TAUX_REDEVANCE_Q"][scenario] * param["V_REST"])

    # cash flow
    production = power * 365 * 24
    CF_2030 = (-opex + loss_2030 * electricity_price * production + gain_redevance)
    CF_2050 = ( -opex + loss_2050 * electricity_price * production+ gain_redevance )

    # VAN
    npv,_=compute_NPV(lifetime,capex,wacc,CF_2030,CF_2050,)

    return npv



