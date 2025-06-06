import matplotlib.pyplot as plt
import numpy as np

# Data from the table (x in cm, V in mV)
x_cm = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
V_mV = np.array([334.6, 335.1, 334.9, 334.8, 334.9, 334.4, 334.1, 333.5, 333.0, 332.2, 331.5, 329.8, 327.4, 322.7, 313.6, 290.3, 241.6, 178.6, 180.0, 116.5, 59.57, 10.72])

plt.figure(figsize=(8, 6))
plt.plot(x_cm, V_mV, 'o-')

plt.xlabel('Distance from Center x (cm)')
plt.ylabel('Induced Voltage V (mV)')
plt.title('V-x Curve along Solenoid Axis (f=2000Hz, I=20mA)')
plt.grid(True)
plt.show()