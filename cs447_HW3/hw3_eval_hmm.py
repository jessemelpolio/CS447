########################################
## CS447 Natural Language Processing  ##
##           Homework 2               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Evaluate the output of your bigram HMM POS tagger
##
import os.path
import sys
from operator import itemgetter
from collections import defaultdict

# A class for evaluating POS-tagged data
class Eval:
    ################################
    #intput:                       #
    #    goldFile: string          #
    #    testFile: string          #
    #output: None                  #
    ################################
    def __init__(self, goldFile, testFile):
        # print("Your task is to implement an evaluation program for POS tagging")
        self.goldFile = goldFile
        self.testFile = testFile

    ################################
    #intput: None                  #
    #output: float                 #
    ################################
    def getTokenAccuracy(self):
        # print("Return the percentage of correctly-labeled tokens")
        # return 1.0
        total_cnt = 0
        correct_cnt = 0
        gold_file = open(self.goldFile, "r")
        test_file = open(self.testFile, "r")
        for (gold_line, test_line) in zip(gold_file, test_file):
            gold_raw = gold_line.split()
            test_raw = test_line.split()
            for (gold_token, test_token) in zip(gold_raw, test_raw):
                if gold_token == test_token:
                    correct_cnt += 1
                total_cnt += 1
        return correct_cnt/total_cnt

    ################################
    #intput: None                  #
    #output: float                 #
    ################################
    def getSentenceAccuracy(self):
        # print("Return the percentage of sentences where every word is correctly labeled")
        # return 1.0
        total_cnt = 0
        correct_cnt = 0
        gold_file = open(self.goldFile, "r")
        test_file = open(self.testFile, "r")
        for (gold_line, test_line) in zip(gold_file, test_file):
            gold_raw = gold_line.split()
            test_raw = test_line.split()
            if gold_raw == test_raw:
                correct_cnt += 1
            total_cnt += 1
        return correct_cnt/total_cnt

    ################################
    #intput:                       #
    #    outFile: string           #
    #output: None                  #
    ################################
    def writeConfusionMatrix(self, outFile):
        # print("Write a confusion matrix to outFile; elements in the matrix can be frequencies (you don't need to normalize)")
        con_mat = defaultdict(lambda: defaultdict(int))
        tag_set = set()
        gold_file = open(self.goldFile, "r")
        test_file = open(self.testFile, "r")
        for (gold_line, test_line) in zip(gold_file, test_file):
            gold_raw = gold_line.split()
            test_raw = test_line.split()
            for (gold_token, test_token) in zip(gold_raw, test_raw):
                gold_tag = gold_token.split('_')[1]
                test_tag = test_token.split('_')[1]
                tag_set.add(gold_tag)
                tag_set.add(test_tag)
                con_mat[gold_tag][test_tag] += 1
        tag_list = list(tag_set)
        f = open(outFile, 'w')
        for tag in tag_list:
            f.write('\t{0}'.format(tag))
        f.write('\n')
        for gt in tag_list:
            f.write(gt)
            for tt in tag_list:
                f.write("\t{0}".format(con_mat[gt][tt]))
            f.write('\n')

    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    def getPrecision(self, tagTi):
        # print("Return the tagger's precision when predicting tag t_i")
        # return 1.0
        total_cnt = 0
        correct_cnt = 0
        gold_file = open(self.goldFile, "r")
        test_file = open(self.testFile, "r")
        for (gold_line, test_line) in zip(gold_file, test_file):
            gold_raw = gold_line.split()
            test_raw = test_line.split()
            for (gold_token, test_token) in zip(gold_raw, test_raw):
                gold_tag = gold_token.split('_')[1]
                test_tag = test_token.split('_')[1]
                if test_tag == tagTi:
                    total_cnt += 1
                    if test_tag == gold_tag:
                        correct_cnt += 1
        return correct_cnt/total_cnt


    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    # Return the tagger's recall on gold tag t_j
    def getRecall(self, tagTj):
        # print("Return the tagger's recall for correctly predicting gold tag t_j")
        # return 1.0
        total_cnt = 0
        correct_cnt = 0
        gold_file = open(self.goldFile, "r")
        test_file = open(self.testFile, "r")
        for (gold_line, test_line) in zip(gold_file, test_file):
            gold_raw = gold_line.split()
            test_raw = test_line.split()
            for (gold_token, test_token) in zip(gold_raw, test_raw):
                gold_tag = gold_token.split('_')[1]
                test_tag = test_token.split('_')[1]
                if gold_tag == tagTj:
                    total_cnt += 1
                    if test_tag == gold_tag:
                        correct_cnt += 1
        return correct_cnt/total_cnt


if __name__ == "__main__":
    # Pass in the gold and test POS-tagged data as arguments
    if len(sys.argv) < 2:
        print("Call hw2_eval_hmm.py with two arguments: gold.txt and out.txt")
    else:
        gold = sys.argv[1]
        test = sys.argv[2]
        # You need to implement the evaluation class
        eval = Eval(gold, test)
        # Calculate accuracy (sentence and token level)
        print("Token accuracy: ", eval.getTokenAccuracy())
        print("Sentence accuracy: ", eval.getSentenceAccuracy())
        # Calculate recall and precision
        print("Recall on tag NNP: ", eval.getPrecision('NNP'))
        print("Precision for tag NNP: ", eval.getRecall('NNP'))
        # Write a confusion matrix
        eval.writeConfusionMatrix("confusion_matrix.txt")
