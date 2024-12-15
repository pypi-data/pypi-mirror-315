def program_1():
    return """
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

    # Evaluate regression algorithm on training dataset
    def evaluate_algorithm(dataset, algorithm):
        test_set = []
        for row in dataset:
            row_copy = list(row)
            row_copy[-1] = None
            test_set.append(row_copy)
        predicted = algorithm(dataset, test_set)
        print(predicted)
        actual = [row[-1] for row in dataset]
        rmse = rmse_metric(actual, predicted)
        return rmse

    # Calculate the mean value of a list of numbers
    def mean(values):
        return sum(values) / float(len(values))

    # Calculate covariance between x and y
    def covariance(x, mean_x, y, mean_y):
        covar = 0.0
        for i in range(len(x)):
            covar += (x[i] - mean_x) * (y[i] - mean_y)
        return covar / float(len(x))

    # Calculate the variance of a list of numbers
    def variance(values, mean):
        return sum([(x - mean)**2 for x in values]) / float(len(values))

    # Calculate coefficients
    def coefficients(dataset):
        x = [row[0] for row in dataset]
        y = [row[1] for row in dataset]
        x_mean, y_mean = mean(x), mean(y)
        b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
        b0 = y_mean - b1 * x_mean
        return [b0, b1]

    # Simple linear regression algorithm
    def simple_linear_regression(train, test):
        predictions = []
        b0, b1 = coefficients(train)
        for row in test:
            yhat = b0 + b1 * row[0]
            predictions.append(yhat)
        return predictions

    # Test simple linear regression
    dataset = [[1, 1], [2, 3], [4, 3], [3, 2], [5, 5]]
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    mean_x, mean_y = mean(x), mean(y)
    var_x, var_y = variance(x, mean_x), variance(y, mean_y)

    print('x stats: Mean = %.3f Variance = %.3f' % (mean_x, var_x))
    print('y stats: Mean = %.3f Variance = %.3f' % (mean_y, var_y))

    covar = covariance(x, mean_x, y, mean_y)
    print('Covariance : %.3f' % (covar))

    rmse = evaluate_algorithm(dataset, simple_linear_regression)
    print('RMSE: %.3f' % (rmse))

    # Calculate coefficients
    b0, b1 = coefficients(dataset)
    print('Coefficients: B0 = %.3f, B1 = %.3f' % (b0, b1))

    """

def program_2():
    return """
    import pandas as pd
    import numpy as np

    #to read the data in the csv file
    data = pd.read_csv("C:/Users/ISE14/Documents/CSV_AIML/P2Data.csv")
    print(data)

    #making an array of all the attributes
    d = np.array(data)[:,:-1]
    print("The attributes are: \n",d)
    
    #segragating the target that has positive and negative examples
    target = np.array(data)[:,-1]
    print("The target is: ",target)
    #training function to implement find-s algorithm
    def train(c,t):
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
    #obtaining the final hypothesis
    print("The final hypothesis is:",train(d,target))
    """

def program_3():
    return """
    # Importing Important Libraries
    import numpy as np
    import pandas as pd

    # Loading the data
    data = pd.read_csv('C:/Users/ISE-LAB7/Documents/P3Data.csv')
    print(data)

    # Extracting concepts and target variables
    concepts = np.array(data.iloc[:, 0:-1])
    print(concepts)
    target = np.array(data.iloc[:, -1])
    print(target)

    # Candidate Elimination algorithm
    def learn(concepts, target):
        specific_h = concepts[0].copy()
        print("\nInitialization of specific_h and general_h")
        print("\nSpecific hypothesis: ", specific_h)

        general_h = [["?" for _ in range(len(specific_h))] for _ in range(len(specific_h))]
        print("\nGeneric hypothesis: ", general_h)

        for i, h in enumerate(concepts):
            print("\nInstance", i + 1, "is", h)
            
            if target[i] == "Yes":
                print("Instance is Positive")
                for x in range(len(specific_h)):
                    if h[x] != specific_h[x]:
                        specific_h[x] = '?'
                        general_h[x][x] = '?'
            
            if target[i] == "No":
                print("Instance is Negative")
                for x in range(len(specific_h)):
                    if h[x] != specific_h[x]:
                        general_h[x][x] = specific_h[x]
                    else:
                        general_h[x][x] = '?'
            
            print("Specific hypothesis after", i + 1, "Instance is", specific_h)
            print("Generic hypothesis after", i + 1, "Instance is", general_h)
            print("\n")

        # Removing redundant generic hypotheses
        indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
        for i in indices:
            general_h.remove(["?", "?", "?", "?", "?", "?"])

        return specific_h, general_h

    # Running the Candidate Elimination algorithm
    s_final, g_final = learn(concepts, target)

    # Output final hypotheses
    print("Final Specific_h: ", s_final, sep="\n")
    print("Final General_h: ", g_final, sep="\n")

    """

def program_4():
    return """
    # Importing important libraries
    import pandas as pd
    from pandas import DataFrame

    # Reading Dataset
    df_tennis = pd.read_csv('C:/Users/Lochan/OneDrive/Documents/P4Data.csv')
    print(df_tennis)

    # Function to calculate final Entropy
    def entropy(probs):    
        import math
        return sum([-prob*math.log(prob,2) for prob in probs])

    # Function to calculate Probabilities of positive and negative examples
    def entropy_of_list(a_list):  
        from collections import Counter  
        cnt = Counter(x for x in a_list)   

        # Count the positive and negative examples
        num_instances = len(a_list)  
        # Calculate the probabilities for the entropy formula   
        probs = [x / num_instances for x in cnt.values()]   
        # Calling entropy function for final entropy   
        return entropy(probs)

    total_entropy = entropy_of_list(df_tennis['PT']) 
    print("\nTotal Entropy of PlayTennis Data Set:", total_entropy)

    # Defining Information Gain Function   
    def information_gain(df, split_attribute_name, target_attribute_name, trace=0):  
        print("\nInformation Gain Calculation of ", split_attribute_name)  
        print("target_attribute_name:", target_attribute_name)
        
        # Grouping features of Current Attribute  
        df_split = df.groupby(split_attribute_name)  
        for name, group in df_split: 
            print("Name: ", name)  
            print("Group: ", group)  
        nobs = len(df.index) * 1.0  
        print("NOBS", nobs) 
        
        # Calculating Entropy of the Attribute and probability part of the formula   
        df_agg_ent = df_split.agg( 
            Entropy=(target_attribute_name, entropy_of_list),  
            Prob1=(target_attribute_name, lambda x: len(x) / nobs) 
        ) 
        print("df_agg_ent", df_agg_ent)  
        
        # Calculate Information Gain  
        avg_info = sum(df_agg_ent['Entropy'] * df_agg_ent['Prob1'])  
        old_entropy = entropy_of_list(df[target_attribute_name])  
        return old_entropy - avg_info 

    print('Info-gain for Outlook is : '+str(information_gain(df_tennis, 'Outlook', 'PT')),"\n")

    # Defining ID3 Algorithm Function  
    def id3(df, target_attribute_name, attribute_names, default_class=None):  
        # Counting Total number of yes and no classes (Positive and negative examples) 
        from collections import Counter  
        cnt = Counter(x for x in df[target_attribute_name])  
        if len(cnt) == 1: 
            return next(iter(cnt)) 
        # Return None for Empty Data Set   
        elif df.empty or (not attribute_names):  
            return default_class  
        else: 
            default_class = max(cnt.keys()) 
            print("attribute_names:", attribute_names)  
            gainz = [information_gain(df, attr, target_attribute_name) for attr in attribute_names]   
            # Separating the maximum information gain attribute after calculating the information gain   
            index_of_max = gainz.index(max(gainz))  # Index of Best Attribute   
            best_attr = attribute_names[index_of_max]  # Choosing best attribute   
            # The tree is initially an empty dictionary  
            tree = {best_attr: {}}  # Initiate the tree with the best attribute as a node   
            remaining_attribute_names = [i for i in attribute_names if i != best_attr]  
            for attr_val, data_subset in df.groupby(best_attr):  
                subtree = id3(data_subset, target_attribute_name, remaining_attribute_names, default_class) 
                tree[best_attr][attr_val] = subtree  
            return tree  

    # Get Predictor Names (all but 'class')  
    attribute_names = list(df_tennis.columns)  
    print("List of Attributes:", attribute_names)   
    attribute_names.remove('PT')  # Remove the class attribute   
    print("Predicting Attributes:", attribute_names)  

    # Run Algorithm (Calling ID3 function)  
    from pprint import pprint  
    tree = id3(df_tennis, 'PT', attribute_names)  
    print("\n\nThe Resultant Decision Tree is :\n")  
    pprint(tree)  
    attribute = next(iter(tree))  
    print("Best Attribute :\n", attribute)  
    print("Tree Keys:\n", tree[attribute].keys())

    # Defining a function to calculate accuracy  
    def classify(instance, tree, default=None):  
        attribute = next(iter(tree))  
        print("Key:", tree.keys())  
        print("Attribute:", attribute)  
        print("Instance of Attribute:", instance[attribute], attribute)  
        if instance[attribute] in tree[attribute].keys(): 
            result = tree[attribute][instance[attribute]]  
            print("Instance Attribute:", instance[attribute], "TreeKeys:", tree[attribute].keys())  
            if isinstance(result, dict):   
                return classify(instance, result)  
            else:  
                return result   
        else:  
            return default  

    df_tennis['predicted'] = df_tennis.apply(classify, axis=1, args=(tree, 'No'))   
    print(df_tennis['predicted'])  
    print('\n Accuracy is:\n' + str(sum(df_tennis['PT'] == df_tennis['predicted']) / (1.0 * len(df_tennis.index))))  
    df_tennis[['PT', 'predicted']]  

    training_data = df_tennis.iloc[1:-4]   
    test_data = df_tennis.iloc[-4:]  
    train_tree = id3(training_data, 'PT', attribute_names)  
    test_data['predicted2'] = test_data.apply(classify, axis=1, args=(train_tree, 'Yes'))   
    print('\n\n Accuracy is : ' + str(sum(test_data['PT'] == test_data['predicted2']) / (1.0 * len(test_data.index))))

    """

def program_5():
    return """
    import numpy as np
    import pandas as pd
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    from sklearn import metrics

    # Column names
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']

    # Read dataset to pandas dataframe
    dataset = pd.read_csv("C:/Users/65/Documents/P5Data.csv")

    # Features and target variable
    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    # Display the first few rows of X
    print(X.head())

    # Split dataset into training and testing sets
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.10)

    # Create and train KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors=5).fit(Xtrain, ytrain)

    # Make predictions
    ypred = classifier.predict(Xtest)

    # Output comparison of original and predicted labels
    print("\n-------------------------------------------------------------------------")
    print('%-25s %-25s %-25s' % ('Original Label', 'Predicted Label', 'Correct/Wrong'))
    print("-------------------------------------------------------------------------")

    # Compare each label in the test set
    i = 0
    for label in ytest:
        print('%-25s %-25s' % (label, ypred[i]), end="")
        if label == ypred[i]:
            print(' %-25s' % ('Correct'))
        else:
            print(' %-25s' % ('Wrong'))
        i += 1

    print("-------------------------------------------------------------------------")

    # Display confusion matrix and classification report
    print("\nConfusion Matrix:\n", metrics.confusion_matrix(ytest, ypred))
    print("-------------------------------------------------------------------------")
    print("\nClassification Report:\n", metrics.classification_report(ytest, ypred))
    print("-------------------------------------------------------------------------")

    # Display accuracy score
    print('Accuracy of the classifier is %0.2f' % metrics.accuracy_score(ytest, ypred))
    print("-------------------------------------------------------------------------")

    """

def program_6():
    return """
   
    import numpy as np
    import csv
    import pandas as pd
    from pgmpy.models import BayesianModel
    from pgmpy.estimators import MaximumLikelihoodEstimator
    from pgmpy.inference import VariableElimination

    # Load the dataset and replace missing values
    heartDisease = pd.read_csv("C:/Users/Lochan/OneDrive/Documents/P6Data.csv")
    heartDisease = heartDisease.replace('?', np.nan)

    # Display a few examples from the dataset
    print('Few examples from the dataset are given below')
    print(heartDisease.head())

    # Define the structure of the Bayesian Network
    model = BayesianModel([
        ('age', 'Heartdisease'),
        ('gender', 'Heartdisease'),
        ('exang', 'Heartdisease'),
        ('cp', 'Heartdisease'),
        ('Heartdisease', 'restecg'),
        ('Heartdisease', 'chol')
    ])

    # Learn the Conditional Probability Distributions (CPDs) using Maximum Likelihood Estimators
    print('\nLearning CPDs using Maximum Likelihood Estimators...')
    model.fit(heartDisease, estimator=MaximumLikelihoodEstimator)

    # Perform inference with the Bayesian Network
    print('\nInferencing with Bayesian Network:')
    heartDiseasetest_infer = VariableElimination(model)

    # 1. Probability of HeartDisease given evidence: age = 35
    print('\n1. Probability of HeartDisease given evidence: age = 35')
    q1 = heartDiseasetest_infer.query(variables=['Heartdisease'], evidence={'age': 35})
    print(q1)

    # 2. Probability of HeartDisease given evidence: chol = 250
    print('\n2. Probability of HeartDisease given evidence: chol = 250')
    q2 = heartDiseasetest_infer.query(variables=['Heartdisease'], evidence={'chol': 250})
    print(q2)

    """

def program_7():
    return """
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    from sklearn import metrics

    # Data for clustering
    x1 = np.array([3, 1, 1, 2, 1, 6, 6, 6, 5, 6, 7, 8, 9, 8, 9, 9, 8])
    x2 = np.array([5, 4, 6, 6, 5, 8, 6, 7, 6, 7, 1, 2, 1, 2, 3, 2, 3])

    # First plot: Original dataset
    plt.plot()
    plt.xlim([0, 10])
    plt.ylim([0, 10])
    plt.title('Dataset')
    plt.scatter(x1, x2)
    plt.show()  # Display the first plot showing the dataset

    # Second plot: Clustering using KMeans
    plt.plot()

    # Combine the data into a 2D array
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)

    # KMeans clustering
    K = 3  # Number of clusters
    kmeans_model = KMeans(n_clusters=K).fit(X)

    # Colors and markers for different clusters
    colors = ['b', 'g', 'r']
    markers = ['o', 'v', 's']

    # Plot the clustered data points with different colors and markers
    for i, l in enumerate(kmeans_model.labels_):
        plt.plot(x1[i], x2[i], color=colors[l], marker=markers[l], ls='None')

    # Set the plot limits and show the plot
    plt.xlim([0, 10])
    plt.ylim([0, 10])
    plt.show()  # Display the second plot showing the clustered data

    """

def program_8():
    return """
    from sklearn.cluster import KMeans
    from sklearn.mixture import GaussianMixture
    import sklearn.metrics as metrics
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Load the dataset
    dataset = pd.read_csv("C:/Users/Lochan/OneDrive/Documents/P8Data.csv")

    # Prepare the features and labels
    X = dataset.iloc[:, :-1]
    label = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    y = [label[c] for c in dataset.iloc[:, -1]]

    # Set up the color map for visualization
    colormap = np.array(['red', 'lime', 'black'])

    # Create subplots for visualizations
    plt.figure(figsize=(14, 7))

    # REAL PLOT
    plt.subplot(1, 3, 1)
    plt.title('Real')
    plt.scatter(X.Petal_Length, X.Petal_Width, c=colormap[y])

    # K-MEANS PLOT
    model = KMeans(n_clusters=3, random_state=3425).fit(X)
    plt.subplot(1, 3, 2)
    plt.title('KMeans')
    plt.scatter(X.Petal_Length, X.Petal_Width, c=colormap[model.labels_])

    # Print KMeans performance metrics
    print('The accuracy score of K-Mean: ', metrics.accuracy_score(y, model.labels_))
    print('The Confusion matrix of K-Mean:\n', metrics.confusion_matrix(y, model.labels_))

    # GMM (Gaussian Mixture Model) PLOT
    gmm = GaussianMixture(n_components=3, random_state=3425).fit(X)
    y_cluster_gmm = gmm.predict(X)
    plt.subplot(1, 3, 3)
    plt.title('GMM Classification')
    plt.scatter(X.Petal_Length, X.Petal_Width, c=colormap[y_cluster_gmm])

    # Print GMM performance metrics
    print('The accuracy score of EM: ', metrics.accuracy_score(y, y_cluster_gmm))
    print('The Confusion matrix of EM:\n', metrics.confusion_matrix(y, y_cluster_gmm))

    # Show the plots
    plt.show()

    """

def program_9():
    return """
    # Hierarchical Clustering
    # Importing the libraries
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    # Importing the dataset
    dataset = pd.read_csv('C:/Users/Lochan/OneDrive/Documents/P9Data.csv')
    X = dataset.iloc[:, [3, 4]].values  # Selecting the relevant columns for clustering

    # Using the dendrogram to find the optimal number of clusters
    import scipy.cluster.hierarchy as sch
    dendrogram = sch.dendrogram(sch.linkage(X, method='ward'))
    plt.title('Dendrogram')
    plt.xlabel('Customers')
    plt.ylabel('Euclidean distances')
    plt.show()

    # Fitting Hierarchical Clustering to the dataset
    from sklearn.cluster import AgglomerativeClustering
    hc = AgglomerativeClustering(n_clusters=5, metric='euclidean', linkage='ward')
    y_hc = hc.fit_predict(X)

    # Visualising the clusters
    plt.scatter(X[y_hc == 0, 0], X[y_hc == 0, 1], s=100, c='red', label='Cluster 1')
    plt.scatter(X[y_hc == 1, 0], X[y_hc == 1, 1], s=100, c='blue', label='Cluster 2')
    plt.scatter(X[y_hc == 2, 0], X[y_hc == 2, 1], s=100, c='green', label='Cluster 3')
    plt.scatter(X[y_hc == 3, 0], X[y_hc == 3, 1], s=100, c='cyan', label='Cluster 4')
    plt.scatter(X[y_hc == 4, 0], X[y_hc == 4, 1], s=100, c='magenta', label='Cluster 5')

    # Adding title and labels
    plt.title('Clusters of Customers')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.legend()
    plt.show()

    """

def program_10():
    return """
    
    import numpy as np

    # Input data
    x = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
    print("small x:\n", x)

    # Output data
    y = np.array(([92], [86], [89]), dtype=float)

    # Normalizing input data
    X = x / np.amax(x, axis=0)  # Normalize the inputs to the range [0, 1]
    print("Capital X (Normalized Input):\n", X)

    # Sigmoid Activation Function
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    # Derivative of Sigmoid Function
    def derivatives_sigmoid(x):
        return x * (1 - x)

    # Initializing Variables
    epoch = 7000  # Number of training iterations
    lr = 0.1  # Learning rate
    inputlayer_neurons = 2  # Number of input layer neurons
    hiddenlayer_neurons = 3  # Number of hidden layer neurons
    output_neurons = 1  # Number of output layer neurons

    # Initializing weights and biases with random values
    wh = np.random.uniform(size=(inputlayer_neurons, hiddenlayer_neurons))  # Weights for hidden layer
    bh = np.random.uniform(size=(1, hiddenlayer_neurons))  # Bias for hidden layer
    wout = np.random.uniform(size=(hiddenlayer_neurons, output_neurons))  # Weights for output layer
    bout = np.random.uniform(size=(1, output_neurons))  # Bias for output layer

    # Training the Neural Network (Forward Propagation and Backpropagation)
    for i in range(epoch):
        # Forward Propagation
        hinp1 = np.dot(X, wh)  # Weighted sum for hidden layer
        hinp = hinp1 + bh  # Adding bias
        hlayer_act = sigmoid(hinp)  # Activation for hidden layer
        
        outinp1 = np.dot(hlayer_act, wout)  # Weighted sum for output layer
        outinp = outinp1 + bout  # Adding bias
        output = sigmoid(outinp)  # Final output after sigmoid activation
        
        # Backpropagation Algorithm (Error Calculation and Weight Update)
        EO = y - output  # Error at output layer
        outgrad = derivatives_sigmoid(output)  # Derivative of sigmoid at output
        d_output = EO * outgrad  # Gradient of error at output layer

        EH = d_output.dot(wout.T)  # Error at hidden layer
        hiddengrad = derivatives_sigmoid(hlayer_act)  # Derivative of sigmoid at hidden layer
        d_hiddenlayer = EH * hiddengrad  # Gradient of error at hidden layer

        # Update the weights and biases using the learning rate
        wout += hlayer_act.T.dot(d_output) * lr  # Update weights for output layer
        bout += np.sum(d_output, axis=0, keepdims=True) * lr  # Update biases for output layer
        wh += X.T.dot(d_hiddenlayer) * lr  # Update weights for hidden layer
        bh += np.sum(d_hiddenlayer, axis=0, keepdims=True) * lr  # Update biases for hidden layer

    # Print the actual vs predicted output
    print("Actual Output: \n", y)
    print("Predicted Output: \n", output)

    """
