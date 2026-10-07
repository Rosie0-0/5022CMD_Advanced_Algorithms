#Question 1: Hashing

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
        #self.table = [None] * size
        self.table: list[Medicine | None] = [None] * size

    #Hash Function
    def hash_function(self, product_id):
        hash_value = sum(ord(char) for char in product_id) #Total integer Unicode code point
        return hash_value % self.size #Get index

    #Find slot (done)
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

    #Insert Function (done)
    def insert(self, medicine):
        status, index = self.find_slot(medicine.product_id)
        #Check index status
        if status == "full":
            return "Table full"
        if status == "duplicate":
            return "Duplicate product"
        #Product are stored
        self.table[index] = medicine
        return index

    #Search Function
    #def search(self, product_id):

#Performance Testing

def main():
    #Create hash table with size 23
    hash_table = HashTable(23)

    #User Input
    medicine = Medicine("1042", "Paracetamol 500mg", 5.90, 120)
    #Display the Pharmacy menu
    print("==== Pharmacy Inventory System ====")
    print("Product Found!")
    print(medicine)


if __name__ == "__main__":
    main()