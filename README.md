# Vector-Space-Model


## Introduction

Vector Space Model in Information Retrieval Systems is an improvement over <a href = "https://github.com/siddiki002/Boolean-Retrieval-Model" target = _blank>Boolean Retrieval Model</a>.
It gives following benefits over Boolean Retrieval Model
* Partial Matching was possible
* Ranking of the documents was possible
* Query expansion (using Rocchio's algorithm) was possible

## About the Repository

### Directories
The repo contains following directories
1. Dataset (_It contains the dataset used for making the Vector Space Model_)
2. Preprocessing (_It contains the indexing and vectors of the documents saved in binary format using <a href = "https://docs.python.org/3/library/pickle.html" target = _blank>Pickle</a> library to prevent processing and vector creation everytime the program is executed_) 
3. Testcases (_It contains the Gold query set and the results obtained by our model_)
4. main.py is the file where all the work is done
<a name="libraries"></a>
### Libraries Used
* Pickel (_can be accessed by <a href = "https://docs.python.org/3/library/pickle.html" target = _blank>clicking here</a>_)
* nltk (_can be accessed by <a href  ="https://www.nltk.org/" target = _blank>clicking here</a>_)
* tkinter (_can be accessed by <a href = "https://docs.python.org/3/library/tkinter.html" target = _blank>clicking here</a>_)
* math (_can be accessed by <a href = "https://docs.python.org/3/library/math.html" target = _blank>clicking here</a>_)


### Language Used
<img src = "https://img.shields.io/badge/-Python3-yellow?logo=python&style=for-the-badge" />

For running application simply run main.py file and tkinter GUI will open and write your query. Remember to install all the mentioned <a href = "#libraries">Libraries</a>
Don't forget to give this repo a star if you found it helpful and give me a follow on my <a href = "https://www.linkedin.com/in/muhammad-ammar-siddiqui-09b519221/">Linkedin</a>
