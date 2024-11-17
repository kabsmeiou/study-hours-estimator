# # Problem Description:
# ```
# The objective of this project is to create a machine learning model that predicts the total number of study hours a student may need to prepare for a particular topic or course. Using general features such as target exam score, sleep hours, motivation level, and access to resources, the model will predict the number of studying required and the result will be processed and categorized into predefined categories(e.g., 5-10 hours, 10-15 hours, 15-20 hours, etc.). This is a regression task aimed at helping students plan their study schedules by providing time estimates that align with their individual learning needs, habits, and current circumstances.
# ### About the Dataset:
# ```
# Sourced from: https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
# Provenance: The "Student Performance Factors" dataset is a synthetic dataset generated for educational and analytical purposes. The data is not sourced from any real-world institutions but is created to simulate realistic scenarios for analyzing student performance factors.
# ```

import numpy as np
import pandas as pd

# visuals
import matplotlib.pyplot as plt
import seaborn as sns

# metrics
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.metrics import mean_absolute_error

# for features
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

# model
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

# saving/loading
import pickle

print("PREPARING DATA...")

df = pd.read_csv('../study-dataset/StudentPerformanceFactors.csv')

# # Data Preparation
# column names to lowercase
df.columns = df.columns.str.lower()

cat_variables = df.select_dtypes('object').columns

# make values uniform
for column_name in cat_variables:
    df[column_name] = df[column_name].str.lower().str.replace(' ', '_')


ordinal_order = ['low', 'medium', 'high']
ordinal_data = ['parental_involvement', 'access_to_resources', 'family_income', 'teacher_quality', 'motivation_level']

for cols in ordinal_data:
    df[cols] = pd.Categorical(df[cols], categories=ordinal_order, ordered=True)

# drop the rows containing null values
df.dropna(inplace=True)

y = df['hours_studied'].values

# split data 80 20 (splitting another 20 from 80 later)
df_full_train, df_test, y_full, y_test = train_test_split(df, y, test_size=0.2, random_state=1)

print("REMOVING OUTLIERS...")
# extract the outliers from exam_score(a moderately correlated feature to hours studied)
Q1 = df_full_train['exam_score'].quantile(0.25)
Q3 = df_full_train['exam_score'].quantile(0.75)
IQR = Q3 - Q1
outlier_condition = (df_full_train['exam_score'] < (Q1 - 1.5 * IQR)) | (df_full_train['exam_score'] > (Q3 + 1.5 * IQR))
outliers = df_full_train[outlier_condition]
# handle outlier using median
median_score = df_full_train['exam_score'].median()
df_full_train.loc[outlier_condition, 'exam_score'] = median_score

del df_full_train['hours_studied']
del df_test['hours_studied']
df_train, df_val, y_train, y_val = train_test_split(df_full_train, y_full, test_size=len(df_test), random_state=1)


print("TRAINING XGB MODEL...")
dv = DictVectorizer(sparse=False)
# convert df to dictionary for dictvectorizer
train_dict = df_train.to_dict(orient='records')
val_dict = df_val.to_dict(orient='records')
# fit dv
dv.fit(train_dict)
# perform one hot encoding
X_train = dv.transform(train_dict)
X_val = dv.transform(val_dict)

# train on validation
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_val, label=y_val)

# handling validation from xgb.train
def parse_output(output):
  df_score = []
  s = output.stdout
  for line in s.split('\n')[:-1]: # separate each line
    # print(line)
    n_iter, validation_text = line.split('\t') # separate \t
    n_iter = int(n_iter.strip('[]')) # convert to integer after stripping the brackets
    result = float(validation_text.split(':')[1]) # extract the number
    df_score.append((n_iter, result))
  
  return pd.DataFrame(df_score, columns=["n_iteration", "mae"])

# train the regression model
params = {
    "eval_metric": "mae",              # mae for evaluation
    "learning_rate": 0.3,
    "max_depth": 4,
    "seed": 42
}

model = xgb.train(
    params,
    dtrain,
    num_boost_round=500,
    evals=[(dval, "Validation")],
    early_stopping_rounds=10,
    verbose_eval=10
)

print("FULL TRAINING XGB MODEL...")

test_dict = df_test.to_dict(orient='records')
X_test = dv.transform(test_dict)

full_dict = df_full_train.to_dict(orient='records')
X_full = dv.transform(full_dict)

# train on full
dtrain = xgb.DMatrix(X_full, label=y_full)
dval = xgb.DMatrix(X_test, label=y_test)

params = {
    "eval_metric": "mae",            
    "learning_rate": 0.3,
    "max_depth": 4,
    "seed": 42
}

model = xgb.train(
    params,
    dtrain,
    num_boost_round=500,
    evals=[(dval, "Validation")],
    early_stopping_rounds=10,
    verbose_eval=10
)

# predict
y_pred = model.predict(xgb.DMatrix(X_test))
# assign each prediction to the closest ordinal category
y_pred_cat = np.round(y_pred).astype(int)

# mae
mae = mean_absolute_error(y_test, y_pred)
print("Final Mean Absolute Error:", mae)


from sklearn.metrics import r2_score
# for categorizing the target variable 'hours_studied'
def categorize_hours(hours):
    middle = np.round(hours)
    return (middle-2, middle+2)

predicted_cat = pd.Series(y_pred_cat).apply(categorize_hours)
actual_cat = pd.Series(y_test)
df_result = pd.DataFrame({
    'predictions': y_pred,
    'actual': y_test,
    'predicted_cat': predicted_cat,
    'actual_cat': actual_cat
})

r2 = r2_score(actual_cat, y_pred_cat)
print(f'R-squared(R²) Score: {r2}')

# I decided to make the range of estimation +-2. This would allow for more flexibility when it comes to time management as many other factors may affect the number of hours a student needs for studying. 

# function to check if an actual category falls within a predicted category
def is_within_range(actual, predicted):
    return predicted[0] <= actual <= predicted[1]

# calculate the accuracy
accuracy = df_result.apply(lambda row: is_within_range(row['actual_cat'], row['predicted_cat']), axis=1).mean()
print(f'Accuracy: {accuracy}')

# ### Test on random Sample
test_student = {'attendance': 88,
 'parental_involvement': 'medium',
 'access_to_resources': 'medium',
 'extracurricular_activities': 'yes',
 'sleep_hours': 8,
 'previous_scores': 89,
 'motivation_level': 'medium',
 'internet_access': 'yes',
 'tutoring_sessions': 3,
 'teacher_quality': 'medium',
 'school_type': 'public',
 'peer_influence': 'positive',
 'physical_activity': 3,
 'learning_disabilities': 'no',
 'distance_from_home': 'near',
 'exam_score': 71}

student = dv.transform(test_student)
pd.Series(model.predict(xgb.DMatrix(student)))

# Save Model
output_file=f'study_hestimator.bin'

# f_out = open(output_file, 'wb')
with open(output_file, 'wb') as f_out:
    pickle.dump((model, dv), f_out)

print("Execution Sucess!")