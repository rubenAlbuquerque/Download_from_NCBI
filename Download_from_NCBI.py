import requests


def dowloader():
    # Choose the database and organism to search on NCBI
    print("~~~~~~ Chose the database number you want: ~~~~~~")
    print("~~~~~~        1.- protein                  ~~~~~~")
    print("~~~~~~        2.- nucleotide               ~~~~~~")
    print("~~~~~~        3.- nuccore                  ~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    option = input("-->")
    if option == "1":
        database = "db=protein"
    elif option == "2":
        database = "db=nucleotide"
    elif option == "3":
        database = "db=nuccore"
    else:
        print("This database does not exist.")
        dowloader()

    organism_name = "&term=" + input("Enter which organism you want to look for:")

    link_info = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + database + \
                organism_name + "&usehistory=y"

    info_ncbi = requests.get(link_info, timeout=123)

    # len("<WebEnv>") = 8, len("<QueryKey>")= 10
    web_env = "&WebEnv=" + (info_ncbi.text[info_ncbi.text.find("<WebEnv>") + 8:info_ncbi.text.find("</WebEnv>")])
    query_key = "&query_key=" + (info_ncbi.text[info_ncbi.text.find("<QueryKey>") + 10:info_ncbi.text.find("</QueryKey>")])

    # It will request the data
    link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + database + web_env + query_key + "&rettype=fasta"
    getdata_ncbi = requests.get(link)

    print("~" * 80)

    # This for will add to the dictionary the name with its sequence
    dicionary = sequence_dicionary(getdata_ncbi.text.split("\n"))

    how_many_sequences(dicionary, getdata_ncbi)



def save_file(text):
    print(" 1.- Want to add text to file \n 2.- Just have text in file")
    # print("C:\Users\ruben\Desktop\biologia\sequence.txt")
    option = input("-->")
    if option == "1":
        filename = input("Type the file path:")
        with open(filename, 'a') as file:
            file.write("\n" + text)

    elif option == "2":
        # rewrite the text
        filename = input("Type the file path:")
        with open(filename, "w") as file:
            file.write(text)

    else:
        print("You didn't choose any of the options")
        save_file(text)

    print("The sequences were saved in the file")


def sequence_dicionary(text):
    dicionary = {}
    for i in text:
        if i.startswith(">"):
            name = i.replace(">", "> ")
            dicionary[name] = ""
        else:
            dicionary[name] += i
    return dicionary


def how_many_sequences(dicionary, getdata_ncbi):
    print("  1.- You want to save all sequences. \n  2.- You want to save only one sequence")
    option = input("-->")
    if option == "1":
        save_file(getdata_ncbi.text)
    elif option == "2":
        # Show all alternatives
        count = 0
        for i in dicionary.keys():
            count += 1
            print(str(count), i)
        # ask what sequence you want
        print("~" * 80 + "\n~~~~  Choose the name and enter the number. ~~~~\n" + "~" * 80)
        option = int(input("-->"))

        count = 0
        anwser = []
        for i in dicionary.keys():
            count += 1
            if count == option:
                anwser.append(i)

        if len(anwser) == 0:
            print("Your chose do not exist.")
            how_many_sequences(dicionary, getdata_ncbi)

        elif len(anwser) == 1:
            save_file(anwser[0] + '\n' + dicionary[anwser[0]])

    else:
        how_many_sequences(dicionary, getdata_ncbi)


dowloader()













