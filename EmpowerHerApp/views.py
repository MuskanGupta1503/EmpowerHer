from django.shortcuts import redirect, render
import PyPDF2
import textract
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
import os 
from .models import *
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.
def resume_screening(request):
    if request.method=='POST':
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(filename)
        pdfFileObj = open(os.path.join(r"C:\Users\Hello\Desktop\pythonfiles\EmpowerHer\media", filename),'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        num_pages = pdfReader.numPages
        print(num_pages)
        count = 0
        text = ""
        # Extract text from every page on the file
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()
        # Convert all strings to lowercase
        text = text.lower()
        # Remove numbers
        text = re.sub(r'\d+','',text)
        # Remove punctuation
        text = text.translate(str.maketrans('','',string.punctuation))
        # Create dictionary with industrial and system engineering key terms by area
        terms = {'Quality/Six Sigma':['black belt','capability analysis','control charts','doe','dmaic','fishbone',
                                    'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                                    'pdsa','performance improvement','process improvement','quality',
                                    'quality circles','quality tools','root cause','six sigma',
                                    'stability analysis','statistical analysis','tqm'],      
                'Operations management':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                        'machinery','maintenance','manufacture','line balancing','oee','operations',
                                        'operations research','optimization','overall equipment effectiveness',
                                        'pfmea','process','process mapping','production','resources','safety',
                                        'stoppage','value stream mapping','utilization'],
                'Supply chain':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                                'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                                'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                                'third party logistics','transport','transportation','traffic','supply chain',
                                'vendor','warehouse','wip','work in progress'],
                'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                                    'finance','kanban','leader','leadership','management','milestones','planning',
                                    'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
                'Data analytics':['analytics','api','aws','big data','business intelligence','clustering','code',
                                'coding','data','database','data mining','data science','deep learning','hadoop',
                                'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                                'predictive','programming','python','r','sql','tableau','text mining',
                                'visualuzation'],
                'Healthcare':['adverse events','care','clinic','cphq','ergonomics','healthcare',
                            'health care','health','hospital','human factors','medical','near misses',
                            'patient','reporting system']}

        # Initializie score counters for each area
        quality = 0
        operations = 0
        supplychain = 0
        project = 0
        data = 0
        healthcare = 0
        # Create an empty list where the scores will be stored
        scores = []
        # Obtain the scores for each area
        for area in terms.keys():
            if area == 'Quality/Six Sigma':
                for word in terms[area]:
                    if word in text:
                        quality +=1
                scores.append(quality)
                
            elif area == 'Operations management':
                for word in terms[area]:
                    if word in text:
                        operations +=1
                scores.append(operations)
                
            elif area == 'Supply chain':
                for word in terms[area]:
                    if word in text:
                        supplychain +=1
                scores.append(supplychain)
                
            elif area == 'Project management':
                for word in terms[area]:
                    if word in text:
                        project +=1
                scores.append(project)
                
            elif area == 'Data analytics':
                for word in terms[area]:
                    if word in text:
                        data +=1
                scores.append(data)
                
            else:
                for word in terms[area]:
                    if word in text:
                        healthcare +=1
                scores.append(healthcare)
                
        # Create a data frame with the scores summary
        summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
        print(summary)

        # # Create pie chart visualization
        output_dir= './media/'
        pie = plt.figure(figsize=(8,8))
        plt.pie(summary['score'], labels=summary.index, explode = (0.1,0.2,0.3,0.4,0.5,0.6), autopct='%1.0f%%',shadow=True,startangle=90)
        plt.title('Industrial Engineering Candidate - Resume Decomposition by Areas')
        plt.axis('equal')
        
        # plt.show()
        pie.savefig('{}resume_screening_results.png'.format(output_dir))
        img_link='{}resume_screening_results.png'.format(output_dir)
        print(img_link)
        return render(request, 'resume_screening.html', {
            'uploaded_file_url': img_link
        })
    elif request.method=='POST' and 'btnform2' in request.POST:
        job_description=request.FILES['job_description']
        resume=request.FILES['resume']
        if job_description:
            print(job_description)
            print(resume)
    return render(request,'resume_screening.html')

def index(request):
    return render(request,'index.html')

def index1(request):
    return render(request,'index1.html')

def interview(request):
    return render(request,'interview.html')

def home(request):
    return render(request,'home.html')

def opportunity(request):
    data={}
    category=Category.objects.all()
    opportunity=Opportunity.objects.all()
    categoryID=request.GET.get('category')
    print(categoryID)
    if categoryID:
        opportunity=Opportunity.objects.filter(category=categoryID)
    data['category']=category
    data['opportunity']=opportunity
    return render(request,'opportunity.html',data)

def book_slots(request):
    data={}
    person=Person.objects.all()
    data['person']=person
    return render(request,'book_slots.html',data)

def post_opportunity(request):
    error=""
    if request.method=='POST':
        title=request.POST['title']
        lastdate=request.POST['lastdate']
        applylink=request.POST['applylink']
        description=request.POST['description']
        myfile = request.FILES['myfile']
        isForWomen=request.POST['isForWomen']
        cat_name=request.POST['category']
        category = Category.objects.get(name=cat_name)
        try:
            print("Enter Try")
            Opportunity.objects.create(title=title,
            lastdate=lastdate,category=category,description=description,
            applylink=applylink,isForWomen=isForWomen,image=myfile)
            print("Opportunity Created")
            return redirect('opportunity')
        except:
            error="yes"
    return render(request,'post_opportunity.html')

def join_panel(request):
    error=""
    if request.method=='POST':
        name=request.POST['name']
        linkedinId=request.POST['linkedinId']
        twitter=request.POST['twitter']
        description=request.POST['description']
        myfile = request.FILES['myfile']
        try:
            print("Enter Try")
            Person.objects.create(name=name,
            linkedinId=linkedinId,twitter=twitter,description=description,image=myfile)
            print("Person Created")
            return redirect('book_slots')
        except:
            error="yes"
    return render(request,'join_panel.html') 

# def support_our_cause(request):
#     return render(request,'support_our_cause.html')

def match_with_jd(request):
    if request.method=='POST':
        resume=request.FILES['resume']
        job_description=request.FILES['job_description']
        fs = FileSystemStorage()
        resumename = fs.save(resume.name, resume)
        print(resumename)
        resumeFileObj = open(os.path.join(r"C:\Users\Hello\Desktop\pythonfiles\EmpowerHer\media", resumename),'rb')
        resumeRead=docx2txt.process(resumeFileObj)
        jdname = fs.save(job_description.name, job_description)
        print(jdname)
        jdFileObj = open(os.path.join(r"C:\Users\Hello\Desktop\pythonfiles\EmpowerHer\media", jdname),'rb')
        jdRead=docx2txt.process(jdFileObj)
        text=[resumeRead,jdRead]
        cv=CountVectorizer()
        count_matrix=cv.fit_transform(text)
        print(cosine_similarity(count_matrix))
        matchPercent=cosine_similarity(count_matrix)[0][1]*100
        matchPercent=round(matchPercent,2)
        result="Your resume matches about " + str(matchPercent) + "% of job description"
        data={}
        data['result']=result
        return render(request,'match_with_jd.html',data)
    return render(request,'match_with_jd.html')