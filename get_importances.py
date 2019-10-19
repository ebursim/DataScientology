import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tpot import TPOTClassifier

match_data = pd.read_csv('filtered_match_data20k.csv')

x = match_data.drop(["Win"], axis=1)
y = match_data["Win"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
tpot = TPOTClassifier(generations=5, population_size=20, verbosity = 2)
tpot.fit(x_train, y_train)
best_model = tpot.fitted_pipeline_.steps[-1][1]
best_model.fit(x, y)
imp = best_model.feature_importances_
imp_order = np.argsort(imp)
for i in range(len(imp_order)):
    print(variable_list[imp_order[i]], imp[imp_order[i]])
