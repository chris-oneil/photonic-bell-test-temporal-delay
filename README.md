# Paper 2: Uncharacterized In-Situ Setting-Dependent Propagation Delay and Temporal Coincidence Bounds in Photonic Bell Tests

This directory contains the manuscript, simulation code, and vector figures for Paper 2: **"Uncharacterized In-Situ Setting-Dependent Propagation Delay and Temporal Coincidence Bounds in Photonic Bell Tests"**.

It evaluates how active basis-switching transients in electro-optic modulators (EOMs) dynamically shift photon arrival times relative to the rigid software coincidence window ($2\Delta t_{\text{window}}$), acting as a physical, setting-dependent data selector that systematically bypasses classical Bell ceilings.

## Theoretical Background

In high-speed loophole-free Bell tests, active switching of EOMs draws sharp capacitive transient currents of up to **$2.0\text{ A}$**. This creates two compounding physical timing delay mechanisms that scale to the picosecond level:

1. **Driver-Induced Discriminator Jitter (Electronic):** The transient current draw induces local electronic ground bounce and rail sag within the shared receiver and TDC chassis. A $\approx 10\text{ mV}$ rail sag shifts comparator thresholds, which translates directly to a **$10\text{ to }100\text{ ps}$** time-tag delay.
2. **Dynamic PMD Splitting (Optical):** Underdamped polarization ringing projects the photon wavepacket across both the slow and fast axes of the birefringent routing fiber ($\approx 1.0\text{ to }1.5\text{ ps/m}$), splitting the wavepacket and shifting the arrival-time center of mass by **$10\text{ to }150\text{ ps}$**.

This shift pushes borderline photons outside the rigid temporal coincidence window, creating a physics-grounded instantiation of Pearle's data-rejection framework.

## Directory Structure

*   `main.tex`: The publication-grade LaTeX manuscript in `revtex4-2` format.
*   `chronos_simulation.py`: The Monte Carlo numerical integration script simulating the joint spatial-temporal filtering spaces.
*   `generate_chronos_schematics.py`: The Matplotlib script generating the multi-panel vector figures (`chronos_schematic.pdf` / `chronos_schematic.svg`).
*   `arxiv_submission.zip`: The pre-packaged zip archive containing all necessary sources for direct upload to arXiv.org.

## Running the Simulation

Execute the core numerical integration script to verify the unified spatial-temporal correlation bounds:

```bash
python chronos_simulation.py
```

### Simulation Scenarios & Physical Parameters

*   **Isotropic absorption efficiency ($\eta_{\text{base}}$):** $0.48$
*   **Spatial efficiency variation ($\eta_{\text{var}}$):** $0.52$
*   **Baseline SNSPD timing jitter ($\sigma_j$):** $100\text{ ps}$
*   **Coincidence half-width ($\Delta t_{\text{window}}$):** $500\text{ ps}$
*   **Peak EOM-induced delay shift ($\tau_{\max}$):** $150\text{ ps}$
*   **Expected Violation Ceiling:** $S_{\text{max}} \approx 2.264$ with total-variation distance supremum $\delta_{\text{sup}} \approx 0.199$.

## Generating the Figures

Regenerate the publication-grade multi-panel vector diagrams:

```bash
python generate_chronos_schematics.py
```

This updates both `chronos_schematic.pdf` and `chronos_schematic.svg`.
