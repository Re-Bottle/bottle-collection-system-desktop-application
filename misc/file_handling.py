def save_to_file(data: str, filename: str) -> bool:
    try:
        with open(filename, "w") as file:
            file.write(data)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
