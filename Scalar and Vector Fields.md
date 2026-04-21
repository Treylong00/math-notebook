A scalar field assigns a single number to every point in space. A vector field assigns a direction and magnitude. Together, they describe nearly everything in physics — temperature, pressure, gravity, electric fields, fluid flow — and the operations connecting them (gradient, divergence, curl) form the backbone of multivariable calculus.

This notebook builds the ideas visually, starting from the simplest scalar fields and working toward the key differential operators.

## Scalar Fields

A **scalar field** is a function $f : \mathbb{R}^2 \to \mathbb{R}$ — it takes a point $(x, y)$ and returns a single real number. Think of it as a landscape: every point on the ground has an elevation.

Some examples:

- **Paraboloid:** $f(x, y) = x^2 + y^2$ — a bowl centered at the origin. The value increases uniformly in all directions.
- **Saddle:** $f(x, y) = x^2 - y^2$ — curves up along $x$ and down along $y$. A horse saddle shape.
- **Gaussian:** $f(x, y) = e^{-(x^2 + y^2)}$ — a smooth bump, peaking at $1$ at the origin and decaying to $0$.

![[Figures/scalar_fields_panel.png]]
*Figure 1: Contour plots of three scalar fields: the paraboloid $x^2 + y^2$, the saddle $x^2 - y^2$, and the Gaussian $e^{-(x^2 + y^2)}$.*

We visualize scalar fields with **contour plots** — lines of constant value, like elevation lines on a topographic map. The spacing of contour lines tells you how steep the field is: closely spaced lines mean the value changes rapidly.

## The Gradient

Given a scalar field $f(x, y)$, the **gradient** is the vector field

$$\nabla f = \left(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right)$$

At each point, $\nabla f$ points in the direction of steepest ascent, and its magnitude is the rate of change in that direction. The gradient is always perpendicular to the contour lines — it points "uphill" across them.

![[Figures/gradient_panel.png]]
*Figure 2: Gradient vector fields overlaid on the contour plots of the paraboloid, saddle, and Gaussian, showing arrows perpendicular to contour lines.*

The gradient is the fundamental bridge from scalar fields to vector fields. Every conservative force field in physics — gravity, electrostatics — is the (negative) gradient of a potential.

## Vector Fields

A **vector field** is a function $\mathbf{F} : \mathbb{R}^2 \to \mathbb{R}^2$ — it assigns a vector $(u, v)$ to every point $(x, y)$. We can visualize these with **quiver plots** (arrows at sample points) or **streamlines** (curves that are everywhere tangent to the field).

Some fundamental examples:

- **Rotation:** $\mathbf{F}(x, y) = (-y, x)$ — every vector is tangent to a circle centered at the origin. Uniform counterclockwise rotation.
- **Source:** $\mathbf{F}(x, y) = \frac{(x, y)}{r}$ — radial outward flow with unit magnitude. Models fluid emitted from a point.
- **Vortex:** $\mathbf{F}(x, y) = \frac{(-y, x)}{r}$ — rotation with magnitude $1/r$, decaying away from the center. The free vortex in fluid dynamics.

![[Figures/vector_fields_panel.png]]
*Figure 3: Streamlines and quiver plots of three vector fields: uniform rotation $(-y, x)$, radial source $(x, y)/r$, and the free vortex $(-y, x)/r$.*

## Divergence

The **divergence** of a vector field $\mathbf{F} = (u, v)$ is the scalar field

$$\nabla \cdot \mathbf{F} = \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y}$$

It measures how much the field "spreads out" from each point. Positive divergence means the field acts as a source (fluid flows outward); negative means a sink (fluid flows inward); zero means the field is **incompressible** — nothing is created or destroyed.

![[Figures/divergence_panel.png]]
*Figure 4: Vector fields with their divergence shown as a colored background for the rotation, source, and vortex fields.*

## Curl

In two dimensions, the **curl** of a vector field $\mathbf{F} = (u, v)$ is the scalar

$$\nabla \times \mathbf{F} = \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}$$

It measures the local rotation — how much the field swirls around each point. A field with zero curl everywhere is called **irrotational**, and (on simply connected domains) it must be a gradient field.

![[Figures/curl_panel.png]]
*Figure 5: Vector fields with their scalar curl shown as a colored background for the rotation, source, and vortex fields.*

## Gravitational Field

A point mass at the origin creates a gravitational potential

$$\phi(x, y) = -\frac{1}{\sqrt{x^2 + y^2}}$$

The gravitational field is $\mathbf{g} = -\nabla\phi$, pointing toward the mass. This is a physical example tying together everything above: the scalar potential, its gradient, the resulting vector field, and the fact that gravity is both irrotational ($\nabla \times \mathbf{g} = 0$) and divergence-free away from the source ($\nabla \cdot \mathbf{g} = 0$ for $r > 0$).

![[Figures/gravitational_panel.png]]
*Figure 6: Gravitational potential $\phi = -1/r$, its gradient field $\mathbf{g} = -\nabla\phi$, and the divergence and curl of the resulting field.*

## Where to Go Next

- **Laplacian** $\nabla^2 f = \nabla \cdot \nabla f$ — the divergence of the gradient. Harmonic functions ($\nabla^2 f = 0$) connect back to [[Complex Numbers]] via analytic functions.
- **Conservative fields** — when is a vector field a gradient? Path independence, exact differentials, and the connection to curl-free fields.
- **Green's theorem** — relating a line integral around a curve to a double integral over the enclosed region. The 2D version of Stokes' theorem.
- **Three dimensions** — extending to $\mathbb{R}^3$, where curl becomes a vector and we gain the full machinery of $\nabla \times \mathbf{F}$.
- **Electromagnetic fields** — $\mathbf{E} = -\nabla\phi$ and $\mathbf{B} = \nabla \times \mathbf{A}$, Maxwell's equations as the interplay of divergence and curl.
