#!/usr/bin/env python3

#====================================================================
# Syntax        : python testing/generateTestData.py
# Description   : Generate DB data for test purposes.
#                 Script must be called from the root folder.
#                 Output of SQLite commands is saved into a file.
#                 Output will include deletion of existing data.
# Prerequisites : DB must already have the tables created.
#                 Folder media/ must have images:
#                   + For posts: images_*
#                   + User avatars: avatars_*
# Author        : AP
# Date          : 27 Oct 2015
#--------------------------------------------------------------------


#====================================================================
# Imports
#--------------------------------------------------------------------
import os
import os.path
import glob
import random
import datetime


#====================================================================
# Initializations
#--------------------------------------------------------------------
outfile = 'testdata.sql'
max_posts = 120
words = ['abstineo', 'accipio', 'ad', 'adulescens', 'aequus', 'aetas', 'affero', 'alius', 'alloquor', 'alter', 'amicus', 'an', 'animus', 'annus', 'ante', 'antecapio', 'antefero', 'arma', 'attineo', 'aufero', 'aut', 'autem', 'bellum', 'bonus', 'certus', 'civis', 'civitas', 'colloquor', 'comprobo', 'computo', 'concipio', 'confero', 'conscio', 'consequor', 'contineo', 'contra', 'corpus', 'crimen', 'debeo', 'decipio', 'defero', 'deinde', 'deputo', 'detineo', 'deus', 'differo', 'dignus', 'disputo', 'do', 'dum', 'dux', 'effero', 'ego', 'eloquor', 'enim', 'eo', 'et', 'etiam', 'excipio', 'exputo', 'facilis', 'fero', 'filius', 'fio', 'gens', 'gravis', 'habeo', 'haud', 'hic', 'homo', 'hostis', 'iam', 'idem', 'ille', 'imperium', 'imputo', 'incipio', 'inde', 'infero', 'ingenium', 'inquam', 'inter', 'intercipio', 'interdico', 'interdo', 'intereo', 'interloquor', 'ipse', 'is', 'iste', 'ita', 'iudicium', 'ius', 'mater', 'miles', 'modo', 'mors', 'moveo', 'mulier', 'nam', 'ne', 'nec', 'nemo', 'neque', 'neuter', 'nihil', 'nolo', 'nomen', 'non', 'nondum', 'nos', 'nullus', 'nunc', 'obloquor', 'obtineo', 'occipio', 'occupo', 'offero', 'omnis', 'opes', 'ordo', 'pars', 'pater', 'per', 'percipio', 'perfero', 'perputo', 'pertineo', 'possum', 'post', 'postfero', 'postputo', 'potestas', 'praecipio', 'praefero', 'praeloquor', 'primus', 'principium', 'profero', 'proloquor', 'promitto', 'promoveo', 'propono', 'prosequor', 'prosum', 'provenio', 'provideo', 'provoco', 'publicus', 'qualis', 'quam', 'quantus', 'qui', 'quidam', 'quidem', 'quis', 'quisque', 'recipio', 'refero', 'regnum', 'reputo', 'retineo', 'rex', 'salvus', 'satis', 'se', 'similis', 'sol', 'solus', 'subsequor', 'substo', 'subsum', 'subvenio', 'subvereor', 'sum', 'summitto', 'summoveo', 'suppeto', 'suppono', 'suscipio', 'sustineo', 'suus', 'talis', 'tam', 'tantus', 'tempus', 'teneo', 'totus', 'traloquor', 'trans', 'transeo', 'transfero', 'transmitto', 'transmoveo', 'transpono', 'transtineo', 'tu', 'tuus', 'ubi', 'ullus', 'unde', 'unus', 'urbs', 'uter', 'uxor', 'vereor', 'verus', 'vester', 'video', 'vir', 'virtus', 'volo', 'vos']
topics = ['Aerospace', 'Agriculture', 'Automotive', 'Electrical & Electronics', 'General', 'Green Energy', 'IT & Computing', 'Medical', 'Telecommunications']
names = ['Aditya Kumar', 'Bonita Crittendon', 'Christal Delrosario', 'Davis Stump', 'Florencia Schurman', 'Francis Lamkin', 'Graham Velarde', 'Kristie Luna', 'Mesha Mukhopadhyay', 'Porsche Lunn', 'Shandra Craner', 'Wally Rains']
tags = ['Cloud', 'Big Data', 'Virtualization', 'Data Viz', 'IoT', 'Programming', 'Tips & Tricks', 'Networking', 'Standardization', 'FinTech', 'Event', 'Technology', 'Business', 'Open Source', 'Data Science', 'AI/ML/DL', 'Process', 'Opinion', 'Platform', 'Tools']
options = ['Allow comments', 'Share on Facebook', 'Tweet this post']
images = [os.path.basename(f) for f in glob.glob('media/images_*')]
avatars = [os.path.basename(f) for f in glob.glob('media/avatars_*')]
domains = ['yahoo.com.uk', 'gmail.com', 'outlook.com', 'rediff.com']
last_id = {}


#====================================================================
# Functions
#--------------------------------------------------------------------
def get_words(min=4, max=15):
    ''' Get a random number of words within specified limits.
    '''
    return random.sample(words, random.randint(min, max))


def get_sentence(min=8, max=15, is_title=False):
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


def get_paragraph(min=4, max=8):
    ''' Get a paragraph with a random number of sentences within
        specified limits.
    '''
    para = []
    for i in range(random.randint(min, max)):
        para.append(get_sentence())
    return ' '.join(para)


def get_paragraphs(min=6, max=12):
    ''' Get a random number of paragraphs within specified limits.
    '''
    paras = []
    for _ in range(random.randint(min, max)):
        paras.append(get_paragraph())
    return '\n'.join(paras)


def get_next_id(k):
    ''' Get the next id allocation for the specified key.
        Updated the id allocation.
    '''
    last_id[k] = last_id.get(k, 0) + 1
    return last_id[k]


def get_random_past_time(ref, low, high):
    ''' Get a random time in the past from the specified reference.
        Offset is random based on low and high values.
        Returns a datetime object.
    '''
    delta = datetime.timedelta(days=random.randint(low,high),
                               minutes=random.randint(low,high*10),
                               seconds=random.randint(low,high*10))
    return ref-delta


def clear_db(fout):
    ''' Clear relevant DB tables.
    '''
    for table in ['auth_user', 'blog_author', 'blog_post_options', 'blog_post_tags', 'blog_post', 'blog_option', 'blog_tag', 'blog_topic']:
        fout.write("DELETE FROM {};\n".format(table))


def generate_users_authors(fout):
    ''' Generate users and authors from global variable.
    '''
    for i, name in enumerate(names):
        first_name, last_name = name.split()
        userid = get_next_id('user')

        # Take first user as admin
        if i == 0:
            username = 'admin'
            is_superuser = 1
        else:
            username = '{}.{}'.format(first_name, last_name[:1]).lower()
            is_superuser = 0

        # Password is encrypted form of 'Django'
        fields = {
            'id': userid,
            'password': 'pbkdf2_sha256$20000$ovR5K6mybius$h+/lDPs1TeWzJIdPHgvXUIadsXdCsh5SYqY0SRoLiSw=',
            'is_superuser': is_superuser,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': '{}@{}'.format(username, random.choice(domains)),
            'is_staff': is_superuser,
            'is_active': 1,
            'date_joined': get_random_past_time(datetime.datetime.now(), 500, 800),
            'last_login': None
        }
        keys = sorted(fields.keys())
        s = "INSERT INTO auth_user ({0}) VALUES('{{{1}}}');\n".format(','.join(keys), "}','{".join(keys))
        fout.write(s.format(**fields))

        fields = {
            'id': get_next_id('author'),
            'profile': get_paragraphs(1, 3),
            'photo': avatars[userid % len(avatars)],
            'user_id': userid
        }
        keys = sorted(fields.keys())
        s = "INSERT INTO blog_author ({0}) VALUES('{{{1}}}');\n".format(','.join(keys), "}','{".join(keys))
        fout.write(s.format(**fields))


def generate_blog_options(fout):
    ''' Generate blog options from global variable.
    '''
    for opt in options:
        fields = {
            'id': get_next_id('option'),
            'name': opt
        }
        keys = sorted(fields.keys())
        s = "INSERT INTO blog_option ({0}) VALUES('{{{1}}}');\n".format(','.join(keys), "}','{".join(keys))
        fout.write(s.format(**fields))


def generate_blog_tags(fout):
    ''' Generate tags from global variable.
    '''
    for tag in tags:
        fields = {
            'id': get_next_id('tag'),
            'name': tag
        }
        keys = sorted(fields.keys())
        s = "INSERT INTO blog_tag ({0}) VALUES('{{{1}}}');\n".format(','.join(keys), "}','{".join(keys))
        fout.write(s.format(**fields))


def generate_blog_topics(fout):
    ''' Generate topics from global variable.
    '''
    for topic in topics:
        fields = {
            'id': get_next_id('topic'),
            'name': topic,
            'description': get_paragraph(2, 2)
        }
        keys = sorted(fields.keys())
        s = "INSERT INTO blog_topic ({0}) VALUES('{{{1}}}');\n".format(','.join(keys), "}','{".join(keys))
        fout.write(s.format(**fields))


def generate_post(fout):
    ''' Insert a single post.
        Returns the ID of the newly inserted post.
    '''
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
        'author_id': random.randint(1, len(names)),
        'image': random.choice(images),
        'state': state,
        'topic_id': random.randint(1, len(topics)),
        'text': get_paragraphs(),
        'featured': random.randint(0, 1)
    }

    keys = sorted(fields.keys())
    s = "INSERT INTO blog_post ({0}) VALUES('{{{1}}}');\n".format(','.join(keys), "}','{".join(keys))
    fout.write(s.format(**fields))

    return fields['id']


def generate_post_tags(fout, post_id):
    ''' Get database command to insert tags for a post specified
        by its id.
    '''
    for i in random.sample(range(1,len(tags)+1), random.randint(0,5)):
        fout.write("INSERT INTO blog_post_tags (post_id, tag_id) VALUES({:d},{:d});\n".format(post_id, i))


def generate_post_options(fout, post_id):
    ''' Get database command to insert options for a post specified
        by its id.
    '''
    for i in range(1, last_id['option']+1):
        if random.randint(0, 1):
            fout.write("INSERT INTO blog_post_options (post_id, option_id) VALUES({:d},{:d});\n".format(post_id, i))


#====================================================================
# Main Processing
#--------------------------------------------------------------------
if __name__ == '__main__':
    with open(outfile, "w+") as fout:
        clear_db(fout)
        generate_users_authors(fout)
        generate_blog_options(fout)
        generate_blog_tags(fout)
        generate_blog_topics(fout)

        for _ in range(max_posts):
            post_id = generate_post(fout)
            generate_post_tags(fout, post_id)
            generate_post_options(fout, post_id)
