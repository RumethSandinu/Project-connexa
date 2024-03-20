class ItemManager:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, item_name):
        self.items[item_id] = item_name
        print(f"Item {item_id}: {item_name} added successfully.")

    def delete_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
            print(f"Item {item_id} deleted successfully.")
        else:
            print(f"Item {item_id} not found.")

    def update_item(self, item_id, new_name):
        if item_id in self.items:
            self.items[item_id] = new_name
            print(f"Item {item_id} updated successfully.")
        else:
            print(f"Item {item_id} not found.")

    def display_items(self):
        print("Current Items:")
        for item_id, item_name in self.items.items():
            print(f"{item_id}: {item_name}")

# Function to display menu
def display_menu():
    print("\nMenu:")
    print("1. Add Item")
    print("2. Update Item")
    print("3. Delete Item")
    print("4. Display Items")
    print("0. Exit")

# Example usage with menu:
item_manager = ItemManager()

while True:
    display_menu()
    choice = input("Enter your choice (0-4): ")

    if choice == "1":
        item_id = int(input("Enter Item ID: "))
        item_name = input("Enter Item Name: ")
        item_manager.add_item(item_id, item_name)
    elif choice == "2":
        item_id = int(input("Enter Item ID to update: "))
        new_name = input("Enter New Item Name: ")
        item_manager.update_item(item_id, new_name)
    elif choice == "3":
        item_id = int(input("Enter Item ID to delete: "))
        item_manager.delete_item(item_id)
    elif choice == "4":
        item_manager.display_items()
    elif choice == "0":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter a number between 0 and 4.")
