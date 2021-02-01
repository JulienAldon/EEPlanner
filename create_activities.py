import json
import csv
import datetime
from datetime import timedelta
import pprint
import requests
import browsercookie
import statistics
import copy
from bs4 import BeautifulSoup

attendance_list = []
dict_attendance = {}
all_sessions = []
url_create_activity = "https://intra.epitech.eu/module/2020/B-INN-000/LYN-0-1/create?format=json"
url_hub = "https://intra.epitech.eu/module/2020/B-INN-000/LYN-0-1/"
cj = browsercookie.load()

# <option value="12544">Talk</option>
# <option value="58">Workshop</option>
# <option value="44">Project</option>
# <option value="12547">Experience</option>
# <option value="12546">Hackathon</option>

def get_id_activities():

    r_activities = requests.get("https://intra.epitech.eu/module/2020/B-INN-000/LYN-0-1/numbycategory?format=json",cookies=cj)

    for key,value in r_activities.json().items():
        list_id = []
        if key == "12544":
            for i in value:
                list_id.append(int(i))
            id_talk = int(max(list_id)) + 1
        if key == "58":
            for i in value:
                list_id.append(int(i))
            id_workshop = int(max(list_id)) + 1
        if key == "44":
            for i in value:
                list_id.append(int(i))
            id_project = int(max(list_id)) + 1
        if key == "12547":
            for i in value:
                list_id.append(int(i))
            id_experience = int(max(list_id)) + 1
        if key == "12546":
            for i in value:
                list_id.append(int(i))
            id_hackathon = int(max(list_id)) + 1

    return id_talk, id_workshop, id_project, id_experience, id_hackathon


if __name__ == '__main__':

    id_talk, id_workshop, id_project, id_experience, id_hackathon = get_id_activities()

    type_activity            = input("Please enter the type of activity (T/W/P/E/H)     : ")
    date_activity            = input("Please enter the date of activity (%Y-%m-%d %H)   : ")
    custom_duration_activity = input("Please enter the duration of activity (in hours)  : ")
    title_activity           = input("Please enter the title of activity (# auto added) : ")

    if type_activity == "T":
        category_id_activity = "12544"
        id_activity = id_talk
        tag_activity = "#TALK"
        search_tag = "Talk"
        duration_activity = 1
    elif type_activity == "W":
        category_id_activity = "58"
        id_activity = id_workshop
        tag_activity = "#WORKSHOP"
        search_tag = "Workshop"
        duration_activity = 3
    elif type_activity == "P":
        category_id_activity = "44"
        id_activity = id_project
        tag_activity = "#PROJECT"
        search_tag = "Project"
        duration_activity = 1
    elif type_activity == "E":
        category_id_activity = "12547"
        id_activity = id_experience
        tag_activity = "#EXPERIENCE"
        search_tag = "Experience"
        duration_activity = 1
    elif type_activity == "H":
        category_id_activity = "12546"
        id_activity = id_hackathon
        tag_activity = "#HACKATHON"
        search_tag = "Hackathon"
        duration_activity = 3

    date_activity = datetime.datetime.strptime(date_activity, '%Y-%m-%d %H')

    if custom_duration_activity:
        duration_activity = custom_duration_activity

    duration_activity = int(duration_activity)


    title_activity = ' '.join([tag_activity,title_activity])

    begin = date_activity.strftime("%Y-%m-%d %H:00:00")
    end = (date_activity + timedelta(hours=duration_activity)).strftime("%Y-%m-%d %H:00:00")


    print(title_activity)
    print("{:02d}:00".format(duration_activity))
    print(begin)
    print(end)


    actity_creation = requests.post('https://intra.epitech.eu/module/2020/B-INN-000/LYN-0-1/create?format=json', 
        data = {
        'category[id]': category_id_activity,
        'nb_group': "1",
        'num': id_activity,
        'begin': begin,
        'end': end,
        'nb_hours': "{:02d}:00".format(duration_activity),
        'register': "1",
        'title[en]': title_activity,
        'instanciation_multiple':"1",
        }, 
        cookies=cj)

    # print(actity_creation.text)

    if actity_creation.status_code == 200:

        page = requests.get(url_hub, cookies=cj)
        soup = BeautifulSoup(page.content, 'html.parser')

        for li in soup.findAll("li", class_="activite"):
            for span3 in li.findAll("span", class_="categ"):
                categorie = span3.text.strip().split(' ')
                if categorie[0] == search_tag and int(categorie[1]) == id_activity:
                    for div in li.findAll("div", class_="main"):
                        for link_div in div.findAll("div", class_="project"):
                            for link_a in link_div.findAll("a"):
                                link = url_hub+link_a['href'] #link
                                link = link.replace('#!/group','?format=json')
                    print(link)
                    link_acti = link.replace('project/?format=json','')

                    actity_planify = requests.post(link_acti+'planify?format=json', 
                        data = {
                            'start': begin,
                            'location': "FR/LYN/Virtuel/Teams",
                            'type': "salle_machine",
                            }, 
                        cookies=cj)
                    print(actity_planify)


    # else:
    #     print(actity_creation.text)



