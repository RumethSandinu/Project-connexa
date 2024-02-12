import re

class ItemValidator:

    # initialise item details
    def __init__(self, name, category, price_kg, stock, description, image):
        self.name = name
        self.category = category
        self.price_kg = price_kg
        self.stock = stock
        self.description = description
        self.image = image

    # validate item name
    def validate_name(self):
        pattern = r'^[a-zA-Z0-9_ ]+$'
        if len(self.name) <= 100:
            return re.match(pattern, self.name) is not None
        return False

    # validate item category
    def validate_category(self):
        pattern = r'^[a-zA-Z0-9_ ]+$'
        if len(self.category) <= 100:
            return re.match(pattern, self.category) is not None
        return False

    # validate item price
    def validate_price_kg(self):
        pattern = r'^\d+$'
        if re.match(pattern, self.price_kg) is not None:
            return self.price_kg > 0
        return False

    # validate item stock
    def validate_stock(self):
        pattern = r'^\d+$'
        if re.match(pattern, self.stock) is not None:
            return self.stock > 0
        return False

    # validate item description
    def validate_description(self):
        pattern = r'^[a-zA-Z0-9_ ]+$'
        if len(self.description) <= 1000:
            return re.match(pattern, self.description) is not None
        return False

    # validate item image
    def validate_image(self):
        image_pattern = r'\.(png|jpe?g|gif|bmp|tiff|webp)$'
        return re.search(image_pattern, self.image, flags=re.IGNORECASE) is not None

    # validate item details
    def validate_item_details(self):
        return (self.validate_name() and self.validate_category() and self.validate_price_kg() and self.validate_stock()
                and self.validate_description() and self.validate_image())

