# Tag quiz

This is a script based on the Natural Language Toolkit (NLTK) that allows the user to test how accurate they are at tagging English corpus data in the Penn Treebank corpus using the Penn Treebank tag set, with a general goal of familiarizing the user with the tag set used in the corpus and the conventions used for tagging data in this system. The script takes five sentences from a random point in the corpus and asks the user to tag the tokens in each sentence. The user's tags are then evaluated against the tags in the corpus, and the user is told the percentage of correct tags as as well as which tokens were tagged incorrectly. At the end, and overall score is shown, and frequently misidentified tags are reported to help the user identify tags that they may not fully understand.

## Requirements

- Python 3
- NLTK 3 (the source of the corpora)
- colorama (to make things look a bit more readable in the terminal)

## Usage

- After starting the script, the corpus will be loaded and the sentences will be selected and parsed. 
- After this, the first sentence will be presented, and the user will be presented with a prompt (>) where the tags should be entered.
- The user should enter the tags as a single string, with each tag separated by a space.
    - If the sentence is _The duck saw me ._
    - ...then the user should enter `DT NN VBD PRP .`
    - User input is case-insensitive, so this could also be `dt nn vbd prp .` or even `dt NN VbD pRp .`
- Once the user is done, hit Enter (or I guess Return if you're on a Mac), and you'll see how well you did on the sentence as well as the mistakes you made. The script will then proceed to the next sentence.

## Background

I wanted to brush up a bit on my knowledge of the Penn tag set because it's been years since I last had to use it in any way. I figured there would be some sort of application on the internet that would allow somebody to practice tagging with this particular tag set and test how accurate they were at using it. I was really surprised that I could find no such pre-existing application on the web. Fortunately, with access to the subset of the Penn Treebank provided by the NLTK, it was fairly easy to code up my own solution in an evening. 

## To do

- Allow the user to choose how many sentences will appear in each quiz.
    - Probably as a CLI option. This should take a minute to do and I have no excuse for not having done it yet.
- Build in an option to run quizzes on other corpora with different tag sets. 
    - In principle this can be adapted to work with any corpus with any tag set. The code right now is set up specifically to extract tags from the parsed trees in the NLTK's subset of the Penn Treebank corpus, so a little work is needed to generalize the code and make it work with other tagged corpora that come with the NLTK.
