# Mathematical Formulation

## Sets and Notation
- Let \( \mathcal{P} = \{p_1,\dots,p_N\} \) be the set of piano notes (e.g., \(N=88\) or a subset for the MVP).  
- Let \( \mathcal{K} = \{k_1,\dots,k_M\} \) be the set of keyboard states (each state = a specific key on the laptop, possibly with a modifier layer).  
- Decision variable: binary assignment matrix \( X \in \{0,1\}^{N\times M} \) where  
  \[
  X_{ij}=1 \iff p_i \text{ is mapped to } k_j .
  \]

## Constraints (Injective Mapping)
\[
\begin{aligned}
\sum_{j=1}^{M} X_{ij} &= 1 &&\forall i\in\{1,\dots,N\} \quad\text{(each note assigned)}\\
\sum_{i=1}^{N} X_{ij} &\le 1 &&\forall j\in\{1,\dots,M\} \quad\text{(no key receives >1 note)}\\
X_{ij} &\in \{0,1\} &&\forall i,j .
\end{aligned}
\]
If \(M \ge N\) the inequality allows unused keys; for a strict bijection replace “\(\le\)” with “\(=\)”.

## Parameters
### Musical Relationship Matrix \(W\)
- \(W\in\mathbb{R}_{\ge0}^{N\times N}\), symmetric, with zero diagonal.  
- Defined as the inverse of sensory dissonance (see *Derivation of W* below).  

### Biomechanical Cost Matrix \(C\)
- \(C\in\mathbb{R}_{\ge0}^{M\times M}\), generally **asymmetric**.  
- \(C_{ab}\) = predicted movement time (seconds) to go from keyboard state \(a\) to state \(b\).  
- Derived from a Fitts‑type model with finger‑, hand‑, modifier‑, and postural terms (see *Derivation of C* below).

## Objective Function
\[
\boxed{
\displaystyle
\min_{X}\; \sum_{i=1}^{N}\sum_{j=1}^{N}
   W_{ij}\; C_{\; \bigl(\sum_{k} k\,X_{ik}\bigr),\; \bigl(\sum_{\ell} \ell\,X_{j\ell}\bigr)}
}
\]
Using the induced mapping \(f(i)=\sum_{k}k\,X_{ik}\) (the index of the keyboard state assigned to note \(i\)), this is equivalently
\[
\min_{f\ \text{injective}}\; \sum_{i,j} W_{ij}\; C_{f(i),f(j)} .
\]

This is a **Quadratic Assignment Problem (QAP)**: minimise the weighted sum of pairwise distances (here, movement costs) between two weighted graphs.

---


### Derivation of \(W\) (Musical‑Relationship Matrix)

1. **Pitch‑class distance**  
   For notes \(p_i,p_j\) with MIDI numbers \(m_i,m_j\),  
   \[
   \Delta_{ij}= \min\bigl\{|m_i-m_j|,\;12-|m_i-m_j|\bigr\}\in\{0,\dots,6\}.
   \]

2. **Frequency ratio (12‑TET)**  
   \[
   r_{ij}=2^{\Delta_{ij}/12}.
   \]

3. **Sensory dissonance (Plomp‑Levelt model)**  
   \[
   D(r_{ij}) = \sum_{k=1}^{K}\sum_{\ell=1}^{L}
      A_k A_\ell\,
      \exp\!\bigl[-b_1\,|kF_i-\ell F_j|\bigr]\,
      \bigl[1-\exp\!\bigl(-b_2\,|kF_i-\ell F_j|\bigr)\bigr],
   \]
   where  
   - \(F_i = 440\cdot2^{(m_i-69)/12}\) Hz,  
   - \(A_k\propto 1/k^{2}\) (typical piano harmonic envelope),  
   - \(b_1 = 2/\operatorname{ERB}(1000)\), \(b_2 = 1/\operatorname{ERB}(1000)\),  
   - \(\operatorname{ERB}(F)=24.7\bigl(4.37\,F/1000+1\bigr)\) Hz (Glasberg & Moore, 1990).  

4. **Weight definition**  
   \[
   W_{ij}= \frac{1}{D(r_{ij})}, \qquad W_{ii}=0 .
   \]
   No additional scaling constants are needed; any global factor cancels in the QAP objective.

---

### Derivation of \(C\) (Biomechanical Movement‑Cost Matrix)

For an ordered pair of keyboard states \(a\rightarrow b\):

1. **Geometric term** (Fitts‑type)
   \[
   D_{ab}= \sqrt{w_x(\Delta x)^2 + w_y(\Delta y)^2}
           + \lambda_h\,\Delta_h
           + \lambda_f\,(1-s_{ab})
           + \lambda_m\,\Delta_m,
   \]
   where  
   - \(\Delta x = x_b-x_a,\;\Delta y = y_b-y_a\) (mm),  
   - \(w_x,w_y\) are anisotropic scaling factors (obtained from horizontal/vertical Fitts fits),  
   - \(\Delta_h = \mathbf{1}_{h_a\neq h_b}\) (hand change),  
   - \(s_{ab} = \mathbf{1}_{f_a=f_b}\) (same‑finger flag),  
   - \(\Delta_m = \mathbf{1}_{m_a\neq m_b}\) (modifier change).

2. **Effective target width**
   \[
   \frac{1}{W_e}= \frac{1}{W_0}\Bigl[1
          + \kappa_w|\theta|
          + \kappa_{wf}(1-s_{ab})
          + \kappa_{wh}\Delta_h
          + \kappa_{wm}\Delta_m\Bigr],
   \]
   with \(\theta = \operatorname{atan2}(\Delta y,\Delta x)\) and \(W_0\) the nominal key width (~19 mm).

3. **Index of difficulty**
   \[
   \text{ID}_{ab}= \log_2\!\left(\frac{D_{ab}}{W_e}+1\right).
   \]

4. **Postural / joint‑effort term**
   \[
   P_{ab}= \alpha_w|\theta_w|
          + \alpha_f\sum_{j\in\{\text{MCP},\text{PIP},\text{DIP}\}}|\Delta\phi_j|
          + \alpha_h|\Delta\theta_{\text{humerus}}|
          + \alpha_t|\Delta\theta_{\text{torso}}|,
   \]
   where the angle terms are obtained via a 2‑D inverse‑kinematics model of the finger‑hand‑arm chain given the start and end key centres and the prescribed finger/hand.

5. **Base actuation cost**
   \[
   c_0 = \text{average key‑down/up time for a stationary finger}.
   \]

6. **Movement time**
   \[
   C_{ab}= \frac{1}{TP}\,\text{ID}_{ab} + P_{ab} + c_0 .
   \]

All coefficients (\(TP,w_x,w_y,\lambda_{\*},\kappa_{\*},\alpha_{\*},c_0\)) are estimated from a short calibration experiment (see *Methodology*). No ad‑hoc constants remain after calibration.

---

## Summary
The optimisation problem is a **parameter‑light QAP**:
- **W** is fully derived from equal‑tempered tuning + the standard auditory ERB model (no free musical parameters).  
- **C** is derived from a physiologically grounded Fitts‑type model whose coefficients are obtained via a brief, repeatable calibration.  

Thus the only inputs required are the physical keyboard layout and the chosen tuning system; everything else follows from first‑principles models of human perception and motor control.