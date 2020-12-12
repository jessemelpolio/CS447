########################################
## CS447 Natural Language Processing  ##
##           Homework 1               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Develop a smoothed n-gram language model and evaluate it on a corpus
##
import os.path
import sys
import random
from operator import itemgetter
from collections import defaultdict
import numpy as np
#----------------------------------------
#  Data input 
#----------------------------------------

# Read a text file into a corpus (list of sentences (which in turn are lists of words))
# (taken from nested section of HW0)
def readFileToCorpus(f):
    """ Reads in the text file f which contains one sentence per line.
    """
    if os.path.isfile(f):
        file = open(f, "r") # open the input file in read-only mode
        i = 0 # this is just a counter to keep track of the sentence numbers
        corpus = [] # this will become a list of sentences
        print("Reading file ", f)
        for line in file:
            i += 1
            sentence = line.split() # split the line into a list of words
            #append this lis as an element to the list of sentences
            corpus.append(sentence)
            if i % 1000 == 0:
    	#print a status message: str(i) turns int i into a string
    	#so we can concatenate it
                sys.stderr.write("Reading sentence " + str(i) + "\n")
        #endif
    #endfor
        return corpus
    else:
    #ideally we would throw an exception here, but this will suffice
        print("Error: corpus file ", f, " does not exist")
        sys.exit() # exit the script
    #endif
#enddef


# Preprocess the corpus to help avoid sess the corpus to help avoid sparsity
def preprocess(corpus):
    #find all the rare words
    freqDict = defaultdict(int)
    for sen in corpus:
	    for word in sen:
	       freqDict[word] += 1
	#endfor
    #endfor

    #replace rare words with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if freqDict[word] < 2:
                sen[i] = UNK
	    #endif
	#endfor
    #endfor

    #bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)
    #endfor
    
    return corpus
#enddef

def preprocessTest(vocab, corpus):
    #replace test words that were unseen in the training with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if word not in vocab:
                sen[i] = UNK
	    #endif
	#endfor
    #endfor
    
    #bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)
    #endfor

    return corpus
#enddef

# Constants 
UNK = "UNK"     # Unknown word token
start = "<s>"   # Start-of-sentence token
end = "</s>"    # End-of-sentence-token


#--------------------------------------------------------------
# Language models and data structures
#--------------------------------------------------------------

# Parent class for the three language models you need to implement
class LanguageModel:
    # Initialize and train the model (ie, estimate the model's underlying probability
    # distribution from the training corpus)
    def __init__(self, corpus):
        print("""Your task is to implement five kinds of n-gram language models:
      a) an (unsmoothed) unigram model (UnigramModel)
      b) a unigram model smoothed using Laplace smoothing (SmoothedUnigramModel)
      c) an unsmoothed bigram model (BigramModel)
      """)
    #enddef

    # Generate a sentence by drawing words according to the 
    # model's probability distribution
    # Note: think about how to set the length of the sentence 
    #in a principled way
    def generateSentence(self):
        print("Implement the generateSentence method in each subclass")
        return "mary had a little lamb ."
    #emddef

    # Given a sentence (sen), return the probability of 
    # that sentence under the model
    def getSentenceProbability(self, sen):
        print("Implement the getSentenceProbability method in each subclass")
        return 0.0
    #enddef

    # Given a corpus, calculate and return its perplexity 
    #(normalized inverse log probability)
    def getCorpusPerplexity(self, corpus):
        print("Implement the getCorpusPerplexity method")
        return 0.0
    #enddef

    # Given a file (filename) and the number of sentences, generate a list
    # of sentences and write each to file along with its model probability.
    # Note: you shouldn't need to change this method
    def generateSentencesToFile(self, numberOfSentences, filename):
        filePointer = open(filename, 'w+')
        for i in range(0,numberOfSentences):
            sen = self.generateSentence()
            prob = self.getSentenceProbability(sen)
            stringGenerated = str(prob) + " " + " ".join(sen) 
            
	#endfor
    #enddef
#endclass

# Unigram language model
class UnigramModel(LanguageModel):
    def __init__(self, corpus):
        self.corpus = corpus
        self.freqDict = defaultdict(int)
        self.probDict = defaultdict(int)
        self.token_num = 0
        self.word_num = 0
        for sen in self.corpus:
            for word in sen:
                self.freqDict[word] += 1
                self.token_num += 1
                if word != start:
                    self.word_num += 1
                    self.probDict[word] += 1
        for key in self.freqDict.keys():
            self.freqDict[key] /= self.token_num
        for key in self.probDict.keys():
            self.probDict[key] /= self.word_num
    #endddef

    def generateSentence(self):
        sen = [start]
        word = np.random.choice(list(self.freqDict.keys()), p=list(self.freqDict.values()))
        while word != end:
            sen.append(word)
            if word == start:
                continue
            word = np.random.choice(list(self.freqDict.keys()), p=list(self.freqDict.values()))
        sen.append(end)
        return sen

    def getSentenceProbability(self, sen):
        pr = 1
        for word in sen:
            if word != start:
                pr *= self.probDict[word]
        return pr
    
    def getCorpusPerplexity(self, corpus):
        perp = 0
        cnt = 0
        for sen in corpus:
            for word in sen:
                if word == start:
                    continue
                cnt += 1
                perp += np.log(self.probDict[word])
        return np.exp(-1/cnt*perp)
#endclass

#Smoothed unigram language model (use laplace for smoothing)
class SmoothedUnigramModel(LanguageModel):
    def __init__(self, corpus):
        self.corpus = corpus
        self.freqDict = defaultdict(int)
        self.probDict = defaultdict(int)
        self.token_num = 0
        self.word_num = 0
        for sen in self.corpus:
            for word in sen:
                self.freqDict[word] += 1
                self.token_num += 1
                if word != start:
                    self.word_num += 1
                    self.probDict[word] += 1
        for key in self.freqDict.keys():
            self.freqDict[key] = (self.freqDict[key] + 1)/(self.token_num + len(self.freqDict.keys()))
        for key in self.probDict.keys():
            self.probDict[key] = (self.probDict[key] + 1)/(self.word_num + len(self.probDict.keys()))
    #endddef

    def generateSentence(self):
        sen = [start]
        word = np.random.choice(list(self.freqDict.keys()), p=list(self.freqDict.values()))
        while word != end:
            sen.append(word)
            if word == start:
                continue
            word = np.random.choice(list(self.freqDict.keys()), p=list(self.freqDict.values()))
        sen.append(end)
        return sen

    def getSentenceProbability(self, sen):
        pr = 1
        for word in sen:
            if word != start:
                pr *= self.probDict[word]
        return pr
    
    def getCorpusPerplexity(self, corpus):
        perp = 0
        cnt = 0
        for sen in corpus:
            for word in sen:
                if word == start:
                    continue
                cnt += 1
                perp += np.log(self.probDict[word])
        return np.exp(-1/cnt*perp)

# Unsmoothed bigram language model
class BigramModel(LanguageModel):
    def __init__(self, corpus):
        self.corpus = corpus
        self.freqDict = defaultdict(dict)
        self.token_num = defaultdict(int)
        self.word_num = 0
        for sen in self.corpus:
            for i in range(1, len(sen)): 
                if sen[i-1] in self.freqDict and sen[i] in self.freqDict[sen[i-1]]: 
                    self.freqDict[sen[i-1]][sen[i]] += 1
                else:
                    self.freqDict[sen[i-1]][sen[i]] = 1
                self.token_num[sen[i-1]] += 1
        for key in self.freqDict.keys():
            for k in self.freqDict[key].keys():
                self.freqDict[key][k] /= self.token_num[key]

    def generateSentence(self):
        sen = [start]
        word = np.random.choice(list(self.freqDict[start].keys()), p=list(self.freqDict[start].values()))
        while word != end:
            sen.append(word)
            word = np.random.choice(list(self.freqDict[word].keys()), p=list(self.freqDict[word].values()))
        sen.append(end)
        return sen

    def getSentenceProbability(self, sen):
        pr = 1
        for i in range(1, len(sen)):
            if sen[i-1] in self.freqDict and sen[i] in self.freqDict[sen[i-1]]: 
                pr *= self.freqDict[sen[i-1]][sen[i]]
            else:
                return 0
        return pr
    
    def getCorpusPerplexity(self, corpus):
        perp = 0
        cnt = 0
        for sen in corpus:
            for i in range(1, len(sen)):
                if sen[i-1] in self.freqDict and sen[i] in self.freqDict[sen[i-1]]: 
                    perp += np.log(self.freqDict[sen[i-1]][sen[i]])
                    cnt += 1
                else:
                    return np.inf
        return np.exp(-1/cnt*perp)
#endclass
#endclass
#endclass

#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    #read your corpora
    trainCorpus = readFileToCorpus('train.txt')
    trainCorpus = preprocess(trainCorpus)
    uni =   UnigramModel(trainCorpus)
    smooth = SmoothedUnigramModel(trainCorpus)
    bi = BigramModel(trainCorpus)

    uni.generateSentencesToFile(20,'unigram_output.txt')
    smooth.generateSentencesToFile(20,'smooth_unigram_output.txt')
    bi.generateSentencesToFile(20,'bigram_output.txt')
    
    posTestCorpus = readFileToCorpus('pos_test.txt')
    negTestCorpus = readFileToCorpus('neg_test.txt')

    vocab = set()
    for sen in trainCorpus:
        for word in sen:
            vocab.add(word)
    # Please write the code to create the vocab over here before the function preprocessTest
    print("""Task 0: create a vocabulary(collection of word types) for the train corpus""")
    posTestCorpus = preprocessTest(vocab, posTestCorpus)
    negTestCorpus = preprocessTest(vocab, negTestCorpus)

    print ("POSTIVE")
    print (uni.getCorpusPerplexity(posTestCorpus))
    print (smooth.getCorpusPerplexity(posTestCorpus))
    print (bi.getCorpusPerplexity(posTestCorpus))

    print ("NEGTIVE")
    print (uni.getCorpusPerplexity(negTestCorpus))
    print (smooth.getCorpusPerplexity(negTestCorpus))
    print (bi.getCorpusPerplexity(negTestCorpus))

