#!/usr/bin/env python
#
# Copyright 2012 Mark Johnson
# Copyright 2017 Mathieu Bernard, Elin Larsen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Word segmentation evaluation.

Evaluates a segmented text against it's gold version. Display the
precision, recall and f-score at type, token and boundary levels.

"""

import codecs

from wordseg import utils, Separator


DEFAULT_SEPARATOR = Separator(None, None, ' ')
"""Separation for words only, separated by ' '"""


class Evaluation:
    def __init__(self):
        self.test = 0
        self.gold = 0
        self.correct = 0
        self.n = 0
        self.n_exactmatch = 0

    def precision(self):
        return self.correct / (self.test + 1e-100)

    def recall(self):
        return self.correct / (self.gold + 1e-100)

    def fscore(self):
        return 2 * self.correct / (self.test + self.gold + 1e-100)

    def exact_match(self):
        return self.n_exactmatch / (self.n + 1e-100)

    def update(self, test_set, gold_set):
        self.n += 1

        if test_set == gold_set:
            self.n_exactmatch += 1

        self.test += len(test_set)
        self.gold += len(gold_set)
        self.correct += len(test_set & gold_set)

    def update_lists(self, test_sets, gold_sets):
        if len(test_sets) != len(gold_sets):
            raise ValueError(
                '#words different in test and gold: {} != {}'
                .format(len(test_sets), len(gold_sets)))

        for t, g in zip(test_sets, gold_sets):
            self.update(t, g)


class StringPos(object):
    """Compute start and stop index of words in an utterance"""
    def __init__(self):
        self.idx = 0

    def __call__(self, n):
        """Return the position of the current word given its length `n`"""
        start = self.idx
        self.idx += n
        return start, self.idx


def read_data(text, separator=DEFAULT_SEPARATOR):
    """Load text data for evaluation

    :param list(str) text: a list of utterances

    :param Separator separator: token separation to split the
        utterances into words

    :return: two lists (words, positions) where `words` are the input
        utterences with word separators removed, and `positions`
        stores the start/stop index of each word for each utterance.

    """
    words, positions = [], []
    for line in text:
        line = list(separator.split(line.strip(), level='word'))
        words.append(''.join(line))

        idx = StringPos()
        positions.append({idx(len(word)) for word in line})
    return words, positions


def _stringpos_boundarypos(stringpos):
    return [{left for left, _ in line if left > 0} for line in stringpos]


def _stringpos_typepos(stringpos):
    return [{pos for pos in line} for line in stringpos]


def evaluate(text, gold, separator=DEFAULT_SEPARATOR):
    text_words, text_stringpos = read_data(text, separator)
    gold_words, gold_stringpos = read_data(gold, separator)

    if len(gold_words) != len(text_words):
        raise RuntimeError(
            'gold and train have different size: len(gold)={}, len(train)={}'
            .format(len(gold_words), len(text_words)))

    for i, (g, t) in enumerate(zip(gold_words, text_words)):
        if g != t:
            raise RuntimeError(
                'gold and train differ at line {}: gold="{}", train="{}"'
                .format(i+1), g, t)

    type_eval = Evaluation()
    type_eval.update_lists(_stringpos_typepos(text_stringpos),
                           _stringpos_typepos(gold_stringpos))

    token_eval = Evaluation()
    token_eval.update_lists(text_stringpos, gold_stringpos)

    boundary_eval = Evaluation()
    boundary_eval.update_lists(_stringpos_boundarypos(text_stringpos),
                               _stringpos_boundarypos(gold_stringpos))

    return {
        'type_f-score': type_eval.fscore(),
        'type_precision': type_eval.precision(),
        'type_recall': type_eval.recall(),
        'token_f-score': token_eval.fscore(),
        'token_precision': token_eval.precision(),
        'token_recall': token_eval.recall(),
        'bound_f-score': boundary_eval.fscore(),
        'bound_precision': boundary_eval.precision(),
        'bound_recall': boundary_eval.recall()}


@utils.CatchExceptions
def main():
    """Entry point of the 'wordseg-eval' command"""
    streamin, streamout, separator, log, args = utils.prepare_main(
        name='wordseg-eval',
        description=__doc__,
        separator=DEFAULT_SEPARATOR,
        add_arguments=lambda parser: parser.add_argument(
            'gold', metavar='<gold-file>',
            help='gold file to evaluate the input data on'))

    # load the gold text as a list of utterances
    gold = [l.strip() for l in codecs.open(args.gold, 'r', encoding='utf8')]

    # load the text as a list of utterances
    text = [l.strip() for l in streamin]

    # evaluation returns a dict of 'score name' -> float
    results = evaluate(text, gold)

    streamout.write('\n'.join(
        # display scores with 4-digit float precision
        '{}\t{}'.format(k, '%.4g' % v) for k, v in results.items()) + '\n')


if __name__ == '__main__':
    main()
