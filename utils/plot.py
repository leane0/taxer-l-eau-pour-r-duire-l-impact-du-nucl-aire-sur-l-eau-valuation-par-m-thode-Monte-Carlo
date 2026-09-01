import numpy as np
import matplotlib.pyplot as plt

# fonctions d'affichage

def print_results(mean,median,std,q025,q975,probability_positive,mean_roi,std_roi):
    print(f"Mean NPV : {mean/1e6:.1f} M€")
    print(f"Median NPV : {median/1e6:.1f} M€")
    print(f"NPV standard deviation : {std/1e6:.1f} M€")

    print(
        f"95% interval : "
        f"[{q025/1e6:.1f} ; {q975/1e6:.1f}] M€"
    )

    print(
        f"Probability NPV > 0 : "
        f"{probability_positive*100:.1f}%"
    )

    print(f"Mean ROI : {mean_roi*100:.1f}%")
    print(f"ROI standard deviation : {std_roi*100:.1f}%")

def plot_convergence(NPV_results,n_sim,CNPE,scenario,os,scenario_dir):
    cum_mean = (np.cumsum(NPV_results)/ np.arange(1, n_sim + 1) )

    plt.figure(figsize=(8, 5))

    plt.plot(cum_mean / 1e6)

    plt.xlabel("Number of simulations")
    plt.ylabel("Mean NPV (M€)")

    plt.title(
        f"Monte Carlo convergence\n"
        f"{CNPE} - {scenario}"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join( scenario_dir, "convergence.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def plot_ROI(ROI_results,CNPE,scenario,os,scenario_dir) :
    plt.figure(figsize=(8, 5))

    plt.hist( ROI_results * 100, bins=100)

    plt.xlabel("ROI (%)")
    plt.ylabel("Frequency")

    plt.title(
        f"Monte Carlo distribution of ROI\n"
        f"{CNPE} - {scenario}"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(   scenario_dir, "ROI_hist.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def plot_NPV(NPV_results,CNPE,scenario,os,scenario_dir):
    plt.figure(figsize=(8, 5))
    
    plt.hist(
        NPV_results / 1e6,
        bins=100
    )

    plt.xlabel("NPV (M€)")
    plt.ylabel("Frequency")

    plt.title(
        f"Monte Carlo distribution of NPV\n"
        f"{CNPE} - {scenario}"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            scenario_dir,
            "NPV_hist.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()