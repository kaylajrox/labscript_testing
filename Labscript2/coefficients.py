import numpy as np
from scipy.special import hermite
from scipy.integrate import quad
from math import factorial, sqrt, pi

# Define constants
m = 1.0         # Mass
omega = 1.0     # Angular frequency
hbar = 1.0      # Reduced Planck's constant
xi_0 = 1.0      # Displacement of the Gaussian

# Pre-factor for normalization
norm_factor = (m * omega / (pi * hbar))**0.25

# Define the Gaussian wavepacket centered at xi_0
def gaussian_wavepacket(xi):
    return norm_factor * np.exp(-0.5 * (xi - xi_0)**2)

# Define the nth Hermite-Gaussian wavefunction
def hermite_gaussian(xi, n):
    H_n = hermite(n)  # Generate the nth Hermite polynomial
    return norm_factor * (1 / sqrt(2**n * factorial(n))) * H_n(xi) * np.exp(-0.5 * xi**2)

# Define the integrand for C_n
def integrand(xi, n):
    return gaussian_wavepacket(xi) * hermite_gaussian(xi, n)

# Compute C_n for a given n
def compute_coefficient(n):
    integral, _ = quad(integrand, -10, 10, args=(n,))
    return integral

# Compute coefficients for several values of n
coefficients = [compute_coefficient(n) for n in range(10)]
print("Coefficients:", coefficients)
