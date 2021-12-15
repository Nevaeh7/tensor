from youtube_dl import YoutubeDL
from pathlib import Path
import pandas as pd
import re
from pathlib import Path


df = pd.read_excel("./1.xlsx")
df = df.dropna(axis=1,how="all")
df = df.fillna(method="ffill")
df = df.set_index("first_class_file_name")
df = df.drop_duplicates()
print(df)
action = df[df.columns[-1]]
all_uniq_action = action[~action.isna()].unique()

action_list = list(all_uniq_action)

out2 = open("all_qsub.sh","w")
i = 0
pre = ''
for folder,info in df.iterrows():
    if info['animal_name'] == pre:
        continue
    i+=1
    pre = info['animal_name']
    name = re.compile("[a-zA-Z]+").findall(folder)[0]
    Path('code').mkdir(exist_ok=True)
    file = Path('code')/f"run_{name}_{i}.sh"
    with open(file,encoding='utf-8',mode='w') as out:
        out.write(f"""#!/bin/bash
#SBATCH -N 1
#SBATCH --partition=batch
#SBATCH -J {name}
#SBATCH -o {name}.%J.out
#SBATCH --mail-user=xiaoming-sudo@outlook.com
#SBATCH --mail-type=ALL
#SBATCH --time=24:00:00
#SBATCH --mem=50G
#SBATCH --ntasks-per-node=20\n""")
        out.write(f"""python main_mut_new_1.py "{folder}||{info['animal_name']}||{str(action_list)}"\n""")
    out2.write(f"sbatch {file}\n")
out2.close()
