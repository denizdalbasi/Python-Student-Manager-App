# Import necessary tools (libraries) for creating the graphical window.
import tkinter as tk  # 'tkinter' is the main library for creating windows. 'tk' is a shorter nickname.
from tkinter import ttk, messagebox, \
    simpledialog  # Other useful parts of tkinter for tables, pop-up messages, and input boxes.
from Student import *  # Import everything from our 'Student.py' file (the Student blueprint).
from Classroom import *  # Import everything from our 'Classroom.py' file (the Classroom organizer).


class StudentManagerApp:
    # This defines the blueprint for our main application window.

    def __init__(self, root):
        # This is the constructor for the application window itself.
        # 'root' is the main window that Tkinter creates.

        self.root = root  # Store the main window so we can control it.
        self.root.title("Student Manager")  # Set the text that appears at the top of the window.
        self.root.geometry("900x600")  # Set the initial size of the window (width x height in pixels).

        self.classroom = Classroom()  # Create a new 'Classroom' object to manage our students.
        self.data_file = "students.txt"  # Define the name of the file where we'll save and load student data.

        self.current_students = []  # This list will hold the students currently shown in the table.
        # (It might be all students, or just search results, or sorted results).
        self.load_students()  # Call a function to load any existing student data from the file.

        self.create_search_widgets()  # Call a function to set up the search bar area at the top.
        self.create_widgets()  # Call a function to set up all the buttons and the main student table.
        self.refresh_student_list()  # Call a function to fill the table with all students when the app starts.

    def create_search_widgets(self):
        # This function sets up the search bar part of the window.

        search_frame = tk.Frame(self.root)  # Create a rectangular area (frame) to neatly hold search-related items.
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        # 'pack' arranges the frame: put it at the TOP, make it fill the available horizontal space (X),
        # and give it some padding (space) around its edges.

        search_label = tk.Label(search_frame, text="Search:")  # Create a text label that says "Search:".
        search_label.pack(side=tk.LEFT, padx=(0, 5))  # Place the label to the LEFT inside the search frame.

        self.search_var = tk.StringVar()  # Create a special variable that can hold text and notify us when it changes.
        self.search_var.trace_add('write',
                                  self.on_search_change)  # Tell this variable: "Whenever someone types into me ('write'),
        # run the 'on_search_change' function."

        search_entry = tk.Entry(search_frame, textvariable=self.search_var)  # Create an input box for typing.
        # Link it to our 'search_var' variable.
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Place the input box to the LEFT, fill horizontally,
        # and let it expand to take up extra space.

    def on_search_change(self, *_):
        # This function runs automatically every time the user types something in the search box.
        # '*_' is a placeholder for extra information Tkinter sends, which we don't need right now.

        search_text = self.search_var.get().strip()  # Get the text from the search box and remove extra spaces.
        if search_text == "":
            self.show_all_students()  # If the search box is empty, show all students again.
        else:
            filtered = self.classroom.search_student_partial(
                search_text)  # Use the Classroom to find students matching the search.
            self.refresh_student_list(filtered)  # Update the table to show only the found students.

    def create_widgets(self):
        # This function sets up all the main buttons and the student table in the window.

        button_frame = tk.Frame(self.root)  # Create another frame to hold all the buttons.
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)  # Place it at the TOP, filling horizontally.

        # Now, create each button and tell it what function to run when clicked ('command=').
        # They are all packed to the LEFT, filling horizontally and expanding evenly.
        btn_add = tk.Button(button_frame, text="Add Student", command=self.add_student)
        btn_add.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_update = tk.Button(button_frame, text="Update Student", command=self.update_student)
        btn_update.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_delete = tk.Button(button_frame, text="Delete Student", command=self.delete_student)
        btn_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_show_all = tk.Button(button_frame, text="Show All", command=self.show_all_students)
        btn_show_all.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # --- NEW SORTING BUTTONS ---
        # These are the new buttons to sort the student list.
        btn_sort_name = tk.Button(button_frame, text="Sort by Name", command=self.sort_by_name)
        btn_sort_name.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        btn_sort_average = tk.Button(button_frame, text="Sort by Average", command=self.sort_by_average)
        btn_sort_average.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        # --- END NEW BUTTONS ---

        # Frame to hold the student table (Treeview) with scrollbars.
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # This frame will fill all remaining space.

        # Define the names of the columns that will appear in our table.
        columns = ("first_name", "last_name", "midterm", "final", "project", "attendance", "average", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")  # Create the table widget.
        # 'show="headings"' means only show column titles, not a blank first column.

        # Loop through each column name to set up its title and how wide it is.
        for col in columns:
            self.tree.heading(col, text=col.replace("_",
                                                    " ").title())  # Set the column title (e.g., "first_name" becomes "First Name").
            self.tree.column(col, anchor=tk.CENTER, width=100,
                             stretch=True)  # Center text, set min width, and let it stretch.

        # Create a vertical scrollbar for the table.
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)  # Place it on the RIGHT and make it fill vertically.

        # Create a horizontal scrollbar for the table.
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)  # Place it at the BOTTOM and make it fill horizontally.

        # Connect the scrollbars to the table so they work together.
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill=tk.BOTH, expand=True)  # Place the table itself, filling all remaining space.

    def add_student(self):
        # This function is called when the "Add Student" button is clicked.

        # Pop up dialog boxes to ask for student information.
        first = simpledialog.askstring("Add Student", "First Name:")
        if not first: return  # If the user cancels or types nothing, stop here.
        last = simpledialog.askstring("Add Student", "Last Name:")
        if not last: return  # Stop if canceled/empty.
        try:
            # Ask for grades and attendance, converting them to numbers.
            midterm = float(simpledialog.askstring("Add Student", "Midterm Grade:"))
            final = float(simpledialog.askstring("Add Student", "Final Grade:"))
            project = float(simpledialog.askstring("Add Student", "Project Grade:"))
            attendance = float(simpledialog.askstring("Add Student", "Attendance %:"))
        except (TypeError, ValueError):
            # If the user types something that's not a valid number, show an error message.
            messagebox.showerror("Error", "Please enter valid numeric values.")
            return  # Stop here.

        # Create a new Student object using the collected information.
        # For new students, the status is automatically calculated by the Student class.
        student = Student(first, last, midterm, final, attendance, project)
        self.classroom.add_student(student)  # Add this new student to our Classroom's list.

        self.save_students()  # Save all students (including the new one) to the file.
        self.refresh_student_list()  # Update the table to show the new student.
        self.search_var.set("")  # Clear the search box.

    def update_student(self):
        # This function is called when the "Update Student" button is clicked.

        selected = self.tree.selection()  # Get which row (student) is currently selected in the table.
        if not selected:
            messagebox.showwarning("Warning",
                                   "Please select a student to update.")  # If no student is selected, warn the user.
            return  # Stop here.

        idx = int(selected[0])  # Get the unique ID of the selected row and convert it to a number (our index).
        student = self.current_students[idx]  # Use that index to get the actual Student object from our list.

        try:
            # Pop up dialogs to ask for new grades/attendance, showing the current values as a starting point.
            midterm = float(simpledialog.askstring("Update Student", "Midterm Grade:", initialvalue=student.midterm))
            final = float(simpledialog.askstring("Update Student", "Final Grade:", initialvalue=student.final))
            project = float(simpledialog.askstring("Update Student", "Project Grade:", initialvalue=student.project))
            attendance = float(
                simpledialog.askstring("Update Student", "Attendance %:", initialvalue=student.attendance))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Please enter valid numeric values.")  # Error if input is not a number.
            return  # Stop here.

        # Update the student object's properties with the new values.
        student.midterm = midterm
        student.final = final
        student.project = project
        student.attendance = attendance
        student.status = student.calculate_status()  # **IMPORTANT:** Recalculate the student's status based on their new grades.

        self.save_students()  # Save all changes to the file.
        self.refresh_student_list()  # Update the table to show the updated student.
        self.search_var.set("")  # Clear search.

    def delete_student(self):
        # This function is called when the "Delete Student" button is clicked.

        selected = self.tree.selection()  # Get the selected student row.
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete.")  # Warn if none selected.
            return  # Stop here.

        idx = int(selected[0])  # Get the index of the selected student.
        student = self.current_students[idx]  # Get the actual Student object.

        # Ask the user to confirm they want to delete this student.
        confirm = messagebox.askyesno("Confirm Delete", f"Delete {student.first_name} {student.last_name}?")
        if confirm:  # If they confirm:
            self.classroom.delete_student(student.first_name,
                                          student.last_name)  # Tell the Classroom to delete the student.
            self.save_students()  # Save the updated list (with the student removed) to the file.
            self.refresh_student_list()  # Update the table.
            self.search_var.set("")  # Clear search.

    # --- NEW SORTING METHODS ---
    def sort_by_name(self):
        # This function is called when the "Sort by Name" button is clicked.
        self.classroom.sort_students_by_name()  # Tell the Classroom to sort its internal list of students by name.
        self.refresh_student_list()  # Update the table to show the newly sorted list.
        self.search_var.set("")  # Clear the search box so the full, sorted list is visible.

    def sort_by_average(self):
        # This function is called when the "Sort by Average" button is clicked.
        self.classroom.sort_students_by_average()  # Tell the Classroom to sort students by their average grade.
        self.refresh_student_list()  # Update the table to show the newly sorted list.
        self.search_var.set("")  # Clear the search box.

    # --- END NEW METHODS ---

    # NOTE: The `filter_students` method is no longer connected to a button,
    # but it still exists in `Classroom.py` and `StudentManagerApp.py`.
    # You can remove it if you are sure you won't need it.
    def filter_students(self, status):  # This function is still here but not used by a button.
        filtered = self.classroom.filter_students(status)
        self.refresh_student_list(filtered)
        self.search_var.set("")

    def show_all_students(self):
        # This function is called when the "Show All" button is clicked (or search is cleared).

        # It refreshes the list to show all students currently in the classroom's main list.
        # This list might be the original order, or it might be sorted if a sort button was clicked.
        self.refresh_student_list(self.classroom.students)
        self.search_var.set("")  # Clear the search box.

    def refresh_student_list(self, students=None):
        # This is a very important function. It clears the table and then fills it with student data.
        # 'students=None' means it can either be given a specific list of students (like search results)
        # or it will use all students from the classroom.

        for item in self.tree.get_children():
            self.tree.delete(item)  # Loop through all existing rows in the table and delete them.

        if students is None:
            students = self.classroom.students  # If no specific list was given, use all students from the classroom.

        self.current_students = students  # Remember which students are currently displayed in the table.

        for idx, student in enumerate(students):
            avg = f"{student.average():.2f}"  # Calculate the average and format it to two decimal places.
            self.tree.insert("", "end", iid=str(idx), values=(
                student.first_name,  # Insert each piece of student data into a new row in the table.
                student.last_name,
                student.midterm,
                student.final,
                student.project,
                student.attendance,
                avg,  # The formatted average.
                student.status  # The student's status (Passed/Failed).
            ))

    def save_students(self):
        # This function saves all student data from the classroom's list to the 'students.txt' file.

        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                # Open the file in 'write' mode ("w"), which means it will erase any old content and start fresh.
                # 'encoding="utf-8"' helps handle different characters correctly.
                for student in self.classroom.students:  # Go through each student in our classroom.
                    # Create a line of text for each student, separating values with commas.
                    # This now includes the 'student.status' at the end.
                    line = f"{student.first_name},{student.last_name},{student.midterm},{student.final},{student.attendance},{student.project},{student.status}\n"
                    f.write(line)  # Write this line to the file.
        except Exception as e:
            # If anything goes wrong during saving (like file problems), show an error message.
            messagebox.showerror("Error", f"Failed to save students: {e}")

    def load_students(self):
        # This function loads student data from the 'students.txt' file into our classroom.

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                # Open the file in 'read' mode ("r").
                for line in f:  # Go through each line of text in the file.
                    try:
                        student = Student.from_line(
                            line)  # Use our Student blueprint's helper function to turn the line into a Student object.
                        self.classroom.add_student(student)  # Add this newly created student object to our classroom.
                    except ValueError as e:
                        # If a line in the file is badly formatted (e.g., missing commas), show a warning but keep going.
                        messagebox.showwarning("Data Load Warning", f"Skipping invalid line: {line.strip()} - {e}")
        except FileNotFoundError:
            # If the 'students.txt' file doesn't exist yet, that's okay, just do nothing.
            pass
        except Exception as e:
            # For any other loading error, show an error message.
            messagebox.showerror("Error", f"Failed to load students: {e}")


if __name__ == "__main__":
    # This special 'if' statement means the code inside it only runs when you start this file directly (not when imported).
    root = tk.Tk()  # Create the main window of our application.
    app = StudentManagerApp(root)  # Create an instance of our StudentManagerApp, passing it the main window.
    root.mainloop()  # Start the Tkinter event loop. This keeps the window open and responsive to clicks and typing.