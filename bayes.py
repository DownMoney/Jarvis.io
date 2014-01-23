from __future__ import division
import math
import nltk
import json

class Bayes(object):
        """docstring for Bayes"""
        def __init__(self):
                super(Bayes, self).__init__()
                
                self.features = {}
                self.labelCount = {}
                self.vocab = {}

                self.Load()
                

        def Save(self):
                brain = {}
                brain['features'] = self.features
                brain['labelCount'] = self.labelCount
                brain['vocab'] = self.vocab
                data = open('classifier.json', 'w')
                data.write(json.dumps(brain))
                data.close()

        def Load(self):
                data = open('classifier.json', 'r')
                brain = json.loads(data.read())                
                data.close()
                self.labelCount = brain['labelCount']       
                self.features = brain['features']
                self.vocab = brain['vocab']

        def Train(self, f):        
                data = open(f, 'r')
                for line in data:
                        x = line.lower().strip().split('|')
                        label = x[1]
                        tokens = nltk.word_tokenize(x[0])
                        
                        if label in self.labelCount:
                                self.labelCount[label] += 1
                        else:
                                self.labelCount[label] = 1

                        for token in tokens:
                                if token in vocab:
                                        self.vocab[token] += 1
                                else:
                                        self.vocab[token] = 1

                                if label in self.features:
                                        if token in self.features[label]:
                                                self.features[label][token] += 1
                                        else:
                                                self.features[label][token] = 1
                                else:
                                        self.features[label] = {}
                                        self.features[label][token] =1

                self.Save()


        def Classify(self,data):
                tokens = data.strip().lower().split(' ')
                probLabel = {}
                for label in self.labelCount:                
                        prob = 0.0
                        for token in tokens:
                                if label in self.features and token in self.features[label]:
                                        prob += math.log(self.features[label][token]/self.labelCount[label])
                                else:
                                        prob -= 1

                        probLabel[label] = (self.labelCount[label]/sum(self.labelCount.values())) * math.exp(float(prob))

                return max(probLabel, key = lambda classLabel: probLabel[classLabel])





if __name__ == "__main__":
        bayes = Bayes()
        print bayes.Classify('Sunny Mild Normal Strong')