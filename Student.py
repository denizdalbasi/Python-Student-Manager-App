class Student:
    # This line defines a new 'blueprint' or 'type' called 'Student'.
    # Everything indented below 'class Student:' belongs to this blueprint.

    def __init__(self, first_name, last_name, midterm, final, attendance, project, initial_status=None):
        # This is a special function called the 'constructor'.
        # It's like the instruction manual for building a new 'Student' object.
        # When you create a student (e.g., Student("John", "Doe", ...)), this function runs automatically.
        # 'self' refers to the specific student object being created.
        # 'initial_status=None' means 'initial_status' is optional. If you don't provide it, it defaults to nothing.

        self.first_name = first_name  # Store the student's first name inside this student object.
        self.last_name = last_name  # Store the student's last name.
        self.midterm = midterm  # Store their midterm grade.
        self.final = final  # Store their final grade.
        self.attendance = attendance  # Store their attendance percentage.
        self.project = project  # Store their project grade.

        # Now, let's figure out if they passed or failed:
        if initial_status is not None:
            # If someone gave us an 'initial_status' (like "Passed" or "Failed" from the file)...
            self.status = initial_status  # ...then we use that status directly.
        else:
            # If no 'initial_status' was given (e.g., for a brand new student)...
            self.status = self.calculate_status()  # ...we'll figure out their status using the grades.

    def average(self):
        # This function calculates the student's overall average grade.
        # It belongs to each student object.
        # 'self' again refers to the specific student whose average we are calculating.

        # It's a weighted average: midterm (40%), final (40%), project (20%).
        return self.midterm * 0.4 + self.final * 0.4 + self.project * 0.2

    def calculate_status(self):
        # This function determines if a student "Passed" or "Failed" based on their grades and attendance.

        # Check two conditions: Is their average grade 60 or higher AND is their attendance 70% or higher?
        if self.average() >= 60 and self.attendance >= 70:
            return "Passed"  # If both are true, they passed!
        else:
            return "Failed"  # Otherwise, they failed.

    def __str__(self):
        # This is another special function that tells Python how to represent a Student object as a simple text string.
        # It's useful when you try to 'print()' a student object.

        # It creates a neat string showing their name, average, and status.
        return f"{self.first_name} {self.last_name} - Avg: {self.average():.2f}, Status: {self.status}"

    @staticmethod
    def from_line(line):
        # This is a 'static method'. It's like a helper function that belongs to the 'Student' blueprint,
        # but it doesn't need a specific student object to work.
        # Its job is to take a line of text (like from our 'students.txt' file) and turn it into a Student object.

        parts = line.strip().split(',')
        # 'line.strip()' removes any extra spaces or newlines from the ends of the text line.
        # '.split(',')' breaks the line into smaller pieces (a list of strings) wherever it finds a comma.
        # For example, "John,Doe,80,75,90,85,Passed" becomes ["John", "Doe", "80", "75", "90", "85", "Passed"].

        # Check if the line has 7 pieces (our new format with status at the end):
        if len(parts) == 7:
            return Student(
                parts[0],  # The first piece is the first name.
                parts[1],  # The second piece is the last name.
                float(parts[2]),  # Convert the third piece (midterm) to a number (decimal).
                float(parts[3]),  # Convert the fourth piece (final) to a number.
                float(parts[4]),  # Convert the fifth piece (attendance) to a number.
                float(parts[5]),  # Convert the sixth piece (project) to a number.
                parts[6]  # The seventh piece is the status (keep as text).
            )
        # For old files that might only have 6 pieces (no status mentioned):
        elif len(parts) == 6:
            return Student(
                parts[0],  # First name.
                parts[1],  # Last name.
                float(parts[2]),  # Midterm.
                float(parts[3]),  # Final.
                float(parts[4]),  # Attendance.
                float(parts[5])  # Project.
                # Notice: No status here. The Student's '__init__' function will calculate it.
            )
        else:
            # If the line doesn't have 6 or 7 pieces, it's a mistake.
            raise ValueError(f"Invalid line format in student data file: {line}")
            # This stops the program and shows an error message, telling us the line was badly formatted.