from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk

def mainwindow() :
    global w,h
    window = Tk()
    window.title('POS System Final Project')
    window.config(bg='dodgerblue4')
    w = 1100
    h = 900
    x = window.winfo_screenwidth()/2 - w/2
    y = window.winfo_screenheight()/2 - h/2
    window.geometry("%dx%d+%d+%d"%(w,h,x,y))
    window.option_add('*font',"tahoma 16 bold")
    window.rowconfigure(0,weight=1)
    window.columnconfigure(0,weight=1)
    return window


def buy_window():
    global buy_frame,add_frame,result,productid_entry,productn_entry,cost_entry,quantity_entry  
    cursor.execute('SELECT * from lists')
    result = cursor.fetchall()
    buy_frame = Frame(window, bg='darkslategray4')
    buy_frame.grid(row=0,column=0,padx=50,pady=50,sticky='news')

    buy_frame.columnconfigure((0,1),weight=1)
    buy_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)

    buy_lbl = Label(buy_frame, text='Buy',bg='darkslategray4',fg='white',font='Tahoma 20 bold')
    buy_lbl.grid(row=0,column=0,columnspan=2)

    Button(buy_frame,text='Edit',command=edit_product).grid(row=0,column=1)

    add_frame = Frame(window, bg='darkslategray4')
    add_frame.grid(row=0,column=1,padx=50,pady=50,sticky='news')

    add_frame.columnconfigure((0,1),weight=1)
    add_frame.rowconfigure((0,1,2,3,4),weight=1)

    add_lbl = Label(add_frame, text='Add Product',bg='darkslategray4',fg='white',font='Tahoma 20 bold')
    add_lbl.grid(row=0,column=0,columnspan=2)

    Label(add_frame,text="Product ID",bg='#d2e69c').grid(row=1,column=0,stick='we')
    productid_entry = Entry(add_frame,width=20,textvariable=productid_spy)
    productid_entry.grid(row=1,column=1,sticky='w',pady=10)
    Label(add_frame,text="Product Name",bg='#d2e69c').grid(row=2,column=0,stick='we')
    productn_entry = Entry(add_frame,width=20,textvariable=productn_spy)
    productn_entry.grid(row=2,column=1,sticky='w',pady=10)
    Label(add_frame,text="Cost",bg='#d2e69c').grid(row=3,column=0,stick='we')
    cost_entry = Entry(add_frame,width=20,textvariable=cost_spy)
    cost_entry.grid(row=3,column=1,sticky='w',pady=10)
    Label(add_frame,text="Quantity",bg='#d2e69c').grid(row=4,column=0,stick='we')
    quantity_entry = Entry(add_frame,width=20,textvariable=quantity_spy)
    quantity_entry.grid(row=4,column=1,sticky='w',pady=10)

    if result:
        for i,data in enumerate(result):
            #print(data[0],data[1],data[2],data[3])
            listss = str(data[0])+" "+str(data[1])+" "+str(data[2])
            print(result)
            Radiobutton(buy_frame,text=listss,bg='#8fd9a8',value=i,variable=radiospy,command=clickradio).grid(row=i+1,column=0,sticky='s')
            

def clickradio():
    row = radiospy.get()
    #print(result[row][0],result[row][1],result[row][2])
    productid_entry['state'] = 'normal'
    productn_entry['state'] = 'normal'
    cost_entry['state'] = 'normal'

    productid_entry.delete(0,END)
    productn_entry.delete(0,END)
    cost_entry.delete(0,END)
    quantity_entry.delete(0,END)

    productid_entry.insert(0,result[row][0])
    productn_entry.insert(0,result[row][1])
    cost_entry.insert(0,result[row][2])
    quantity_entry.insert(0,1)

    productid_entry['state'] = 'readonly'
    productn_entry['state'] = 'readonly'
    cost_entry['state'] = 'readonly'

    update_button = Button(add_frame,text="Add to cart",command=add)
    update_button.grid(row=5,column=0,ipadx=5,ipady=5,pady=20)
    login_button = Button(add_frame,text="Go to cart",command=go_cart)
    login_button.grid(row=5,column=1,ipadx=5,ipady=5,pady=20)

def add():
    sql = '''
    insert into cart values (?,?,?,?)
    '''
    cursor.execute(sql,[productid_entry.get(),productn_entry.get(),cost_entry.get(),quantity_entry.get()])
    conn.commit()
    messagebox.showinfo("Admin:","Add to cart complete")
    productid_entry['state'] = 'normal'
    productn_entry['state'] = 'normal'
    cost_entry['state'] = 'normal'
    productid_entry.delete(0,END)
    productn_entry.delete(0,END)
    cost_entry.delete(0,END)
    quantity_entry.delete(0,END)

def go_cart():
    global carttree,pidcart_entry,pncart_entry,costcart_entry,qcart_entry,cartboxframe,cart_frame
    buy_frame.destroy()
    add_frame.destroy()
    cart_frame = Frame(window, bg='darkslategray4')
    cart_frame.pack(pady=20)
    cartbar = Scrollbar(cart_frame)
    cartbar.pack(side=RIGHT,fill=Y)
    Label(cart_frame,text="Cart",bg='darkslategray4').pack()
    carttree = ttk.Treeview(cart_frame,columns=("id","product","price","quantity"),yscrollcommand=cartbar.set)
    carttree.pack()
    cartbar.config(command=carttree.yview)
    carttree.heading("#0",text="",anchor=W)
    carttree.heading("id",text="Product ID",anchor=W)
    carttree.heading("product",text="Product Name",anchor=W)
    carttree.heading("price",text="Price Per Piece",anchor=W)
    carttree.heading("quantity",text="Quantity",anchor=W)
    carttree.column("#0",width=0,minwidth=0)
    carttree.column("id",anchor=W,width=120)
    carttree.column("product",anchor=W,width=120)
    carttree.column("price",anchor=W,width=120)
    carttree.column("quantity",anchor=W,width=120)
    carttree.delete(*carttree.get_children())
    carttree.bind('<Double-1>',carttreeclick)
    #labels
    cartboxframe = Frame(window,bg='pink')
    cartboxframe.pack(pady=20)
    pidcartlbl = Label(cartboxframe,text='Product ID',bg='lightblue')
    pidcartlbl.grid(row=0,column=0,sticky='news',padx=5,pady=5)
    pncartlbl = Label(cartboxframe,text='Product Name',bg='lightblue')
    pncartlbl.grid(row=0,column=1,sticky='news',padx=5,pady=5)
    costcartlbl = Label(cartboxframe,text='Cost',bg='lightblue')
    costcartlbl.grid(row=0,column=2,sticky='news',padx=5,pady=5)
    qcartlbl = Label(cartboxframe,text='Quantity',bg='lightblue')
    qcartlbl.grid(row=0,column=3,sticky='news',padx=5,pady=5)
    #EntryBoxes
    pidcart_entry = Entry(cartboxframe,bg='lightgrey',justify=CENTER)
    pidcart_entry.grid(row=1,column=0)
    pncart_entry = Entry(cartboxframe,bg='lightgrey',justify=CENTER)
    pncart_entry.grid(row=1,column=1)
    costcart_entry = Entry(cartboxframe,bg='lightgrey',justify=CENTER)
    costcart_entry.grid(row=1,column=2)
    qcart_entry = Entry(cartboxframe,bg='lightgrey',justify=CENTER)
    qcart_entry.grid(row=1,column=3)
    Button(window,text='Edit')
    sql = '''
    SELECT * FROM cart
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    for i,data in enumerate(result):
        if result:
            carttree.insert('','end',values=(data[0],data[1],data[2],data[3]))

    Button(cartboxframe,text="Edit",command=update_cart).grid(row=2,column=0,padx=10,ipadx=10,ipady=10)
    Button(cartboxframe,text="Delete",command=remove_cart).grid(row=2,column=1,padx=10,ipadx=10,ipady=10)
    Button(cartboxframe,text="Cashout",command=cashout).grid(row=2,column=2,padx=10,ipadx=10,ipady=10)
    Button(cartboxframe,text="Return to Home",command=home).grid(row=2,column=3,padx=10,ipadx=10,ipady=10)

def carttreeclick(event):
    pidcart_entry['state'] = 'normal'
    pncart_entry['state'] = 'normal'
    costcart_entry['state'] = 'normal'
    pidcart_entry.delete(0,END)
    pncart_entry.delete(0,END)
    costcart_entry.delete(0,END)
    qcart_entry.delete(0,END)
    valuescart = carttree.item(carttree.focus(),'values')
    pidcart_entry.insert(0,valuescart[0])
    pncart_entry.insert(0,valuescart[1])
    costcart_entry.insert(0,valuescart[2])
    qcart_entry.insert(0,valuescart[3])
    pidcart_entry['state'] = 'readonly'
    pncart_entry['state'] = 'readonly'
    costcart_entry['state'] = 'readonly'
    
def update_cart():
    selectedcart = carttree.focus()
    carttree.item(selectedcart,text="",values=(pidcart_entry.get(),pncart_entry.get(),costcart_entry.get(),qcart_entry.get()))
    sql = '''
            update cart
            set quantity=?
            where id=?
    '''
    cursor.execute(sql,[qcart_entry.get(),pidcart_entry.get()])
    conn.commit()

    pidcart_entry['state'] = 'normal'
    pncart_entry['state'] = 'normal'
    costcart_entry['state'] = 'normal'
    pidcart_entry.delete(0,END)
    pncart_entry.delete(0,END)
    costcart_entry.delete(0,END)
    qcart_entry.delete(0,END)

def remove_cart():
    msgcart = messagebox.askquestion ('Delete this product','Are you sure you want to delete this product on your cart',icon = 'warning')
    if msgcart == 'no':
        pidcart_entry['state'] = 'normal'
        pncart_entry['state'] = 'normal'
        costcart_entry['state'] = 'normal'
        pidcart_entry.delete(0,END)
        pncart_entry.delete(0,END)
        costcart_entry.delete(0,END)
        qcart_entry.delete(0,END)
    else:
        deletecartrow = carttree.selection()
        values = carttree.item(carttree.focus(),'values')
        carttree.delete(deletecartrow)
        sql = '''
            delete from cart where id=?
        '''
        cursor.execute(sql,[pidcart_entry.get()])
        conn.commit()
        pidcart_entry['state'] = 'normal'
        pncart_entry['state'] = 'normal'
        costcart_entry['state'] = 'normal'
        pidcart_entry.delete(0,END)
        pncart_entry.delete(0,END)
        costcart_entry.delete(0,END)
        qcart_entry.delete(0,END)
    
def cashout():
    global total,totalframe
    sql = '''
    select price,quantity from cart
    '''
    cursor.execute(sql)
    resultcash = cursor.fetchall()
    for i,data in enumerate(resultcash):
        total =  total+(int(data[0])*int(data[1]))
        continue
    totalcostwithtax = total*1.07
    totalframe = Frame(window,bg='pink')
    totalframe.pack(pady=20)
    lbltotalcost = Label(totalframe,text='')
    lbltotalcost.pack(pady=20)
    lbltotalcostwithtax = Label(totalframe,text='')
    lbltotalcostwithtax.pack(pady=20)
    lbltotalcost['text'] = "Total " + str(total) + " Baht."
    lbltotalcostwithtax['text'] = "Total with TAX 7% : " + str(totalcostwithtax) + " Baht."
    cartboxframe.destroy()
    Button(totalframe,text="Return to Home",command=home1).pack(ipady=20)


def edit_product():
    global pnedit_entry,costedit_entry,editframe,edittree,editboxframe,rowId
    #print('hi')
    buy_frame.destroy()
    add_frame.destroy()
    editframe = Frame(window, bg='darkslategray4')
    editframe.pack(ipady=20)
    editbar = Scrollbar(editframe)
    editbar.pack(side=RIGHT,fill=Y)
    Label(editframe,text="EditProduct",bg='darkslategray4').pack()
    edittree = ttk.Treeview(editframe,columns=("id","product","price"),yscrollcommand=editbar.set)
    edittree.pack()
    editbar.config(command=edittree.yview)
    edittree.heading("#0",text="",anchor=W)
    edittree.heading("id",text="Product ID",anchor=W)
    edittree.heading("product",text="Product Name",anchor=W)
    edittree.heading("price",text="Price Per Piece",anchor=W)
    edittree.column("#0",width=0,minwidth=0)
    edittree.column("id",anchor=W,width=120)
    edittree.column("product",anchor=W,width=120)
    edittree.column("price",anchor=W,width=120)
    edittree.delete(*edittree.get_children())
    edittree.bind('<Double-1>',edittreeclick)
    #labels
    editboxframe = Frame(window,bg='pink')
    editboxframe.pack(pady=20)
    pneditlbl = Label(editboxframe,text='Product Name',bg='lightblue')
    pneditlbl.grid(row=0,column=0,sticky='news',padx=5,pady=5)
    costeditlbl = Label(editboxframe,text='Cost',bg='lightblue')
    costeditlbl.grid(row=0,column=1,sticky='news',padx=5,pady=5)
    #EntryBoxes
    pnedit_entry = Entry(editboxframe,bg='lightgrey',justify=CENTER)
    pnedit_entry.grid(row=1,column=0)
    costedit_entry = Entry(editboxframe,bg='lightgrey',justify=CENTER)
    costedit_entry.grid(row=1,column=1)

    sql = '''
    SELECT * FROM lists
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    for i,data in enumerate(result):
        if result:
            edittree.insert('','end',values=(data[0],data[1],data[2]))
            rowId = i
    print(rowId)
    Button(editboxframe,text="Add",command=add_product).grid(row=2,column=0,padx=10,ipadx=10,ipady=10)
    Button(editboxframe,text="Edit",command=update_edit).grid(row=2,column=1,padx=10,ipadx=10,ipady=10)
    Button(editboxframe,text="Delete",command=remove_edit).grid(row=3,column=0,padx=10,ipadx=10,ipady=10)
    Button(editboxframe,text="Return to Home",command=home2).grid(row=3,column=1,padx=10,pady=5,ipadx=10,ipady=10)

def add_product():
    lastrow = rowId+1
    print(lastrow)
    sql = '''
    insert into lists values (?,?,?)
    '''
    cursor.execute(sql,[lastrow,pnedit_entry.get(),costedit_entry.get()])
    conn.commit()
    edittree.insert('','end', values=(lastrow,pnedit_entry.get(),costedit_entry.get()))
    pnedit_entry.delete(0,END)
    costedit_entry.delete(0,END)

def edittreeclick(event):
    global pidedit_entry
    pnedit_entry.delete(0,END)
    costedit_entry.delete(0,END)
    productedit = edittree.item(edittree.focus(),'values')
    pidedit_entry = productedit[0]
    pnedit_entry.insert(0,productedit[1])
    costedit_entry.insert(0,productedit[2])

def update_edit():
    selectededit = edittree.focus()
    edittree.item(selectededit,text="",values=(pidedit_entry,pnedit_entry.get(),costedit_entry.get()))
    sql = '''
            update lists
            set product=?,price=?
            where id=?
    '''
    cursor.execute(sql,[pnedit_entry.get(),costedit_entry.get(),pidedit_entry])
    conn.commit()

    pnedit_entry['state'] = 'normal'
    costedit_entry['state'] = 'normal'
    pnedit_entry.delete(0,END)
    costedit_entry.delete(0,END)

def remove_edit():
    msgedit = messagebox.askquestion ('Delete this product','Are you sure you want to delete this product on your shop',icon = 'warning')
    if msgedit == 'no':
        pnedit_entry['state'] = 'normal'
        costedit_entry['state'] = 'normal'
        pnedit_entry.delete(0,END)
        costedit_entry.delete(0,END)
    else:
        deleteeditrow = edittree.selection()
        values = edittree.item(edittree.focus(),'values')
        edittree.delete(deleteeditrow)
        sql = '''
            delete from lists where id=?
        '''
        cursor.execute(sql,[pidedit_entry])
        conn.commit()
        pnedit_entry['state'] = 'normal'
        costedit_entry['state'] = 'normal'
        pnedit_entry.delete(0,END)
        costedit_entry.delete(0,END)

def home():
    cart_frame.destroy()
    cartboxframe.destroy()
    buy_window()

def home1():
    sql = '''
    delete from cart
    '''
    cursor.execute(sql)
    conn.commit()
    cart_frame.destroy()
    cartboxframe.destroy()
    totalframe.destroy()
    buy_window()

def home2():
    editframe.destroy()
    editboxframe.destroy()
    buy_window()

window = mainwindow()
conn = sqlite3.connect('db/db_pos.db')
cursor = conn.cursor()  
radiospy = IntVar()
productid_spy = StringVar()
productn_spy = StringVar()
cost_spy = IntVar()
quantity_spy = IntVar()
total = 0
totalcostwithtax = 0
buy_window()
window.mainloop()