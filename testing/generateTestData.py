#!/usr/bin/env python3

#====================================================================
# Syntax      : generateTestData.py
# Description : Generate DB data for test purposes. Script must be
#               called from the project's root directory.
# Author      : AP
# Date        : 27 Oct 2015
#--------------------------------------------------------------------


#====================================================================
# Imports
#--------------------------------------------------------------------
import os
import random
import datetime


#====================================================================
# Initializations
#--------------------------------------------------------------------
max_posts = 20
words = ['abstineo', 'accipio', 'ad', 'adulescens', 'aequus', 'aetas', 'affero', 'alius', 'alloquor', 'alter', 'amicus', 'an', 'animus', 'annus', 'ante', 'antecapio', 'antefero', 'arma', 'attineo', 'aufero', 'aut', 'autem', 'bellum', 'bonus', 'certus', 'civis', 'civitas', 'colloquor', 'comprobo', 'computo', 'concipio', 'confero', 'conscio', 'consequor', 'contineo', 'contra', 'corpus', 'crimen', 'debeo', 'decipio', 'defero', 'deinde', 'deputo', 'detineo', 'deus', 'differo', 'dignus', 'disputo', 'do', 'dum', 'dux', 'effero', 'ego', 'eloquor', 'enim', 'eo', 'et', 'etiam', 'excipio', 'exputo', 'facilis', 'fero', 'filius', 'fio', 'gens', 'gravis', 'habeo', 'haud', 'hic', 'homo', 'hostis', 'iam', 'idem', 'ille', 'imperium', 'imputo', 'incipio', 'inde', 'infero', 'ingenium', 'inquam', 'inter', 'intercipio', 'interdico', 'interdo', 'intereo', 'interloquor', 'ipse', 'is', 'iste', 'ita', 'iudicium', 'ius', 'mater', 'miles', 'modo', 'mors', 'moveo', 'mulier', 'nam', 'ne', 'nec', 'nemo', 'neque', 'neuter', 'nihil', 'nolo', 'nomen', 'non', 'nondum', 'nos', 'nullus', 'nunc', 'obloquor', 'obtineo', 'occipio', 'occupo', 'offero', 'omnis', 'opes', 'ordo', 'pars', 'pater', 'per', 'percipio', 'perfero', 'perputo', 'pertineo', 'possum', 'post', 'postfero', 'postputo', 'potestas', 'praecipio', 'praefero', 'praeloquor', 'primus', 'principium', 'profero', 'proloquor', 'promitto', 'promoveo', 'propono', 'prosequor', 'prosum', 'provenio', 'provideo', 'provoco', 'publicus', 'qualis', 'quam', 'quantus', 'qui', 'quidam', 'quidem', 'quis', 'quisque', 'recipio', 'refero', 'regnum', 'reputo', 'retineo', 'rex', 'salvus', 'satis', 'se', 'similis', 'sol', 'solus', 'subsequor', 'substo', 'subsum', 'subvenio', 'subvereor', 'sum', 'summitto', 'summoveo', 'suppeto', 'suppono', 'suscipio', 'sustineo', 'suus', 'talis', 'tam', 'tantus', 'tempus', 'teneo', 'totus', 'traloquor', 'trans', 'transeo', 'transfero', 'transmitto', 'transmoveo', 'transpono', 'transtineo', 'tu', 'tuus', 'ubi', 'ullus', 'unde', 'unus', 'urbs', 'uter', 'uxor', 'vereor', 'verus', 'vester', 'video', 'vir', 'virtus', 'volo', 'vos']
images = os.listdir('media')
globalvars = {
    'image_idx': 0
}
last_id = {
    'user': 5,
    'post' : 2,
    'tag' : 15,
    'option' : 3,
    'category' : 9,
}


#====================================================================
# Functions
#--------------------------------------------------------------------
def get_words(min=4, max=15):
    ''' Get a random number of words within specified limits.
    '''
    return random.sample(words, random.randint(min, max))


def get_sentence(min=4, max=15, is_title=False):
    ''' Get a sentence with a random number of words within 
        specified limits. Return a sentence including a terminating
        period unless it is a title.
    '''
    words = get_words(min, max)
    if is_title:
        sentence = ' '.join(words).title()
    else:
        sentence = ' '.join(words).capitalize() + '.'
    return sentence


def get_paragraph(min=8, max=20):
    ''' Get a paragraph with a random number of sentences within 
        specified limits. 
    '''
    para = []
    for i in range(random.randint(min,max)):
        para.append(get_sentence())
    return ' '.join(para)


def get_paragraphs(min=1, max=4):
    ''' Get a random number of paragraphs within specified limits.
    '''
    paras = []
    for i in range(random.randint(min,max)):
        paras.append(get_paragraph())
    return '\r\n'.join(paras)


def get_next_id(k):
    ''' Get the next id allocation for the specified key.
        Updated the id allocation.
    '''
    if k in last_id:
        last_id[k] += 1
        return last_id[k]
    else:
        return 0


def get_random_past_time(ref, low, high):
    ''' Get a random time in the past from the specified reference.
        Offset is random based on low and high values.
        Returns a datetime object.
    '''
    delta = datetime.timedelta(days=random.randint(low,high),
                               minutes=random.randint(low,high*10),
                               seconds=random.randint(low,high*10))
    return ref-delta


def generate_post():
    ''' Get database command to insert a single post.
    '''
    image = images[globalvars['image_idx']]
    globalvars['image_idx'] = (globalvars['image_idx'] + 1) % len(images)

    state = random.choice(['Draft', 'Published', 'Unpublished'])
    if state != 'Draft':
        pd = get_random_past_time(datetime.datetime.now(), 1, 100)
        cd = get_random_past_time(pd, 1, 10)
    else:
        pd = 'NULL'
        cd = get_random_past_time(datetime.datetime.now(), 1, 10)

    fields = {
        'id': get_next_id('post'),
        'title': get_sentence(is_title=True),
        'created_date': str(cd),
        'published_date': str(pd),
        'author_id': random.randint(1, last_id['user']),
        'image': './' + image,
        'state': state,
        'category_id': random.randint(1, last_id['category']),
        'text': get_paragraphs(),
    }

    keys = sorted(fields.keys())
    s = "INSERT INTO blog_post ({0}) VALUES('{{{1}}}');".format(','.join(keys), "}','{".join(keys));
    print(s.format(**fields));

    return fields['id']


def generate_post_tags(post_id):
    ''' Get database command to insert tags for a post specified
        by its id.
    '''
    for i in random.sample(range(1,last_id['tag']+1), random.randint(0,5)):
        print("INSERT INTO blog_post_tags (post_id, tag_id) VALUES({:d},{:d});".format(post_id, i));


def generate_post_options(post_id):
    ''' Get database command to insert options for a post specified
        by its id.
    '''
    for i in range(1, last_id['option']+1):
        if random.randint(0,1):
            print("INSERT INTO blog_post_options (post_id, option_id) VALUES({:d},{:d});".format(post_id, i));


#====================================================================
# Main Processing
#--------------------------------------------------------------------
if __name__ == '__main__':
    for _ in range(max_posts):
        post_id = generate_post()
        generate_post_tags(post_id)
        generate_post_options(post_id)


