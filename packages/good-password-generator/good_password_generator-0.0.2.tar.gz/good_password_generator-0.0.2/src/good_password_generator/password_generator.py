import random
import string

def generate_strong_password(length=12):
    if length < 7:
        raise ValueError("Password length must be at least 7 to include required characters.")
    
    #we have to first make sure the password generated must have atleast seven characters

    # Character pools
    numbers = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase

    # Ensure the password contains at least one of each required character type
    password = [
        random.choice(numbers),
        random.choice(symbols),
        random.choice(uppercase),
        random.choice(lowercase)
    ]

    # Fill the remaining length with random characters from all pools
    all_characters = numbers + symbols + uppercase + lowercase
    password += random.choices(all_characters, k=length - 4)

    # Shuffle the password list to randomize character order
    random.shuffle(password)

    return ''.join(password)

# Example usage
# newPassword = generate_strong_password()
# print('the strong password is' + newPassword)


