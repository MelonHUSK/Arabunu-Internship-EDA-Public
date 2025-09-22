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

# Initial velocity components
v_x0 = v0 * np.cos(np.radians(theta))
v_y0 = v0 * np.sin(np.radians(theta))

# Time parameters
#0.001
dt = 2              # Time step (s)
t_max = 600               # Max simulation time (s)

# Function to calculate drag force
def drag_force(v_rel):
    return 0.5 * Cd * rho * A * v_rel**2


# Euler method to compute position and velocity over time
def euler_method(v_x0, v_y0, v_wind, dt, t_max):
    t_values = np.arange(0, t_max, dt)  # Array of time values
    x_values = np.zeros_like(t_values)  # Horizontal position array
    y_values = np.zeros_like(t_values)  # Vertical position array
    v_x_values = np.zeros_like(t_values)  # Horizontal velocity array
    v_y_values = np.zeros_like(t_values)  # Vertical velocity array

    # Initial conditions
    x = 0
    y = 0
    v_x = v_x0
    v_y = v_y0

    for i in range(1, len(t_values)):
        # Calculate relative velocities
        v_rel_x = v_x - v_wind  # Relative velocity to wind (horizontal)
        v_rel_y = v_y           # Relative velocity for vertical motion

        # Calculate drag forces
        F_drag_x = drag_force(v_rel_x)
        F_drag_y = drag_force(v_rel_y)

        # Update velocity (horizontal and vertical)
        dv_x = - (F_drag_x / m) * dt  # Drag affects horizontal velocity
        dv_y = (-g - (F_drag_y / m)) * dt  # Drag and gravity affect vertical velocity

        v_x += dv_x
        v_y += dv_y

        # Update position
        x += v_x * dt
        y += v_y * dt

        # Store values
        x_values[i] = x
        y_values[i] = y
        v_x_values[i] = v_x
        v_y_values[i] = v_y

        # Stop if the projectile hits the ground
        if y < -100:
            break

    return x_values[:i], y_values[:i]

# Calculate the trajectory using Euler's method
x_vals, y_vals = euler_method(v_x0, v_y0, v_wind, dt, t_max)

# Plot the trajectory y(x)
plt.plot(x_vals, y_vals)
plt.xlabel('Horizontal Distance (m)')
plt.ylabel('Vertical Distance (m)')
plt.title('Projectile Trajectory with Drag (Wind Speed Impact on Drag Only)')
plt.grid(True)
plt.show()
