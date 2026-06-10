# Machine learning fundamentals Course Coverage

Total lessons: 10

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Supervised Learning Basics

Objective: Understand the core training loop behind many ML systems.

Concepts taught:
- Supervised learning trains a model from labeled examples: inputs paired with target outputs.
- Training adjusts parameters to reduce loss on the training set.
- Validation data estimates whether the model generalizes beyond examples it memorized.

Practice: Define a toy spam classifier dataset with input text, label, train split, validation split, and metric.

Quick check: What data split estimates generalization during development?

## Lesson 2: Loss, Metrics, and Baselines

Objective: Learn how ML systems decide whether a model is improving.

Concepts taught:
- Loss is optimized during training; metrics express performance in business or task terms.
- Accuracy can hide failures on imbalanced data, so precision, recall, F1, ROC-AUC, or MAE may matter more.
- A baseline gives you a simple reference point before adding complexity.

Practice: Pick metrics for spam detection, fraud detection, price prediction, and support-ticket routing.

Quick check: What simple reference should you compare a new ML model against?

## Lesson 3: Overfitting and Generalization

Objective: Understand why models can perform well in training and poorly in production.

Concepts taught:
- Overfitting means the model learns training quirks instead of reusable patterns.
- Generalization means the model works on new examples from the same real-world process.
- Regularization, more data, better splits, simpler models, and early stopping can reduce overfitting.

Practice: Sketch symptoms of overfitting by comparing training loss, validation loss, and test performance.

Quick check: What is it called when a model memorizes training quirks?

## Lesson 4: Data Leakage and Dataset Quality

Objective: Learn one of the most common causes of misleading ML results.

Concepts taught:
- Data leakage occurs when training data includes information that would not be available at prediction time.
- Duplicates, bad labels, time leakage, target leakage, and biased sampling can ruin evaluation.
- Dataset quality often matters more than model complexity.

Practice: Review a hypothetical churn dataset and identify fields that might leak future information.

Quick check: What is it called when training uses information unavailable at prediction time?

## Lesson 5: Mathematical foundations for ML

Objective: Cover the minimum math needed to read ML and AI engineering explanations confidently.

Concepts taught:
- Vectors, matrices, dot products, and matrix multiplication are the language of model computations.
- Derivatives, gradients, and the chain rule explain how models learn from loss.
- Probability and Bayes' theorem describe uncertainty and conditional reasoning.
- Mean, variance, standard deviation, correlation, entropy, cross-entropy, and KL divergence show up in training and evaluation.

Example:
```text
x = [1, 2, 3]
w = [0.2, 0.5, 0.3]
score = dot(x, w)
grad = d_loss_d_w(score, target)
```

Practice: Connect one math idea to a concrete ML use case such as loss gradients or similarity search.

Quick check: What quantity tells gradient descent which way to change parameters?

## Lesson 6: Core ML concepts and data splits

Objective: Understand the basic training loop before choosing a model family.

Concepts taught:
- Supervised learning uses labeled examples; unsupervised learning looks for structure without labels.
- Reinforcement learning learns from rewards and feedback rather than fixed labels.
- Training data, loss functions, optimizers, and learning rate form the core learning loop.
- Train/validation/test splits, cross-validation, and the bias-variance tradeoff protect against misleading metrics.

Example:
```text
train, val, test = split(data, 0.7, 0.15, 0.15)
model.fit(train.X, train.y)
print(metric(model, val))
```

Practice: Describe how you would split a small dataset and why the test set stays untouched.

Quick check: Which split should stay untouched until the end?

## Lesson 7: Classical supervised learning

Objective: Learn the algorithm families that still matter in real ML systems.

Concepts taught:
- Linear regression predicts continuous values, often with MSE as the training objective.
- Logistic regression maps features to class probabilities with a sigmoid decision boundary.
- Decision trees, random forests, and boosting methods capture nonlinear structure in tabular data.
- SVMs, k-nearest neighbors, and naive Bayes are still useful baselines and teaching tools.

Example:
```text
y_reg = linear_regression(X)
y_cls = logistic_regression(X)
tree = decision_tree.fit(X, y)
```

Practice: Pick one classical algorithm for regression, one for classification, and one for text.

Quick check: Which algorithm is a common tabular baseline for classification?

## Lesson 8: Unsupervised learning and anomaly detection

Objective: See how clustering, dimensionality reduction, and outlier detection fit into AI workflows.

Concepts taught:
- K-means and DBSCAN group similar examples without labels.
- PCA, t-SNE, and UMAP reduce dimensionality or reveal structure in high-dimensional data.
- Isolation forests and statistical methods help flag anomalies and unusual points.
- Unsupervised methods are useful when labels are missing or the goal is exploration.

Example:
```text
clusters = kmeans(X, k=4)
low_dim = PCA(2).fit_transform(X)
outliers = isolation_forest(X)
```

Practice: Choose an unsupervised method for clustering users, compressing embeddings, and finding outliers.

Quick check: Which algorithm is commonly used for clustering?

## Lesson 9: Evaluation metrics and model selection

Objective: Choose metrics that actually match the problem and business goal.

Concepts taught:
- Classification metrics include accuracy, precision, recall, F1, confusion matrix, ROC-AUC, and PR curves.
- Regression metrics include MSE, RMSE, MAE, and R^2.
- Class imbalance often requires oversampling, undersampling, SMOTE, or weighted loss.
- Comparing models should include confidence intervals or significance checks when decisions matter.

Example:
```text
precision = tp / (tp + fp)
recall = tp / (tp + fn)
rmse = sqrt(mse(y, yhat))
```

Practice: Pick the right metric for spam filtering, churn, and price prediction.

Quick check: Which metric is usually best for imbalanced binary classification?

## Lesson 10: Feature engineering and preprocessing

Objective: Prepare data so simple models and deep models both get a fair shot.

Concepts taught:
- Normalization, standardization, and scaling make numeric features comparable.
- Categorical variables often need one-hot, label, or target encoding.
- Missing data can be handled with imputation, deletion, or model-aware strategies.
- TF-IDF, bag-of-words, and EDA remain useful baselines before jumping to embeddings.

Example:
```text
X = standardize(X_num)
X = one_hot(X_cat)
X = impute_missing(X)
```

Practice: Show how you would clean a mixed numeric/categorical dataset before training.

Quick check: What is one common way to encode categorical variables?
