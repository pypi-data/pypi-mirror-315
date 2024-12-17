try:
    from cipher import Enigma
    import utilitis
except:
    from . cipher import Enigma
    from . import utilitis


class CipherReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as file:
            self.file = file.read()


    def cipher_file(self, key_code: str=None, rewrite: bool = False, key_lenght: int = 32, save: bool = True) -> tuple[str, str]:
        enigma = Enigma()

        if key_code == None:
            key = enigma.generate_key(key_length=key_lenght)
        else:
            key = key_code

        cipher_text = enigma.cipher_text(key=key, text=self.file)
        
        path = self.__get_path(self.file_path, "cipher")

        if save:
            with open(path, "w", encoding="utf-8") as file:
                file.write(cipher_text)
        
        return key, cipher_text
    
    def anti_cipher_file(self, key: str, save: bool = True) -> str:
        enigma = Enigma()
        anti_cipher_text = enigma.anti_cipher_text(key=key, text=self.file)
        path = self.__get_path(path=self.file_path, addon_name="test", count_endpoints=2)

        if save:
            with open(path, "w", encoding="utf-8") as file:
                file.write(anti_cipher_text)

        return anti_cipher_text

    def __get_path(self, path: str, addon_name, count_endpoints: int = 1) -> str:
        splitter = path.split(".")
        current_path = splitter[:-count_endpoints]
        print(current_path, splitter[len(splitter) - 1])
        output_path = f"{utilitis.get_text_from_array(arr=current_path)}.{addon_name}.{splitter[len(splitter) - 1]}"

        return output_path
    
