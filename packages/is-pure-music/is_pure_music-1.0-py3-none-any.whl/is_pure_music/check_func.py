import numpy as np
import torch
from utils import extract_mel_spectrogram,resize_spectrogram
import os
import logging

def is_pure_music(music_path,model_path='./checkpoint/model.pth'):
    """
    判断音乐是否为纯音乐
    :param music_path: 音乐路径
    :return: True or False
    """
    music_name=os.path.basename(music_path)
    mel_spec=extract_mel_spectrogram(music_path)
    resized_mel_spec=resize_spectrogram(mel_spec,(128,4096))
    model=torch.load(model_path)
    input_data=torch.Tensor(resized_mel_spec).unsqueeze(0).cuda()
    output=model(input_data)
    _, predicted = torch.max(output, 1)
    if predicted==0:
        return False
    else:
        return True
