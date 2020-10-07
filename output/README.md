# mSpRL2017Eval
These are CLEF-2017 shared task Evaluation scripts.

## Usage
```
java -jar mSpRLEval.jar actual.xml predicted.xml resutls.txt o/e a/ex-d/ex-dm
```

use `o` for overlapping matching and `e` for exact matching.

use `a` to evaluate all specific type values, `ex-d` to exclude distance relations and `ex-dm` to exclude distance and multi-label relations.

java -jar mSpRLEval.jar gold.xml gold.xml resutls.txt o ex-dm

java -jar mSpRLEval.jar train.xml train.xml resutls.txt o ex-dm

java -jar mSpRLEval.jar test.xml gold.xml resutls.txt o ex-dm
java -jar mSpRLEval.jar gold.xml test.xml resutls.txt o ex-dm

java -jar mSpRLEval.jar train.xml train-output.xml resutls.txt o ex-dm
java -jar mSpRLEval.jar gold.xml test-output.xml resutls.txt o ex-dm
