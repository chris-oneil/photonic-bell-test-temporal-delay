#!/usr/bin/env python3
"""
EOM Crystal Thermodynamic Solver & Burst-Mode Simulator
=========================================================
Numerically solves the 1D heat equation in a Rubidium Titanyl Phosphate (RTP) EOM crystal
under active basis-switching dielectric losses.

Compares continuous switching vs. the proposed Burst-Mode Audit Protocol.
Proves that the Burst-Mode Audit Protocol bounds crystal temperature drift
to a stochastically and metrologically negligible level (Delta T <= 0.01 K),
bypassing the "circularity trap" of EOM thermal index drifts.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# Calibrated Physical Constants for RTP (Rubidium Titanyl Phosphate)
# ==============================================================================
RTP_DENSITY = 3600.0          # rho = 3.6 g/cm^3 = 3600 kg/m^3
RTP_SPECIFIC_HEAT = 690.0     # Cp = 690 J/(kg*K)
# RTP is anisotropic: K_x ~ 2.0, K_y ~ 3.0, K_z ~ 3.3 W/(m*K).
# K = 3.0 W/(m*K) corresponds to the specific crystallographic axis (e.g., y-axis) along the transverse conduction path.
RTP_CONDUCTIVITY = 3.0        # K = 3.0 W/(m*K)
RTP_DIFFUSIVITY = RTP_CONDUCTIVITY / (RTP_DENSITY * RTP_SPECIFIC_HEAT) # alpha = K / (rho * Cp)

# EOM Electrical Parameters
CRYSTAL_CAPACITANCE = 10e-12   # C = 10 pF
SWITCHING_VOLTAGE = 400.0      # V = 400 V
LOSS_TANGENT = 0.005           # tan(delta) = 0.005 for RTP at 100 MHz
BURST_FREQUENCY = 100e6        # f = 100 MHz during active burst

# Crystal Geometry (Standard Aperture EOM)
CRYSTAL_WIDTH = 3.0e-3         # W = 3 mm (heat conducts to copper jaws at x=0 and x=W)
CRYSTAL_HEIGHT = 3.0e-3        # H = 3 mm
CRYSTAL_LENGTH = 10.0e-3       # L = 10 mm
CRYSTAL_VOLUME = CRYSTAL_WIDTH * CRYSTAL_HEIGHT * CRYSTAL_LENGTH
CRYSTAL_MASS = RTP_DENSITY * CRYSTAL_VOLUME

# Ambient Thermal Boundaries
T_AMBIENT = 293.15             # 20 deg C (infinite copper heat sink jaws at boundaries)

# Calculate active power dissipation during continuous 100 MHz switching
P_ACTIVE = 2.0 * np.pi * BURST_FREQUENCY * CRYSTAL_CAPACITANCE * (SWITCHING_VOLTAGE**2) * LOSS_TANGENT
Q_VOLUMETRIC = P_ACTIVE / CRYSTAL_VOLUME  # W/m^3 uniform volumetric heat source

# Realistic continuous switching steady-state temperature under 1D heat conduction:
# T_max = T_ambient + q * W^2 / (8 * K)
T_MAX_STEADY_STATE = T_AMBIENT + (Q_VOLUMETRIC * (CRYSTAL_WIDTH**2)) / (8.0 * RTP_CONDUCTIVITY)

print("="*60)
print("RTP EOM THERMODYNAMIC SOLVER — PARAMETERS")
print("="*60)
print(f"Active Dielectric Loss Power (P_active): {P_ACTIVE:.3f} W")
print(f"Volumetric Heat Generation (q):          {Q_VOLUMETRIC:.2e} W/m^3")
print(f"RTP Thermal Diffusivity (alpha):         {RTP_DIFFUSIVITY:.2e} m^2/s")
print(f"Crystal mass:                            {CRYSTAL_MASS*1e3:.3f} grams")
print(f"Continuous Steady-State Temp (Conduction): {T_MAX_STEADY_STATE:.2f} K ({T_MAX_STEADY_STATE - 273.15:.2f} °C)")
print("="*60)


def solve_continuous_adiabatic_drift(time_horizon=5.0):
    """Calculates continuous adiabatic temperature rise (no heat conduction)."""
    t = np.linspace(0, time_horizon, 100)
    # dT/dt = P_active / (mass * Cp)
    dT_dt = P_ACTIVE / (CRYSTAL_MASS * RTP_SPECIFIC_HEAT)
    T = T_AMBIENT + dT_dt * t
    return t, T, dT_dt


def solve_heat_equation_burst_mode(num_cycles=5, N_x=60):
    """
    Numerically solves the 1D Heat Equation with boundary conditions T(0,t) = T(W,t) = T_ambient.
    Uses an explicit finite-difference scheme with adaptive time-stepping:
      - Tiny time-steps during the active burst (to resolve rapid nanosecond heating).
      - Larger time-steps during the cooling window (for computational efficiency).
    
    Audit Protocol Duty Cycle:
      - Burst: N_b = 100 pulses at 100 MHz (t_burst = 1 us).
      - Cooling: t_cool = 10 ms.
    """
    t_burst = 1.0e-6    # 1 microsecond active switching burst
    t_cool = 10.0e-3    # 10 milliseconds cooling period
    t_cycle = t_burst + t_cool
    
    # Spatial discretization
    dx = CRYSTAL_WIDTH / (N_x - 1)
    x = np.linspace(0, CRYSTAL_WIDTH, N_x)
    
    # Initialize temperature array to ambient
    T = np.full(N_x, T_AMBIENT)
    
    # Pre-allocate tracking arrays
    time_history = []
    T_center_history = []
    
    # Temporal steps count
    steps_burst = 50
    dt_burst = t_burst / steps_burst
    
    steps_cool = 100
    dt_cool = t_cool / steps_cool
    
    # Verify explicit stability criteria for the cooling time step
    # Fourier number Fo = alpha * dt / dx^2 must be <= 0.5
    fo_cool = RTP_DIFFUSIVITY * dt_cool / (dx**2)
    if fo_cool > 0.5:
        # Auto-adjust spatial grid or cooling steps to remain stable
        steps_cool = int(np.ceil(RTP_DIFFUSIVITY * t_cool / (0.45 * dx**2)))
        dt_cool = t_cool / steps_cool
        fo_cool = RTP_DIFFUSIVITY * dt_cool / (dx**2)
        
    fo_burst = RTP_DIFFUSIVITY * dt_burst / (dx**2)
    
    t_curr = 0.0
    
    # Loop over active burst-cooling cycles
    for cycle in range(num_cycles):
        # 1. ACTIVE BURST PHASE (1 us, Volumetric heating active)
        q_source = Q_VOLUMETRIC
        for _ in range(steps_burst):
            T_new = np.copy(T)
            # Finite difference update
            for i in range(1, N_x - 1):
                diffusion = RTP_DIFFUSIVITY * (T[i+1] - 2.0*T[i] + T[i-1]) / (dx**2)
                generation = q_source / (RTP_DENSITY * RTP_SPECIFIC_HEAT)
                T_new[i] = T[i] + dt_burst * (diffusion + generation)
            
            # Enforce Dirichlet boundary conditions (chassis jaws at constant T)
            T_new[0] = T_AMBIENT
            T_new[-1] = T_AMBIENT
            
            T = T_new
            t_curr += dt_burst
            
            time_history.append(t_curr)
            T_center_history.append(T[N_x // 2])
            
        # 2. COOLING PHASE (10 ms, Volumetric heating off)
        q_source = 0.0
        for _ in range(steps_cool):
            T_new = np.copy(T)
            for i in range(1, N_x - 1):
                diffusion = RTP_DIFFUSIVITY * (T[i+1] - 2.0*T[i] + T[i-1]) / (dx**2)
                T_new[i] = T[i] + dt_cool * diffusion
            
            T_new[0] = T_AMBIENT
            T_new[-1] = T_AMBIENT
            
            T = T_new
            t_curr += dt_cool
            
            time_history.append(t_curr)
            T_center_history.append(T[N_x // 2])
            
    return np.array(time_history), np.array(T_center_history), x, T


def run_thermodynamic_analysis():
    # 1. Solve Continuous Adiabatic case
    t_cont, T_cont, dT_dt = solve_continuous_adiabatic_drift(time_horizon=2.0)
    
    # 2. Solve Burst-Mode case
    num_cycles = 5
    t_burst, T_burst, x, T_final = solve_heat_equation_burst_mode(num_cycles=num_cycles)
    
    # Find maximum thermal fluctuation
    max_T = np.max(T_burst)
    delta_T_max = max_T - T_AMBIENT
    
    print("\n[SIM] Simulation completed.")
    print(f"  Continuous Adiabatic Heating Rate: {dT_dt:.2f} K/s")
    print(f"  Continuous Temp after 2.0 seconds: {T_cont[-1]:.2f} K ({T_cont[-1]-273.15:.2f} °C)")
    print(f"  Continuous Steady-State Temp (Conduction): {T_MAX_STEADY_STATE:.2f} K ({T_MAX_STEADY_STATE - 273.15:.2f} °C)")
    print(f"  Burst-Mode Max Fluctuation (dT):   {delta_T_max:.6f} K")
    print("="*60)
    
    # Validate the Burst-Mode threshold
    assert delta_T_max < 0.01, f"Validation failed! Burst-mode thermal sag ({delta_T_max:.4f} K) exceeded 0.01 K safety limit."
    print("[OK] Burst-mode thermodynamic safety criteria validated (Delta T <= 0.01 K).")
    
    # ==========================================================================
    # Generate Publication-Quality Plots
    # ==========================================================================
    plt.figure(figsize=(12, 10))
    
    # Subplot 1: Continuous vs. Burst-Mode Comparison (Log-scale split)
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(t_cont, T_cont - 273.15, label="Continuous 100 MHz Switching", color="#d62728", linewidth=2.5)
    ax1.plot(t_burst, T_burst - 273.15, label="Proposed Burst-Mode Audit Protocol", color="#2ca02c", linewidth=2.0)
    ax1.set_title("EOM Thermodynamic Behavior: Continuous vs. Gated Burst-Mode", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Time (seconds)", fontsize=11)
    ax1.set_ylabel("Temperature (°C)", fontsize=11)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")
    
    # Subplot 2: Detailed Microscopic View of Burst-Mode Fluctuations
    ax2 = plt.subplot(2, 1, 2)
    # Plot only burst-mode temperature change in milli-Kelvin
    ax2.plot(t_burst * 1e3, (T_burst - T_AMBIENT) * 1e3, color="#2ca02c", linewidth=2.0, label=r"Crystal Center Temp ($\Delta T$)")
    ax2.set_title("Microscopic Fluctuation of Crystal Center (Burst-Mode)", fontsize=13, fontweight="bold")
    ax2.set_xlabel("Time (milliseconds)", fontsize=11)
    ax2.set_ylabel(r"Temperature Rise $\Delta T$ (mK)", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.6)
    
    # Shade active burst regions (first 1 us of every 10 ms cycle)
    t_cycle_ms = 10.001  # cycle length in ms
    for cycle in range(num_cycles):
        ax2.axvspan(cycle * t_cycle_ms, cycle * t_cycle_ms + 0.1, color="#d62728", alpha=0.15)
    # Add annotation for the burst pulses
    ax2.annotate("Active Burst\n(100 pulses, 1 μs)", xy=(0.05, delta_T_max*800), xytext=(1.5, delta_T_max*700),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.2),
                 fontsize=9, color="#d62728", fontweight="bold")
                 
    ax2.legend(loc="upper right")
    
    plt.tight_layout()
    
    output_path = os.path.join(os.path.dirname(__file__), "thermal_burst_mode.png")
    plt.savefig(output_path, dpi=300)
    print(f"[OK] Thermodynamic analysis plot saved to: {output_path}")
    plt.close()


if __name__ == "__main__":
    run_thermodynamic_analysis()
