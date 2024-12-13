def threeA():
    return """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        s_df=pd.read_csv("Salary_Data.csv")

        s_df.info()

        plt.scatter(data=s_df, x= "YearsExperience",y="Salary")
        plt.title("Salary based on year of experience")
        plt.xlabel("Year of experience")
        plt.ylabel("Salary")
        plt.show()

        x=s_df.loc[:, "YearsExperience"].values
        y=s_df.loc[:,"Salary"].values

        from sklearn.model_selection import train_test_split

        x_train,x_test,y_train,y_test,= train_test_split(x,y,test_size=0.3,random_state=0)

        x_train.shape,x_test.shape,y_train.shape,y_test.shape

        from sklearn.linear_model import LinearRegression

        reg_model=LinearRegression()

        reg_model.fit(x_train.reshape(-1,1),y_train.reshape(-1,1))

        reg_model.coef_

        reg_model.intercept_

        y_predicted = reg_model.predict(x_test.reshape(-1,1))

        from sklearn.metrics import mean_squared_error
        mse = mean_squared_error(y_test,y_predicted)
        rmse = np.sqrt(mse)

        plt.scatter(x=x_test, y=y_test, color='red')
        plt.scatter(x = x_test, y=y_predicted, color='green')
        plt.title("Salary Test Vs Predicted")
        plt.xlabel("Years of Experience")
        plt.ylabel("Salary")

        data={'voltage':[0,1,2,3,4,5,6,7,8,9,10],'current':[0,1,2,2.99,4,5,6,6.99,8,9,10]}

        df=pd.DataFrame(data)

        df

        plt.scatter(data=df, x= "voltage",y="current")
        plt.title("Voltage Vs Current")
        plt.xlabel("Voltage")
        plt.ylabel("Current")
        plt.show()

        homeprice={'area':[2600,3000,3200,3600,4000],'price':[550000,565000,610000,680000,725000]}

        df=pd.DataFrame(homeprice)

        df

        plt.scatter(data=df, x= "area",y="price")
        plt.title("House Area Vs Price")
        plt.xlabel("Area")
        plt.ylabel("Price")
        plt.show()

        s_df.shape

        s_df.info()

        s_df.head()

        s_df.describe()

        plt.scatter(data=s_df, x= "YearsExperience",y="Salary")
        plt.title("Salary based on the Years of experience")
        plt.xlabel("Years of experience")
        plt.ylabel("Salary")
        plt.show()

        x=s_df.loc[:, 'YearsExperience'].values
        y=s_df.loc[:,'Salary'].values

        from sklearn.model_selection import train_test_split

        x_train,x_test,y_train,y_test,= train_test_split(x,y,test_size=0.3,random_state=0)

        x_train.shape,x_test.shape,y_train.shape,y_test.shape

        type(x_train)

        from sklearn.linear_model import LinearRegression

        reg_model = LinearRegression()
        reg_model.fit(x_train.reshape(-1,1), y_train.reshape(-1,1))

        reg_model.coef_

        y_predicted = reg_model.predict(x_test.reshape(-1,1))
        y_predicted
        y_test

        reg_model.intercept_

        from sklearn.metrics import mean_squared_error, r2_score

        r_square = r2_score(y_test, y_predicted)
        r_square

        plt.scatter(x = x_test, y = y_test, color = "red")
        plt.scatter(x = x_test, y = y_predicted, color = "green")
        plt.title("Test vs Predicted")
        plt.show()      
        """

def threeB():
    return """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        startups_df=pd.read_csv('./50_Startups.csv')

        startups_df.shape

        startups_df.head()

        startups_df.info()

        startups_df.describe()

        startups_df.duplicated().sum()

        sns.pairplot(data=startups_df)
        plt.show()

        print(startups_df)

        plt.figure(figsize=(19,7))
        sns.boxplot(data=startups_df)
        plt.grid()
        plt.show()

        startups_df=pd.get_dummies(data=startups_df, columns=['State'],drop_first=True, dtype=np.int64)

        startups_df.head()

        from sklearn.preprocessing import StandardScaler

        scaler=StandardScaler()

        startups_df=pd.DataFrame(scaler.fit_transform(startups_df), columns=startups_df.columns)

        startups_df.head()

        startups_df.describe()

        plt.figure(figsize=(19,7))
        sns.boxplot(startups_df)
        plt.grid()
        plt.show()

        startups_df.shape

        Q1=startups_df.quantile(0.25)
        Q3=startups_df.quantile(0.75)
        IQR=Q3-Q1
        print(IQR)

        ul=Q3+1.5*IQR
        ll=Q1-1.5*IQR

        print(ul)
        print(ll)

        startups_df=startups_df[~((startups_df<ll)|(startups_df>ul)).any(axis=1)]

        startups_df.shape

        plt.figure(figsize=(19,7))
        sns.boxplot(startups_df)
        plt.grid()
        plt.show()

        x=startups_df.drop('Profit',axis=1).values
        y=startups_df.loc[:, 'Profit'].values

        from sklearn.model_selection import train_test_split

        x_train,x_test,y_train,y_test,= train_test_split(x,y,test_size=0.2,random_state=1)

        x_train.shape,x_test.shape,y_train.shape,y_test.shape

        from sklearn.linear_model import LinearRegression
        linear_model=LinearRegression()

        linear_model.fit(x_train,y_train)

        linear_model.coef_

        linear_model.intercept_

        linear_model.score(x_train,y_train)

        y_predict=linear_model.predict(x_test)

        y_predict

        from sklearn.metrics import r2_score

        r2_score(y_test, y_predict)

        linear_model.score(x_test,y_test)      
        """

def four():
    return """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        heart_df=pd.read_csv('./Heart.csv')
        
        heart_df.shape

        heart_df.head()

        heart_df.info()

        heart_df.drop('Unnamed: 0',axis=1,inplace=True)

        heart_df.info()

        heart_df.describe()

        sns.countplot(data=heart_df, x='target')
        plt.title("Count Plot for target variable")
        plt.show()

        sns.countplot(data=heart_df, x='target', hue='sex')
        plt.title("Count Plot for target variable w.r.t gender")
        plt.show()

        heart_df.duplicated().sum()

        heart_df.drop_duplicates(inplace=True)

        heart_df.shape

        sns.boxplot(data=heart_df)
        plt.show()

        Q1=heart_df.quantile(0.25)
        Q3=heart_df.quantile(0.75)
        IQR=Q3-Q1
        print(IQR)

        ul=Q3+1.5*IQR
        ll=Q1-1.5*IQR

        heart_df=heart_df[~((heart_df<ll) | (heart_df>ul)).any(axis=1)]

        heart_df.shape

        sns.boxplot(data=heart_df)
        plt.show()

        x=heart_df.drop('target', axis=1)
        y=heart_df['target']

        from sklearn.model_selection import train_test_split

        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()

        x=scaler.fit_transform(x)

        from sklearn.model_selection import train_test_split

        x_train,x_test,y_train,y_test,= train_test_split(x,y,test_size=0.2,random_state=2)

        from sklearn.linear_model import LogisticRegression

        logistic_model=LogisticRegression()

        logistic_model.fit(x_train, y_train)

        logistic_model.score(x_train, y_train)

        logistic_model.score(x_test, y_test)

        y_predict=logistic_model.predict(x_test)

        from sklearn.metrics import confusion_matrix, accuracy_score, recall_score

        confusion_matrix(y_test, y_predict)

        sns.heatmap(confusion_matrix(y_test, y_predict), annot=True, cbar=False,cmap='viridis', annot_kws={"fontsize":18})
        plt.xlabel('PREDICTED VALUE', fontsize=18)
        plt.ylabel('ACTUAL VALUE', fontsize=18)
        plt.show()

        accuracy_score(y_test, y_predict)

        precision_score(y_test, y_predict)
        """

def five():
    return """
        import numpy as np
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

        accuracy_score(y_test,y_predict)
        """