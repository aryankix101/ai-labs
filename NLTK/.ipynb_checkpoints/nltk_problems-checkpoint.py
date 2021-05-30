import nltk
from nltk.corpus import state_union

#4
print(state_union.fileids())
cfd = nltk.ConditionalFreqDist((target,fileid[:4])for fileid in state_union.fileids() for w in state_union.words(fileid) for target in  ['men','women'] if w.lower().startswith(target))
cfd.plot()