#Question 2: Graph
#1. Graph class
class Graph:
    #Constructor
    def __init__(self):
        #Store vertices and outgoing edges using an adjacency list
        self.adjacency_list = {} #vertex -> list of vertices it points to (outgoing edges)

    #Add a vertex if it does not already exist
    def addVertex(self, vertex):
        if vertex in self.adjacency_list:
            return False
        self.adjacency_list[vertex] = []
        return True

    #Add a directed edge if both vertices exist
    def addEdge(self, from_vertex, to_vertex):
        if from_vertex not in self.adjacency_list or to_vertex not in self.adjacency_list:
            return False #One or both vertices are not found
        if to_vertex in self.adjacency_list[from_vertex]:
            return False #Edge already exists
        #Both vertices exist but no edge yet
        self.adjacency_list[from_vertex].append(to_vertex) #Add to_vertex to from_vertex's outgoing list
        return True #Edge added successfully

    #Remove an existing directed edge
    def removeEdge(self, from_vertex, to_vertex):
        if from_vertex not in self.adjacency_list or to_vertex not in self.adjacency_list[from_vertex]:
            return False #Edge not found
        self.adjacency_list[from_vertex].remove(to_vertex) #Remove edge between both vertices
        return True

    #List all incoming vertices with an edge pointing into this vertex (Option 3)
    def listIncomingAdjacentVertex(self, vertex):
        incoming = []
        for other_vertex in self.adjacency_list:
            if vertex in self.adjacency_list[other_vertex]:
                incoming.append(other_vertex)
        return incoming

    #List all outgoing vertices pointed by this vertex (Option 4)
    def listOutgoingAdjacentVertex(self, vertex):
        return self.adjacency_list[vertex]

    #Get all vertices
    def getVertices(self):
        return list(self.adjacency_list.keys())

#2. Course Class
class Course:
    #Constructor
    def __init__(self, course_code, course_name, credit_hours, level):
        self.course_code = course_code      #str
        self.course_name = course_name      #str
        self.credit_hours = credit_hours    #int
        self.level = level                  #str: "Core" or "Elective"

    #Display a readable course representation (Option 1)
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

    #Display the full details of the course (Option 2)
    def details(self):
        return (f"Course Code   : {self.course_code}\n"
                f"Course Name   : {self.course_name}\n"
                f"Credit Hours  : {self.credit_hours}\n"
                f"Level         : {self.level}")

    #Display Profile with course information based on Core / Elective level (Option 5)
    def profile(self):
        if self.level == "Core":
            return self.details()
        return f"Course Name : {self.course_name}\n(Details hidden for elective courses)"

#3. Helper Functions
#Find a course using its course code, return None if not found
def find_course(courses, course_code):
    if course_code in courses:
        return courses[course_code]
    return None

#Check if a course name already exists (ignores upper/lower case)
def course_name_exists(courses, course_name):
    for course in courses.values(): #loop over the values to read the names
        if course.course_name.lower() == course_name.lower():
            return True #Course name found
    return False

#Ask user for a course code and return the course (None if not found)
def input_course(courses, message):
    course_code = input(message).strip().upper() #Accept lowercase input
    course = find_course(courses, course_code)
    if course is None:
        print("Course Not Found")
    return course

#Print a list of courses or a message if empty
def print_course_list(course_list, empty_message):
    if len(course_list) == 0:
        print(empty_message)
    for course in course_list:
        print(f"- {course.course_code} ({course.course_name})")

def main():
    #Create graph and course lookup (course code -> Course)
    graph = Graph()
    courses = {}

    #Create predefined Course objects
    predefined_courses = [
        #Course(course_code, course_name, credit_hours, level)
        Course("CS101", "Introduction to Programming", 4, "Core"),
        Course("CS102", "Discrete Mathematics", 3, "Core"),
        Course("CS201", "Data Structures", 4, "Core"),
        Course("CS202", "Database Systems", 3, "Core"),
        Course("CS301", "Algorithms", 4, "Core"),
        Course("CS302", "Web Development", 3, "Elective"),
        Course("CS401", "Machine Learning", 3, "Elective")
    ]

    #Add each course as a graph vertex
    for course in predefined_courses:
        graph.addVertex(course)
        courses[course.course_code] = course

    #Add prerequisites: edge from prerequisite -> course it unlocks
    prerequisites = [
        ("CS101", "CS201"), #Introduction to Programming -> Data Structures.
        ("CS101", "CS202"), #Introduction to Programming -> Database Systems.
        ("CS102", "CS201"), #Discrete Mathematics -> Data Structures.
        ("CS102", "CS301"), #Discrete Mathematics -> Algorithms.
        ("CS201", "CS301"), #Data Structures -> Algorithms.
        ("CS202", "CS302"), #Database Systems -> Web Development.
        ("CS301", "CS401"), #Algorithms -> Machine Learning.
    ]

    for prerequisites_code, course_code in prerequisites:
        graph.addEdge(courses[prerequisites_code], courses[course_code])

    #Menu Loop
    while True:
        print("\n==== University Course Prerequisite System ====")
        print("1. View All Courses")
        print("2. View Course Details")
        print("3. View Prerequisites of a Course")
        print("4. View Courses Unlocked by a Course")
        print("5. View Course Profile (Core / Elective)")
        print("6. Add Course")
        print("7. Add Prerequisite")
        print("8. Remove Prerequisite")
        print("9. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            #List all course names
            print("\nAvailable Courses:")
            number = 1
            for course in graph.getVertices():
                print(f"{number}. {course}")
                number += 1

        elif choice == "2":
            #View all details of one course
            course = input_course(courses, "Enter course code: ")
            if course is not None:
                print(course.details())

        elif choice == "3":
            #Prerequisites = incoming edges
            course = input_course(courses, "Enter course code: ")
            if course is not None:
                print(f"Prerequisites for {course}:")
                print_course_list(graph.listIncomingAdjacentVertex(course), "No prerequisites.")

        elif choice == "4":
            #Unlocked courses = outgoing edges
            course = input_course(courses, "Enter course code: ")
            if course is not None:
                print(f"Courses unlocked by {course}:")
                print_course_list(graph.listOutgoingAdjacentVertex(course), "Does not unlock any course.")

        elif choice == "5":
            #Profile depends on Core / Elective
            course = input_course(courses, "Enter course code: ")
            if course is not None:
                print(course.profile())

        elif choice == "6":
            #Add a new course (new vertex)
            if len(courses) >= 10:
                print("Maximum of 10 courses reached.")
                continue
            #Verify course_code
            course_code = input("Enter new course code: ").strip().upper()
            if course_code == "":
                print("Course code cannot be empty. Please try again.")
                continue
            if find_course(courses, course_code) is not None:
                print("Course Already Exists")
                continue
            #Verify course_name
            course_name = input("Enter new course name: ").strip()
            if course_name == "":
                print("Course name cannot be empty. Please try again.")
                continue
            if course_name_exists(courses, course_name):
                print("Course name already exists")
                continue
            #Verify credit hours
            try:
                credit_hours = int(input("Enter credit hours: "))
            except ValueError:
                print("Invalid credit hours. Please try again.")
                continue
            if credit_hours <= 0:
                print("Credit hours must be greater than 0. Please try again.")
                continue
            #Verify level
            level = input("Enter level (Core / Elective): ").strip().capitalize()
            if level != "Core" and level != "Elective":
                print("Level must be Core or Elective. Please try again.")
                continue

            #Create new Course object and add it to the graph and dictionary
            course = Course(course_code, course_name, credit_hours, level)
            graph.addVertex(course)
            courses[course_code] = course
            print(f"Course {course} added successfully.")

        elif choice == "7":
            #7. Add Prerequisite
            #Course X adds course Y as prerequisite: new edge Y-> X
            course_x = input_course(courses, "Enter course code: ")
            if course_x is None:
                continue
            course_y = input_course(courses, "Enter prerequisite course code: ")
            if course_y is None:
                continue
            if course_x == course_y:
                print("A course cannot be its own prerequisite. Please try again.")
                continue
            if graph.addEdge(course_y, course_x):
                print(f"{course_y.course_code} is now a prerequisite of {course_x.course_code}.")
            else:
                print(f"{course_y.course_code} is already a prerequisite of {course_x.course_code}.")

        elif choice == "8":
            #8. Remove Prerequisite
            #Course X removes course Y as prerequisite: remove edge Y -> X
            course_x = input_course(courses, "Enter course code: ")
            if course_x is None:
                continue
            course_y = input_course(courses, "Enter prerequisite course code to remove: ")
            if course_y is None:
                continue

            if graph.removeEdge(course_y, course_x):
                print(f"{course_y.course_code} is no longer a prerequisite of {course_x.course_code}.")
            else:
                print(f"{course_y.course_code} is not a prerequisite of {course_x.course_code}.")

        elif choice == "9":
            #Exit program
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
