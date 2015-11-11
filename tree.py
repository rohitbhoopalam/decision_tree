"""
Author: Rohit Bhoopalam
UTA Student-ID: 1001100534
Decision Tree
"""
import numpy as np
import math
from collections import Counter

class TNode(object):

    def __init__(self, data=[], attributes={}, parent=None, children=[]):
        self.parent = parent
        self.children = children
        self.data = data
        self.attributes = attributes.copy()
        self.name = ""
        self.predicted_class = {}

    def activeAttributes(self):
        active_attributes = []
        for att in self.attributes:
            if self.attributes[att]:
                active_attributes.append(att)

        return active_attributes

    def splitNode(self):
        """
            Returns the index of the attribute to split on
        """
        score = []

        active_attributes = self.activeAttributes()
        for att_index in active_attributes:
            score.append(self.entropy(att_index))
        print "Entropy scores", score
        min_index = score.index(min(score))

        return active_attributes[min_index]

    def attributeActualIndex(self, att_index):
        return att_index
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

    def computeOfChildren(self, min_att):
        """
            Returns the number of unique elements
            Assuming those will be the total number of children
            the current node can have
        """
        actual_attribute_index = self.attributeActualIndex(min_att)
        _unique_types = set(self.data[:, actual_attribute_index])
        return _unique_types

    def findChildrenDataAttributes(self, child, min_att):
        actual_attribute_index = self.attributeActualIndex(min_att)
        _data = self.data[np.where(self.data[:, actual_attribute_index] == child)]
        self.attributes[actual_attribute_index] = False 
        _attributes = self.attributes.copy()

        return _data, _attributes

    def findSplittingRequired(self):
        classes = set(self.data[:,-1])
        class_case = True if len(classes) > 1 else False
        att_case = False
        for att in self.attributes:
            if self.attributes[att] == True:
                att_case = True
        
        return class_case and att_case

    def findChildren(self):
        """
        """
        min_att = self.splitNode()

        self.name = str(min_att)
        children = self.computeOfChildren(min_att)

        print min_att, children
        for child in children:
            _data, _attributes = self.findChildrenDataAttributes(child, min_att)
            print child, _data, _attributes, len(_data)
            _parent = self


            node = TNode(_data, _attributes, _parent)
            self.children.append(node)

            _splitting_required = node.findSplittingRequired()

            if _splitting_required:
                node.findChildren()
            else:
                node.processClass()

    def processClass(self):
        """
        """
        predicted_class = Counter(self.data[:,-1])
        class_total = 0
        for cls in predicted_class:
            class_total += predicted_class[cls]

        for cls in predicted_class:
            predicted_class[cls] = float(predicted_class[cls])/float(class_total)
        
        self.predicted_class = predicted_class

if __name__ == "__main__":
    #reading data
    data = []

    f = open("MushroomTrain.csv")
    for all_lines in f:
        all_lines = all_lines.split()
        for line in all_lines:
            line = line.split(',')
            temp = line[1:-1]
            temp.append(line[0])
            temp = np.array(temp)
            data.append(temp)
            print temp
    
    data = np.array(data)
    attributes = {0: True, 1: True, 2: True, 3: True}
    root = TNode(data, attributes, None, [])
    root.findChildren()

