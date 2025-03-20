import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import seaborn as sns
import matplotlib.pyplot as plt
dataset=pd.read_csv('landslide_dataset.csv')


print(dataset)

Season_encoder=LabelEncoder()
encoded_season=Season_encoder.fit_transform(y=dataset.Season)
dataset.Season=encoded_season

Slop_encoder=LabelEncoder()
encoded_slope=Slop_encoder.fit_transform(y=dataset.Slope)
dataset.Slope=encoded_slope

Stress_encoder=LabelEncoder()
encoded_stress=Stress_encoder.fit_transform(y=dataset.Stress)
dataset.Stress=encoded_stress

Type_encoder=LabelEncoder()
encoded_type=Type_encoder.fit_transform(y=dataset.Type)
dataset.Type=encoded_type

print(dataset)
for label, original_class in zip(Season_encoder.transform(Season_encoder.classes_), Season_encoder.classes_):
    print(f"{label}: {original_class}")
   
for label, original_class in zip(Type_encoder.transform(Type_encoder.classes_), Type_encoder.classes_):
    print(f"{label}: {original_class}")
  
for label, original_class in zip(Stress_encoder.transform(Stress_encoder.classes_), Stress_encoder.classes_):
    print(f"{label}: {original_class}")
    

X=np.array(dataset.iloc[:,:-1])
X=X.astype(dtype='int')
Y=np.array(dataset.iloc[:,-1])
Y=Y.reshape(-1,)

X_train, X_test, y_train, y_test =train_test_split(X,Y,test_size=0.25,
                                                   random_state=42)

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import svm

# import seaborn as sb
# import joblib
print(X_train.shape)


model_RR=RandomForestClassifier(n_estimators=100,random_state=42)
model_RR.fit(X_train,y_train)
# joblib.dump(model_RR, "RF_model.joblib")
# X_test=[0,0,0,0,1,1,0,1,1]

# y_predicted_RR=model_RR.predict(np.asarray(X_test).reshape(1,-1))
y_predicted_RR=model_RR.predict(X_test)
print(y_predicted_RR)
confusion=confusion_matrix(y_test,y_predicted_RR)
accuracy=accuracy_score(y_test,y_predicted_RR)
# accuracy_score(y_test,y_predicted_RR)
print(confusion)
print(accuracy)

report = classification_report(y_test, y_predicted_RR)
print(report)
sns.heatmap(confusion,
			annot=True,
			fmt='g',
			xticklabels=['Normal','Landslide'],
			yticklabels=['Normal','Landslide'])
plt.ylabel('Prediction',fontsize=13)
plt.xlabel('Actual',fontsize=13)
plt.title('Confusion Matrix',fontsize=17)
plt.show()
print('-'*30)

