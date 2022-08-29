import numpy as np
import RTLearner as rt
from scipy import stats


class BagLearner(object):
    def __init__(self, learner = rt.RTLearner, kwargs = {"leaf_size":1}, bags = 20, boost = False, verbose = False):
        """
        Constructor method
        """
        self.boost = boost
        self.verbose = verbose
        self.learner = learner
        self.bags = bags
        self.learners=[]
        for i in range(0, bags):
            self.learners.append(learner(**kwargs))

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner
        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        for learner in self.learners:
            row = np.random.choice(data_x.shape[0], size = int(data_x.shape[0]),replace = True)
            learner.add_evidence(data_x[row],data_y[row])



    def query(self, points):
        """
        Estimate a set of test points given the model we built.
        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        results = []
        for learner in self.learners:
            results.append(learner.query(points))
        results = np.array(results)
        return stats.mode(results)[0]




if __name__ == "__main__":
    print("BagLearner main")
