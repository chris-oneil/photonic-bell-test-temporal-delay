#!/usr/bin/env python3
"""
Physical Optics Single-Mode Fiber Overlap Simulator
====================================================
Numerically computes the 2D spatial overlap integral between a laterally displaced
incident Gaussian beam (EOM walk-off) and the fundamental guided mode (LP00)
of a single-mode fiber (SMF-28).

Verifies the "Link-Loss Translation" by confirming that EOM walk-off translates
directly to a dynamic, setting-dependent coupling loss at the fiber input.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad

# Calibrated Physical Constants for Standard Telecom Setup
WAVELENGTH = 1.55e-6          # 1550 nm (Telecom C-band)
FIBER_MFD = 10.4e-6           # SMF-28 Mode Field Diameter is ~10.4 um
FIBER_WAIST = FIBER_MFD / 2.0  # w_f = 5.2 um

def analytical_efficiency(dx, w_i, w_f=FIBER_WAIST):
    """
    Computes analytical coupling efficiency for a displaced 2D Gaussian beam.
    Formula: eta = [ 4 * w_i^2 * w_f^2 / (w_i^2 + w_f^2)^2 ] * exp( -2 * dx^2 / (w_i^2 + w_f^2) )
    """
    prefactor = (4.0 * (w_i**2) * (w_f**2)) / ((w_i**2 + w_f**2)**2)
    exponent = -2.0 * (dx**2) / (w_i**2 + w_f**2)
    return prefactor * np.exp(exponent)

def numerical_overlap_integrand_num(x, y, dx, w_i, w_f):
    """Numerator integrand: E_i(x, y) * E_f^*(x, y)"""
    E_i = np.exp(-((x - dx)**2 + y**2) / w_i**2)
    E_f = np.exp(-(x**2 + y**2) / w_f**2)
    return E_i * E_f

def numerical_overlap_integrand_den_i(x, y, w_i):
    """Denominator integrand for incident beam: |E_i(x, y)|^2"""
    return np.exp(-2.0 * (x**2 + y**2) / w_i**2)

def numerical_overlap_integrand_den_f(x, y, w_f):
    """Denominator integrand for fiber mode: |E_f(x, y)|^2"""
    return np.exp(-2.0 * (x**2 + y**2) / w_f**2)

def compute_numerical_efficiency(dx, w_i, w_f=FIBER_WAIST):
    """
    Numerically computes coupling efficiency using 2D double-quadrature integration
    over the transverse coordinate plane (x, y).
    Integrates from -6*max(w_i, w_f) to +6*max(w_i, w_f) to prevent boundary truncation.
    """
    limit = 6.0 * max(w_i, w_f)
    
    # Numerator integral (Overlap)
    num_val, _ = dblquad(
        numerical_overlap_integrand_num,
        -limit, limit,
        lambda x: -limit, lambda x: limit,
        args=(dx, w_i, w_f)
    )
    
    # Denominator integrals (Norms)
    den_i, _ = dblquad(
        numerical_overlap_integrand_den_i,
        -limit, limit,
        lambda x: -limit, lambda x: limit,
        args=(w_i,)
    )
    
    den_f, _ = dblquad(
        numerical_overlap_integrand_den_f,
        -limit, limit,
        lambda x: -limit, lambda x: limit,
        args=(w_f,)
    )
    
    # eta = |Overlap|^2 / (Norm_i * Norm_f)
    return (num_val**2) / (den_i * den_f)

def run_verification_tests():
    """Verify numerical integration against analytical formulas under distinct waists and displacements."""
    print("[TEST] Running automated physical-optics verification tests...")
    
    test_displacements = [0.0, 1.0e-6, 2.5e-6, 4.0e-6]
    test_waists = [3.0e-6, 5.2e-6, 7.0e-6]
    w_f = FIBER_WAIST
    
    passed_tests = 0
    total_tests = 0
    
    for w_i in test_waists:
        for dx in test_displacements:
            total_tests += 1
            analytical = analytical_efficiency(dx, w_i, w_f)
            numerical = compute_numerical_efficiency(dx, w_i, w_f)
            
            error = abs(analytical - numerical)
            assert error < 1e-6, f"Validation failed at w_i={w_i:.1e}, dx={dx:.1e}: numerical={numerical:.6f}, analytical={analytical:.6f}, error={error:.2e}"
            passed_tests += 1
            
    print(f"[TEST] Verification complete. Passed {passed_tests}/{total_tests} test cases successfully (Error < 1e-6).")

def generate_overlap_plots():
    """Runs sweeps and plots Coupling Efficiency (fraction and dB loss) vs displacement."""
    print("\n[SIM] Sweeping EOM walk-off displacements and compiling loss curves...")
    
    displacements = np.linspace(0, 8.0e-6, 100)  # Sweep 0 to 8 um
    
    # Incident waist cases to model:
    # 1. Perfectly matched waist (w_i = w_f = 5.2 um)
    # 2. Focused beam too small (w_i = 3.0 um)
    # 3. Defocused beam too large (w_i = 7.5 um)
    waist_cases = [
        {"name": "Waist Matched ($w_i = 5.2\\,\\mu$m)", "w_i": 5.2e-6, "color": "#2ca02c", "style": "-"},
        {"name": "Under-focused ($w_i = 3.0\\,\\mu$m)", "w_i": 3.0e-6, "color": "#1f77b4", "style": "--"},
        {"name": "Over-focused ($w_i = 7.5\\,\\mu$m)", "w_i": 7.5e-6, "color": "#d62728", "style": "-."},
    ]
    
    plt.figure(figsize=(10, 8))
    
    # Top plot: Fractional Efficiency (eta)
    ax1 = plt.subplot(2, 1, 1)
    
    # Bottom plot: Attenuation (dB)
    ax2 = plt.subplot(2, 1, 2)
    
    for case in waist_cases:
        w_i = case["w_i"]
        label = case["name"]
        color = case["color"]
        style = case["style"]
        
        # Calculate coupling efficiency over the sweep
        eff = analytical_efficiency(displacements, w_i, FIBER_WAIST)
        
        # Calculate Decibel Loss: dB = 10 * log10(eta)
        # Avoid division-by-zero or log-of-zero
        eff_clipped = np.clip(eff, 1e-12, 1.0)
        db_loss = 10.0 * np.log10(eff_clipped)
        
        # Plot fractional efficiency
        ax1.plot(displacements * 1e6, eff, label=label, color=color, linestyle=style, linewidth=2)
        
        # Plot decibel loss
        ax2.plot(displacements * 1e6, db_loss, label=label, color=color, linestyle=style, linewidth=2)
        
    # Styling Top plot
    ax1.set_title("Single-Mode Fiber Coupling Efficiency vs. EOM Walk-off", fontsize=14, fontweight="bold", pad=15)
    ax1.set_ylabel("Coupling Efficiency $\\eta$", fontsize=12)
    ax1.set_xlim(0, 8)
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right", framealpha=0.9)
    
    # Add a horizontal indicator for 50% coupling efficiency
    ax1.axhline(0.5, color="gray", linestyle=":", alpha=0.5)
    
    # Styling Bottom plot
    ax2.set_xlabel("EOM Transients Beam Walk-off $\\Delta x$ ($\\mu$m)", fontsize=12)
    ax2.set_ylabel("Coupling Loss (dB)", fontsize=12)
    ax2.set_xlim(0, 8)
    ax2.set_ylim(-25, 0.5)
    ax2.grid(True, linestyle=":", alpha=0.6)
    
    # Add highlighting for standard walk-offs
    # For instance, a 2.0 um deflection is completely macroscopically invisible at system level,
    # yet translates to -1.3 dB to -2.0 dB transient transmission sags.
    ax2.axvspan(0.0, 2.0, color="#2ca02c", alpha=0.08, label="Micro-Steering Zone")
    ax2.legend(loc="lower left", framealpha=0.9)
    
    plt.tight_layout()
    
    # Save the output image
    output_path = os.path.join(os.path.dirname(__file__), "fiber_coupling_loss.png")
    plt.savefig(output_path, dpi=300)
    print(f"[OK] Coupling loss plot successfully saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    print("="*60)
    print("PHYSICAL OPTICS OVERLAP SIMULATOR — RUNNING VALIDATION")
    print("="*60)
    
    # Run tests to cross-verify numerical and analytical physics
    run_verification_tests()
    
    # Generate and save the coupling curves
    generate_overlap_plots()
    
    print("\n[DONE] Fiber overlap simulation pipeline successfully completed!")
    print("="*60)
