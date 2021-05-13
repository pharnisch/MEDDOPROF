import os
import filecmp

# This code should help to understand similarities or differences between the training data of task 1 and 2
# After my first intuition, I thought that both tasks would share the exact same occupations, and just a different classification direction
# The following code tells us that this is true for tha training data. All the .txt-files are identical used in those tasks.
# Further, they share the exact same occupations (<T-value>, <Start>, <End>).

# same files?

folder_task_1 = "../task1/"
folder_task_2 = "../task2/"

directory_task_1 = os.fsencode(folder_task_1)
directory_task_2 = os.fsencode(folder_task_2)

file_names_task_1 = []
file_names_task_2 = []

for file in os.listdir(directory_task_1):
    file_name = os.fsdecode(file)
    file_names_task_1.append(file_name)

for file in os.listdir(directory_task_2):
    file_name = os.fsdecode(file)
    file_names_task_2.append(file_name)

if len(file_names_task_1) == len(file_names_task_2):
    for file_name in file_names_task_1:
        if file_name not in file_names_task_2:
            print("Certain file from task 1 not found for task 2!")
            quit()
else:
    print("Different amount of training files for task 1 and 2!")
    quit()

print("[x] Same training files!")


# same content within that files?

for file_name in file_names_task_1:
    file_task_1 = open(folder_task_1 + file_name, "r", encoding="utf-8")
    file_task_2 = open(folder_task_2 + file_name, "r", encoding="utf-8")
    if ".txt" in file_name:
        content_file_task_1 = file_task_1.read()
        content_file_task_2 = file_task_2.read()
        if not filecmp.cmp(folder_task_1 + file_name, folder_task_2 + file_name, shallow=False):
            print(f"Text-file {file_name} differs for task 1 and 2!")
    elif ".ann" in file_name:
        for line_task_1, line_task_2 in zip(file_task_1, file_task_2):
            line_split_task_1 = line_task_1.split("\t")
            line_split_task_2 = line_task_2.split("\t")
            if line_split_task_1[0] != line_split_task_2[0] or line_split_task_1[1].split(" ")[1] != line_split_task_2[1].split(" ")[1] or line_split_task_1[1].split(" ")[2] != line_split_task_2[1].split(" ")[2] or line_split_task_1[2] != line_split_task_2[2]:
                print(f"Annotation-file {file_name} differs for task 1 and 2! ({line_task_1}, {line_task_2})")

print("[x] Same .txt-file-content and target-occupations within the .ann-files!")

