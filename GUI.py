from tkinter import *
from tkinter import filedialog as fd
from Generator import Generator
import Patcher
root = Tk()
root.title("MTTNE Randomiser")
root.geometry("720x360")
root.config(background="#1e1e1e")

class Error(Exception):
    pass

class itemError(Error):
    pass

class fileError(Error):
    pass

gen = Generator()

def selectFile(arg):
    filetypes = (('Data files', '*.dat'), ('All files', '*.*'))
    
    if arg == "in":
        filename = fd.askopenfilename(title='Select a Decoded map file', filetypes=filetypes)
        e.delete(0, END)
        e.insert(0, filename)
    elif arg == "out":
        filename = fd.asksaveasfilename(title='Choose Output Directory', defaultextension=".dat", filetypes=filetypes)
        o.delete(0, END)
        o.insert(0, filename)

def generateGame():
    try:
        infile = e.get()
        outfile = o.get()
        if infile == "" or outfile == "":
            raise fileError
        if seedEntry.get() != "":
            seed = int(seedEntry.get())
        else:
            seed = ""
        missiles = int(MissEntry.get())
        supers = int(SupEntry.get())
        powerBombs = int(PBEntry.get())
        magShields = int(ShieldEntry.get())
        eTanks = int(ETankEntry.get())
        if missiles + supers + powerBombs + magShields + eTanks > 114:
            raise itemError
        itemDict = gen.generate_game(seed, missiles, supers, eTanks, powerBombs, magShields)
        Patcher.patch(infile, outfile, itemDict)
        print("Done!")
    except ValueError:
        pass
    except itemError:
        pass
    except fileError:
        pass

def updateItems():
    try:
        missiles = int(MissEntry.get())
        supers = int(SupEntry.get())
        powerBombs = int(PBEntry.get())
        magShields = int(ShieldEntry.get())
        eTanks = int(ETankEntry.get())
        count = missiles + supers + powerBombs + magShields + eTanks
    except ValueError:
        count = "N/A"
    Itemcount.config(text=str(count) + "/114")
    root.after(100, updateItems)


seedEntry = Entry(root)
seedLabel = Label(root, text="Input Seed (Optional): ", fg="white",bg="#1e1e1e")
e = Entry(root)
o = Entry(root)
inbutton = Button(root, text="Choose Decoded Map File", width="20",command=lambda: selectFile("in"))
outButton = Button(root, text="Choose Output File", width="20",command=lambda: selectFile("out"))
patchButton = Button(root, text="Patch", width="20",command=generateGame) 

MissLabel = Label(root, text="Missiles:", fg="white", bg="#1e1e1e")
SupLabel = Label(root, text="Super Missiles:", fg="white", bg="#1e1e1e")
PBLabel = Label(root, text="Power Bombs:",fg="white",bg="#1e1e1e")
ShieldLabel = Label(root, text="Shields:",fg="white",bg="#1e1e1e")
ETankLabel = Label(root, text="E-Tanks:",fg="white",bg="#1e1e1e")
Itemcount = Label(root, text="0/110", fg="white", bg="#1e1e1e")

MissEntry = Entry(root)
MissEntry.insert(0, "50")
SupEntry = Entry(root)
SupEntry.insert(0, "20")
PBEntry = Entry(root)
PBEntry.insert(0, "16")
ShieldEntry = Entry(root)
ShieldEntry.insert(0, "14")
ETankEntry = Entry(root)
ETankEntry.insert(0, "14")


seedEntry.grid(column=1, row=2, pady="5")
seedLabel.grid(column=0, row=2, padx="5")
e.grid(column=1, row=0, padx="10")
o.grid(column=1,row=1, pady="5")
inbutton.grid(column=0, row=0)
outButton.grid(column=0,row=1)
patchButton.grid(column=0,row=3)
MissLabel.grid(column=2, row=0, padx="10")
SupLabel.grid(column=2, row=1, padx="10")
PBLabel.grid(column=2, row=2, padx="10")
ShieldLabel.grid(column=2, row=3, padx="10")
ETankLabel.grid(column=2, row=4, padx="10")
Itemcount.grid(column=2, row=5, padx="10")
MissEntry.grid(column=3, row=0, pady="5")
SupEntry.grid(column=3, row=1, pady="5")
PBEntry.grid(column=3, row=2, pady="5")
ShieldEntry.grid(column=3, row=3, pady="5")
ETankEntry.grid(column=3, row=4, pady="5")


updateItems()
root.mainloop()