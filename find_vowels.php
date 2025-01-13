def reverse_string(input_string):
    # Initialize an empty string for the reversed version
    reversed_str = ""
    
    # Iterate through the string in reverse order
    for char in input_string:
        reversed_str = char + reversed_str  # Prepend each character
    
    return reversed_str

# Input from the user
user_input = input("Enter a string: ")
reversed_string = reverse_string(user_input)

# Display the result
print("Reversed string:", reversed_string)
