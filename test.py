import pypdf
import re
import neattext.functions as nfx

def file_read(path):
    pdf = pypdf.PdfReader(path)
    text2 = ''
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text2 = text2 + page.extract_text().strip()

    return text2

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