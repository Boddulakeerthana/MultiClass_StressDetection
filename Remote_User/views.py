from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import VotingClassifier
#model selection
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_stress_detection,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})

    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_Stress_Detection(request):
    if request.method == "POST":

        if request.method == "POST":

            FID= request.POST.get('FID')
            MEAN_RR= request.POST.get('MEAN_RR')
            MEDIAN_RR= request.POST.get('MEDIAN_RR')
            SDRR= request.POST.get('SDRR')
            RMSSD = request.POST.get('RMSSD')
            SDSD= request.POST.get('SDSD')
            SDRR_RMSSD= request.POST.get('SDRR_RMSSD')
            HR= request.POST.get('HR')
            VLF= request.POST.get('VLF')
            VLF_PCT= request.POST.get('VLF_PCT')
            LF= request.POST.get('LF')
            LF_PCT= request.POST.get('LF_PCT')
            LF_NU= request.POST.get('LF_NU')
            HF= request.POST.get('HF')
            HF_PCT= request.POST.get('HF_PCT')
            HF_NU= request.POST.get('HF_NU')
            TP= request.POST.get('TP')
            LF_HF= request.POST.get('LF_HF')
            HF_LF= request.POST.get('HF_LF')
            sampen= request.POST.get('sampen')
            higuci= request.POST.get('higuci')


        df = pd.read_csv('Datasets.csv', encoding='latin-1')

        def apply_results(label):
            if (label == 'no stress'):
                return 0  # No Stress
            elif (label == 'stress'):
                return 1  # Stress

        df['results'] = df['condition'].apply(apply_results)

        x = df["FID"]
        y = df["results"]


        cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
        x = cv.fit_transform(x)

        print("Data")
        print(x)
        print("Results")
        print(y)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Naive Bayes")

        from sklearn.naive_bayes import MultinomialNB
        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes = accuracy_score(y_test, predict_nb) * 100
        print(naivebayes)
        print(confusion_matrix(y_test, predict_nb))
        print(classification_report(y_test, predict_nb))
        models.append(('naive_bayes', NB))

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))

        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        FID1 = [FID]
        vector1 = cv.transform(FID1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'No Stress'
        elif prediction == 1:
            val = 'Stress'

        print(prediction)
        print(val)

        predict_stress_detection.objects.create(
        FID=FID,
        MEAN_RR=MEAN_RR,
        MEDIAN_RR=MEDIAN_RR,
        SDRR=SDRR,
        RMSSD=RMSSD,
        SDSD=SDSD,
        SDRR_RMSSD=SDRR_RMSSD,
        HR=HR,
        VLF=VLF,
        VLF_PCT=VLF_PCT,
        LF=LF,
        LF_PCT=LF_PCT,
        LF_NU=LF_NU,
        HF=HF,
        HF_PCT=HF_PCT,
        HF_NU=HF_NU,
        TP=TP,
        LF_HF=LF_HF,
        HF_LF=HF_LF,
        sampen=sampen,
        higuci=higuci,
        Prediction=val)

        return render(request, 'RUser/Predict_Stress_Detection.html',{'objs': val})
    return render(request, 'RUser/Predict_Stress_Detection.html')

