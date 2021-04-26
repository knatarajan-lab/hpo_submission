import os
import pandas as pd
from constant import output_path, note_txt_folder


def extract_note_txt():
    note_txt = pd.read_csv(os.path.join(output_path, 'note_text.csv'))
    for index, row in note_txt.iterrows():
        file = open(os.path.join(note_txt_folder, str(row['note_id']) + '.txt'), 'w')
        file.write(row['note_text'])
        file.close()
    return 'note text files saved'
