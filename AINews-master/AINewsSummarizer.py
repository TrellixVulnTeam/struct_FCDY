# This file is part of NewsFinder.
# https://github.com/joshuaeckroth/AINews
#
# Copyright (c) 2011 by the Association for the Advancement of
# Artificial Intelligence. This program and parts of it may be used and
# distributed without charge for non-commercial purposes as long as this
# notice is included.

from operator import itemgetter
from subprocess import *
import sys
import os
import re
import nltk

from AINewsConfig import stopwords, paths



class AINewsSummarizer:
    def __init__(self):
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    def summarize_first_two_sentences(self, content):
        content = re.sub(r'^\s*[\(\[].*?[\)\]]\s*', '', content)
        sentences = self.sent_detector.tokenize(content)
        return " ".join(sentences[:2]).strip()

    def summarize_single_ots(self, content):
        f = open(paths['ainews.output'] + 'content.txt', 'w')
        f.write(content)
        f.close()
        (stdout, _) = Popen("%s -r 30 %s" % (paths['libraries.ots'], (paths['ainews.output'] + 'content.txt')), \
                                shell = True, stdout=PIPE).communicate()
        sentences = self.sent_detector.tokenize(stdout)
        return " ".join(sentences[:4]).strip()
    
