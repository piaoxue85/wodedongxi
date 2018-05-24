import warnings
warnings.simplefilter('ignore')
import pymc3 as pm
import numpy as np
np.random.seed(1000)
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 500)
y = 4 + 2 * x + np.random.standard_normal(len(x)) * 2

reg = np.polyfit(x, y, 1)

# plt.figure(figsize=(8, 4))
# plt.scatter(x, y, c=y, marker='v')
# plt.plot(x, reg[1] + reg[0] * x, lw=2.0)
# plt.colorbar()
# plt.grid(True)
# plt.xlabel('x')
# plt.show()

# model = pm.Model()
with pm.Model() as model:
    # model specifications in PyMC3
    # are wrapped in a with statement
    # define priors
    alpha = pm.Normal('alpha' , mu=0, sd=20)
    beta = pm.Normal('beta' , mu=0, sd=20)
    sigma = pm.Uniform('sigma' , lower=0, upper=10)
    # define linear regression
    y_est = alpha + beta * x
    # define likelihood
    likelihood = pm.Normal('y', mu=y_est, sd=sigma, observed=y)
    # inference
    start = pm.find_MAP()
    # find starting value by optimization
    step = pm.NUTS(scaling=start)
    # instantiate MCMC sampling algorithm
    trace = pm.sample(100, step, start=start, progressbar=False)

print((trace[0]))

fig = pm.traceplot(trace, lines={'alpha': 4, 'beta': 2, 'sigma': 2})
plt.figure(figsize=(8, 8))
plt.show()
plt.figure(figsize=(8, 4))
plt.scatter(x, y, c=y, marker='v')
plt.colorbar()
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
for i in range(len(trace)):
    plt.plot(x, trace['alpha'][i] + trace['beta'][i] * x)
plt.show()
a= ""