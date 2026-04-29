import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
path_to_datafile = "data/drop-jump/all_participant_data_rsi.csv"

file = pd.read_csv(path_to_datafile)

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

# force plate data
force = file["force_plate_rsi"]
force_mu = force.mean()
force_std = force.std()

print(f'Force Plate RSI: mu = {force_mu}, std = {force_std}')

# acceleration data
accel = file["accelerometer_rsi"]
accel_mu = accel.mean()
accel_std = accel.std()

print(f'Accelerometer RSI: mu = {accel_mu}, std = {accel_std}')

x = np.linspace(0, 2, 100)

# map the data to normal distributions
force_pdf = norm.pdf(x, force_mu, force_std)
accel_pdf = norm.pdf(x, accel_mu, accel_std)

# plot the data and the fitted distributions
plt.plot(x, force_pdf, label='Force Plate RSI Probability Distribution Function')
plt.plot(x, accel_pdf, label='Accel RSI Probability Distribution Function')

#plt.hist(accel, bins=16, density=True, alpha=0.5, label='Accel RSI Data')
#plt.hist(force, bins=16, density=True, alpha=0.5, label='Force Plate RSI Data')
plt.title('RSI Data and Fitted Normal Distributions')
plt.xlabel('RSI Value')
plt.ylabel('Distribution Probability')
plt.legend()
plt.show()


"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between
[0,2), add append -inf and +inf to both ends of the bins. An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

"""
Acceleration
"""
# goodness of fit test for acceleration data
accel_bins = np.linspace(0, 2, 10)
accel_bins = np.append(accel_bins, [np.inf])
accel_bins = np.insert(accel_bins, 0, -np.inf)

# get the observed counts for each bin
observed, _ = np.histogram(accel, bins=accel_bins)

# get the expected counts for each bin using the normal distribution
norm_accel = np.random.normal(loc=accel_mu, scale=accel_std, size=10000)
expected_counts, _ = np.histogram(norm_accel,bins=accel_bins)
probs = np.diff(norm.cdf(accel_bins, loc=accel_mu, scale=accel_std))
expected = probs * len(accel)

# perform the chi2 test
accel_chi2_stat, accel_p_value = chisquare(f_obs=observed, f_exp=expected)

print(f'Acceleration Data: Chi2 Stat = {accel_chi2_stat}, p-value = {accel_p_value}')

# is it a good fit?
if accel_p_value < 0.05:
    print('The acceleration data is not a good fit for the normal distribution.')
else:
    print('The acceleration data is a good fit for the normal distribution.')


"""
Force Plate
"""
# goodness of fit test for force plate data
force_bins = np.linspace(0, 2, 10)
force_bins = np.append(force_bins, [np.inf])
force_bins = np.insert(force_bins, 0, -np.inf)

# get the observed counts for each bin
observed, _ = np.histogram(force, bins=force_bins)

# get the expected counts for each bin using the normal distribution
norm_force = np.random.normal(loc=force_mu, scale=force_std, size=10000)
expected_counts, _ = np.histogram(norm_force,bins=force_bins)
probs = np.diff(norm.cdf(force_bins, loc=force_mu, scale=force_std))
expected = probs * len(force)

# perform the chi2 test
force_chi2_stat, force_p_value = chisquare(f_obs=observed, f_exp=expected)
print(f'Force Plate Data: Chi2 Stat = {force_chi2_stat}, p-value = {force_p_value}')

# is it a good fit?
if force_p_value < 0.05:
    print('The force plate data is not a good fit for the normal distribution.')
else:
    print('The force plate data is a good fit for the normal distribution.')


"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

# perform the t-test
t_stat, p_value = ttest_ind(accel, force)
print(f'T-test: t-statistic = {t_stat}, p-value = {p_value}')

# is it a significant difference?
if p_value < 0.05:
    print('The RSI means for the acceleration and force plate data are significantly different.')
else:
    print('The RSI means for the acceleration and force plate data are not significantly different.')


"""
Question 4: Calculate the RSI Error for the dataset where error is expressed as the difference between the
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""
print('\n\n-----Question 4-----')

# calculate the RSI error
rsi_error = force - accel

# fit the error distribution to a normal curve
error_mu = rsi_error.mean()
error_std = rsi_error.std()

# generate the x and y points for the plot
x = np.linspace(rsi_error.min(), rsi_error.max(), 1000)
y = norm.pdf(x, loc=error_mu, scale=error_std)

# plot the histogram and the fitted normal curve
plt.hist(rsi_error, bins=16, density=True, alpha=0.5, label='RSI Error Data')
plt.plot(x, y, label='Fitted Normal Distribution')
plt.title('RSI Error and Fitted Normal Distribution')
plt.xlabel('RSI Error (Force Plate RSI - Accelerometer RSI)')
plt.ylabel('Distribution Probability')
plt.legend()
plt.show()

print('See plot for RSI error distribution and fitted normal curve.', end='\n\n')
