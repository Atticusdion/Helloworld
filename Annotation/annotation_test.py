path = 'Annotation/coding_qual_input.txt'

def decode(message_file):

    step = 1
    position = 1
    code = ""

    with open(message_file, 'r') as file:
        
        lines = file.readlines()

        while position <= len(lines):
            
            for line in lines:   
                words = line.strip().split()

                if words and int(words[0]) == position:
                    code = code + words[1] + " "

            step += 1
            position += step

    code = code.strip()
    return code

print(f"The decoded text is '{decode(path)}'")