class Classroom:
    # This defines the blueprint for a 'Classroom'.

    def __init__(self):
        # This is the constructor for creating a new Classroom object.
        self.students = []  # When a classroom is created, it starts with an empty list to hold students.

    def add_student(self, student):
        # This function tries to add a 'student' object to the classroom's list.

        # 'not any(...)' checks if there is *no* student in the current list
        # that has the same first AND last name (ignoring if they are uppercase/lowercase).
        if not any(s.first_name.lower() == student.first_name.lower() and \
                   s.last_name.lower() == student.last_name.lower() for s in self.students):
            self.students.append(student)  # If no duplicate is found, add the new student to the list.
            return True  # Tell whoever called this function that it worked.
        return False  # Tell them it didn't work (because a student with that name already exists).

    def delete_student(self, first_name, last_name):
        # This function removes a student from the classroom's list by their name.

        original_count = len(self.students)  # Remember how many students we had before trying to delete.

        # This line creates a *new* list of students.
        # It includes all students from the old list EXCEPT the one with the matching first and last name.
        self.students = [s for s in self.students if not \
            (s.first_name.lower() == first_name.lower() and \
             s.last_name.lower() == last_name.lower())]

        # Check if the number of students is now less than before (meaning one was deleted).
        return len(self.students) < original_count

    def find_student(self, first_name, last_name):
        # This function searches for a specific student by their first and last name.

        for student in self.students:  # Go through each student in our list.
            if student.first_name.lower() == first_name.lower() and \
                    student.last_name.lower() == last_name.lower():
                return student  # If we find a match, give that student object back.
        return None  # If we go through all students and find no match, return nothing.

    def search_student_partial(self, query):
        # This function searches for students whose names *contain* a part of the 'query' text.

        query_lower = query.lower()  # Convert the search query to lowercase for easy comparison.
        # This creates a new list containing only students whose first OR last name (in lowercase)
        # has the 'query_lower' text inside it.
        return [s for s in self.students if \
                query_lower in s.first_name.lower() or \
                query_lower in s.last_name.lower()]

    def filter_students(self, status_to_filter):
        # This function creates a new list containing only students who have a specific 'status' (Passed/Failed).
        # (Note: This function is still here, but no longer connected to a button in the app.)

        return [s for s in self.students if s.status.lower() == status_to_filter.lower()]

    def sort_students_by_name(self):
        # This function rearranges the 'students' list within the classroom.
        # It sorts them alphabetically by their last name first, then by their first name.
        # 'key=lambda s: (...)' tells Python to sort based on these parts of the student object.
        self.students.sort(key=lambda s: (s.last_name.lower(), s.first_name.lower()))

    def sort_students_by_average(self):
        # This function rearranges the 'students' list.
        # It sorts them by their average grade, with the highest average first.
        # 'reverse=True' makes it sort from largest to smallest.
        self.students.sort(key=lambda s: s.average(), reverse=True)