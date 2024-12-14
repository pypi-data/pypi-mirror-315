import argparse
import os
import json


def json2py(json_file_path, output_directory):
    """
    Tworzy pliki na podstawie zawartości pliku JSON.

    Args:
        json_file_path (str): Ścieżka do pliku JSON zawierającego nazwy i zawartości plików.
        output_directory (str): Ścieżka do katalogu, w którym mają być zapisane pliki.
    """
    # Upewnij się, że katalog wyjściowy istnieje
    os.makedirs(output_directory, exist_ok=True)

    # Wczytaj zawartość pliku JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        file_data = json.load(json_file)

    # Iteracja po elementach JSON i zapisanie plików
    for filename, content in file_data.items():
        file_path = os.path.join(output_directory, filename)
        
        # Utwórz katalogi, jeśli to konieczne
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Zapisz zawartość pliku
        with open(file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)

        print(f"Plik zapisany: {file_path}")


def py2json(directory, output_file):
    py_files_content = {}
    try:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in files:
                if filename.endswith('.py'):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        relative_path = os.path.relpath(file_path, directory)
                        py_files_content[relative_path] = file.read()

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(py_files_content, json_file, indent=4, ensure_ascii=False)

    except FileNotFoundError as e:
        print(f"Błąd: {e}")
    except PermissionError:
        print("Błąd: Brak uprawnień do odczytu/zapisu plików.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")


def main_py2json():
    parser = argparse.ArgumentParser(description="Tworzenie pliku JSON z zawartością plików .py w katalogu i podkatalogach.")
    parser.add_argument("directory", help="Ścieżka do katalogu z plikami .py")
    parser.add_argument("output", help="Ścieżka do pliku wynikowego JSON")
    args = parser.parse_args()
    py2json(args.directory, args.output)

def main_json2py():
    parser = argparse.ArgumentParser(description="Tworzenie skrytów py na podstawie pliku json z kodami")
    parser.add_argument("json_file", help="Ścieżka pliku JSON")
    parser.add_argument("output_directory", help="Ścieżka do folderu z projektem")
    args = parser.parse_args()
    json2py(args.json_file, args.output_directory)


if __name__ == "__main__":
    main_py2json()
