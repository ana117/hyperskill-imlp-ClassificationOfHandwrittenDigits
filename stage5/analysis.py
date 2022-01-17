import tensorflow as tf
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import Normalizer

# models
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

# load MNIST dataset
(features, target), *_ = tf.keras.datasets.mnist.load_data()

# reshape to total_image x total_pixel
total_pixels = features.shape[1] * features.shape[2]
features = features.reshape(features.shape[0], total_pixels)

# split into train and test sets
NUM_OF_ROWS = 6000
TEST_SIZE = 0.3
RAND_SEED = 40
X_train, X_test, y_train, y_test = train_test_split(features[:NUM_OF_ROWS],
                                                    target[:NUM_OF_ROWS],
                                                    test_size=TEST_SIZE,
                                                    random_state=RAND_SEED)

# normalize data
transformer = Normalizer()
X_train_norm = transformer.transform(X_train)
X_test_norm = transformer.transform(X_test)


def fit_predict_eval(model, features_train, features_test, target_train, target_test):
    model.fit(features_train, target_train)
    prediction = model.predict(features_test)
    score = accuracy_score(target_test, prediction)
    print(f'best estimator: {model}\naccuracy: {score:.3f}\n')


# using KNN and RandomForest (best algorithm in stage 4)
# with normalized data (better accuracy in stage 4)

# K-NearestNeighbours
knn_params = {"n_neighbors": [3, 4],
              "weights": ['uniform', 'distance'],
              "algorithm": ['auto', 'brute']}
knn_gs = GridSearchCV(estimator=KNeighborsClassifier(),
                      param_grid=knn_params,
                      scoring="accuracy",
                      n_jobs=-1)
knn_gs.fit(X_train_norm, y_train)

print("K-nearest neighbours algorithm")
fit_predict_eval(model=knn_gs.best_estimator_,
                 features_train=X_train_norm,
                 features_test=X_test_norm,
                 target_train=y_train,
                 target_test=y_test)


# RandomForestClassifier
rfc_params = {"n_estimators": [300, 500],
              "max_features": ['auto', 'log2'],
              "class_weight": ['balanced', 'balanced_subsample']}
rfc_gs = GridSearchCV(estimator=RandomForestClassifier(random_state=RAND_SEED),
                      param_grid=rfc_params,
                      scoring="accuracy",
                      n_jobs=-1)
rfc_gs.fit(X_train_norm, y_train)

print("Random forest algorithm")
fit_predict_eval(model=rfc_gs.best_estimator_,
                 features_train=X_train_norm,
                 features_test=X_test_norm,
                 target_train=y_train,
                 target_test=y_test)
