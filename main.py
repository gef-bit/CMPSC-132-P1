from abc import ABC, abstractmethod

class Product:
    def __init__(self, product_id, name, price, quantity=1):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
    def update_price(self, new_price):
        self.price = new_price
    def get_product_info(self):
        return {'product_id':self.product_id,'name':self.name,'price':self.price,'quantity':self.quantity}
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity, file_size, product_link):
        super().__init__(product_id, name, price, quantity)
        self.file_size = file_size
        self.product_link = product_link
    def get_product_info(self):
        return {'product_id':self.product_id,'name':self.name,'price':self.price,'quantity':self.quantity,'file_size':self.file_size,'product_link':self.product_link}
class PhysicalProduct(Product):
    """
    Represents a physical product in the inventory system.

    This class extends the base Product class to include additional attributes and
    functionality specific to physical products, such as weight, dimensions, and
    shipping costs. It is designed to handle and represent products that are tangible
    and require shipping.

    :ivar weight: The weight of the physical product in kilograms.
    :type weight: float
    :ivar dimensions: The dimensions of the physical product as a string (e.g.,
        "10x20x30 cm").
    :type dimensions: str
    :ivar shipping_cost: The cost of shipping the physical product.
    :type shipping_cost: float
    """
    def __init__(self, product_id, name, price, quantity, weight, dimensions, shipping_cost):
        super().__init__(product_id,name,price,quantity)
        self.weight = weight
        self.dimensions = dimensions
        self.shipping_cost = shipping_cost
    def get_product_info(self):
        return {'product_id':self.product_id,'name':self.name,'price':self.price,'quantity':self.quantity,'weight':self.weight,'dimensions':self.dimensions,'shipping_cost':self.shipping_cost}


class Cart:
    def __init__(self):
        self._cart_items = []

    def add_product(self, product):
        """Add a product to the cart."""
        self._cart_items.append(product)

    def remove_product(self, product_id):
        """Remove a product from the cart by its ID."""
        item = self._find_item_by_id(product_id)
        if item:
            self._cart_items.remove(item)

    def view_cart(self):
        """
        Provide a summary of items in the cart.
        :return: A list of dictionaries, where each dictionary represents a cart item's details.
        """
        def format_item(item):
            """Convert a cart item into a dictionary."""
            return {"product_id": item.product_id,"name": item.name,"price": item.price,"quantity": item.quantity}
        return [format_item(item) for item in self._cart_items]

    def calculate_total(self, discounts=None):
        """
        Calculate the total cost of the cart.
        :param discounts: List of discount objects to be applied. Discounts may target specific products or the entire total.
        :return: Final total price after discounts.
        """
        base_total = sum(
            item.price * item.quantity + (item.shipping_cost if isinstance(item, PhysicalProduct) else 0)
            for item in self._cart_items
        )
        final_total = self._apply_discounts(base_total, discounts)
        return final_total

    def _find_item_by_id(self, product_id):
        """Helper method to find an item in the cart by its ID."""
        return next((item for item in self._cart_items if item.product_id == product_id), None)
    def _apply_discounts(self, base_total, discounts):
        """
        Apply discounts, if any, to the given total.
        :param base_total: The initial total price of the cart.
        :param discounts: List of discount objects.
        :return: Total price after applying discounts.
        """
        if discounts:
            for discount in discounts:
                base_total = discount.apply_discount(base_total, self._cart_items)
        return base_total


class User:
    def __init__(self, user_id, name, cart=None, discounts=None):
        self.user_id = user_id
        self.name = name
        self.cart = cart
        if not self.cart:
            self.cart = Cart()
        self.discounts = discounts
    def add_to_cart(self, product):
        self.cart.add_product(product)
    def remove_from_cart(self, product_id):
        self.cart.remove_product(product_id)
    def checkout(self):
        temp = self.cart.calculate_total(self.discounts)
        self.cart = Cart()
        return temp


class Discount(ABC):
    @abstractmethod
    def apply_discount(self, total_price, cart_items):
        """
        Apply the discount to the given total price or cart items.

        :param total_price: The total price of the cart before applying the discount.
        :param cart_items: List of items in the cart.
        :return: The total price after applying the discount.
        """
        pass
class PercentageDiscount(Discount):
    def __init__(self, percentage):
        self.percentage = percentage
    def apply_discount(self, total_price, cart_items):
        return total_price * (1 - self.percentage / 100)
class FixedAmountDiscount(Discount):
    def __init__(self, fixed_amount):
        self.fixed_amount = fixed_amount

    def apply_discount(self, total_price, cart_items):
        return max(0, total_price - self.fixed_amount)  # Ensure no negative totals.

def test_product_class():
    # Test Product Creation
    product = Product(product_id=1, name="Test Product", price=10.0, quantity=2)
    assert product.product_id == 1, f"Expected product_id 1, got {product.product_id}"
    assert product.name == "Test Product", f"Expected name 'Test Product', got {product.name}"
    assert product.price == 10.0, f"Expected price 10.0, got {product.price}"
    assert product.quantity == 2, f"Expected quantity 2, got {product.quantity}"
    print("Product creation works correctly.")

    # Test update_quantity(new_quantity)
    product.update_quantity(5)
    assert product.quantity == 5, f"Expected quantity 5, got {product.quantity}"
    print("update_quantity works correctly.")

    # Test get_product_info()
    product_info = product.get_product_info()
    expected_info = {"product_id":1,"name":"Test Product","price":10.0,"quantity":5}
    assert product_info == expected_info, f"Expected product info {expected_info}, got {product_info}"
    print("get_product_info works correctly.")
def test_digital_and_physical_product_classes():
    # Test DigitalProduct creation
    digital_product = DigitalProduct(
        product_id=101, name="E-Book", price=12.99, quantity=1, file_size="5MB",
        product_link="www.example.com/download"
    )
    assert digital_product.product_id == 101, f"Expected product_id 101, got {digital_product.product_id}"
    assert digital_product.name == "E-Book", f"Expected name 'E-Book', got {digital_product.name}"
    assert digital_product.price == 12.99, f"Expected price 12.99, got {digital_product.price}"
    assert digital_product.quantity == 1, f"Expected quantity 1, got {digital_product.quantity}"
    assert digital_product.file_size == "5MB", f"Expected file_size '5MB', got {digital_product.file_size}"
    assert digital_product.product_link == "www.example.com/download", f"Expected product_link 'www.example.com/download', got {digital_product.product_link}"
    print("DigitalProduct creation works correctly.")

    # Test DigitalProduct get_product_info()
    digital_product_info = digital_product.get_product_info()
    expected_digital_info = {
        "product_id": 101,
        "name": "E-Book",
        "price": 12.99,
        "quantity": 1,
        "file_size": "5MB",
        "product_link": "www.example.com/download"
    }
    assert digital_product_info == expected_digital_info, f"Expected {expected_digital_info}, got {digital_product_info}"
    print("DigitalProduct.get_product_info works correctly.")

    # Test PhysicalProduct creation
    physical_product = PhysicalProduct(
        product_id=202,
        name="Laptop",
        price=999.99,
        quantity=1,
        weight=2.5,
        dimensions="15x10x1 inches",
        shipping_cost=25.00,
    )
    assert physical_product.product_id == 202, f"Expected product_id 202, got {physical_product.product_id}"
    assert physical_product.name == "Laptop", f"Expected name 'Laptop', got {physical_product.name}"
    assert physical_product.price == 999.99, f"Expected price 999.99, got {physical_product.price}"
    assert physical_product.quantity == 1, f"Expected quantity 1, got {physical_product.quantity}"
    assert physical_product.weight == 2.5, f"Expected weight '2.5kg', got {physical_product.weight}"
    assert physical_product.dimensions == "15x10x1 inches", f"Expected dimensions '15x10x1 inches', got {physical_product.dimensions}"
    assert physical_product.shipping_cost == 25.00, f"Expected shipping_cost 25.00, got {physical_product.shipping_cost}"
    print("PhysicalProduct creation works correctly.")

    # Test PhysicalProduct get_product_info()
    physical_product_info = physical_product.get_product_info()
    expected_physical_info = {
        "product_id": 202,
        "name": "Laptop",
        "price": 999.99,
        "quantity": 1,
        "weight": 2.5,
        "dimensions": "15x10x1 inches",
        "shipping_cost": 25.00,
    }
    assert physical_product_info == expected_physical_info, f"Expected {expected_physical_info}, got {physical_product_info}"
    print("PhysicalProduct.get_product_info works correctly.")
def test_cart_class():
    # Create product instances
    product1 = Product(product_id=1, name="Book", price=10.0, quantity=2)
    product2 = Product(product_id=2, name="Notebook", price=5.0, quantity=1)
    product3 = Product(product_id=3, name="Pen", price=2.0, quantity=3)

    # Create a cart instance
    cart = Cart()

    # Test add_product(product) method
    cart.add_product(product1)
    cart.add_product(product2)
    assert cart.view_cart() == [
        {"product_id": 1, "name": "Book", "price": 10.0, "quantity": 2},
        {"product_id": 2, "name": "Notebook", "price": 5.0, "quantity": 1},
    ], "add_product failed: Products not added correctly to the cart."
    print("add_product works correctly.")

    # Test remove_product(product_id) method
    cart.remove_product(1)  # Remove product with ID 1
    assert cart.view_cart() == [
        {"product_id": 2, "name": "Notebook", "price": 5.0, "quantity": 1}
    ], "remove_product failed: Product not removed correctly from the cart."
    print("remove_product works correctly.")

    # Add products again for further testing
    cart.add_product(product1)
    cart.add_product(product3)

    # Test view_cart() method
    expected_cart_items = [
        {"product_id": 2, "name": "Notebook", "price": 5.0, "quantity": 1},
        {"product_id": 1, "name": "Book", "price": 10.0, "quantity": 2},
        {"product_id": 3, "name": "Pen", "price": 2.0, "quantity": 3},
    ]
    assert cart.view_cart() == expected_cart_items, "view_cart failed: Incorrect cart items displayed."
    print("view_cart works correctly.")

    # Test calculate_total() method
    total_price = cart.calculate_total()
    expected_total = 10.0 * 2 + 5.0 * 1 + 2.0 * 3  # (Book x2) + (Notebook x1) + (Pen x3)
    assert total_price == expected_total, f"calculate_total failed: Expected {expected_total}, got {total_price}."
    print("calculate_total works correctly.")

    # Verify cart_items is private
    try:
        _ = cart.cart_items  # Attempt to access private attribute directly
        assert False, "cart_items should be private but is accessible directly."
    except AttributeError:
        print("cart_items is private and only accessible through public methods.")
def test_discount_classes():
    # Verify that Discount cannot be instantiated directly
    try:
        discount = Discount()  # Should raise a TypeError
    except TypeError as e:
        print("Confirmed: Discount is abstract and cannot be instantiated directly.")

    # Test PercentageDiscount
    percentage_discount = PercentageDiscount(10)  # 10% discount
    total_price = 100.0
    discounted_price = percentage_discount.apply_discount(total_price, [])
    assert discounted_price == 90.0, f"Expected 90.0, got {discounted_price}"
    print("PercentageDiscount.apply_discount works correctly.")

    # Test FixedAmountDiscount
    fixed_discount = FixedAmountDiscount(15)  # $15 discount
    discounted_price = fixed_discount.apply_discount(total_price, [])
    assert discounted_price == 85.0, f"Expected 85.0, got {discounted_price}"
    print("FixedAmountDiscount.apply_discount works correctly.")

    # Test polymorphism with different discounts
    discounts = [PercentageDiscount(20), FixedAmountDiscount(30)]  # Apply 20% and then $30 off
    final_price = total_price
    for discount in discounts:
        final_price = discount.apply_discount(final_price, [])
    assert final_price == 50.0, f"Expected 50.0, got {final_price}"  # 20% off $100 = $80;$80-$30=$50
    print("Polymorphic discount application works correctly.")
def test_cart_operations():
    product1 = Product(product_id=1, name="Book", price=10.0, quantity=2)
    product2 = Product(product_id=2, name="Notebook", price=5.0, quantity=1)
    product3 = Product(product_id=3, name="Pen", price=2.0, quantity=3)

    discount = PercentageDiscount(percentage=10) # 10% off

    user = User(user_id=1, name="John Doe", discounts=[discount])

    # Test add_to_cart(product)
    user.add_to_cart(product1)
    user.add_to_cart(product2)
    view_cart_output = user.cart.view_cart()
    assert view_cart_output == [
        {"product_id": 1, "name": "Book", "price": 10.0, "quantity": 2},
        {"product_id": 2, "name": "Notebook", "price": 5.0, "quantity": 1}
    ], "add_to_cart failed: Items not added to cart correctly."

    # Test remove_from_cart(product_id)
    user.remove_from_cart(1)  # Remove product with ID 1
    view_cart_output = user.cart.view_cart()
    assert view_cart_output == [
        {"product_id": 2, "name": "Notebook", "price": 5.0, "quantity": 1}
    ], "remove_from_cart failed: Item not removed from cart correctly."

    # Add products again for testing checkout
    user.add_to_cart(product1)
    user.add_to_cart(product3)

    # Test checkout()
    total = user.checkout()  # This should apply discounts and clear the cart

    # Verify total is calculated correctly with the discount applied
    expected_total = ((10.0 * 2) + (5.0 * 1) + (2.0 * 3)) * 0.9  # 10% discount
    assert total == expected_total, f"checkout failed: Expected total {expected_total}, got {total}."

    # Verify cart is cleared after checkout
    assert user.cart.view_cart() == [], "checkout failed: Cart was not cleared."

    print("All tests passed for add_to_cart, remove_from_cart, and checkout methods.")

if __name__ == "__main__":
    # Testing
    test_product_class() # 1: Testing Product class
    test_digital_and_physical_product_classes() # 2: Testing DigitalProduct & Physical Product classes
    test_cart_class() # 3: Testing Cart class
    test_cart_operations() # 4: Testing User class
    test_discount_classes() # 5: Testing Discount and its derived classes


    # Execution of Sample Scenario
    # 2 instances of DigitalProduct and 3 instances of PhysicalProduct
    digital_product1 = DigitalProduct(product_id=1,name="E-Book",price=15.0,quantity=1,file_size="10MB",product_link="ebook.com")
    digital_product2 = DigitalProduct(product_id=2,name="Online Course",price=50.0,quantity=1,file_size="1GB",product_link="course.com")
    physical_product1 = PhysicalProduct(product_id=3,name="Laptop",price=1000.0,quantity=1,weight=2.5,dimensions="15x10x1 inches",shipping_cost=20.0)
    physical_product2 = PhysicalProduct(product_id=4,name="Chair",price=150.0,quantity=1,weight=10.0,dimensions="30x30x40 inches",shipping_cost=50.0)
    physical_product3 = PhysicalProduct(product_id=5,name="Desk",price=250.0,quantity=1,weight=15.0,dimensions="50x30x50 inches",shipping_cost=75.0)

    # Create 2 instances of the User class and add the digital products to the user1's cart and physical products to the user2’s cart
    user1 = User(user_id=1, name="Alice")
    user2 = User(user_id=2, name="Bob")

    user1.add_to_cart(digital_product1)
    user1.add_to_cart(digital_product2)
    user2.add_to_cart(physical_product1)
    user2.add_to_cart(physical_product2)
    user2.add_to_cart(physical_product3)

    # Verify carts
    print("Alice's Cart:", user1.cart.view_cart())
    print("Bob's Cart:", user2.cart.view_cart())

    # Creating discounts
    percentage_discount = PercentageDiscount(percentage=10)  # 10% discount
    fixed_amount_discount = FixedAmountDiscount(fixed_amount=100)  # $100 fixed discount

    # Applying discounts to carts
    print(f"Alice's Total Before Discount: ${user1.cart.calculate_total():,.2f}")
    print(f"Alice's Total After 10% Discount: ${user1.cart.calculate_total(discounts=[percentage_discount]):,.2f}")

    print(f"Bob's Total Before Discount: ${user2.cart.calculate_total():,.2f}")
    print(f"Bob's Total After $100 Discount: ${user2.cart.calculate_total(discounts=[fixed_amount_discount]):,.2f}")




