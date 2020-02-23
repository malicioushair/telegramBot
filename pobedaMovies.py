import urllib, json
from datetime import date, datetime


def reloadData():
    currentDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    url = "https://vpobede.ru/backend/api/event/events?type=type_movie&_lastSessions=1&startTime=" + currentDate + "&_scope=list_20&_sort%5Bsession%5D=asc&_limit=100"
    response = urllib.request.urlopen(url)
    jsonData = json.loads(response.read())
    return jsonData

def getMovieNames(data):
    result = []
    for item in data:
        result.append(item["name"])
    return result

def getNamesByDate(data, date, subs = False):
    result = []
    for item in data:
        for performance in item["performances"]:
            for session in performance["sessions"]:
                userDate = datetime.strptime(date, '%d.%m')
                sessionDate = datetime.strptime(session["startTime"], '%Y-%m-%dT%H:%M:%S%z')
                if (userDate.day == sessionDate.day or userDate.month == sessionDate.month) and subs and performance["sessionSubtitles"]:
                    result.append(item["name"] + " " + sessionDate.strftime('%H:%M') + " price:  " + str(session["maxPrice"]) + " subs: " + str(performance["sessionSubtitles"]))
                elif (userDate.day == sessionDate.day or userDate.month == sessionDate.month) and not subs:
                    result.append(item["name"] + " " + sessionDate.strftime('%H:%M') + " price:  " + str(session["maxPrice"]))
    return result