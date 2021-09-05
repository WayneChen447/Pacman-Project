# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """

        "*** YOUR CODE HERE ***"


        label_prob = util.Counter();
        for label in self.legalLabels:
            label_prob[label] = float(trainingLabels.count(label)) / len(trainingLabels)
        self.label_prop = label_prob;
        
        best_accuracy = 0;
        best_k = 0;
        best_conditional_prob = util.Counter();
        if (not self.automaticTuning):
            kgrid = [self.k];
        for k in kgrid:
            accuracy = 0;
            count_0 = util.Counter();
            count_1 = util.Counter();
            conditional_prob_0 = util.Counter();
            for label in self.legalLabels:
                count_0[label] = util.Counter();
                count_1[label] = util.Counter();
                conditional_prob_0[label] = util.Counter();
            for i in range(len(trainingData)):
                x = trainingData[i];
                label = trainingLabels[i];
                for key, value in x.items():
                    if (value == 0):
                        count_0[label][key] += 1;
                    else:
                        count_1[label][key] += 1;
            for label in self.legalLabels:
                for feature in self.features:
                    conditional_prob_0[label][feature] = float((count_0[label][feature] + k)) / \
                                                          (count_0[label][feature] + count_1[label][feature] + 2 * k);
            self.conditional_prob = conditional_prob_0;
            num_correct = 0;
            for i in range(len(validationData)):
                x = validationData[i];
                true_label = validationLabels[i];
                prob = self.calculateLogJointProbabilities(x);

                if (true_label == prob.argMax()):
                    num_correct += 1;
            accuracy = float(num_correct) / len(validationData);
            if (accuracy > best_accuracy):
                best_k = k;
                best_accuracy = accuracy;
                best_conditional_prob = conditional_prob_0;
                
        self.conditional_prob = best_conditional_prob;
        
        self.k = best_k;
                
    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()
        
        "*** YOUR CODE HERE ***"
        for label in self.legalLabels:
          
            logJoint[label] = math.log(self.label_prop[label]);
            for feature in self.features:
                
                if (datum[feature] == 0):
                    logJoint[label] += math.log(self.conditional_prob[label][feature]);
                else:
                    logJoint[label] += math.log(1 - self.conditional_prob[label][feature])
        return logJoint;
    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        featuresOdds = [];
        "*** YOUR CODE HERE ***"
        for feature in self.features:
            odd = (1 - self.conditional_prob[label1][feature]) / (1 - self.conditional_prob[label2][feature]);
            featuresOdds.append((odd, feature));
        featuresOdds.sort(reverse = True);
        featuresOdds = [item[1] for item in featuresOdds];
        return featuresOdds[0:100]
