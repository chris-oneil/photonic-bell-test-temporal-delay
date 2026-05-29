import numpy as np
import argparse

def evaluate_chronos_loophole(eta_base, eta_var, sigma_j_ps, delta_t_window_ps, tau_max_ps, N=1000000):
    """
    Monte Carlo simulation of the Chronos Loophole combining:
    1. Spatial Filter: Polarization-dependent walk-off at the SNSPD.
    2. Temporal Filter: Dynamic coincidence window shift due to EOM active transition transients.
       Note: The timing shift tau_max_ps represents the compounding physical scaling of:
         - Driver-induced Ground Bounce (electronic cross-talk shifting discriminator thresholds by ~10-100 ps)
         - Dynamic PMD Splitting (birefringent group-delay splitting across fast/slow fiber axes)
         - Chromatic GVD chirp-dispersion coupling (femtosecond scale base).
    """
    # Settings (standard CHSH maximum violation configuration)
    a_angles = [0.0, np.pi / 4]       # a, a_prime
    b_angles = [np.pi / 8, 3 * np.pi / 8] # b, b_prime
    
    # Active voltage pulse transitions
    # a_prime (pi/4), b (pi/8), and b_prime (3pi/8) require active EOM state shifts (high-voltage pulses).
    # a (0.0) represents the inactive ground state (no pulse, zero transient delay).
    active_settings_A = [False, True]
    active_settings_B = [True, True]
    
    lambdas = np.random.uniform(0, np.pi, N)
    
    # SNSPD and coincidence filter parameters (in picoseconds)
    sigma_j = sigma_j_ps
    t_w = delta_t_window_ps
    
    def temporal_acceptance(active, angle, lmbda):
        if not active:
            # Inactive state: No EOM ringing, no chirp, zero group delay shift
            d_tau = 0.0
        else:
            # Active state: EOM ringing induces dynamic chirp and electronic/birefringent arrival time shifts.
            # The shift is modeled as a function of the local phase mismatch
            d_tau = tau_max_ps * np.cos(2 * (angle - lmbda))
            
        # Analytical integration of the Gaussian jitter over the strict coincidence window [-t_w, t_w]
        # P_time = \int_{-t_w}^{t_w} 1/(sig*sqrt(2pi)) * exp(-(t-d_tau)^2 / (2*sig^2)) dt
        from scipy.special import erf
        P_time = 0.5 * (erf((t_w - d_tau) / (sigma_j * np.sqrt(2))) - erf((-t_w - d_tau) / (sigma_j * np.sqrt(2))))
        return P_time

    E_results = []
    delta_results = []
    
    for i, angle_a in enumerate(a_angles):
        active_a = active_settings_A[i]
        for j, angle_b in enumerate(b_angles):
            active_b = active_settings_B[j]
            
            # Spatial efficiency component (clipped to [0.0, 1.0])
            eta_A = np.clip(eta_base + eta_var * np.cos(angle_a - lambdas) ** 2, 0.0, 1.0)
            eta_B = np.clip(eta_base + eta_var * np.cos(angle_b - lambdas) ** 2, 0.0, 1.0)
            
            # Temporal acceptance component
            P_time_A = temporal_acceptance(active_a, angle_a, lambdas)
            P_time_B = temporal_acceptance(active_b, angle_b, lambdas)
            
            # Joint probability space
            P_coincidence = eta_A * eta_B * P_time_A * P_time_B
            P_acc = np.mean(P_coincidence)
            
            # Total-Variation distance (delta) from uniform prior
            delta = 0.5 * np.mean(np.abs((P_coincidence / P_acc) - 1.0))
            delta_results.append(delta)
            
            # Outcome functions (single-angle model representing spatial walk-off geometry)
            A = np.sign(np.cos(angle_a - lambdas))
            B = np.sign(np.cos(angle_b - lambdas))
            A[A == 0] = 1
            B[B == 0] = 1
            
            E = np.mean(A * B * P_coincidence) / P_acc
            E_results.append(E)
            
    # CHSH value: S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
    S = E_results[0] - E_results[1] + E_results[2] + E_results[3]
    delta_sup = max(delta_results)
    
    return S, delta_sup

def main():
    parser = argparse.ArgumentParser(description="Unified Simulation of Spatial and Temporal Filters in Photonic Bell Tests")
    parser.add_argument("--eta-base", type=float, default=0.48, help="Base isotropic absorption efficiency")
    parser.add_argument("--eta-var", type=float, default=0.52, help="Setting-dependent spatial efficiency variance")
    parser.add_argument("--sigma-j", type=float, default=100.0, help="Baseline SNSPD timing jitter in ps")
    parser.add_argument("--t-window", type=float, default=500.0, help="Coincidence window half-width in ps")
    parser.add_argument("--tau-max", type=float, default=150.0, help="Maximum physical arrival-time shift in ps (ground-bounce + PMD)")
    parser.add_argument("--runs", type=int, default=1000000, help="Number of simulated emissions")
    
    args = parser.parse_args()
    
    print("======================================================================")
    print("Running Hardened Unified Simulation for Paper 2 (The Chronos Loophole)")
    print(f"Physical Parameters:")
    print(f"  Base Efficiency (eta_base): {args.eta_base}")
    print(f"  Spatial Variance (eta_var): {args.eta_var}")
    print(f"  SNSPD Jitter (sigma_j):      {args.sigma_j} ps")
    print(f"  Coincidence Half-Width:     {args.t_window} ps")
    print(f"  Max Transient Delay Shift:  {args.tau_max} ps")
    print("----------------------------------------------------------------------")
    
    S, delta = evaluate_chronos_loophole(
        args.eta_base, args.eta_var, args.sigma_j, args.t_window, args.tau_max, N=args.runs
    )
    
    print(f"Hardened Unified Simulation Results:")
    print(f"  CHSH Correlation S_max = {S:.4f}")
    print(f"  TV Dispersion delta_sup = {delta:.4f}")
    print("======================================================================\n")

if __name__ == "__main__":
    main()
