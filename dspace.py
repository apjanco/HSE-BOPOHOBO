import os
from tkinter import filedialog
from tkinter import *
import xml.etree.ElementTree as ET


path = os.getcwd()

def browse_button():
    print(
        """Welcome to the dspace-er.  Please open the directory that contains the files you would like to process""")

    # Allow user to select a directory and store it in global var
    # called folder_path

    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    return filename

root = Tk()
folder_path = StringVar()
lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=1)
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=0, column=3)

class MarcRecord:
    def __init__(self, title, contributor, language, date, type, subject, publisher, rights, format, identifier, ispartof, ispartofseries):
        self.title = title
        self.contributor = contributor
        self.language = language
        self.date = date
        self.type = type
        self.subject = subject
        self.publisher = publisher
        self.rights = rights
        self.format = format
        self.identifier = identifier
        self.ispartof = ispartof
        self.ispartofseries = ispartofseries

def make_xml_file(marc, path):
    xml_start = """<?xml version="1.0" encoding="UTF-8"?> 
    <dublin_core schema="dc">"""

    try:
        identifier = marc.identifier
    except AttributeError:
        identifier = ''
    identifier_input = input("Enter identifier:other [{}]: ".format(identifier))
    if identifier_input == '':
        identifier_input = identifier
    marc.identifier = identifier_input
    identifier_text = '<dcvalue element="identifier" qualifier="other">{}</dcvalue>'.format(identifier_input)
    
    try:
        ispartof = marc.ispartof
    except AttributeError:
        ispartof = ''
    ispartof_input = input("Enter relation:ispartof [{}]: ".format(ispartof))
    if ispartof_input == '':
        ispartof_input = ispartof
    marc.ispartof = ispartof_input
    ispartof_text = '<dcvalue element="relation" qualifier="ispartof">{}</dcvalue>'.format(ispartof_input)

    try:
        ispartofseries = marc.ispartofseries
    except AttributeError:
        ispartofseries = ''
    ispartofseries_input = input("Enter relation:ispartofseries [{}]: ".format(ispartofseries))
    if ispartofseries_input == '':
        ispartofseries_input = ispartofseries
    marc.ispartofseries = ispartofseries_input
    ispartofseries_text = '<dcvalue element="identifier" qualifier="other">{}</dcvalue>'.format(ispartof_input)

    try:
        title = marc.title
    except AttributeError:
        title = ''
    title_input = input("Enter title [{}]: ".format(title))
    if title_input == '':
        title_input = title
    marc.title = title_input
    title_text = '<dcvalue element="title">{}</dcvalue>'.format(title_input)

    try:
        contributor = marc.contributor
    except AttributeError:
        contributor = ''
    contributor_input = input("Enter contributor:author [{}]: ".format(contributor))
    if contributor_input == '':
        contributor_input = contributor
    marc.contributor = contributor_input
    contributor_text = '<dcvalue element="contibutor" qualifier="author">{}</dcvalue>'.format(contributor_input)

    try:
        language = marc.language
    except AttributeError:
        language = ''
    language_input = input("Enter language [{}]: ".format(language))
    if language_input == '':
        language_input = language
    marc.language = language_input
    language_text = '<dcvalue element="language" qualifier="iso">{}</dcvalue>'.format(language_input)

    try:
        date = marc.date
    except AttributeError:
        date = ''
    date_input = input("Enter date:issued (YYYY-YYYY) [{}]: ".format(date))
    if date_input == '':
        date_input = date
    marc.date = date_input
    date_text = '<dcvalue element="date" qualifier="issued">{}</dcvalue>'.format(date_input)

    try:
        type = marc.type
    except AttributeError:
        type = ''
    type_input = input("Enter type [{}]: ".format(type))
    if type_input == '':
        type_input = type
    marc.type = type_input
    type_text = '<dcvalue element="type">{}</dcvalue>'.format(type_input)
    
    try:
        subject = marc.subject
    except AttributeError:
        subject = ''
    subject_input = input("Enter subject:aat [{}]: ".format(subject))
    if subject_input == '':
        subject_input = subject
    marc.subject = subject_input
    subject_text = '<dcvalue element="subject" qualifier="aat">{}</dcvalue>'.format(subject_input)

    try:
        publisher = marc.publisher
    except AttributeError:
        publisher = ''
    publisher_input = input("Enter publisher [{}]: ".format(publisher))
    if publisher_input == '':
        publisher_input = publisher
    marc.publisher = publisher_input
    publisher_text = '<dcvalue element="publisher">{}</dcvalue>'.format(publisher_input)
    
    try:
        rights = marc.rights
    except AttributeError:
        rights = ''
    rights_input = input("Enter rights:access [{}]: ".format(rights))
    if rights_input == '':
        rights_input = rights
    marc.rights = rights_input
    rights_text = '<dcvalue element="rights" qualifier="access">{}</dcvalue>'.format(rights_input)

    try:
        _format = marc.format
    except AttributeError:
        _format = ''
    format_input = input("Enter format [{}]: ".format(_format))
    if format_input == '':
        format_input = _format
    marc.format = format_input
    format_text = '<dcvalue element="format" qualifier="extent">{}</dcvalue>'.format(format_input)
    
    xml_end = '</dublin_core>'
    xmlstring = xml_start + identifier_text + ispartof_text + ispartofseries_text + title_text + contributor_text \
                + language_text + date_text + type_text + subject_text + publisher_text + rights_text + format_text \
                + xml_end
    root = ET.fromstring(xmlstring)
    return root

def make_permissions(file):
    permissions = ['permissions-r HC_Theses	description:** Archive Staff Only **',
                   'permissions:-r HC	description: Thesis',
                   'permissions:-r BiCo	description: Thesis',
                   'permissions:-r TriCo	description: Thesis',
                   'permissions:-r HC_Theses	description: Thesis']
    for i in permissions:
        print(permissions.index(i), i)

    input_index = input("Select the permissions number: ")
    try:
        permission = permissions[int(input_index)]
    except ValueError:
        print("oops, too many enters!")
        input_index = input("Select the permissions number: ")
        permission = permissions[int(input_index)]

    text = """{0} {1}""".format(file, permission)
    return text

def process_directory(marc, directory):
    counter = 1
    for file in os.listdir(directory):
        print(file)
        item_label = 'item_{0:03}'.format(counter)
        if os.path.isdir(directory + '/' + item_label):
            print('item folder already exists')
        else:
            os.mkdir(directory + '/' + item_label)
            os.rename(directory + '/' + file, directory + '/' + item_label + '/' + file)
            xml_file = make_xml_file(marc, directory +'/' + file)
            tree = ET.ElementTree(xml_file)
            tree.write(directory + '/' + item_label +'/' + 'dublin_core.xml')
            text = make_permissions(file)
            with open(directory + '/' + item_label +'/' + 'contents', 'w') as f:
                f.write(text)


            counter += 1



if __name__ == "__main__":
    marc = MarcRecord
    directory = browse_button()
    process_directory(marc, directory)



