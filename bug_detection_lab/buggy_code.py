def greet(name):
	print(f"Hello, {name}")


def add_numbers():
	number1 = int(input("Enter a number: "))
	number2 = int(input("Enter another number: "))
	total = number1 + number2
	print(f"The sum of {number1} and {number2} is {total}")


def is_eligible_for_discount(age):
	"""Return True if the customer gets the senior discount (age 60 or older)."""
	return age >= 60


if __name__ == "__main__":
	greet("Asha")
	add_numbers()
	print(is_eligible_for_discount(60))