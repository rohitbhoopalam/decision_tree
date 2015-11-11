"""
Author: Rohit Bhoopalam
UTA Student-ID: 1001100534
Decision Tree
"""
import numpy as np
import math
from collections import Counter

class TNode(object):
    NUMBER_OF_CLASSES = 10
    CLASSES = []
    self.parent = None
    self.children = []
    self.data = []
    self.attributes = []

    def __init__(self, data=[], children=[], parent=None, attributes=[]):
        self.parent = parent
        self.children = children
        self.data = data
        self.attributes = attributes

    def splitNode(self):
        """
            Returns the index of the attribute to split on
        """
        score = []

        for i in range(len(self.attributes)):
            score.append(self.entropy(i))
        min_index = score.index(min(score))

        return min_index

    def attributeActualIndex(self, att_index):
        #attribute index in data
        actual_attribute_index = self.attributes[att_index]
        return actual_attribute_index

    def uniqueAttributes(self, att_index):
        """
            Returns unique attributes of att_index
            in the data
        """
        actual_attribute_index = self.attributeActualIndex(att_index)
        unique_attributes = set(self.data[:, actual_attribute_index])
        return unique_attributes

    def classCounts(self, att_index, att):
        actual_attribute_index = self.attributeActualIndex(att_index)
        classes = self.data[np.where(self.data[:, actual_attribute_index] == att)][:,-1]
        class_counts = Counter(classes)
        counts = []
        for cls in class_counts:
            counts.append(class_counts[cls])

        return counts

    def dataForEntropy(self, att_index):
        """
            Returns entropy_data for entropy calculation
        """
        unique_attributes = self.uniqueAttributes(att_index)
        entropy_data = []

        for att in unique_attributes:
            cls_count_data = self.classCounts(att_index, att)
            entropy_data.append(cls_count_data)

        return entropy_data

    def entropy(self, att_index):
        """
            Returns the entropy for a particular attribute
            with index i
        """
        def _entropy(cls, sum_child):
            t = float(cls)/sum_child
            return -1.0*t*math.log(t,2)

        entropy_data = self.dataForEntropy(att_index)
        data_len = float(len(self.data))

        attribute_entropy = 0 
        for child in entropy_data:
            child_entropy = 0
            sum_child = float(sum(child))
            for cls in child:
                cls_entropy = _entropy(cls, sum_child)
                child_entropy += cls_entropy

            attribute_entropy += (sum_child/data_len) * child_entropy
        return attribute_entropy

    def computeOfChildren(self, min_att_index):
        """
            Returns the number of unique elements
            Assuming those will be the total number of children
            the current node can have
        """
        actual_attribute_index = self.attributeActualIndex(min_att_index)
        _unique_types = set(self.data[:, actual_attribute_index])
        return _unique_types

    def findChildren(self):
        """
        """
        min_att_index = self.splitNode(self)

        children = self.computeOfChildren(min_att_index)

        for child in children:
            _data = []
            _attributes = []
            _parent = self
            _children = []
            _splitting_required = findSplittingRequired()

            node = TNode(_data, _attributes, _parent, _children)
            self.children.append(node)
            if _splitting_required:
                node.findChildren()

if __name__ == "__main__":
    root = TNode(data, attributes, None, [])
    root.findChildren()
