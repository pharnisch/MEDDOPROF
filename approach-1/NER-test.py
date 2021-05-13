from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger

columns = {0: "text", 1: "ner-1", 2: "ner-2"}
data_folder = "../constructed-training-data/"
corpus = ColumnCorpus(data_folder, columns, train_file="all.txt") #.downsample(0.1)

tagger = SequenceTagger.load("taggers/test/best-model.pt")
result, loss = tagger.evaluate(corpus.test)
print(result.detailed_results, loss)