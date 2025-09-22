import numpy as np
import matplotlib.pyplot as plt

# Constants
v0 = 440.0               # Initial velocity (m/s)
theta = 40.0             # Launch angle (degrees)
v_wind = 20.0            # Wind speed (m/s)
Cd = 5e-5                # Drag coefficient
m = 4.1                  # Mass of the projectile (kg)
rho = 1.225              # Air density (kg/m^3)
d = 0.12                 # Diameter of the projectile (m)
A = np.pi * (d/2)**2     # Cross-sectional area (m^2)
g = 9.81                 # Gravitational acceleration (m/s^2)

# Initial horizontal velocity component
v_x0 = v0 * np.cos(np.radians(theta))

# Time parameters
dt = 0.001               # Time step (s)
t_max = 10              # Max simulation time (s)

# Function to calculate drag force
def drag_force(v_rel):
    return 0.5 * Cd * rho * A * v_rel**2

# Euler method to compute position and velocity over time
def euler_method(v_x0, v_wind, dt, t_max):
    t_values = np.arange(0, t_max, dt)  # Array of time values
    v_x_values = np.zeros_like(t_values)  # Horizontal velocity array
    x_values = np.zeros_like(t_values)    # Horizontal position array
    
    v_x = v_x0  # Initial horizontal velocity
    x = 0       # Initial horizontal position
    
    for i in range(1, len(t_values)):
        v_rel_x = v_x - v_wind  # Relative velocity to wind
        F_drag_x = drag_force(v_rel_x)  # Drag force
        
        # Newton's second law for horizontal motion
        dv_x = - (F_drag_x / m) * dt  # Change in velocity
        
        # Update velocity and position
        v_x += dv_x
        x += v_x * dt
        
        # Store values
        v_x_values[i] = v_x
        x_values[i] = x
    
    return t_values, x_values, v_x_values

# Calculate the horizontal motion with Euler's method
t_values, x_values, v_x_values = euler_method(v_x0, v_wind, dt, t_max)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(t_values, x_values, label="Horizontal Position (x)")
plt.title("Horizontal Position of a Projectile with Drag and Wind")
plt.xlabel("Time (s)")
plt.ylabel("Horizontal Position (m)")
plt.grid(True)
plt.legend()
plt.show()
