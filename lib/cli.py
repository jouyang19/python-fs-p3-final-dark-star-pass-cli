from db.user import User
from db.password import Password

user_id = None

def delete_entry(entry_id=None):
    if entry_id is None:
        delete_id = input("    Type account # to delete: ")
        entry = Password.find_by_id(delete_id)
        entry.delete_row()
        view_vault()
    elif entry_id:
        entry = Password.find_by_id(entry_id)
        entry.delete_row()
    else:
        return view_vault()

def sign_up():
    new_username = input("    Username: ")
    new_password = input("    Password: ")
    user = User.create(new_username, new_password)
    global user_id
    user_id = user.id
    return main()

def log_in():
    username = input("    Username: ")
    password = input("    Password: ")
    user = User.find_by_name(username)
    if user:
        if password == user.password:
            global user_id
            user_id = user.id
            return user_dashboard()
    else:
        print("    Wrong username or password")
        return main()
    
    
def view_vault():
    print('''
    ================================================
    **************** Password Vault ****************
    (Accounts)''')
    for item in Password.find_all_by_user_id(user_id):
        print("    ")
        print(item)
    print("""
    (Options)
    [1] View Acccount
    [2] Edit Account
    [3] Delete Account
    [4] Go Back
    
    """)
    
    def select():
        choice = input("    Select an option: ")
        if choice == "1":
            def again():
                entry_id = input("    Enter Account #: ")
                if entry_id.isdigit():
                    view_entry(entry_id)
                elif entry_id.isdigit() is False:
                    print("    Please try again.")
                    again()
                else:
                    print("    Account does not exist")
                    return view_vault()
            again()
        elif choice == "2":
            entry_id = input("    Enter Account #: ")
            return edit_entry(entry_id)
        elif choice == "3":
            return delete_entry()
        elif choice == "4": 
            return user_dashboard()
        else:
            return view_vault()
        
    select()
    
    
def view_entry(entry_id):
    
    entry = Password.find_by_id(entry_id)
    
    if entry and entry.user_id == user_id:
        print(f''' 
    ===============================================   
    *************** Account Details ***************
    
    {entry.title}
    
    Username: {entry.username}
    Password: {entry.password}
    
    [1] Edit    
    [2] Back                             [3] Delete
    ''')
    choice = input("    select an option: ")
    if choice == "1":
        edit_entry(entry.id)
    elif choice == "2":
        return view_vault()
    elif choice == "3":
        delete_entry()
    elif choice == "4": 
        return user_dashboard()
        
    else:
        return view_entry(entry.id)
    
def edit_entry(entry_id): 
    
    entry = Password.find_by_id(entry_id)
    
    if entry and entry.id == entry_id:
        print(f'''
    ===============================================
    *************** Account Details ***************
        
    {entry.title}
        
    Username: {entry.username}
    Password: {entry.password}
        
    Which field would you like to edit:
        
    (1) Title? or (2) Username? or (3) Password?
                                            
    (4) Back                       (5) Delete entry                        
    ===============================================
    ''')
        choice = input("    select an option: ")
        if choice == "1":
            new_title = input("    Enter new title: ")
            entry.title = new_title
            entry.update()
            print("    Title updated successfully!")
            return edit_entry(entry.id)
        elif choice == "2":
            new_username = input("    Enter new username: ")
            entry.username = new_username
            entry.update()
            print("    Username updated successfully!")
            return edit_entry(entry.id)
        elif choice == "3":
            new_password = input("    Enter new password: ")
            entry.password = new_password
            entry.update()
            print("Password updated successfully!")
            return edit_entry(entry.id)
        elif choice == "4":
            return view_entry(entry.id)
        elif choice == "5":
            delete_entry(entry.id)
            return view_vault()
        else:
            return edit_entry(entry.id)
    else: 
        print("    Account does not exist")
        return view_vault()

def user_dashboard():
    print("""
    ===============================================
    ****************** Dashboard ******************

    [1] Password Vault
    [2] Add Password
    [3] Search
    [4] Log Out

    """)
    choice = input("    Select an option: ")
    if choice == "1":
        view_vault()
    elif choice == "2":
        Password.create_table()
        title = input("    Account Title: ")
        username = input("    Account Username: ")
        password = input("    Account Password: ")
        global user_id
        account = Password.create(title, username, password, user_id)
        return user_dashboard()
    elif choice == "3":
        pass
    elif choice == "4":
        user_id = None
        return main()
    else:
        return user_dashboard()

def main():

    print("""
    ===============================================
    **************** Dark Star Pass ***************

    [1] Log In
    [2] Sign Up
    [3] Quit

    """)

    done = False

    while not done:
        
        choice = input("    Select an option: ")
        if choice == "1":
            log_in()
            return main()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            exit()
        else:
            print('Please try again.')

if __name__ == "__main__":
    Password.create_table()
    User.create_table()
    main()
    