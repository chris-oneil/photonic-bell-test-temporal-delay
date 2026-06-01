# Technical Addendum: Physical Optics and Thermodynamic Bounding of Active Modulator Transients in Photonic Bell Tests

**Author:** Christopher O'Neil  
**Affiliation:** Independent Researcher, Big Rapids, MI, USA  
**Contact:** christopheroneil@gmail.com  
**Date:** June 2026

---

## Overview

This technical addendum supplements the parent manuscript (*Uncharacterized In-Situ Setting-Dependent Propagation Delay and Temporal Coincidence Bounds in Photonic Bell Tests*) with two independent physical analyses that resolve anticipated objections to the setting-dependent temporal selection framework.

### 1. Single-Mode Fiber Coupling and the Link-Loss Translation

We derive the complete 2D Gaussian spatial overlap integral at the post-EOM single-mode collection fiber facet. The key result is the **Link-Loss Translation**: lateral beam walk-off induced by EOM switching transients is not erased by the single-mode fiber — it is converted directly into a setting-dependent coupling attenuation, leaving the total-variation (TV) bounds on CHSH violations fully invariant.

**Script:** [`fiber_overlap.py`](fiber_overlap.py) — Computes and plots the coupling efficiency $\eta(\Delta x)$ as a function of EOM-induced lateral displacement for various beam waist parameters.

### 2. Thermodynamic Conduction Bounding of RTP Crystal Heating

We numerically solve the 1D heat diffusion equation for a capacitive RTP crystal under continuous and burst-mode switching. We prove that continuous 100 MHz switching yields a catastrophic steady-state center temperature rise of 20.94 K (causing 12.7 rad of phase drift), while the proposed **Burst-Mode Gated Calibration Protocol** bounds thermal fluctuations to $\Delta T \approx 10^{-4}$ K — nearly two orders of magnitude below the metrological safety threshold.

**Script:** [`thermal_model.py`](thermal_model.py) — Finite-difference PDE solver for the time-dependent heat equation with boundary conditions at copper holding jaws.

---

## Repository Contents

| File | Description |
|:---|:---|
| `Technical Addendum.pdf` | Compiled PDF of the full technical addendum |
| `main.tex` | LaTeX source |
| `fiber_overlap.py` | 2D Gaussian overlap integral computation and coupling loss curves |
| `fiber_overlap_math.md` | Step-by-step mathematical derivation of the overlap integral |
| `fiber_coupling_loss.png` | Generated figure: coupling efficiency vs. lateral walk-off |
| `thermal_model.py` | 1D heat diffusion PDE solver (continuous vs. burst-mode) |
| `thermal_burst_mode.png` | Generated figure: thermal response under burst-mode protocol |

---

## Requirements

- Python 3.x
- `numpy`
- `matplotlib`

---

## Usage

```bash
# Generate the fiber coupling loss figure
python fiber_overlap.py

# Generate the thermal burst-mode response figure
python thermal_model.py
```

---

## License

The physical optics and thermodynamic analysis scripts in this addendum are released under the **GNU GPL v3** license, consistent with the parent repository.
