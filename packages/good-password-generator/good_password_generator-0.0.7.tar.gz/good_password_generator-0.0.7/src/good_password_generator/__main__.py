
import argparse
from good_password_generator import generate_strong_password

def main():
    parser = argparse.ArgumentParser(description="Generate a strong password.")
    parser.add_argument('--length', type=int, default=12, help="Length of the password.")
    parser.add_argument('--exclude-symbols', action='store_true', help="Exclude symbols from the password.")
    args = parser.parse_args()

    try:
        password = generate_strong_password(args.length, include_symbols=not args.exclude_symbols)
        print(f"Generated Password: {password}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
