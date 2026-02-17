import pickle
import os 
import pypdf
import re
import neattext.functions as nfx
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import contractions
import unicodedata
import re
import nltk
from nltk.corpus import wordnet
import re
import nltk
import argparse
import csv
from gensim.summarization import keywords
from collections import Counter

os.chdir('d:\Rohan\Dhrima\PROJECT\project3-main (1)\project3-main')

with open('model.pkl', "rb") as f:
    tfidf = pickle.load(f)
    model = pickle.load(f)
    

def file_read(path):
    pdf = pypdf.PdfReader(path)
    text2 = ''
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text2 = text2 + page.extract_text().strip()

    return text2

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def expand_contractions(text):
    # creating an empty list
    expanded_words = []   
    for word in text.split():
      # using contractions.fix to expand the shortened words
      expanded_words.append(contractions.fix(word))  

    expanded_text = ' '.join(expanded_words)
    return expanded_text

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def pre_process(text):
    # Remove links
    text = re.sub('http://\S+|https://\S+', '', text)
    text = re.sub('http[s]?://\S+', '', text)
    text = re.sub(r"http\S+", "", text)
 
    # Convert HTML references
    text = re.sub('&amp', 'and', text)
    text = re.sub('&lt', '<', text)
    text = re.sub('&gt', '>', text)

    # Remove new line characters
    text = re.sub('[\r\n]+', ' ', text)
    
    # Remove mentions
    text = re.sub(r'@\w*', '', text)
    
    # Remove hashtags
    text = re.sub(r'#\w*', '', text)

    # Remove multiple space characters
    text = re.sub('\s+',' ', text)
    
    # Convert to lowercase
    text = text.lower()
    

    # Apply NeatText functions
    text = nfx.remove_emojis(text)
    text = nfx.remove_numbers(text)
    text = nfx.remove_emails(text)
    text = nfx.remove_stopwords(text)
    text = nfx.remove_puncts(text)
    text = nfx.remove_userhandles(text)
    text = nfx.remove_accents(text)
    text = nfx.remove_accents(text)
    text = nfx.remove_special_characters(text)

    return text

def remove_repeated_characters(tokens):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'
    def replace(old_word):
        if wordnet.synsets(old_word):
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word
            
    correct_tokens = [replace(word) for word in tokens]
    
    return correct_tokens

def clean_title(city):
    city = city.replace('.\\smartcity','').replace('.pdf','').replace('\\','')
    return city

def keys(text, ratio=0.01):
    return keywords(text, ratio=ratio).replace('\n',' ')

def summarize_text(text):
    # tokenize the text into individual words
    words = nltk.word_tokenize(text)

    # remove stop words such as 'a', 'the', 'is', etc.
    stopwords = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word.lower() not in stopwords]

    # count the frequency of each word
    word_freq = Counter(words)

    # get the 5 most common words and phrases
    summary = [word for word, _ in word_freq.most_common(100)]

    # join the summary words into a single sentence
    summary = ' '.join(summary)

    return summary

def append_data(city,raw_text,cleaned_text,cluster_id,summary,keywords):
        
    # Define the row of data to append
    new_row = [city,raw_text,cleaned_text,cluster_id[0],summary,keywords]

    # Open the TSV file in append mode and write the new row of data
    with open('smartcity_predict.tsv', mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(new_row)

    return 'data added successfully'

def main(pdfname,summary,keywords):

    #extracting the text from the file
    text = file_read(pdfname)
    raw_text = text

    #cleaning the text
    text = remove_accented_chars(text)
    text = expand_contractions(text)
    text = remove_special_characters(text)
    text = pre_process(text)
    
    correct_tokens = remove_repeated_characters(nltk.word_tokenize(text))
    cleaned_text =' '.join(correct_tokens)

    #transforming
    X = tfidf.transform([cleaned_text])

    #prediction
    cluster_id = model.predict(X)
        
    city = clean_title(pdfname)

    #append data to tsv file
    append_data(city,raw_text,cleaned_text,cluster_id,summary,keywords)

    
    print('[{}]'.format(city) +' ' +'cluster id: {}'.format(cluster_id[0]))
    print('[{}]'.format(city) + ' ' + 'summary: {}'.format(summary))
    print('[{}]'.format(city) + ' '+ 'keywords: {}'.format(keywords))
    return cluster_id[0]


if __name__ == '__main__':
    parser  = argparse.ArgumentParser(description='project3')

    parser.add_argument('--document', type=str, help='path to pdf file')
    parser.add_argument('--summary', nargs='?',type=str, help='summary of the pdf',default=' ')
    parser.add_argument('--keywords', nargs='?',type=str, help='keywords of the pdf',default=' ')

    args = parser.parse_args()

    main(args.document,args.summary,args.keywords)






