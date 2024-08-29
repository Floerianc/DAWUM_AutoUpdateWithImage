import requests, datetime, matplotlib.pyplot as plt, time
from discord_webhook import DiscordWebhook, DiscordEmbed

DAWUMAPIURL = 'https://api.dawum.de/'

def initialize():
    data = requests.get(DAWUMAPIURL).json()
    keys = list(data['Surveys'].keys())
    MRS = data['Surveys'][f"{keys[0]}"]

    return data, keys, MRS

def compareLastSurveyData(keys):
    with open("mrs_key.key", "r", encoding="UTF-8") as kf:      # kf = key file
        key = kf.read()
        if key == keys[0]:
            print(f"Keine neuen Wahlergebnisse gefunden\nHour: {datetime.datetime.now().hour}\nOld Key: {key}\tNew Key: {keys[0]}")
            return False
        else:
            print(f"Wahlergebnisse werden aktualisiert... {datetime.datetime.now()}")
            with open("mrs_key.key", "w", encoding="UTF-8") as kf:
                kf.write(keys[0])
            
            return True

def parseResults(MRS):
    resultsDAWUM = MRS['Results']
    
    results = []
    
    for key in resultsDAWUM.keys():
        partyName = data['Parties'][f"{key}"]["Name"]
        abbreviation = data['Parties'][f"{key}"]['Shortcut']
        percentage = resultsDAWUM[f"{key}"]
        
        results.append((partyName, abbreviation, percentage))
    return results

def buildGraph(results):
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    
    names = []
    values = []

    for i in range(len(results)):
        names.append(results[i][1])
        values.append(results[i][2])
    
    filename = f'image_folder/{day}.{month}.png'
    
    fig, ax = plt.subplots(figsize=(7.000, 4.000), dpi=100)
    ax.pie(values, labels=names, autopct='%1.1f%%')
    
    plt.savefig(filename, dpi=1000)
    return filename

def prepareMessage():
    date = MRS["Date"] # Gets date of first Survey
    surveyed_people = MRS["Surveyed_Persons"] # How many people contributed
    parliament_ID = MRS["Parliament_ID"] # Parliament ID
    institute_ID = MRS["Institute_ID"] # usw...
    parliament_name = data["Parliaments"][f"{parliament_ID}"]["Name"]
    institute_name = data["Institutes"][f"{institute_ID}"]["Name"]
    return parliament_ID, institute_ID, date, parliament_name, institute_name, surveyed_people

def buildMessage(results, filename):
    p, i, d, pn, insn, sp = prepareMessage()
    
    def get_url():
        # https://dawum.de/Europawahl/Forschungsgruppe_Wahlen/2024-05-30/
        parliament_url = data["Parliaments"][f"{p}"]["Election"]
        institute_url = i.replace(" ", "_")
        mrs_url = f"https://dawum.de/{parliament_url}/{institute_url}/{d}"
        return mrs_url
    
    mrsURL = get_url()

    resultsSTR = ""
    content = f"Parlament: **{pn}**\nInstitut: **{insn}**\nDatum: **{d}**\nAnzahl befragte Personen: **{sp}**\n# __Ergebnisse__\n"

    for i in range(len(results)):
        if i == 0:
            heading = "#"*(i+3) # a hashtag '#' in a discord message makes the font size bigger, so the top 1 party have a bigger font than the rest.
        else:
            heading = "" # if the party is not in the top 1, the texts size will be normal
        
        resultsSTR += f"\n> {heading} **{i+1}.** {results[i][0]} *({results[i][1]}):* {results[i][2]}%"
    resultsSTR += f"\n\nUm die Ergebnisse nochmal auf der offiziellen DAWUM-Website einzusehen, klicken Sie [hier.]({mrsURL})"

    content = content + resultsSTR # combines date, surveyed people, parliament, institute and the results into one big string

    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1245098208028397661/4kGA9gaAdBJIF9bKg_Xj_byjQ7D8DJvtCE2Vpn-6y-2uA0R7FSamGyVhHO43ENDmPGLv") # sets up a Discord Webhook
    embed = DiscordEmbed(title="NEUESTE WAHLERGEBNISSE", description=content, color="ff0313") # creates a Discord Embed

    with open(filename, "rb") as f:
        webhook.add_file(file=f.read(), filename=filename)
    
    webhook.add_embed(embed)
    response = webhook.execute() # sends the message
    return

if __name__ == "__main__":
    while True:
        hour = datetime.datetime.now().hour
        
        if hour > 8:
            data, keys, MRS = initialize()
            if compareLastSurveyData(keys):
                results = parseResults(MRS)
                filename = buildGraph(results)
                buildMessage(results, filename)
        time.sleep(1500)