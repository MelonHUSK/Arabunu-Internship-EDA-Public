from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt


# Constants
v0 = 440.0               # Initial velocity (m/s)
theta = 40.0             # Launch angle (degrees)
v_wind = 20.0            # Wind speed (m/s)
Cd = 5e-1                # Drag coefficient
m = 4.1                  # Mass of the projectile (kg)
rho = 1.225              # Air density (kg/m^3)
d = 0.12                 # Diameter of the projectile (m)
A = np.pi * (d/2)**2     # Cross-sectional area (m^2)
g = 9.81                 # Gravitational acceleration (m/s^2)

dt = 0.00001               # Time step (s)
t_max = 40               # Max simulation time (s)

v_x0 = v0 * np.cos(np.radians(theta))
v_y0 = v0 * np.sin(np.radians(theta))


# Function to calculate drag force
def drag_force_horizontal(v_rel):
    return 0.5 * Cd * rho * A * v_rel**2

def drag_force_vertical(v_rel):
    return v_rel**2*Cd

# Function to compute derivatives
def derivatives(t, y, v_wind, Cd, A, rho, m, g):
    x, y_pos, v_x, v_y = y  # Unpack state variables
    v_rel_x = v_x - v_wind
    v_rel_y = v_y
    v_rel = np.sqrt(v_rel_x**2 + v_rel_y**2)
    
    # Drag forces
    F_drag_x = 0.5 * Cd * rho * A * v_rel * v_rel_x
    F_drag_y = 0.5 * Cd * rho * A * v_rel * v_rel_y
    
    # Derivatives
    dxdt = v_x
    dydt = v_y
    dv_xdt = -F_drag_x / m
    dv_ydt = -g - F_drag_y / m
    
    return [dxdt, dydt, dv_xdt, dv_ydt]



# Initial conditions: [x, y, v_x, v_y]
y0 = [0, 0, v_x0, v_y0]

# Time span
t_span = (0, t_max)
t_eval = np.linspace(0, t_max, 1000)

# Solve the system using Runge-Kutta (solve_ivp)
sol = solve_ivp(derivatives, t_span, y0, args=(v_wind, Cd, A, rho, m, g), t_eval=t_eval)

# Plot results
plt.plot(sol.y[0], sol.y[1])  # Plot x vs y (trajectory)
plt.xlabel('Horizontal Distance (m)')
plt.ylabel('Vertical Distance (m)')
plt.title('Projectile Trajectory with Runge-Kutta')
plt.grid(True)
plt.show()
