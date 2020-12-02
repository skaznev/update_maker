import os
for root, dirs, files in os.walk(r"C:\temp\TEST"):
    for file in files:
        if file.lower() == ("новый текстовый документ.txt"):
             print(os.path.join(root, file))