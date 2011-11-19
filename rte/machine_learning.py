#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lars
#
# Created:     17.11.2011
# Copyright:   (c) Lars 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import featureExtractor
import Orange
import orange,orngTest,orngStat,orngTree

def main():
    f = featureExtractor.FeatureExtractor(createFile =False)
    FeatureTable = orange.ExampleTable("table")
    learner,res = CrossValidation(FeatureTable,f.size,10)
    #learner = orngTree.TreeLearner(FeatureTable)
    #learner = orange.kNNLearner(FeatureTable, k=10)
    #res = orngTest.learnAndTestOnLearnData([learner], FeatureTable)
    #res = orngTest.crossValidation([learner], FeatureTable, folds=10)
    #res = orngTest.testOnData([learner],FeatureTable)

    print "result length: " + str(len(res.results))
    print "data size: " + str(f.size)
    for r in res.results:
        print str(r.classes[0]) + " vs correct: " + str(r.actualClass)
    #res = orngTest.leaveOneOut([learner],FeatureTable)
    print orngStat.CA(res, orngStat.IS(res))
    #res = orange.evaluation.testing.cross_validation([learner], FeatureTable)
    #print orange.evaluation.scoring.MSE(res)[0]

def CrossValidation(FeatureTable,n, p):
    """
    FeatureTable = an orange ExampeTable with training data
    n = the size of the test data
    p = the number of sections you will make of the training data
    """
    learner = None
    results = None
    best = 0
    for i in range(p):
        start = i*n/p
        end = start + (n/p)
        testData = FeatureTable.getItems(range(start,end))
        trainingData = FeatureTable.getItems(range(0,start))
        for x in range(end,n):
            trainingData.append(FeatureTable[x])
        l = orngTree.TreeLearner(trainingData)
        res = orngTest.testOnData([l],testData)
        c = 0
        for r in res.results:
            if r.classes[0] == r.actualClass:
                c = c+1
        if c > best:
            best = c
            learner = l
            results = res

    return learner,results

if __name__ == '__main__':
    main()
