#from sematch.evaluation import AspectEvaluation
#from sematch.application import SimClassifier, SimSVMClassifier
#from sematch.semantic.similarity import WordNetSimilarity

import sematch as sem


# create aspect classification evaluation
evaluation = sem.AspectEvaluation()
# load the dataset
X, y = evaluation.load_dataset()
# define word similarity function
wns = WordNetSimilarity()
word_sim = lambda x, y: wns.word_similarity(x, y)
# Train and evaluate metrics with unsupervised classification model
simclassifier = SimClassifier.train(zip(X,y), word_sim)
evaluation.evaluate(X,y, simclassifier)


from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()