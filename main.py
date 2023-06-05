from nltk.stem import PorterStemmer #PorterStemmer for stemming
from tkinter import *   # library for GUI
import pickle   #library for filing
import math     #library for math functions
dictionary = dict()
vectors = dict()
N = 30      #number of documents in collection
alpha = 0.35    #alpha value to filter documents
"""
The dictionary is of following pattern:

term : [idf_value,{doc_id : term_frequency_in_document}]

Each term is token retrieved after document processing. The term frequency is the number of times the term is repeated in entire collection and
the dictionary in the end is a key:value pair of document ID and the frequency of the term in that document .

"""
# a simple list of stop words
stopwords = list()
# function to create document vectors
def getVector(doc_id):
    vector = list()
    for word in dictionary:
        freq_dict = dictionary[word][1]
        if doc_id in freq_dict:
            vector.append(dictionary[word][0]*freq_dict[doc_id])
        else:
            vector.append(0)
    return vector


#function making all the vectors
def createVectors():
    global vectors
    for i in range(1,31):
        vectors[i] = getVector(i)

#function to add a word to dictionary and make inverted index
def add_to_dictionary(word,doc_id):
    global dictionary
    if word in dictionary:
        value = dictionary[word]
        # value[0]+=1
        post_dict = value[1]
        if doc_id in post_dict:
            post_dict[doc_id]+=1
            value[1] = post_dict
        else:
            post_dict[doc_id] = 1
            value[1] = post_dict
        dictionary[word] = value
    else:
        dictionary[word] = [0,{doc_id:1}]
#function to write dictionary to file
def writeDictTofile():
    with open('Preprocessing/Dictionary.txt','wb') as file:
        pickle.dump(dictionary,file)
        file.close()
#function to read dictionary from file
def readDictfromfile():
    global dictionary
    with open('Preprocessing/Dictionary.txt','rb') as file:
        dictionary = pickle.loads(file.read())
        file.close()
        return dictionary
#function to write vectors to file
def writeVectortoFile():
    with open('Preprocessing/Vector.txt','wb') as file:
        pickle.dump(vectors, file)
        file.close()
#function to read vectors from file
def readVectorfromFile():
    global vectors
    with open('Preprocessing/Vector.txt','rb') as file:
        vectors = pickle.loads(file.read())
        file.close()

# simple function to check if the given string contains space or not
def containspace(word):

    for i in range(0,len(word)):
        if word[i]==' ':
            return True
    
    return False
# function to remove symbols and special characters
def remove_symbols(line):
    return ''.join(ch for ch in line if ch.isalnum())

# function that returns posting list
def findPostingList(word):
    if word not in dictionary:
        return []
    else:
        return list(dictionary[word][1].keys())

#function to find idf-value for a term
def findidf(word):
    df = len(findPostingList(word))
    return math.log(N/df)
#simple function to make the dictionary
def makedictionary():
    global dictionary
    # porter stemmer    
    ps = PorterStemmer()
    # filling the stopwords() list
    with open("Preprocessing/Stopword-List.txt","r") as stpfile:
        fileData = stpfile.readlines()
        for line in fileData:
            line = line.replace('\n', '')
            line = line.replace(' ', '')
            stopwords.append(line)

    # processing each document to create inverted index

    for doc_id in range(1,31):
        file = open("Dataset/"+str(doc_id)+".txt","r")
        data = file.readlines()
        
        for line in data:
            word = line.split()
            for i in range(0,len(word)):
                # normalizing the words
                word[i] = remove_symbols(word[i]) # removing symbols and special character from each token
                word[i] = word[i].lower()   #peforming case-folding
                word[i] = word[i].replace("nbsp"," ")   # handling the nbsp problem in the documents
                if containspace(word[i]):
                    subword = word[i].split()
                    word[i] = ps.stem(subword[0])
                    for j in range(1,len(subword)):
                        word.append(ps.stem(subword[j]))

                else:
                    word[i] = ps.stem(word[i])
            
            for alphabet in word:   # adding the normalized list of words into the dictionary to create inverted index
                if alphabet not in stopwords:
                    add_to_dictionary(alphabet, doc_id)
    
    for word in dictionary:
        dictionary[word][0] = findidf(word)
#function to calculate tf for the query
def countWord(query,word):
    count = 0
    for i in query:
        if i==word:
            count+=1
    return count
#function to create the query vector               
def createQueryvector(query):
    queryVector = list()
    for word in dictionary:
        if word in query:
            queryVector.append(dictionary[word][0] * countWord(query,word))
        else:
            queryVector.append(0.0)
    return queryVector
#function to calculate dot product between query and document vector
def dotProduct(docVector,queryVector):
    cosValue = 0
    for i in range(0,len(docVector)):
        if docVector[i]!=0 and queryVector[i]!=0:
            cosValue+=docVector[i]*queryVector[i]
    return cosValue
#function to calculate the magnitude of the Vector
def modulus(vector):
    mod = 0
    for i in range(0,len(vector)):
        if vector[i]!=0:
            mod+=math.pow(vector[i], 2)
    
    return math.sqrt(mod)

#function to calculate cosine similarity between two vectors
def cosineSimilarity(docVector,queryVector):
    modDocVector = modulus(docVector)
    modQueryVector = modulus(queryVector)
    if modDocVector==0 or modQueryVector==0:
        return 0 
    similarity = dotProduct(docVector,queryVector)/(modDocVector*modQueryVector)
    
    return similarity

def getSecondElement(tup):
    return tup[1]            

# driver code:
def main(query):
    readDictfromfile()
    readVectorfromFile()
    ps = PorterStemmer()
    query = query.split()

    # performing normalization on the query
    for i in range(0,len(query)):
        query[i] = remove_symbols(query[i])
        query[i] = query[i].lower()
        query[i] = ps.stem(query[i])
    
    rankOrder = list()  #initial answer set
    queryVector = createQueryvector(query)  
    for i in range(1,31):
        sim = cosineSimilarity(vectors[i], queryVector)
        if sim>0:
            rankOrder.append((i,sim))
    if len(rankOrder)>0:
        rankOrder.sort(reverse=True,key=getSecondElement)
    else:
        return rankOrder
    resultSet = list()
    if len(rankOrder)>0:
        threshold = alpha * getSecondElement(rankOrder[0])
        
        for i in range(0,len(rankOrder)):

            if getSecondElement(rankOrder[i]) >= threshold:
                resultSet.append(rankOrder[i])
    return resultSet        #final result set

#Below code is for the GUI
frame = Tk()
frame.title("IR assignment 02 Vector Space Model (20k-0177)")
frame.geometry('1920x1080')
frame.configure(bg='black')


def showquery():
    lbl.configure(text='')
    inp = inputtxt.get(1.0,"end-1c")
    # sending the query to the main function and getting the answer
    inp = main(inp)    
    lbl.configure(height=1000,width=50,font=('Times',10))
    answerText = "The terms are present in following documents:\n"
    for i in range(0,len(inp)):
        answerText+= "Document "+str(inp[i][0])+"\n"
    if len(inp)==0:
        answerText = "No result exist"
    lbl.configure(foreground='white',background='grey')
    lbl.configure(text=answerText)
    # lbl.configure(fg=red)

queryLabel = Label(frame,text="Enter Query\nThe value of alpha used is 0.3\ndf=log(N/df), no normalization is performed")
queryLabel.configure(background='black',foreground='white')
queryLabel.pack()
inputtxt = Text(frame,height=4,width=25)
inputtxt.configure(fg='black',background='white')
inputtxt.pack()

search = Button(frame,text="search",command=showquery)
search.pack()

lbl = Label(frame,text="")
lbl.pack()

frame.mainloop()