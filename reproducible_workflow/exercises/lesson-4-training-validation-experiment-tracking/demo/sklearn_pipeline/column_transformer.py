import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


# Example dataframe from the sklearn docs
df = pd.DataFrame(
    {'city': ['London', 'London', 'Paris', 'Sallisaw'],
     'title': ["His Last Bow", "How Watson Learned the Trick",
               "A Moveable Feast", "The Grapes of Wrath"],
     'expert_rating': [5, 3, 4, 5],
     'user_rating': [4, 5, 4, 3],
     'click': ['yes', 'no', 'no', 'yes']})
y = df.pop("click")
X = df

# Build a Column transformer
categorical_preproc = OneHotEncoder()  # categorical columns pipeline
text_preproc = TfidfVectorizer()  # NLP tool tranforming text in a usable vector (using TF-IDF)
# SimpleImputer handle missing values,
numerical_preprocessing = make_pipeline(SimpleImputer(), StandardScaler())  # numerical columns pipeline
preproc = ColumnTransformer(
    transformers=[
        ("cat_transform", categorical_preproc, ['city']), # can use list here as OneHotEncoder handles 2 dim inputs
        ("text_transform", text_preproc, 'title'),  # not a list because TfidfVectorizer accepts only 1 dim inputs
        ("num_transform", numerical_preprocessing, ['expert_rating', 'user_rating'])
    ],
    remainder='drop'  # means that all the other columns are dropped
)
# Inference pipeline
pipe = make_pipeline(preproc, LogisticRegression())
pipe.fit(X, y)
