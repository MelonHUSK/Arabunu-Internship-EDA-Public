import numpy as np
import openpyxl

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

# Initial velocity components
v_x0 = v0 * np.cos(np.radians(theta))
v_y0 = v0 * np.sin(np.radians(theta))

# Time parameters
dt = 0.001  # Time step (1 second)
t_max = 600  # Max simulation time (s)

# Function to calculate drag force
def drag_force(v_rel):
    return 0.5 * Cd * rho * A * v_rel**2

# Euler method to compute position and velocity over time and write to Excel
def euler_to_excel(v_x0, v_y0, v_wind, dt, t_max, filename):
    # Create a new workbook and select the active sheet
    wb = openpyxl.Workbook()
    sheet = wb.active

    # Write headers to the sheet
    sheet.append(["Time (s)", "x (m)", "y (m)", "v_x (m/s)", "v_y (m/s)", "F_drag_x (N)", "F_drag_y (N)", "a_x (m/s^2)", "a_y (m/s^2)"])

    # Initial conditions
    t = 0
    x = 0
    y = 0
    v_x = v_x0
    v_y = v_y0

    # Time iteration
    while t <= t_max:
        # Calculate relative velocities
        v_rel_x = v_x - v_wind  # Relative velocity to wind (horizontal)
        v_rel_y = v_y           # Relative velocity for vertical motion

        # Calculate drag forces
        F_drag_x = drag_force(v_rel_x)
        F_drag_y = drag_force(v_rel_y)

        # Calculate accelerations
        a_x = - F_drag_x / m
        a_y = -g - F_drag_y / m

        # Write the current time step's data to the Excel sheet
        sheet.append([t, x, y, v_x, v_y, F_drag_x, F_drag_y, a_x, a_y])

        # Update velocities and positions using Euler's method
        v_x += a_x * dt
        v_y += a_y * dt
        x += v_x * dt
        y += v_y * dt

        # Stop the simulation when the projectile hits the ground
        if y <= 0:
            break

        # Update time
        t += dt

    # Save the workbook
    wb.save(filename)
    print(f"Data written to {filename}")

# Run the Euler method and write the results to an Excel file
euler_to_excel(v_x0, v_y0, v_wind, dt, t_max, "projectile_motion.xlsx")
