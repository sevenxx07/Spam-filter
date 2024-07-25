# Formulation of the problem
The goal of this task is to program a functional spam filter. Its structure is to include
the test() method and the train() method. The interest is to create an algorithm that would
evaluate SPAM or HAM with the greatest possible accuracy. There are three possible strategy. 
Create a filter with only the test() method, which will have a simple tag determination algorithm
SPAM or HAM. Or go the route of a pre-learned filter. And the last option we are
we also chose is a learning filter with the train() method

# Implementation of the problem
First of all, I focused on cleaning emails from characters and parts that I don't need.
In the split_email() method, I separate the header from the body of the email, the subject and the address. The body then passes through
clear_text() and delete_HTML_code() and gets it into the form to parse.It strips it of the html code, converts all letters to lowercase, 
and replaces the signs with a space. Subsequently, it also deletes words containing a number, words that are one or twoletters long and
words from the so-called stop words that have no meaning in the text. The delete_HTML_code() method has a method
my_split() which solved our problem with identifying the html code in the text.
Since I chose to create a learning filter, I came up with an algorithm inspired by Naive Bayesian spam filtering. At the same time, 
I also analyzed the text as such and tried using methods derived from it to refine the basic algorithm. I combined together four methods, of which
each has some say in the final outcome based on the success of that method. 
* classify_black_list()
I created a file containing email addresses marked as spam from dataset 1 and 2. In the train method,I update this list.
* classify_amount_chars()
In the test() method, I also run count_signs() and count the number of upper and lower case letters, numbers and
signs. I also separate these properties for the subject and body of the email. Based on the analysis of emails from 1 and 2
dataset, I came up with the following data:
![obrazek](https://github.com/user-attachments/assets/9c9ca139-c25c-4151-aa49-570a54a00455)<br />
![obrazek](https://github.com/user-attachments/assets/230397ac-d151-426e-9a3b-2daa2b57c726)<br />
Based on those, I derived the percentages in the second line, which we then used in u email classification.
* Classify_HTML_tags_to_sentence()
The method uses further data analysis on the basis of which I again classify SPAM or HAM:
![obrazek](https://github.com/user-attachments/assets/47cec6ba-ccfb-4465-887d-aecd04bb2bec)
<br />
* Classify_naive_bayes()
This method is based on an algorithm that is similar to Naive Bayes spam filtering and is implemented in the train() method.
The train_guard variable watches if the train() method has been run and if therefore the classification can be used.
* train() method
There are created two word frequency dictionaries in spam and ham emails. Emails go through the split_email(),
clear_text() and delete_HTML_code() methods. After all emails are retrieved and there are deleted those words that appeared
five times or less in the emails to avoid inaccuracies in the algorithm due to rare words. Subsequently, probability of individual words
are calculated by dividing the frequency and the number of elements in the ham_pred or spam_pred dictionary.
In classify_naive_bayes, I go through the words in the email and calculate the probability that it is an email
SPAM or HAM. Therefore, the frequency of this word is set to 1 and from the beginning we set the initial frequency of the written words
in the train method to 2. The formula for calculating the probability of spam and ham:
![obrazek](https://github.com/user-attachments/assets/d9acdc45-3a50-44d8-bab0-165848f9c65a)
<br />
 &emsp; &emsp;Source:https://en.wikipedia.org/wiki/Naive_Bayes_spam_filtering
# Results of training
![obrazek](https://github.com/user-attachments/assets/f98e68ff-85ff-48a3-86a5-974b0f578962)
<br />
