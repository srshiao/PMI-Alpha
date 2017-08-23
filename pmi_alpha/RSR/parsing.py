#all imports
import re
import pandas
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.tokenize import RegexpTokenizer
from nltk import ngrams
import re
import usaddress
from fuzzywuzzy.process import dedupe
import nltk
import pandas as pd
import os
import codecs
from gensim.models import Phrases
from gensim.models import Word2Vec
import json
import re

#main function goes through all different extraction and puts it into a dictionary so it can be put into the database
def parse_file(resume):
    print(resume)
    parsed = {}
    #execution of extracting name, email, phone number
    parsed['person'] = personel_information(resume)
    #extract major minor of undergrad need work on grad
    parsed['education'] = extract_School(resume)
    #extract companies and work experience but needs a lot of work
    parsed['work'] = extract_company(resume)
    #extracts skills really well but takes time
    parsed['skills'] = extract_all_skills(resume)
    return parsed


#extract name finished
def extract_first_name(resume):
    name = resume.split('\n', 1)[0]
    first_name = name.split(' ', 1)[0]
    return (first_name)

def extract_last_name(resume):
    name = resume.split('\n', 1)[0]
    last_name = name.split(' ', 1)[-1]
    return (last_name)

def extract_name(resume):
    name = extract_first_name(resume) + extract_last_name(resume)
    return name

#extract email finished
def extract_email(resume):
    regular_expression = re.compile(r"(\w+[.|\w])*@(\w+[.])*\w+", re.IGNORECASE)
    result = re.search(regular_expression, resume)
    if result:
        result = result.group()
    return result

#extract phone number finished
def check_phone_number1(resume):
    resume2 = "".join(c for c in resume if c not in ('!','.','-','(',')',' ','+',))
    result = re.findall(r"\d{10}", resume2)
    result = ''.join(result)
    return (result)

def check_phone_number2(resume):
    resume2 = "".join(c for c in resume if c not in ('!','.','-','(',')',' ','+',))
    result = re.findall(r"\d{11}", resume2)
    result = ''.join(result)
    result = result[1:11]
    return (result)

def extract_phone_number(resume):
    try:
        return check_phone_number1(resume)
    except:
        return check_phone_number2(resume)

#aux function to get all personel information
def personel_information(resume):
    personel = {}
    resume_file = resume
    resume_file2 = resume_file.lower()
    #change path
    personel['name'] = extract_name(resume)

    personel['email'] = extract_email(resume)
    personel['phone'] = extract_phone_number(resume)
    personel['address'] = extract_address(resume)
    personel['github'] = check_GitHub(resume)
    #print(check_email(resume))
    personel['linkedin'] = check_linkedin(resume)
    #print(check_phone_number(resume))
    #print('URLs: ',extract_URLs(resume))
    return personel

#gets the school
def extract_School(resume):
    resume_file = resume
    resume_file2 = resume_file.lower()
    major_df = pandas.read_excel(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','majors.xlsx')))
    major_df.columns
    major_file = major_df['Majors'].values
    major_lower = [item.lower() for item in major_file]
    tokenizer = RegexpTokenizer(r'\w+')
    resume_token = tokenizer.tokenize(resume_file)
    resume_token2 = tokenizer.tokenize(resume_file2)
    major_distinct = []
    dictionary = {'Name': 5}
    regular_expression = re.compile(r"/BA|BS|B\.S|Bachelor of Science|Bachelor of Arts|BBA |B/A|Bachelor of Business Administration/", re.IGNORECASE)
    bach_major_result = re.search(regular_expression, resume_file)
    regular_expression_two = re.compile(r"minor|Minor", re.IGNORECASE)
    minor_result = re.search(regular_expression_two, resume_file)
    regular_expression_three = re.compile(r"Master|master", re.IGNORECASE)
    master_major_result = re.search(regular_expression_three, resume_file)
    regular_expression_four = re.compile(r"university", re.IGNORECASE)
    university_major_result = re.search(regular_expression_four, resume_file)
    updated_majors1 = []
    indexes_majors1 = []
    updated_majors2 = []
    indexes_majors2 = []
    updated_majors3 = []
    indexes_majors3 = []
    updated_majors4 = []
    indexes_majors4 = []
    university_df1 = pandas.read_excel(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','China_University.xlsx')))
    university_df2 = pandas.read_excel(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','India_University.xlsx')))
    university_df3 = pandas.read_excel(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','US_University.xlsx')))
    university_file1 = university_df1['Universities'].values
    university_file2 = university_df2['Universities'].values
    university_file3 = university_df3['Universities'].values
    university_lower1 = [item.lower() for item in university_file1]
    university_lower2 = [item.lower() for item in university_file2]
    university_lower3 = [item.lower() for item in university_file3]
    university_combined = university_lower1 + university_lower2 + university_lower3
    get_majors(resume_token2, major_lower)
    get_majors2(resume_token2, major_lower,major_distinct)
    get_majors_index(major_distinct,resume_file2,dictionary)
    get_bach_index(bach_major_result,resume_file)
    get_minor_index(minor_result,resume_file)
    get_master_index(master_major_result,resume_file)
    get_university_index(university_major_result,resume_file)
    print('BACH: ',get_bach_major(dictionary,resume_file,bach_major_result,updated_majors1,indexes_majors1))
    print('MASTER: ',get_master_major(dictionary,resume_file,master_major_result,updated_majors2,indexes_majors2))
    print('MINOR: ',get_minor(dictionary,resume_file,minor_result,updated_majors3,indexes_majors3))
    print('What is this: ',get_university_major(dictionary,resume_file,university_major_result,updated_majors4,indexes_majors4))
    print('UNI: ',extract_university(resume_token2,university_combined))
    print('GPA: ',extract_GPA(resume_file))
    schools = []
    school = {}
    school_info = {}
    major_info = {}
    school_info['name'] = extract_university(resume_token2,university_combined)
    school_info['degreeLevel'] = 'Undergraduate'
    school['school'] = school_info
    school['gradDate'] = 'Jan 2012'
    GPA = extract_GPA(resume_file)
    if GPA != None:
        school['GPA'] = GPA
    else:
        school['GPA'] = 0

    major_info['major'] = get_university_major(dictionary,resume_file,university_major_result,updated_majors4,indexes_majors4)
    major_info['dept'] = '?'
    major_info['major/minor'] = 'Major'
    school['major'] = major_info
    schools.append(school)
    print('SCHOOL:  ',schools)

    return schools
#major, University, gpa
def get_bigrams(input):
    n = 2
    result = []
    bigrams = ngrams(input, n)
    for grams in bigrams:
        x = "%s %s" % grams
        result.append(x)
    return (result)


def get_threegrams(input):
    n = 3
    result = []
    threegrams = ngrams(input, n)
    for grams in threegrams:
        x = "%s %s %s" % grams
        result.append(x)
    return (result)

def get_fourgrams(input):
    n = 4
    result = []
    fourgrams = ngrams(input, n)
    for grams in fourgrams:
        x = "%s %s %s %s" % grams
        result.append(x)
    return (result)

def get_fivegrams(input):
    n = 5
    result = []
    fivegrams = ngrams(input, n)
    for grams in fivegrams:
        x = "%s %s %s %s %s" % grams
        result.append(x)
    return (result)

def get_sixgrams(input):
    n = 6
    result = []
    sixgrams = ngrams(input, n)
    for grams in sixgrams:
        x = "%s %s %s %s %s %s" % grams
        result.append(x)
    return (result)

def get_majors(a,b):
    majors=[]
    for x in a:
        if x in b:
            majors.append(x)
    return (majors)

def get_majors2(a,b,major_distinct):
    unigram_major = get_majors(a, b)
    bigram_major = get_majors(get_bigrams(a), b)
    threegram_major = get_majors(get_threegrams(a), b)
    combined_majors_list = unigram_major + bigram_major + threegram_major
    for i in combined_majors_list:
        if i not in major_distinct:
            major_distinct.append(i)
    return(major_distinct)

def get_majors_index(major_distinct,resume_file2,dictionary):
    for i, element in enumerate(major_distinct):
        x = resume_file2.find(element)
        dictionary[element] = x
    del dictionary['Name']
    return dictionary

def get_bach_index(bach_major_result,resume_file):
    if bach_major_result:
        bach_major_result = bach_major_result.group()
    if bach_major_result is not None:
        bach_major_index = resume_file.find(bach_major_result)
        return(bach_major_index)
    else:
        return 0

def get_minor_index(minor_result,resume_file):
   if minor_result:
       minor_result = minor_result.group()
   if minor_result is not None:
       minor_index = resume_file.find(minor_result)
   else:
       minor_index = 0
   return(minor_index)

def get_master_index(master_major_result,resume_file):
    if master_major_result:
        master_major_result = master_major_result.group()
    if master_major_result is not None:
        master_major_index = resume_file.find(master_major_result)
        return(master_major_index)
    else:
        return 0

def get_university_index(university_major_result,resume_file):
    if university_major_result:
        university_major_result = university_major_result.group()
    if university_major_result is not None:
        university_major_index = resume_file.find(university_major_result)
        return(university_major_index)
    else:
        return 0

def get_bach_major(dictionary,resume_file,bach_major_result,updated_majors1,indexes_majors1):
    bach_major_index = get_bach_index(bach_major_result,resume_file) - 100
    upper_bound = bach_major_index + 100
    for k, v in dictionary.items():
        if (bach_major_index < v < upper_bound):
            updated_majors1.append(k)
            indexes_majors1.append(v)
    return updated_majors1

def get_master_major(dictionary,resume_file,master_major_result,updated_majors2,indexes_majors2):
    master_major_index = get_master_index(master_major_result,resume_file)
    if master_major_index == 0:
        return []
    upper_bound = master_major_index +100
    for k, v in dictionary.items():
        if (master_major_index < v < upper_bound):
            updated_majors2.append(k)
            indexes_majors2.append(v)
    return updated_majors2
def get_minor(dictionary,resume_file,minor_result,updated_majors3,indexes_majors3):
    minor_index = get_minor_index(minor_result,resume_file)
    upper_bound = minor_index +100
    for k, v in dictionary.items():
        if (minor_index < v < upper_bound):
            updated_majors3.append(k)
            indexes_majors3.append(v)
    return updated_majors3

def get_university_major(dictionary,resume_file,university_major_result,updated_majors4,indexes_majors4):
    university_major_index = get_university_index(university_major_result,resume_file)
    if university_major_index == 0:
        return []
    upper_bound = university_major_index +100
    for k, v in dictionary.items():
        if (university_major_index < v < upper_bound):
            updated_majors4.append(k)
            indexes_majors4.append(v)
    return updated_majors4



def extract_major(majors_minors_all):
    majors_minors_all = updated_majors1 + updated_majors2 + updated_majors3 + updated_majors4
    majors_minors_final_list = list(dedupe(majors_minors_all))
    return (majors_minors_final_list)


#extract University:
def get_university(a,b):
    resume_university=[]
    for x in a:
        if x in b:
            resume_university.append(x)
    return (resume_university)

def extract_university(resume_token_lower,university_combined):
    unigram_university = get_university(resume_token_lower, university_combined)
    bigram_university = get_university(get_bigrams(resume_token_lower), university_combined)
    threegram_university = get_university(get_threegrams(resume_token_lower), university_combined)
    fourgram_university = get_university(get_fourgrams(resume_token_lower), university_combined)
    fivegram_university = get_university(get_fivegrams(resume_token_lower), university_combined)
    sixgram_university = get_university(get_sixgrams(resume_token_lower), university_combined)
    combined_university_extraction = list(bigram_university + threegram_university + fourgram_university + fivegram_university + sixgram_university)
    print('UNI: ', bigram_university,threegram_university,fourgram_university)
    return combined_university_extraction

#execution of extracting university:

#extract GPA:
def extract_GPA(resume):
    result = re.search(r'(GPA|gpa):( ?\d.\d{1,})',resume)
    if result:
        result = result.group(2)
        result = float(result)
    return (result)

#execution of extracting GPA:


#HENRY

#Extracting Address


#extract the address
def extract_address (text):
    text = text.replace('\n', ' ')
    regex = re.compile(r"[0-9]+ .*[.,-]? .*[.,-]? ([A-Z]{2}|\w+)[.,-]? [0-9]{5}(-[0-9]{4})?")
    result = re.search(regex, text)
    if result:
        result = result.group()
    return result

#Parse the address components
def parse_address(result):
    address = usaddress.tag(result)
    return address

#2. Extracting Company

import codecs
import itertools
import os
import pandas as pd
from fuzzywuzzy.process import dedupe
import spacy
from nltk.corpus import stopwords


def extract_company(resume):

#Read the Work_Experience_List
    data = pd.read_excel(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing',"Work Experience.xlsx")), header=0)
    experience_list = list(data['Example'])
    exp_header = find_exp_header(resume,experience_list)
    exp_header = (exp_header[0], resume.find(exp_header[0]))
    next_section = find_next_section(resume,exp_header)
    workexp_section = get_workexp_section(resume,next_section,exp_header)
    workexp_section = workexp_section.split('\n')
    company_info = get_exp_info(workexp_section)
    #Print the company info
    for i, company in enumerate(company_info):
        company = company.replace('\t', '')
        print('\nCompany {}:'.format(i+1), company)

    nlp = spacy.load('en')
    print('COMPANY: ',extract_exp_info(company_info))
    comp = extract_exp_info(company_info)
    if comp == None:
        return []
    else:
        return comp

#Find the experience header
def find_exp_header (resume,experience_list):
    exp_header_list=[]
    for word in experience_list:
        if resume.find(word) != -1:
            exp_header_list.append(word)

    #remove duplicates of experience header
    exp_header = list(dedupe(exp_header_list))
    return exp_header



#Find next section header
def find_next_section (resume,exp_header):
    #Find all capitalized words
    next_section_upper = re.findall(r'([A-Z]{3,}( [A-Z]+)?( [A-Z]+)?( [A-Z]+)?)',
                                   resume[(exp_header[1] + len(exp_header[0])+ 1):])
    next_section_upper = list((itertools.chain.from_iterable(next_section_upper)))

    #Find all words with the first letter capitalized
    next_section_lower = re.findall(r'([A-Z]{1}\w+( [A-Z]{1}\w+)?( [A-Z]{1}\w+)?( [A-Z]{1}\w+)?)',
                                    resume[(exp_header[1] + len(exp_header[0])+ 1):])
    next_section_lower = list((itertools.chain.from_iterable(next_section_lower)))

    #Combine into a list
    next_section_list = next_section_upper + next_section_lower

    #if one of the items matches items in section list, that item is the next section header
    next_section = (0,0)
    for item in next_section_list:
        if item in next_section_list and (resume[resume.find(item)+len(item)]=='\n' or resume[resume.find(item)-1]=='\n'):
            next_section = (item, resume.find(item))
            break
    return next_section


# Get the section of Work_Experience
def get_workexp_section(resume,next_section,exp_header):
    if next_section:
        workexp_section = str(resume[(exp_header[1]+ len(exp_header[0])+ 1):next_section[1]])
    else:
        workexp_section = str(resume[(exp_header[1]+ len(exp_header[0])+ 1):])
    return workexp_section



#Remove the detail and get the experience information
def get_exp_info(work_exp):
    company_info=[]
    temp_str=''
    for i, sent in enumerate(work_exp):
        if sent != '':
            #Everything before the bullet will be put into one sentence, for one company
            if not sent.startswith(('•','', u'\uf095', '§', '§','○')):
                temp_str += sent + ' '
            else:
                if not work_exp[i-1].startswith(('•','', u'\uf095', '§', '§','○')):
                    company_info.append(temp_str)
                    temp_str=''
    return company_info



#Parse company info components
def extract_exp_info(company_info):
    count = 0
    for i, sent in enumerate(company_info):
        sent = sent.replace('\t', '')
        parsed_sent = nlp(sent)
        print('\nCompany {}'.format(i+1))

        company=''
        location=''
        time=''
        role=''
        for i ,token in enumerate(parsed_sent):
            if token.ent_type_ =='ORG':
                company += ' ' + str(token)
            elif token.ent_type_ =='GPE':
                location += ' ' + str(token)
            elif token.ent_type_ =='DATE' or token.ent_type_ =='TIME':
                time += ' ' + str(token)
            elif token.ent_type_ =='':
                if str(token).isalpha() and str(token) not in stopwords.words('english'):
                    role += ' ' + str(token)
        company_info  = {}
        company_info['company'] = company
        company_info['title'] = role
        company_info['startDate'] = time
        company_info['endDate'] = '2000-01-01'
        company_info['experience'] = ''
        company_info['summary'] = ''
        return company_info


#3. Extract Skills (Just Skills)
def extract_all_skills(resume):
    #Read the Skill_List.xlsx

    data = pd.read_excel(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing',"Skills.xlsx")), header=0)
    skill_list = list(data['Skill Names'])
    skill_list = set(skill_list)
    skill_list= [skill.lower() for skill in skill_list]

    filename ='all_text1.txt'
    trained_resume_path = os.path.join('Trained Resumes', filename)

    resume_text = resume
    special_characters = ['!','#', '$', '%','&','*','-', '/', '=','?',
                          '^','.','_','`', '{', '|', '}','~', "'", ',', '(',')', ':', '•', '§' ]
    unigram_resume = resume_processing(resume_text,special_characters)
    print('time1')
    #Create bigram model
    bigram_resume = create_bigram(unigram_resume)
    #Create trigram model
    trigram_resume = create_trigram(bigram_resume)
    normalized_resume = normalize_words(trigram_resume)
    labeled_words=[labeled_word(sentence,skill_list) for sentence in normalized_resume]
    featuresets=[]
    for labeled_sent in labeled_words:
        unlabeled_sent = [word[0] for word in labeled_sent]
        for i, (w, label) in enumerate(labeled_sent):
            featuresets.append((extract_features(unlabeled_sent, i,skill_list), label))
    print('time2')

    size = int(len(featuresets)*0.1)
    train_set = featuresets[size:]
    test_set = featuresets[:size]

    #Train the data with NaiveBayes model
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    #Evaluate the accuracy
    nltk.classify.accuracy(classifier, test_set)
    skills =[]
    for sent in normalized_resume:
        for (i,_) in enumerate(sent):
            if classifier.classify(extract_features(sent, i,skill_list))=='skill':
                skills.append(sent[i])
                extracted_skills = set(skills)
    #print('Resume ',len(extracted_skills),'Skills: ', extracted_skills)
    all_skills = []

    for skills in extracted_skills:
        skill_dict = {}
        skill_dict['skill'] = skills
        skill_dict['YearsOfExperience'] = 0
        all_skills.append(skill_dict)
    return all_skills
# Processing text
def resume_processing (resume_text,special_characters):
    #tokenize sentences
    resume_sents = nltk.sent_tokenize(resume_text)

    #tokenize words
    resume_words = [nltk.word_tokenize(sent) for sent in resume_sents]

    #remove stopwords and special characters
    processed_resume=[]
    for sentence in resume_words:
        sent = [w.lower() for w in sentence
                          if w.lower() not in stopwords.words('english') and w.lower() not in special_characters]
        processed_resume.append(sent)

    return processed_resume



# Create bigram words
def create_bigram (unigram_resume):
    bigram_model = Phrases.load(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','bigram_model')))
    #bigram_model.add_vocab(unigram_resume)
    bigram_resume = [bigram_model[sentence] for sentence in unigram_resume]
    return bigram_resume



# Create trigram words
def create_trigram (bigram_resume):
    trigram_model = Phrases.load(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','trigram_model')))
    #trigram_model.add_vocab(bigram_resume)
    trigram_resume = [trigram_model[sentence] for sentence in bigram_resume]
    return trigram_resume


#Normalize bigram/trigram words
def normalize_words (trigram_resume):
    for sentence in trigram_resume:
        for i, word in enumerate(sentence):
            if len(re.findall(r'\w+\_\w+', word))!= 0:
                sentence[i] = re.sub('_', ' ', word)
    return trigram_resume


#label skills in the resume
def labeled_word (sentence,skill_list):
    labels=[]
    for word in sentence:
        if word in skill_list:
            labels.append((word, 'skill'))
        else:
            labels.append((word, 'not skill'))
    return labels


#Get 25 similar words based on word2vec model
def similar_prob(word,res2vec,skill_series):
    count = 0
    terms = get_related_terms(word,25,res2vec)
    for w in terms:
        if w in skill_series:
            count+=1
    return count/25

#Check if the word is in skill clusters, based on KMeans algorithm
def in_skill_cluster(word,skills):
    if word in skills:
        return True
    return False

def get_related_terms(token,topn,res2vec):
    arr =[]
    for word,similar in res2vec.wv.most_similar(positive = [token],topn=topn):
        #print(word,':',round(similar,3))
        arr.append(word)
    return arr
#extract featurres of skills
def extract_features (sentence, i,skill_list):
    res2vec = Word2Vec.load(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','vector_models')))
    res2vec.init_sims()
    features={}
    #first feature: evaluate if that word is in skill list
    features["({})in_skill_list".format(sentence[i])]= (sentence[i] in skill_list)

    if sentence[i] in res2vec.wv.vocab:
        features["probality_of_similar_words_skills"] = similar_prob(sentence[i],res2vec,skill_list)
        features["in_skill_cluster"] = in_skill_cluster(sentence[i],skill_list)

    #if the word is in begining of the sentence, return <Start> for prev_word
    if i==0 and len(sentence)-1 != 0:
        features["prev_word_in_skill_list"]= '<Start>'
        features["next_word_in_skill_list"]= (sentence[i+1] in skill_list)

    #if the word is in begining of the sentence, return <End> for next_word
    elif i == len(sentence)-1 and  i != 0:
        features["prev_word_in_skill_list"]= (sentence[i-1] in skill_list)
        features["next_word_in_skill_list"]= '<End>'

    #if the sentence has only 1 word, return False for both prev_word and next_word
    elif i==0 and len(sentence)-1 == 0:
        features["prev_word_in_skill_list"]= False
        features["next_word_in_skill_list"]= False
    else:
        features["prev_word_in_skill_list"]= (sentence[i-1] in skill_list)
        features["next_word_in_skill_list"]= (sentence[i+1] in skill_list)
    return features



#Extract the skills


#VAIBHAV

#Import Statements
import csv
import re

#Email Address (Finished)
def check_email(string_to_search):
    regular_expression = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,3}", re.IGNORECASE)
    result = re.search(regular_expression, string_to_search)
    if result:
        result = result.group()
    return result
    #except:
     #   result=0
      #  return result

#LinkedIn Address(Finished)
def check_linkedin(string_to_search):
    regular_expression1 = re.compile(r"https://"
                                    r"[A-Z]{2,3}"
                                    r".linkedin.com/in/"
                                    r"[-_a-z 0-9]{5,30}", re.IGNORECASE)
    result = re.search(regular_expression1, string_to_search)
    try:
        result = result.group()
        return result
    except:
        regular_expression1 = re.compile(r"[A-Z]{2,3}"
                                        r".linkedin.com/in/"
                                        r"[-_a-z 0-9]{5,30}", re.IGNORECASE)
        result = re.search(regular_expression1, string_to_search)
        try:
            result=result.group()
            return result
        except:
            regular_expression1 = re.compile(r"[A-Z]{2,3}"
                                        r".linkedin.com/"
                                        r"[-_a-z 0-9]{5,30}", re.IGNORECASE)
            result = re.search(regular_expression1, string_to_search)
            try:
                result=result.group()
                return result
            except:
                return ''

#GitHub Address (Finished)
def check_GitHub(string_to_search):
    regular_expression = re.compile(r"https://github.com/"
                                    r"[-_A-Z0-9]{5,30}", re.IGNORECASE)
    result = re.search(regular_expression, string_to_search)
    try:
        result = result.group()
        return result
    except:
        return ""

#Contact Number (Finished)
def check_phone_number(string_to_search):
    try:
        regular_expression = re.compile(r"\(?"  # open parenthesis
                                        r"(\d{3})?"  # area code
                                        r"\)?"  # close parenthesis
                                        r"[\s\.-]{0,2}?"  # area code, phone separator
                                        r"(\d{3})"  # 3 digit exchange
                                        r"[\s\.-]{0,2}"  # separator bbetween 3 digit exchange, 4 digit local
                                        r"(\d{4})",  # 4 digit local
                                        re.IGNORECASE)
        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.groups()
            result = "-".join(result)
        return result
    except:
        return 0000000000


#Ashish (LinkedIn Profiles and Every other URL in the file)

# import all headers
# function to extract all URLs
# implemented using regex
def extract_URLs(parsedResume):
    parsedResume = parsedResume.replace('\n', ' ')
    regex = regex = re.compile('(?:(?:https?|ftp|file)://|www\.|ftp\.)[-A-Z0-9+&@#/%=~_|$?!:,.]*[A-Z0-9+&@#/%=~_|$]', re.IGNORECASE)
    result = re.findall(regex, parsedResume)
    #if result:
        #result = result.group()
    return result

# function to extract LinkedIN Profile
# implemented using regex
def extract_linkedin(parsedResume):
    parsedResume = parsedResume.replace('\n', ' ')
    regex = re.compile(r"https://www.linkedin.com/in/([a-zA-Z]|[0-9]|[-])+/?")
    result = re.search(regex, parsedResume)
    if result:
        result = result.group()
    return result

# TESTING
# path where all resumes are located
