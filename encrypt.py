#Take in a string and hash it and return it as a string
def hash(text):
    result = ""
    x = sum([ord(i) for i in text])//len(text)
    for i in range(len(text)):
        result += chr(ord(text[i])+x)
    return result