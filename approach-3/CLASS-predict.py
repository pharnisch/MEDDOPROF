import os
from flair.models import SequenceTagger
from flair.data import Sentence

test_texts_path = "../predictions_toy_data/class/1-sequenceTagger/"
encoding = "utf-8"

tagger = SequenceTagger.load("taggers/2-stacked/best-model.pt")

for file in os.listdir(test_texts_path):
    file_name = os.fsdecode(file)
    if ".txt" in file_name:
        txt_file = open(test_texts_path + file_name, "r", encoding=encoding)
        txt = txt_file.read()
        sent = Sentence(txt)

        tagger.predict(sent)
        ann_file = open(test_texts_path + file_name[:-4] + ".ann", "w", encoding=encoding)

        occupation = 0
        label = ""
        start = -1
        end = -1
        for tkn in sent:
            tag = tkn.get_tag("ner-2").value
            if "B-" in tag or "I-" in tag:
                spl = tag.split("-")
                prefix = spl[0]
                label = spl[1]

                occupation += 1
                if prefix == "B":
                    start = tkn.start_position
                end = tkn.end_position  # last one overwrites at last

            else:
                if start != -1 and end != -1:
                    print(" ... adding one line to ann-file!")
                    text = txt[start:end]
                    print(text)
                    ann_file.write(f"T{occupation}\t{label} {start} {end}\t{text}\n")
                    label = ""
                    start = -1
                    end = -1
        if start != -1 and end != -1:
            print(" ... adding one line to ann-file!")
            text = txt[start:end]
            print(text)
            ann_file.write(f"T{occupation}\t{label} {start} {end}\t{text}\n")
            label = ""
            start = -1
            end = -1
        txt_file.close()
        ann_file.close()





