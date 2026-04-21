In [[Complex Numbers]], we saw how analytic functions map the complex plane to itself — $z^2$ folds it, $e^z$ wraps it, $1/z$ inverts it. In [[Harmonic Functions]], we saw that the Cauchy-Riemann equations force the contour lines of $\mathrm{Re}(f)$ and $\mathrm{Im}(f)$ to cross at right angles. These two threads come together here: analytic functions don't just preserve the orthogonal net of their own contour lines — they preserve the angle between *any* two curves that pass through a point. Such maps are called **conformal**.

## Grid Deformations

The simplest way to see what a complex function does geometrically is to draw a grid of horizontal and vertical lines in the $z$-plane and map each line through $f$. Because the input lines cross at right angles, conformality means the output curves must also cross at right angles — no matter how much the grid bends, stretches, or compresses.

![[Figures/conformal_grid_gallery.png]]
*Figure 1: Regular grids mapped through four analytic functions. The image curves bend and stretch, but every crossing remains a right angle.*

Each panel tells a different story:

- **$z^2$** wraps the grid around the origin — horizontal lines become parabolas, vertical lines become their orthogonal complements. The grid doubles in angular extent (a half-plane maps to a full plane).
- **$e^z$** converts the rectangular grid into a polar one — horizontal lines become radial rays, vertical lines become concentric circles. This is Euler's formula at work: $e^{x+iy} = e^x e^{iy}$, so the real part controls the radius and the imaginary part controls the angle.
- **$1/z$** inverts the plane — circles through the origin become lines, and lines not through the origin become circles. Near the pole at $z = 0$, the grid bunches up intensely.
- **$(z-1)/(z+1)$** is a Möbius transform that maps the imaginary axis to the unit circle and the right half-plane to the unit disk. The grid deformation is smooth except at the pole $z = -1$.

In every panel, the blue and orange curves still cross at $90°$, confirming that each map is conformal.

## Angle Preservation

Conformality isn't limited to right angles. If two curves cross at any angle $\alpha$ in the $z$-plane, their images cross at the same angle $\alpha$ in the $w$-plane.

![[Figures/conformal_angle_preservation.png]]
*Figure 2: Two curves crossing at $60°$ at the point $z_0 = 1 + 0.5i$, and their images under $w = z^2$. The crossing angle is preserved.*

In the left panel, a horizontal line and a ray from the origin meet at $z_0 = 1 + 0.5i$ at an angle of $60°$. The map $f(z) = z^2$ bends both curves, shifts the crossing point to $w_0 = z_0^2 = 0.75 + i$, and rotates both tangent directions — but the angle between them is still exactly $60°$.

This is the defining property of a conformal map: it can stretch, compress, and rotate, but the angle between any two directions at a point is left unchanged.

## The Jacobian as a Scaled Rotation

Why does an analytic function preserve angles? The answer is in its Jacobian. If $f = u + iv$ maps $(x, y) \to (u, v)$, the Jacobian matrix is

$$J = \begin{pmatrix} u_x & u_y \\ v_x & v_y \end{pmatrix}$$

For a general smooth map, this is an arbitrary $2 \times 2$ matrix — it can shear, reflect, and distort angles. But the Cauchy-Riemann equations from [[Harmonic Functions]] constrain it:

$$u_x = v_y, \qquad u_y = -v_x$$

Substituting, the Jacobian becomes

$$J = \begin{pmatrix} u_x & -v_x \\ v_x & u_x \end{pmatrix} = \underbrace{\sqrt{u_x^2 + v_x^2}}_{\displaystyle|f'(z)|} \begin{pmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{pmatrix}$$

where $\phi = \arg(f'(z))$. This is a **rotation by $\phi$** followed by a **uniform scaling by $|f'(z)|$**. A scaled rotation changes the size and orientation of infinitesimal figures, but it preserves all angles between them. That's conformality.

![[Figures/conformal_jacobian_element.png]]
*Figure 3: A small square at $z_0 = 1 + 0.5i$ mapped through $z^2$. The Jacobian sends $\mathrm{d}x$ to $(u_x, v_x)$ and $\mathrm{d}y$ to $(u_y, v_y)$. The dotted lines decompose each image vector into its $u$ and $v$ components: $u_x = v_y = 2$ and $u_y = -v_x = -1$. The Cauchy-Riemann equations make the two image vectors perpendicular and equal in length — the square maps to a rotated, scaled square.*

The complex derivative $f'(z) = u_x + iv_x$ encodes both pieces: its modulus $|f'(z)|$ is the local scaling factor, and its argument $\arg(f'(z))$ is the local rotation angle. This is why differentiability in $\mathbb{C}$ is so much stronger than differentiability in $\mathbb{R}^2$ — the Cauchy-Riemann equations collapse four independent partial derivatives into two constraints, forcing the Jacobian to be a scaled rotation.

## Critical Points

The argument above requires $f'(z) \neq 0$. At a **critical point** where $f'(z) = 0$, the scaling factor vanishes and the Jacobian degenerates — the map is no longer conformal. Something else happens: angles get *multiplied*.

If $f'(z_0) = 0$ but $f^{(n)}(z_0) \neq 0$ (the first nonzero derivative is of order $n$), then near $z_0$ the map looks like $f(z) \approx f(z_0) + c(z - z_0)^n$. The map $z \mapsto z^n$ multiplies angles by $n$, so angles at $z_0$ are multiplied by $n$ as well.

![[Figures/conformal_critical_points.png]]
*Figure 4: A polar grid in the first quadrant ($90°$ sector) mapped through $z$, $z^2$, and $z^3$. The identity preserves the $90°$ sector; $z^2$ doubles it to $180°$; $z^3$ triples it to $270°$.*

The identity map $w = z$ has $f'(0) = 1 \neq 0$ — the $90°$ sector maps to a $90°$ sector. The map $w = z^2$ has $f'(0) = 0$ with a simple zero — the $90°$ sector opens to $180°$, a half-plane. The map $w = z^3$ has a double zero at the origin — the $90°$ sector opens to $270°$. In each case, the angle at the origin is multiplied by the order of the zero of $f'$.

Away from $z = 0$, these maps are still conformal — the grid lines still cross at right angles. It's only at the critical point itself that conformality breaks down.

## Möbius Transforms

The **Möbius transforms** (or fractional linear transforms) are the maps of the form

$$f(z) = \frac{az + b}{cz + d}, \qquad ad - bc \neq 0$$

They are the simplest conformal maps beyond linear ones, and they have a remarkable geometric property: **they map circles and lines to circles and lines**. (Here "lines" are circles of infinite radius — Möbius transforms treat $\mathbb{C} \cup \{\infty\}$ as a sphere, the **Riemann sphere**, where lines are just circles through the point at infinity.)

![[Figures/conformal_mobius_circles.png]]
*Figure 5: Five circles and the imaginary axis in the $z$-plane, mapped through the Möbius transform $w = (z-1)/(z+1)$. Every circle maps to a circle, and the imaginary axis (a line through $z = 0$) maps to the unit circle.*

The transform $w = (z-1)/(z+1)$ has a pole at $z = -1$ (marked with an $\times$). It maps:
- The imaginary axis (a line through the origin) to the unit circle (a circle through $w = -1$ and $w = 1$, shown as the dashed gray circle).
- Each colored circle to another circle, though the centers and radii change.
- Circles that pass through the pole $z = -1$ to straight lines in the $w$-plane — you can see this in the blue circle, whose image opens up as it passes near the pole.

A Möbius transform is completely determined by where it sends three points. Given any three distinct points $z_1, z_2, z_3$ and any three distinct targets $w_1, w_2, w_3$, there is exactly one Möbius transform with $f(z_k) = w_k$. This three-point property makes them central to the theory of conformal mapping.

## The Joukowski Airfoil

One of the most striking applications of conformal mapping is the **Joukowski transform**:

$$w = z + \frac{1}{z}$$

This map has critical points at $z = \pm 1$, where $f'(z) = 1 - 1/z^2 = 0$. If we take a circle in the $z$-plane that passes through one of these critical points, its image is not a smooth curve — it develops a **cusp** at the critical point. By choosing the right circle, this cusp becomes the sharp trailing edge of an airfoil.

![[Figures/conformal_joukowski.png]]
*Figure 6: A circle centered slightly off the origin, passing through the critical point $z = 1$, is mapped by the Joukowski transform to an airfoil shape. The trailing edge cusp forms at the image of the critical point.*

The left panel shows the input: a circle centered at $(-0.1, 0.08)$ with radius chosen so that it passes through $z = 1$. The unit circle (dashed) and the critical points $z = \pm 1$ are marked for reference. The right panel shows the image: a smooth, asymmetric airfoil with a sharp trailing edge at $w = 2$ (the image of $z = 1$).

This works because the Joukowski transform is conformal everywhere except at the critical points. At $z = 1$, where $f'(z) = 0$, the smooth circle develops the cusp. The offset of the circle's center controls the camber (asymmetry) and thickness of the airfoil — shifting the center up adds camber, shifting it left increases thickness.

The power of this construction is that potential flow around the circle (which is easy to compute analytically) maps to potential flow around the airfoil — because conformal maps preserve Laplace's equation. This was how airfoil aerodynamics was first understood mathematically, and it remains one of the canonical examples of conformal mapping in applied mathematics.

![[Figures/anim_conformal_mapping.gif]]
*Animation 1: A regular grid in the complex plane continuously deforming under the conformal map $z \to z^2$, showing how the grid bends while preserving crossing angles.*

## Where to Go Next

- **The Riemann mapping theorem** — any simply connected region in $\mathbb{C}$ (other than $\mathbb{C}$ itself) can be conformally mapped to the unit disk. This is an existence theorem — it guarantees the map exists but doesn't tell you what it is.
- **Schwarz-Christoffel mappings** — explicit conformal maps from the upper half-plane to polygonal regions. These are the workhorses for computing conformal maps in practice.
- **Applications to potential theory** — since conformal maps preserve harmonic functions (the connection from [[Harmonic Functions]]), they transform solutions of Laplace's equation in one geometry to solutions in another. This is how electrostatics problems in complicated geometries are solved by mapping to simpler ones.
- **Riemann surfaces** — the multi-valuedness of $\sqrt{z}$ and $\ln(z)$ from [[Complex Numbers]] can be resolved by "unfolding" the complex plane into a surface where these functions become single-valued and conformal everywhere.
