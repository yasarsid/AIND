import warnings
from asl_data import SinglesData
import traceback


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    probabilities = []
    guesses = []
    for word_index in test_set.get_all_sequences().keys():
        log_l_dict = dict()
        optimum_log_l_score = float("-inf")
        best_guess = ''
        for model_key in models.keys():
            try:
                X, lengths = test_set.get_item_Xlengths(word_index)
                log_l_score = models[model_key].score(X, lengths)
                log_l_dict[model_key] = log_l_score
                if log_l_score > optimum_log_l_score:
                    optimum_log_l_score = log_l_score
                    best_guess = model_key
            except :
                log_l_dict[model_key] = float('-inf')
        probabilities.append(log_l_dict)
        guesses.append(best_guess)
    return probabilities, guesses
