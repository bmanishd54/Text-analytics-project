# cs5293sp23-project3
Template repo for Project 3

`smartcity/`  - contains the pdf applications \
`project3.ipynb` - template notebook to follow for Project3

Please change this README.md as needed.


Name : Payel Sujon

project3.py
The project3.py is used for predicting the cluster of the new city provided by the user. it predicts the cluster of the new city based on the model trained in the project3.ipynb file using pickle file.

To run the program you simple need to write the following script on the command line

pipenv run python3.py 'path to the pdf' 'summary' 'keywords'

Here, the path is the require argument whereas the other two arguments are optional. the predicted output is appended into the smartcity_predict.tsv file.

Demo video of how to run the project3.py file.


Video Link
https://github.com/Rohan19072/project3/assets/84516953/977b4951-f208-44a0-99b6-a8a8b7e12d3c




Functions used in the project3.py file:

file_read(path) : 
This function is used to read the text from the pdf. it will extract all the text from the pdf and return it.

Functions used for preprocessing and cleaning the text
remove_accented_characters(text) :
this funciton will remove the characters from the text  and return it.

expand_contractions(text):
this funciton will expand the short contractions of the words in the text.

remove_special_characters(text):
this funciton will remove the special characters from the text and return it.

pre_process(text):
this funciton will do some basic preprocessing of the text like removing stopwords removing extra spaces, numbers, emails, links, punctuation marks etc.

remove_repeated_characters(text):
this funciton will remove the repeated characters of the words.

clean_title(city):
this funciton will clean the title of the pdf and return as city name for the tsv file.

append_data(pdfname,raw_text,cleaned_text,cluster_id,summary,keywords):
this function will append all the data to the smartcity_predict.tsv file.

main():pdfname,summary,keywords):
this is the main function which will be called when the script is executed it will extract all the data from the pdf file mentioned, preprocess it and then append it to the smartcity_predict.tsv.
