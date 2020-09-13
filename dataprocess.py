# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:50:35 2020

@author: SANOVE DEVASIA
"""
import seq2seq_wrapper
import importlib
importlib.reload(seq2seq_wrapper)
import data_preprocessing
import data_utils_1
import data_utils_2
import csv
import pyttsx3 
import speech_recognition as sr


posmsg = ["yes", "s", "of course", "yeah", "i do", "i have", "mm", "hm", "right", "correct", "true", "100", "absolutely", "exactly"]
negmsg = ["don't", "nope", "not at all", "do not", "doesn't", "nah", "does not", "wrong", "incorrect", "false", "0", "no chance", "impossible"]

gsymlist = []
gsymm = csv.reader(open("symtoms.csv", newline=''))
for row in gsymm:
    gsymlist.append(row[0].replace('_', ' '))

def gettoldsym(sym):
    t = []
    for s in gsymlist:
        if s in sym:
            t.append(s)
    return t

def checkpos(msg):
    for m in posmsg:
        if m in msg:
            return True
    return False

def checkneg(msg):
    if msg == "no":
        return True
    for m in negmsg:
        if m in msg:
            return True
    return False

def chatbot(txt):
    #chatbot code here 
    # Importing the dataset
    metadata, idx_q, idx_a = data_preprocessing.load_data(PATH = './')
    # Splitting the dataset into the Training set and the Test set
    (trainX, trainY), (testX, testY), (validX, validY) = data_utils_1.split_dataset(idx_q, idx_a)
    # Embedding
    xseq_len = trainX.shape[-1]
    yseq_len = trainY.shape[-1]
    batch_size = 16
    vocab_twit = metadata['idx2w']
    xvocab_size = len(metadata['idx2w'])  
    yvocab_size = xvocab_size
    emb_dim = 1024
    idx2w, w2idx, limit = data_utils_2.get_metadata()
    # Building the seq2seq model
    model = seq2seq_wrapper.Seq2Seq(xseq_len = xseq_len,
                                yseq_len = yseq_len,
                                xvocab_size = xvocab_size,
                                yvocab_size = yvocab_size,
                                ckpt_path = './weights',
                                emb_dim = emb_dim,
                                num_layers = 3)
    # Loading the weights and Running the session
    session = model.restore_last_session()
    # Getting the ChatBot predicted answer
    def respond(question):
        encoded_question = data_utils_2.encode(question, w2idx, limit['maxq'])
        answer = model.predict(session, encoded_question)[0]
        return data_utils_2.decode(answer, idx2w) 
    # Setting up the chat 
    #while True :
        ''''
        engine = pyttsx3.init()
        engine.runAndWait()
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                print('You :')
                x=r.recognize_google(audio)
                print(x)
        except:
            continue
        question=x.lower()'''
    question=txt
        #question = input("You: ")
        #if question=='good bye':
        #print('Ok Bye')
        #break
        #answer = respond(question)
    return respond(question)
        #engine.say(answer) 
        #engine.runAndWait() 
        #print ("ChatBot: "+answer)
    #return answer #replace this with chatbot output

def readtemp():
    #temperature sensor code here
    return 40 #replace this with measured temp value

def readhb():
    #heartbeat sensor code here
    return 110 #replace this with measured heartbeat value

def login(uname, password):
    reader = csv.reader(open("userpasswd.csv"))
    for row in reader:
        if list(row)[0] == uname and list(row)[1] == password:
            return True
    #f.close()
    return False

def unameavailable(uname):
    reader = csv.reader(open("userpasswd.csv"))
    for row in reader:
        if list(row)[0] == uname:
            return False
    #reader.close()
    return True

def signup(uname, password, name, age, place, bgroup, rdate):
    f = open("userpasswd.csv", "w", newline='')
    writer = csv.writer(f)
    writer.writerow([uname, password])
    f.close()
    f = open("userdet.csv", "w", newline='')
    writer = csv.writer(f)
    writer.writerow([uname, name, age, place, bgroup, rdate])
    f.close()
    return True

def findsym(dis):
    pass

def findmed(dis):
    pass

def fetchdis(question):
    words = question.split(' ')
    return words[-1]

def mergeall():
    reader1 = csv.reader(open("Training.csv"))
    reader = csv.reader(open("Testing.csv"))
    f = open("medicaldata.csv", "w", newline='')
    writer = csv.writer(f)

    for row in reader1:
        writer.writerow(row)
    for rows in reader:
        writer.writerow(rows)
    f.close()
    

def get_sym():
    reader1 = csv.reader(open("medicalset.csv"))
    f = open("symtoms.csv", "w", newline='')
    writer = csv.writer(f)
    for row in reader1:
        i = 1
        for sym in list(row):
            writer.writerow([sym, i])
            i += 1
        break
    f.close()
    
    


def get_dis():
    reader1 = csv.reader(open("medicalset.csv", newline=''))
    f = open("diseases.csv", "w", newline='')
    writer = csv.writer(f)
    i = 0
    mylist = []
    for row in reader1:
        if i == 0:
            i += 1
            continue
        if len(row) != 0 and list(row)[-1] not in mylist:
            writer.writerow([list(row)[-1], i])
            i += 1
            mylist.append(list(row)[-1])
            
            
def save_dis(t):
    i = 0
    f = open("sorteddisnum.csv", "w", newline='')
    writer = csv.writer(f)
    for k, v in t:
        writer.writerow([k, i])
        i += 1
    
    
def get_numset():
    medicalset = csv.reader(open("medicalset.csv"))
    symtoms = csv.reader(open("symtoms.csv", newline=''))
    numset = {}
    i = 0 
    for row in medicalset:
        if i == 0:
            i += 1
            continue
        if len(row) != 0:
            if list(row)[-1] == 'prognosis':
                pass
            if list(row)[-1] not in numset:
                numset[list(row)[-1]] = []
            tl = []
            for x in range(len(list(row)[:-1])):
                if list(row)[x] == '1':
                    tl.append(x)
            if tl not in numset[list(row)[-1]]:
                numset[list(row)[-1]].append(tl)



    #save numset (dis name list of sym no)*******
    tm = numset.items()
    newtm = tuple(tm) 
    for k, v in newtm:
        if len(v) == 1:
            t = v[0]
            numset.pop(k)
            numset[k] = v[0]
        else:
            i = 0
            for item in v:
                numset[k+' '+str(i)] = item
                i += 1
            numset.pop(k)
    numset.pop('prognosis')
    t = sorted(numset.items(), key = lambda kv:(kv[1], kv[0]))
    save_dis(t)
    finallist = {}
    i = 0
    for k, v in t:
        finallist[i] = v
        i += 1
    #print(finallist)
    symlist = []
    numtosym = {}
    ss = csv.reader(open("symtoms.csv", newline=''))
    for row in ss:
        numtosym[row[0].replace('_', ' ')] = int(row[1])-1
    while True:
        #print('......', list(finallist.keys()))
        small = min(list(finallist.keys()))
        ind1 = -1
        engine = pyttsx3.init()
        engine.say('Do you have any other symptom')
        engine.runAndWait()
        print('Do you have any other symptom')
        
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                text=r.recognize_google(audio)
                print(text)
        except:
            continue
        
        sym=text.lower()
        if checkneg(sym):
            break
        alltoldsym = gettoldsym(sym)
        if len(alltoldsym) == 0:
            engine.say('Sorry, It is not recognized as symptom')
            engine.runAndWait()
            print('Sorry, It is not recognized as symptom')
            continue
        else:
            for sy in alltoldsym:
                sym = numtosym[sy]
                small = min(list(finallist.keys()))
                ind1 = -1
                print(sym)
                symlist.append(sym)
                for k, v in finallist.items():
                    if v[0] <= sym and v[-1] >= sym:
                        ind1 = k
                        break
                print('ffffff', ind1)
                for i in range(small, ind1):
                    del finallist[i]
                    ind2 = -1
                for k, v in finallist.items():
                    if v[0] > sym:
                        ind2 = k
                        break
                if ind2 == -1:
                    ind2 = max(finallist.keys())
                print('llllllllll', ind2)
                maxx = max(finallist.keys())
                for i in range(ind2, maxx+1):
                    del finallist[i]
                for k, v in finallist.items():
                    print(k, ' : ', v)
                #print('iiiiiiiii', list(finallist.keys()))  
    engine = pyttsx3.init()
    engine.say('Place the heartbeat sensor on your arm above your wrist and hold it for one minute')
    engine.runAndWait()
    print('Place the heartbeat sensor on your arm above your wrist and hold it for one minute')
    hr = readhb()
    if hr > 100 and 58 not in symlist:
        symlist.append(58)


    engine.say('Place the temperature sensor on your arm and hold it for one minute')
    engine.runAndWait()
    print('Place the temperature sensor on your arm and hold it for one minute')
    tm = readtemp()
    if tm >= 39 and 25 not in symlist:
        symlist.append(25)
    elif tm >= 37 and 41 not in symlist:
        symlist.append(41)
    elif tm <= 35 and 17 not in symlist:
        symlist.append(17)


    tkey = list(finallist.keys())
    for k in tkey:
        for sym in symlist:
            if sym not in finallist[k]:
                del finallist[k]
                break
    print('...........................................')
    for k, v in finallist.items():
        print(k, ' : ', v)
    for k in finallist.keys():
        for sym in symlist:
            finallist[k].remove(sym)
    print('...........................................')
    for k, v in finallist.items():
        print(k, ' : ', v)
    if len(finallist) == 1:
        return finallist
    allsym = []
    for k, v in finallist.items():
        for item in v:
            if item not in allsym:
                allsym.append(item)
    tall = []
    for item in allsym:
        for k, v in finallist.items():
            if item not in v:
                tall.append(item)
                break
    print('...........................................')
    print(tall)
    symletr = []
    for sn in symtoms:
        num = int(sn[1])-1
        if num in tall:
            symletr.append((num, sn[0]))
    print(symletr)
    
    
    
    #asking sym
    for sym in symletr:
        kk = list(finallist.keys())
        while True:
            engine = pyttsx3.init()
            engine.say('Do you have '+sym[1].replace('_', ' '))
            engine.runAndWait()
            print('Do you have '+sym[1].replace('_', ' ')+'?')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
                    break
            except:
                continue
            
        ans=text.lower()    
        #ans = input('Do you have '+sym[1].replace('_', ' ')+'?')
        if checkneg(ans) != True:
            for k in kk:
                if sym[0] not in finallist[k]:
                    del finallist[k]
        else:
            for k in kk:
                if sym[0] in finallist[k]:
                    del finallist[k]
        if len(finallist) == 1:
            return finallist
def queries():
    while True:
        engine = pyttsx3.init()
        engine.say('Please ask your question')
        engine.runAndWait()
        print('Please ask your question..')
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                text=r.recognize_google(audio)
                print(text)
        except:
            continue
        question = text.lower()
        #question = 'Could you please say the medicine for Phuemonia'
        if 'medicine' in question:
            #dis = fetchdis(question)
            #findmed(dis)
            engine.say('Antobotics can treat many forms of Phuemonia. Some forms pf Phuemonia can be prevented by vaccines. ')
            print('Antobotics can treat many forms of Phuemonia. Some forms pf Phuemonia can be prevented by vaccines.')
        elif 'symptoms of' in question:
            dis = fetchdis(question)
            findsym(dis)
        else:
            ans = chatbot(question)
            engine = pyttsx3.init()
            engine.say(ans)
            engine.runAndWait()
            print(ans)
        while True:
            engine = pyttsx3.init()
            engine.say('Do you have any other questions')
            engine.runAndWait()
            print('Do you have any other questions?')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
                    break
            except:
                continue
        if checkneg(text.lower()):
            engine = pyttsx3.init()
            engine.say('Thank you for your cooperation')
            engine.runAndWait()
            print('Thank you for your cooperation')
            break
        exit()
    #questions reply 
def diagnosis():
    dis=''
    finallist = get_numset()
    print(finallist)
    diseases = csv.reader(open("sorteddisnum.csv", newline=''))
    disnum = list(finallist.keys())[0]
    for row in diseases:
        if int(row[1]) == disnum:
            dis = row[0][:-1]
            break
    engine = pyttsx3.init()
    engine.say('You have '+dis)
    engine.runAndWait()
    print('You have ', dis)
    while True:
        engine = pyttsx3.init()
        engine.say('Do you have any questions')
        engine.runAndWait()
        print("Do you have any questions?")
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                text=r.recognize_google(audio)
                print(text)
        except:
            continue
        if checkneg(text.lower()) != True:
            queries()




while True:
    print('Running')
    try:
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text=r.recognize_google(audio)
            print(text)
    except:
        continue
    if text.lower() != "hello robot":
        continue
    engine = pyttsx3.init()
    engine.say('Hello user, Do you already have an account in this system')
    engine.runAndWait()
    print('Hello user, Do you already have an account in this system?')
    try:
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text=r.recognize_google(audio)
            print(text)
    except:
        continue
    if checkneg(text.lower()) != True:
        uname = ''
        passwd = ''
        engine.say('Please tell your user name')
        engine.runAndWait()
        print('Please tell your user name')
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                uname=r.recognize_google(audio)
                print(uname)
        except:
            continue
        uname = uname.lower()
        engine.say('Please tell your password')
        engine.runAndWait()
        print('Please tell your password')
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                passwd=r.recognize_google(audio)
                print(passwd)
        except:
            continue
        passwd = passwd.lower()
        if login(uname, passwd):
            engine.say('Login successful')
            engine.runAndWait()
            print('Login successful...')
            while True:
                engine.say('Do you want to diagnose your disease')
                print('Do you want to diagnose your disease')
                engine.runAndWait()
                try:
                    r = sr.Recognizer()
                    mic = sr.Microphone()
                    with mic as source:
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source)
                        text=r.recognize_google(audio)
                        print(text)
                        break
                except:
                    continue
            if checkneg(text.lower()) != True:
                diagnosis()
            else:
                queries()
    else:
        uname = ''
        passwd = ''
        name = ''
        age = ''
        place = ''
        bgroup = ''
        from datetime import datetime
        now = datetime.now()
        rdate = now.strftime("%m/%d/%Y, %H:%M:%S")
        while True:
            engine.say('Please tell one user name')
            engine.runAndWait()
            print('Please tell one user name')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    uname=r.recognize_google(audio)
                    print(uname)
            except:
                continue
            engine.say('Do you want to continue with ' + uname.lower())
            engine.runAndWait()
            print('Do you want to continue with ',  uname.lower())
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
            except:
                continue
            if checkneg(text.lower()) != True:
                if unameavailable(uname.lower()):
                    break
                else:
                    engine.say('User name already exist, please choose another one')
                    engine.runAndWait()
                    print('User name already exist! please choose another one..')
                    continue


        while True:
            engine.say('Please tell a password')
            engine.runAndWait()
            print('Please tell a password..')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    passwd=r.recognize_google(audio)
                    print(passwd)
            except:
                continue
            engine.say('Do you want to continue with ' + passwd.lower())
            engine.runAndWait()
            print('Do you want to continue with ',  passwd.lower())
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
            except:
                continue
            if checkneg(text.lower()) != True:
                    break


        while True:
            engine.say('Please tell your name')
            engine.runAndWait()
            print('Please tell your name..')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    name=r.recognize_google(audio)
                    print(name)
            except:
                continue
            engine.say('Do you want to continue with ' + name.lower())
            engine.runAndWait()
            print('Do you want to continue with ',  name.lower())
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
            except:
                continue
            if checkneg(text.lower()) != True:
                    break


        while True:
            engine.say('Please tell your age')
            engine.runAndWait()
            print('Please tell your age..')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    age=r.recognize_google(audio)
                    print(age)
            except:
                continue
            engine.say('Do you want to continue with ' + age.lower())
            engine.runAndWait()
            print('Do you want to continue with ',  age.lower())
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
            except:
                continue
            if checkneg(text.lower()) != True:
                    break


        while True:
            engine.say('Please tell your place')
            engine.runAndWait()
            print('Please tell your place..')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    place=r.recognize_google(audio)
                    print(place)
            except:
                continue
            engine.say('Do you want to continue with ' + place.lower())
            engine.runAndWait()
            print('Do you want to continue with ',  place.lower())
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
            except:
                continue
            if checkneg(text.lower()) != True:
                    break



        while True:
            engine.say('Please tell your blood group')
            engine.runAndWait()
            print('Please tell your blood group..')
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    bgroup=r.recognize_google(audio)
            except:
                continue
            bgroup = bgroup.lower()
            if bgroup == 'a positive' or bgroup == 'apositive':
                bgroup = 'A+'
            elif bgroup == 'a negative' or bgroup == 'anegative':
                bgroup = 'A-'
            elif bgroup == 'b positive' or bgroup == 'be positive':
                bgroup = 'B+'
            elif bgroup == 'b negative' or bgroup == 'be negative':
                bgroup = 'B-'
            elif bgroup == 'o positive' or bgroup == 'opositive' or bgroup == 'opposite':
                bgroup = 'O+'
            elif bgroup == 'o negative' or bgroup == 'onegative':
                bgroup = 'O-'
            elif bgroup == 'a be positive' or bgroup == 'a b positive' or bgroup == 'ab positive':
                bgroup = 'AB+'
            elif bgroup == 'a be negative' or bgroup == 'a b negative' or bgroup == 'ab negative':
                bgroup = 'AB-'
            else:
                bgroup = 'O+'
            engine.say('Do you want to continue with ' + bgroup)
            engine.runAndWait()
            print('Do you want to continue with ',  bgroup)
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    text=r.recognize_google(audio)
                    print(text)
            except:
                continue
            if checkneg(text.lower()) != True:
                    break
        if signup(uname, passwd, name, age, place, bgroup, rdate):
            engine.say('Account created successfully')
            engine.runAndWait()
            print('Account created successfully...')
            while True:
                engine.say('Do you want to diagnose your disease')
                print('Do you want to diagnose your disease')
                engine.runAndWait()
                try:
                    r = sr.Recognizer()
                    mic = sr.Microphone()
                    with mic as source:
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source)
                        text=r.recognize_google(audio)
                        print(text)
                        break
                except:
                    continue
            if checkneg(text.lower()) != True:
                diagnosis()
            else:
                queries()







   
#dischromic  patches
#nodal skin eruptions
#itching

#dischromic  patches
#skin rash
#itching
















 
    
    
    
    
    
    
    
    
    
    
    
    