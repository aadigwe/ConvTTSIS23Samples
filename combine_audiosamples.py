import argparse
import os
import numpy as np
from pydub import AudioSegment

combined_sound = 0

conversation_id = ['155', '247', '271', '299', '359', '414',
                   '715', '797', '826', '832', '840', '898', '1054',
                   '1236', '1251', '1298', '1443', '1479', '1624',
                   '1725', '1746', '2075', '2394']

for conv_id in conversation_id:
    combined_sound = 0
    folder = sorted([fn for fn in os.listdir("RealRecordings/" + conv_id)
                     if fn.endswith('.wav')], key=lambda x: int(x.split("_")[0]))
    txtfolder = sorted([fn for fn in os.listdir("RealRecordings/" + conv_id)
                        if fn.endswith('.txt')], key=lambda x: int(x.split("_")[0]))
    #os.path.join("RealRecordings", conv_id, fn)
    audiofolder = [os.path.join("RealRecordings/", conv_id, fn)
                   for fn in folder]
    textfolder = [os.path.join("RealRecordings/", conv_id, fn)
                  for fn in txtfolder]
    print(textfolder[0:5])
    print(audiofolder[0:5])

    for audioitem in audiofolder[0:5]:
        print(audioitem)
        combined_sound += AudioSegment.from_wav(audioitem)

    textfile_lines = []
    with open('previous_history/'+"prevhistory_"+conv_id+".txt", 'w') as outfile:
        for textitem in textfolder[0:5]:
            speaker = textitem.split('_')[1]
            with open(textitem) as f:
                line = f.readline()
            newline = "Speaker" + speaker + " " + line + "\n"
            outfile.write(newline)

    combined_sound.export("previous_history/" +
                          "prevhistory_" + conv_id + '.wav', format="wav")
