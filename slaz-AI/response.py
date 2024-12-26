import random
import iniload


def auto_response(prev, message_words, required_words, answers):
    """Returns a random response from the provided answers if all required words are present in the message words. Otherwise, returns the previous response."""
    
    # Check if conditions of auto-answear are fulfilled
    # arguments:
    # prev - if condition is not meed, return this string
    # mess - table of words (message of user)
    # requir - required words to meet requirements
    # answ - table of answears (strings) if conditions is meet (bot will take one string of table at random)
    
    return random.choice(answers) if all(req in message_words for req in required_words) else prev

def random_joke():
    """Returns a random joke from a predefined list of jokes."""
    jokes = [
        ['Dlaczego trzyletnie nieszczepione dziecko płacze?', 'Bo przechodzi kryzys wieku średniego'],
        ['Dlaczego choinka nie jest głodna?', 'Bo jodła'],
        ['', '']
    ]
    return random.choice(jokes)

def blacklist_usernames(message_words):
    """Checks if the message contains blacklisted usernames and returns a 'ban' response if found."""
    return auto_response('', message_words, ['twitter', 'com', 'h0nde'], ['ban'])

def response_list(command_words, original_words, channel, guild, message, client):
    """Generates a response based on the command words and predefined response patterns. It also handles debug commands and counts swear words."""
    responses = [
        [['version'], ['1.5 AI']],
        [['<@', '!', '40543924654820569>'], ['Nie pinguj pajacu', 'No nie wytrzymam, nie pinguj gnoju']],
        [['@everyone'], ['No brawo', 'Ktoś, coś ban?', 'JPRDL']],
        [['witam'], ['Hejka', 'Cześć', 'Elo']],
        [['cześć'], ['Hejka', 'Cześć', 'Elo']],
        [['hej'], ['No hejka']],
        [['dobranoc'], ['Śpij dobrze']],
        [['f'], ['[*]']],
        [['nasze'], ['"Ours" \n https://cdn.discordapp.com/attachments/801861475395698740/801861585097981972/nasze.png']],
        [['pog'], ['https://cdn.discordapp.com/attachments/801861475395698740/801861857706639400/pogchamp.png']],
        [['lubisz', 'mnie', '?'], ['No homo', 'Nie pajacu', 'Spierdalaj', 'To zależy', 'Oczywiście gnojku']],
        [['ślazatek', 'inteligentny'], ['Dokładnie']],
        [['ślazatek', 'inteligentny', 'nie'], ['Spierdalaj']],
        [['ślazatek', 'głupi'], ['Spierdalaj']],
        [['rze'], ['Za takie błędy ortograficzne powinien być ban']],
        [['kture'], ['Za takie błędy ortograficzne powinien być ban']],
        [['napewno'], ['*Na pewno się pisze pajacu']],
        [['wogóle'], ['Tak "Wogóle" to ty możesz bana dostać']],
        [['wogule'], ['Tak "Wogule" to ty możesz bana dostać']],
        [['narazie'], ['pisze się " na razie"']],
        [['muj'], ['"muj" mózg nie wytrzyma jak widze twoje błędy']],
        [['niewiem'], ['kurła, orto boli']],
        [['wziąść'], ['też mogę "wziąść"']],
        [['nje'], ['*nie']],
        [['takih'], ['*takich']],
        [['problemuf'], ['*problemów']],
        [['problemuw'], ['*problemów']],
        [['dobsze'], ['*dobrze']],
        [['tesz'], ['*też']],
        [['conajmniej'], ['*co najmniej']],
        [['jusz'], ['*już']],
        [['niewiem'], ['*nie wiem']],
        [['kasztany'], ['Orzechy > Kasztany']],
        [['orzechy'], ['Orzechy > Kasztany']],
        [['chwasty'], ['Pal gumę gnoju']],
        [['chwaście'], ['Pal gumę gnoju']],
        [['chwast'], ['Pal gumę gnoju']],
        [['ty', 'kurwo'], ['Śmieciu']],
        [['sztorm'], ['Właśnie, kiedy sztorm?']],
        [['szturm'], ['Właśnie, kiedy sztorm?']],
        [['orange'], ['Orange, rusz dupę i rób grę']],
        [['kjedy', 'fefef'], ['Właśnie, kiedy fefef?']],
        [['kiedy', 'fefef'], ['Właśnie, kiedy fefef?']],
        [['kjedy', 'f'], ['Właśnie, kiedy fefef?']],
        [['kiedy', 'f'], ['Właśnie, kiedy fefef?']],
        [['damian', 'kurwa'], ['Kiedy fefef?']],
        [['dałmian', 'kurwa'], ['Kiedy fefef?']],
        [['dałnmian', 'kurwa'], ['Kiedy fefef?']],
        [['sranie'], ['Mroczne']],
        [['mroczne'], ['Sranie']],
        [['mroczne', 'granie'], ['Mroczne Sranie']],
        [['dałmian'], ['Kurwa Dałmian']],
        [['gówno'], ['zjedz je równo']],
        [['zjebałeś'], ['sam zjebałeś gnoju']],
        [['się', 'zesrałem'], ['To nie dobrze']],
        [['kasztan'], ['Kurła kasztan kiedy sztorm']],
        [['szturm'], ['*sztorm', 'chyba miałeś na myśli sztOrm', 'no chyba sztorm']]
    ]

    resp = ''
    for response in responses:
        resp = auto_response(resp, command_words, response[0], response[1])

    resp = auto_response(resp, command_words, ['.'], [''])

    resp = count_swears(resp, command_words, message)

    resp = auto_response(resp, original_words, ['&debug-p'], [original_words])
    resp = auto_response(resp, command_words, ['&debug'], [command_words])

    return resp

def count_swears(resp, command_words, message):
    """Counts the number of swear words in the message and updates the swear count for the user. Returns a reminder if the swear count reaches a multiple of 10."""
    swear_words = ['japierdole','jebać','wypierdol','spierdalaj','chuj','chuja', 'chujek', 'chuju', 'chujem', 'chujnia','chujowy', 'chujowa', 'chujowe', 'cipa', 'cipę', 'cipe', 'cipą','cipie', 'dojebać','dojebac', 'dojebie', 'dojebał', 'dojebal','dojebała', 'dojebala', 'dojebałem', 'dojebalem', 'dojebałam','dojebalam', 'dojebię', 'dojebie', 'dopieprzać', 'dopieprzac','dopierdalać', 'dopierdalac', 'dopierdala', 'dopierdalał','dopierdalal', 'dopierdalała', 'dopierdalala', 'dopierdoli','dopierdolił', 'dopierdolil', 'dopierdolę', 'dopierdole', 'dopierdoli','dopierdalający', 'dopierdalajacy', 'dopierdolić', 'dopierdolic','dupa', 'dupie', 'dupą', 'dupcia', 'dupeczka', 'dupy', 'dupe', 'huj','hujek', 'hujnia', 'huja', 'huje', 'hujem', 'huju', 'jebać', 'jebac','jebał', 'jebal', 'jebie', 'jebią', 'jebia', 'jebak', 'jebaka', 'jebal','jebał', 'jebany', 'jebane', 'jebanka', 'jebanko', 'jebankiem','jebanymi', 'jebana', 'jebanym', 'jebanej', 'jebaną', 'jebana','jebani', 'jebanych', 'jebanymi', 'jebcie', 'jebiący', 'jebiacy','jebiąca', 'jebiaca', 'jebiącego', 'jebiacego', 'jebiącej', 'jebiacej','jebia', 'jebią', 'jebie', 'jebię', 'jebliwy', 'jebnąć', 'jebnac','jebnąc', 'jebnać', 'jebnął', 'jebnal', 'jebną', 'jebna', 'jebnęła','jebnela', 'jebnie', 'jebnij', 'jebut', 'koorwa', 'kórwa', 'kurestwo','kurew', 'kurewski', 'kurewska', 'kurewskiej', 'kurewską', 'kurewska','kurewsko', 'kurewstwo', 'kurwa', 'kurwaa', 'kurwami', 'kurwą', 'kurwe','kurwę', 'kurwie', 'kurwiska', 'kurwo', 'kurwy', 'kurwach', 'kurwami','kurewski', 'kurwiarz', 'kurwiący', 'kurwica', 'kurwić', 'kurwic','kurwidołek', 'kurwik', 'kurwiki', 'kurwiszcze', 'kurwiszon','kurwiszona', 'kurwiszonem', 'kurwiszony', 'kutas', 'kutasa', 'kutasie','kutasem', 'kutasy', 'kutasów', 'kutasow', 'kutasach', 'kutasami','matkojebca', 'matkojebcy', 'matkojebcą', 'matkojebca', 'matkojebcami','matkojebcach', 'nabarłożyć', 'najebać', 'najebac', 'najebał','najebal', 'najebała', 'najebala', 'najebane', 'najebany', 'najebaną','najebana', 'najebie', 'najebią', 'najebia', 'naopierdalać','naopierdalac', 'naopierdalał', 'naopierdalal', 'naopierdalała','naopierdalala', 'naopierdalała', 'napierdalać', 'napierdalac','napierdalający', 'napierdalajacy', 'napierdolić', 'napierdolic','nawpierdalać', 'nawpierdalac', 'nawpierdalał', 'nawpierdalal','nawpierdalała', 'nawpierdalala', 'obsrywać', 'obsrywac', 'obsrywający','obsrywajacy', 'odpieprzać', 'odpieprzac', 'odpieprzy', 'odpieprzył','odpieprzyl', 'odpieprzyła', 'odpieprzyla', 'odpierdalać','odpierdalac', 'odpierdol', 'odpierdolił', 'odpierdolil','odpierdoliła', 'odpierdolila', 'odpierdoli', 'odpierdalający','odpierdalajacy', 'odpierdalająca', 'odpierdalajaca', 'odpierdolić','odpierdolic', 'odpierdoli', 'odpierdolił', 'opieprzający','opierdalać', 'opierdalac', 'opierdala', 'opierdalający','opierdalajacy', 'opierdol', 'opierdolić', 'opierdolic', 'opierdoli','opierdolą', 'opierdola', 'piczka', 'pieprznięty', 'pieprzniety','pieprzony', 'pierdel', 'pierdlu', 'pierdolą', 'pierdola', 'pierdolący','pierdolacy', 'pierdoląca', 'pierdolaca', 'pierdol', 'pierdole','pierdolenie', 'pierdoleniem', 'pierdoleniu', 'pierdolę', 'pierdolec','pierdola', 'pierdolą', 'pierdolić', 'pierdolicie', 'pierdolic','pierdolił', 'pierdolil', 'pierdoliła', 'pierdolila', 'pierdoli','pierdolnięty', 'pierdolniety', 'pierdolisz', 'pierdolnąć','pierdolnac', 'pierdolnął', 'pierdolnal', 'pierdolnęła', 'pierdolnela','pierdolnie', 'pierdolnięty', 'pierdolnij', 'pierdolnik', 'pierdolona','pierdolone', 'pierdolony', 'pierdołki', 'pierdzący', 'pierdzieć','pierdziec', 'pizda', 'pizdą', 'pizde', 'pizdę', 'piździe', 'pizdzie','pizdnąć', 'pizdnac', 'pizdu', 'podpierdalać', 'podpierdalac','podpierdala', 'podpierdalający', 'podpierdalajacy', 'podpierdolić','podpierdolic', 'podpierdoli', 'pojeb', 'pojeba', 'pojebami','pojebani', 'pojebanego', 'pojebanemu', 'pojebani', 'pojebany','pojebanych', 'pojebanym', 'pojebanymi', 'pojebem', 'pojebać','pojebac', 'pojebalo', 'popierdala', 'popierdalac', 'popierdalać','popierdolić', 'popierdolic', 'popierdoli', 'popierdolonego','popierdolonemu', 'popierdolonym', 'popierdolone', 'popierdoleni','popierdolony', 'porozpierdalać', 'porozpierdala', 'porozpierdalac','poruchac', 'poruchać', 'przejebać', 'przejebane', 'przejebac','przyjebali', 'przepierdalać', 'przepierdalac', 'przepierdala','przepierdalający', 'przepierdalajacy', 'przepierdalająca','przepierdalajaca', 'przepierdolić', 'przepierdolic', 'przyjebać','przyjebac', 'przyjebie', 'przyjebała', 'przyjebala', 'przyjebał','przyjebal', 'przypieprzać', 'przypieprzac', 'przypieprzający','przypieprzajacy', 'przypieprzająca', 'przypieprzajaca','przypierdalać', 'przypierdalac', 'przypierdala', 'przypierdoli','przypierdalający', 'przypierdalajacy', 'przypierdolić','przypierdolic', 'qrwa', 'rozjebać', 'rozjebac', 'rozjebie','rozjebała', 'rozjebią', 'rozpierdalać', 'rozpierdalac', 'rozpierdala','rozpierdolić', 'rozpierdolic', 'rozpierdole', 'rozpierdoli','rozpierducha', 'skurwić', 'skurwiel', 'skurwiela', 'skurwielem','skurwielu', 'skurwysyn', 'skurwysynów', 'skurwysynow', 'skurwysyna','skurwysynem', 'skurwysynu', 'skurwysyny', 'skurwysyński','skurwysynski', 'skurwysyństwo', 'skurwysynstwo', 'spieprzać','spieprzac', 'spieprza', 'spieprzaj', 'spieprzajcie', 'spieprzają','spieprzaja', 'spieprzający', 'spieprzajacy', 'spieprzająca','spieprzajaca', 'spierdalać', 'spierdalac', 'spierdala', 'spierdalał','spierdalała', 'spierdalal', 'spierdalalcie', 'spierdalala','spierdalający', 'spierdalajacy', 'spierdolić', 'spierdolic','spierdoli', 'spierdoliła', 'spierdoliło', 'spierdolą', 'spierdola','srać', 'srac', 'srający', 'srajacy', 'srając', 'srajac', 'sraj','sukinsyn', 'sukinsyny', 'sukinsynom', 'sukinsynowi', 'sukinsynów','sukinsynow', 'śmierdziel', 'udupić', 'ujebać', 'ujebac', 'ujebał','ujebal', 'ujebana', 'ujebany', 'ujebie', 'ujebała', 'ujebala','upierdalać', 'upierdalac', 'upierdala', 'upierdoli', 'upierdolić','upierdolic', 'upierdoli', 'upierdolą', 'upierdola', 'upierdoleni','wjebać', 'wjebac', 'wjebie', 'wjebią', 'wjebia', 'wjebiemy','wjebiecie', 'wkurwiać', 'wkurwiac', 'wkurwi', 'wkurwia', 'wkurwiał','wkurwial', 'wkurwiający', 'wkurwiajacy', 'wkurwiająca', 'wkurwiajaca','wkurwić', 'wkurwic', 'wkurwi', 'wkurwiacie', 'wkurwiają', 'wkurwiali','wkurwią', 'wkurwia', 'wkurwimy', 'wkurwicie', 'wkurwiacie', 'wkurwić','wkurwic', 'wkurwia', 'wpierdalać', 'wpierdalac', 'wpierdalający','wpierdalajacy', 'wpierdol', 'wpierdolić', 'wpierdolic', 'wpizdu','wyjebać', 'wyjebac', 'wyjebali', 'wyjebał', 'wyjebac', 'wyjebała','wyjebały', 'wyjebie', 'wyjebią', 'wyjebia', 'wyjebiesz', 'wyjebie','wyjebiecie', 'wyjebiemy', 'wypieprzać', 'wypieprzac', 'wypieprza','wypieprzał', 'wypieprzal', 'wypieprzała', 'wypieprzala', 'wypieprzy','wypieprzyła', 'wypieprzyla', 'wypieprzył', 'wypieprzyl', 'wypierdal','wypierdalać', 'wypierdalac', 'wypierdala', 'wypierdalaj','wypierdalał', 'wypierdalal', 'wypierdalała', 'wypierdalala','wypierdalać', 'wypierdolić', 'wypierdolic', 'wypierdoli','wypierdolimy', 'wypierdolicie', 'wypierdolą', 'wypierdola','wypierdolili', 'wypierdolił', 'wypierdolil', 'wypierdoliła','wypierdolila', 'zajebać', 'zajebac', 'zajebie', 'zajebią', 'zajebia','zajebiał', 'zajebial', 'zajebała', 'zajebiala', 'zajebali', 'zajebana','zajebani', 'zajebane', 'zajebany', 'zajebanych', 'zajebanym','zajebanymi', 'zajebiste', 'zajebisty', 'zajebistych', 'zajebista','zajebistym', 'zajebistymi', 'zajebiście', 'zajebiscie', 'zapieprzyć','zapieprzyc', 'zapieprzy', 'zapieprzył', 'zapieprzyl', 'zapieprzyła','zapieprzyla', 'zapieprzą', 'zapieprza', 'zapieprzy', 'zapieprzymy','zapieprzycie', 'zapieprzysz', 'zapierdala', 'zapierdalać','zapierdalac', 'zapierdalaja', 'zapierdalał', 'zapierdalaj','zapierdalajcie', 'zapierdalała', 'zapierdalala', 'zapierdalali','zapierdalający', 'zapierdalajacy', 'zapierdolić', 'zapierdolic','zapierdoli', 'zapierdolił', 'zapierdolil', 'zapierdoliła','zapierdolila', 'zapierdolą', 'zapierdola', 'zapierniczać','zapierniczający', 'zasrać', 'zasranym', 'zasrywać', 'zasrywający','zesrywać', 'zesrywający', 'zjebać', 'zjebac', 'zjebał', 'zjebal','zjebała', 'zjebala', 'zjebana', 'zjebią', 'zjebali', 'zjeby']
    swear_count = 0
    for swear in swear_words:
        swear_count += command_words.count(swear)

    if swear_count > 0:
        swear_total = int(iniload.ini_load('licznik.conf', 'swears', str(message.author.id), '0'))
        iniload.ini_change('licznik.conf', 'swears', str(message.author.id), str(swear_total + swear_count))

        if (swear_total + swear_count) % 10 == 0:
            resp = f'Przypomnienie! Przeklnąłeś już {swear_total + swear_count} raz!'
        else:
            resp = resp

    return resp