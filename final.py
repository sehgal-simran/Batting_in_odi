from bs4 import BeautifulSoup
import requests

#setting file up
filename="Batting-runs-in-ODIs.csv"
f= open(filename, "w")

#making headers of file
headers="Player Name,"
for x in range(0,50):
    theyearis=x+1970
    thecharyearis=str(theyearis)+","
    headers+=thecharyearis
f.write(headers)
f.write("\n")

#constructing headers
url_base='http://www.howstat.com/cricket/Statistics/Players/PlayerBatGraph.asp?PlayerID='
url_end='&c=ODI'


#for loop to make url for player 1-19, 
for index in range(1,6000):
    id=str(index)
    new_id=id.zfill(4)
    the_url=url_base+new_id+url_end
    url = requests.get(the_url)
    soup= BeautifulSoup(url.content, "html.parser")
    #checking if we have an odi player, good link
    firstcheck=soup.html.head.title.text.split(' ')[1]
    if firstcheck == 'Error':
        continue

    veracity=soup.html.head.title.text.split('-')[2]
    if veracity !=' Batting Graph':
        continue

    #finding player name
    playername=soup.find("a","LinkOff")
    player=playername.text.split('-')[0]

    #making container of all matches played by him
    containers= soup.findAll('area', shape="rect")

    year=0
    prevyear=-1
    aggregate= [0]*50

    #extracting the year of matches and aggregate runs in that year
    for container in containers:
        playerstring=container["alt"]
        dirtyyear=container.attrs['alt'].split('\r\n')[1]
        hadabathyear=dirtyyear.split('\t\t')
        cleanyear=hadabathyear[1].split('/')[2]
        cleanyear
        cleanestyear=cleanyear.split(' ')[0]
        cleanestyear
        year=int(cleanestyear)-1970
        if year<0:
            continue

        dirtyruns= container.attrs['alt'].split('\r\n')[2]
        hadabathruns=dirtyruns.split('\t\t')[1]
        cleanruns=hadabathruns.split('*')[0]
        run=int(cleanruns)

        if year==prevyear:
        
            aggregate[year]+=run
        else:
            aggregate[year]=aggregate[year-1]
            aggregate[year]+=run

        prevyear=year
       
    f.write(player+",")
    aggregate_print= [0]*50
    for i in range(0,50):
        aggregate_print[i]=str(aggregate[i])
        f.write(aggregate_print[i]+",")
    f.write("\n")
   
f.close
