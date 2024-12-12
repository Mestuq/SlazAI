import random
import iniLoad

# Check if conditions of auto-answear are fulfilled
# arguments:
# prev - if condition is not meed, return this string
# mess - table of words (message of user)
# requir - required words to meet requirements
# answ - table of answears (strings) if conditions is meet (bot will take one string of table at random)
def auto_resp(perv,mess,requir,answ):
    for req in requir:
        fulfills=False
        for mes in mess:
            if req == mes:
                fulfills=True
        if fulfills == False:
            return perv
    return random.choice(answ)

# Random joke function. Returns string
def randomjoke(channel):
    los = random.randint(0,2)
    if los == 0:
        return ['Dlaczego trzyletnie nieszczepione dziecko płacze?','Bo przechodzi kryzys wieku średniego']
    elif los == 1:
        return ['Dlaczego choinka nie jest głodna?','Bo jodła']
    elif los==2:
        return ['']

# Banned words in username. (Automoderator)
def blacklist_usernames(tabela):
    resp = ''
    resp = auto_resp(resp,tabela,['twitter','com','h0nde'],['ban'])
    return resp
    
# Clever answears list. string '' means no message.
def response_list(tabela,tabela_pierwotna,channel,guild,message,client):
    
    # List of possible bot responses
    listOfResponses = [
        [['version'],['1.5 AI']],
        [['<@','!','40543924654820569>'],['Nie pinguj pajacu','No nie wytrzymam, nie pinguj gnoju']],
        [['@everyone'],['No brawo','Ktoś, coś ban?','JPRDL']],
        [['witam'],['Hejka','Cześć','Elo']],
        [['cześć'],['Hejka','Cześć','Elo']],
        [['hej'],['No hejka']],
        [['dobranoc'],['Śpij dobrze']],
        [['f'],['[*]']],
        [['nasze'],['\"Ours\" \n https://cdn.discordapp.com/attachments/801861475395698740/801861585097981972/nasze.png']],
        [['pog'],['https://cdn.discordapp.com/attachments/801861475395698740/801861857706639400/pogchamp.png']],
        [['lubisz','mnie','?'],['No homo','Nie pajacu','Spierdalaj','To zależy','Oczywiście gnojku']],
        [['ślazatek','inteligentny'],['Dokładnie']],
        [['ślazatek','inteligentny','nie'],['Spierdalaj']],
        [['ślazatek','głupi'],['Spierdalaj']],
        [['rze'],['Za takie błędy ortograficzne powinien być ban']],
        [['kture'],['Za takie błędy ortograficzne powinien być ban']],
        [['napewno'],['*Na pewno się pisze pajacu']],
        [['wogóle'],['Tak \"Wogóle\" to ty możesz bana dostać']],
        [['wogule'],['Tak \"Wogule\" to ty możesz bana dostać']],
        [['narazie'],['pisze się \" na razie\"']],
        [['muj'],['\"muj\" mózg nie wytrzyma jak widze twoje błędy']],
        [['niewiem'],['kurła, orto boli']],
        [['wziąść'],['też mogę \"wziąść\"']],
        [['nje'],['*nie']],
        [['takih'],['*takich']],
        [['problemuf'],['*problemów']],
        [['problemuw'],['*problemów']],
        [['dobsze'],['*dobrze']],
        [['tesz'],['*też']],
        [['conajmniej'],['*co najmniej']],
        [['jusz'],['*już']],
        [['niewiem'],['*nie wiem']],
        [['kasztany'],['Orzechy > Kasztany']],
        [['orzechy'],['Orzechy > Kasztany']],
        [['chwasty'],['Pal gumę gnoju']],
        [['chwaście'],['Pal gumę gnoju']],
        [['chwast'],['Pal gumę gnoju']],
        [['ty','kurwo'],['Śmieciu']],
        [['sztorm'],['Właśnie, kiedy sztorm?']],
        [['szturm'],['Właśnie, kiedy sztorm?']],
        [['orange'],['Orange, rusz dupę i rób grę']],
        [['kjedy','fefef'],['Właśnie, kiedy fefef?']],
        [['kiedy','fefef'],['Właśnie, kiedy fefef?']],
        [['kjedy','f'],['Właśnie, kiedy fefef?']],
        [['kiedy','f'],['Właśnie, kiedy fefef?']],
        [['damian','kurwa'],['Kiedy fefef?']],
        [['dałmian','kurwa'],['Kiedy fefef?']],
        [['dałnmian','kurwa'],['Kiedy fefef?']],
        [['sranie'],['Mroczne']],
        [['mroczne'],['Sranie']],
        [['mroczne','granie'],['Mroczne Sranie']],
        [['dałmian'],['Kurwa Dałmian']],
        [['gówno'],['zjedz je równo']],
        [['zjebałeś'],['sam zjebałeś gnoju']],
        [['się','zesrałem'],['To nie dobrze']],
        [['kasztan'],['Kurła kasztan kiedy sztorm']],
        [['szturm'],['*sztorm','chyba miałeś na myśli sztOrm','no chyba sztorm']]
    ]

    # Checking conditions
    resp=''
    #for odp in listOfResponses:
    #    #match is only supported in newer version of python, so i used if's
    #    if len(odp) == 0:
    #        print('One pair is missing in response list')
    #    if len(odp) == 1:
    #        print('One element has no pair:')
    #        print(odp[0])
    #    if len(odp) == 2:
    #        resp = auto_resp(resp,tabela,odp[0],odp[1])

    # Ignore answear if dot is in the message
    resp = auto_resp(resp,tabela,['.'],['']) #Niech ślazatek nie spami, jak ktoś piszę długi wywód

    # Count swaers
    resp = bez_przeklenstw(resp,tabela,message)
    
    # DEBUGING
    resp = auto_resp(resp,tabela_pierwotna,['&debug-p'],[tabela_pierwotna])
    resp = auto_resp(resp,tabela_pierwotna,['&debug'],[tabela])
    
    return resp

# If user swear, add one to his counter. "Licznik.conf" file.
def bez_przeklenstw(resp,tabela,message):
    backupresp=resp
        
    # Count swears in one message
    dodaj_tyle=0
    for w in wulgaryzmy:
        for m in tabela:
            if m == w:
                dodaj_tyle=dodaj_tyle+1
                print("wulgaryzm")
    
    if dodaj_tyle != 0:
        print("analiza")
        # Add to counter
        ile_razy=int(iniLoad.iniLoad('licznik.conf','swears',str(message.author.id),'0'))
        iniLoad.iniChange('licznik.conf','swears',str(message.author.id),str(ile_razy+1))

         # Reminder of round noumber
        if (ile_razy+1)%10 ==0:
            resp='Przypomnienie! Przeklnąłeś już '+str(ile_razy+1)+" raz!"
        else:
            resp=backupresp
        
    return resp

# List of bad words
wulgaryzmy = ['japierdole','jebać','wypierdol','spierdalaj','chuj','chuja', 'chujek', 'chuju', 'chujem', 'chujnia','chujowy', 'chujowa', 'chujowe', 'cipa', 'cipę', 'cipe', 'cipą','cipie', 'dojebać','dojebac', 'dojebie', 'dojebał', 'dojebal','dojebała', 'dojebala', 'dojebałem', 'dojebalem', 'dojebałam','dojebalam', 'dojebię', 'dojebie', 'dopieprzać', 'dopieprzac','dopierdalać', 'dopierdalac', 'dopierdala', 'dopierdalał','dopierdalal', 'dopierdalała', 'dopierdalala', 'dopierdoli','dopierdolił', 'dopierdolil', 'dopierdolę', 'dopierdole', 'dopierdoli','dopierdalający', 'dopierdalajacy', 'dopierdolić', 'dopierdolic','dupa', 'dupie', 'dupą', 'dupcia', 'dupeczka', 'dupy', 'dupe', 'huj','hujek', 'hujnia', 'huja', 'huje', 'hujem', 'huju', 'jebać', 'jebac','jebał', 'jebal', 'jebie', 'jebią', 'jebia', 'jebak', 'jebaka', 'jebal','jebał', 'jebany', 'jebane', 'jebanka', 'jebanko', 'jebankiem','jebanymi', 'jebana', 'jebanym', 'jebanej', 'jebaną', 'jebana','jebani', 'jebanych', 'jebanymi', 'jebcie', 'jebiący', 'jebiacy','jebiąca', 'jebiaca', 'jebiącego', 'jebiacego', 'jebiącej', 'jebiacej','jebia', 'jebią', 'jebie', 'jebię', 'jebliwy', 'jebnąć', 'jebnac','jebnąc', 'jebnać', 'jebnął', 'jebnal', 'jebną', 'jebna', 'jebnęła','jebnela', 'jebnie', 'jebnij', 'jebut', 'koorwa', 'kórwa', 'kurestwo','kurew', 'kurewski', 'kurewska', 'kurewskiej', 'kurewską', 'kurewska','kurewsko', 'kurewstwo', 'kurwa', 'kurwaa', 'kurwami', 'kurwą', 'kurwe','kurwę', 'kurwie', 'kurwiska', 'kurwo', 'kurwy', 'kurwach', 'kurwami','kurewski', 'kurwiarz', 'kurwiący', 'kurwica', 'kurwić', 'kurwic','kurwidołek', 'kurwik', 'kurwiki', 'kurwiszcze', 'kurwiszon','kurwiszona', 'kurwiszonem', 'kurwiszony', 'kutas', 'kutasa', 'kutasie','kutasem', 'kutasy', 'kutasów', 'kutasow', 'kutasach', 'kutasami','matkojebca', 'matkojebcy', 'matkojebcą', 'matkojebca', 'matkojebcami','matkojebcach', 'nabarłożyć', 'najebać', 'najebac', 'najebał','najebal', 'najebała', 'najebala', 'najebane', 'najebany', 'najebaną','najebana', 'najebie', 'najebią', 'najebia', 'naopierdalać','naopierdalac', 'naopierdalał', 'naopierdalal', 'naopierdalała','naopierdalala', 'naopierdalała', 'napierdalać', 'napierdalac','napierdalający', 'napierdalajacy', 'napierdolić', 'napierdolic','nawpierdalać', 'nawpierdalac', 'nawpierdalał', 'nawpierdalal','nawpierdalała', 'nawpierdalala', 'obsrywać', 'obsrywac', 'obsrywający','obsrywajacy', 'odpieprzać', 'odpieprzac', 'odpieprzy', 'odpieprzył','odpieprzyl', 'odpieprzyła', 'odpieprzyla', 'odpierdalać','odpierdalac', 'odpierdol', 'odpierdolił', 'odpierdolil','odpierdoliła', 'odpierdolila', 'odpierdoli', 'odpierdalający','odpierdalajacy', 'odpierdalająca', 'odpierdalajaca', 'odpierdolić','odpierdolic', 'odpierdoli', 'odpierdolił', 'opieprzający','opierdalać', 'opierdalac', 'opierdala', 'opierdalający','opierdalajacy', 'opierdol', 'opierdolić', 'opierdolic', 'opierdoli','opierdolą', 'opierdola', 'piczka', 'pieprznięty', 'pieprzniety','pieprzony', 'pierdel', 'pierdlu', 'pierdolą', 'pierdola', 'pierdolący','pierdolacy', 'pierdoląca', 'pierdolaca', 'pierdol', 'pierdole','pierdolenie', 'pierdoleniem', 'pierdoleniu', 'pierdolę', 'pierdolec','pierdola', 'pierdolą', 'pierdolić', 'pierdolicie', 'pierdolic','pierdolił', 'pierdolil', 'pierdoliła', 'pierdolila', 'pierdoli','pierdolnięty', 'pierdolniety', 'pierdolisz', 'pierdolnąć','pierdolnac', 'pierdolnął', 'pierdolnal', 'pierdolnęła', 'pierdolnela','pierdolnie', 'pierdolnięty', 'pierdolnij', 'pierdolnik', 'pierdolona','pierdolone', 'pierdolony', 'pierdołki', 'pierdzący', 'pierdzieć','pierdziec', 'pizda', 'pizdą', 'pizde', 'pizdę', 'piździe', 'pizdzie','pizdnąć', 'pizdnac', 'pizdu', 'podpierdalać', 'podpierdalac','podpierdala', 'podpierdalający', 'podpierdalajacy', 'podpierdolić','podpierdolic', 'podpierdoli', 'pojeb', 'pojeba', 'pojebami','pojebani', 'pojebanego', 'pojebanemu', 'pojebani', 'pojebany','pojebanych', 'pojebanym', 'pojebanymi', 'pojebem', 'pojebać','pojebac', 'pojebalo', 'popierdala', 'popierdalac', 'popierdalać','popierdolić', 'popierdolic', 'popierdoli', 'popierdolonego','popierdolonemu', 'popierdolonym', 'popierdolone', 'popierdoleni','popierdolony', 'porozpierdalać', 'porozpierdala', 'porozpierdalac','poruchac', 'poruchać', 'przejebać', 'przejebane', 'przejebac','przyjebali', 'przepierdalać', 'przepierdalac', 'przepierdala','przepierdalający', 'przepierdalajacy', 'przepierdalająca','przepierdalajaca', 'przepierdolić', 'przepierdolic', 'przyjebać','przyjebac', 'przyjebie', 'przyjebała', 'przyjebala', 'przyjebał','przyjebal', 'przypieprzać', 'przypieprzac', 'przypieprzający','przypieprzajacy', 'przypieprzająca', 'przypieprzajaca','przypierdalać', 'przypierdalac', 'przypierdala', 'przypierdoli','przypierdalający', 'przypierdalajacy', 'przypierdolić','przypierdolic', 'qrwa', 'rozjebać', 'rozjebac', 'rozjebie','rozjebała', 'rozjebią', 'rozpierdalać', 'rozpierdalac', 'rozpierdala','rozpierdolić', 'rozpierdolic', 'rozpierdole', 'rozpierdoli','rozpierducha', 'skurwić', 'skurwiel', 'skurwiela', 'skurwielem','skurwielu', 'skurwysyn', 'skurwysynów', 'skurwysynow', 'skurwysyna','skurwysynem', 'skurwysynu', 'skurwysyny', 'skurwysyński','skurwysynski', 'skurwysyństwo', 'skurwysynstwo', 'spieprzać','spieprzac', 'spieprza', 'spieprzaj', 'spieprzajcie', 'spieprzają','spieprzaja', 'spieprzający', 'spieprzajacy', 'spieprzająca','spieprzajaca', 'spierdalać', 'spierdalac', 'spierdala', 'spierdalał','spierdalała', 'spierdalal', 'spierdalalcie', 'spierdalala','spierdalający', 'spierdalajacy', 'spierdolić', 'spierdolic','spierdoli', 'spierdoliła', 'spierdoliło', 'spierdolą', 'spierdola','srać', 'srac', 'srający', 'srajacy', 'srając', 'srajac', 'sraj','sukinsyn', 'sukinsyny', 'sukinsynom', 'sukinsynowi', 'sukinsynów','sukinsynow', 'śmierdziel', 'udupić', 'ujebać', 'ujebac', 'ujebał','ujebal', 'ujebana', 'ujebany', 'ujebie', 'ujebała', 'ujebala','upierdalać', 'upierdalac', 'upierdala', 'upierdoli', 'upierdolić','upierdolic', 'upierdoli', 'upierdolą', 'upierdola', 'upierdoleni','wjebać', 'wjebac', 'wjebie', 'wjebią', 'wjebia', 'wjebiemy','wjebiecie', 'wkurwiać', 'wkurwiac', 'wkurwi', 'wkurwia', 'wkurwiał','wkurwial', 'wkurwiający', 'wkurwiajacy', 'wkurwiająca', 'wkurwiajaca','wkurwić', 'wkurwic', 'wkurwi', 'wkurwiacie', 'wkurwiają', 'wkurwiali','wkurwią', 'wkurwia', 'wkurwimy', 'wkurwicie', 'wkurwiacie', 'wkurwić','wkurwic', 'wkurwia', 'wpierdalać', 'wpierdalac', 'wpierdalający','wpierdalajacy', 'wpierdol', 'wpierdolić', 'wpierdolic', 'wpizdu','wyjebać', 'wyjebac', 'wyjebali', 'wyjebał', 'wyjebac', 'wyjebała','wyjebały', 'wyjebie', 'wyjebią', 'wyjebia', 'wyjebiesz', 'wyjebie','wyjebiecie', 'wyjebiemy', 'wypieprzać', 'wypieprzac', 'wypieprza','wypieprzał', 'wypieprzal', 'wypieprzała', 'wypieprzala', 'wypieprzy','wypieprzyła', 'wypieprzyla', 'wypieprzył', 'wypieprzyl', 'wypierdal','wypierdalać', 'wypierdalac', 'wypierdala', 'wypierdalaj','wypierdalał', 'wypierdalal', 'wypierdalała', 'wypierdalala','wypierdalać', 'wypierdolić', 'wypierdolic', 'wypierdoli','wypierdolimy', 'wypierdolicie', 'wypierdolą', 'wypierdola','wypierdolili', 'wypierdolił', 'wypierdolil', 'wypierdoliła','wypierdolila', 'zajebać', 'zajebac', 'zajebie', 'zajebią', 'zajebia','zajebiał', 'zajebial', 'zajebała', 'zajebiala', 'zajebali', 'zajebana','zajebani', 'zajebane', 'zajebany', 'zajebanych', 'zajebanym','zajebanymi', 'zajebiste', 'zajebisty', 'zajebistych', 'zajebista','zajebistym', 'zajebistymi', 'zajebiście', 'zajebiscie', 'zapieprzyć','zapieprzyc', 'zapieprzy', 'zapieprzył', 'zapieprzyl', 'zapieprzyła','zapieprzyla', 'zapieprzą', 'zapieprza', 'zapieprzy', 'zapieprzymy','zapieprzycie', 'zapieprzysz', 'zapierdala', 'zapierdalać','zapierdalac', 'zapierdalaja', 'zapierdalał', 'zapierdalaj','zapierdalajcie', 'zapierdalała', 'zapierdalala', 'zapierdalali','zapierdalający', 'zapierdalajacy', 'zapierdolić', 'zapierdolic','zapierdoli', 'zapierdolił', 'zapierdolil', 'zapierdoliła','zapierdolila', 'zapierdolą', 'zapierdola', 'zapierniczać','zapierniczający', 'zasrać', 'zasranym', 'zasrywać', 'zasrywający','zesrywać', 'zesrywający', 'zjebać', 'zjebac', 'zjebał', 'zjebal','zjebała', 'zjebala', 'zjebana', 'zjebią', 'zjebali', 'zjeby']
