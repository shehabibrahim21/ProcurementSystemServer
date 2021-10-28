
# coding: utf-8

# In[1]:

from config import config
import psycopg2
import re
import re
from collections import Counter
def get_specifics():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT specifics1, specifics2, specifics3, specifics4,specifics5
                FROM public."Item" LEFT JOIN public."Specifications" ON 
                public."Item".specificscode = public."Specifications".specificscode 
                ''')
    

    row = cur.fetchone()
    lst = []
    while row is not None:
        for i in list(row):
            if i != ' ' and i not in lst:
                lst.append(i.strip().lower())
        row = cur.fetchone()
    cur.close()
    return lst


# In[2]:


def get_generic_names():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT DISTINCT(genericname) FROM public."Item"''')
    

    row = cur.fetchone()
    lst = []
    while row is not None:
        lst.append(row[0])
        row = cur.fetchone()
    cur.close()
    return lst


# In[3]:



def populate_syn_dict(dct_syn,key,value):
    if key not in dct_syn:
        dct_syn[key] = value
    else:
        temp_lst = dct_syn[key]
        for val in value:
            if val not in temp_lst:
                temp_lst.append(val)
        dct_syn[key] = temp_list


# In[4]:

def lookup(str_):
    dct_syn = {}
    populate_syn_dict(dct_syn, 'short', ['letter', '8.5 by 11', '8.5 x 11'])
    populate_syn_dict(dct_syn, 'long', ['legal', '8.5 by 14', '8.5 x 14'])
    populate_syn_dict(dct_syn, 's-20', ['sub 20', 'substance 20'])
    populate_syn_dict(dct_syn, 's-16', ['sub 16', 'substance 16'])

    lst1 = ['letter', '8.5 by 11', '8.5 x 11']
    lst2 = ['legal', '8.5 by 14', '8.5 x 14']
    lst3 = ['sub 20', 'substance 20']
    lst4 = ['sub 16', 'substance 16']
    lst_ = get_specifics()
    lst_main = lst1 + lst2 + lst3 + lst4 + lst_
    # lst_main = [word.split() for word in lst_main]
    # lst_main = [item.strip() for sublist in lst_main for item in sublist]
    WORDS = Counter(lst_main)

    def words(text):
        return re.findall(r'\w+', text.lower())

    def P(word, N=sum(WORDS.values())):
        "Probability of `word`."
        return WORDS[word] / N

    def correction(word):
        "Most probable spelling correction for word."
        return max(candidates(word), key=P)

    def candidates(word):
        "Generate possible spelling corrections for word."
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

    def known(words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in WORDS)

    def edits1(word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    str_ = str_.lower()
    lst_generics = get_generic_names()
    generic = ''

    for name in lst_generics:
        name = name.lower()
        if name in str_:
            generic = name
            break

    specifics = str_.replace(generic, '')
    specifics = re.sub(' +', ' ', specifics)
    lst_specifics = specifics.split(' ')
    lst_specifics = [word for word in lst_specifics if word]
    temp = ''
    temp_lst = []
    temp_lst_specifics = lst_specifics

    for specific in lst_specifics:
        temp = specific
        for key, val in dct_syn.items():
            if specific in val:
                temp = key
                temp_lst.append(temp)
                temp_lst_specifics.remove(specific)

    lst_tups = []
    for index, specific in enumerate(lst_specifics):
        try:
            str_ = lst_specifics[index] + " " + lst_specifics[index + 1]
            lst_tups.append(str_)
        except:
            pass

    for specific in lst_tups:
        temp = specific
        for key, val in dct_syn.items():
            if specific in val:
                temp = key
                temp_lst.append(temp)
                for word in specific.split(' '):
                    temp_lst_specifics.remove(word)
    temp_lst.extend(temp_lst_specifics)
    lst_ = []
    lst_.append(generic)
    temp_lst = lst_ + temp_lst

    temp_lst = [word.title() for word in temp_lst]
    return temp_lst