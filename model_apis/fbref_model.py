import os
import pandas as pd
import soccerdata as sd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

class Predict():
    def __init__(self) -> None:
        self.model = None

    def load_data(self, path) -> pd.DataFrame :
        if os.path.exists(path):
            stats_pd_data = pd.read_csv(path)
            print(f"Read data from {path}")
        else:
            sd.FBref.available_leagues()

            # MUST RUN BEFORE CREATING NEW DATA FILE
            fbref = sd.FBref(leagues="ENG-Premier League", seasons=['18-19','19-20','20-21','21-22','22-23']) # expected performance stats missing before 2018
            # print(fbref.__doc__)

            ### Get data
            stats_pd = fbref.read_player_season_stats(stat_type='standard')

            ### Convert data types
            cols = list(stats_pd.columns)
            for col in cols:
                if col in [('nation', ''),('pos', ''),('born', '')]:
                    stats_pd[col] = stats_pd[col].astype(str)
                else:
                    stats_pd[col] = stats_pd[col].apply(pd.to_numeric)
            print(stats_pd.info())

            stats_pd_data = stats_pd.drop(columns=[('nation', ''),('pos', ''),('born', '')])
            stats_pd_data.fillna(value=0, inplace=True)

            stats_pd_data.to_csv(path)
            print(f"Successfully created and loaded data to {path}")

        return stats_pd_data

    def preprocess(self, df) -> str:
        ### Data processing
        # create subsets with players that played more than half the season
        df = df[df['Playing Time']['90s'] > 19]

        # Group data by player
        player_groups = self.df.groupby('player')

        # Transform data columns to arrays
        expected_ga = player_groups.mean()['Expected']['npxG+xAG'].to_numpy()
        actual_ga = player_groups.mean()['Performance']['G+A'].to_numpy()

        # Split the data into training/testing sets
        x_train = expected_ga[:-20].reshape(-1, 1)
        x_test = expected_ga[-20:].reshape(-1, 1)

        # Split the targets into training/testing sets
        y_train = actual_ga[:-20]
        y_test = actual_ga[-20:]

        return x_train, y_train, x_test, y_test

    def linear_regression(self, x_train, y_train, x_test, y_test) -> None:
        ## Linear regression
        # Create linear regression object
        reg = linear_model.LinearRegression()

        # Train the model using the training sets
        reg.fit(x_train,y_train)

        # Make predictions using the testing set
        y_pred = reg.predict(x_test)

        # The coefficients
        print("\nCoefficients: ", reg.coef_)
        # The mean squared error
        print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
        # The coefficient of determination: 1 is perfect prediction
        print("R squared: %.2f" % r2_score(y_test, y_pred))

        #Create plot area
        fig, ax = plt.subplots()

        ax.set_title("Predicted Goal Contributions")
        ax.set_ylabel("Actual Goal Contributions")
        ax.set_xlabel("Expected Goal Contributions")

        # Plot outputs
        plt.scatter(x_test, y_test, color="black")
        plt.plot(x_test, y_pred, color="blue", linewidth=3)

        plt.show()

    def predict(self, df, model):
        x_train, y_train, x_test, y_test = self.preprocess(df)
        if self.model == 'Linear Regression':
            self.linear_regression(x_train, y_train, x_test, y_test)