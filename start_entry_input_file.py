'''
This will be the starting point for users to use the program.
Widget will open asking users to input the file containing the training data and parsed output for comparison.
Users will also be able to input 2 separate files that will use the trained model to do address comparisons.
'''

from tkinter import *

master = Tk()

variable = StringVar()
variable.set("csv")

Label(master, text="File Name Containing the Training Data").grid(row=0)
Label(master, text="Select the File Type for the Training Data").grid(row=1)
OptionMenu(master, variable, "csv", "excel").grid(row=1, column=1)
Label(master, text="Field Name Containing the Unstructured Addresses").grid(row=2)
Label(master, text="Field with Parsed Street Number").grid(row=3)
Label(master, text="Field with Parsed Unit Type").grid(row=4)
Label(master, text="Field with Parsed Unit Number").grid(row=5)
Label(master, text="Field with Parsed Pre Street Name Direction").grid(row=6)
Label(master, text="Field with Parsed Street Name").grid(row=7)
Label(master, text="Field with Parsed Street Type").grid(row=8)
Label(master, text="Field with Parsed Post Street Type Direction").grid(row=9)
Label(master, text="Field with Parsed City").grid(row=10)
Label(master, text="Field with Parsed State").grid(row=11)
Label(master, text="Field with Parsed Country").grid(row=12)
Label(master, text="Field with Parsed Zip Code").grid(row=13)
Label(master, text="File 1 Containing Unstructured Addresses").grid(row=14)
Label(master, text="File 2 Containing Unstructured Addresses").grid(row=15)

Button(master, text='OK', command=master.quit).grid(row=16, column=0, sticky=W, pady=4)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)
e7 = Entry(master)
e8 = Entry(master)
e9 = Entry(master)
e10 = Entry(master)
e11 = Entry(master)
e12 = Entry(master)
e13 = Entry(master)
e14 = Entry(master)
e15 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=2, column=1)

parsed_field_names_inputs = [e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13]

row_num = 3
column_num = 1
for item in parsed_field_names_inputs:
    item.grid(row = row_num, column = column_num)
    row_num += 1

e14.grid(row=14, column=1)
e15.grid(row=15, column=1)

mainloop()

file_name = e1.get()
unstructured_training_data = e2.get()

parsed_field_names = list()

for item in parsed_field_names_inputs:
    parsed_field_names.append(item.get())

