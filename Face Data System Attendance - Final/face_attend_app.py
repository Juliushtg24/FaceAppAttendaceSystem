# import the library

import tkinter as tk
from tkinter import Message, ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
from numpy.lib.shape_base import column_stack
import pandas as pd
import datetime
import time


# USER DEFINED FUNCTION #
def clear():
    id_entry.delete(0, 'end')
    name_entry.delete(0, 'end')



# Assuring if the path for training image is exists
def is_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


# Add person to data csv
def add_person():
    is_path_exists("PersonData/")
    df = pd.read_csv("PersonData/PersonDatabase.csv")
    current_id = df.iloc[-1:,0].values
    current_id = str(current_id)
    next_id_text = current_id[1:-1]
    next_id = int(next_id_text) + 1

    new_person = tsd.askstring('New Person' , "Enter the Name")

    if(new_person !=  "" or new_person.isalpha() == False):
        row = [next_id,"", new_person ,"", "NO"]
        with open("PersonData\PersonDatabase.csv", "a+") as csvData:
                writer = csv.writer(csvData)
                writer.writerow(row)
        csvData.close()
    else:
        mess._show(title="Input Error" ,message="Enter real name")
        return

    print(next_id)

def student_info():
    root = tk.Tk()
    root.title("Student Data")
    width = 500
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    TableMargin = tk.Frame(root, width=500)
    TableMargin.pack(side=tk.TOP)
    scrollbarx = tk.Scrollbar(TableMargin, orient=tk.HORIZONTAL)
    scrollbary = tk.Scrollbar(TableMargin, orient=tk.VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("ID", "NAME"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
    tree.heading('ID', text="ID", anchor=tk.W)
    tree.heading('NAME', text="NAME", anchor=tk.W)
    tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
    tree.column('#1', stretch=tk.NO, minwidth=0, width=200)
    tree.column('#2', stretch=tk.NO, minwidth=0, width=200)
    tree.pack()

    with open('PersonData/PersonDatabase.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            ID = row['ID']
            NAME = row['NAME']
            tree.insert("", 0, values=(ID , NAME))

    root.mainloop()

def check():
    id_text = int(id_entry.get())
    is_path_exists("PersonData/")
    df = pd.read_csv("PersonData/PersonDatabase.csv")

    if id_text != "" or id_text.isdigit() == False:
        name_text = df.loc[df['ID'] == id_text]['NAME'].values
        face_status = df.loc[df['ID'] == id_text]['FACES'].values

        print(name_text)
        name_text = str(name_text)
        name_data = name_text[2:-2]
        face_status = str(face_status)
        face_data = face_status[2:-2]

        print(face_status)
        if (face_data == "YES"):
            mess._show(title="Check Error" ,message="ID " + str(id_text) + " already have faces id")
        else:
            name_entry.configure(text=name_data)
    else:
        name_entry.configure(text="Wrong Input")

# check haarscascade frontal face file exists 

def check_haarscascade():
    file_exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if file_exists:
        pass
    else:
        mess._show(title="haarscascade is missing" , message="Please email us if you have any problems")
        window.destroy()

# About us
def about():
    mess._show(title="About Us" , message="This program is created by julius and abraham if you need anything contact juliushut9704@gmail.com")

# password to save profile

def password():
    is_path_exists("ImageLabel/")
    file_exists = os.path.isfile("Password\pwd.txt")
    if file_exists:
        file = open("Password/pwd.txt" , "r")
        key = file.read()
    else: 
        mess._show(title="Password Error" , message="Please check password file")

    
    password = tsd.askstring('Password' , "Enter the password" , show="*")
    if(password == key):
        TrainImages()
    elif(password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')


# TRAINING AND TAKE THE PERSON IMAGES

# check person if they already have id face
def checkIDFace():
    id_text = int(id_entry.get())
    df = pd.read_csv("PersonData/PersonDatabase.csv")
    face_data_exists = df.loc[df["ID"] == id_text]["FACES"].values
    face_data_exists = str(face_data_exists)
    isface_exists = face_data_exists[2:-2]

    if(isface_exists == "YES"):
        mess._show(title="Check Error" ,message="ID " + str(id_text) + " already have faces id")
        return
    else:
        pass




def TakeImages():
    check_haarscascade()
    columns = ['SERIAL NO.', '', 'ID', 'NAME']
    is_path_exists("PersonData/")
    is_path_exists("ImageTraining/")
    checkIDFace()
    serial_no = 0
    file_exist = os.path.isfile("PersonData\PersonData.csv")
    df = pd.read_csv("PersonData/PersonDatabase.csv")
    
    if file_exist:
        with open("PersonData\PersonData.csv" , "r") as csvData:
            file_reader = csv.reader(csvData)
            for line in file_reader:
                serial_no += 1
        serial_no = (serial_no // 2)
        csvData.close()
    else:
        with open("PersonData\PersonData.csv", "a+") as csvData:
            writer = csv.writer(csvData)
            writer.writerow(columns)
            serial_no = 1
        csvData.close()
    # take input id and name data into csv file
    id_text = (id_entry.get())
    id_num = int(id_text)
    name_text = (name_entry.cget("text"))
    print(id_text + ' ' + name_text)
    if ((name_text.isalpha()) or (' ' in name_text)):
        camera = cv2.VideoCapture(0)
        haarcascade = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(haarcascade)
        sampleImage = 0
        while(True):
            ret, img = camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleImage = sampleImage + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("ImageTraining\ " + name_text + "." + str(serial_no) + "." + id_text + '.' + str(sampleImage) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleImage > 100:
                break
        camera.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID " + id_text
        row = [serial_no, '', id_text, '', name_text]
        with open("PersonData\PersonData.csv", "a+") as csvData:
            writer = csv.writer(csvData)
            writer.writerow(row)
        csvData.close()
        print(df.loc[df["ID"] == id_num]["FACES"].values)
        df.loc[df["ID"] == id_num , "FACES"] = "YES"
        df.to_csv("PersonData/PersonDatabase.csv", index=False)
        print(df.loc[df["ID"] == id_num]["FACES"].values)
        regis_status.configure(text=res)
    else:
        if(name_text.isalpha() == False):
            res = "Enter the real name"
            print("Enter the real name")


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def TrainImages():
    check_haarscascade()
    is_path_exists("ImageTraining/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces, ID = getImagesAndLabels("ImageTraining")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!')
        return
    recognizer.write("Trainner.yml")
    res = "Profile Saved Successfully"
    regis_status.configure(text=res)
    
def TrackImages():
    check_haarscascade()
    is_path_exists("AttendData/")
    is_path_exists("PersonData/")
    for k in data_view.get_children():
        data_view.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("Trainner.yml")
    if exists3:
        recognizer.read("Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    haarcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(haarcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("PersonData\PersonData.csv")
    if exists1:
        df = pd.read_csv("PersonData\PersonData.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb + "  {0}%".format(round(100 - conf))), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("AttendData\AttenData_" + date + ".csv")
    if exists:
        with open("AttendData\AttenData_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("AttendData\AttenData_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("AttendData\AttenData_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    data_view.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

# COLOR PALLETE #

MAGENTA  = "#9A0680"
PURPLE = "#79018C"
DARK_PURPLE = "#4C0070"
VERY_DARK_PURPLE = "#160040"

# FRONT END #

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.configure(background=MAGENTA)
window.title("Face Attendance Data System")

frame1 = tk.Frame(window, bg=VERY_DARK_PURPLE)
frame1.place(relx=0.11, rely=0.17 , relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#00aeff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

title1 = tk.Label(window , text="Face Attendance Data System" , fg="Yellow" , bg=MAGENTA, width=55 , height=1, font=('roboto', 29, ' bold '))
title1.place(x=10 , y=10)

### date and time 
###

title_frame1 = tk.Label(frame1, text="                       Person Attendance Data                      ", fg="Yellow", bg=VERY_DARK_PURPLE, font=('times', 17, ' bold '))
title_frame1.place(x=0 , y=20)

title_frame2 = tk.Label(frame2, text="                       Registrations Person Face                      " , fg="Yellow", bg="#00aeff" ,font=('times', 17, ' bold '))
title_frame2.place(x=0 , y=20)

id_label = tk.Label(frame2, text="Enter ID" , width=20 , height=1 , fg="black" , bg="#00aeff" , font=('times', 12, ' bold '))
id_label.place(x=-20 , y=65)

id_entry = tk.Entry(frame2, width=34 , fg="black" , font=('times', 15, ' bold '))
id_entry.place(x=120 , y=65)


name_label = tk.Label(frame2, text="Person Name" , width=20 , height=1 , fg="black" , bg="#00aeff" , font=('times', 12, ' bold '))
name_label.place(x=-20, y=150)

name_entry = tk.Label(frame2, width=20 , bg="#00aeff" ,fg="black" , font=('times', 15, ' bold '))
name_entry.place(x=120 , y=150)

tutor_message1 = tk.Label(frame2, text="How to save images?", fg="black" , bg="#00aeff" , font=('times', 15 , "bold"))
tutor_message1.place(x=150, y=250)

tutor_message2 = tk.Label(frame2, text="Step 1 - Take Images", fg="black" , bg="#00aeff" , font=('times', 15 , "bold"))
tutor_message2.place(x=150 , y=280)

tutor_message3 = tk.Label(frame2, text="Step 2 - Save Images", fg="black" , bg="#00aeff" , font=('times', 15 , "bold"))
tutor_message3.place(x=150 , y=320)

regis_status = tk.Label(frame2, text="", fg="black" , bg="#00aeff" , font=('times', 15 , "bold"))
regis_status.place(x=140, y=470)




clear_button  = tk.Button(frame2, text="Check" , fg="white", bg="red" , command=check ,width=35 , height=1 , font=('times' , 15 , 'bold'))
clear_button.place(x=30 , y=200)

take_image_button = tk.Button(frame2, text="Take Images",fg="white"  ,bg="blue", command=TakeImages ,width=34  ,height=1 ,font=('times', 15, ' bold '))
take_image_button.place(x=30, y=360)

train_image_button = tk.Button(frame2, text="Save Profile",fg="white"  ,bg="blue"  , command=password ,width=34  ,height=1, font=('times', 15, ' bold '))
train_image_button.place(x=30, y=420)

take_attend_button = tk.Button(frame1, text="Attendance",fg="white"  ,bg="blue", command=TrackImages  ,width=16  ,height=1, font=('times', 15, ' bold '))
take_attend_button.place(x=20 , y=500)

quit_button = tk.Button(frame1, text="Quit App",fg="white"  ,bg="red"  ,width=16  ,height=1, font=('times', 15, ' bold '))
quit_button.place(x=260, y=500)

#Data Attendance table list

data_view = ttk.Treeview(frame1 , height=13 , columns= ('name' , 'date' , 'time'))
data_view.column('#0', width=82)
data_view.column('name', width=130)
data_view.column('date', width=130)
data_view.column('time', width=130)
data_view.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
data_view.heading('#0' , text="ID")
data_view.heading('name' , text="Attendant Name")
data_view.heading('date' , text="Date")
data_view.heading('time' , text="Time")


tabmenu = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(tabmenu, tearoff=0)
addmenu = tk.Menu(tabmenu,tearoff=0)
filemenu.add_command(label='About Us', command=about)
filemenu.add_command(label='Exit',command = window.destroy)
addmenu.add_command(label="Info Student", command=student_info)
addmenu.add_command(label="Add Student", command=add_person)
tabmenu.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)
tabmenu.add_cascade(label="Data", font=('times' , 29 , 'bold'), menu=addmenu)


scroll=ttk.Scrollbar(frame1,orient='vertical',command=data_view.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
data_view.configure(yscrollcommand=scroll.set)

window.configure(menu=tabmenu)
window.mainloop()