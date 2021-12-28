from youtube_dl import YoutubeDL
from pathlib import Path
import pandas as pd
import re
from pathlib import Path
import numpy as np

df = pd.read_excel('./id-download videos格式(3).xlsx')

columns = df.columns

df[columns[0:3]] = df[columns[0:3]].fillna(method="ffill")

out2 = open("all_video.sh","w")
i = 0
pre = ''
for i in range(len(df)):
    folder = df.iloc[i][0]
    animal_name = df.iloc[i][1]
    action = df.iloc[i][2]
    id_list = list(df.iloc[i][3:])
    id_list = [ids for ids in id_list if ids is not np.nan]
#     id_l_str = '$$'.join(id_list)
    Path('code').mkdir(exist_ok=True)
    file = Path('code')/f"run_{folder}_{animal_name}_{action}.sh"
    with open(file,encoding='utf-8',mode='w') as out:
        out.write(f"""#!/bin/bash
#SBATCH -N 1
#SBATCH --partition=batch
#SBATCH -J {folder}
#SBATCH -o {folder}.%J.out
#SBATCH --mail-user=xiaoming-sudo@outlook.com
#SBATCH --mail-type=ALL
#SBATCH --time=24:00:00
#SBATCH --mem=50G
#SBATCH --ntasks-per-node=20\n""")
        out.write(f"""python download_all_video.py "{folder}||{animal_name}||{action}||{str(id_list)}"\n""")
    out2.write(f"sbatch {file}\n")
out2.close()
