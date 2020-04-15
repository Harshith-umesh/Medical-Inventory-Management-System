import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn import svm


import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('train.csv', index_col=False)
df.columns = ['id','months_since_last_donation','num_donations','vol_donations','months_since_first_donation', 'class']
df = df.drop(['id'], axis=1)

#Enter test values in the below line here
test = pd.DataFrame(columns=['months_since_last_donation','num_donations','vol_donations','months_since_first_donation'], data=[[2, 6, 1500, 16]])

df["class"] = df["class"].astype(int)

Y_train = df["class"]

X_train = df.drop(labels = ["class"],axis = 1)

sc = StandardScaler()
X_train_scaled = sc.fit_transform(X_train)
test_scaled = sc.transform(test)

clf = svm.SVC(kernel='linear', C = 1.0, probability=True)
clf.fit(X_train_scaled,Y_train)

predictions = clf.predict_proba(test_scaled)
predictions = predictions[:,1]

if(predictions[0]>0.24):
    output = "Yes, Will donate"
else:
    output = "No, Will not donate"

print(output)
