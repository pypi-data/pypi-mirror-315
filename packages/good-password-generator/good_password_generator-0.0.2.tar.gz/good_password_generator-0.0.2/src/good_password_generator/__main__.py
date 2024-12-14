from .password_generator import generate_strong_password

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate a strong password.")
    parser.add_argument('--length', type=int, default=12, help="Length of the password (default: 12)")
    parser.add_argument('--exclude-symbols', action='store_true', help="Exclude symbols from the password")
    args = parser.parse_args()

    password = generate_strong_password(args.length, include_symbols=not args.exclude_symbols)
    print(f"Generated Password: {password}")

if __name__ == "__main__":
    main()
