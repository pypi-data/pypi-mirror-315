import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 9.81  # Gravité (m/s²)
RHO = 1.225  # Masse volumique de l'air au niveau de la mer (kg/m³)

# Paramètres physiques de l'objet
CD = 0.5  # Coefficient de traînée (hypothèse fusée/missile)
CL = 0.2  # Coefficient de portance
AREA = 0.1  # Section transversale de la fusée (m²)
MASS = 50.0  # Masse de la fusée (kg)

# Conditions initiales
initial_velocity = 300.0  # Vitesse initiale (m/s)
launch_angle = 45.0  # Angle de lancement (en degrés)
time_step = 0.01  # Pas de temps (s)
max_time = 60  # Durée maximale de la simulation (s)


def compute_forces(vx, vy):
    """Calcule les forces aérodynamiques : traînée et portance"""
    velocity = np.sqrt(vx**2 + vy**2)
    if velocity == 0:
        return 0, 0  # Pas de mouvement => pas de force

    # Direction de la vitesse
    drag_force = 0.5 * CD * RHO * AREA * velocity**2
    lift_force = 0.5 * CL * RHO * AREA * velocity**2

    # Composantes directionnelles (traînée opposée à la vitesse, portance perpendiculaire)
    drag_x = -drag_force * (vx / velocity)
    drag_y = -drag_force * (vy / velocity)

    lift_x = -lift_force * (vy / velocity)
    lift_y = lift_force * (vx / velocity)

    return (drag_x + lift_x, drag_y + lift_y)


def simulate_trajectory():
    """Simule la trajectoire de la fusée"""
    # Conditions initiales
    angle_rad = np.radians(launch_angle)
    vx = initial_velocity * np.cos(angle_rad)
    vy = initial_velocity * np.sin(angle_rad)

    x, y = 0, 0  # Position initiale
    t = 0  # Temps

    positions_x = [x]
    positions_y = [y]
    times = [t]

    # Boucle d'intégration (Euler)
    while y >= 0 and t < max_time:
        # Forces aérodynamiques
        force_x, force_y = compute_forces(vx, vy)

        # Accélérations (a = F/m)
        ax = force_x / MASS
        ay = force_y / MASS - G

        # Mise à jour des vitesses
        vx += ax * time_step
        vy += ay * time_step

        # Mise à jour des positions
        x += vx * time_step
        y += vy * time_step

        # Mise à jour du temps
        t += time_step

        # Sauvegarde des positions et temps
        positions_x.append(x)
        positions_y.append(y)
        times.append(t)

    return positions_x, positions_y, times


def plot_trajectory(x, y):
    """Affiche la trajectoire avec matplotlib"""
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label="Trajectoire balistique avec traînée et portance")
    plt.title("Trajectoire balistique d'une fusée")
    plt.xlabel("Distance horizontale (m)")
    plt.ylabel("Altitude (m)")
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Simulation
    x_positions, y_positions, time = simulate_trajectory()

    # Affichage
    plot_trajectory(x_positions, y_positions)
