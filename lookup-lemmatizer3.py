### This program is a very simple lemmatizer, which learns a
### lemmatization function from an annotated corpus. The function is
### so basic I wouldn't even consider it machine learning: it's
### basically just a big lookup table, which maps every word form
### attested in the training data to the most common lemma associated
### with that form. At test time, the program checks if a form is in
### the lookup table, and if so, it gives the associated lemma; if the
### form is not in the lookup table, it gives the form itself as the
### lemma (identity mapping).
### The program performs training and testing in one run: it reads the
### training data, learns the lookup table and keeps it in memory,
### then reads the test data, runs the testing, and reports the
### results.
### The program takes two command line arguments, which are the paths
### to the training and test files. Both files are assumed to be
### already tokenized, in Universal Dependencies format, that is: each
### token on a separate line, each line consisting of fields separated
### by tab characters, with word form in the second field, and lemma
### in the third field. Tab characters are assumed to occur only in
### lines corresponding to tokens; other lines are ignored.
import sys
import re
import random
random.seed(55)
### Global variables
# Paths for data are read from command line
train_file = sys.argv[1]
test_file = sys.argv[2]
# Counters for lemmas in the training data: word form -> lemma -> count
lemma_count = {}
# Lookup table learned from the training data: word form -> lemma
lemma_max = {}
# Variables for reporting results
training_stats = ['Wordform types', 'Wordform tokens', 'Unambiguous types', 'Unambiguous tokens', 'Ambiguous types',
                  'Ambiguous tokens', 'Ambiguous most common tokens', 'Identity tokens']
training_counts = dict.fromkeys(training_stats, 0)
test_outcomes = ['Total test items', 'Found in lookup table', 'Lookup match', 'Lookup mismatch',
                 'Not found in lookup table', 'Identity match', 'Identity mismatch']
test_counts = dict.fromkeys(test_outcomes, 0)
accuracies = {}
### Training: read training data and populate lemma counters
train_data = open(train_file, 'r', encoding="utf8")
for line in train_data:
    # Tab character identifies lines containing tokens
    if re.search('\t', line):
        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')
        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        ######################################################
        ### Insert code for populating the lemma counts    ###
        if form in lemma_count:
            temp = lemma_count[form]
            if lemma in temp:
                count = temp[lemma]
                count += 1
                temp[lemma] = count
            else:
                temp[lemma] = 1
        else:
            temp = {}
            temp[lemma] = 1
            lemma_count[form] = temp
        ######################################################
## Model building and training statistics
for form in lemma_count.keys():
######################################################
### Insert code for building the lookup table      ###
    temp = lemma_count[form]
    val = max(temp.values())
    # tie = []
    for key,values in temp.items():
        if val == values:
            lemma_max[form] = key
            # break
    #         tie.append(key)
    # idx = random.randint(0,len(tie)-1)
    # lemma_max[form] = tie[idx]
######################################################
######################################################
### Insert code for populating the training counts ###
count = 0
unambiguous = 0
ambiguous = 0
ambiguous_tokens = 0
unambiguous_tokens = 0
identity_tokens = 0
max_ambiguous_tokens = 0
for form in lemma_count:
    temp = lemma_count[form]
    if len(temp.keys()) == 1:
        unambiguous += 1
    else:
        ambiguous += 1
        max_ambiguous_tokens += max(temp.values())
    for key in temp:
        count += temp[key]
        if len(temp.keys()) == 1:
            unambiguous_tokens += temp[key]
        else:
            ambiguous_tokens += temp[key]
        if form == key:
            identity_tokens += temp[key]
training_counts['Wordform types'] = len(lemma_count.keys())
training_counts['Wordform tokens'] = count
training_counts['Unambiguous types'] = unambiguous
training_counts['Ambiguous types'] = ambiguous
training_counts['Unambiguous tokens'] = unambiguous_tokens
training_counts['Ambiguous tokens'] = ambiguous_tokens
training_counts['Identity tokens'] = identity_tokens
training_counts['Ambiguous most common tokens'] = max_ambiguous_tokens
#####################################################
accuracies['Expected lookup'] = float((training_counts['Ambiguous most common tokens'] + training_counts['Unambiguous tokens'])/ training_counts['Wordform tokens'])
accuracies['Expected identity'] = float(training_counts['Identity tokens']/ training_counts['Wordform tokens'])
### Testing: read test data, and compare lemmatizer output to actual lemma
# for key,value in lemma_max.items():
#     print(key,': ',value)
test_data = open(test_file, 'r', encoding="utf8")
for line in test_data:
    # Tab character identifies lines containing tokens
    if re.search('\t', line):
        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')
        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        ######################################################
        ### Insert code for populating the test counts     ###
        test_counts['Total test items'] += 1
        if form in lemma_max:
            test_counts['Found in lookup table'] += 1
            if lemma == lemma_max[form]:
                test_counts['Lookup match'] += 1
            else:
                test_counts['Lookup mismatch'] += 1
        else:
            test_counts['Not found in lookup table'] += 1
            if form == lemma:
                test_counts['Identity match'] += 1
            else:
                test_counts['Identity mismatch'] += 1
        ######################################################
#
accuracies['Lookup'] =  float(test_counts['Lookup match']/test_counts['Found in lookup table'])
#
accuracies['Identity'] =  float(test_counts['Identity match']/test_counts['Not found in lookup table'])
#
accuracies['Overall'] =  float(test_counts['Found in lookup table']/test_counts['Total test items'])
# for key,value in training_counts.items():
#     print(key,": ",value)
for key,value in test_counts.items():
    print(key,': ',value)
# for key,value in accuracies.items():
#     print(key,': ',value)
### Report training statistics and test results
output = open('lookup-output.txt', 'w')
output.write('Training statistics\n')
for stat in training_stats:
    output.write(stat + ': ' + str(training_counts[stat]) + '\n')
for model in ['Expected lookup', 'Expected identity']:
    output.write(model + ' accuracy: ' + str(accuracies[model]) + '\n')
output.write('Test results\n')
for outcome in test_outcomes:
    output.write(outcome + ': ' + str(test_counts[outcome]) + '\n')
for model in ['Lookup', 'Identity', 'Overall']:
    output.write(model + ' accuracy: ' + str(accuracies[model]) + '\n')
output.close