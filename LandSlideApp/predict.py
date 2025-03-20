import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


def predict(form_data):
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

    X=np.array(dataset.iloc[:,:-1])
    X=X.astype(dtype='int')
    Y=np.array(dataset.iloc[:,-1])
    Y=Y.reshape(-1,)

    X_train, X_test, y_train, y_test =train_test_split(X,Y,test_size=0.25,
                                                    random_state=42)
    # import seaborn as sb
    # import joblib
    print(X_train.shape)
    model_RR=RandomForestClassifier(n_estimators=100,random_state=42)
    model_RR.fit(X_train,y_train)
    # joblib.dump(model_RR, "RF_model.joblib")
    # X_test=[0,0,0,0,1,1,0,1,1]
    y_predicted_RR=model_RR.predict(np.asarray(form_data).reshape(1,-1))
    # y_predicted_RR=model_RR.predict(X_test)
    print(y_predicted_RR)

    return y_predicted_RR[0]
    # confusion=confusion_matrix(y_test,y_predicted_RR)
    # accuracy=accuracy_score(y_test,y_predicted_RR)
    # # accuracy_score(y_test,y_predicted_RR)
    # print(confusion)
    # print(accuracy)

