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
import orange,orngTest,orngStat

def main():
    learner = orange.TreeLearner
    f = featureExtractor.FeatureExtractor()
    FeatureTable = f.ExampleTable
    res = orngTest.crossValidation([learner], FeatureTable, folds=10)
    print orngStat.CA(res, orngStat.IS(res))
    #res = orange.evaluation.testing.cross_validation([learner], FeatureTable)
    #print orange.evaluation.scoring.MSE(res)[0]

if __name__ == '__main__':
    main()
