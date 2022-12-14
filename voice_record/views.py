from django.shortcuts import render
from voice_record.models import *
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect, HttpResponse


import soundfile
from .models import *
import speech_recognition as sr
from django.conf import settings
import os
# import json
import requests
# import time

from gingerit.gingerit import GingerIt
import numpy as np
import pandas as pd



header = {
	'authorization': '92d481b159ef4c93a3e0fb9c81942306',
	'content-type': 'application/json'
}

api_key = '92d481b159ef4c93a3e0fb9c81942306'

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


def _read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def upload_file(audio_file, header):
    upload_response = requests.post(
        upload_endpoint,
        headers=header, data=_read_file(audio_file)
    )
    return upload_response.json()



# Create your views here.
def home(request):
    return render(request, 'voice_record/home.html')


from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site

@csrf_exempt
def record(request):
    if request.method == "POST":
        audio_file = request.FILES.get("audio")
        print(audio_file)
        

        fs = FileSystemStorage()
        filename = fs.save('m.mp3', audio_file)
        uploaded_file_url = fs.url(filename)

        print('OOOOO: ',uploaded_file_url)


        language = 'dd'
        record = Record.objects.create(language=language, voice_record=uploaded_file_url)
        record.save()
        saved_id = record.pk

        # return redirect('details', saved_id)
        return HttpResponse('home')


    
    step_data           = {}
    step                = Step.objects.filter(active= True).prefetch_related('step_questions').order_by('page_number')
    step_count          = step.count()
    page_number_list    = list(step.values_list('page_number', flat=True))
    step_data2 = []
    for i in step:
        step_data2.append ({ 
                'page_no'               : i.page_number,
                'duration_in_sec'       : i.duration_in_sec, 
                'question'              : (list(i.step_questions.filter(active = True).order_by('?').values_list('question', flat=True)[:int(i.no_question_to_display)]))
        })





    context = {
        "page_title"            : "Record audio",
        'step_count'            : step_count,
        'step_range'            : range(1,step_count+1),
        'step_data2'            : step_data2,
        'page_number_list'      : page_number_list
        }
    # return render(request, "voice_record/record.html", context)
    return render(request, "voice_record/new_record.html", context)


import json
@csrf_exempt
def new_record_(request):
    if request.method == "POST":
        audio_file = request.FILES.get("audio")
        print(audio_file)
        

        fs = FileSystemStorage()
        filename = fs.save('m.mp3', audio_file)
        uploaded_file_url = fs.url(filename)

        print('OOOOO: ',uploaded_file_url)


        language = 'dd'
        record = Record.objects.create(language=language, voice_record=uploaded_file_url)
        record.save()
        saved_id = record.pk
        site_ = str(get_current_site(request).domain)
        full  = "http://"+site_ + "/record/details/"+str(saved_id)

        # return redirect('details', saved_id)
        # return JsonResponse({"status": 1})
        # return HttpResponse(json.dumps({"status": 1}), content_type='application/json')
        return HttpResponse(full)


    record = get_object_or_404(Record, id=saved_id)
    base_dir = str(settings.BASE_DIR)

    # path = "C:\\temp\myFolder\example\\"
    newPath = base_dir.replace(os.sep, '/')

    print("IIIIIIIII: ",newPath)
    filename = newPath + str(record.voice_record)
    # print("UUUUUUUUUUUUU: ",settings.BASE_DIR)
    # filename = os.path.join(settings.BASE_DIR_NEW, str(record.voice_record))
    # filename = record.voice_record
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX : ",filename)
    # out = os.path.join(settings.MEDIA_ROOT, str('out2.wav'))
    
    # filename = os.path.join(settings.MEDIA_ROOT, str(record.voice_record))
    re = upload_file(filename,header)
    file_url = re['upload_url']

    TRANSCRIPT_ENDPOINT = transcript_endpoint

    response = requests.post(
    TRANSCRIPT_ENDPOINT,
    headers={'authorization': api_key, 'content-type': 'application/json'},
    json={
        'audio_url': file_url,
        'sentiment_analysis': True
    },
    )
    response_json = response.json()
    id_ = response_json['id']



    context = {
        "page_title": "Recorded audio detail",
        "record": record,
        "text": 'text',
        "id_": id_
    }
    return render(request, "voice_record/record_detail.html", context)
    


    # context = {
        
    #     }
    # # return render(request, "voice_record/record.html", context)
    # return render(request, "voice_record/new_record.html", context)










import os

def record_detail(request, id):
    record = get_object_or_404(Record, id=id)
    base_dir = str(settings.BASE_DIR)

    # path = "C:\\temp\myFolder\example\\"
    newPath = base_dir.replace(os.sep, '/')

    print("IIIIIIIII: ",newPath)
    filename = newPath + str(record.voice_record)
    # print("UUUUUUUUUUUUU: ",settings.BASE_DIR)
    # filename = os.path.join(settings.BASE_DIR_NEW, str(record.voice_record))
    # filename = record.voice_record
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX : ",filename)
    # out = os.path.join(settings.MEDIA_ROOT, str('out2.wav'))
    
    # filename = os.path.join(settings.MEDIA_ROOT, str(record.voice_record))
    re = upload_file(filename,header)
    file_url = re['upload_url']

    TRANSCRIPT_ENDPOINT = transcript_endpoint

    response = requests.post(
    TRANSCRIPT_ENDPOINT,
    headers={'authorization': api_key, 'content-type': 'application/json'},
    json={
        'audio_url': file_url,
        'sentiment_analysis': True
    },
    )
    response_json = response.json()
    id_ = response_json['id']



    context = {
        "page_title": "Recorded audio detail",
        "record": record,
        "text": 'text',
        "id_": id_
    }
    return render(request, "voice_record/record_detail.html", context)




def split2(list_a, chunk_size):

  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

def unique(list1):
    npArray1 = np.array(list1)
    uniqueNpArray1 = np.unique(npArray1)
    return uniqueNpArray1.tolist()


def text(request,id):
    
    id_ = id
    api_key = '92d481b159ef4c93a3e0fb9c81942306'

    TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript/' + str(id_)



    response = requests.get(
    TRANSCRIPT_ENDPOINT,
    headers={'authorization': api_key},
    )

    response_json = response.json()
    text = response_json['text']
    print("LLLLLLLLLL: ", text)


    total_words = ''
    total_mistaks = ''
    unique_words = ''
    total_rare_words = ''
    total_common_words = ''
    new_dict = {}
    display = '0'
    # text2 = ''
    if str(text) == "None" or str(text) == "":
        display = '1'
        text2 = "We are converting your voice to text. click on 'Show Now' after 5 seconds"
        text = ''


    # text = '''In early FY23, Pakistan’s economy was undergoing an overdue adjustment, as it recovered from the impacts of COVID-19. Supported by accommodative macroeconomic policies, the economy expanded by 6.0 percent in FY22. Strong domestic demand, coupled with low productivity growth, high world commodity prices, and the global economic slowdown contributed to severe external imbalances. To stabilize the economy, the Government began implementing a range of policies to constrain aggregate demand, including a contractionary budget and increases in administered energy prices. As a result of stabilization measures, growth was expected to slow, the exchange rate was expected to stabilize, total public debt was expect to decline gradually from current high levels, while foreign exchange reserves were expected to slowly accumulate.
    # Recent floods have had enormous human and economic impacts. Pakistan has been experiencing heavy monsoon rains since June 2022 leading to catastrophic and unprecedented flooding. Almost 15% of the country are underwater and just over 33 million peoples are affected. More than 2 million houses have been damaged or destroyed. Loss of life has also been considerable with 1,700 fatalities report to date. Loss of livestock is also significant with more than 1.1 million animals estimated to have perished, while over 25,000 animal shelters have been damaged. More than 13,000 km of roads is reported to have been affected and 440 bridges have been damaged or destroyed, with these number expected to rise. Economic impacts are concentrate in the agricultural sector, with over 9.4 million acres of cultivated land destroyed, resulting in significant losses to cotton, date, wheat, and rice crops. Lower agriculture output is expected to negatively impact industrial and services sector activity, especially given textile sector reliance on cotton (textiles account for around 25 percent of industrial output). Flooding will impose a lingering drag on output through infrastructure damage, disruption to crop cycles, possible financial sector impacts (microfinance institutions report major solvency problems), and loss of human capital. Preliminary estimates suggest that as a direct consequence of the flood, the national poverty rate will increase by 2.5 to 4.0 percentage points, pushing between 5.8 and 9.0 million people into poverty.'''
    words_list = text.strip().split(' ')
    # if str(text) != "None":

    words_list = text.strip().split(' ')
    total_words = len(words_list)

    all_ =  str(text).split(' ')
    chunk_size = 50
    my_list = all_
    new_text = list(split2(my_list, chunk_size))


    total_mistaks = 0

    for i in new_text:
        print(len(i))
        new_txt = ' '.join(i)
        # print(new_txt)
        parser = GingerIt()
        correct_text = parser.parse(new_txt)
        print(correct_text)

        try:
            total_mistaks += len(correct_text['Corrections'])
        except:
            total_mistaks += len(correct_text['corrections'])

    s = unique(words_list)
    unique_words = len(s)

    _5000_english = os.path.join(settings.MEDIA_ROOT, str('5000_english_words.txt'))
    with open(_5000_english) as file_in:
        lines = []
        for line in file_in:
            lines.append(line)

    lines = [x.replace('\n','') for x in lines]

    rare_words = []
    for i in words_list:
        if i not in lines:
            rare_words.append(i)

    total_rare_words = len(rare_words)

    _2000_english = os.path.join(settings.MEDIA_ROOT, str('2000_english_words.txt'))
    with open(_2000_english) as file_in:
        lines2 = []
        for line in file_in:
            lines2.append(line)

    lines2 = [x.replace('\n','') for x in lines2]

    common_word = []
    for i in words_list:
        if i in lines2:
            common_word.append(i)

    total_common_words = len(common_word)

    dict_of_counts = {item:words_list.count(item) for item in words_list}


    new_dict = {}
    for k,l in dict_of_counts.items():
        if l >= 3:
            new_dict[k] = l


        

    

    context = {'text':text,'total_words':total_words, 'total_mistaks':total_mistaks, 'unique_words':unique_words, 
    'total_rare_words':total_rare_words, 'total_common_words':total_common_words, 'repetation':new_dict,
    'display' : display, 'text2' : text2
    
    }
    return render(request, "voice_record/index.html", context)
    