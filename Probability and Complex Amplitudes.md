In classical physics, probability is straightforward. If there's a 30% chance a particle goes left and a 70% chance it goes right, the probabilities add: $0.3 + 0.7 = 1$. If two independent events can each lead to the same outcome, you add their probabilities. This is how coin flips, dice rolls, and everyday statistics work.

Quantum mechanics breaks this rule. Instead of assigning probabilities directly, nature assigns **complex amplitudes** — numbers in $\mathbb{C}$ — and the probability only emerges when you take the modulus squared. This distinction is the single most important idea separating quantum from classical physics, and it leads directly to interference: the phenomenon that makes quantum mechanics fundamentally different.

## Complex Amplitudes

In quantum mechanics, the state of a particle is described by a **wavefunction** $\psi(x)$, which is a complex-valued function. At each point $x$, the value $\psi(x)$ is a complex number — it has a real part and an imaginary part, or equivalently a modulus and a phase:

$$\psi(x) = |\psi(x)| \, e^{i\varphi(x)}$$

This is exactly the polar form from [[Complex Numbers]]: the wavefunction at each point is a modulus (how "much" amplitude is there) times a rotation (what phase does it carry). The modulus tells you about probability; the phase tells you about interference.

The probability of finding the particle near position $x$ is not $\psi(x)$ itself — it's

$$P(x) = |\psi(x)|^2 = \psi^*(x) \, \psi(x)$$

where $\psi^*$ is the complex conjugate. This is the **Born rule**, and it's a postulate of quantum mechanics — it cannot be derived from anything more basic. Notice how the modulus squared $|\psi|^2 = \psi^* \psi$ connects back to the definition of modulus from [[Complex Numbers]]: $|z|^2 = z \bar{z} = a^2 + b^2$.

## The Born Rule

The Born rule says: if $\psi(x)$ is a wavefunction, then $|\psi(x)|^2$ is a **probability density**. To find the probability of the particle being in some interval $[a, b]$, you integrate:

$$P(a \le x \le b) = \int_a^b |\psi(x)|^2 \, dx$$

For this to be a valid probability distribution, the total probability must be 1:

$$\int_{-\infty}^{\infty} |\psi(x)|^2 \, dx = 1$$

This is the normalization condition from [[Hilbert Spaces]] — the wavefunction must be a unit vector in $L^2(\mathbb{R})$. The inner product $\langle \psi | \psi \rangle = \int |\psi|^2 \, dx = 1$ is exactly the statement that the particle exists *somewhere*.

![[Figures/prob_born_rule.png]]
*Figure 1: A complex Gaussian wave packet showing Re, Im, and $|\psi|$ (left) and the resulting probability density $|\psi(x)|^2$ (right).*

The left panel shows a complex wavefunction — a Gaussian wave packet with carrier frequency $k_0$. The real and imaginary parts oscillate inside an envelope, and the modulus $|\psi|$ traces that envelope. The right panel shows the probability density $|\psi(x)|^2$: a smooth bell curve whose total area is 1. All the oscillatory structure of $\psi$ is gone — the phase information is erased when you take the modulus squared. Measurement only sees $|\psi|^2$, never $\psi$ itself.

## Interference

Here is where the complex structure of $\psi$ becomes essential. Suppose a particle can reach a detector through two paths — say, two slits — with amplitudes $\psi_1(x)$ and $\psi_2(x)$. The total amplitude is the **sum**:

$$\psi(x) = \psi_1(x) + \psi_2(x)$$

Now compute the probability:

$$|\psi_1 + \psi_2|^2 = (\psi_1^* + \psi_2^*)(\psi_1 + \psi_2) = |\psi_1|^2 + |\psi_2|^2 + \underbrace{\psi_1^* \psi_2 + \psi_2^* \psi_1}_{\text{interference terms}}$$

If amplitudes were real and positive (like classical probabilities), those cross terms would always be positive, and you'd just get "more probability" everywhere. But because $\psi_1$ and $\psi_2$ are complex, the interference terms $\psi_1^* \psi_2 + \psi_2^* \psi_1 = 2 \, \mathrm{Re}(\psi_1^* \psi_2)$ can be **positive or negative**. Where the wavefunctions are in phase, they add constructively. Where they are out of phase, they cancel.

![[Figures/prob_interference.png]]
*Figure 2: Single-slit probability densities $|\psi_1|^2$ and $|\psi_2|^2$ (first two panels) and the two-slit result $|\psi_1 + \psi_2|^2$ with interference fringes compared to the classical sum (third panel).*

The first two panels show what you'd see with each slit open alone: two smooth bumps. The third panel shows what happens with both slits open. The gray dashed line is the classical expectation — just add the probabilities $|\psi_1|^2 + |\psi_2|^2$. The solid curve is the quantum result $|\psi_1 + \psi_2|^2$, which shows interference fringes. At some points the probability is *larger* than the classical sum; at others it's *smaller*. Probability has been redistributed by the phase relationship between the two amplitudes.

This is impossible with real-valued or purely probabilistic descriptions. Classical probabilities always satisfy $P(A \cup B) \le P(A) + P(B)$. In quantum mechanics, amplitudes can cancel, making $|\psi_1 + \psi_2|^2 < |\psi_1|^2 + |\psi_2|^2$ at some locations. Complex numbers aren't a mathematical convenience — they're the reason interference exists.

## Phase Matters

The interference pattern depends entirely on the **relative phase** between the two amplitudes. If we shift $\psi_2$ by a phase $e^{i\Delta\phi}$, the interference terms become:

$$2 \, \mathrm{Re}(\psi_1^* \, e^{i\Delta\phi} \, \psi_2)$$

When $\Delta\phi = 0$, the amplitudes reinforce each other (constructive interference). When $\Delta\phi = \pi$, they oppose each other (destructive interference). Any value in between gives a shifted pattern.

![[Figures/prob_phase_matters.png]]
*Figure 3: Two-slit interference with $\Delta\phi = 0$ (left, constructive) versus $\Delta\phi = \pi$ (right, destructive), showing how relative phase flips the pattern.*

The left panel shows $|\psi_1 + \psi_2|^2$ with no relative phase shift — peaks in the center where the wave packets overlap. The right panel shows $|\psi_1 + e^{i\pi}\psi_2|^2$ — the same wave packets, but with a $\pi$ phase flip, turning peaks into valleys. The *only* thing that changed was a complex phase. The moduli $|\psi_1|$ and $|\psi_2|$ are identical in both cases.

## Superposition

The two-slit example is a special case of a general principle: **superposition**. Any quantum state can be written as a linear combination of basis states:

$$|\psi\rangle = c_1 |1\rangle + c_2 |2\rangle + \cdots$$

where the coefficients $c_n \in \mathbb{C}$ are complex amplitudes. The probability of measuring the system in state $|n\rangle$ is $|c_n|^2$, and normalization requires:

$$\sum_n |c_n|^2 = 1$$

This is the connection to [[Hilbert Spaces]]: the coefficients $(c_1, c_2, \ldots)$ are the components of $|\psi\rangle$ in some orthonormal basis, and $\sum |c_n|^2 = 1$ says $|\psi\rangle$ is a unit vector.

Two key facts about these complex coefficients:

1. **Global phase doesn't matter.** The states $|\psi\rangle$ and $e^{i\alpha}|\psi\rangle$ give identical probabilities for every measurement, because $|e^{i\alpha} c_n|^2 = |c_n|^2$. You can always multiply the entire state by a phase without changing any physics.

2. **Relative phase matters.** The states $c_1|1\rangle + c_2|2\rangle$ and $c_1|1\rangle + e^{i\phi}c_2|2\rangle$ give *different* probability distributions, because the interference between the two components depends on $\phi$.

![[Figures/prob_superposition.png]]
*Figure 4: Probability density $|\psi(x)|^2$ for the superposition $\frac{1}{\sqrt{2}}(\psi_1 + e^{i\phi}\psi_2)$ at four values of relative phase $\phi$.*

Each panel shows the probability density $|\psi(x)|^2$ for a superposition of the first two particle-in-a-box eigenstates, $\psi = \frac{1}{\sqrt{2}}(\psi_1 + e^{i\phi}\psi_2)$, with a different relative phase $\phi$. The probabilities $|c_1|^2 = |c_2|^2 = \frac{1}{2}$ are the same in every panel — the only thing changing is the complex phase. Yet the probability distribution shifts dramatically: from peaked on the left ($\phi = 0$) to centered ($\phi = \pi/2$) to peaked on the right ($\phi = \pi$) and back. The phase of a complex amplitude is a physical degree of freedom.

## Expectation Values

If $|\psi\rangle$ is a quantum state and $\hat{A}$ is an observable (a Hermitian operator, from [[Operators and Eigenvalues]]), the **expectation value** — the average result of many measurements — is:

$$\langle \hat{A} \rangle = \langle \psi | \hat{A} | \psi \rangle = \int_{-\infty}^{\infty} \psi^*(x) \, \hat{A} \, \psi(x) \, dx$$

This is the inner product from [[Hilbert Spaces]], but with an operator sandwiched in between. The structure $\psi^* \hat{A} \psi$ mirrors the Born rule: probability is $\psi^* \psi = \langle \psi | \psi \rangle$, and expectation values generalize this to $\langle \psi | \hat{A} | \psi \rangle$.

For example, the expectation value of position is:

$$\langle x \rangle = \int_{-\infty}^{\infty} \psi^*(x) \, x \, \psi(x) \, dx = \int_{-\infty}^{\infty} x \, |\psi(x)|^2 \, dx$$

This is just the mean of the probability distribution $|\psi|^2$, weighted by $x$. The Born rule and expectation values are two sides of the same coin: both emerge from the inner product structure of $L^2$ and the fact that amplitudes are complex.

Because $\hat{A}$ is Hermitian, the spectral theorem guarantees that its eigenvalues are real (from [[Operators and Eigenvalues]]). This is why measured values are always real numbers, even though the state $\psi$ is complex-valued. The complex amplitudes carry the full quantum information; measurement extracts real numbers from that information via $|\cdot|^2$.

## Looking Forward

We now have the conceptual foundation: quantum states are complex amplitudes, probabilities come from the Born rule, and interference arises from the phase structure of $\mathbb{C}$. The next question is: how do these amplitudes evolve in time? That's the subject of [[The Schrodinger Equation]].
