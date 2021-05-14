from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.embeddings import TransformerWordEmbeddings, FlairEmbeddings, StackedEmbeddings, WordEmbeddings
from torch.optim.lr_scheduler import OneCycleLR
import flair
import torch

flair.set_seed(1)

task = "ner-2"  # 1 (NER): ner-1, 2 (CLASS): ner-2
columns = {0: "text", 1: "ner-1", 2: "ner-2"}
data_folder = "../constructed-training-data/"
# TODO: for full retraining at the end, sample_missing_splits=False
corpus = ColumnCorpus(data_folder, columns, train_file="all.txt")  #.downsample(0.1)

print(f"The training corpus contains {len(corpus.train)} (pretty long) sample sentences.")
print(f"The validation corpus contains {len(corpus.dev)} (pretty long) sample sentences.")
print(f"The testing corpus contains {len(corpus.test)} (pretty long) sample sentences.")

hidden_size = 128
embeddings = StackedEmbeddings(embeddings=[WordEmbeddings("es"), FlairEmbeddings("es-forward"), FlairEmbeddings("es-backward")]) # TransformerWordEmbeddings()
dictionary = corpus.make_tag_dictionary(task)
tagger = SequenceTagger(hidden_size, embeddings, dictionary, task)

trainer = ModelTrainer(tagger, corpus, optimizer=torch.optim.AdamW)
trainer.train(
    base_path=f"taggers/{task}-stacked",
    train_with_dev=False,
    max_epochs=30,
    learning_rate=0.001,
    mini_batch_size=32,
    weight_decay=0.,
    embeddings_storage_mode="none",
    scheduler=OneCycleLR,
)


# trainer = ModelTrainer(tagger, corpus)
# trainer.train(
#     base_path="taggers/2-stacked",
#     train_with_dev=False,
#     max_epochs=30,
#     learning_rate=0.1,
#     mini_batch_size=32,
# )
