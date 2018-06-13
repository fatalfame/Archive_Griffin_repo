#!/usr/bin/python3

import yaml
import tweepy
import re
from textgenrnn import textgenrnn
textgen = textgenrnn()
import pandas as pd
import random



# textgen.train_from_file('..//markov/trumptweets.txt', num_epochs=1)
# textgen.generate()

textgen = textgenrnn(weights_path='..//markov/video_games_colaboratory_weights.hdf5',
                       vocab_path='..//markov/video_games_colaboratory_vocab.json',
                       config_path='..//markov/video_games_colaboratory_config.json')

# textgen.generate_samples(max_gen_length=1000)
textgen.generate(20, prefix='', temperature=0.7)
# textgen.generate_to_file('..//markov/textgenrnn_dd_100_texts.txt', max_gen_length=1000)

# latest_file = ('..//markov/depechedad.txt')

# model_cfg = {
#     'rnn_size': 128,
#     'rnn_layers': 4,
#     'rnn_bidirectional': True,
#     'max_length': 40,
#     'max_words': 10000,
#     'dim_embeddings': 100,
#     'word_level': False,
# }
#
# train_cfg = {
#     'line_delimited': True,
#     'num_epochs': 3,
#     'gen_epochs': 1,
#     'batch_size': 1024,
#     'train_size': 0.7,
#     'dropout': 0.2,
#     'max_gen_length': 300,
#     'validation': True,
#     'is_csv': False
# }
#
# model_name = 'colaboratory'
# textgen = textgenrnn(name=model_name)
#
# train_function = textgen.train_from_file if train_cfg['line_delimited'] else textgen.train_from_largetext_file
#
# train_function(
#     file_path=latest_file,
#     new_model=True,
#     num_epochs=train_cfg['num_epochs'],
#     gen_epochs=train_cfg['gen_epochs'],
#     batch_size=train_cfg['batch_size'],
#     train_size=train_cfg['train_size'],
#     dropout=train_cfg['dropout'],
#     max_gen_length=train_cfg['max_gen_length'],
#     validation=train_cfg['validation'],
#     is_csv=train_cfg['is_csv'],
#     rnn_layers=model_cfg['rnn_layers'],
#     rnn_size=model_cfg['rnn_size'],
#     rnn_bidirectional=model_cfg['rnn_bidirectional'],
#     max_length=model_cfg['max_length'],
#     dim_embeddings=model_cfg['dim_embeddings'],
#     word_level=model_cfg['word_level'])