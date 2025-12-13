#Decode

#file path
file_path = r'C:\Users\Lenovo\Desktop\python\stegmatogragy\newenvyimage.bmp'

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
file_content = list(file_content)
byte = (file_content[top_row_offset:])
secret_message = ''
counter = 0
for i in byte:
 
    #checking if pixel values odd or even
    if i % 2 == 0:
        #if its even then the value is 0
        secret_message += "0"      
    #if its odd
    elif i % 2 == 1:
        #if its odd then the value is 1
        secret_message += "1"   
        
        
    counter += 1
    
counter = 0


decoded_text = ''
counter = 0
for i in range(0, len(secret_message),8):
    char = secret_message[counter:counter+8]

    if char == "00000000":
        break
    decoded_text += chr(int(char, 2))
    counter += 8

print(decoded_text)


