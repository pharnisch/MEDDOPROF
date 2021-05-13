from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.embeddings import TransformerWordEmbeddings, FlairEmbeddings, StackedEmbeddings, WordEmbeddings
import flair

flair.set_seed(1)

columns = {0: "text", 1: "ner-1", 2: "ner-2"}
data_folder = "../constructed-training-data/"
corpus = ColumnCorpus(data_folder, columns, train_file="all.txt")  #.downsample(0.1)

print(f"The training corpus contains {len(corpus.train)} (pretty long) sample sentences.")
print(f"The validation corpus contains {len(corpus.dev)} (pretty long) sample sentences.")
print(f"The testing corpus contains {len(corpus.test)} (pretty long) sample sentences.")

hidden_size = 128
embeddings = StackedEmbeddings(embeddings=[WordEmbeddings("es"), FlairEmbeddings("es-forward"), FlairEmbeddings("es-backward")]) # TransformerWordEmbeddings()
dictionary = corpus.make_tag_dictionary("ner-1")
tagger = SequenceTagger(hidden_size, embeddings, dictionary, "ner-1")

trainer = ModelTrainer(tagger, corpus)
trainer.train(
    base_path="taggers/stacked-1",
    train_with_dev=False,
    max_epochs=50,
    learning_rate=0.1,
    mini_batch_size=32,
)

# TODO: do not split data into train, val and test. only in train and val. because there will be coming extra test data without annotation!