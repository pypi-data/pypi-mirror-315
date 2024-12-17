import random

try:
    import config
    import utilitis
except:
    from . import config
    from . import utilitis



class Enigma:
    def __init__(self):
        pass

    def cipher_text(self, key: str, text: str) -> str:
        offset = key[:3]
        keyOf = key[3:]
        cipher_text = list(text)

        for char in range(len(cipher_text)):
            cipher_text[char] = chr(ord(cipher_text[char]) + int(offset))


        for char in range(len(cipher_text)):
            key_code = -1
            try: 
                key_code = int(char % len(keyOf)) * -1

            except: 
                key_code = ord(char % len(keyOf))

            cipher_text[char] = chr(ord(cipher_text[char]) + key_code)

        

        output_text = utilitis.get_text_from_array(cipher_text)
        
        return output_text
    
    def anti_cipher_text(self, key: str, text: str):
        offset = key[:2]
        keyOf = key[2:]
        cipher_text = list(text)


        for char in range(len(cipher_text)):
            key_code = -1
            try: 
                key_code = int(char % len(keyOf)) * -1

            except: 
                key_code = ord(char % len(keyOf))

            cipher_text[char] = chr(ord(cipher_text[char]) - key_code)

        for char in range(len(cipher_text)):
            cipher_text[char] = chr(ord(cipher_text[char]) - int(offset))

        output_text = utilitis.get_text_from_array(cipher_text)
        
        return output_text
    
    def generate_key(self, key_length):
        key = ""
        key += str(random.randint(200, 300))
        for char in range(key_length):
            key += config.SYMBWOL[random.randint(0, len(config.SYMBWOL) - 1)]
            key += str(random.randint(0, 9))

        return key


    

