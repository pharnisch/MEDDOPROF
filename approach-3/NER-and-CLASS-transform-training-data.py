import os
from flair.data import Sentence

# This file assumes that check-for-same-occupations-in-1-and-2.py works! (so that task 1 and 2 share same occupations)

def get_O_for_empty_strings(s: str):
    if s == "":
        return "O"
    return s

# create corpus:
encoding = "utf-8"
folder_task_1 = "../task1/"
folder_task_2 = "../task2/"
directory_task_1 = os.fsencode(folder_task_1)
directory_task_2 = os.fsencode(folder_task_2)
#save_file_all = open("../constructed-training-data/all.txt", "w", encoding=encoding)
token_max = 0
longest_text = ""

files_amount = len(os.listdir(directory_task_1))/2  # because of .txt and .ann files (but semantically it is only one thing)
files_parsed = 0
amount_of_files_to_parse = -1
for file in os.listdir(directory_task_1):
    file_name = os.fsdecode(file)
    if ".txt" in file_name:
        files_parsed += 1
        file_txt = open(folder_task_1 + file_name, "r", encoding=encoding)
        #file_ann_1 = open(folder_task_1 + file_name[:-4] + ".ann", "r", encoding=encoding)
        #file_ann_2 = open(folder_task_2 + file_name[:-4] + ".ann", "r", encoding=encoding)

        if files_parsed % 100 == 0:
            print(f" ... {(files_parsed*100/files_amount):6.2f}% parsed ({files_parsed} out of {files_amount})")

        txt = file_txt.read()
        sent = Sentence(txt)
        if len(sent) > token_max:
            token_max = len(sent)
            longest_text = txt
        continue

        for line_1, line_2 in zip(file_ann_1, file_ann_2):
            line_split_1 = line_1.strip().split("\t")
            inner_split_1 = line_split_1[1].split(" ")

            line_split_2 = line_2.strip().split("\t")
            inner_split_2 = line_split_2[1].split(" ")

            offset_start = int(inner_split_1[1])
            offset_end = int(inner_split_1[2])
            occupation_text = line_split_1[2]

            for tkn in sent:
                if tkn.start_position == offset_start:
                    tkn.add_tag("ner-1", f"B-{inner_split_1[0]}")
                    tkn.add_tag("ner-2", f"B-{inner_split_2[0]}")
                elif tkn.start_position > offset_start and tkn.end_position <= offset_end:
                    tkn.add_tag("ner-1", f"I-{inner_split_1[0]}")
                    tkn.add_tag("ner-2", f"I-{inner_split_2[0]}")

        # write annotated sentence into a training file
        #save_file_all.writelines([f'{tkn.text} {get_O_for_empty_strings(tkn.get_tag("ner-1").value)} {get_O_for_empty_strings(tkn.get_tag("ner-2").value)}\n' for tkn in sent] + ["\n"])


        if files_parsed % 100 == 0:
            print(f" ... {(files_parsed*100/files_amount):6.2f}% parsed ({files_parsed} out of {files_amount})")
        if amount_of_files_to_parse == files_parsed:
            #save_file_all.close()
            quit()

print(token_max)
print(longest_text)
#save_file_all.close()

