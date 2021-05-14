CONTACT
Name: Philipp Harnisch
Organization: Humboldt-Universität zu Berlin (Student)
E-Mail: p.harnisch.privat@gmail.com

SYSTEM
For each of NER and CLASS, I use a flair SequenceTagger with a stacked embedding
(pretrained on spanish language: word-embedding, flair-embedding-forward, flair-embedding-backward).
For NORM, I use the SequenceTagger trained for NER to find all occupation mentions.
For the second part, calculate the distance between strings and all valid strings, to then take the nearest.
