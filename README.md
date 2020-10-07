#####################################################################################
#       Function: Automated Spatial Semantic Analysis Towards Commonsense Reasoning
#       Author:   Chao Xu
#       Affiliation: Shandong University
#       Date:     2020-10-7
#####################################################################################

How to run the program?
------------------------------------------------------------------------------------
1. Download StanfordCoreNLP https://stanfordnlp.github.io/CoreNLP/download.html
2. Start StanfordCoreNLP server by using following command:
  java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
3. Use http://localhost:9000/ to test whether the server is up and running.
4. Run semeval2017.py and wsc.py respectively
5. Find the result file test-output.xml and wsc-output.xml in Output directory.
Tips: When you first run python code, it may report an error about the server.
Run it again, then it works.
------------------------------------------------------------------------------------

How to get analysis result of semeval2017?
------------------------------------------------------------------------------------
1. Go to output directory in the terminal.
2. Run the following command:
  java -jar mSpRLEval.jar gold.xml test-output.xml results.txt o ex-dm
3. Find analysis result in results.txt
------------------------------------------------------------------------------------

How to get the statistic data of types of spatial expressions?
------------------------------------------------------------------------------------
1. Run semeval2017-statistic.py
2. Find statistic result in output/statistic
------------------------------------------------------------------------------------

Paper related files:
------------------------------------------------------------------------------------
1. results.txt: Table 6 Overview of the performance of our system
2. wsc_out: analysis result of the examples in Winograd Schema Challenge
------------------------------------------------------------------------------------

the list of program files：
------------------------------------------------------------------------------------
1. classes.py: define two classes, semantic_unit and motion_event
2. conjugate.py: When replacing verb with verb+prep form, we use it to keep the consistency of tense.
3. corenlp.py: get the result of Stanford dependency parser
4. fuzzy_match.py: construction recognition.
5. mapping.py: get semantic roles according to the correspondence relation between syntactic roles and semantic roles.
6. semantic.py: get basic semantic unit of the sentence.
7. semeval2017.py: get the output of spatial role labeling(SpRL) task in Semeval2017.
8. wsc.py: get the output of the examples in Winograd Schema Challenge.
------------------------------------------------------------------------------------

The list of parameter files: in the param directory
------------------------------------------------------------------------------------
1. all_preps: the list of prepositions
2. motion_prep: the corresponding roles of dynamic prepositions (See Table 5 in the paper)
3. path_verb: the list of verbs that incorportate path information
4. spatial_verb: the list of motion verbs and caused-motion verbs
5. SpRL_test.xml: the unannotated data of spatial role labeling task in Semeval2017
6. verb_form: the word forms of verbs
7. wsc_examples: the examples in Winograd Schema Challenge
------------------------------------------------------------------------------------

The list of output files: in the output directory
------------------------------------------------------------------------------------
1. gold.xml: the human-annotated data of spatial role labeling task
2. mSpRLEval.jar: is used to get analysis result of SpRL
3. results.txt: the analysis result of SpRL
4. test-output.xml: the output of semeval2017.py
5. wsc-output.xml: the output of wsc.py
------------------------------------------------------------------------------------
