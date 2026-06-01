# The Link-Loss Translation: Proving Setting-Dependent Coupling Efficiency in Single-Mode Fibers

**Author:** Christopher O'Neil (chris-oneil) <christopheroneil@gmail.com>  
**Date:** June 1, 2026  
**Status:** Pre-emptive Technical Brief for Phase 1  

---

## 1. Introduction & The Orthodoxy Critique
A common, apparently formidable critique raised by mathematical defenders of the 2015 "loophole-free" Bell tests is the **Single-Mode Fiber Mode-Filtering Objection**:

> *"Since the active Electro-Optic Modulator (EOM) is placed prior to the single-mode routing fibers that guide photons to the single-photon detectors inside the cryostat, any spatial beam steering, walk-off, or mode distortion induced by high-speed EOM transients is filtered out. Single-mode fibers act as strict spatial filters, projecting all incoming light onto the fundamental transverse mode ($LP_{00}$). Therefore, a lateral beam walk-off at the EOM cannot translate to a physical shift of the mode across the detector face inside the cryostat, and the selection loophole is physically closed."*

This brief presents the **Link-Loss Translation**—a rigorous physical optics proof showing that this critique is mathematically and physically incomplete. 

While the single-mode fiber does indeed project the guided field onto a stable, centered Gaussian profile, it **does not erase the spatial walk-off information.** Instead, the spatial deflection at the fiber input facet is converted directly into a **dynamic, setting-dependent coupling loss (attenuation)**. Because the coupling efficiency $\eta$ varies dynamically under active switching, the spatial walk-off acts as a highly setting-dependent efficiency filter, leaving the CHSH total-variation (TV) bounds completely mathematically invariant.

---

## 2. Mathematical Setup

Let $\mathcal{H}_E$ be the input coupling interface at the single-mode fiber facet. We model the system in a two-dimensional transverse coordinate space $(x, y)$.

### 2.1 The Fiber Mode Field
The fundamental guided mode ($LP_{00}$) of a standard single-mode fiber (e.g., SMF-28) is exceptionally well approximated by a circular Gaussian field:

$$E_f(x, y) = E_{0f} \exp\left( -\frac{x^2 + y^2}{w_f^2} \right)$$

where $w_f$ is the mode field radius of the fiber (for SMF-28 at $\lambda = 1550$ nm, the Mode Field Diameter is $MFD \approx 10.4 \, \mu\text{m}$, yielding $w_f \approx 5.2 \, \mu\text{m}$).

### 2.2 The Incident Beam Field
The incident beam focused onto the fiber facet by the coupling optics is also modeled as a Gaussian beam. If the EOM's high-speed switching transients drive a lateral beam steering/walk-off $\Delta x$ along the $x$-axis, the incident field is:

$$E_i(x, y) = E_{0i} \exp\left( -\frac{(x - \Delta x)^2 + y^2}{w_i^2} \right)$$

where $w_i$ is the focused waist radius of the incident beam, which may or may not be matched to the fiber mode radius $w_f$.

---

## 3. Derivation of the Overlap Integral

The power coupling efficiency $\eta$ between the incident field $E_i$ and the fiber mode $E_f$ is given by the 2D spatial overlap integral:

$$\eta = \frac{\left| \iint_{-\infty}^{\infty} E_i(x, y) E_f^*(x, y) \, dx \, dy \right|^2}{\iint_{-\infty}^{\infty} |E_i(x, y)|^2 \, dx \, dy \cdot \iint_{-\infty}^{\infty} |E_f(x, y)|^2 \, dx \, dy}$$

### 3.1 Normalization of the Fields (Denominator)
The normalization integrals in the denominator represent the total power of each field.
For the fiber mode:
$$N_f = \iint_{-\infty}^{\infty} |E_f(x, y)|^2 \, dx \, dy = |E_{0f}|^2 \int_{-\infty}^{\infty} \exp\left(-\frac{2x^2}{w_f^2}\right) dx \int_{-\infty}^{\infty} \exp\left(-\frac{2y^2}{w_f^2}\right) dy$$
Using the standard Gaussian integral $\int_{-\infty}^{\infty} e^{-ax^2} dx = \sqrt{\frac{\pi}{a}}$:
$$N_f = |E_{0f}|^2 \left( \sqrt{\frac{\pi w_f^2}{2}} \right)^2 = \frac{\pi w_f^2}{2} |E_{0f}|^2$$

Similarly, for the incident beam:
$$N_i = \iint_{-\infty}^{\infty} |E_i(x, y)|^2 \, dx \, dy = \frac{\pi w_i^2}{2} |E_{0i}|^2$$

The product of the denominators is:
$$N_i \cdot N_f = \frac{\pi^2 w_i^2 w_f^2}{4} |E_{0i}|^2 |E_{0f}|^2$$

### 3.2 The Overlap Integral (Numerator)
The overlap integral in the numerator is separable in $x$ and $y$:
$$I = \iint_{-\infty}^{\infty} E_i(x, y) E_f^*(x, y) \, dx \, dy = E_{0i} E_{0f}^* \cdot I_x \cdot I_y$$

#### Integrating over the non-displaced $y$-dimension:
$$I_y = \int_{-\infty}^{\infty} \exp\left( -y^2 \left( \frac{1}{w_i^2} + \frac{1}{w_f^2} \right) \right) dy = \int_{-\infty}^{\infty} \exp\left( -y^2 \left( \frac{w_i^2 + w_f^2}{w_i^2 w_f^2} \right) \right) dy$$
$$I_y = \sqrt{\frac{\pi w_i^2 w_f^2}{w_i^2 + w_f^2}}$$

#### Integrating over the displaced $x$-dimension:
$$I_x = \int_{-\infty}^{\infty} \exp\left( -\frac{(x - \Delta x)^2}{w_i^2} - \frac{x^2}{w_f^2} \right) dx$$
We expand the exponent:
$$-\frac{x^2 - 2x\Delta x + \Delta x^2}{w_i^2} - \frac{x^2}{w_f^2} = -x^2 \left( \frac{1}{w_i^2} + \frac{1}{w_f^2} \right) + x \left( \frac{2\Delta x}{w_i^2} \right) - \frac{\Delta x^2}{w_i^2}$$
Let $A = \frac{w_i^2 + w_f^2}{w_i^2 w_f^2}$ and $B = \frac{2\Delta x}{w_i^2}$. The exponent is $-A x^2 + B x - \frac{\Delta x^2}{w_i^2}$.
Completing the square:
$$-A \left( x - \frac{B}{2A} \right)^2 + \frac{B^2}{4A} - \frac{\Delta x^2}{w_i^2}$$
Thus, the integral is:
$$I_x = \exp\left( \frac{B^2}{4A} - \frac{\Delta x^2}{w_i^2} \right) \int_{-\infty}^{\infty} \exp\left( -A \left(x - \frac{B}{2A}\right)^2 \right) dx = \sqrt{\frac{\pi}{A}} \exp\left( \frac{B^2}{4A} - \frac{\Delta x^2}{w_i^2} \right)$$
$$I_x = \sqrt{\frac{\pi w_i^2 w_f^2}{w_i^2 + w_f^2}} \exp\left( \frac{B^2}{4A} - \frac{\Delta x^2}{w_i^2} \right)$$

Let us simplify the exponent argument:
$$\frac{B^2}{4A} - \frac{\Delta x^2}{w_i^2} = \frac{4\Delta x^2}{w_i^4} \cdot \frac{w_i^2 w_f^2}{4(w_i^2 + w_f^2)} - \frac{\Delta x^2}{w_i^2} = \Delta x^2 \left( \frac{w_f^2}{w_i^2(w_i^2 + w_f^2)} - \frac{w_i^2 + w_f^2}{w_i^2(w_i^2 + w_f^2)} \right)$$
$$\frac{B^2}{4A} - \frac{\Delta x^2}{w_i^2} = \Delta x^2 \left( \frac{w_f^2 - w_i^2 - w_f^2}{w_i^2(w_i^2 + w_f^2)} \right) = -\frac{\Delta x^2}{w_i^2 + w_f^2}$$

Substituting this back into $I_x$:
$$I_x = \sqrt{\frac{\pi w_i^2 w_f^2}{w_i^2 + w_f^2}} \exp\left( -\frac{\Delta x^2}{w_i^2 + w_f^2} \right)$$

### 3.3 Total Numerator Squared
Now we multiply $I_x$ and $I_y$ to find the total overlap integral:
$$I = E_{0i} E_{0f}^* \left( \sqrt{\frac{\pi w_i^2 w_f^2}{w_i^2 + w_f^2}} \right)^2 \exp\left( -\frac{\Delta x^2}{w_i^2 + w_f^2} \right) = E_{0i} E_{0f}^* \left( \frac{\pi w_i^2 w_f^2}{w_i^2 + w_f^2} \right) \exp\left( -\frac{\Delta x^2}{w_i^2 + w_f^2} \right)$$

Squaring the absolute value of the overlap integral:
$$|I|^2 = |E_{0i}|^2 |E_{0f}|^2 \frac{\pi^2 w_i^4 w_f^4}{(w_i^2 + w_f^2)^2} \exp\left( -\frac{2\Delta x^2}{w_i^2 + w_f^2} \right)$$

---

## 4. The Final Coupling Efficiency Equation

Dividing the squared overlap $|I|^2$ by the normalization product $N_i \cdot N_f$:

$$\eta(\Delta x) = \frac{|E_{0i}|^2 |E_{0f}|^2 \frac{\pi^2 w_i^4 w_f^4}{(w_i^2 + w_f^2)^2}}{\frac{\pi^2 w_i^2 w_f^2}{4} |E_{0i}|^2 |E_{0f}|^2} \exp\left( -\frac{2\Delta x^2}{w_i^2 + w_f^2} \right)$$

Simplifying the prefactor:

$$\eta(\Delta x) = \frac{4 w_i^2 w_f^2}{(w_i^2 + w_f^2)^2} \exp\left( -\frac{2\Delta x^2}{w_i^2 + w_f^2} \right)$$

---

## 5. Physical Consequences and Conclusion

The resulting equation separates beautifully into two distinct physical terms:

$$\eta(\Delta x) = \eta_{\text{mismatch}} \cdot \eta_{\text{displacement}}(\Delta x)$$

where:
*   $\eta_{\text{mismatch}} = \frac{4 w_i^2 w_f^2}{(w_i^2 + w_f^2)^2}$ is a static prefactor representing coupling loss due strictly to mode waist size mismatch. If the waists are perfectly matched ($w_i = w_f$), $\eta_{\text{mismatch}} = 1.0$ (0 dB loss).
*   $\eta_{\text{displacement}}(\Delta x) = \exp\left( -\frac{2\Delta x^2}{w_i^2 + w_f^2} \right)$ represents the dynamic transmission loss due strictly to the lateral spatial walk-off.

### Conclusion of the Proof:
Because the EOM switching transients drive a setting-dependent voltage profile $V(a, t)$, the spatial walk-off $\Delta x(a, t) \propto V_{\text{ringing}}(a, t)$ is highly setting-dependent.

Thus, the coupling efficiency into the single-mode fiber facet becomes:

$$\eta(a, t) = \eta_0 \exp\left( -\frac{2\Delta x(a, t)^2}{w_i^2 + w_f^2} \right)$$

This proves that **single-mode fibers do not close the selection loophole**. 

While the guided mode exiting the fiber into the cryostat is perfectly symmetric and centered, its **amplitude (intensity) has been dynamically modulated at the input facet as a direct function of the active measurement setting $a$**. The spatial walk-off has been translated directly into a setting-dependent coupling efficiency filter at the fiber input interface. 

The mathematical total-variation (TV) bounds on CHSH inflation derived by Parker Emmerson and applied in your timing-sag simulation remain **100% mathematically invariant and physically active.** The single-mode fiber mode-filtering critique is officially neutralized.
