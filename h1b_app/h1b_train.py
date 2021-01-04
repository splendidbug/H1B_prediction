# -*- coding: utf-8 -*-
"""h1b-train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UwLX4sDFywnL4S0oPcWI9DDHDnawoy7A
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split 
from sklearn import metrics

df = pd.read_csv('/content/drive/MyDrive/h1b_kaggle.csv')
df

df.describe()

df.info()

df.isnull().sum()

import warnings
warnings.filterwarnings("ignore")
df.CASE_STATUS[df['CASE_STATUS']=='REJECTED'] = 'DENIED'
df.CASE_STATUS[df['CASE_STATUS']=='INVALIDATED'] = 'DENIED'
df.CASE_STATUS[df['CASE_STATUS']=='PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED'] = 'DENIED'
df.CASE_STATUS[df['CASE_STATUS']=='WITHDRAWN'] = 'DENIED'
df.CASE_STATUS[df['CASE_STATUS']=='CERTIFIED-WITHDRAWN'] = 'CERTIFIED'

df['CASE_STATUS'].value_counts()

df['EMPLOYER_NAME'].describe()

emp_mode = df['EMPLOYER_NAME'].mode()[0]
emp_mode

df['EMPLOYER_NAME'].fillna(emp_mode, inplace=True)

df.drop(labels=['Unnamed: 0','YEAR','lon', 'lat'], axis=1,inplace=True)
df.isnull().sum()

df['JOB_TITLE'].mode()

df['JOB_TITLE'].fillna(df['JOB_TITLE'].mode()[0], inplace = True)

df.isnull().sum()

df['PREVAILING_WAGE'].mode()

df['PREVAILING_WAGE'].fillna(df['PREVAILING_WAGE'].mode()[0], inplace = True)
df['SOC_NAME'].fillna(df['SOC_NAME'].mode()[0], inplace = True)
df['FULL_TIME_POSITION'].fillna(df['FULL_TIME_POSITION'].mode()[0], inplace = True)
df.isnull().sum()

df.dropna(inplace=True)
df.isnull().sum()

df['WORKSITE'].describe()

df['CASE_STATUS'].value_counts()

from sklearn.utils import resample
# Separate majority and minority classes
df_majority = df[df.CASE_STATUS=='CERTIFIED']
df_minority = df[df.CASE_STATUS=='DENIED']
 
# Downsample majority class
df_majority_downsampled = resample(df_majority, 
                                 replace=False,    # sample without replacement
                                 n_samples=184163,     # to match minority class
                                 random_state=123) # reproducible results
 
# Combine minority class with downsampled majority class
df_downsampled = pd.concat([df_majority_downsampled, df_minority])
df_downsampled['CASE_STATUS'].value_counts()

df_downsampled.info()

df_downsampled['PREVAILING_WAGE'].describe()

"""
for i in range(df_downsampled.shape[0]):
    if (df_downsampled['PREVAILING_WAGE'].iloc[i] <=50000):
        df_downsampled['PREVAILING_WAGE'].iloc[i] = "VERY LOW"
    elif (df_downsampled['PREVAILING_WAGE'].iloc[i] >50000 and df_downsampled['PREVAILING_WAGE'].iloc[i] <= 70000):
        df_downsampled['PREVAILING_WAGE'].iloc[i] = "LOW"
    elif (df_downsampled['PREVAILING_WAGE'].iloc[i] >70000 and df_downsampled['PREVAILING_WAGE'].iloc[i] <= 90000):
        df_downsampled['PREVAILING_WAGE'].iloc[i] = "MEDIUM"
    elif (df_downsampled['PREVAILING_WAGE'].iloc[i] >90000 and df_downsampled['PREVAILING_WAGE'].iloc[i]<=150000):
        df_downsampled['PREVAILING_WAGE'].iloc[i] = "HIGH"
    elif (df_downsampled['PREVAILING_WAGE'].iloc[i] >=150000):
        df_downsampled['PREVAILING_WAGE'].iloc[i] = "VERY HIGH"
    print(i)
"""

def wage_calc(wage):
    if(wage <=50000):
        return 'VERY LOW'
    elif (wage >50000 and wage <=70000):
        return "LOW"
    elif (wage >70000 or wage <=90000):
        return "MEDIUM"
    elif (wage >90000 or wage <=150000):
        return "HIGH"
    elif (wage >=150000):
        return "VERY HIGH"

df_downsampled['PREVAILING_WAGE'] = df_downsampled['PREVAILING_WAGE'].apply(wage_calc)
df_downsampled

###############################################################################

def categorisation_visagrant(ratio_of_acceptance):
    if ratio_of_acceptance == -1:
        return "AR"
    elif ratio_of_acceptance >=0.0 and ratio_of_acceptance<0.20:
        return "VLA"
    elif ratio_of_acceptance>=0.20 and ratio_of_acceptance<0.40:
        return "LA"
    elif ratio_of_acceptance>=0.40 and ratio_of_acceptance<0.60:
        return "MA"
    elif ratio_of_acceptance>=0.60 and ratio_of_acceptance<0.80:
        return "HA"
    elif ratio_of_acceptance>=0.80:
        return "VHA"

def states(work_site):
    return work_site.split(', ')[1]

df_downsampled['WORKSITE'] = df_downsampled['WORKSITE'].apply(states)

df_downsampled.WORKSITE.nunique()

df_downsampled.describe()

n = 5
df_downsampled['EMPLOYER_NAME'].value_counts()[:n].index.tolist()

def employer(emp):
    if('UNIVERSITY' in emp):
        return 'UNIVERSITY'
    elif ('INFOSYS' in emp):
        return "INFOSYS"
    elif ('IBM' in emp):
        return "IBM"
    elif ('TATA' in emp):
        return "TATA"
    elif ('WIPRO' in emp):
        return "WIPRO"
    elif ('DELOITTE' in emp):
        return "DELOITTE"
    else:
        return "OTHER"

df_downsampled['EMPLOYER_NAME'] = df_downsampled['EMPLOYER_NAME'].apply(employer)
df_downsampled

df_downsampled.describe()

def soc_recreate(soc):
    soc=soc.lower()
    if('computer' in soc or 'programmer' in soc or 'software' in soc or 'web developer' in soc or 'database' in soc):
        return 'computer guy'
    elif ('math' in soc or 'statistic' in soc or 'predictive model' in soc or 'stats' in soc):
        return "math fellow"
    elif ('teacher' in soc or 'linguist' in soc or 'professor' in soc or 'teach' in soc or 'school principal' in soc or 'principal' in soc):
        return "teacher"
    elif ('medical' in soc or 'doctor' in soc or 'physician' in soc or 'dentist' in soc or 'health' in soc or 'physical therapists' in soc or 'surgeon' in soc or 'nurse' in soc or 'psychiatr' in soc):
        return "medical"
    elif ('physicist' in soc or 'chemist' in soc or 'biology' in soc or 'scientist' in soc or 'biologi' in soc or 'clinical research' in soc):
        return "advance science"
    elif ('public relation' in soc or 'manage' in soc or 'management' in soc or 'operation' in soc or 'chief' in soc or 'plan' in soc or 'executive' in soc):
        return "manager"
    elif ('advertis' in soc or 'marketing' in soc or 'promotion' in soc or 'market research' in soc):
        return "marketing"
    elif ('business' in soc or 'business analyst' in soc or 'business systems analyst' in soc):
        return "business"
    elif ('accountant' in soc or 'finance' in soc or 'financial' in soc):
        return "financial"
    elif ('engineer' in soc or 'architect' in soc or 'surveyor' in soc or 'carto' in soc or 'technician' in soc or 'drafter' in soc or 'information security' in soc or 'information tech' in soc):
        return "arch and eng"
    else:
        return "OTHER"

df_downsampled['SOC_NAME'] = df_downsampled['SOC_NAME'].apply(soc_recreate)
df_downsampled

df_downsampled

df_downsampled2 = df_downsampled.drop('JOB_TITLE', axis=1)
df_downsampled2

df_downsampled2=pd.get_dummies(df_downsampled2, columns=['EMPLOYER_NAME', 'SOC_NAME', 'PREVAILING_WAGE', 'WORKSITE'])
df_downsampled2['CASE_STATUS'] = df_downsampled2['CASE_STATUS'].map({'CERTIFIED':1, 'DENIED':0})
df_downsampled2['FULL_TIME_POSITION'] = df_downsampled2['FULL_TIME_POSITION'].map({'Y':1, 'N':0})

df_downsampled2

df_downsampled2.reset_index(inplace=True)

df_downsampled2

df_downsampled2.drop('index', axis=1, inplace=True)
df_downsampled2

X=df_downsampled2.copy()
X.drop('CASE_STATUS', axis=1, inplace=True)
y=df_downsampled2['CASE_STATUS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.20, random_state=10)

dTree = DecisionTreeClassifier(criterion = 'gini', random_state=10)
dTree.fit(X_train, y_train)

print(dTree.score(X_train, y_train))
print(dTree.score(X_test, y_test))

clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

y_prob = dTree.predict_proba(X_test)

print("test", y_test[:10])
print("pred", y_pred[:10])
print()

print(metrics.confusion_matrix(y_test,y_pred))
print(metrics.classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators = 75, random_state = 50)
# Train the model on training data
rf.fit(X_train, y_train)

y_pred_rf =  rf.predict(X_test)
probs = rf.predict_proba(X_test)

print("test", y_test[:10])
print("pred", y_pred[:10])
print(metrics.confusion_matrix(y_test,y_pred_rf))
print(metrics.classification_report(y_test, y_pred_rf))

import pickle
filename = 'rf_model.sav'
pickle.dump(rf, open(filename, 'wb'))

X_test

all_cols = ['FULL_TIME_POSITION',	'EMPLOYER_NAME_DELOITTE',	'EMPLOYER_NAME_IBM',	'EMPLOYER_NAME_INFOSYS',	'EMPLOYER_NAME_OTHER',	'EMPLOYER_NAME_TATA',	'EMPLOYER_NAME_UNIVERSITY',	'EMPLOYER_NAME_WIPRO',	'SOC_NAME_OTHER',	'SOC_NAME_advance science',	'SOC_NAME_arch and eng',	'SOC_NAME_business',	'SOC_NAME_computer guy',	'SOC_NAME_financial',	'SOC_NAME_manager',	'SOC_NAME_marketing',	'SOC_NAME_math fellow',	'SOC_NAME_medical',	'SOC_NAME_teacher',	'PREVAILING_WAGE_LOW',	'PREVAILING_WAGE_MEDIUM',	'PREVAILING_WAGE_VERY LOW',	'WORKSITE_ALABAMA',	'WORKSITE_ALASKA',	'WORKSITE_ARIZONA',	'WORKSITE_ARKANSAS',	'WORKSITE_CALIFORNIA',	'WORKSITE_COLORADO',	'WORKSITE_CONNECTICUT',	'WORKSITE_DELAWARE',	'WORKSITE_DISTRICT OF COLUMBIA',	'WORKSITE_FLORIDA',	'WORKSITE_GEORGIA',	'WORKSITE_HAWAII',	'WORKSITE_IDAHO',	'WORKSITE_ILLINOIS',	'WORKSITE_INDIANA',	'WORKSITE_IOWA',	'WORKSITE_KANSAS',	'WORKSITE_KENTUCKY',	'WORKSITE_LOUISIANA',	'WORKSITE_MAINE',	'WORKSITE_MARYLAND',	'WORKSITE_MASSACHUSETTS',	'WORKSITE_MICHIGAN',	'WORKSITE_MINNESOTA',	'WORKSITE_MISSISSIPPI',	'WORKSITE_MISSOURI',	'WORKSITE_MONTANA',	'WORKSITE_NA',	'WORKSITE_NEBRASKA', 'WORKSITE_NEVADA',	'WORKSITE_NEW HAMPSHIRE',	'WORKSITE_NEW JERSEY',	'WORKSITE_NEW MEXICO',	'WORKSITE_NEW YORK',	'WORKSITE_NORTH CAROLINA',	'WORKSITE_NORTH DAKOTA',	'WORKSITE_OHIO',	'WORKSITE_OKLAHOMA',	'WORKSITE_OREGON',	'WORKSITE_PENNSYLVANIA',	'WORKSITE_PUERTO RICO',	'WORKSITE_RHODE ISLAND',	'WORKSITE_SOUTH CAROLINA',	'WORKSITE_SOUTH DAKOTA',	'WORKSITE_TENNESSEE',	'WORKSITE_TEXAS',	'WORKSITE_UTAH',	'WORKSITE_VERMONT',	'WORKSITE_VIRGINIA',	'WORKSITE_WASHINGTON',	'WORKSITE_WEST VIRGINIA',	'WORKSITE_WISCONSIN',	'WORKSITE_WYOMING']

df_pred = pd.DataFrame(columns=all_cols)
df_pred.loc[0]=0
df_pred

full_time = 'Y'
emp_name =  'OTHER'
soc = 'programmer'
wage = 80000
state='ALASKA'

state='WORKSITE_'+ state

if(full_time=='Y'):
    full_time=1
    
else:
    full_time=0


if('UNIVERSITY' in emp_name):
    emp_name='EMPLOYER_NAME_UNIVERSITY'
elif('INFOSYS' in emp_name):
    emp_name='EMPLOYER_NAME_INFOSYS'
elif('IBM' in emp_name):
    emp_name='EMPLOYER_NAME_IBM'
elif('TATA' in emp_name):
    emp_name='TATA'
elif('WIPRO' in emp_name):
    emp_name='EMPLOYER_NAME_WIPRO'
elif('DELOITTE' in emp_name):
    emp_name='EMPLOYER_NAME_DELOITTE'
else:
    emp_name='EMPLOYER_NAME_OTHER'

if('computer' in soc or 'programmer' in soc or 'software' in soc or 'web developer' in soc or 'database' in soc):
        soc = 'SOC_NAME_'+'computer guy'
elif ('math' in soc or 'statistic' in soc or 'predictive model' in soc or 'stats' in soc):
        soc = "SOC_NAME_"+"math fellow"
elif ('teacher' in soc or 'linguist' in soc or 'professor' in soc or 'teach' in soc or 'school principal' in soc or 'principal' in soc):
        soc = "SOC_NAME_"+"teacher"
elif ('medical' in soc or 'doctor' in soc or 'physician' in soc or 'dentist' in soc or 'health' in soc or 'physical therapists' in soc or 'surgeon' in soc or 'nurse' in soc or 'psychiatr' in soc):
        soc = "SOC_NAME_"+"medical"
elif ('physicist' in soc or 'chemist' in soc or 'biology' in soc or 'scientist' in soc or 'biologi' in soc or 'clinical research' in soc):
        soc = "SOC_NAME_"+"advance science"
elif ('public relation' in soc or 'manage' in soc or 'management' in soc or 'operation' in soc or 'chief' in soc or 'plan' in soc or 'executive' in soc):
        soc = "SOC_NAME_"+"manager"
elif ('advertis' in soc or 'marketing' in soc or 'promotion' in soc or 'market research' in soc):
        soc = "SOC_NAME_"+"marketing"
elif ('business' in soc or 'business analyst' in soc or 'business systems analyst' in soc):
        soc = "SOC_NAME_"+"business"
elif ('accountant' in soc or 'finance' in soc or 'financial' in soc):
        soc = "SOC_NAME_"+"financial"
elif ('engineer' in soc or 'architect' in soc or 'surveyor' in soc or 'carto' in soc or 'technician' in soc or 'drafter' in soc or 'information security' in soc or 'information tech' in soc):
        soc = "SOC_NAME_"+"arch and eng"
else:
        soc = "SOC_NAME_"+"OTHER"

if(wage <=50000):
        wage = 'PREVAILING_WAGE_VERY LOW'
elif (wage >50000 and wage <=70000):
        wage = "PREVAILING_WAGE_LOW"
elif (wage >70000 or wage <=90000):
        wage = "PREVAILING_WAGE_MEDIUM"
elif (wage >90000 or wage <=150000):
        wage = "PREVAILING_WAGE_HIGH"
elif (wage >=150000):
        wage = "PREVAILING_WAGE_VERY HIGH"

df_pred['FULL_TIME_POSITION'] = full_time

lst = [emp_name,soc, wage, state]
df_pred[lst]=1

df_pred

loaded_model = pickle.load(open(filename, 'rb'))
y_pred_rf =  loaded_model.predict(df_pred)
y_pred_rf[0]

