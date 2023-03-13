import numpy as np
import pandas as pd
import csv
import os

conversation_id = ['155', '247', '271', '299', '359', '414',
                   '715', '797', '826', '832', '840', '898', '1054',
                   '1236', '1251', '1298', '1443', '1479', '1624',
                   '1725', '1746', '2075', '2394']
styletext = '<style>table {width:100%;}table, th, td {border: 1px solid black;border-collapse: collapse;}</style>'

comparison_models_dict = {
    "no_context": "no_context/",
    "guo_context": "guo_context/",
    "gst_realmels": "gst_realmels/",
    "dialog_gcn": "dialog_gcn/",
    "discourse_gcn": "discourse_gcn/",
    "real_recordings": "RealRecordings/",
}

########################################################################################


def build_conv_dataframe(dialog_id):
    utterance_texts = []
    basenames = []

    dialogpath = os.path.join(
        comparison_models_dict["dialog_gcn"], dialog_id)
    dialogue_basenames = sorted([fn for fn in os.listdir(dialogpath)
                                 if fn.endswith('wav')], key=lambda x: int(x.split("_")[0]))

    for textfilepath in dialogue_basenames:
        basename = textfilepath.replace(".wav", "")
        text_filepath = os.path.join(
            dialogpath, textfilepath.replace(".wav", ".txt"))
        text_filepath = text_filepath.replace("dialog_gcn", "RealRecordings")
        # print(text_filepath)
        with open(text_filepath) as f:
            lines = f.readlines()
        utterance_texts.append(lines[0])
        basenames.append(basename)
        # print(lines[0], basename)

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
                                           all_models_list[5])),
                                  columns=['Basename', 'Text', 'No_context',
                                           'Guo_context',  'GST_realmels',
                                           'DialogCGN', 'DiscourseGCN',
                                           'Real_Recordings'])

    return pd_audio_frame


pd_audio_frame = build_conv_dataframe('414')  # '271', '299', '359', '414'

# START---------------------------------------------------------------------------------------------------------------

html_file = open('index.html', 'w')
# Title
html_file.write('<!DOCTYPE html><html>'+styletext +
                '<body><h1>Context Modelling for Conversational TTS</h1>')

for dialog_id in conversation_id:
    # Table Heading
    html_file.write('<h3> Dialog ID:' + dialog_id + '</h3>')

    # Previous History
    prev_contextaudio = "previous_history/prevhistory_" + dialog_id + ".wav"
    prev_contexttext = prev_contextaudio.replace(".wav", ".txt")
    with open(prev_contexttext) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    for ln in lines:
        html_file.write('<p>' + ln + '</p>')
    html_file.write('<br />')
    html_file.write('<p> Real Recordings of first five turns </p>')
    html_file.write('<td><audio controls><source src='+'"' +
                    prev_contextaudio + '"' + ' type="audio/mpeg"></audio></td>')

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
                        row["GST_realmels"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["DialogCGN"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["DiscourseGCN"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<td><audio controls><source src='+'"' +
                        row["Real_Recordings"]+'"' + ' type="audio/mpeg"></audio></td>')
        html_file.write('<tr>')

    html_file.write('</table>')

html_file.write('</body></html>')
html_file.close()
