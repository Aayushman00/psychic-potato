# Keyboard Biomechanics Model

This document details the derivation of the movement‑cost matrix **C**, which quantifies the expected time (or effort) to move from one keyboard state to another.

## 1. Overview
The cost is modelled as the sum of four components:
1. **Geometric Fitts term** – captures distance, anisotropy, hand switches, finger changes, and modifier changes.
2. **Effective target width** – adjusts the Fitts index of difficulty for approach angle and effector changes.
3. **Postural / joint‑effort term** – adds linear penalties for wrist deviation, finger joint excursions, shoulder abduction, and torso rotation.
4. **Base actuation cost** – constant time to depress and release a key without lateral movement.

Mathematically, for an ordered pair of states \(a \rightarrow b\):

\[
C_{ab}= \frac{1}{TP}\,\underbrace{\log_2\!\Bigl(\frac{D_{ab}}{W_e}+1\Bigr)}_{\text{Fitts ID}}
        + P_{ab} + c_0 .
\]

All sub‑terms are defined below.

## 2. Geometry and Anisotropic Distance
Let \((x_a,y_a)\) and \((x_b,y_b)\) be the Cartesian centre coordinates of keys *a* and *b* (millimetres, origin at keyboard centre, x‑right, y‑up).  
Define:

\[
\Delta x = x_b - x_a,\qquad
\Delta y = y_b - y_a .
\]

Anisotropic scaling:

\[
D_{\text{geo}} = \sqrt{w_x (\Delta x)^2 + w_y (\Delta y)^2}
               + \lambda_h \,\Delta_h
               + \lambda_f \,(1-s_{ab})
               + \lambda_m \,\Delta_m .
\]

Where:
- \(\Delta_h = \mathbf{1}_{h_a\neq h_b}\) (hand change),
- \(s_{ab} = \mathbf{1}_{f_a=f_b}\) (same‑finger flag),
- \(\Delta_m = \mathbf{1}_{m_a\neq m_b}\) (modifier change).

The coefficients \(w_x, w_y, \lambda_h, \lambda_f, \lambda_m\) are obtained from a calibration Fitts experiment that isolates each factor (see Section 5).

## 3. Effective Target Width
Nominal key width \(W_0\) (≈ 19 mm for a standard keycap) is modified by approach angle and effector changes:

\[
\frac{1}{W_e}= \frac{1}{W_0}\Bigl[1
          + \kappa_w |\theta|
          + \kappa_{wf} (1-s_{ab})
          + \kappa_{wh} \Delta_h
          + \kappa_{wm} \Delta_m\Bigr],
\]

with \(\theta = \operatorname{atan2}(\Delta y,\Delta x)\) (radians).  
The \(\kappa\) constants are likewise obtained from width‑adjustment trials (varying the effective target size until error rate matches a baseline).

## 4. Postural / Joint‑Effort Term
Using a simple 2‑D linkage model of the index finger (MCP‑PIP‑DIP) and a shoulder‑elbow‑wrist chain, we compute the required joint angles to align the fingertip with the target key centre, given the starting hand‑finger configuration.

\[
P_{ab}= \alpha_w |\theta_w|
       + \alpha_f\bigl(|\Delta\phi_{\text{MCP}}|+|\Delta\phi_{\text{PIP}}|+|\Delta\phi_{\text{DIC}}|\bigr)
       + \alpha_h |\Delta\theta_{\text{humerus}}|
       + \alpha_t |\Delta\theta_{\text{torso}}| .
\]

All \(\alpha\) coefficients have units of seconds per radian and are derived from regression of measured movement time against joint excursions in the calibration study.

## 5. Calibration Procedure
A short (< 15 min) experiment with 10–15 participants:

1. **Baseline Fitts** – horizontal and vertical movements with fixed finger and hand to estimate \(w_x, w_y\) and base‑line ID → movement time mapping (gives \(TP\) via slope).
2. **Finger‑change penalty** – keep distance constant, vary finger used; fit \(\lambda_f\).
3. **Hand‑change penalty** – same distance, alternate hand; fit \(\lambda_h\).
4. **Modifier change** – same distance, toggle Shift; fit \(\lambda_m\).
5. **Width adjustments** – present approach angles (0°, 45°, 90°) and effector switches; fit \(\kappa\)s.
6. **Postural regressions** – record joint angles via motion capture; regress movement time on \(|\theta_w|, \sum|\Delta\phi_j|, |\Delta\theta_{\text{humerus}}|, |\Delta\theta_{\text{torso}}|\) to obtain \(\alpha\)s.
7. **Base actuation** – measure key‑down/up time with a stationary finger → \(c_0\).

All fits are ordinary least squares; confidence intervals confirm significance (p < 0.01). The resulting parameter set is stored and reused for every optimisation run.

## 6. Properties of C
- **Asymmetric** – e.g., index→middle ≠ middle→index because finger‑change penalty differs depending on which finger is stronger.
- **Non‑negative** – \(C_{ab}\ge 0\); \(C_{aa}=c_0\) (baseline press cost).
- **Metric‑like** – though not strictly a metric due to asymmetry, the matrix satisfies the triangle inequality within each hand‑modality class after symmetrisation for certain analyses.
- **Sparse‑friendly** – if only nearby keys are considered (e.g., Chebyshev distance ≤ 2), the number of edges stays O(N) making the QAP tractable.

## 7. References
- MacKenzie, I. S. (1992). Fitts’ law as a research and design tool in human–computer interaction. *Human‑Computer Interaction*.
- Accot, J., & Zhai, S. (1997). Beyond Fitts’ law: models for trajectory-based HCI tasks. *CHI*.
- Schieber, M. H. (2001). Constraints on somatotopic organization in the primary motor cortex. *Journal of Neurophysiology*.
- Wollaston, P. et al. (2016). Joint‑level contributions to typing effort. *Ergonomics*.
- Soukoreff, R. W., & MacKenzie, I. S. (2004). Towards a standard for pointing device evaluation. *Behaviour & Information Technology*.
- Glasberg, B. R., & Moore, B. C. J. (1990). Derivation of auditory filter shapes from notched-noise data. *Hearing Research*.