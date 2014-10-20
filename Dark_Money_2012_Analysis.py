#execfile("Dark_Money_2012_Munging.py")

# In[247]:

from pandas.stats.api import ols
res = ols(y=issues_all_df['Percentage_of_Vote'], x=issues_all_df[['Rate', 'Spt/Week']])
res

# In[248]:

issues_all_df[['Rate', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Length_in_Sec', 'AM', 'PM',
                                                                  '10:00', '10:30', '11:00', '11:30', '11:35', '12:00', 
                                                                  '12:05', '12:30', '12:35', '1:00', '1:05', '1:30', 
                                                                  '1:35', '2:00', '3:00', '3:30', '4:00', '4:30', '4:59', 
                                                                  '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '7:58', 
                                                                  '8:00', '8:30', '9:00', '9:30', 'Dark_Money', 'Liberal', 
                                                                  'Local', 'Renewable_Energy', 'Pro_Collective_Bargaining',
                                                                  'Casino_Expansion', 'Anti_2nd_Detroit_Bridge', 'Homecare_in_State_Constitution', 
                                                                  'Romney_for_President', 'Govt_Emergency_Fund', 'McCormack_for_Supreme_Ct_D', 
                                                                  'Universal_Healthcare', 'Stabenow_for_Senate_D_I', 'In_Place']]


# In[249]:

issues_all_df[['Rate', 'Spt/Week', 'Total_Dollars']]


# In[250]:

X = issues_all_df[['Rate', 'Spt/Week']]
y = issues_all_df['Percentage_of_Vote']
print X.shape
print y.shape


# Splitting the data
# ==================
# We want to split the data into train set and test set. We fit the linear model on the train set, and we show that it performs good on test set. 
# 
# Before splitting the data, we shuffle (mix) the examples, because for some datasets the examples are ordered. 
# 
# If we wouldn't shuffle, train set and test set could be totally different, thus linear model fitted on train set wouldn't be valid on test set.
# Now we shuffle:
# 

# In[251]:

from sklearn.utils import shuffle
X, y = shuffle(X, y, random_state=1)
print X.shape
print y.shape


# Each example of data has 7 columns in total.
# 
# We want to work with 1-dim data because it is simple to visualize. Therefore select only one column, e.g column 2 and fit linear model on it:

# In[252]:

# Use only one column from data
print(X.shape)
X = X[:, 0:1]
print(X.shape)


# Split the data into training/testing sets

# In[253]:

train_set_size = 1000
X_train = X[:train_set_size]  # selects first 250 rows (examples) for train set
X_test = X[train_set_size:]   # selects from row 250 until the last one for test set
print(X_train.shape)
print(X_test.shape)


# Split the targets into training/testing sets

# In[254]:

y_train = y[:train_set_size]   # selects first 250 rows (targets) for train set
y_test = y[train_set_size:]    # selects from row 250 until the last one for test set
print(y_train.shape)
print(y_test.shape)


# Now we can look at our train data. We can see that the examples have linear relation. 
# 
# Therefore, we can use linear model to make good classification of our examples.
# 
# ##Well, this isn't totally true --> what are those guys around 1??

# In[255]:

plt.scatter(X_train, y_train, color = 'red')
plt.scatter(X_test, y_test, color = 'green')
plt.xlabel('Advertiser_Data')
plt.ylabel('Election_Outcome');


# Linear regression
# =================
# Create linear regression object, which we use later to apply linear regression on data

# In[256]:

from sklearn import linear_model
regr = linear_model.LinearRegression()


# Fit the model using the training set

# In[257]:

regr.fit(X_train, y_train);


# We found the coefficients and the bias (the intercept)

# In[258]:

print(regr.coef_)
print(regr.intercept_)


# Now we calculate the mean square error on the test set

# In[259]:

# The mean square error
print("Training error: ", np.mean((regr.predict(X_train) - y_train) ** 2))
print("Test     error: ", np.mean((regr.predict(X_test) - y_test) ** 2))


# Plotting data and linear model
# ==============================
# Now we want to plot the train data and teachers (marked as dots). 
# 
# With line we represents the data and predictions (linear model that we found):
# 

# In[260]:

# Visualises dots, where each dot represent a data exaple and corresponding teacher
plt.scatter(X_train, y_train,  color='black')
# Plots the linear model
plt.plot(X_train, regr.predict(X_train), color='blue', linewidth=3);
plt.xlabel('Ad Rate')
plt.ylabel('Election_Outcome')


# We do similar with test data, and show that linear model is valid for a test set:

# In[261]:

# Visualises dots, where each dot represent a data exaple and corresponding teacher
plt.scatter(X_test, y_test,  color='black')
# Plots the linear model
plt.plot(X_test, regr.predict(X_test), color='blue', linewidth=3);
plt.xlabel('Data')
plt.ylabel('Target');


# In[262]:

Xdf = pd.DataFrame(issues_all_df[['Rate', 'Spt/Week']])
Xdf


# In[263]:

ydf = pd.DataFrame(issues_all_df['Percentage_of_Vote'])
ydf


# In[264]:

multi_regression = regr.fit(Xdf, ydf)


# In[265]:

print(regr.coef_)
coef =multi_regression
print(regr.intercept_)


# In[266]:

print("error: ", np.mean((regr.predict(Xdf) - ydf) ** 2))


# In[267]:

Xdf_alt = Xdf.iloc[:, 1:]
multi_regression_alt = regr.fit(Xdf_alt, ydf)
print(regr.coef_)
coef_alt = multi_regression
print(regr.intercept_)
print("error: ", np.mean((regr.predict(Xdf_alt) - ydf) ** 2))


# #Soma: I think this is the graph that is important because I THINK it says what coefficients pull the regression line up?

# In[268]:

Xdf_alt_2 = Xdf.iloc[:, (0,1)]
multi_regression_alt = regr.fit(Xdf_alt_2, ydf)
print dir(multi_regression_alt)
print(regr.coef_)
coef_alt_2 = multi_regression_alt
print(regr.intercept_)
print("error: ", np.mean((regr.predict(Xdf_alt_2) - ydf) ** 2))


# In[269]:

multi_regression_alt.score()


# In[ ]:

#x.shape


# In[270]:

print coef_alt
print range(1,2)
print coef_alt_2[0]
coef[0]


# In[271]:

plot(range(1,2), coef_alt[0], label = "alt")
plot([0,1], coef_alt_2[0], label = "alt 2")
plot(range(2), coef[0], label = "regression")
grid()
legend(loc = 2)
plt.xlabel('Ad Rate and Spots Per Week')
plt.ylabel('Election_Outcome')


# In[272]:

issues_all_df.columns


# In[276]:

import numpy as np

# Generate some data that lies along a line

x = issues_all_df['Spt/Week']
y = issues_all_df['Rate']
z = issues_all_df['Percentage_of_Vote']

data = np.concatenate((x[:, np.newaxis], 
                       y[:, np.newaxis], 
                       z[:, np.newaxis]), 
                      axis=1)

# Perturb with some Gaussian noise
#data += np.random.normal(size=data.shape) * 0.4

# Calculate the mean of the points, i.e. the 'center' of the cloud
datamean = data.mean(axis=0)

# Do an SVD on the mean-centered data.
uu, dd, vv = np.linalg.svd(data - datamean)

# Now vv[0] contains the first principal component, i.e. the direction
# vector of the 'best fit' line in the least squares sense.

# Now generate some points along this best fit line, for plotting.

# I use -7, 7 since the spread of the data is roughly 14
# and we want it to have mean 0 (like the points we did
# the svd on). Also, it's a straight line, so we only need 2 points.
linepts = vv[0] * np.mgrid[-7:7:2j][:, np.newaxis]

# shift by the mean to get the line in the right place
linepts += datamean

# Verify that everything looks right.

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as m3d

ax = m3d.Axes3D(plt.figure())
ax.scatter3D(*data.T)
ax.plot3D(*linepts.T)
plt.show()


# In[274]:

get_ipython().system(u'pip install statsmodels formula')


# In[275]:

import statsmodels.api as sm
#import statsmodels.formula.api as smf


plt.scatter(issues_all_df['Rate'], issues_all_df['Spt/Week'], alpha=0.3)
plt.xlabel('Spots Per Week')
plt.ylabel('Rate')

income_linspace = np.linspace(issues_all_df['Rate'].min(), issues_all_df['Spt/Week'].max(), 100)

#est = smf.OLS(formula='Rate ~ Spt/Week + hlthp', data=issues_all_df).fit()
est = smf.OLS(issues_all_df['Rate'], issues_all_df['Spt/Week']).fit()


plt.plot(income_linspace, est.params[0] + est.params[1] * income_linspace + est.params[2] * 0, 'r')
plt.plot(income_linspace, est.params[0] + est.params[1] * income_linspace + est.params[2] * 1, 'g')
short_summary(est)


# In[ ]:

from statsmodels.regression.linear_model import OLS
import statsmodels.formula.api 

# load the boston housing dataset - median house values in the Boston area
#df = pd.read_csv('http://vincentarelbundock.github.io/Rdatasets/csv/MASS/Boston.csv')

# plot lstat (% lower status of the population) against median value
plt.figure(figsize=(6 * 1.618, 6))
plt.scatter(issues_all_df['Rate'], issues_all_df['Spt/Week'], s=10, alpha=0.3)
plt.xlabel('Rate')
plt.ylabel('Spt/Week')

# points linearlyd space on lstats
x = pd.DataFrame({'Rate': np.linspace(issues_all_df['Rate'].min(), issues_all_df['Rate'].max(), 100)})

# 1-st order polynomial
poly_1 = smf.OLS(formula='Spt/Week ~ 1 + Rate', data=issues_all_df).fit()
plt.plot(x.lstat, poly_1.predict(x), 'b-', label='Poly n=1 $R^2$=%.2f' % poly_1.rsquared, 
         alpha=0.9)

# 2-nd order polynomial
poly_2 = smf.OLS(formula='Spt/Week ~ 1 + Rate + I(Rate ** 2.0)', data=df).fit()
plt.plot(x.lstat, poly_2.predict(x), 'g-', label='Poly n=2 $R^2$=%.2f' % poly_2.rsquared, 
         alpha=0.9)

# 3-rd order polynomial
poly_3 = smf.OLS(formula='Spt/Week ~ 1 + Rate + I(Rate ** 2.0) + I(Rate ** 3.0)', data=df).fit()
plt.plot(x.lstat, poly_3.predict(x), 'r-', alpha=0.9,
         label='Poly n=3 $R^2$=%.2f' % poly_3.rsquared)

plt.legend()


# #Non-Linear Regression:

# In[ ]:

get_ipython().magic(u'matplotlib inline')
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# In[ ]:

xdata = issues_all_df[['Rate', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Length_in_Sec', 'AM', 'PM',
                                                                  'Dark_Money', 'Liberal', 
                                                                  'Local', 'Renewable_Energy', 'Pro_Collective_Bargaining',
                                                                  'Casino_Expansion', 'Anti_2nd_Detroit_Bridge', 'Homecare_in_State_Constitution', 
                                                                  'Romney_for_President', 'Govt_Emergency_Fund', 'McCormack_for_Supreme_Ct_D', 
                                                                  'Universal_Healthcare', 'Stabenow_for_Senate_D_I', 'In_Place']]
ydata = issues_all_df['Percentage_of_Vote']


# In[ ]:

plt.plot(xdata,ydata,'*')
plt.xlabel('xdata')
plt.ylabel('ydata');


# In[ ]:

def func(x, p1,p2):
  return p1*np.cos(p2*x) + p2*np.sin(p1*x)


# In[ ]:

#popt, pcov = curve_fit(func, xdata, ydata,p0=(1.0,0.2))
#popt


# In[ ]:




# #Making everything about dark money:

# In[ ]:

non_candidate_2012_df[non_candidate_2012_df['Dark_Money'] ==300]['Advertiser_Clean2'].value_counts()


# In[ ]:

dark_money_2012_df = non_candidate_2012_df[non_candidate_2012_df['Dark_Money'] ==300]


# In[ ]:

ad_total_grouped = dark_money_2012_df['Total_Dollars'].groupby(dark_money_2012_df['Ad_Focus'])


# In[ ]:

ad_total_size = ad_total_grouped.size()


# ###How do I sort the x axis by normal distribution, not alphabet?

# In[ ]:

ad_total_size.plot(kind = 'barh', xlim = [0, 800], 
                   title = "Dark Money Ad Focus 2012 (Color: Advertiser's Politics)", 
                   color = ['r', 'r'])


# In[ ]:

ad_local_grouped = dark_money_2012_df['Local'].groupby(dark_money_2012_df['Ad_Focus'])


# In[ ]:

ad_local_size = ad_local_grouped.size()


# In[ ]:

local_advertisers = dark_money_2012_df[dark_money_2012_df['Local'] == 300]


# In[ ]:

national_advertisers = dark_money_2012_df[dark_money_2012_df['Local'] == 0]


# In[ ]:

local_advertisers.columns


# ###How do I smooth out these lines?
# 
# ###I want to add in two markers: 30 days before primary and 60 days before general election
# 
# ###Hypothesis: there is so much more spending by national groups in the early days because they don't have to report those days to the FEC.

# #National dark money only for 2012

# In[ ]:

#local_advertisers.plot(x = 'Ending_Date', y = 'Total_Dollars', color = 'brown')


# In[ ]:

import numpy as np
import matplotlib.pyplot as plt

#local_advertisers['Cum_Dollars'] = np.cumsum(local_advertisers['Total_Dollars'])
national_advertisers['Cum_Dollars'] = np.cumsum(national_advertisers['Total_Dollars'])

#local_y = cumsum(local_advertisers['Total_Dollars'])
#local_x = local_advertisers['Air_or_Ending_Date']


#local_advertisers.plot('Ending_Date', 'Cum_Dollars', color = 'blue')

national_advertisers.plot(x = 'Ending_Date', ylim = [0,1000000],
                          title = "Ad Spending Over Time 2012 (Green: National)", 
                          y = 'Cum_Dollars', color = 'green')


# In[ ]:

#national_advertisers.plot(x = 'Ending_Date', 
 #                         title = "Ad Spending Sched (Brown: Local Advertiser, Green: National Advertiser)", 
  #                        y = 'Total_Dollars', color = 'green')


# In[ ]:

local_ad_total_grouped = local_advertisers['Total_Dollars'].groupby(dark_money_2012_df['Ad_Focus'])

national_ad_total_grouped = national_advertisers['Total_Dollars'].groupby(dark_money_2012_df['Ad_Focus'])

local_ad_total_size = local_ad_total_grouped.size()

national_ad_total_size = national_ad_total_grouped.size()


# In[ ]:

all_total_grouped = non_candidate_2012_df['Total_Dollars'].groupby(non_candidate_2012_df['Ad_Focus'])


# In[ ]:




# In[ ]:

all_total_grouped = non_candidate_2012_df['Total_Dollars'].groupby(non_candidate_2012_df['Dark_Money', 'Ad_Focus'])
#all_total_size = all_total_grouped.size()


# In[ ]:




# In[ ]:


all_total_size.plot(kind = 'barh', xlim = [0, 800], 
                   title = "Ad Focus 2012 (Purple: Dark Money)",
                   color = ['yellow'])
ad_total_size.plot(kind = 'barh', xlim = [0, 800],  
                   color = ['purple'])


# In[ ]:

all_total_grouped = non_candidate_2012_df['Total_Dollars'].groupby(non_candidate_2012_df['Ad_Focus'])
all_total_size = all_total_grouped.size()


# In[ ]:

all_total_size.plot(kind = 'barh', xlim = [0, 800], 
                   title = "Ad Focus 2012 (Purple: Dark Money)",
                   color = ['yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'purple',
                            'purple', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
                             'yellow', 'yellow',])


# In[ ]:




# In[ ]:

#local_ad_total_size.plot(kind = 'bar', title = "Negative vs Positive Ads Local Groups Only 2012 (Purple: Negative, Yellow: Positive)", color = ['purple', 'purple','purple', 'purple', 'purple', 'purple', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow'])


# In[ ]:

#national_ad_total_size.plot(kind = 'bar', title = "Negative vs Positive Ads National Groups Only 2012(Purple: Negative, Yellow: Positive)", color = ['purple', 'purple', 'purple',  'purple', 'purple', 'yellow', 'yellow',  'yellow', 'yellow', 'yellow'])


# In[ ]:

#local_ad_total_size.plot(kind = 'barh', color = 'blue')
national_ad_total_size.plot(kind = 'barh', 
                            title = "Local Spending vs National Spending 2012 (Green: National)", color = 'green')

