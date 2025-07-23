#Python Student Manager App
#Overview
    The Python Student Manager App is a desktop application built using tkinter that provides a user-friendly interface for managing student records. It allows users to add, update, delete, search, and sort student data, including grades, attendance, and automatically calculated academic status (Passed/Failed). All data is persistently stored in a text file.

#Features
    Add Student: Easily add new student records with their first name, last name, midterm, final, project grades, and attendance percentage.
    
    Update Student: Modify existing student records.
    
    Delete Student: Remove student records from the system.
    
    Search Students: Quickly find students by typing partial first or last names in the search bar.
    
    Sort by Name: Organize the student list alphabetically by last name, then first name.
    
    Sort by Average: Arrange students by their overall average grade, from highest to lowest.
    
    Automatic Status Calculation: Student status ("Passed" or "Failed") is automatically determined based on their average grade (40% midterm, 40% final, 20% project) and attendance (minimum 60% average and 70% attendance to pass).
    
    Data Persistence: All student data is saved to and loaded from a students.txt file, ensuring your records are retained between sessions.
    
    User-Friendly Interface: Intuitive graphical interface with a clear table view for student data.


#File Structure
    Student.py: Defines the Student class, which is the blueprint for individual student objects, handling their attributes, average calculation, and pass/fail status.
    
    Classroom.py: Defines the Classroom class, which manages a collection of Student objects. It provides methods for adding, deleting, searching, and sorting students.
    
    StudentManagerApp.py: This is the main application file. It sets up the tkinter GUI, connects user interactions (button clicks, search input) to the Classroom and Student logic, and handles data loading/saving.
    
    students.txt (created automatically): This text file stores all your student data. Each line represents a student, with values separated by commas.

Data File Format (students.txt)
  The students.txt file stores student data in a comma-separated format. Each line represents one student record.

  #Format:
    first_name,last_name,midterm_grade,final_grade,attendance_percentage,project_grade,status
    
    Example:
    
    Oliver,Brown,88.0,7.0,7.0,7.0,Failed
    Ava,Davis,82.0,79.0,88.0,85.0,Passed
    Henry,Parker,68.0,69.0,65.0,60.0,Failed

    When you add a new student, their status is automatically calculated and saved.
    
    If you manually edit students.txt, ensure you maintain this 7-field comma-separated format for each student record.
