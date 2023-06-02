# Program for managing tasks assigned to users, which writes to and reads tasks and users
# from the "tasks.txt" and "user.txt" files respectively

# Import required module

import datetime
import os, time
import stat


# Define required functions

# Function to create dictionary of username/password combinations

def username_check():
    # Declare local variables

    users = {}

    # Access "user.txt" file in read mode

    with open("user.txt", "r") as f:

        # Run through "user.txt" file to check for matching combination

        for line in f:

            user_check = line.strip("\n")

            # Prevent range out of bound errors as caused by empty lines

            if user_check != "":
                user_check = user_check.split(", ")
                users.update({user_check[0]: user_check[1]})

    return users


# Function to create a list of tasks

def task_check():
    # Declare local variables

    tasks = []
    count = 1

    # Access "tasks.txt" file in read mode

    with open("tasks.txt", "r") as f:

        # Run through "tasks.txt" file to check for matching combination

        for line in f:

            task_check = line.strip("\n")

            # Prevent range out of bound errors as caused by empty lines

            if task_check != "":
                task_check = [task_check.split(", ") + [count]]
                tasks.extend(task_check)
                count += 1

    return tasks


# Function to log onto task manager program by matching username/password combination

def login():
    # Get username and password combination from user

    username = input("Please enter your username:\n")
    password = input("Please enter your password:\n")
    print()

    # Call username_check() function to compare login details to dictionary storage

    user_list = username_check()

    if username in user_list and user_list.get(username) == password:
        return username

    else:
        print("Your username and/or password is incorrect, please ensure your caps lock is off and try again.\n")
        return "loop"


# Function to display appropriate menu

def menu():
    # Declare local variables

    carry_on = True

    # While loop to continue returning to menu until user selects exit

    while carry_on:
        print("Please select one of the following options:\n")
        print("r\t- register user\n")
        print("a\t- add task\n")
        print("va\t- view all tasks\n")
        print("vm\t- view my tasks\n")
        print("gr\t- generate reports\n")

        # Only show the display statistics option if admin is logged in
        if admin_rights:
            print("d\t- display statistics\n")

        print("e\t- exit")
        print()
        selection = input()
        print()

        # if-elif-else statement to call appropriate function based on menu selection

        if selection.lower() == "r":
            reg_user()

        elif selection.lower() == "a":
            add_task()

        elif selection.lower() == "va":
            view_all()

        elif selection.lower() == "vm":
            view_mine()

        elif selection.lower() == "d":
            display_statistics()

        elif selection.lower() == "e":
            carry_on = False

        elif selection.lower() == "gr":
            generate_reports()

        else:
            print("Your selection did not meet a menu item. Please try again.\n")


# Function to register a new user to "user.txt" file

def reg_user():
    # Declare local variables

    carry_on = True

    user_list = username_check()

    # check that user has admin rights

    if admin_rights == False:
        print("You do not have permission to perform this action.\n")

    else:

        # While loop to ensure correct details are added

        while (carry_on):

            # Access "user.txt" file in append mode

            with open("user.txt", "a") as f:

                # Get username to be added from admin

                new_username = input("Please enter the username you would like to add, or 'e' to exit:\n")
                print()

                # check that username does not exist

                if new_username in user_list:
                    print("That username is already taken, please try a different username.\n")

                else:
                    password = input(f"Please enter a password for {new_username}:\n")
                    print()
                    confirmation = input("Please confirm the password entered:\n")

                    if password == confirmation:
                        f.write(f"\n{new_username}, {password}\n")
                        print(f"new user {new_username} has been added!")
                        print()
                        carry_on = False

                    else:
                        print("Your password and confirmation do not match, please try again.\n")


# Function to add a task to "tasks.txt" file

def add_task():
    # Declare local variables

    on_user_list = True

    # Call user_check for validation

    users_list = username_check()

    # Access the "tasks.txt" file in append mode

    with open("tasks.txt", "a") as f:

        # Get task information from user
        while (on_user_list):
            asigned_user = input("Who is the owner for this task?\n")

            # Ensure that assigned user is in the "user.txt" file
            if asigned_user in users_list:
                on_user_list = False
            else:
                print("The given user does not exist, please try again.\n")

        title = input("What is the task title?\n")
        description = input("Please enter a description of the task:\n")

        # Determine assigned date from local time

        today = datetime.date.today()

        # Format date to be in dd mmm yyyy format

        today = today.strftime("%d %b %Y")

        date_due = input("Please enter when the task is due in dd mmm yyyy format:\n")
        complete = "No"

        f.write(f"\n{asigned_user}, {title}, {description}, {today}, {date_due}, {complete}\n")


# Function to view all tasks within the "tasks.txt" file

def view_all():
    # Get list of tasks

    tasks = task_check()

    # Loop through each tasks to print them

    for i in range(0, len(tasks)):
        # Print task in a user friendly manner

        print("-" * 50)
        print(f"Task:\t\t\t{tasks[i][1]}")
        print(f"Assigned to:\t\t{tasks[i][0]}")
        print(f"Date assigned:\t\t{tasks[i][3]}")
        print(f"Due date:\t\t{tasks[i][4]}")
        print(f"Task complete?\t\t{tasks[i][5]}")
        print(f"Task description:\n{tasks[i][2]}")

    print("-" * 50)
    print()


# Function to view all tasks assigned to the logged in user within the "tasks.txt" file

def view_mine():
    # Get list of tasks

    tasks = task_check()

    # Loop through each tasks to print them

    for i in range(0, len(tasks)):

        # If user and assigned_user are the same, print task in a user friendly manner

        if user == tasks[i][0]:
            print("-" * 50)
            print(f"Task reference:\t\t{tasks[i][6]}")
            print(f"Task:\t\t\t{tasks[i][1]}")
            print(f"Assigned to:\t\t{tasks[i][0]}")
            print(f"Date assigned:\t\t{tasks[i][3]}")
            print(f"Due date:\t\t{tasks[i][4]}")
            print(f"Task complete?\t\t{tasks[i][5]}")
            print(f"Task description:\n{tasks[i][2]}")

    print("-" * 50)
    print()

    # Run function to choose a task to edit or mark complete
    select_task()


# Function to print the files "task_overview.txt" and "user_overview.txt" to the screen
# If files do not exist, first generate files

def display_statistics():
    # Declare local variables

    old_file = True

    # Check that files have been generated

    if (os.path.exists('./task_overview.txt') == False) or (os.path.exists('./user_overview.txt') == False):
        generate_reports()

    else:

        # Check when files were generated and ask user if they would like to update them

        task_time = os.stat('task_overview.txt')
        # convert format to a human readable form
        task_time = time.ctime(task_time[stat.ST_MTIME])

        user_time = os.stat('user_overview.txt')
        user_time = time.ctime(user_time[stat.ST_MTIME])

        print(f"task_overview.txt was last modified {task_time} and user_overview.txt was last modified {user_time}")

        while (old_file):

            regenerate = input("Would you like to update the files before proceeding? y/n\n")
            print()

            if regenerate.lower() == "y":
                generate_reports()
                print()
                old_file = False

            elif regenerate.lower() == "n":
                old_file = False

            else:
                print("invalid input\n")

    # Print both files to the screen
    with open('task_overview.txt', 'r') as f:
        for line in f:
            print(line, end='')

    print()

    with open('user_overview.txt', 'r') as g:
        for line in g:
            print(line, end='')

    print()


# Function to select a task

def select_task():
    # Get list of tasks

    tasks = task_check()

    # Declare local variables

    task_selection = True

    # While loop to get desired task number input

    while (task_selection):

        task_number = input("Please enter your task reference or '-1' to return to menu:\n")

        try:
            task_number = int(task_number)

        except:
            print("Invalid input\n")

        if task_number == -1:
            print()
            task_selection = False
            return

        else:
            for i in range(0, len(tasks)):

                # If user and assigned_user are the same plus task_number matches task reference, alow user to edit task or mark complete
                if task_number == tasks[i][6] and tasks[i][5].lower() == "yes":
                    print(f"task reference {task_number} is already complete, no further editing is permitted\n")

                elif user == tasks[i][0] and task_number == tasks[i][6]:
                    modify_or_complete = input("Please enter 'mt' to mark task as complete or 'ed' to edit task?\n")
                    print()

                    if modify_or_complete.lower() != 'mt' and modify_or_complete.lower() != 'ed':
                        print("Invalid input.\n")

                    elif modify_or_complete.lower() == 'mt':
                        mark_task(task_number)
                        return

                    else:
                        edit_task(task_number)
                        return


# Function to mark task as complete

def mark_task(task_number):
    # Get list of tasks

    tasks = task_check()

    # Declare local variables

    string_task = ""

    # Check for matching task number and amend completed statement to "yes"

    for i in range(0, len(tasks)):
        if task_number == tasks[i][6]:
            tasks[i][5] = "Yes"

        # Remove number added in by task_check() function

        tasks[i].pop()

        # Store each task in variable to be written to "tasks.txt" file

        string_task += ", ".join(tasks[i]) + "\n"

    # Open "tasks.txt" in write mode and write the variable "string_task" to file
    with open("tasks.txt", "w") as f:
        f.write(string_task)


# Function to edit assigned user and/or due date

def edit_task(task_number):
    # Get list of tasks and users

    tasks = task_check()
    user_list = username_check()

    # Declare local variables

    string_task = ""

    editing = True

    # Check if user would like to edit assigned person or due date
    while (editing):
        user_or_date = input(
            "Please enter 'user' to edit task assignment, 'date' to edit due date or 'both' to edit both:\n")

        if user_or_date.lower() == "user":

            # Have user enter newly assigned user, checking that username exists
            new_user = input("Please enter the username to which this task should be assigned:\n")

            if new_user in user_list:
                for i in range(0, len(tasks)):
                    if task_number == tasks[i][6]:
                        tasks[i][0] = new_user

                    # Remove number added in as part of task_check() function
                    tasks[i].pop()

                    string_task += ", ".join(tasks[i]) + "\n"

                editing = False

            else:
                print("Username does not exist\n")

        # have user enter in new due date

        elif user_or_date.lower() == "date":
            new_date = input("Please enter when the task is due in dd mmm yyyy format:\n")
            for i in range(0, len(tasks)):
                if task_number == tasks[i][6]:
                    tasks[i][4] = new_date
                tasks[i].pop()

                string_task += ", ".join(tasks[i]) + "\n"

                editing = False

        # Have user enter new assigned user, checking that username exists, and enter new due date

        elif user_or_date.lower() == "both":
            new_user = input("Please enter the username to which this task should be assigned:\n")
            if new_user in user_list:
                new_date = input("Please enter when the task is due in dd mmm yyyy format:\n")

                for i in range(0, len(tasks)):
                    if task_number == tasks[i][6]:
                        tasks[i][0] = new_user
                        tasks[i][4] = new_date

                    tasks[i].pop()

                    string_task += ", ".join(tasks[i]) + "\n"

                    editing = False
            else:
                print("Username does not exist\n")

    # Open "tasks.txt" file in write mode and write the variable "string_task" to it
    with open("tasks.txt", "w") as f:
        f.write(string_task)


# Function to generate 2 files: "task_overview.txt" and "user_overview.txt"

def generate_reports():
    # Get task list and user list

    task = task_check()
    users = username_check()

    # Convert dictionary "users" to a list of key values

    users = [*users]

    # Declare local variables

    total = len(task)
    total_users = len(users)
    complete = 0
    incomplete = 0
    overdue = 0
    percent_incomplete = 0
    percent_overdue = 0

    # Find and keep count of all tasks, incomplete tasks and overdue tasks
    for i in range(0, total):
        if task[i][5].lower() == "yes":
            complete += 1
        elif task[i][5].lower() == "no" and datetime.datetime.strptime(task[i][4],
                                                                       '%d %b %Y') < datetime.datetime.now():
            incomplete += 1
            overdue += 1
            percent_incomplete = (incomplete / total) * 100
            percent_overdue = (overdue / total) * 100

        elif task[i][5].lower() == "no":
            incomplete += 1
            percent_incomplete = (incomplete / total) * 100

    # Generate "task_overview.txt" file in an easy to read manner

    with open("task_overview.txt", "w") as f:
        f.write(f"Number of tasks\t\t- {total}\n")
        f.write(f"Number completed\t- {complete}\n")
        f.write(f"Number incomplete\t- {incomplete}\n")
        f.write(f"Number overdue\t\t- {overdue}\n")
        f.write(f"Percentage incomplete\t- {percent_incomplete:.2f}%\n")
        f.write(f"Percentage overdue\t- {percent_overdue:.2f}%\n")

    # Generate "user_overview.txt" filen an easy to read manner

    with open("user_overview.txt", "w") as g:
        g.write(f"Total users\t- {total_users}\n")
        g.write(f"Total tasks\t- {total}\n\n")

        # Loop through users to seperate tasks by their specific assigned user

        for i in range(0, total_users):

            # Local variables declared within for loop to prevent double counting from occuring

            user_tasks = 0
            completed = 0
            not_complete = 0
            user_overdue = 0
            task_percent = 0
            complete_percent = 0
            incomplete_percent = 0
            overdue_percent = 0

            # Loop through specific user tasks to find completion status and due dates. Count of number of tasks, completed or not and due date maintained

            for j in range(0, total):
                if users[i] == task[j][0] and task[j][5].lower() == "yes":
                    user_tasks += 1
                    completed += 1

                # datetime.datetime.strptime(input, format) converts the string format date into a date object format, allowing comparison against the current time
                # obtained via datetime.datetime.now(). datetime.today unsuitable due to the time element not generating as was present in teh strptime() method

                elif users[i] == task[j][0] and task[j][5].lower() == "no" and datetime.datetime.strptime(task[j][4],
                                                                                                          '%d %b %Y') < datetime.datetime.now():
                    user_tasks += 1
                    not_complete += 1
                    user_overdue += 1


                elif users[i] == task[j][0] and task[j][5].lower() == "no":
                    user_tasks += 1
                    not_complete += 1

                # Calculate user percentages, ensuring that 0 assigned tasks does not result in a divide by 0 error

                task_percent = (user_tasks / total) * 100
                if user_tasks != 0:
                    complete_percent = (completed / user_tasks) * 100
                    incomplete_percent = (not_complete / user_tasks) * 100
                    overdue_percent = (user_overdue / user_tasks) * 100

            # Write the results to the file before progressing to the next registered user
            g.write("-" * 50 + "\n")
            g.write(f"User: {users[i]}\n\n")
            g.write(f"Number of user tasks\t\t- {user_tasks}\n")
            g.write(f"Percentage of total tasks\t- {task_percent:.2f}%\n")
            g.write(f"Percentage completed\t\t- {complete_percent:.2f}%\n")
            g.write(f"Percentage incomplete\t\t- {incomplete_percent:.2f}%\n")
            g.write(f"Percentage overdue\t\t- {overdue_percent:.2f}%\n")


# Declare global variables

login_attempt = True
admin_rights = False

# Main program

# Loop to log onto task manager program
# If admin logs on, assign admin rights

while (login_attempt):
    user = login()

    if user == "admin":
        admin_rights = True
        login_attempt = False

    elif user != "loop":
        login_attempt = False

menu()