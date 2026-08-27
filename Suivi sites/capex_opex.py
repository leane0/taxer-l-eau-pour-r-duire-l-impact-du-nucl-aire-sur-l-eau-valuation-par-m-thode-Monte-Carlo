REF_CAPEX_VALUE = (3370.0 + 1420.0) * 1e6 / 7344000 # $ 2010 / gpm
REF_CAPEX_VALUE = REF_CAPEX_VALUE * 1.45 * 0.88 # € 2026 /gpm

REF_HELPER_COOLING_TOWER = 100e6 #$ 1993
REF_HELPER_COOLING_TOWER = REF_HELPER_COOLING_TOWER * 2.31 *0.88 #€ 2026

REF_OPEX_VALUE = (24.0 + 31.0) * 1e6 / 7344000 # $ 2010 / gpm
REF_OPEX_VALUE = REF_OPEX_VALUE * 1.45 * 0.88 # € 2026 /gpm

def calc_capex (water_flowrate) : # power in MW
    water_flowrate = 13198 * water_flowrate #m3/s to gpm
    capex = REF_CAPEX_VALUE * water_flowrate
    print (capex)
    return capex * 0.75 , capex , capex *1.25

def calc_opex (water_flowrate) : # power in MW
    water_flowrate = 13198 * water_flowrate #m3/s to gpm
    opex = REF_OPEX_VALUE * water_flowrate
    print(opex)
    return opex * 0.75 , opex , opex *1.25

def calc_capex_helper():
    capex = REF_HELPER_COOLING_TOWER * 1.4 + 30e6
    return capex * 0.75 , capex , capex *1.25

def calc_opex_helper():
    opex = REF_HELPER_COOLING_TOWER * 0.02 + 2.5e6
    return opex * 0.75 , opex , opex *1.25

print (calc_capex_helper())