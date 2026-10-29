#Question 2: Graph
#1. Graph class
class Graph:
    #Constructor
    def __init__(self):
        #Store vertices and outgoing edges using an adjacency list
        self.adjacency_list = {} #vertex -> list of vertices it points to (outgoing edges)

    def addVertex(self, vertex):
        #Add a vertex if it does not already exist
        if vertex in self.adjacency_list:
            return False
        self.adjacency_list[vertex] = []
        return True

    def addEdge(self, from_vertex, to_vertex):
        #Add a directed edge if both vertices exist
        return True

    def removeEdge(self, from_vertex, to_vertex):
        #Remove an existing directed edge
        return True

    def listIncomingAdjacentVertex(self, vertex):
        #Return all vertices pointing into this vertex
        incoming = []
        return incoming

    def listOutgoingAdjacentVertex(self, vertex):
        #Return all vertices pointed to by this vertex
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

    #Display the full details of the course
    def details(self):
        return (f"Course Code   : {self.course_code}\n"
                f"Course Name   : {self.course_name}\n"
                f"Credit Hours  : {self.credit_hours}\n"
                f"Level         : {self.level}")

    def profile(self):
        #Display course information based on Core / Elective level
        return f"Course Name : {self.course_name}\n(Details hidden for elective courses)"

#3. Helper Functions
#Find a course using its course code, return None if not found
def find_course(courses, course_code):
    return None

#Ask user for a course code and return the course (None if not found)
def input_course(courses, message):
    course_code = input(message).strip().upper()

#Print a list of courses or a message if empty
def print_course_list(course_list, empty_message):
    print(empty_message)

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

        elif choice == "2":
            #View all details of one course
            course = input_course(courses, "Enter Course Code: ")

        elif choice == "3":
            #Prerequisites = incoming edges
            course = input_course(courses, "Enter Course Code: ")

        elif choice == "4":
            #Unlocked courses = outgoing edges
            course = input_course(courses, "Enter Course Code: ")

        elif choice == "5":
            #Profile depends on Core / Elective
            course = input_course(courses, "Enter Course Code: ")

        elif choice == "6":
            #Add a new course (new vertex)
            course_code = input("Enter new course code: ").strip().upper()

        elif choice == "7":
            #Course X adds course Y as prerequisite: new edge Y-> X
            course_x = input_course(courses, "Enter course code: ")

        elif choice == "8":
            #Course X removes course Y as prerequisite: remove edge Y -> X
            course_x = input_course(courses, "Enter course code: ")

        elif choice == "9":
            #Exit program
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()






















