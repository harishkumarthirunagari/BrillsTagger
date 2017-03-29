#!/usr/bin/env python

from optparse import OptionParser
import os, logging
import utils
import copy
import collections
import operator




def create_model(sentences):
	 ## Pos tagger code
    # we create dictonary objects for model
    model = collections.defaultdict(str)
    counts = collections.defaultdict(int)
    tagsperwordcoll = collections.defaultdict(str)
    allDistinctTags = []
    for sentence in sentences:
        for token in sentence:
            word = token.word
            tag = token.tag
            if not tag in allDistinctTags:
                allDistinctTags.append(tag)
            counts[word + '/' + tag] += 1
            tag += '_'
            tagsineachwordstr = tagsperwordcoll[word]
            if not tag in tagsineachwordstr:
                tagsperwordcoll[token.word] += tag

    for word1 in tagsperwordcoll.keys():
        temptaglist = tagsperwordcoll[word1].split('_')
        max = 0
        maxtag = ''
        for temptag in temptaglist:
            if counts[word1 + '/' + temptag] > max:
                max = counts[word1 + '/' + temptag]
                maxtag = temptag
        model[word1] = maxtag
    return model

    ## YOUR CODE GOES HERE: create a model

    #return model

def predict_tags(sentences, model):
    ## YOU CODE GOES HERE: use the model to predict tags for sentences
    #in this part we change tags basde on most likely tag algorithm
    for sentence in sentences:
        for token in sentence:
                token.tag = model[token.word]
                if model[token.word] is '':
                        token.tag = "NN"		
            #token.tag = model.get(token.word,'NN')
    return sentences













#######Rule 1 creation######################Change tag1 ot tag2 if previoustag is tag0
def rule1(predictedtags,handtags):
    rules = {}
    x=0
   
    
    for sentences in range(len(handtags)):
            
            tinital =1;
            for handtag,predictedtag in zip(handtags[sentences],predictedtags[sentences]):
                    
                    if(tinital == 1):
                            tinital = 0;
                            previoustag = predictedtag.tag
                            continue
                    if(handtag.tag != predictedtag.tag):
                            x+= 1
                            temp =(previoustag,predictedtag.tag,handtag.tag)
                            if temp in rules:
                                    rules[temp]+=1;
                            else:
                                    rules[temp]=1
                    previoustag = predictedtag.tag;
    print x
    return rules

################apply rule1################
def apply_rule1(predictions, rules):
    for rule in rules:
        previoustag = rule[0]
        initaltag =rule[1]
        totag=rule[2]
        for sentences in predictions:
                tinital = 1
                for token in sentences:
                        if (tinital == 1):
                                tinital = 0
                                previoustrainingtag = token.tag
                                continue
                        if(token.tag == initaltag):
                                if(previoustag == previoustrainingtag):
                                        token.tag =totag
                        previoustrainingtag = token.tag
    return predictions




#################taking only some rules that can increase accuracy#######
def threshold_rule1(rules, training_sents, predictions,accuracy):
    new_rules = []
    rulesapplied=0
    for temp in rules:
            if(rules[temp]>200):
                    predictions1 = copy.deepcopy(predictions)
                    rule = []
                    rule.append(temp)
                    new_Predictions = apply_rule1(predictions1,rule)
                    accuracy1 = utils.calc_accuracy(training_sents,new_Predictions)
                    rulesapplied+=1
                    print 'creating rule %s' %rulesapplied
                    if(accuracy1 > accuracy):
                            new_rules.append(temp)
                    
    print rulesapplied
    return new_rules













##############create rule2####################change x to y if two tag before x is z
def rule2(training_sents, predictions):
        rules = collections.defaultdict(int)
        rulesapplied =0
        
        
        for sentences in range(len(training_sents)):  
                
                tinital = 1
                previoustag = ''
                for handtag, predictedtag in zip(training_sents[sentences], predictions[sentences]): 
                        if (tinital == 1):
                                tinital =0
                                previous2tag = previoustag
                                previoustag = predictedtag.tag
                                continue
                        if (handtag.tag != predictedtag.tag):
                                rulesapplied+=1
                                temp = (previoustag, predictedtag.tag, handtag.tag) #[z,x,y]//once change here at last
                                if temp in rules:
                                    rules[temp]+=1
                                else:
                                    rules[temp]=1
                        previous2tag = previoustag
                        previoustag = predictedtag.tag##be careful here it can cause some error
        print rulesapplied

        return rules

    
#################################selecting only some rules############
def threshold_rule2(rules, training_sents, predictions,accuracy):
    new_rules = []
    rulesapplied =0
    for temp in rules.keys():
        if(rules[temp]>300):
            predictions1 = copy.deepcopy(predictions)
            rule = []
            rule.append(temp)
            new_Predictions = apply_rule2(predictions1,rule)
            accuracy1 = utils.calc_accuracy(training_sents,new_Predictions)
            rulesapplied+=1
            print 'creating rule %s' %rulesapplied
            if(accuracy1 > accuracy):
                new_rules.append(temp)
            #print accuracy1
    print rulesapplied
    return new_rules



####################applying selected rules#########
def apply_rule2(predictions, rules):
        
        for rule in rules:
                previousTag = rule[0]
                fromTag = rule[1]
                toTag = rule[2]
                for sentence in predictions:
                        tinital = 1
                        previoustagC = ''
                        for token in sentence:
                                if (tinital == 1):
                                        tinital = 0
                                        previous2tag = previoustagC
                                        previoustagC = token.tag
                                        continue
                                if (token.tag == fromTag):
                                        if (previousTag == previoustagC):
                                                token.tag = toTag
                                previous2tag = previoustagC
                                previoustagC = token.tag
        return predictions








####################creating rule3#############changing x to y if next tag is z
def rule3(training_sents3, predictions3):
    rules3 = collections.defaultdict(int)
    
    
    for sentences in range(len(training_sents3)):  # for sentence in sentences:
        
        tinital = 0
        for handtag3, predictedtag3 in zip(training_sents3[sentences], predictions3[sentences]): # for token in sentence
            if (tinital == 1):
                tinital = 0
                presenttagC = predictedtag3.tag
                temp = (presenttagC, predictedtag, handtag) #[z,x,y]
                if temp in rules3:
                    rules3[temp]+=1
                else:
                    rules3[temp]=1
            if (handtag3.tag != predictedtag3.tag):
                predictedtag = predictedtag3.tag
                handtag = handtag3.tag
                tinital = 1
    
    return rules3


########################selecting only required rules###########################
def threshold_rule3(rules3, training_sents3, predictions3,accuracy3):
        new_rules3 = []
        rulesapplied =0
        for temp in rules3.keys():
                if(rules3[temp]>100):
                        predictionsnew_3 = copy.deepcopy(predictions3)
                        rule = []
                        rule.append(temp)
                        new_Predictions3 = apply_rule3(predictionsnew_3,rule)
                        accuracy_test = utils.calc_accuracy(training_sents3,new_Predictions3)
                        rulesapplied+=1
                        print rulesapplied
                        if(accuracy_test > accuracy3):
                            new_rules3.append(temp)
        print rulesapplied                      
        return new_rules3


######################applying selected rules####################
def apply_rule3(predictions3, rules3):
        for rule3 in rules3:
                nexttag = rule3[0]
                fromtag = rule3[1]
                totag = rule3[2]
                for sentence in predictions3:
                        for token, ftoken in zip(sentence[0::1],sentence[1::1]):
                                if (token.tag == fromtag):
                                        if (nexttag == ftoken.tag):
                                                token.tag = totag
        return predictions3





#######################main##########################################
if __name__ == "__main__":
    usage = "usage: %prog [options] GOLD TEST"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    training_file = "C:\Users\mangw\Downloads\New folder\homework2\hw3_train"
    
    #training phase
    training_sents = utils.read_tokens(training_file)
    model = create_model(training_sents)
	

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(training_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(training_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)
    print"Brill's Tagger"
    print' In Process Of Creating Rules'

    
    #-------------------------------------------------------------
    #rule 1
    print 'RULE -1'
    rules = rule1(predictions,training_sents);
    print 'Number of rules created'
    print len(rules)
    print 'Total Number Of Rules applied'
    rules_new =threshold_rule1(rules,training_sents,predictions,accuracy)
    
    
    predictions_new =  apply_rule1(predictions,rules_new)
    accuracy_new = utils.calc_accuracy(training_sents, predictions_new)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy_new)

    
    #----------------------------------------------------------------
    # rule 2
    print 'RULE -2'
    rules = rule2(training_sents,predictions_new);
    print 'Number of rules created'
    print len(rules)
    rules_new2 = threshold_rule2(rules, training_sents, predictions_new,accuracy_new)
    print 'Total Number of Rules applied'        
    predictions_new2 = apply_rule2(predictions_new,rules_new2);
    accuracy_new2 = utils.calc_accuracy(training_sents, predictions_new2)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy_new2)

    
    #------------------------------------------------------------
    #rule3
    print 'RULE -3'
    rules =rule3(training_sents,predictions_new2)
    print 'Number of rules Created'
    print len(rules)
    rules_new3 = threshold_rule3(rules,training_sents,predictions_new2,accuracy_new2)
    print 'Total Number of Rules applied'
    predictions_new3 = apply_rule3(predictions_new2,rules_new3)
    accuracy_new3 = utils.calc_accuracy(training_sents, predictions_new3)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy_new3)


    #=================================================================================
    #testing phase
    print 'Testing Phase'

    test_file = "C:\Users\mangw\Downloads\New folder\postagger nlp\hw3_heldout"
    testing_sents = utils.read_tokens(test_file)
    test_model = create_model(testing_sents)
    sents_test = utils.read_tokens(test_file)
    test_predictions = predict_tags(sents_test,test_model)
	

    ## read sentences again because predict_tags(...) rewrites the tags
    #test_sents = utils.read_tokens(test_file)
    #test_predictions = predict_tags(testing_sents, model)
    accuracy = utils.calc_accuracy(testing_sents, test_predictions)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy)
    print"Creating Rules for Testing phase"

    
    #-------------------------------------------------------------
    #rule 1
    print 'Creating Rule-1'
    #rules = rule1(predictions,testing_sents);
    #print len(rules)
    #rules_new =filter_rule1(rules,testing_sents,predictions,accuracy)
    predictions_new =  apply_rule1(test_predictions,rules_new)
    accuracy_new = utils.calc_accuracy(testing_sents, predictions_new)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy_new)

    
    #----------------------------------------------------------------
    # rule 2
    print 'Creating Rule-2'
    #rules = create_rule2(testing_sents,predictions_new);
     #print len(rules)
    #rules_new2 = filter_rule2(rules, testing_sents, predictions_new,accuracy_new)
            
    predictions_new2 = apply_rule2(predictions_new,rules_new2);
    accuracy_new2 = utils.calc_accuracy(testing_sents, predictions_new2)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy_new2)

    
    #------------------------------------------------------------
    #rule3
    print 'rule3 processing'
    #rules =create_rule3(testing_sents,predictions_new2)
    #print len(rules)
    #rules_new3 = filter_rule3(rules,testing_sents,predictions_new2,accuracy_new2)
    predictions_new3 = apply_rule3(predictions_new2,rules_new3)
    accuracy_new3 = utils.calc_accuracy(testing_sents, predictions_new3)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy_new3)
    

    ## read sentences again because predict_tags(...) rewrites the tags
    #sents = utils.read_tokens(test_file)
    #predictions = predict_tags(sents, model)
    #accuracy = utils.calc_accuracy(test_sents, predictions)
    #print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)
