import matplotlib.pyplot as plt
import numpy as np

# Data from the table (I in mA, V in mV)
I = np.array([10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0])
V_4000Hz = np.array([334.9, 500.2, 668.9, 835.2, 1002.3, np.nan, np.nan])
V_2000Hz = np.array([168.03, 251.6, 334.8, 418.2, 502.1, 585.1, 668.8])
V_1000Hz = np.array([84.69, 126.31, 168.3, 210.1, 251.9, 293.1, 335.4])

plt.figure(figsize=(8, 6))
plt.plot(I, V_4000Hz, 'o-', label='f = 4000 Hz')
plt.plot(I, V_2000Hz, 's-', label='f = 2000 Hz')
plt.plot(I, V_1000Hz, '^-', label='f = 1000 Hz')

plt.xlabel('Current I (mA)')
plt.ylabel('Induced Voltage V (mV)')
plt.title('V-I Curves at x=0 for Different Frequencies')
plt.legend()
plt.grid(True)
plt.show()