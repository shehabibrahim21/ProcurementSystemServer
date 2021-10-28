
# coding: utf-8

# In[32]:


import psycopg2
import re
from config import config

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from itertools import chain
from operator import itemgetter
from sklearn.datasets import fetch_20newsgroups
# from IPython.display import display, HTML

def get_items_database(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT public."PPMP_itemdescription".id,public."PPMP_item".general_name,specifics1,specifics2,specifics3,specifics4,specifics5 FROM public."PPMP_itemdescription"
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id where 
    public."PPMP_item".category_id_id = %s''',(str(id_),))
    

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        lst3 = list(row[1:])
        lst3.sort()
        lst3 = [word.strip() for word in lst3]
        dct[row[0]] = lst3
        lst2.append(lst3)
#         return row[0]
        row = cur.fetchone()
    cur.close()
#     lst2 = [word.strip() for word in lst2 if word != 'None']
    return lst2,dct


# In[30]:


def check(lst_given,id_):
    lst_db = get_items_database(id_)[0]
    print("lst_db:",lst_db)
    lst_given.sort()

    print("lst_given",lst_given)
    if lst_given in lst_db:
        return True
    return False


# In[39]:


def get_id(lst_given,id_):
    dct =  get_items_database(id_)[1]
    
    for key,val in dct.items():
        if val == lst_given:
            return key

def get_price_unit(lst_given, id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT price,unit,id,date_created FROM public."PPMP_prices" where item_id_id = %s''',
                (str(get_id(lst_given, id_)),))

    row = cur.fetchone()
    dct = {}
    while row is not None:
        dct[row[3]] = list(row)[0:3]
        row = cur.fetchone()
    cur.close()

    lst1 = []
    for i in dct:
        lst1.append(i)
    i_max = max(lst1)

    return dct[i_max]


class Vectorizer:
    def __init__(self):
        self.word_idf = {}
        self.index_word = {}
        self.word_index = {}

    def build_mappings(self, texts):
        """Initialize word-index mappings

        Parameter
        ---------
        texts : sequence of str
            Corpus to build mappings for
        """
        word_doccount = Counter()
        for text in texts:
            word_doccount.update(set(text.lower().split()))
        N = len(texts)
        self.word_idf = {word: np.log(N / doccount)
                         for word, doccount in word_doccount.items()}
        self.index_word = dict(enumerate(self.word_idf.keys()))
        self.word_index = {v: k for k, v in self.index_word.items()}

    def vectorize(self, text, normalize=None, idf=False):
        """Return the BoW vector representation of text

        Parameters
        ----------
        text : str
            Text to compute the vector representation of
        normalize : 'total', 'norm' or None, optional
            If `total`, normalize by total number of words. If 'norm',
            normalize by Euclidean norm. If None, no normalization is
            performed
        idf : boolean, optional
            Perform IDF weighting if True

        Returns
        -------
        vec : ndarray
            BoW vector representation of text
        """
        word_freq = Counter(text.lower().split())
        vec = np.zeros(len(self.index_word))
        word_freq = Counter(text.lower().split())
        vec = np.zeros(len(self.index_word))

        if idf is True:
            for index, word in self.index_word.items():
                vec[index] = word_freq[word] * self.word_idf[word]
        else:
            for index, word in self.index_word.items():
                vec[index] = word_freq[word]
        if normalize == 'total':
            vec = vec / vec.sum()
        elif normalize == 'norm':
            vec = vec / np.sqrt((vec ** 2).sum())
        return vec


def lpnorm(vec1, vec2, p=2):
    """Compute the L_p-norm distance between vec1 and vec2

    Parameters
    ----------
    vec1 : ndarray
        First vector
    vec2 : ndarray
        Second vector
    p : int or float, optional
        Order of L_p norm; the `p` in L_p norm

    Returns
    -------
    norm : float
        L_p norm distance of `vec1` and `vec2`
    """
    norm = ((abs(vec1 - vec2) ** p).sum()) ** (1 / p)
    return norm


def get_top_three(word):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT 
    public."PPMP_item".general_name,
    public."PPMP_itemdescription".specifics1,
    public."PPMP_itemdescription".specifics2,
    public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4,
    public."PPMP_itemdescription".specifics5


    FROM public."PPMP_item" JOIN public."PPMP_itemdescription" 
    ON  public."PPMP_item".id =  public."PPMP_itemdescription".item_id_id
    ''')

    row = cur.fetchone()
    items = []
    while row is not None:
        str_ = " ".join(list(row))
        str_ = str_.replace("None", "")
        str_ = re.sub(' +', ' ', str_)
        str_ = str_.strip()
        items.append(str_)
        #         lst1.append(list(row))

        row = cur.fetchone()
    cur.close()

    vectorizer = Vectorizer()
    vectorizer.build_mappings(items)

    #     str_ = 'Bond Paper Short'
    item_vectorized = vectorizer.vectorize(word, normalize='norm')
    dct_ = {}
    for item in items:
        vectorized = vectorizer.vectorize(item, normalize='norm')
        dct_[item] = lpnorm(item_vectorized, vectorized)

    dct_ = {k: v for k, v in sorted(dct_.items(), key=lambda item: item[1])}
    top_three = []

    for i, u in dct_.items():
        top_three.append(i)
    return top_three[:3]


def get_item_from_database(item):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT
    public."PPMP_itemdescription".id,
    public."PPMP_item".general_name,
    public."PPMP_itemdescription".specifics1,
    public."PPMP_itemdescription".specifics2,
    public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4,
    public."PPMP_itemdescription".specifics5


    FROM public."PPMP_item" JOIN public."PPMP_itemdescription" 
    ON  public."PPMP_item".id =  public."PPMP_itemdescription".item_id_id
    ''')

    row = cur.fetchone()
    items = []
    #     id_ = []
    lst_of_items = []
    while row is not None:
        lst_orig = row[1:]
        lst_orig = ['' if x == 'None' else x for x in lst_orig]
        lst_of_items.append(lst_orig)
        lst_ = list(row)
        str_ = " ".join(lst_[1:])
        str_ = str_.replace("None", "")
        str_ = re.sub(' +', ' ', str_)
        str_ = str_.strip()
        items.append(str_)
        #         id_.append(lst_[0])
        #         lst1.append(list(row))

        row = cur.fetchone()
    cur.close()
    #     tup_ = (items,lst_of_items)

    for i, u in zip(items, lst_of_items):
        if item == i:
            return u
            break