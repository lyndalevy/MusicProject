import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from collections import Counter

client_id = '0314a2282eb3470d9ab666ac305108a3'
client_secret = 'a74e9a59716e45628c08a706614c671d'
redirect_uri = 'http://localhost:8888/callback/'
scope = 'playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def line():
    print("--------------------------------------------------------------------------------")

def dottedLine():
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

def makePlaylist(songsList, playlistName, playlistDescription, printBool):
    userId = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=userId, name=playlistName, public=True, description=playlistDescription)
    print(f"Creating playlist: {playlist['name']}")
    trackIds = getTrackIds(songsList, printBool)
    chunkSize = 100
    for trackChunk in chunkList(trackIds, chunkSize):
        sp.playlist_add_items(playlist_id=playlist['id'], items=trackChunk)
    print("Tracks added to playlist.")

def chunkList(bigList, chunkSize):
    for i in range(0, len(bigList), chunkSize):
        yield bigList[i:i + chunkSize]

def getTrackIds(songsList, printBool):
    trackIds = []
    
    print("Adding songs...")
    for song, artist in songsList:
        song_clean = song.strip()
        artist_clean = artist.strip()
        query = f"{song_clean} {artist_clean}"
        if printBool:
            print(f"{song_clean} - {artist_clean}")
        try:
            results = sp.search(q=query, limit=1, type='track')
            if not results['tracks']['items']:
                results = sp.search(q=f"track:{song_clean}", limit=1, type='track')
            if results['tracks']['items']:
                trackId = results['tracks']['items'][0]['id']
                trackIds.append(trackId)
            else:
                print(f"Song '{song_clean}' by '{artist_clean}' not found on Spotify.")
        except Exception as e:
            print(f"Error searching for '{song_clean}' by '{artist_clean}': {e}")
    return trackIds

def csvToTuples(filePath):
    if not os.path.isfile(filePath):
        print(f"Error: {filePath} does not exist.")
        return None
    try:
        with open(filePath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            dataList = [tuple(row[:3]) for row in reader]
    except Exception as e:
        print(f"Error reading {filePath}: {e}")
        return None
    return dataList

def getPerson(peopleList, personName, listOfLists):
    if len(peopleList) == 1:
        personName = str(peopleList[0])
        number = 0
        for i in range(len(peopleList)):
            if personName == peopleList[number]:
                personList = listOfLists[number]
            number += 1
    else:
        personName = input(f"Who is the  person for the playlist?\nChoose from these options: {peopleList}: ")
        number = 0
        for i in range(len(peopleList)):
            if personName == peopleList[number]:
                personList = listOfLists[number]
            number += 1
    return personList, personName

def printList(listToPrint):
    number = 0
    for song in range(len(listToPrint)):
        print(f"{listToPrint[number][0]}, {listToPrint[number][1]}")
        number += 1

def appearing(songList, popularNumber):
    songCounts = {}
    for song in songList:
        if song in songCounts:
            songCounts[song] += 1
        else:
            songCounts[song] = 1
    sortedList = [[song, count] for song, count in songCounts.items()]
    sortedListPopular = []
    if popularNumber == 0:
        return sortedList
    else:
        number = 0
        for song in sortedList:
            if sortedList[number][1] >= popularNumber:
                sortedListPopular.append(song)
            number += 1
        return sortedListPopular

def blend(peopleList, listOfLists):
    if len(peopleList) == 2: #2 people selected
        person1Name = str(peopleList[0])
        person1List = []
        number = 0
        for i in range(len(peopleList)):
            if person1Name == peopleList[number]:
                person1List = listOfLists[number]
            number += 1
        person2Name = str(peopleList[1])
        person2List = []
        number = 0
        for i in range(len(peopleList)):
            if person2Name == peopleList[number]:
                person2List = listOfLists[number]
            number += 1
    else: #choose 2 people
        person1Name = input(f"Who is the first person for the blend?\nChoose from these options: {peopleList}: ")
        person1List = []
        number = 0
        for i in range(len(peopleList)):
            if person1Name == peopleList[number]:
                person1List = listOfLists[number]
            number += 1
        peopleList2 = peopleList.copy()
        peopleList2.remove(person1Name)
        person2Name = input(f"Who is the second person for the blend?\nChoose from these options: {peopleList2}: ")
        person2List = []
        number = 0
        for i in range(len(peopleList)):
            if person2Name == peopleList[number]:
                person2List = listOfLists[number]
            number += 1
    popularNumber = int(input("How many listens should a song for it to be in the playlist? "))
    dottedLine()
    person1List = [(item[0], item[1]) for item in person1List]
    person2List = [(item[0], item[1]) for item in person2List]
    sorted1List = appearing(person1List, popularNumber)
    sorted2List = appearing(person2List, popularNumber)
    combinedList = []
    number = 0
    for song1 in sorted1List:
        for song2 in sorted2List:
            if song1[0] == song2[0]:
                combinedList.append(sorted1List[number][0])
                break
        number += 1
    number = 0
    for song in combinedList:
        if combinedList[number] == ('', ''):
            combinedList.remove(combinedList[number])
        number += 1
    makePlaylist(combinedList, f" The {person1Name.title()} {person2Name.title()} Mix", "Made with my code!", True)
    line()
    
def topArtist(peopleList, listOfLists):
    personList = []
    personName = ""
    personList, personName = getPerson(peopleList, personName, listOfLists)
    number = 0
    personList = [(item[0], item[1]) for item in personList]
    artistName = str(input("Enter artist's name: "))
    foundArtist = False
    dottedLine()
    songListOnce = []
    songListAll = []
    for song in personList:
        if artistName in song[1]:
            foundArtist = True
            songListAll.append(song[0])
            if song[0] not in songListOnce:
                songListOnce.append(song[0])
    listUnsortedSongs = []
    number = 0
    for song in songListOnce:
        songCount = songListAll.count(song)
        listUnsortedSongs.append([songCount, song])
        number += 1
    if not foundArtist:
        print("No songs found by this specific artist.")
    else:
        listSortedSongs = sorted(listUnsortedSongs, key=lambda x: x[0], reverse=True)
        makePlaylistList = []
        number = 0
        for song in listSortedSongs:
            makePlaylistList.append([listSortedSongs[number][1], artistName])
            number += 1
        makePlaylist(makePlaylistList, f"{personName.title()}'s top songs by {artistName}", "Made with my code!", False)
        number = 0
        for song in listSortedSongs:
            print(f"{listSortedSongs[number][1]}, {listSortedSongs[number][0]} times")
            number += 1
    line()

def topSongs(peopleList, listOfLists):
    personList = []
    personName = ""
    personList, personName = getPerson(peopleList, personName, listOfLists)
    personList = [(item[0], item[1]) for item in personList]
    topNumber = int(input("How many of your top songs would you like to see? "))
    unsortedList = appearing(personList, 3)
    sortedList = sorted(unsortedList, key=lambda x: x[1], reverse = True)
    number = 0
    for song in sortedList:
        if sortedList[number][0] == ('', ''):
            sortedList.remove(sortedList[number])
        number += 1
    line()
    makePlaylistlist = []
    number = 0
    for song in range(topNumber):
        makePlaylistlist.append(sortedList[number][0])
        number += 1
    makePlaylist(makePlaylistlist, f"{personName.title()}'s top {topNumber} songs", "Made with my code!", False)
    number = 0
    for song in range(topNumber):
        print(f"{sortedList[number][0][0]} - {sortedList[number][0][1]}, {sortedList[number][1]} times")
        number += 1
    line()

def hebrewOnly(peopleList, listOfLists):
    personList = []
    personName = ""
    personList, personName = getPerson(peopleList, personName, listOfLists)
    personList = [(item[0], item[1]) for item in personList]
    personHebrewList = []
    artistNameList = []
    number = 0
    for song in personList: #find hebrew characters in song names
        songName = personList[number][0]
        artistName = personList[number][1]
        try:
            if ord(songName[0]) >= 0x0590 and ord(songName[0]) <= 0x05FF:
                if personList[number] not in personHebrewList:
                    personHebrewList.append(personList[number])
                    artistList = []
                    artistList = personList[number][1].split(", ")
                    for artist in artistList:
                        if artist not in artistNameList:
                            artistNameList.append(personList[number][1])
        except IndexError:
            break
        try:
            if ord(artistName[0]) >= 0x0590 and ord(artistName[0]) <= 0x05FF:
                if personList[number][1] not in personHebrewList:
                    personHebrewList.append(personList[number])
                    if personList[number][1] not in artistNameList:
                        artistNameList.append(personList[number][1])
        except IndexError:
            break
        number += 1
    number = 0
    for song in personList: #find all songs by artists w hebrew songs
        for artist in artistNameList:
            if artist in personList[number][1]:
                try:
                    if personList[number] not in personHebrewList:
                        personHebrewList.append(personList[number])
                except IndexError:
                    break
        number += 1
        """
    print(personName.title() + "'s Hebrew songs:")
    printList(personHebrewList)
    """
    makePlaylist(personHebrewList, f"{personName.title()}'s Hebrew songs", "Made with my code!", True)
    line()

def date(peopleList, listOfLists):
    personList = []
    personName = ""
    personList, personName = getPerson(peopleList, personName, listOfLists)
    personListNoDates = [(item[0], item[1]) for item in personList]
    date = input("Enter the date you'd like to see made into a playlist(YYYY-MM-DD): ")
    playlist = []
    number = 0
    dateFound = False
    for song in personList:
        if date in personList[number][2]:
            playlist.append(personListNoDates[number])
            dateFound = True
        else:
            if dateFound == True:
                break
        number += 1
    dateList = date.split("-")
    playlistTitle = dateList[1] + dateList[2] + dateList[0]
    makePlaylist(playlist, f"{playlistTitle}", "Made with my code!", True)
    line()

def main():
    print("Welcome to Lynda's Spotify Data sorter!") #make it not case sensitive
    line()
    print("Who's data will you need in this code? Options are Lynda, LJ, Nini, and Sivan.")
    peopleString = (input("Write 'all' for all, if not, write their names separeted by spaces: ")).lower()
    peopleList = peopleString.split()
    listOfLists = []
    dottedLine()
    if "all" in peopleList:
        lynda = makeLynda()
        listOfLists.append(lynda)
        lj = makeLJ()
        listOfLists.append(lj)
        nini = makeNini()
        listOfLists.append(nini)
        sivan = makeSivan()
        listOfLists.append(sivan)
        peopleList = ["lynda", "lj", "nini", "sivan"]
    else:
        if "lynda" in peopleList:
            lynda = makeLynda()
            listOfLists.append(lynda)
        if "lj" in peopleList:
            lj = makeLJ()
            listOfLists.append(lj)
        if "nini" in peopleList:
            nini = makeNini()
            listOfLists.append(nini)
        if "sivan" in peopleList:
            sivan = makeSivan()
            listOfLists.append(sivan)
    programStatus = True
    while programStatus == True:
        print("What would you like to do?")
        print("     For a blended playlist, type 'blend'")
        print("     For a top playlist of a certain artist, type 'top artist'")
        print("     For someome's top songs, type 'top songs'")
        print("     For someone's Hebrew songs, type 'hebrew'")
        print("     For what someone listend to on a certain day, type 'date'")
        print("     To stop, type 'quit'")
        answer = input("Type here: ")
        line()
        if answer == "blend":
            if len(peopleList) == 1:
                print ("Cannot make blended playlist with one person")
                line()
            else:
                print("Making blended playlist...")
                blend(peopleList, listOfLists)
        elif answer == "top artist":
            print("Making top artist playlist...")
            topArtist(peopleList, listOfLists)
        elif answer == "hebrew":
            print("Making Hebrew playlist...")
            hebrewOnly(peopleList, listOfLists)
        elif answer == "top songs":
            print("Making top song playlist...")
            topSongs(peopleList, listOfLists)
        elif answer == "date":
            print("Making date playlist...")
            date(peopleList, listOfLists)
        elif answer == "quit":
            print("Done")
            dottedLine()
            programStatus = False
        else:
            print("Type in a valid code word please")
            line()

def makeLynda():
    lynda = []
    print("Gathering Lynda's data...")
    #lynda += csvToTuples("L 18-21.csv")
    lynda += csvToTuples("L 21-22.csv")
    lynda += csvToTuples("L 22-23.csv")
    lynda += csvToTuples("L 23.csv")
    lynda += csvToTuples("L 23-24.csv")
    lynda += csvToTuples("L 24.csv")
    lynda += csvToTuples("L 24 2.csv")
    print("Lynda's data gathered successfully!")
    dottedLine()
    return lynda

def makeLJ():
    lj = []
    print("Gathering LJ's data...")
    lj += csvToTuples("LJ 16-17.csv")
    lj += csvToTuples("LJ 17-18.csv")
    lj += csvToTuples("LJ 18.csv")
    lj += csvToTuples("LJ 18-19.csv")
    lj += csvToTuples("LJ 19.csv")
    lj += csvToTuples("LJ 19-20.csv")
    lj += csvToTuples("LJ 20-21.csv")
    lj += csvToTuples("LJ 21.csv")
    lj += csvToTuples("LJ 21 2.csv")
    lj += csvToTuples("LJ 21-22.csv")
    lj += csvToTuples("LJ 22.csv")
    lj += csvToTuples("LJ 22 2.csv")
    lj += csvToTuples("LJ 22 3.csv")
    lj += csvToTuples("LJ 22 4.csv")
    lj += csvToTuples("LJ 22-23.csv")
    lj += csvToTuples("LJ 23.csv")
    lj += csvToTuples("LJ 23 2.csv")
    lj += csvToTuples("LJ 23 3.csv")
    lj += csvToTuples("LJ 23-24.csv")
    lj += csvToTuples("LJ 24.csv")
    lj += csvToTuples("LJ 24 2.csv")
    print("LJ's data gathered successfully!")
    dottedLine()
    return lj

def makeNini():
    nini = []
    print("Gathering Nini's data...")
    nini += csvToTuples("N 20.csv")
    nini += csvToTuples("N 20-22.csv")
    nini += csvToTuples("N 22-23.csv")
    nini += csvToTuples("N 23.csv")
    nini += csvToTuples("N 23-24.csv")
    nini += csvToTuples("N 24.csv")
    nini += csvToTuples("N 24 2.csv")
    nini += csvToTuples("N 24 3.csv")
    print("Nini's data gathered successfully!")
    dottedLine()
    return nini

def makeSivan():
    sivan = []
    print("Gathering Sivan's data...")
    sivan += csvToTuples("S 21.csv")
    sivan += csvToTuples("S 21-22.csv")
    sivan += csvToTuples("S 22.csv")
    sivan += csvToTuples("S 22 2.csv")
    sivan += csvToTuples("S 22-23.csv")
    sivan += csvToTuples("S 23.csv")
    sivan += csvToTuples("S 23 2.csv")
    sivan += csvToTuples("S 23-24.csv")
    sivan += csvToTuples("S 24.csv")
    sivan += csvToTuples("S 24 2.csv")
    print("Sivan's data gathered successfully!")
    dottedLine()
    return sivan
        
main()
