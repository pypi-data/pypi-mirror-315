def program_1():
    return """
    Implement simple linear regression using a python program and estimate
    statistical quantities from training data.

    Python Code:

    import matplotlib.pyplot as plt
    import numpy as np
    from math import sqrt

    # Calculate root mean squared error
    def rmse_metric(actual, predicted):
        sum_error = 0.0
        for i in range(len(actual)):
            prediction_error = predicted[i] - actual[i]
            sum_error += (prediction_error**2)
        mean_error = sum_error / float(len(actual))
        return sqrt(mean_error)

    ...

    Output:

    x stats: Mean = 3.000 Variance = 2.000
    y stats: Mean = 2.800 Variance = 1.760
    Covariance : 1.600
    RMSE: 0.693
    Coefficients: B0 = 0.400, B1 = 0.800
    """

def program_2():
    return """
    Implement and demonstrate the FIND-S algorithm for finding the most specific
    hypothesis based on a given set of training data samples. Read the training data
    from a .CSV file.

    Python Code:

    import pandas as pd
    import numpy as np

    # to read the data in the csv file
    data = pd.read_csv("C:/Users/ISE14/Documents/CSV_AIML/P2Data.csv")
    print(data)

    # making an array of all the attributes
    d = np.array(data)[:, :-1]
    print("The attributes are: \n", d)

    # segregating the target that has positive and negative examples
    target = np.array(data)[:, -1]
    print("The target is: ", target)

    # training function to implement find-s algorithm
    def train(c, t):
        for i, val in enumerate(t):
            if val == "Yes":
                specific_hypothesis = c[i].copy()
                break
        for i, val in enumerate(c):
            if t[i] == "Yes":
                for x in range(len(specific_hypothesis)):
                    if val[x] != specific_hypothesis[x]:
                        specific_hypothesis[x] = "?"
                    else:
                        pass
        return specific_hypothesis

    # obtaining the final hypothesis
    print("The final hypothesis is:", train(d, target))

    Output:

    The attributes are:
    [['Morning' 'Sunny' 'Warm' 'Yes' 'Mild' 'Strong']
     ['Evening' 'Rainy' 'Cold' 'No' 'Mild' 'Normal']
     ['Morning' 'Sunny' 'Moderate' 'Yes' 'Normal' 'Normal']
     ['Evening' 'Sunny' 'Cold' 'Yes' 'High' 'Strong']]
    The target is:  ['Yes' 'No' 'Yes' 'Yes']
    The final hypothesis is: ['?' 'Sunny' '?' 'Yes' '?' '?']
    """

def program_3():
    return """
    For a given set of training data examples stored in a .CSV file, implement and
    demonstrate the Candidate-Elimination algorithm to output a description of the
    set of all hypotheses consistent with the training examples.

    Python Code:

    import numpy as np
    import pandas as pd

    data = pd.read_csv('C:/Users/ISE-LAB7/Documents/P3Data.csv')
    print(data)
    concepts = np.array(data.iloc[:, 0:-1])
    print(concepts)
    target = np.array(data.iloc[:, -1])
    print(target)

    # Candidate Elimination algorithm
    def learn(concepts, target):
        specific_h = concepts[0].copy()
        print("\nInitialization of specific_h and general_h")
        print("\nSpecific hypothesis: ", specific_h)
        general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
        print("\nGeneric hypothesis: ", general_h)
        for i, h in enumerate(concepts):
            print("\nInstance", i + 1, "is ", h)
            if target[i] == "Yes":
                print("Instance is Positive ")
                for x in range(len(specific_h)):
                    if h[x] != specific_h[x]:
                        specific_h[x] = '?'
                        general_h[x][x] = '?'
            if target[i] == "No":
                print("Instance is Negative ")
                for x in range(len(specific_h)):
                    if h[x] != specific_h[x]:
                        general_h[x][x] = specific_h[x]
                    else:
                        general_h[x][x] = '?'
            print("Specific hypothesis after ", i + 1, "Instance is ", specific_h)
            print("Generic hypothesis after ", i + 1, "Instance is ", general_h)
            print("\n")
        indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
        for i in indices:
            general_h.remove(["?", "?", "?", "?", "?", "?"])
        return specific_h, general_h

    s_final, g_final = learn(concepts, target)
    print("Final Specific_h: ", s_final, sep="\n")
    print("Final General_h: ", g_final, sep="\n")

    Output:

    Final Specific_h:  ['Sunny' 'Warm' '?' 'Strong' '?' '?']
    Final General_h:  [['Sunny', '?', '?', '?', '?', '?'], ['?', 'Warm', '?', '?', '?', '?']]
    """

def program_4():
    return """
    Demonstrate the working of the decision tree based ID3 algorithm. Use an
    appropriate data set for building the decision tree and apply this knowledge to
    classify a new sample.

    Python Code:

    import pandas as pd
    from pandas import DataFrame

    df_tennis = pd.read_csv('C:/Users/Lochan/OneDrive/Documents/P4Data.csv')
    print(df_tennis)

    ...

    Output:

    Total Entropy of PlayTennis Data Set: 0.940
    Info-gain for Outlook is : 0.247

    The Resultant Decision Tree is :
    {'Outlook': {'Overcast': 'Yes', 'Rainy': {'Windy': {'Strong': 'No', 'Weak': 'Yes'}}, 'Sunny': {'Humidity': {'High': 'No', 'Normal': 'Yes'}}}}
    Accuracy is : 0.75
    """

def program_5():
    return """
    Develop a program to implement K-Nearest Neighbor algorithm to classify the
    iris data set. Print both correct and wrong predictions.

    Python Code:

    import numpy as np
    import pandas as pd
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    from sklearn import metrics

    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
    dataset = pd.read_csv("C:/Users/65/Documents/P5Data.csv")
    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]
    print(X.head())
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.10)
    classifier = KNeighborsClassifier(n_neighbors=5).fit(Xtrain, ytrain)
    ypred = classifier.predict(Xtest)

    print("\n-------------------------------------------------------------------------")
    print ('%-25s %-25s %-25s' % ('Original Label', 'Predicted Label', 'Correct/Wrong'))
    print ("-------------------------------------------------------------------------")
    for i, label in enumerate(ytest):
        print ('%-25s %-25s' % (label, ypred[i]), end="")
        if (label == ypred[i]):
            print (' %-25s' % ('Correct'))
        else:
            print (' %-25s' % ('Wrong'))

    print("-------------------------------------------------------------------------")
    print("\nConfusion Matrix:\n", metrics.confusion_matrix(ytest, ypred))
    print("Classification Report:\n", metrics.classification_report(ytest, ypred))
    print('Accuracy of the classifier is %0.2f' % metrics.accuracy_score(ytest, ypred))

    Output:

    Confusion Matrix:
    [[6 0 0]
     [0 2 0]
     [0 1 6]]
    Classification Report:
    Accuracy of the classifier is 0.93
    """

def program_6():
    return """
    Develop a program to construct a Bayesian network considering medical data.
    Use this model to demonstrate the diagnosis of heart patients using standard Heart
    Disease Data Set.

    Python Code:

    import numpy as np
    import pandas as pd
    from pgmpy.models import BayesianModel
    from pgmpy.estimators import MaximumLikelihoodEstimator
    from pgmpy.inference import VariableElimination

    heartDisease = pd.read_csv("C:/Users/Lochan/OneDrive/Documents/P6Data.csv")
    heartDisease = heartDisease.replace('?', np.nan)
    print('Few examples from the dataset are given below')
    print(heartDisease.head())

    model = BayesianModel([('age', 'HeartDisease'), ('gender', 'HeartDisease'),
                           ('exang', 'HeartDisease'), ('cp', 'HeartDisease'),
                           ('HeartDisease', 'restecg'), ('HeartDisease', 'chol')])
    model.fit(heartDisease, estimator=MaximumLikelihoodEstimator)

    print('Inferencing with Bayesian Network:')
    infer = VariableElimination(model)
    print('Probability of HeartDisease given evidence= restecg')
    print(infer.query(variables=['HeartDisease'], evidence={'restecg': 0}))

    Output:

    Few examples from the dataset are given below
    Probability of HeartDisease given evidence= restecg
    """

def program_7():
    return """
    For the given table, write a python program to perform K-Means Clustering.

    Python Code:

    from sklearn.cluster import KMeans
    import numpy as np
    import matplotlib.pyplot as plt

    x1 = np.array([3, 1, 1, 2, 1, 6, 6, 6, 5, 6, 7, 8, 9, 8, 9, 9, 8])
    x2 = np.array([5, 4, 6, 6, 5, 8, 6, 7, 6, 7, 1, 2, 1, 2, 3, 2, 3])

    plt.scatter(x1, x2)
    plt.title('Dataset')
    plt.show()

    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
    kmeans_model = KMeans(n_clusters=3).fit(X)
    plt.scatter(x1, x2, c=kmeans_model.labels_, cmap='viridis')
    plt.title('K-Means Clustering')
    plt.show()

    Output:

    Dataset Visualization and K-Means Clustering
    """

def program_8():
    return """
    Apply EM algorithm to cluster a set of data stored in a .CSV file. Use the same
    dataset for clustering using k-Means algorithm. Compare the results of these two
    algorithms and comment on the quality of clustering.

    Python Code:

    from sklearn.cluster import KMeans
    from sklearn.mixture import GaussianMixture
    import pandas as pd
    import matplotlib.pyplot as plt

    dataset = pd.read_csv("C:/Users/Lochan/OneDrive/Documents/P8Data.csv")
    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    kmeans = KMeans(n_clusters=3).fit(X)
    gmm = GaussianMixture(n_components=3).fit(X)
    y_kmeans = kmeans.predict(X)
    y_gmm = gmm.predict(X)

    plt.subplot(1, 2, 1)
    plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y_kmeans)
    plt.title('K-Means Clustering')

    plt.subplot(1, 2, 2)
    plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y_gmm)
    plt.title('EM Algorithm Clustering')
    plt.show()

    Output:

    Clustering visualizations and comparison of K-Means and EM Algorithm
    """

def program_9():
    return """
    For the given customer dataset, using the dendrogram to find the optimal
    number of clusters and finding Hierarchical Clustering to the dataset.

    Python Code:

    from sklearn.cluster import AgglomerativeClustering
    import matplotlib.pyplot as plt
    import pandas as pd
    import scipy.cluster.hierarchy as sch

    dataset = pd.read_csv('C:/Users/Lochan/OneDrive/Documents/P9Data.csv')
    X = dataset.iloc[:, [3, 4]].values

    dendrogram = sch.dendrogram(sch.linkage(X, method='ward'))
    plt.title('Dendrogram')
    plt.show()

    hc = AgglomerativeClustering(n_clusters=5).fit(X)
    plt.scatter(X[:, 0], X[:, 1], c=hc.labels_, cmap='rainbow')
    plt.title('Hierarchical Clustering')
    plt.show()

    Output:

    Dendrogram and Hierarchical Clustering
    """

def program_10():
    return """
    Build an Artificial Neural Network by implementing the Back propagation
    algorithm and test the same using appropriate data sets.

    Python Code:

    import numpy as np

    X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
    y = np.array(([92], [86], [89]), dtype=float)

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(x):
        return x * (1 - x)

    epoch = 10000
    lr = 0.1
    inputlayer_neurons = 2
    hiddenlayer_neurons = 3
    output_neurons = 1

    wh = np.random.uniform(size=(inputlayer_neurons, hiddenlayer_neurons))
    bh = np.random.uniform(size=(1, hiddenlayer_neurons))
    wout = np.random.uniform(size=(hiddenlayer_neurons, output_neurons))
    bout = np.random.uniform(size=(1, output_neurons))

    for i in range(epoch):
        hinp = np.dot(X, wh) + bh
        hlayer_act = sigmoid(hinp)
        outinp = np.dot(hlayer_act, wout) + bout
        output = sigmoid(outinp)

        EO = y - output
        outgrad = sigmoid_derivative(output)
        d_output = EO * outgrad

        EH = d_output.dot(wout.T)
        hiddengrad = sigmoid_derivative(hlayer_act)
        d_hiddenlayer = EH * hiddengrad

        wout += hlayer_act.T.dot(d_output) * lr
        bout += np.sum(d_output, axis=0, keepdims=True) * lr
        wh += X.T.dot(d_hiddenlayer) * lr
        bh += np.sum(d_hiddenlayer, axis=0, keepdims=True) * lr

    print("Actual Output: ", y)
    print("Predicted Output: ", output)

    Output:

    Actual Output and Predicted Output after training
    """
