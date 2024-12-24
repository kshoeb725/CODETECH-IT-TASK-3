import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database


# Function to validate login credentials
def validate_login(username, password):
   
    return username == "user" and password == "pass"


def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if validate_login(username, password):
        messagebox.showinfo("Login Successful", "Welcome to Inventory Management Sysytem !")
        root.destroy()  # Close the login window
        open_main_app()  # Open the main application
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to open the main application
def open_main_app():
    def insert():
        id =id_entry.get()
        name =name_entry.get()
        stock =stock_entry.get()
        if not (id and name and stock):
            messagebox.showerror('Error','Enter all fields.')
        elif database.id_exists(id):
            messagebox.showerror('Error','ID already Exists')
        else:
            try:
                stock_value=int(stock)
                database.insert_products(id,name,stock_value)
                add_to_treeview()
                clear()
                create_chart()
                messagebox.showinfo('Success','Data has been inserted.')
            except:
                messagebox.showinfo('Error','Stock should be an integer.')
    
    
    def add_to_treeview():
        products=database.fetch_products()
        tree.delete(*tree.get_children())
        for product in products:
            tree.insert('',END,values=product)
    
    def clear(*clicked):
        if clicked:
            tree.selection_remove(tree.focus())
            tree.focus('')
            id_entry.delete(0,END)
            name_entry.delete(0,END)
            stock_entry.delete(0,END)
    

    def display_data(Event):
        selected_item=tree.focus()
        if selected_item:
            row=tree.item(selected_item)['values']
            clear()
            id_entry.insert(0,row[0])
            name_entry.insert(0,row[1])
            stock_entry.insert(0,row[2])
        else:
            pass
    
    
    
    def delete():
        selected_item=tree.focus()
        if not selected_item:
            messagebox.showerror('Error','Choose a prdouct to delete.')
        else:
            id=id_entry.get()
            database.delete_products(id)
            add_to_treeview()
            clear()
            create_chart()
            messagebox.showinfo('success','data has been Deleted.')
        
        
    def update():
        selected_item=tree.focus()
        if not selected_item:
            messagebox.showerror('Error','Chosse a prdouct to update.')
        else:
            id=id_entry.get()
            name=name_entry.get()
            stock=stock_entry.get()
            database.update_products(name,stock,id)
            add_to_treeview()
            clear()
            create_chart()
            messagebox.showinfo('success','data has been updated.')

    
    
    def create_chart():
        product_details=database.fetch_products()
        product_names=[product[1] for product in product_details]
        stock_values=[product[2] for product in product_details]
    
        figure=Figure(figsize=(10,3.8), dpi=80,facecolor='#0A0B0C')
        ax=figure.add_subplot(111)
        ax.bar(product_names,stock_values,width=0.4,color='#11EA05')
        ax.set_xlabel('product Name',color='#fff',fontsize=10)
        ax.set_ylabel('stock values',color='#fff',fontsize=14)    
        ax.set_title("Product Stock Levels",color='#fff',fontsize=14)
        ax.tick_params(axis='y',labelcolor='#fff',labelsize=12)
        ax.tick_params(axis='x',labelcolor='#fff',labelsize=12)
        ax.set_facecolor('#1B181B')
    
        canvas=FigureCanvasTkAgg(figure)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,padx=0,pady=405)
    
    
                
    app=customtkinter.CTk()
    app.title('Inventory Management Sysytem')
    app.geometry('800x720+300-11')
    app.config(bg='#0A0B0C')
    app.resizable(False,False)

    font1=('Arial',25,'bold')
    font2=('Arial',18,'bold')
    font3=('Arial',13,'bold')
    
    title_label=customtkinter.CTkLabel(app,font=font1,text='Product Details',text_color='#fff',bg_color='#0A0B0C')
    title_label.place(x=35,y=15)

    frame=customtkinter.CTkFrame(app,bg_color='#0A0B0C',fg_color='#1B1B21',corner_radius=10,border_width=2,border_color='#fff',width=200,height=370)
    frame.place(x=25,y=45)

    id_label= customtkinter.CTkLabel(frame,font=font2,text='* Product_ID: ',text_color='#fff',bg_color='#1B1B21')
    id_label.place(x=43,y=75)

    id_entry= customtkinter.CTkEntry(frame,font=font2,text_color='#000',fg_color='#fff',border_color='#B2016C',border_width=2,width=160)
    id_entry.place(x=20,y=105)

    name_label= customtkinter.CTkLabel(frame,font=font2,text='* Product Name: ',text_color='#fff',bg_color='#1B1B21')
    name_label.place(x=40,y=140)

    name_entry= customtkinter.CTkEntry(frame,font=font2,text_color='#000',fg_color='#fff',border_color='#B2016C',border_width=2,width=160)
    name_entry.place(x=20,y=175)

    stock_label= customtkinter.CTkLabel(frame,font=font2,text='* In Stock: ',text_color='#fff',bg_color='#1B1B21')
    stock_label.place(x=40,y=210)

    stock_entry= customtkinter.CTkEntry(frame,font=font2,text_color='#000',fg_color='#fff',border_color='#B2016C',border_width=2,width=160)
    stock_entry.place(x=20,y=245)

    add_button= customtkinter.CTkButton(frame,command=insert,font=font2,text='Add',fg_color='#047E43',hover_color='#025B30',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
    add_button.place(x=15,y=280)

    clear_button= customtkinter.CTkButton(frame,command=lambda:clear(True),font=font2,text='Clear',fg_color='#E93E05',hover_color='#A82A00',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
    clear_button.place(x=108,y=280)

    update_button= customtkinter.CTkButton(frame,command=update,font=font2,text='update',fg_color='#E93E05',hover_color='#A82A00',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
    update_button.place(x=15,y=320)

    delete_button= customtkinter.CTkButton(frame,command=delete,font=font2,text='Delete',fg_color='#D20B02',hover_color='#A8F060',bg_color='#1B1B21',cursor='hand2',corner_radius=8,width=80)
    delete_button.place(x=108,y=320)

    style=ttk.Style(app)
    style.theme_use('clam')
    style.configure('Treeview',font=font3,foreground='#fff',background='#1B1B21',fieldground='#1B1B21')
    style.map('Treeview',background=[('selected','#AA04A7')])
    tree=ttk.Treeview(app,height=17)

    tree['column']=('ID','Name','In stock')

    tree.column('#0',width=0,stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER,width=150)
    tree.column('Name',anchor=tk.CENTER,width=150)
    tree.column('In stock',anchor=tk.CENTER,width=150)

    tree.heading('ID',text='ID')
    tree.heading('Name',text='Name')
    tree.heading('In stock',text='In stock')

    tree.place(x=300,y=45)

    tree.bind('<ButtonRelease>',display_data)

    
    add_to_treeview()
    create_chart()
    app.mainloop()


# Create the login window
root = customtkinter.CTk()
root.title("Login Page")
root.geometry('800x720+300-10')

# Create and place the username label and entry
label_username = customtkinter.CTkLabel(root, text="Username:")
label_username.pack(pady=5)
entry_username = customtkinter.CTkEntry(root)
entry_username.pack(pady=5)

# Create and place the password label and entry
label_password = customtkinter.CTkLabel(root, text="Password:")
label_password.pack(pady=5)
entry_password = customtkinter.CTkEntry(root, show="*")
entry_password.pack(pady=5)

# Create and place the login button
button_login = customtkinter.CTkButton(root,command=login, text="Login")
button_login.pack(pady=20)

           
# Start the login window
root.mainloop()