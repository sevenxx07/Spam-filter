from corpus import Corpus
from trainingcorpus import TrainingCorpus
import email
 
 
SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'
STOP_WORDS = [
         "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
         "yours", "yourself", "yourselves", "he", "him", "his", "himself",
         "she", "her", "hers", "herself", "it", "its", "itself", "they", 
         "them", "their", "theirs", "themselves", "what", "which", "who",
         "whom", "this", "that", "these", "those", "am", "is", "are", "was",
         "were", "be", "been", "being", "have", "has", "had", "having", "do",
         "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or",
         "because", "as", "until", "while", "of", "at", "by", "for", "with",
         "about", "against", "between", "into", "through", "during","before",
         "after", "above", "below", "to", "from", "up", "down", "in", "out",
         "on", "off", "over", "under", "again", "further","then", "once",
         "here", "there", "when", "where", "why", "how", "all", "any", "both",
         "each", "few", "more", "most", "other", "some","such", "no", "nor",
         "not", "only", "own", "same", "so", "than", "too", "very", "can",
         "will", "just", "don't", "should", "now", "also", "however", "sure", 
         "able", "us", "even", "jpg", "img", "across", "already", "although", 
         "anything", "i'd", "i'll", "i'm", "i've", "she'd", "she'll", "she's", 
         "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", 
         "we've", "what's", 'when', "when's", 'where', "where's", "you'd", 
         "you'll", "you're", "you've", "isn", "isn't", "it", "it's", "its",
         "he'd", "he'll", "he's", "here's", "how's","research-articl",
         "pagecount", "cit", "ibid", "les", "que", "est", "pas", "vol",
          "los", "volumtype", "par"
         ]
 
 
class MyFilter:
    
   def __init__(self):
      self.ham_pred = {} #dictionary of probability of each word we found in ham email
      self.spam_pred = {} #dictionary of probability of each word we found in spam email
      self.train_guard = 0 #variable checking if def train was running
 
      # the percents was made by ourself and depends on our analysis
      self.pct_of_upper_case_subject = 10
      self.pct_of_digits_subject = 31
      self.pct_of_sign_subject = 31
      self.pct_of_upper_case_body = 10
      self.pct_of_digits_body = 20
      self.pct_of_sign_body = 35
      self.pct_HTML_tags_to_sentences = 10
       
 
   def train(self, train_corpus_dir):
      """Filter is learning on given dataset - Naive Bayes spam filtering"""
      self.train_guard = 1
      #creating two corpuses:
      #one for creating training corpus because of method get_class()
      #other for walking through all emails with method emails() from corpus.py
      c1 = TrainingCorpus(train_corpus_dir) 
      c2 = Corpus(train_corpus_dir)
      self.black_list = self.load_data_from_black_file()
 
      for filename, email_body in c2.emails():
         tag = c1.get_class(filename)
         body = self.split_email(email_body)
 
         #write down words and their frequencies from spam or ham in dictionaries
         if tag == 'OK':
            for word in body:
               if word in self.ham_pred:
                  self.ham_pred[word] += 1
               else:
                  self.ham_pred[word] = 2 #for words that are not in this dictionary is the frequency 1
         else:
            # adding SPAM address to black list
            if self.address_from not in self.black_list:
               self.black_list.append(self.address_from)
 
            for word in body:
               if word in self.spam_pred:
                  self.spam_pred[word] += 1
               else:
                  self.spam_pred[word] = 2
 
      self.upload_data_to_black_file()
 
      #removing word with lower frequency than 5
      ham_prediction = {}
      spam_prediction = {}
      for key in self.ham_pred:
         if self.ham_pred[key] > 5:
            ham_prediction[key] = self.ham_pred[key]
       
      for key in self.spam_pred:
         if self.spam_pred[key] > 5:
            spam_prediction[key] = self.spam_pred[key]
 
      self.ham_pred = ham_prediction
      self.spam_pred = spam_prediction
 
      #computing the probability of each word
      for key in self.ham_pred:
         self.ham_pred[key] = self.ham_pred[key]/len(self.ham_pred)
      for key in self.spam_pred:
         self.spam_pred[key] = self.spam_pred[key]/len(self.spam_pred)
 
 
   def classify(self, email_body):
      """Decide if this email is SPAM/OK"""
 
      # each method return probability of SPAM
      # the probability was made by ourself and depends on our analysis
      # after adding all probabilities we will decide if this email is SPAM/OK
      probability = 0
 
      if self.train_guard == 1:
         probability += self.classify_naive_bayes(email_body)
 
      probability += self.classify_black_list()
      probability += self.classify_amount_chars()
      probability += self.classify_HTML_tags_to_sentences()
 
      if probability >= 1/2:
         return SPAM_TAG
      else:
         return HAM_TAG
 
          
   def test(self, test_corpus_dir):
      """Test filter and make file of predictions"""
      self.black_list = self.load_data_from_black_file()
      predictions = {}
      c = Corpus(test_corpus_dir)
       
      for filename, email_body in c.emails():
         body = self.split_email(email_body)
         my_prediction = self.classify(body)
         predictions[filename] = my_prediction
       
      self.make_file_of_predictions(predictions, test_corpus_dir)
 
 
   def split_email(self, email_body):
      """ Split email to subject, address, time, cc and body.
         Return list(body)"""
      self.count_HTML_tags = 0
      self.count_sentences = 0
      email_msg = email.message_from_string(email_body)
 
      subject = email_msg.get('Subject')
      if subject == None or len(subject) == 0:
         subject = "none"
      self.subject = self.clear_text(subject.split(), 1)
       
      address = email_msg.get('From').replace(">"," ").replace("<"," ").replace('"'," ").split()
      for word in address:
         if '@' in word:
            self.address_from = word.casefold()
 
      # define the body of email
      # we agreed, that all after empty line will be the body
      read = self.my_split(email_body)
      for line in read:
         if line == '':
            index = read.index(line)
            body = read[index:-1]
            self.count_sentences = len(body)
            break
 
      body = self.clear_text(body)
 
      return body
 
 
   def clear_text(self, text, is_subject = 0):
      """Clearing the text. Remove unnecessary words.
         Return list(content)"""
      content = []
 
      for j in range(len(text)):
         string = text[j]
         if string.startswith('\t'):
            string = string[1:]
 
         new_string = self.delete_HTML_code(string) 
 
         for word in new_string:
            if len(word) != 0:
               content.append(word)
 
      # all strings convert to lower cases
      for i in range (len(content)):
         content[i] = content[i].casefold()
 
      list_signs = self.count_signs(content, is_subject)
      # replace all signs to space and after split()
      for i in range(len(content)):
         for j in range(len(content[i])):
            if content[i][j] in list_signs:
               content[i] = content[i].replace(content[i][j], ' ')
       
      # make from list(content) to str(content)
      content = " ".join(content)
      content = content.split()
 
      #removing words containig numbers and words with length 1 or 2
      k = len(content)
      while(k >= 1):
         k -= 1
         for elem in content[k]:
            if elem.isdigit():
               content.pop(k)
               break
            if len(content[k]) == 1 or len(content[k]) == 2:
               content.pop(k)
               break
 
      # remove stop words in content
      content = list({word for word in content if word not in STOP_WORDS})
 
      return content
 
 
   def my_split(self, text):
      """Special split by '\n' """
      # We made this function
      # because we had problems with HTML tags and split('\n') at the same time
      text = text.replace("\n", "|")
      text = list(text)
      # -1 means that tag has not found yet
      tag_start = -1
      tag_end = 0
      index = 0
 
      for char in text:
         if char == '<':
            tag_start = index
            tag_end = -1
         if char == '>':
            tag_end = index
         # use "|" because we have replaced "\n"
         if char == "|":
            if tag_end == -1:
               text[index] = " "
         index += 1
 
      text = ''.join(text)
      text = text.split("|")
 
      return text
 
 
   def delete_HTML_code(self, string):
      """Remove HTML tags. Return list(new_string)"""
      txt = []
      start=[]
      end=[]
 
      for i in range (len(string)):
         if string[i] == '<': 
            start.append(i)
            for j in range(i, len(string)):
               if string[j] == '>':
                  end.append(j)
                  break
            if end == [] or len(start) != len(end):
               start.pop()
 
      # we must reverse indexes in lists and 
      # after we will remove HTML tags from higher to lower indexes
      # otherwise we will get an IndexError: index out of range
      start.reverse()
      end.reverse()
 
      for i in range (len(start)):
         self.count_HTML_tags += 1
         delete = string[start[i]:end[i]+1]
         string = string.replace(delete, "", 1)
 
      HTML_entities = { 
            " ": ' ',
            """: '"',
            "!": '!',
            "#": '#',
            "$": '$',
            "%": '%',
            "&": '&',
            "'": "'",
            "(": '(',
            ")": ')',
            "*": '*',
            "%": '%',
            "+": '+',
            ",": ",",
            ".": '.',
            "/": '/',
            "€": '€',
            ":": ':',
            ";": ';',
            "<": '<',
            "=": '=',
            ">": '>',
            "?": '?',
            "@": '@',
            "[": '[',
            "]": ']',
            "|": '|',
            "&lcub": '{',
            "}": '}',
            "£": '£',
            "¢ ": '¢',
            "§": '§',
            "©": '©',
            "±": '±',
            "²": '²',
            "³": '³',
            "½": '½'
      }
      for key in HTML_entities:
         if key in string:
            string = string.replace(key, HTML_entities[key])
      txt.append(string)
       
      # from list(txt) to str(txt) and after use split()
      txt = ''.join(txt)
      txt = txt.split()
 
      return txt
    
 
   def count_signs(self, text, is_subject):
      """Count signs are in the dict(self.count_chars). Return list_signs"""
      count_chars = {
         "all": 0,
         "upper_case": 0,
         "lower_case": 0,
         "digits": 0,
         "sign": 0
      }
      list_signs = []
      for word in text:
         for char in word:
            count_chars["all"] += 1
            if char.isalnum():
               if char.isdigit():
                  count_chars["digits"] += 1
               elif char.isupper():
                  count_chars["upper_case"] += 1
               elif char.islower():
                  count_chars["lower_case"] += 1
            else:
               count_chars["sign"] += 1
               if char not in list_signs and char != "'": # exception " ' "
                  list_signs.append(char)
       
      if is_subject:
         self.count_chars_subject = count_chars
      else:
         self.count_chars_body = count_chars
 
      return list_signs
 
 
   def classify_amount_chars(self):
      ret = 0
 
      # decision for Subject
      percent_of_upper_case = round((self.count_chars_subject["upper_case"] 
                                      / self.count_chars_subject["all"]) * 100)
      percent_of_digits = round((self.count_chars_subject["digits"]
                                      / self.count_chars_subject["all"]) * 100)
      percent_of_sign = round((self.count_chars_subject["sign"] 
                                      / self.count_chars_subject["all"]) * 100)
 
      if percent_of_upper_case >= self.pct_of_upper_case_subject:
         ret += 2/6
      if percent_of_digits >= self.pct_of_digits_subject:
         ret += 2/6
      if percent_of_sign >= self.pct_of_sign_subject:
         ret += 2/6
 
      # decision for Body
      if self.count_chars_body["all"] == 0:
         return 1 # email is empty, therefore email is SPAM
 
      percent_of_upper_case = round((self.count_chars_body["upper_case"] 
                                         / self.count_chars_body["all"]) * 100)
      percent_of_digits = round((self.count_chars_body["digits"] 
                                         / self.count_chars_body["all"]) * 100)
      percent_of_sign = round((self.count_chars_body["sign"] 
                                         / self.count_chars_body["all"]) * 100)
       
      if percent_of_upper_case >= self.pct_of_upper_case_body:
         ret += 1/6
      if percent_of_digits >= self.pct_of_digits_body:
         ret += 1/6
      if percent_of_sign >= self.pct_of_sign_body:
         ret += 1/6
 
      return ret
 
 
   def classify_black_list(self):
      if self.address_from in self.black_list:
         return 1
      else:
         return 0
 
 
   def classify_HTML_tags_to_sentences(self):
      if self.count_sentences == 0:
         return 1 # email is empty, therefore email is SPAM
 
      percent = round((self.count_HTML_tags / self.count_sentences) * 100)
      if percent > self.pct_HTML_tags_to_sentences:
         return 2/6
      else:
         return 0
 
 
   def classify_naive_bayes(self, email_body):
      #constant of not used word in a dictionary of spam or ham - frequency is 1
      if len(self.spam_pred) == 0:
         constant_spam = 0
      else:
         constant_spam = 1/len(self.spam_pred)
      if len(self.ham_pred) == 0:
         constant_ham = 0
      else:
         constant_ham = 1/len(self.ham_pred) 
 
      result_ham = 1
      result_spam = 1
      result_multi_ham = 1
      result_multi_spam = 1
      #counting the probability that email is ham
      for word in email_body:
         if word in self.ham_pred:
            if word in self.spam_pred:
               prob_word_spam = self.spam_pred[word]
            else:
               prob_word_spam = constant_spam
            #naive bayes spamfiltering
            probability_of_word = self.ham_pred[word]/(self.ham_pred[word]+prob_word_spam)
                
            if probability_of_word != 0 or probability_of_word != 1:
               result_ham *= probability_of_word
               summary = 1 - probability_of_word
            result_multi_ham *= summary
      if result_multi_ham != 0 and result_ham != 0:
         result_ham = result_ham/(result_ham + result_multi_ham)
      else:
         result_ham = 1
 
      #counting the probability that email is spam
      for word in email_body:
         if word in self.spam_pred:
            if word in self.ham_pred:
               prob_word_ham = self.ham_pred[word]
            else:
               prob_word_ham = constant_ham
            probability_of_word = self.spam_pred[word]/(self.spam_pred[word]+prob_word_ham)
            if probability_of_word != 0 or probability_of_word != 1:
               result_spam *= probability_of_word
               summary = 1 - probability_of_word
            result_multi_spam *= summary
      if result_multi_spam != 0 and result_spam != 0:
         result_spam = result_spam/(result_spam + result_multi_spam)
      else:
         result_spam = 1
       
      if result_ham >= result_spam:
         return 0
      else:
         return 3/6
    
 
   def load_data_from_black_file(self):
      black_list = []
      with open("black_list.txt", 'r', encoding="utf-8") as black_file:
         read_bf = black_file.read().split()
      for adress in read_bf:
         black_list.append(adress)
 
      return black_list
 
    
   def upload_data_to_black_file(self):
      with open("black_list.txt", 'w', encoding="utf-8") as black_file:
         for word in self.black_list:
            black_file.write(word + "\n")
    
 
   def make_file_of_predictions(self, predictions, test_corpus_dir):
      with open(test_corpus_dir + '/' +"!prediction.txt", "w", encoding = "utf-8") as file:
         for key in predictions:
            string = str(key) + " " + str(predictions[key]) + "\n"
            file.write(string)
