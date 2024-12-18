from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score, precision_score, recall_score, f1_score
import numpy as np

def display_metrics(actual, predicted):
    if np.issubdtype(actual.dtype, np.floating) or np.issubdtype(predicted.dtype, np.floating):
        R2_score = r2_score(actual, predicted)
        MAE = mean_absolute_error(actual, predicted)
        MSE = mean_squared_error(actual, predicted)
        RMSE = np.sqrt(MSE)
        print(f"RMSE: {RMSE}")
        print(f"MAE: {MAE}")
        print(f"MSE: {MSE}")
        print(f"R² Score: {R2_score}")
    else:
        Accuracy = accuracy_score(actual, predicted)
        Precision = precision_score(actual, predicted)
        Recall = recall_score(actual, predicted)
        F1 = f1_score(actual, predicted)
        print(f"Accuracy: {Accuracy}")
        print(f"Precision: {Precision}")
        print(f"Recall: {Recall}")
        print(f"F1 Score: {F1}")
