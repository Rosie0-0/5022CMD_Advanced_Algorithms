#Question 1: Hashing
import time

class Medicine:
    #Constructor
    def __init__(self, product_id, product_name, price, quantity):
        self.product_id = product_id        #str
        self.product_name = product_name    #str
        self.price = price                  #float
        self.quantity = quantity            #int

    #String Representation for selected medicine
    def __str__(self):
        return f'ID: {self.product_id} | Name: {self.product_name} | Price: RM{self.price:.2f} | Stock: {self.quantity}'

class HashTable:
    #Constructor
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    #Hash Function
    def hash_function(self, product_id):
        hash_value = sum(ord(char) for char in product_id)  #Total integer Unicode code point
        return hash_value % self.size                       #Get index

    #Find slot: find existing index through product_id
    def find_slot(self, product_id):
        index = self.hash_function(product_id)
        start = index

        while self.table[index] is not None:
            if self.table[index].product_id == product_id:
                return "duplicate", index   #Case 1: if ID found in table
            index = (index +1) % self.size
            if index == start:
                return "full", None         #Case 2: Table is full & ID not found
        return "empty", index               #Case 3: Empty slot

    #Insert Function
    def insert(self, medicine):
        status, index = self.find_slot(medicine.product_id)
        #Check index status
        if status == "full":
            return "Table full"
        if status == "duplicate":
            return "Duplicate product"
        #Product is stored
        self.table[index] = medicine
        return index

    #Search Function
    def search(self, product_id):
        #Get the index of the specific product_id
        status, index = self.find_slot(product_id)
        if status == "duplicate":
            return self.table[index]    #product_id found
        return None                     #Not found

    #Display Function
    def display(self):
        print("Product List")
        for item in self.table:
            if item is not None:
                print(item)

#Linear Search (array)
def linear_search(medicine_array, product_id):
    for medicine in medicine_array:
        if medicine.product_id == product_id:
            return medicine
    return None #Not found

#Performance Testing
def performance_testing():
    print()

def main():
    #Create hash table with size 23
    hash_table = HashTable(23)

    #Create One-dimensional array
    medicine_array = []

    #Create Predefine medicines
    predefined_medicines = [
        Medicine("1042", "Paracetamol 500mg", 5.90, 120),
        Medicine("1043", "Ibuprofen 200mg", 7.80, 80),
        Medicine("1044", "Lisinopril 10mg", 6.80, 100),
        Medicine("1045", "Vitamin C 500mg", 8.00, 90)
    ]

    #Insert predefined medicines into HashTable & Array
    for medicine in predefined_medicines:
        hash_table.insert(medicine)
        medicine_array.append(medicine)

    #Menu Loop
    while True:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            #Display Current Product
            hash_table.display()
            #Get user input
            product_id = input("Enter product ID: ").strip() #remove accidental spaces
            product_name = input("Enter product name: ").strip()
            try:
                price = float(input("Enter price: "))
                quantity = int(input("Enter stock quantity: "))
            except ValueError:
                print("Invalid price or quantity. Please enter numbers only. \n")
                continue # return to the menu

            medicine = Medicine(product_id, product_name, price, quantity)
            #Insert into hash table, then array if successful
            result = hash_table.insert(medicine) #return index / "Table full" / "Duplicate product"
            if isinstance(result, int): #check the result is the slot number
                medicine_array.append(medicine)
                print(f"Product inserted successfully into slot [{result}]")
            else:
                print(f"{result}\n")

        elif choice == "2":
            #Search user input
            product_id = input("Enter product ID to search: ").strip()

            #1. Hash Table Search
            start_time = time.perf_counter()  # Performance_Counter(Seconds)
            hash_result = hash_table.search(product_id)
            end_time = time.perf_counter()
            hash_time = end_time - start_time

            #2. Array Table Search
            start_time = time.perf_counter()
            array_result = linear_search(medicine_array, product_id)
            end_time = time.perf_counter()
            array_time = end_time - start_time

            #Show result + both times
            if hash_result is not None and array_result is not None:
                print("Product Found!")
                print(hash_result)
            elif hash_result is None and array_result is None:
                print("Product not found")
            else:
                print("Hash table and array are out of sync")

            print(f"Search completed in {hash_time:.6f} seconds (Hash Table)")
            print(f"Search completed in {array_time:.6f} seconds (Array - same record)")

        elif choice == "3":
            #Exit program
            print("Exiting Inventory System. Goodbye!")
            break
        else:
            print("Enter a valid choice.\n")


if __name__ == "__main__":
    main()