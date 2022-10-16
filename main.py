import fitz
import re 
import datetime 
import time
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
from dfa import nfa
import xlwt
from xlwt import Font, XFStyle, Workbook, Borders, Alignment

pdfs = []
curp_info = []
curp_aux = []


# create the window
root = Tk()
root.title('validador de numeros romanos')
root.resizable(False, False)
root.geometry("600x600")

#define columns
columns = ('Cadenas_validas')
tree = ttk.Treeview(root, columns=columns, show='headings')

# define headings
tree.heading('Cadenas_validas', text='Cadenas validas')

tree.grid(row=0, column=0, sticky='nsew')

scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

def select_files():
       #creo que es pa limpiar la pantalla
    curp_aux.clear()
    pdfs.clear()

    filetypes = (
        ('PDF files', '*.pdf'),
    )

    filenames = filedialog.askopenfilenames(
        title='Open files',
        initialdir='./',
        filetypes=filetypes)

    for f in filenames:
        if f != '':
            pdfs.append(f)
    
    if pdfs.__len__() <= 0:
        messagebox.showerror(
            title='Error al ejecutarse',
            message="No se ha cargado ningun archivo"
        )
        return 

    cleaned_text = readPDF()
    if cleaned_text.__len__() <= 0:
        messagebox.showwarning(
            title='Sin archivos validos',
            message="No hay archivos validos cargados para poder validar"
        )
        return

    msg = validar(cleaned_text)
    if curp_aux.__len__() <= 0:
        messagebox.showwarning(
            title='No hay numeros romanos',
            message="No se encontro ningun numero romano en los archivos revisados",
        )
        return

    messagebox.showinfo(
        title="Validacion completa",
        message="Numeros romanos validados y obtenidas correctamente"
    )
    conta = 0
    tree.delete(*tree.get_children())
    for c in curp_info:
        tree.insert('', conta, values=c)  
        conta += 1
    if msg.__len__() > 0:
        messagebox.showwarning(
            title="Numeros Romanos repetidos",
            message="Los siguientes Numeros Romanos no se pueden agregar ya que estas ya existen:\n" + msg
        )
    save_button.grid(column=0, row=1, sticky='w', padx=100, pady=10)
    clear_button = Button(root,text='Clear All',bg="#ad2d31",command=clearAll)
    clear_button.grid(column=0, row=1, sticky='w', padx=200, pady=10)


# open button
open_button = Button(root,text='Open Files',fg="#FFFFFF", bg="#0b70a6", command=select_files)
open_button.grid(column=0, row=1, sticky='w', padx=10, pady=10)
             
def clearAll():
    tree.delete(*tree.get_children())
    for _ in range(curp_info.__len__()):
        curp_info.pop()
    
def readPDF():
    cleaned_text = []
    right_files = ''
    bad_files = ''
    for i in range(pdfs.__len__()):
        pdf_document = pdfs[i]
        document = fitz.open(pdf_document)
        nameF = pdf_document.split('/')
        filename = nameF[-1]
        text = ''
        for x in range(document.page_count):
            page = document.load_page(x)
            text += page.get_text("text")
        if text.__len__() > 0:
            right_files += filename + "\n"
            entries = re.split(r'[\n,:,-,.,/,", ,!,¡,?,¿,(,),,,{,},<,>,[,]', text)
            for entry in entries:
                temp_text = entry.split(']')
                aux_text = (temp_text[0])
                if aux_text != '':
                    cleaned_text.append(aux_text)
        else:
            bad_files += filename + "\n"
    if right_files.__len__() > 0:
        messagebox.showinfo(
            title="Archivos Validos",
            message="Archivos con contenido valido para su lectura:\n\n" + right_files
        )
    if bad_files.__len__() > 0:        
        messagebox.showwarning(
            title='Error al cargar los archivos',
            message="Archivos PDF sin texto legible:\n\n" + bad_files
        )
    return cleaned_text
        
def validar(cleaned_text):
    msg = ''
    conta = 0   
    
    for t in cleaned_text:
        sex = ''
        if t.__len__() <=21 :     
            nfa
            nfa.show_diagram()
            if nfa.accepts_input(t):
                conta += 1
                curp_aux.append((t))

    for c in curp_aux:
        value = False
        if curp_info.__len__() > 0:
            for i in range(curp_info.__len__()):
                if (c.__eq__(curp_info[i])):
                    msg += str(c[0]) + "\n"
                    value = True
        if value == False:
            curp_info.append(c)
    return msg

def main():
    root.mainloop()

if __name__ == "__main__":
    main()