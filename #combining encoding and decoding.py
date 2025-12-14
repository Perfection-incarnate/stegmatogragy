#combining encoding and decoding 
choose = 28
while choose != 1 and choose != 2:
    print("--------------------------------")
    print("Enter what you wish to do")
    print("1: hiding a secret message into an image")
    print("2: extract a secret message from an image")
    choose = int(input("input the number of your choice :"))
    print()
    print()
    print("-------------------------------------------------")
    if choose != 1 and choose != 2: print("You have entered a noneexistant choice. Try again")
    print("-------------------------------------------------")
    print()


#encoding
if choose == 1: 
    print("-------------------------------------------------")
    print("You chose hiding a secret message into an image")
    print("-------------------------------------------------")
    print()
    print()

    #encoder code
    #Steganography

    while True:#always true
        print("-----------------------------------------------------------------------------------")
        print("Enter the bmp image you wish to hide the secret text in. The image must a bmp image")
        file_name = input("Enter BMP file name: ").strip()
        file_name += ".bmp"

        #check if file is bmp by reading extension
        if not file_name.lower().endswith(".bmp"):
            print("-----------------------------------")
            print("Error: file must be an .bmp image")
            print("-----------------------------------")
            continue #go back to the start

        #if it exists
        try:
            f = open(file_name, "rb")
            f.close()
            break 
        except:
            print("----------------------------------------------------------------------------------")
            print("You have entered a none existant file or the file is not actually a Bmp. try again")
            print("----------------------------------------------------------------------------------")

    print("You have selected:", file_name)



    #file path
    file_path = file_name

    #open the file
    f = open(file_path, 'rb')
    file_content = f.read()

    #Get width and hight from file header
    image_width = int.from_bytes(file_content[18:22], byteorder='little')
    image_height = int.from_bytes(file_content[22:26], byteorder='little')

    #byte offset
    bytes_offset = int.from_bytes(file_content[10 : 14], byteorder='little')

    #making it starting from top left
    row_size = ((image_width * 3 + 3) // 4) * 4
    top_row_offset = bytes_offset + (image_height - 1) * row_size


    #how many changeable varabiles in image
    size_num = (image_height * image_width)
    #checking how many characters can be entered
    character_max = (size_num // 8) - 1



    print(f"max character size: {character_max}")
        
    #take input and convert it into binary
    binary_list = []
    tem = []
    def string_to_binary(text):
        for char in text:
            if char == "’" or char == "‘": char = "'" #fixing bug
            tem.extend((format(ord(char), '08b')))
        
        #add eight zeros at the end
        tem.extend("00000000")
        for i in tem: binary_list.append(int(i))
    
        return binary_list
    
    #take input
    choose_input = 0
    while choose_input != 1 and choose_input != 2:
        print("--------------------------------")
        print("Enter your text input method. note: both inputs only support the english language")
        print("1: inputing text manually")
        print("2: inputing a text file that contains the text")
        choose_input = int(input("input the number of your choice :"))
        print()
        print()
        print("-------------------------------------------------")
        if choose_input != 1 and choose_input != 2: print("You have entered a noneexistant choice. Try again")
        print("-------------------------------------------------")
        print()
        print()


    #entering a text file
    if choose_input == 2:
        #take text file
        while True:
            #take input
            print("You have chosen to input a text file")
            text_file = input("Enter the name of the text file: ")
            text_file += ".txt"
            try:
                file = open(text_file, "r", encoding="utf-8") #encoding so characters that arent in ascii dont break code
                text_string = file.read()
                while len(text_string) > character_max:
                    print(f"Text file is too large. Your image can only take {character_max}")
                    text_file = input("Enter the name of the text file: ")
                    text_file += ".txt"
                    file = open(text_file, "r")
                    text_string = file.read()
                file.close()
                #put it in string input
                string_input = text_string
                break 
            except FileNotFoundError:
                print("Error: File does not exist. Try again")

    #entering text manually         
    if choose_input == 1:
        input_string = "reneter ur input"
        print("You have chosen to enter the text manually")
        input_string = input(str(f"Input your secret sentence. The inputed image can only take {character_max} characters  :"))
        while len(input_string) > character_max:
            if len(input_string) > character_max:
                print(f"input is too large. your image can only take {character_max} characters  :")
                input_string = input(str(f"Input ur secret sentence. The inputed image can only take {character_max} characters  :"))
                #put it in string input
        string_input = input_string


    #take string and run it through converter function
    binary_output = string_to_binary(string_input)




    #changing image 
    file_content = list(file_content)
    counter = 0
    do_nothing = 0
    secret_message_binary = binary_list

    for row in range(image_height):
        row_offset = bytes_offset + (image_height - 1 - row) * row_size
        for column in range(image_width * 3):  #*3 for rgb in pixel
            #making sure counter doesnt go over for loop
            if counter >= len(secret_message_binary):
                break  

            byte = secret_message_binary[counter]
            byte_index = row_offset + column

            #checking if pixel values odd or even
            if file_content[byte_index] % 2 == 0:
                #if its even? check if i is also even
                if byte == 0:
                    #do nothing
                    do_nothing = 0
                #if its 1 then make it odd
                elif byte == 1:
                #make it odd
                # make sure its not 0 before minusing
                    if file_content[byte_index] == 0: file_content[byte_index] += 1
                    else: file_content[byte_index] -= 1

            #if its odd      
            elif file_content[byte_index] % 2 == 1:
                #if its odd? check if i is also odd
                if byte == 1:
                    #do nothing
                    do_nothing = 0
                #if its 0 then make it even
                elif byte == 0:
                    #make it even
                    #make sure its not 0 before minusing
                    if file_content[byte_index] == 0: file_content[byte_index] += 1
                    else: file_content[byte_index] -= 1
                        

            counter += 1

        if counter >= len(secret_message_binary):
            break

    print()
    print()
    print("----------------------------------------")
    Holder = input("Name the exported file. note: if a file already has this name then it will get overwritten: ")
    Holder += ".bmp"
    print (Holder)
    output_path = Holder
    f = open(output_path , "wb")
    f.write(bytes(file_content))

    print(f"File {output_path} is succesfully created")





#decoding
if choose == 2:
    print("----------------------------------------------------")
    print("You choose extracting a secret message from an image") 
    print("----------------------------------------------------")


    #Decode


    #check if file exists and its an bmp
    while True:#always true
        print("-----------------------------------------------------------------------------------")
        file_name = input("Enter BMP file name: ").strip()
        file_name += '.bmp'

        #check if file is bmp by reading extension
        if not file_name.lower().endswith(".bmp"):
            print("-----------------------------------")
            print("Error: file must be an .bmp image")
            print("-----------------------------------")
            continue #go back to the start

        #if it exists
        try:
            f = open(file_name, "rb")
            f.close()
            break 
        except:
            print("----------------------------------------------------------------------------------")
            print("You have entered a none existant file or the file is not actually a Bmp. try again")
            print("----------------------------------------------------------------------------------")

    print("You have selected:", file_name)

    #file path
    file_path = file_name

    #open the file
    f = open(file_path, 'rb')
    file_content = f.read()







    #Get width and hight from file header
    image_width = int.from_bytes(file_content[18:22], byteorder='little')
    image_height = int.from_bytes(file_content[22:26], byteorder='little')

    #byte offset
    bytes_offset = int.from_bytes(file_content[10 : 14], byteorder='little')

    #making it starting from top left
    row_size = ((image_width * 3 + 3) // 4) * 4
    top_row_offset = bytes_offset + (image_height - 1) * row_size


    #how many changeable varabiles in image
    size_num = (image_height * image_width)*3
    #checking how many characters can be entered
    character_max = int(size_num/8)

        


    #changing image 
    file_content = bytearray(file_content)
    secret_bits = []
    secret_message = ''
    counter = 0
    decoded_text = ''
    for row in range(image_height):
        row_offset = bytes_offset + (image_height - 1 - row) * row_size
        for column in range(image_width * 3):  #*3 for rgb in pixel
            byte_index = row_offset + column
            i = file_content[byte_index]

            #checking if pixel values odd or even
            if i % 2 == 0:
                #if its even then the value is 0
                secret_bits.append("0")    
            #if its odd
            else:
                #if its odd then the value is 1
                secret_bits.append("1")   

            counter += 1
            #fixing breakage
            if counter != 0:
                if counter % 8 == 0:
                    current_bits = "".join(secret_bits[counter - 8:counter])
                    #check if loop should end
                    if current_bits == "00000000":
                        print(decoded_text)
                        exit()
                        
                    #decoding
                    decoded_text += chr(int(current_bits, 2))

            
    counter = 0




