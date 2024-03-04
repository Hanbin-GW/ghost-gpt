import matplotlib.pyplot as plt
import numpy as np

# Define the cotangent function
def cot(x):
    return 1/np.tan(x)

# Generate x values
x = np.linspace(-2*np.pi, 2*np.pi, 1000)
x = x[np.logical_not(np.isclose(x % np.pi, 0))]  # Remove points where tan(x) is undefined

# Generate y values for cotangent
y = cot(x)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='cot(x)')

# Asymptotes and Pi multiples for reference
for i in range(-2, 3):
    plt.axvline(i*np.pi, color='gray', linestyle='--', linewidth=0.5)
    plt.text(i*np.pi, 0, f'{i}π', horizontalalignment='center', verticalalignment='bottom')

plt.ylim(-10, 10)
plt.title('Cotangent Function')
plt.xlabel('x')
plt.ylabel('cot(x)')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.show()
