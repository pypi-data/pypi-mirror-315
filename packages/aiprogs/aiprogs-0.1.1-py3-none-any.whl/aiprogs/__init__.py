def one():
    return 1

def five():
    return """import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        plt.rcParams['figure.figsize']=[19,8]

        import warnings
        warnings.filterwarnings('ignore')

        from sklearn.datasets import load_iris

        iris=load_iris()

        dir(iris)

        iris_df=pd.DataFrame(data=iris.data,columns=iris.feature_names)
        iris_df.head()

        iris_df['target']=iris.target
        iris_df.head()

        iris_df.info()

        iris.target_names

        iris_df.duplicated().sum()

        iris_df.drop_duplicates(inplace=True)

        iris_df.duplicated().sum()

        #data visualization
        sns.countplot(data=iris_df,x='target')
        plt.title("Count of target values")
        plt.show()

        #outlier
        sns.boxplot(iris_df)
        plt.show()

        #obtain the first quartile
        Q1=iris_df.quantile(0.25)
        #obtain the first quartile
        Q3=iris_df.quantile(0.75)
        #obtain IQR
        IQR=Q3-Q1
        #print IQR
        print(IQR)

        ul=Q3+1.5*IQR
        ll=Q1-1.5*IQR

        iris_df=iris_df[-((iris_df<ll)|(iris_df>ul)).any(axis=1)]

        sns.boxplot(iris_df)
        plt.show()

        x=iris_df.loc[:, :'petal width (cm)'].values
        y=iris_df.loc[:, 'target'].values

        y

        #data normalization
        from sklearn.preprocessing import StandardScaler

        scaler=StandardScaler()

        x=scaler.fit_transform(x)

        #split the data into train and test data
        from sklearn.model_selection import train_test_split

        #split the data into train and test data
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1)

        #model training
        from sklearn.svm import SVC #support vector classifier

        model=SVC(kernel='linear')

        model.fit(x_train,y_train)

        model.score(x_train,y_train)

        #model evaluation
        model.score(x_test,y_test)

        #model prediction
        y_predict=model.predict(x_test)

        y_predict

        y_test

        from sklearn.metrics import confusion_matrix,accuracy_score,recall_score

        confusion_matrix(y_test,y_predict)

        sns.heatmap(confusion_matrix(y_test,y_predict),annot=True,cbar=False)
        plt.xlabel('PREDICTED VALUE',fontsize=18)
        plt.ylabel('ACTUAL VALUE',fontsize=18)
        plt.show()
        """