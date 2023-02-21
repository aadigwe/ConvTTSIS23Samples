import numpy as np
import pandas as pd
import csv
import os

conversation_id = ['299', '359', '414', '1251',
                   '1298', '1479', '1624', '1725', '1746', '2394', ]
styletext = '<style>table {width:100%;}table, th, td {border: 1px solid black;border-collapse: collapse;}</style>'
'''
comparison_models_dict = {
    "no_context": "/Users/adaezeadigwe/Desktop/Interspeech23/no_context/900000/",
    "guo_context": "/Users/adaezeadigwe/Desktop/Interspeech23/guo_context/900000/",
    "guo_discourse": "/Users/adaezeadigwe/Desktop/Interspeech23/guo_discourse/500000",
    "dialog_gcn": "/Users/adaezeadigwe/Desktop/Interspeech23/dialog_gcn/900000",
    "discourse_gcn": "/Users/adaezeadigwe/Desktop/Interspeech23/discourse_gcn/900000",
    "discourse_gcn_ab": "/Users/adaezeadigwe/Desktop/Interspeech23/discourse_gcn_ab/900000",
    "real_recordings": "/Users/adaezeadigwe/Desktop/Interspeech23/RealRecordings/",
}
'''
comparison_models_dict = {
    "no_context": "no_context/900000/",
    "guo_context": "guo_context/900000/",
    "guo_discourse": "guo_discourse/500000",
    "dialog_gcn": "dialog_gcn/900000",
    "discourse_gcn": "discourse_gcn/900000",
    "discourse_gcn_ab": "discourse_gcn_ab/900000",
    "real_recordings": "RealRecordings/",
}
# Other model
# DialogCGN
# DiscourseCGN
# Discourse + Guo
# Discourse GCN + ablation


def build_conv_dataframe(dialog_id):
    utterance_texts = []
    basenames = []

    dialogpath = os.path.join(
        comparison_models_dict["real_recordings"], dialog_id)
    dialogue_basenames = sorted([fn for fn in os.listdir(dialogpath)
                                 if fn.endswith('txt')], key=lambda x: int(x.split("_")[0]))
    for textfilepath in dialogue_basenames:
        basename = textfilepath.replace(".txt", "")
        text_filepath = os.path.join(dialogpath, textfilepath)
        with open(text_filepath) as f:
            lines = f.readlines()
        utterance_texts.append(lines[0])
        basenames.append(basename)

    # Loop through the different models
    all_models_list = []
    for modeltype in list(comparison_models_dict.keys()):
        model_list = []
        for utt_id in basenames:
            # print(os.path.join(
            #    comparison_models_dict[modeltype], dialog_id, utt_id + ".wav"))
            model_list.append(os.path.join(
                comparison_models_dict[modeltype], dialog_id, utt_id + ".wav"))
        all_models_list.append(model_list)

    pd_audio_frame = pd.DataFrame(list(zip(basenames, utterance_texts, all_models_list[0],
                                           all_models_list[1], all_models_list[2],
                                           all_models_list[3], all_models_list[4],
                                           all_models_list[5], all_models_list[6])),
                                  columns=['Basename', 'Text', 'No_context',
                                           'Guo_context',  'Guo_Discourse',
                                           'DialogCGN', 'DiscourseGCN',
                                           'DiscourseGCN_BERT_only',
                                           'Real_Recordings'])

    return pd_audio_frame


pd_audio_frame = build_conv_dataframe('299')
print(pd_audio_frame)

# START---------------------------------------------------------------------------------------------------------------

html_file = open('index.html', 'w')
# Title
html_file.write('<!DOCTYPE html><html>'+styletext +
                '<body><h1>Context Modelling for Conversational TTS</h1>')

for dialog_id in conversation_id:
    # Table Heading
    html_file.write('<h3> Dialog ID:' + dialog_id + '</h3>')
    # Create the Dialog Table
    html_file.write('<table><tr><th>Utterance Id</th><th>Utterance text</th>')
    for modeltype in list(comparison_models_dict.keys()):
        html_file.write('<th>'+modeltype+'</th>')
    html_file.write('</tr>')

    # Build Pandas frame for the dialog
    pd_audio_frame = build_conv_dataframe(dialog_id)
    for index, row in pd_audio_frame.iterrows():
        # Write row by row and populate each cell
        html_file.write('<tr>')
        html_file.write('<td>' + row["Basename"] + '</td>')
        html_file.write('<td>' + row["Text"] + '</td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["No_context"] + '"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["Guo_context"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["Guo_Discourse"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["DialogCGN"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["DiscourseGCN"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["DiscourseGCN_BERT_only"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["Real_Recordings"] + '"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<tr>')

    html_file.write('</table>')

html_file.write('</body></html>')
html_file.close()
