import numpy as np
import math

sensitivity = 1
epsilon = 2
x = 10
# np.random.seed(123)
sum = []
sum_1 = []
for i in range(100):
    np.random.seed(1)
    noise = np.random.laplace(loc=0, scale=sensitivity / 0.001)
    x_n = x + noise
    x_n_1 = x + noise
    x_n_2 = x + noise
    sum.append(x_n + x_n_1 + x_n_2)
    sum_1.append(noise)
    print(noise)
    # print(round(x_n)+round(x_n_1)+round(x_n_2))
print(np.mean(sum))
print(np.mean(sum_1))
t = [1]
n = 0.5
print(type(np.add(t, n).tolist()))
