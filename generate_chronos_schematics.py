import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch

# Set up beautiful serif typography to match LaTeX documents
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Liberation Serif", "serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

def generate_assets():
    # Time-domain parameters
    t = np.linspace(0, 15, 1000)
    V_target = 400
    zeta = 0.12 # Damping ratio
    omega_n = 1.5 # Natural frequency
    omega_d = omega_n * np.sqrt(1 - zeta**2)

    # EOM voltage response
    V_t = V_target * (1 - np.exp(-zeta * omega_n * t) * (
        np.cos(omega_d * t) + (zeta / np.sqrt(1 - zeta**2)) * np.sin(omega_d * t)
    ))
    
    # Dynamic frequency chirp: dphi/dt proportional to dV/dt
    # dV/dt = V_target * [ zeta*omega_n * e^{-zeta*omega_n*t} * (...) - e^{-zeta*omega_n*t} * (-omega_d*sin + omega_d*zeta/sqrt(1-zeta^2)*cos) ]
    # Let's compute it numerically for simplicity and robustness
    dt = t[1] - t[0]
    dV_dt = np.gradient(V_t, dt)
    chirp = -0.5 * dV_dt  # Chirp in GHz or arbitrary scaling for visualization

    # Create side-by-side subplot with expanded size and wspace to eliminate overlaps
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.0))
    fig.subplots_adjust(wspace=0.45, left=0.08, right=0.92, top=0.88, bottom=0.12)

    # Panel A: Time-Domain EOM Voltage and Chirp
    ax1.plot(t, V_t, color='#d35400', linewidth=2.5, label='Actual $V(t)$')
    ax1.axhline(V_target, color='#2c3e50', linestyle='--', linewidth=1.5, label='Ideal Step ($400$ V)')
    
    # Second y-axis for the frequency chirp
    ax1_chirp = ax1.twinx()
    ax1_chirp.plot(t, chirp, color='#8e44ad', linewidth=2.0, linestyle=':', label='Frequency Chirp $\\Delta\\omega(t)$')
    ax1_chirp.set_ylabel('Induced Chirp $\\Delta\\omega(t)$ (GHz)', color='#8e44ad', labelpad=10)
    ax1_chirp.tick_params(axis='y', labelcolor='#8e44ad')
    ax1_chirp.spines['right'].set_color('#8e44ad')

    ax1.set_xlabel('Time $t$ (ns)')
    ax1.set_ylabel('EOM Driver Voltage $V(t)$ (V)')
    ax1.set_xlim(0, 15)
    ax1.set_ylim(0, 780)
    ax1.spines['top'].set_visible(False)
    ax1.grid(True, linestyle=':', alpha=0.5)
    # Center title to avoid overlap with connecting textbox
    ax1.set_title('(a) EOM Ringing and Dynamic Chirp', loc='center', pad=12, fontweight='bold')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_chirp.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right')

    # Panel B: Temporal Filter & Coincidence Window
    # X-axis represents photon arrival time relative to EOM edge (in picoseconds)
    t_ps = np.linspace(-400, 400, 1000)
    t_window = 150.0
    sigma_j = 100.0
    
    # Intrinsic arrival time distributions
    # Unshifted (ground state, e.g., setting a_prime = 0)
    y_unshifted = 1.0 / (sigma_j * np.sqrt(2 * np.pi)) * np.exp(-t_ps**2 / (2 * sigma_j**2))
    
    # Shifted (active state, e.g., setting a = pi/4 with +30 ps transient group delay)
    tau_shift = 30.0
    y_shifted = 1.0 / (sigma_j * np.sqrt(2 * np.pi)) * np.exp(-(t_ps - tau_shift)**2 / (2 * sigma_j**2))
    
    ax2.plot(t_ps, y_unshifted, color='#2980b9', linewidth=2.5, label='Unshifted $P(t|0)$')
    ax2.plot(t_ps, y_shifted, color='#c0392b', linewidth=2.5, linestyle='--', label='Shifted $P(t|\\pi/4)$')
    
    # Highlight Coincidence Window boundaries
    ax2.axvline(-t_window, color='#2c3e50', linestyle='-', linewidth=1.5)
    ax2.axvline(t_window, color='#2c3e50', linestyle='-', linewidth=1.5)
    
    # Shade Coincidence Window
    ax2.fill_between(t_ps, 0, np.maximum(y_unshifted, y_shifted), 
                     where=(t_ps >= -t_window) & (t_ps <= t_window), 
                     color='#2ecc71', alpha=0.15, label='Coincidence Window')
    
    # Annotate accepted/rejected region
    ax2.text(0, 0.0008, 'Coincidence Window\n$[-\\Delta t_{\\mathrm{window}}, \\Delta t_{\\mathrm{window}}]$', 
             ha='center', va='bottom', color='#27ae60', fontweight='bold', fontsize=9)
    
    # Rejection region annotation
    ax2.annotate('Loss of photons\ndue to shift', xy=(170, 0.0004), xytext=(220, 0.0018),
                 arrowprops=dict(facecolor='#c0392b', edgecolor='none', shrink=0.08, width=0.8, headwidth=5, headlength=5))
    
    ax2.set_xlabel('Photon Arrival Time Delay $\\tau$ (ps)')
    ax2.set_ylabel('Probability Density')
    ax2.set_xlim(-400, 400)
    ax2.set_ylim(0, 0.0048)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(True, linestyle=':', alpha=0.5)
    # Center title to avoid overlap with connecting textbox
    ax2.set_title('(b) Coincidence Window Filtering', loc='center', pad=12, fontweight='bold')
    # Relocate legend to upper right to prevent connection arrow overlap
    ax2.legend(loc='upper right')

    # Connection Patch: Voltage Chirp drives the Timing Window Shift
    con = ConnectionPatch(
        xyA=(peak_time := np.pi / omega_d, 673), 
        xyB=(tau_shift, 0.002), 
        coordsA="data", coordsB="data",
        axesA=ax1, axesB=ax2, 
        color="#8e44ad", linestyle=":", linewidth=2,
        arrowstyle="-|>", mutation_scale=15,
        clip_on=False
    )
    fig.add_artist(con)

    # Label the connection cleanly in the middle gap above the subplots to avoid crossing axes
    fig.text(0.5, 0.95, 'Ringing drives Ground Bounce\nand Dynamic PMD Split', 
             ha='center', va='center', color='#8e44ad', fontsize=9, 
             fontweight='bold', bbox=dict(facecolor='white', edgecolor='#8e44ad', boxstyle='round,pad=0.3', alpha=0.95))

    # Save outputs
    fig.savefig('Paper2/chronos_schematic.svg', format='svg', transparent=True)
    fig.savefig('Paper2/chronos_schematic.pdf', format='pdf', transparent=True, dpi=300)
    plt.close(fig)
    print("Paper 2 schematic assets regenerated successfully.")

if __name__ == '__main__':
    generate_assets()
