# Machine learning fundamentals Course Coverage

Total lessons: 10

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Supervised Learning Basics

Objective: Understand the core training loop behind many ML systems.

Context:
Supervised Learning Basics sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Supervised learning trains a model from labeled examples: inputs paired with target outputs. Training adjusts parameters to reduce loss on the training set.

Validation data estimates whether the model generalizes beyond examples it memorized. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Supervised learning trains a model from labeled examples: inputs paired with target outputs.
- Training adjusts parameters to reduce loss on the training set.
- Validation data estimates whether the model generalizes beyond examples it memorized.

Quick check: What data split estimates generalization during development?

Concept check: In one sentence, explain how this idea matters in a real AI system: Supervised Learning Basics.


## Lesson 2: Loss, Metrics, and Baselines

Objective: Learn how ML systems decide whether a model is improving.

Context:
Loss, Metrics, and Baselines sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Loss is optimized during training; metrics express performance in business or task terms. Accuracy can hide failures on imbalanced data, so precision, recall, F1, ROC-AUC, or MAE may matter more.

A baseline gives you a simple reference point before adding complexity. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Loss is optimized during training; metrics express performance in business or task terms.
- Accuracy can hide failures on imbalanced data, so precision, recall, F1, ROC-AUC, or MAE may matter more.
- A baseline gives you a simple reference point before adding complexity.

Quick check: What simple reference should you compare a new ML model against?

Concept check: In one sentence, explain how this idea matters in a real AI system: Loss, Metrics, and Baselines.


## Lesson 3: Overfitting and Generalization

Objective: Understand why models can perform well in training and poorly in production.

Context:
Overfitting and Generalization sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Overfitting means the model learns training quirks instead of reusable patterns. Generalization means the model works on new examples from the same real-world process.

Regularization, more data, better splits, simpler models, and early stopping can reduce overfitting. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Overfitting means the model learns training quirks instead of reusable patterns.
- Generalization means the model works on new examples from the same real-world process.
- Regularization, more data, better splits, simpler models, and early stopping can reduce overfitting.

Quick check: What is it called when a model memorizes training quirks?

Concept check: In one sentence, explain how this idea matters in a real AI system: Overfitting and Generalization.


## Lesson 4: Data Leakage and Dataset Quality

Objective: Learn one of the most common causes of misleading ML results.

Context:
Data Leakage and Dataset Quality sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Data leakage occurs when training data includes information that would not be available at prediction time. Duplicates, bad labels, time leakage, target leakage, and biased sampling can ruin evaluation.

Dataset quality often matters more than model complexity. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Data leakage occurs when training data includes information that would not be available at prediction time.
- Duplicates, bad labels, time leakage, target leakage, and biased sampling can ruin evaluation.
- Dataset quality often matters more than model complexity.

Quick check: What is it called when training uses information unavailable at prediction time?

Concept check: In one sentence, explain how this idea matters in a real AI system: Data Leakage and Dataset Quality.


## Lesson 5: Mathematical foundations for ML

Objective: Cover the minimum math needed to read ML and AI engineering explanations confidently.

Context:
Mathematical foundations for ML sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Vectors, matrices, dot products, and matrix multiplication are the language of model computations. Derivatives, gradients, and the chain rule explain how models learn from loss.

Probability and Bayes' theorem describe uncertainty and conditional reasoning. Mean, variance, standard deviation, correlation, entropy, cross-entropy, and KL divergence show up in training and evaluation. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Vectors, matrices, dot products, and matrix multiplication are the language of model computations.
- Derivatives, gradients, and the chain rule explain how models learn from loss.
- Probability and Bayes' theorem describe uncertainty and conditional reasoning.
- Mean, variance, standard deviation, correlation, entropy, cross-entropy, and KL divergence show up in training and evaluation.

Quick check: What quantity tells gradient descent which way to change parameters?

Concept check: In one sentence, explain how this idea matters in a real AI system: Mathematical foundations for ML.


## Lesson 6: Core ML concepts and data splits

Objective: Understand the basic training loop before choosing a model family.

Context:
Core ML concepts and data splits sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Supervised learning uses labeled examples; unsupervised learning looks for structure without labels. Reinforcement learning learns from rewards and feedback rather than fixed labels.

Training data, loss functions, optimizers, and learning rate form the core learning loop. Train/validation/test splits, cross-validation, and the bias-variance tradeoff protect against misleading metrics. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Supervised learning uses labeled examples; unsupervised learning looks for structure without labels.
- Reinforcement learning learns from rewards and feedback rather than fixed labels.
- Training data, loss functions, optimizers, and learning rate form the core learning loop.
- Train/validation/test splits, cross-validation, and the bias-variance tradeoff protect against misleading metrics.

Quick check: Which split should stay untouched until the end?

Concept check: In one sentence, explain how this idea matters in a real AI system: Core ML concepts and data splits.


## Lesson 7: Classical supervised learning

Objective: Learn the algorithm families that still matter in real ML systems.

Context:
Classical supervised learning sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Linear regression predicts continuous values, often with MSE as the training objective. Logistic regression maps features to class probabilities with a sigmoid decision boundary.

Decision trees, random forests, and boosting methods capture nonlinear structure in tabular data. SVMs, k-nearest neighbors, and naive Bayes are still useful baselines and teaching tools. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Linear regression predicts continuous values, often with MSE as the training objective.
- Logistic regression maps features to class probabilities with a sigmoid decision boundary.
- Decision trees, random forests, and boosting methods capture nonlinear structure in tabular data.
- SVMs, k-nearest neighbors, and naive Bayes are still useful baselines and teaching tools.

Quick check: Which algorithm is a common tabular baseline for classification?

Concept check: In one sentence, explain how this idea matters in a real AI system: Classical supervised learning.


## Lesson 8: Unsupervised learning and anomaly detection

Objective: See how clustering, dimensionality reduction, and outlier detection fit into AI workflows.

Context:
Unsupervised learning and anomaly detection sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

K-means and DBSCAN group similar examples without labels. PCA, t-SNE, and UMAP reduce dimensionality or reveal structure in high-dimensional data.

Isolation forests and statistical methods help flag anomalies and unusual points. Unsupervised methods are useful when labels are missing or the goal is exploration. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- K-means and DBSCAN group similar examples without labels.
- PCA, t-SNE, and UMAP reduce dimensionality or reveal structure in high-dimensional data.
- Isolation forests and statistical methods help flag anomalies and unusual points.
- Unsupervised methods are useful when labels are missing or the goal is exploration.

Quick check: Which algorithm is commonly used for clustering?

Concept check: In one sentence, explain how this idea matters in a real AI system: Unsupervised learning and anomaly detection.


## Lesson 9: Evaluation metrics and model selection

Objective: Choose metrics that actually match the problem and business goal.

Context:
Evaluation metrics and model selection sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Classification metrics include accuracy, precision, recall, F1, confusion matrix, ROC-AUC, and PR curves. Regression metrics include MSE, RMSE, MAE, and R^2.

Class imbalance often requires oversampling, undersampling, SMOTE, or weighted loss. Comparing models should include confidence intervals or significance checks when decisions matter. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Classification metrics include accuracy, precision, recall, F1, confusion matrix, ROC-AUC, and PR curves.
- Regression metrics include MSE, RMSE, MAE, and R^2.
- Class imbalance often requires oversampling, undersampling, SMOTE, or weighted loss.
- Comparing models should include confidence intervals or significance checks when decisions matter.

Quick check: Which metric is usually best for imbalanced binary classification?

Concept check: In one sentence, explain how this idea matters in a real AI system: Evaluation metrics and model selection.


## Lesson 10: Feature engineering and preprocessing

Objective: Prepare data so simple models and deep models both get a fair shot.

Context:
Feature engineering and preprocessing sits inside Machine learning fundamentals. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Normalization, standardization, and scaling make numeric features comparable. Categorical variables often need one-hot, label, or target encoding.

Missing data can be handled with imputation, deletion, or model-aware strategies. TF-IDF, bag-of-words, and EDA remain useful baselines before jumping to embeddings. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Normalization, standardization, and scaling make numeric features comparable.
- Categorical variables often need one-hot, label, or target encoding.
- Missing data can be handled with imputation, deletion, or model-aware strategies.
- TF-IDF, bag-of-words, and EDA remain useful baselines before jumping to embeddings.

Quick check: What is one common way to encode categorical variables?

Concept check: In one sentence, explain how this idea matters in a real AI system: Feature engineering and preprocessing.
