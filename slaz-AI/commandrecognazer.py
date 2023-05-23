
# How bot interprete evry message. Fixing means if you want to change a content to be easier to interprete, or you just want to split a message

def word_in_message(mess,fixing):

    # BIG to small letter
    if fixing == False:
        mess = mess.lower()
    
    # Remove repeating letters
    if fixing == False:
        nowy=''
        ostatnia=''
        for i in mess:
            if ostatnia != i:
                nowy+=str(i)
                ostatnia=i
    else:
        nowy = mess
    
    # Pass all the punctuation marks
    if fixing == False:
        nowy = nowy.replace(",", " , ")
        nowy = nowy.replace("#", " # ")
        nowy = nowy.replace("?", " ? ")
        nowy = nowy.replace("!", " ! ")
        nowy = nowy.replace(".", " . ")
        nowy = nowy.replace("\"", " \" ")
        nowy = nowy.replace("/", " / ")
        nowy = nowy.replace("\\", " \\ ")
    
    # return result
    mess_tabela = nowy.split()
    return mess_tabela