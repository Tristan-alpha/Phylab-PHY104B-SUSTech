import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Read the CSV data from the file
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("Error: data.csv not found. Please make sure the file is uploaded.")
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")

# Get the wavelengths from the column names
wavelengths = [col.split(' ')[1] for col in df.columns if 'U(V)' in col]

# Determine stopping voltages (Ua) and convert wavelengths to frequencies
stopping_voltages = { 
    '365nm': 1.8,
    '405nm': 1.6,
    '436nm': 1.5,
    '546nm': 0.8,
    '577nm': 0.7
}
frequencies = {}
c = 3e8 # Speed of light in m/s

for wavelength in wavelengths:
    u_col = f'U(V) {wavelength}'
    # Determine the correct current column and unit based on the header
    if f'I (10^-12 A) {wavelength}' in df.columns:
        i_col = f'I (10^-12 A) {wavelength}'
        unit_factor = 1e-12
    elif f'I (10^-13 A) {wavelength}' in df.columns:
        i_col = f'I (10^-13 A) {wavelength}'
        unit_factor = 1e-13
    else:
        print(f"Warning: Current column for {wavelength} not found in the CSV data.")
        continue

    # Convert wavelength (in nm) to frequency (in Hz)
    freq = c / (float(wavelength.replace('nm', '')) * 1e-9)
    frequencies[wavelength] = freq

# Create 2x3 subplot figure
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten() # Flatten the 2x3 array of axes for easy iteration

# Plot I-U curves
for i, wavelength in enumerate(wavelengths):
    u_col = f'U(V) {wavelength}'
    if f'I (10^-12 A) {wavelength}' in df.columns:
        i_col = f'I (10^-12 A) {wavelength}'
        ylabel = 'I (10$^{-12}$ A)'
    elif f'I (10^-13 A) {wavelength}' in df.columns:
        i_col = f'I (10^-13 A) {wavelength}'
        ylabel = 'I (10$^{-13}$ A)'
    else:
        continue

    axes[i].scatter(df[u_col], df[i_col])
    axes[i].set_xlabel('U (V)')
    axes[i].set_ylabel(ylabel)
    axes[i].set_title(f'I-U Curve ({wavelength})')
    axes[i].grid(True)

# Prepare data for nu-Ua plot
nu_values = np.array([frequencies[w] for w in wavelengths])
ua_values = np.array([stopping_voltages[w] for w in wavelengths])

# Perform linear regression (Ua = m*nu + c)
# Note: We are fitting Ua as a function of nu to get slope h/e and intercept -A/e
slope, intercept, r_value, p_value, std_err = linregress(nu_values, ua_values)

# Calculate Planck's constant (h), work function (A), and red limit frequency (nu_0)
e = 1.602e-19 # Elementary charge in C
h_calculated = slope * e
a_calculated = -intercept * e
nu_0_calculated = -intercept / slope # From Ua = 0 = m*nu_0 + c

# Accepted value of Planck's constant
h_accepted = 6.626e-34 # J s

# Calculate relative error
relative_error = np.abs(h_calculated - h_accepted) / h_accepted * 100

# Plot nu-Ua curve and regression line
axes[5].scatter(nu_values, ua_values)
nu_min = nu_values.min()
nu_max = nu_values.max()
axes[5].plot(np.array([nu_min, nu_max]), slope * np.array([nu_min, nu_max]) + intercept, color='red')
axes[5].set_xlabel('Frequency (Hz)')
axes[5].set_ylabel('Stopping Voltage (V)')
axes[5].set_title('Stopping Voltage vs Frequency')
axes[5].grid(True)

# Add text with calculated values
axes[5].text(0.05, 0.95, f'Calculated h: {h_calculated:.2e} J s\nRelative Error: {relative_error:.2f} %\nCalculated A: {a_calculated:.2e} J\nCalculated v_0: {nu_0_calculated:.2e} Hz', transform=axes[5].transAxes, fontsize=10, verticalalignment='top')

# Adjust layout and display plots
plt.tight_layout()
plt.show()

print("\nCalculated Values:")
print(f"Planck's constant (h): {h_calculated:.2e} J s")
print(f"Work function (A): {a_calculated:.2e} J")
print(f"Red limit frequency (nu_0): {nu_0_calculated:.2e} Hz")
print(f"Relative Error in h: {relative_error:.2f} %")