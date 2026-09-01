# parametres.py

CNPE_PARAMETERS = {
    "Tricastin": {
        "CAPEX_MIN": 500e6,#979855095.25,       # $
        "CAPEX_MAX": 1501593879.59, #2427999196.72 ,     # $
        "CAPEX_MODE": 1e9, #1501593879.59 ,    # $
        "PERTE_OPEX_MIN": -0.0044,
        "PERTE_OPEX_MAX": 0.0098,
        "PERTE_OPEX_MODE": 0.0022,
        "FC_ALPHA": 31.6,
        "FC_BETA": 12.3,
        "L":[10,20,30],
        "PERTE_PROD_2030_MIN": 0.005,
        "PERTE_PROD_2030_MODE": 0.010,
        "PERTE_PROD_2030_MAX": 0.015,
        "PERTE_PROD_2050_MIN": 0.010,
        "PERTE_PROD_2050_MODE": 0.020,
        "PERTE_PROD_2050_MAX": 0.030,
        "PUISSANCE" : 3600,
        "TAUX_REDEVANCE_Q" : {"S_REF" : 20,
                       "S_HARM" : 85,
                       "S_RENF" : 100,
                       "S_RENF_FORT" : 850,
                        "S_THER_1":2000,
                        "S_THER_2":4000,},
        "TAUX_REDEVANCE_PREL" : {"S_REF" : 0.34, #t_{prel}^o-\ \frac{t_{prel}^f}{10,2}
                       "S_HARM" : 0.21,
                       "S_RENF" : 1.16,
                       "S_RENF_FORT" : 3.26,
                       "S_THER_1":0.34,
                       "S_THER_2":0.34,},

        "V_REST_OUVERT" : 3446,
        "V_PREL_OUVERT" : 4684,

    },

    "Bugey": {
        "CAPEX_MIN": 500e6 ,       # $
        "CAPEX_MAX": 926537232.21  ,     # $
        "CAPEX_MODE": 713e6  ,     # $
        "PERTE_OPEX_MIN": -0.0044,
        "PERTE_OPEX_MAX": 0.0098,
        "PERTE_OPEX_MODE": 0.0022,
        "FC_ALPHA": 6.84,
        "FC_BETA": 3.07,
        "L":[10,20,30],
        "PERTE_PROD_2030_MIN": 0.010,
        "PERTE_PROD_2030_MODE": 0.020,
        "PERTE_PROD_2030_MAX": 0.025,
        "PERTE_PROD_2050_MIN": 0.020,
        "PERTE_PROD_2050_MODE": 0.040,
        "PERTE_PROD_2050_MAX": 0.050,
        "PUISSANCE" : 1800,
        "TAUX_REDEVANCE_Q" : {"S_REF" : 20,
                       "S_HARM" : 85,
                       "S_RENF" : 100,
                       "S_RENF_FORT" : 200,
                        "S_THER_1":2000,
                        "S_THER_2":4000,},   
         "TAUX_REDEVANCE_PREL" : {"S_REF" : 0.34, #t_{prel}^o-\ \frac{t_{prel}^f}{10,2}
                       "S_HARM" : 0.21,
                       "S_RENF" : 1.16,
                       "S_RENF_FORT" : 3.26,
                       "S_THER_1":0.34,
                        "S_THER_2":0.34,},
        "V_REST_OUVERT" : 1995,  
        "V_PREL_OUVERT" : 2646,   
    },

    "Saint-Alban": {
        "CAPEX_MIN": 500e6  ,       # $
        "CAPEX_MAX": 1197152125.09  ,      # $
        "CAPEX_MODE": 850e6  ,     # $
        "PERTE_OPEX_MIN": -0.0044,
        "PERTE_OPEX_MAX": 0.0098,
        "PERTE_OPEX_MODE": 0.0022,
        "FC_ALPHA": 19,
        "FC_BETA": 5.7,
        "L":[10,20,30],
        "PERTE_PROD_2030_MIN": 0.013,
        "PERTE_PROD_2030_MODE": 0.020,
        "PERTE_PROD_2030_MAX": 0.025,
        "PERTE_PROD_2050_MIN": 0.013,
        "PERTE_PROD_2050_MODE": 0.030,
        "PERTE_PROD_2050_MAX": 0.050,
        "PUISSANCE" : 2600,
        "TAUX_REDEVANCE_Q" : {"S_REF" : 20,
                               "S_HARM" : 85,
                               "S_RENF" : 100,
                               "S_RENF_FORT" : 200,
                               "S_THER_1":2000,
                                "S_THER_2":4000,
                               }, 
        "V_REST_OUVERT" : 2636,
         "TAUX_REDEVANCE_PREL" : {"S_REF" : 0.34, #t_{prel}^o-\ \frac{t_{prel}^f}{10,2}
                       "S_HARM" : 0.21,
                       "S_RENF" : 1.16,
                       "S_RENF_FORT" : 3.26,
                       "S_THER_1":0.34,
                       "S_THER_2":0.34,},
        "V_PREL_OUVERT" : 3600,
        
    },

    "Golfech": {
        "CAPEX_MIN": 35.54e6  ,      # $
        "CAPEX_MAX": 208e6  ,          # $
        "CAPEX_MODE": 57.4e6  ,      # $
        "K_OPEX_MIN": -0.003,
        "K_OPEX_MAX": 0.0246,
        "K_OPEX_MODE": 0.0138,
        "L":[10,20,30,40],
        "PERTE_PROD_2030_MIN": 0.005,
        "PERTE_PROD_2030_MODE": 0.013,
        "PERTE_PROD_2030_MAX": 0.017,
        "PERTE_PROD_2050_MIN": 0.018,
        "PERTE_PROD_2050_MODE": 0.023,
        "PERTE_PROD_2050_MAX": 0.036,
        "PUISSANCE" : 2600,
        "TAUX_REDEVANCE_Q" : {"S_REF" : 54,
                               "S_HARM" : 85,
                               "S_RENF" : 270,
                               "S_RENF_FORT" : 540,
                               "S_THER_1":5400,
                                "S_THER_2":10800,}, 
        "V_REST" : 111.34,
    },

    "Nogent": {
        "CAPEX_MIN": 35.54e6  ,      # $
        "CAPEX_MAX": 208e6  ,          # $
        "CAPEX_MODE": 57.4e6  ,      # $
        "K_OPEX_MIN": -0.003,
        "K_OPEX_MAX": 0.0246,
        "K_OPEX_MODE": 0.0138,
        "L":[10,20,30,40],
        "PERTE_PROD_2030_MIN": 0.000,
        "PERTE_PROD_2030_MODE": 0.002,
        "PERTE_PROD_2030_MAX": 0.01,
        "PERTE_PROD_2050_MIN": 0.000,
        "PERTE_PROD_2050_MODE": 0.005,
        "PERTE_PROD_2050_MAX": 0.010,
        "PUISSANCE" : 2600,
        "TAUX_REDEVANCE_Q" : {"S_REF" : 60,
                               "S_HARM" : 85,
                               "S_RENF" : 300,
                               "S_RENF_FORT" : 600,
                               "S_THER_1":6000,
                               "S_THER_2":12000,},
        "V_REST" : 73.92,
 
    }

}