import os
import string

class SearchEngine:
    def __init__(self):
        self.inverted_index = {}

    # Abro un archivo, le quito la puntuación y lo separo. Recibo la ruta del archivo y devuelvo una lista de palabras limpias.
    def get_words_from_file(self, filepath):
        words = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.translate(str.maketrans('', '', string.punctuation)).lower()
                    words.extend(line.split())
        except Exception as e:
            pass
        return words

    # Leo los archivos y armo el índice invertido. Recibo una lista de rutas de archivos. Guardo los datos en mi diccionario.
    def build_index(self, files_list):
        for filepath in files_list:
            words = self.get_words_from_file(filepath)
            for word in words:
                if word not in self.inverted_index:
                    self.inverted_index[word] = []
                
                if filepath not in self.inverted_index[word]:
                    self.inverted_index[word].append(filepath)

    # Recibo el texto a buscar y devuelvo una lista con las rutas de los archivos que tienen las palabras.
    def search(self, query):
        query_words = query.lower().split()
        
        clean_query = []
        for p in query_words:
            if p != "":
                clean_query.append(p)
                
        if len(clean_query) == 0:
            return []
            
        first_word = clean_query[0]
        if first_word not in self.inverted_index:
            return []
            
        results = self.inverted_index[first_word][:]
        
        for word in clean_query[1:]:
            if word in self.inverted_index:
                new_results = []
                for filepath in results:
                    if filepath in self.inverted_index[word]:
                        new_results.append(filepath)
                results = new_results
            else:
                return []
                
        return results

    # Extraigo las frases exactas donde aparecen las palabras, recibo la ruta del archivo y la consulta, devuelvo una lista de frases.
    def get_snippets(self, filepath, query):
        query_words = query.lower().split()
        clean_query = []
        for p in query_words:
            if p != "":
                clean_query.append(p)
                
        snippets = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            content = content.replace("?", ".")
            content = content.replace("!", ".")
            content = content.replace("\n", " ")
            
            sentences = content.split(".")
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                    
                match = True
                for word in clean_query:
                    if word not in sentence_lower:
                        match = False
                        break
                
                if match and sentence.strip() != "":
                    snippets.append(sentence.strip() + "...")
                    
        except Exception:
            pass
            
        return snippets

# Muestro un menú para elegir qué archivos vamos a leer, devuelvo una lista con las rutas exactas de los archivos.
def get_files_to_index():
    while True:
        print("\n--- SEARCH ENGINE CONFIGURATION ---")
        print("1. Index a specific directory")
        print("2. Index a specific file")
        print("3. Default (Index current directory and its immediate subfolders)")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            dir_path = input("Enter folder path (e.g., bbcnews): ").strip()
            if os.path.isdir(dir_path):
                files = []
                for f in os.listdir(dir_path):
                    if f.endswith(".txt"):
                        files.append(os.path.join(dir_path, f))
                if len(files) > 0:
                    return files
                else:
                    print("Error: No .txt files found in that directory.")
            else:
                print("Error: Directory does not exist.")
                
        elif choice == "2":
            file_path = input("Enter file path (e.g., document.txt): ").strip()
            if os.path.isfile(file_path):
                return [file_path]
            else:
                print("Error: File does not exist.")
                
        elif choice == "3":
            dir_path = "."
            files = []
            
            for item in os.listdir(dir_path):
                full_path = os.path.join(dir_path, item)
                
                if os.path.isfile(full_path) and full_path.endswith(".txt"):
                    files.append(full_path)
                    
                elif os.path.isdir(full_path):
                    try:
                        for sub_item in os.listdir(full_path):
                            if sub_item.endswith(".txt"):
                                files.append(os.path.join(full_path, sub_item))
                    except PermissionError:
                        pass
                        
            if len(files) > 0:
                return files
            else:
                print("Error: No .txt files found in the current directory or its subfolders.")
                
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

def main():
    print("Initializing Systems...")
    
    target_files = get_files_to_index()
    print("\nInitiating indexing sequence for " + str(len(target_files)) + " file(s)...")
    
    engine = SearchEngine()
    engine.build_index(target_files)
    
    print("Indexing completed. " + str(len(engine.inverted_index)) + " unique terms mapped to memory.")
    
    while True:
        query = input("\nQuery (empty query to stop): ").strip()
        
        if query == "":
            print("System shutting down. Goodbye.")
            break
            
        results = engine.search(query)
        
        print("\nResults for query '" + query + "':")
        if len(results) == 0:
            print("No results match that query.")
        else:
            results.sort()
            for i in range(len(results)):
                filepath = results[i]
                print(str(i + 1) + ". File: " + filepath)
                
                snippets = engine.get_snippets(filepath, query)
                for snippet in snippets:
                    print("   \"" + snippet + "\"")
                print("")

if __name__ == '__main__':
    main()