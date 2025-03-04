import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.special import sph_harm, genlaguerre, factorial
import time

# -------------------------------
# Realistic Radial Wavefunction
# -------------------------------
def radial_wavefunction(n, l, r):
    """
    Compute the radial wavefunction for a hydrogen-like orbital
    (in atomic units, with a0=1) using generalized Laguerre polynomials.
    """
    r = np.maximum(r, 1e-10)  # avoid division by zero
    a0 = 1.0
    rho = 2 * r / (n * a0)
    norm = np.sqrt((2/(n*a0))**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-rho/2) * (rho**l) * L

# -------------------------------
# Angular Wavefunction
# -------------------------------
def angular_wavefunction(l, m, theta, phi):
    """
    Compute the spherical harmonic Y_l^m(theta, phi) for the angular part.
    """
    return sph_harm(m, l, phi, theta)

# -------------------------------
# Compute Probability Density on 3D Grid
# -------------------------------
def compute_density(n, l, m, grid_range=15, grid_points=50):
    """
    Create a 3D grid (x,y,z), convert to spherical coordinates,
    compute the full wavefunction ψ = R(r)*Y_l^m(theta,phi),
    and return the probability density |ψ|^2.
    """
    x = np.linspace(-grid_range, grid_range, grid_points)
    y = np.linspace(-grid_range, grid_range, grid_points)
    z = np.linspace(-grid_range, grid_range, grid_points)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    r = np.sqrt(X**2 + Y**2 + Z**2)
    theta = np.arccos(np.clip(Z / r, -1, 1))
    phi = np.arctan2(Y, X)

    R = radial_wavefunction(n, l, r)
    Y_ang = angular_wavefunction(l, m, theta, phi)
    psi = R * Y_ang
    density = np.abs(psi)**2

    # Mask one half of the orbital
    mask = X >= 0
    density[mask] = 0

    return X, Y, Z, density

# -------------------------------
# Electron Configuration Data
# -------------------------------
electron_configurations = {
    "Hydrogen": "1s1",
    "Helium": "1s2",
    "Lithium": "1s2 2s1",
    "Beryllium": "1s2 2s2",
    "Boron": "1s2 2s2 2p1",
    "Carbon": "1s2 2s2 2p2",
    "Nitrogen": "1s2 2s2 2p3",
    "Oxygen": "1s2 2s2 2p4",
    "Fluorine": "1s2 2s2 2p5",
    "Neon": "1s2 2s2 2p6"
}

# -------------------------------
# Predefined Orbital Sequence for Animation (Simplified)
# -------------------------------
orbital_sequence = [
    (1, 0, 0),   # 1s
    (2, 0, 0),   # 2s
    (2, 1, -1),  # 2p, m=-1
    (2, 1, 0),   # 2p, m=0
    (2, 1, 1),   # 2p, m=1
    (3, 0, 0),   # 3s
    (3, 1, -1),  # 3p, m=-1
    (3, 1, 0),   # 3p, m=0
    (3, 1, 1),   # 3p, m=1
    (3, 2, -2),  # 3d, m=-2
    (3, 2, -1),  # 3d, m=-1
    (3, 2, 0),   # 3d, m=0
    (3, 2, 1),   # 3d, m=1
    (3, 2, 2),   # 3d, m=2
    (4, 0, 0),   # 4s
    (4, 1, -1),  # 4p, m=-1
    (4, 1, 0),   # 4p, m=0
    (4, 1, 1),   # 4p, m=1
    (4, 2, -2),  # 4d, m=-2
    (4, 2, -1),  # 4d, m=-1
    (4, 2, 0),   # 4d, m=0
    (4, 2, 1),   # 4d, m=1
    (4, 2, 2),   # 4d, m=2
    (4, 3, -3),  # 4f, m=-3
    (4, 3, -2),  # 4f, m=-2
    (4, 3, -1),  # 4f, m=-1
    (4, 3, 0),   # 4f, m=0
    (4, 3, 1),   # 4f, m=1
    (4, 3, 2),   # 4f, m=2
    (4, 3, 3),   # 4f, m=3
]

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.set_page_config(layout="wide")
st.title("Enhanced Interactive Atomic Orbital Visualizer")

st.header("3D Orbital Visualization")
st.markdown("Select quantum numbers and grid settings to visualize a hydrogen-like orbital.")

# Split screen into two columns: left for controls, right for the display.
col_controls, col_display = st.columns([1, 1])

with col_controls:
    n = st.selectbox("Principal quantum number (n)", options=list(range(1, 30)), index=0)
    l_options = list(range(0, n))
    l = st.selectbox("Azimuthal quantum number (l)", options=l_options, index=0)
    m_options = list(range(-l, l+1)) if l > 0 else [0]
    m = st.selectbox("Magnetic quantum number (m)", options=m_options, index=m_options.index(0))

    grid_points = st.slider("Grid Resolution (points per axis)", min_value=30, max_value=100, value=100, step=1)
    grid_range = st.slider("Grid Range (extent in each direction)", min_value=10, max_value=5000, value=20, step=1)
    iso_percent = st.slider("Isosurface level (%)", min_value=1, max_value=100, value=1)

with st.spinner("Calculating orbital density, please wait..."):
    X, Y, Z, density = compute_density(n, l, m, grid_range=grid_range, grid_points=grid_points)
max_density = np.max(density)
isovalue = iso_percent / 100 * max_density

with col_display:
    # Create the isosurface plot with a fixed square size and adjusted camera.
    fig1 = go.Figure(data=go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=density.flatten(),
        isomin=isovalue,
        isomax=max_density,
        surface_count=2,
        colorscale="Plasma",
        opacity=0.6,  # Make the orbital more fuzzy
        caps=dict(x_show=False, y_show=False, z_show=False)
    ))
    camera = dict(eye=dict(x=0.4, y=0.4, z=0.4))
    fig1.update_layout(
        title=f"Hydrogen-like Orbital (n={n}, l={l}, m={m})",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode='cube',
            camera=camera
        ),
        width=950,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig1, use_container_width=False)

st.markdown("""
### Visualizing Orbital Filling Order

To understand how electrons fill atomic orbitals, follow these steps:

1. **Start with the lowest energy orbital**:
   - **n=1, l=0, m=0**: This corresponds to the **1s orbital**. It is the first orbital to be filled and has a spherical shape.

2. **Move to the next energy level**:
   - **n=2, l=0, m=0**: This corresponds to the **2s orbital**. It is the next orbital to be filled and also has a spherical shape but is larger than the 1s orbital.

3. **Fill the 2p orbitals**:
   - **n=2, l=1, m=-1**: This corresponds to the **2p orbital** oriented along the negative y-axis.
   - **n=2, l=1, m=0**: This corresponds to the **2p orbital** oriented along the z-axis.
   - **n=2, l=1, m=1**: This corresponds to the **2p orbital** oriented along the positive y-axis.

4. **Proceed to the 3s orbital**:
   - **n=3, l=0, m=0**: This corresponds to the **3s orbital**. It is the next orbital to be filled and has a spherical shape but is larger than the 2s orbital.

5. **Fill the 3p orbitals**:
   - **n=3, l=1, m=-1**: This corresponds to the **3p orbital** oriented along the negative y-axis.
   - **n=3, l=1, m=0**: This corresponds to the **3p orbital** oriented along the z-axis.
   - **n=3, l=1, m=1**: This corresponds to the **3p orbital** oriented along the positive y-axis.

6. **Fill the 4s orbital before the 3d orbitals** (according to the Aufbau principle):
   - **n=4, l=0, m=0**: This corresponds to the **4s orbital**. It is the next orbital to be filled and has a spherical shape but is larger than the 3s orbital.

7. **Fill the 3d orbitals**:
   - **n=3, l=2, m=-2**: This corresponds to the **3d orbital** with a complex shape.
   - **n=3, l=2, m=-1**: This corresponds to the **3d orbital** with a different orientation.
   - **n=3, l=2, m=0**: This corresponds to the **3d orbital** oriented along the z-axis.
   - **n=3, l=2, m=1**: This corresponds to the **3d orbital** with another orientation.
   - **n=3, l=2, m=2**: This corresponds to the **3d orbital** with yet another orientation.

8. **Continue with the 4p orbitals**:
   - **n=4, l=1, m=-1**: This corresponds to the **4p orbital** oriented along the negative y-axis.
   - **n=4, l=1, m=0**: This corresponds to the **4p orbital** oriented along the z-axis.
   - **n=4, l=1, m=1**: This corresponds to the **4p orbital** oriented along the positive y-axis.

By following these steps, you can visualize the order in which electrons fill the atomic orbitals according to the Aufbau principle. Each set of quantum numbers (n, l, m) corresponds to a specific orbital with a unique shape and orientation.
""")
