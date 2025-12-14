#Decode


#check if file exists and its an bmp
while True:#always true
    print("-----------------------------------------------------------------------------------")
    file_name = input("Enter BMP file name: ").strip()

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




