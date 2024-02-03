import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, auc, precision_recall_curve
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

def evaluate(y_true, y_pred, y_prob, model_name):
    """
    Function to evaluate and print the model performance.
    """
    # # Print model name
    # print(f"Model: {model_name}")

    # # Confusion Matrix
    # print("Confusion Matrix:")
    # print(confusion_matrix(y_true, y_pred))

    # # Classification Report
    # print("Classification Report:")
    # print(classification_report(y_true, y_pred))

    # # AUC Score - Check if probability predictions are available
    # if y_prob is not None:
    #     print("AUC Score:", roc_auc_score(y_true, y_prob))
    # print("\n")

    metrics = {}

    # Store model name
    metrics['model_name'] = model_name

    # Confusion Matrix
    # metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred)

    # Classification Report
    metrics['classification_report'] = classification_report(y_true, y_pred, output_dict=True)

    # report = f"Model: {model_name}\n"

    # # Classification Report
    # report += "Classification Report:\n"
    # report += classification_report(y_true, y_pred)

    # AUC Score - Check if probability predictions are available
    if y_prob is not None:
        metrics['auc_score'] = roc_auc_score(y_true, y_prob)

    return metrics
    # return report

# Plot ROC curves for all applicable models
def plot_roc(model, X_test, y_test, label):
    y_score = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, lw=2, label=f'{label} (AUC = {roc_auc:.2f})')

# Function to plot Precision-Recall Curve
def plot_precision_recall_curve(model, X_test, y_test, model_name):
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
        precision, recall, _ = precision_recall_curve(y_test, y_prob)

        plt.plot(recall, precision, label=f'{model_name}')


def run_algorithm():       
    # Getting data
    data = load_breast_cancer()
    X = data.data
    y = data.target

    result = {}

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    df = pd.DataFrame(data=np.c_[X, y], columns=np.append(data.feature_names, ["target"]))
    print(df.head())

    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)


    # Logistic Regression

    lr_model = LogisticRegression(max_iter=1000, solver='saga')
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    y_prob_lr = lr_model.predict_proba(X_test)[:, 1]

    # Evaluation
    result['Logistic Regression'] = evaluate(y_test, y_pred_lr, y_prob_lr, "Logistic Regression")

    result_test = result['Logistic Regression']
    # Train K-Nearest Neighbors
    knn_model = KNeighborsClassifier()
    knn_model.fit(X_train, y_train)
    y_pred_knn = knn_model.predict(X_test)
    y_prob_knn = knn_model.predict_proba(X_test)[:,1]

    # Evaluate K-Nearest Neighbors
    result['K-Nearest Neighbors'] = evaluate(y_test, y_pred_knn, y_prob_knn, "K-Nearest Neighbors")


    # Train Support Vector Machine
    svm_model = SVC(probability=True)
    svm_model.fit(X_train, y_train)
    y_pred_svm = svm_model.predict(X_test)
    y_prob_svm = svm_model.predict_proba(X_test)[:, 1]

    # Evaluate Support Vector Machine
    result['Support Vector Machine'] = evaluate(y_test, y_pred_svm, y_prob_svm, "Support Vector Machine")



    dt_model = DecisionTreeClassifier()
    dt_model.fit(X_train, y_train)
    y_pred_dt = dt_model.predict(X_test)
    y_prob_dt = dt_model.predict_proba(X_test)[:,1]

    result['Decision Tree'] = evaluate(y_test, y_pred_dt, y_prob_dt, "Decision Tree")


    # Train Random Forest
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

    # Evaluate Random Forest
    result['Random Forest'] = evaluate(y_test, y_pred_rf, y_prob_rf, "Random Forest")


    # Train Gradient Boosting
    gb_model = GradientBoostingClassifier()
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    y_prob_gb = gb_model.predict_proba(X_test)[:, 1]

    # Evaluate Gradient Boosting
    result['Gradient Boosting'] = evaluate(y_test, y_pred_gb, y_prob_gb, "Gradient Boosting")



    nb_model = GaussianNB()
    nb_model.fit(X_train, y_train)
    y_pred_nb = nb_model.predict(X_test)
    y_prob_nb = nb_model.predict_proba(X_test)[:,1]

    result['Naive Bayes'] = evaluate(y_test, y_pred_nb, y_prob_nb, "Naive Bayes")


    # Train Neural Network
    nn_model = MLPClassifier(max_iter=1000)
    nn_model.fit(X_train, y_train)
    y_pred_nn = nn_model.predict(X_test)

    # Evaluate Neural Network
    result['Neural Network'] = evaluate(y_test, y_pred_nn, None, "Neural Network (MLP Classifier)")


    # Train AdaBoost
    ab_model = AdaBoostClassifier()
    ab_model.fit(X_train, y_train)
    y_pred_ab = ab_model.predict(X_test)
    y_prob_ab = ab_model.predict_proba(X_test)[:, 1]

    # Evaluate AdaBoost
    result['AdaBoost'] = evaluate(y_test, y_pred_ab, y_prob_ab, "AdaBoost")


    # Train XGBoost
    xg_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    xg_model.fit(X_train, y_train)
    y_pred_xg = xg_model.predict(X_test)
    y_prob_xg = xg_model.predict_proba(X_test)[:, 1]

    # Evaluate XGBoost
    result['XGBoost'] = evaluate(y_test, y_pred_xg, y_prob_xg, "XGBoost")


    # Create a figure for ROC curves
    plt.figure(figsize=(10, 8))



    plot_roc(lr_model, X_test, y_test, 'Logistic Regression')
    plot_roc(svm_model, X_test, y_test, 'SVM')
    # plot_roc(rf_model, X_test, y_test, 'Random Forest')
    # plot_roc(gb_model, X_test, y_test, 'Gradient Boosting')
    # plot_roc(ab_model, X_test, y_test, 'AdaBoost')
    # plot_roc(xg_model, X_test, y_test, 'XGBoost')
    # plot_roc(knn_model, X_test, y_test, 'KNN')
    # plot_roc(dt_model, X_test, y_test, 'Decision Tree')
    # plot_roc(nb_model, X_test, y_test, 'Naive Bayes')
    # plot_roc(nn_model, X_test, y_test, 'Neural Network (MLP Classifier)')

    # Plot the diagonal line (random guessing)
    plt.plot([0, 1], [0, 1], 'k--')

    # Set labels and title
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves')

    # Add legends for each model
    plt.legend(loc="lower right")

    # plt.show() # TODO: download
    plt.savefig('first_graph.png')
    plt.close()

    # Plotting Precision-Recall Curves for all applicable models

    # plt.figure(figsize=(10, 8))
    # plot_precision_recall_curve(lr_model, X_test, y_test, 'Logistic Regression')
    # plot_precision_recall_curve(svm_model, X_test, y_test, 'SVM')
    # plot_precision_recall_curve(rf_model, X_test, y_test, 'Random Forest')
    # plot_precision_recall_curve(gb_model, X_test, y_test, 'Gradient Boosting')
    # plot_precision_recall_curve(ab_model, X_test, y_test, 'AdaBoost')
    # plot_precision_recall_curve(xg_model, X_test, y_test, 'XGBoost')
    # # plot_precision_recall_curve(knn_model, X_test, y_test, 'KNN')
    # plot_precision_recall_curve(dt_model, X_test, y_test, 'Decision Tree')
    # plot_precision_recall_curve(nb_model, X_test, y_test, 'Naive Bayes')
    # plot_precision_recall_curve(nn_model, X_test, y_test, 'Neural Network (MLP Classifier)')

    # plt.xlabel('Recall')
    # plt.ylabel('Precision')
    # plt.title('Precision-Recall Curves')
    # plt.legend(loc="lower left")
    # # plt.show() # TODO: download
    # plt.savefig('second_graph.png')
    # plt.close()
    # print("result", result)
    return result_test

# run the algorithm
# run_algorithm()