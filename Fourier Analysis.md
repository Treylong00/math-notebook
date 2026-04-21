The [[Harmonic Functions]] notebook ended with the observation that the real and imaginary parts of analytic functions satisfy Laplace's equation. But there is another family of functions built from complex exponentials that turns out to be just as fundamental — and far more practical. This notebook is about **Fourier analysis**: the idea that any signal can be decomposed into a sum of pure frequencies.

## Why Decompose into Frequencies?

Think about sound. A musical note is a periodic vibration of air pressure. A pure tone — a single frequency — is a sine wave. But real instruments don't produce pure tones. A violin playing middle C produces a complex waveform that repeats 262 times per second. What makes it sound like a violin (and not a flute or a clarinet) is the specific mixture of higher frequencies — the **harmonics** — layered on top of the fundamental.

Fourier's insight, published in 1807, was radical: *every* periodic function can be written as a sum of sines and cosines. Not just smooth ones — even sharp, discontinuous signals like a square wave. The coefficients of the sum tell you how much of each frequency is present. This is the **frequency domain** representation of the signal.

The connection to [[Complex Numbers]] is immediate. Recall Euler's formula:

$$e^{ix} = \cos x + i \sin x$$

Sines and cosines are the real and imaginary parts of complex exponentials. Fourier analysis is really about decomposing functions into complex exponentials — the same $e^{ix}$ that appeared in the polar form of complex numbers.

## Fourier Series

Let $f(x)$ be a periodic function with period $2\pi$. The **Fourier series** of $f$ is

$$f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left[ a_n \cos(nx) + b_n \sin(nx) \right]$$

where the coefficients are computed by integration:

$$a_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \cos(nx) \, dx, \qquad b_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin(nx) \, dx$$

The key idea is **orthogonality**: $\cos(nx)$ and $\cos(mx)$ are "perpendicular" in the sense that their product integrates to zero when $n \neq m$. The same holds for $\sin(nx)$ and $\sin(mx)$, and for any $\cos(nx)$ against any $\sin(mx)$. This orthogonality is what makes the coefficients computable — to extract the $n$-th coefficient, you multiply by the $n$-th basis function and integrate. Everything else cancels.

### The Complex Exponential Form

Using Euler's formula, we can rewrite the series more compactly. Since $\cos(nx) = \frac{1}{2}(e^{inx} + e^{-inx})$ and $\sin(nx) = \frac{1}{2i}(e^{inx} - e^{-inx})$, the Fourier series becomes

$$f(x) = \sum_{n=-\infty}^{\infty} c_n \, e^{inx}$$

where the complex coefficients are

$$c_n = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(x) \, e^{-inx} \, dx$$

This is the form that generalizes most naturally. Each $c_n$ is a complex number whose magnitude $|c_n|$ tells you the amplitude of the $n$-th frequency component, and whose argument $\arg(c_n)$ tells you its phase (how shifted it is).

## Building a Square Wave

The classic demonstration: take a square wave that alternates between $+1$ and $-1$. Its Fourier series contains only odd harmonics:

$$f(x) = \frac{4}{\pi} \left[ \sin(x) + \frac{\sin(3x)}{3} + \frac{\sin(5x)}{5} + \frac{\sin(7x)}{7} + \cdots \right]$$

Each term you add brings the approximation closer to the sharp corners of the square wave. With just one term, you get a single sine wave. With three terms, the shape starts to flatten on top. With fifteen, it looks remarkably close to the target — though there is always a small overshoot near the discontinuities (the **Gibbs phenomenon**, which never fully disappears no matter how many terms you take).

![[Figures/fourier_square_wave.png]]
*Figure 1: Fourier partial sums of a square wave using 1, 3, 5, and 15 odd harmonics, showing progressive convergence and Gibbs phenomenon at the discontinuities.*

<!-- Claude: Figure out why the above figure is missing -->

![[Figures/anim_fourier_convergence.gif]]
*Animation 1: Fourier partial sums converging to the square wave, showing Gibbs phenomenon emerging as terms are added.*

The partial sums $S_N(x)$ use only the first $N$ odd harmonics. As $N$ grows, the approximation sharpens toward the true square wave. The ringing near the jumps is Gibbs' phenomenon — the overshoot converges to about 9% of the jump height.

### The Coefficient Spectrum

We can also look at the complex coefficients $c_n$ directly. For the square wave, only odd-indexed coefficients are nonzero, and their magnitudes decay like $1/|n|$:

![[Figures/fourier_complex_coefficients.png]]
*Figure 2: Complex Fourier coefficients of the square wave, showing the $1/|n|$ magnitude decay for odd harmonics and the alternating $\pm\pi/2$ phase pattern.*

The top panel shows $|c_n|$ — the amplitude of each frequency. The $1/n$ decay explains why the square wave converges slowly: you need many harmonics because the high-frequency components, while small, are not negligible. The bottom panel shows the phase $\arg(c_n)$, which alternates between $+\pi/2$ and $-\pi/2$. This phase pattern encodes the fact that the square wave is built entirely from sine functions (which are shifted cosines).

## The Fourier Transform

The Fourier series works for periodic functions. But most signals in physics are not periodic — a pulse, a Gaussian bump, a decaying oscillation. To handle these, we take the period to infinity. The sum over discrete frequencies $n$ becomes an integral over a continuous frequency variable $\xi$:

$$\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) \, e^{-2\pi i \xi x} \, dx$$

This is the **Fourier transform** of $f$. It takes a function of position (or time) and produces a function of frequency. The inverse transform recovers the original:

$$f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) \, e^{2\pi i \xi x} \, d\xi$$

The transform and its inverse are symmetric — they are essentially the same operation with a sign flip in the exponent. This duality between the time and frequency domains is one of the deepest features of the theory.

## Transform of a Gaussian

The most beautiful example: a Gaussian transforms into another Gaussian. If

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \, e^{-x^2 / (2\sigma^2)}$$

then its Fourier transform is

$$\hat{f}(\xi) = e^{-2\pi^2 \sigma^2 \xi^2}$$

which is again a Gaussian, but with the reciprocal width. A narrow Gaussian in the time domain (small $\sigma$) produces a wide Gaussian in the frequency domain, and vice versa.

![[Figures/fourier_transform_gaussian.png]]
*Figure 3: Gaussians with $\sigma = 0.5$ and $\sigma = 1.5$ in the time domain and their Fourier transforms, demonstrating the reciprocal width relationship.*

The narrow Gaussian ($\sigma = 0.5$, tall and sharp in the left panel) has a broad transform (spread out in the right panel). The wide Gaussian ($\sigma = 1.5$, low and broad on the left) has a narrow transform (concentrated near $\xi = 0$ on the right). You cannot be localized in both domains simultaneously.

This is the **uncertainty principle** in its mathematical form. In quantum mechanics, where $x$ is position and $\xi$ is momentum (up to factors of $\hbar$), this becomes Heisenberg's uncertainty principle: the more precisely you know a particle's position, the less precisely you can know its momentum. But the mathematical statement is purely about Fourier transforms — it has nothing to do with measurement or observers. It is a theorem about waves.

## Parseval's Theorem

The Fourier transform preserves a quantity that physicists call **energy**. If you compute the total "energy" of a signal by integrating $|f(x)|^2$, you get the same answer by integrating $|\hat{f}(\xi)|^2$ in the frequency domain:

$$\int_{-\infty}^{\infty} |f(x)|^2 \, dx = \int_{-\infty}^{\infty} |\hat{f}(\xi)|^2 \, d\xi$$

This is **Parseval's theorem** (or Plancherel's theorem, depending on context). It says the Fourier transform is an **isometry** — it preserves the "size" of functions. No energy is created or destroyed when you switch between time and frequency representations; the information is just reorganized.

![[Figures/fourier_parseval.png]]
*Figure 4: A three-sinusoid signal with its shaded $|f(t)|^2$ area alongside its power spectrum $|\hat{f}(\xi)|^2$, illustrating equal total energy in both domains.*

The left panel shows a signal composed of three sinusoids, with the shaded region representing $|f(t)|^2$. The right panel shows its power spectrum $|\hat{f}(\xi)|^2$, with three sharp peaks at the component frequencies. The total shaded areas are equal — that is Parseval's theorem in action.

## Where to Go Next

Fourier analysis is the gateway to an enormous amount of modern mathematics and physics:

- **[[Linear Algebra]]** — the orthogonality of $\{e^{inx}\}$ is not a coincidence. These functions form an **orthonormal basis** for a vector space of functions. The Fourier coefficients are coordinates in this basis, and the Fourier transform is a change of basis. Parseval's theorem is just the statement that orthonormal changes of basis preserve lengths — the same as in $\mathbb{R}^n$. This is the theory of **Hilbert spaces**.
- **Quantum mechanics** — the wave function $\psi(x)$ and its momentum-space representation $\hat{\psi}(p)$ are Fourier transforms of each other. The uncertainty principle, superposition, and the structure of quantum states all rest on the Fourier framework.
- **Differential equations** — the Fourier transform turns derivatives into multiplication: $\widehat{f'}(\xi) = 2\pi i \xi \, \hat{f}(\xi)$. This converts differential equations into algebraic equations, making them solvable. The [[Harmonic Functions]] (solutions to $\nabla^2 f = 0$) are intimately connected: their Fourier transforms are supported on the "zero set" of the Laplacian's symbol.
- **Signal processing** — filtering, compression, and spectral analysis are all Fourier operations. The Fast Fourier Transform (FFT) algorithm makes them computationally practical.
