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

import featureExtractor,FeatureExtractor2,FeatureExtractor3
import Orange
import orange,orngTest,orngStat,orngTree

def main(phase):

    if(phase == 4):
        f = FeatureExtractor2.FeatureExtractor(createFile =True)
        ft = FeatureExtractor3.FeatureExtractor(createFile=True)
        idlist = f.IDs
        idlist2 = ft.IDs
        FeatureTable = orange.ExampleTable("table2")
        TestTable = orange.ExampleTable("table3")
        training,test = SplitDataInHalf(FeatureTable,f.size)
        learner = orngTree.TreeLearner(training)
        #learner = orngTree.TreeLearner(training)
        #res = orngTest.testOnData([learner],test)
        #learner,res = CrossValidation(FeatureTable,f.size,10)
        res = orngTest.testOnData([learner],test)
        #WriteToFile("test_tonder_olsen.txt",res,idlist2)
        res2 = orngTest.testOnData([learner],FeatureTable)
        #WriteToFile("dev_tonder_olsen.txt",res2,idlist)
    else:
        f = featureExtractor.FeatureExtractor(createFile =True)
        FeatureTable = orange.ExampleTable("table")
        learner,res = CrossValidation(FeatureTable,f.size,10)

    guessyes  = 0
    guessno = 0
    correctyes = 0
    correctno = 0
    for r in res.results:
            if str(r.classes[0]) == "1":
                prtres = "Yes"
            else:
                prtres = "No"

            if str(r.actualClass) == "1":
                prttrue = "Yes"
                correctyes = correctyes +1
            else:
                prttrue = "No"
                correctno = correctno +1
            #print str(r.classes[0]) + " vs correct: " + str(r.actualClass)
            if prtres == "No" and prttrue == "No":
                guessno = guessno +1
            elif prtres == "Yes" and prttrue == "Yes":
                guessyes = guessyes +1
            #print "Guessed " + prtres +" and the correct answer was: " + prttrue
        #res = orngTest.leaveOneOut([learner],FeatureTable)
        #printresult = orngStat.CA(res, orngStat.IS(res))
    #print "Yes Accuracy: " + str(float(guessyes)/float(correctyes))
    #print "No Accuracy: " + str(float(guessno)/float(correctno))
    printresult = orngStat.CA(res)
    print "Accuracy: " + str(printresult[0])
    #print "myAcc: " + str(float((guessno + guessyes)) / float(len(res.results)))

def WriteToFile(name,results,idlist):
    counter = 0
    printstr = "ranked: no\n"
    for r in results.results:
        if str(r.classes[0]) == "1":
            answer = "YES"
        else:
            answer = "NO"
        printstr = printstr + str(idlist[counter]) + " " + answer + "\n"
        counter = counter + 1
    f = open(name,"w")
    f.write(printstr)
    f.close()



def SplitDataInHalf(FeatureTable,n):
    data1 = FeatureTable.getItems(range(0,n/2))
    data2 = FeatureTable.getItems(range(n/2,n))
    return data1,data2

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
    main(4)
