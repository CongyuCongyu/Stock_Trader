import numpy as np
import random

class RTLearner(object):
    def __init__(self, leaf_size = 1, verbose=False):
        """
        Constructor method
        """
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None


    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner
        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        def build_tree(data_x, data_y):
            if (len(np.unique(data_y))==1):
                return np.array([["leaf", np.mean(data_y), None, None]])
            if (data_x.shape[0]<=self.leaf_size):
                return np.array([["leaf", np.mean(data_y),None,None]])

            index = random.randint(0,data_x.shape[1]-1)
            SplitVal = np.median(data_x[:, index])
            if(max(data_x[:,index])==SplitVal):
                return np.array([["leaf", np.mean(data_y), None, None]])
            lefttree = build_tree(data_x[data_x[:, index] <= SplitVal], data_y[data_x[:, index] <= SplitVal])
            righttree = build_tree(data_x[data_x[:, index] > SplitVal], data_y[data_x[:, index] > SplitVal])
            root = np.array([[index, SplitVal, 1, lefttree.shape[0]+1]])
            tree_tmp = np.append(root, lefttree, axis=0)
            tree = np.append(tree_tmp, righttree, axis=0)
            return tree
        self.tree = build_tree(data_x, data_y)

    def query(self, points):
        """
        Estimate a set of test points given the model we built.
        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        results = []
        tree = np.array(self.tree)
        for i in range(0, points.shape[0]):
            row = 0
            while(self.tree[row,0]!="leaf"):
                SplitVal = tree[row,1]
                index = int(tree[row,0])
                if points[i, index]>SplitVal:
                    row = row+int(tree[row,3])
                else:
                    row = row+1
            results.append(tree[row,1])
        return results




if __name__ == "__main__":
    print("RTLearner main")
