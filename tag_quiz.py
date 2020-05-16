"""
A script for practicing Penn Treebank tagging, based on the real Penn Treebank!

The script uses the version of the Penn Treebank corpus that comes with the 
Natural Language Toolkit (NLTK). It pseudo-randomly selects sentences out of
the corpus and asks the user to tag those sentences. The user's responses are 
then compared to the tags in the corpus to assess how accurate the user is.

The user response should be entered as a string with each tag separated by a 
space. Evaluation of the user's response is case-insensitive. So, if the user 
is given the sentence:

    - The man saw me .

any of the following responses are acceptable:

    - DT NN VBD PRP .
    - dt nn vbd prp .
    - DT nN vbd PRp

Evaluations are given for each sentence, and a total score is given when all of
the sentences have been tagged. The default number of sentences to tag is five.
The average number of tokens per sentence in NLTK's Penn Treebank corpus is 
25.72, so the user can expect to see around 125 tokens (though this varies a 
lot depending on where in the corpus the sentences are drawn from).

The version of the Penn Treebank used by the NLTK assumes that 'to' is always
tagged 'TO', even when it's a preposition (so it is never tagged 'IN').

Further details on this tag set can be found at:
https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf
"""

# We'll use the NLTK treebank corpus:
from nltk.corpus import treebank

# We need this to get random sentences from the corpus:
from random import randint

# Makes the output a bit easier to read
from colorama import Fore, Style


# Give some feedback to the user
print("Loading Penn Treebank!")

# There are no tagged sentences in the NLTK version of
# the Penn Treebank, so we load the parsed sentences
# and convert them to tagged sentences as necessary.
parsed_sents = treebank.parsed_sents()

# Converting parsed sentences to tagged sentences
# takes a while, so we will only convert those that
# we need to convert later on below.


def get_sents(corpus, number = 5):
    """ 
    This function takes the given corpus and returns a specified
    number of contiguous sentences from a random position in 
    that corpus (default 5).
    """
    print("Gathering sentences")
    
    # Get the length of the corpus:
    length_corpus = len(corpus)
    
    # Select a random sentence in the corpus making sure
    # not to choose any values that will be out of range:
    start_point = randint(0, length_corpus - number)
    
    # Tell the user where these examples are drawn from;
    # I sometimes use this if I want to see the data again
    # or look at the tree.
    print("Index: ", start_point)
        
    # Return the number of lines of the corpus from the 
    # start point on:
    return corpus[start_point : start_point + number]


def parsed_to_tagged(parsed_sents):
    """
    Converts a list of parsed sentences (i.e., trees) to a list
    of tagged sentences (a list of token--tag tuples). Strips out
    some of the tree-specific tokens/tags that the treebank uses
    that shouldn't really get tagged by the user.
    """
    tagged_sents = []
    for sent in parsed_sents:
        tagged_sent = []
        for (token, tagged) in sent.pos():    
            # This removes any apparent token if its tag is
            # -NONE-. There are a lot of things in the tree 
            # that correspond to traces / SLASHes / empty 
            # categories that shouldn't get tagged by the user.
            # These generally have the tag '-NONE'. I *think* 
            # this shouldn't cause any missing tokens on the
            # user end -- in my experience, it works fine.
            if tagged != "-NONE-":
                tagged_sent.append( (token, tagged) )
                
        tagged_sents.append(tagged_sent)
        
    return tagged_sents


def token_list_print(token_list, width = 80):
    """
    Takes a list of tokens and prints them so that words are
    not broken at the edge of the console window. Makes things
    look a little more presentable.
    """
    length_list = len(token_list)
    column_counter = 0
    for token in token_list:
        if column_counter + len(token) <= width:
            column_counter += len(token) + 1
            print(token, end = " ")
        else:
            print("")
            column_counter = len(token)
            print(token, end = " ")
    
    print("")
    


def sentence_quiz(tagged_sent):
    """
    Takes a tagged sentence and asks the user to identify the
    tag for each token. The correct repsonse rate is reported 
    back as well as which tokens the user tagged incorrectly.
    The results are returned so they can be used to calculate
    an overall score at the end.
    """
    
    # First we separate tags and tokens in the sentence:
    tokens = [token for (token, tag) in tagged_sent]
    tags = [tag for (token, tag) in tagged_sent]
    
    # We'll want to know the number of tokens a few times:
    num_tokens = len(tokens)
    
    # It can be helpful for the user to know how many
    # tokens are in a sentence.
    print(Fore.CYAN + "Total tokens: {}".format(num_tokens) + Style.RESET_ALL)
    
    # We will want to make sure that the user tags
    # every token so we'll use a while loop
    all_tagged = False
    while not all_tagged:
    
        # Now we want to display each token in the sentence
        # and ask the user to tell us which tag they think
        # each token should receive:
        token_list_print(tokens)
        guess_tags = input("> ").upper().split()
    
        # We make sure that the user tagged all the tokens:
        if len(guess_tags) == num_tokens:
            all_tagged = True
        elif len(guess_tags) > num_tokens:
            print("You entered too many tags ({})!".format(len(guess_tags)))
        else:
            print("You entered too few tags ({})!".format(len(guess_tags)))
    
    # Now we zip everything back together.
    tokens_guesses = zip(tokens, tags, guess_tags)
    
    # Checking the answers
    incorrect = []
    for token in tokens_guesses:
        if token[1] != token[2]:
            incorrect.append(token)
            
    correct = len(tags) - len(incorrect)
    
    # Report the final scores:
    print("\n{} correct tags out of {} ({}%)".format(
        Fore.LIGHTGREEN_EX + str(correct) + Style.RESET_ALL, 
        len(tags), 
        Fore.LIGHTGREEN_EX + str(round(correct / len(tags) * 100))
                                    + Style.RESET_ALL ))
    
    # Tell the user which tokens were tagged incorrectly:
    if len(incorrect) > 0:
        print("{:12}  {:7}  {}".format("Token", "Correct", "Your answer"))
        print("{:12}  {:7}  {}".format("─" * 12, "─" * 7, "─" * 11))

        for token in incorrect:
            print("{:12}  {:7}  {}".format(token[0], token[1], token[2]))
        
    # To find out whether the user is doing poorly on any
    # particular tags, we will also return the mistakes:
    mistakes = [(tag, tag_guess) for (token, tag, tag_guess) in incorrect]
            
    return (correct, len(tags), mistakes)
    
def quiz(corpus, sentences = 5):
    """
    Actually runs the full quiz, given a corpus of parsed sentences.
    """
    
    # Get parsed sentences from the treebank
    parsed = get_sents(corpus, number = sentences)
    # Convert the Treebanks parsed trees into tagged sentences:
    tagged = parsed_to_tagged(parsed)
    
    # Keep track of the results and how many sentences we've done.
    results = []
    sent_num = 0
    
    # For each of the sentences from the treebank, ask the user
    # for what the tags are.
    for sentence in tagged:
        sent_num += 1
        print(Fore.CYAN + "\nSentence {} - ".format(sent_num) 
                                            + Style.RESET_ALL,
                                            end = '')
        
        # Put the results of each sentence in the results list.
        results.append(sentence_quiz(sentence))
        
    # Get the stats for how well the user did overall.
    total_correct = sum(correct for (correct, total, mistakes) in results)
    total_attempted = sum(total for (correct, total, mistakes) in results)
    
    # Report these stats to the user:
    print("\nFinal score: {} / {} ({}%)".format(total_correct, total_attempted, round(total_correct / total_attempted * 100)))
    
    # Find out which tags the user is having problems with.
    mistakes_list = (mistake for (correct, total, mistake) in results)

    mistagged = {}
    overused = {}
    for mistakes in mistakes_list:
        for (correct, mistake) in mistakes:
            if correct in mistagged.keys():
                mistagged[correct] += 1
            else:
                mistagged[correct] = 1
                
            if mistake in overused.keys():
                overused[mistake] += 1
            else:
                overused[mistake] = 1
    
    if len(mistagged) > 0:
        average = sum(mistagged[key] for key in mistagged.keys()) / len(mistagged)
        print("Frequently mistagged tags:")
        for key in mistagged.keys():
            if mistagged[key] >= average:
                print("{:4} {}".format(key, mistagged[key]))

quiz(parsed_sents, sentences = 5)    
