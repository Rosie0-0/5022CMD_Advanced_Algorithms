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
        return f'ID: {self.product_id:<6} | Name: {self.product_name:<20} | Price: RM{self.price:>6.2f} | Stock: {self.quantity:>4}'

class HashTable:
    #Constructor
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    #Hash Function (Polynomial hash)
    def hash_function(self, product_id):
        hash_value = 0
        for char in product_id:
            hash_value = hash_value * 131 + ord(char) #Multiply before adding, so character order matters
        return hash_value % self.size                 #Get index

    #Find slot: locate matching ID, empty slot or detect full table
    def find_slot(self, product_id):
        index = self.hash_function(product_id)
        start = index

        while self.table[index] is not None:
            if self.table[index].product_id == product_id:
                return "found", index       #Case 1: if ID found in table
            index = (index + 1) % self.size
            if index == start:
                return "full", None         #Case 2: Table is full & ID not found
        return "empty", index               #Case 3: Empty slot

    #Insert Function
    def insert(self, medicine):
        status, index = self.find_slot(medicine.product_id)
        #Check index status
        if status == "full":
            return "Table full"
        if status == "found":
            return "Duplicate product"
        #Product is stored
        self.table[index] = medicine
        return index

    #Search Function
    def search(self, product_id):
        #Get the index of the specific product_id
        status, index = self.find_slot(product_id)
        if status == "found":
            return self.table[index]    #product_id found
        return None                     #Not found

    #Edit Function
    def edit(self, product_id, product_name, price, quantity):
        medicine = self.search(product_id)
        if medicine is None:
            return None                 #Not found
        #Update details (product_id is the key, so it stays the same and the slot does not change)
        medicine.product_name = product_name
        medicine.price = price
        medicine.quantity = quantity
        return medicine

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

#Compare Search: run hash table search and linear search, return results and times (ns)
def compare_search(hash_table, medicine_array, product_id):
    #1. Hash Table Search
    start_time = time.perf_counter_ns()  #Performance_Counter(nanoseconds)
    hash_result = hash_table.search(product_id)
    end_time = time.perf_counter_ns()
    hash_time = end_time - start_time

    #2. Array Search
    start_time = time.perf_counter_ns()
    array_result = linear_search(medicine_array, product_id)
    end_time = time.perf_counter_ns()
    array_time = end_time - start_time

    return hash_result, array_result, hash_time, array_time

#Performance Testing
def performance_testing():
    print("\n==== Performance Test: Hash Table vs Array ====")
    for size in [100, 1000, 10000]:
        #Create a new hash table (twice the records) and array for testing
        test_table = HashTable(size * 2)
        test_array = []

        #Insert the same records into both
        for i in range(size):
            medicine = Medicine(str(i), "Medicine " + str(i), 1.00, 10)
            test_table.insert(medicine)
            test_array.append(medicine)

        #Search for the last record (worst case for the array)
        product_id = str(size - 1)

        hash_result, array_result, hash_time, array_time = compare_search(test_table, test_array, product_id)

        print(f"\nNumber of records: {size}")
        print(f"Hash Table search time  : {hash_time} ns")
        print(f"Array search time       : {array_time} ns")

def main():
    #Create hash table with size 23
    hash_table = HashTable(23)

    #Create One-dimensional array
    medicine_array = []

    #Create predefined medicines
    predefined_medicines = [
        Medicine("1041", "Paracetamol 500mg", 4.50, 150),
        Medicine("1042", "Amoxicillin 250mg", 12.80, 80),
        Medicine("1043", "Ibuprofen 400mg", 6.20, 200),
        Medicine("1044", "Cetirizine 10mg", 8.00, 120),
        Medicine("1045", "Metformin 500mg", 15.00, 90),
        Medicine("1046", "Omeprazole 20mg", 11.50, 110),
        Medicine("1047", "Loratadine 10mg", 7.50, 95),
        Medicine("1048", "Atorvastatin 20mg", 22.00, 60),
        Medicine("1049", "Aspirin 81mg", 5.00, 300),
        Medicine("1050", "Salbutamol Inhaler", 18.50, 45)
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
        print("3. Edit Product")
        print("4. Performance Test")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            #Display Current Product
            hash_table.display()
            #Get user input
            product_id = input("Enter product ID: ").strip() #Remove accidental spaces
            if not product_id.isdigit(): #Check product ID is not empty and contains digits
                print("Product ID must contain numbers only.\n")
                continue
            if hash_table.search(product_id) is not None: #Check product ID availability
                print("Duplicate product.\n")
                continue

            product_name = input("Enter product name: ").strip()
            if product_name == "":  #Check product name is not empty
                print("Product name cannot be empty.\n")
                continue

            try:
                price = float(input("Enter price: "))
                quantity = int(input("Enter stock quantity: "))
            except ValueError:
                print("Invalid price or quantity. Please enter numbers only.\n")
                continue #Return to the menu

            if price < 0 or quantity < 0: #Check price and quantity are not negative
                print("Price and quantity cannot be negative.\n")
                continue

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

            hash_result, array_result, hash_time, array_time = compare_search(hash_table, medicine_array, product_id)

            #Show result + both times
            if hash_result is not None and array_result is not None:
                print("Product Found!")
                print(hash_result)
            elif hash_result is None and array_result is None:
                print("Product not found")
            else:
                print("Hash table and array are out of sync")

            print(f"Search completed in {hash_time} ns (Hash Table)")
            print(f"Search completed in {array_time} ns (Array - same record)")

        elif choice == "3":
            #Get product to edit
            product_id = input("Enter product ID to edit: ").strip()
            medicine = hash_table.search(product_id)
            if medicine is None:
                print("Product not found.\n")
                continue
            print(medicine)

            #Get new details (press Enter to keep the current value)
            print("Press Enter to keep the current value.")
            new_name = input(f"Enter new product name [{medicine.product_name}]: ").strip()
            new_price = input(f"Enter new price [{medicine.price:.2f}]: ").strip()
            new_quantity = input(f"Enter new stock quantity [{medicine.quantity}]: ").strip()

            #Start with current values, replace only those the user entered
            product_name = medicine.product_name
            price = medicine.price
            quantity = medicine.quantity
            if new_name != "":
                product_name = new_name
            try:
                if new_price != "":
                    price = float(new_price)
                if new_quantity != "":
                    quantity = int(new_quantity)
            except ValueError:
                print("Invalid price or quantity. Please enter numbers only.\n")
                continue #Return to the menu

            if price < 0 or quantity < 0: #Check price and quantity are not negative
                print("Price and quantity cannot be negative.\n")
                continue

            #Array holds the same Medicine object, so it is updated too
            hash_table.edit(product_id, product_name, price, quantity)
            print("Product updated successfully!")
            print(hash_table.search(product_id))

        elif choice == "4":
            #Performance testing: compare hash table and array search on large datasets
            performance_testing()

        elif choice == "5":
            #Exit program
            print("Exiting Inventory System. Goodbye!")
            break
        else:
            print("Enter a valid choice.\n")

if __name__ == "__main__":
    main()