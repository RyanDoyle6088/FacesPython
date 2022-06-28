'''
In this project, we will be prompting users to enter file names of multiple files,
and then returning values for indices in the files. Each file contains blocks of data, 
which the functions will use to return the desired values. These values are computing the cross
product, distance, face area, face normal, and if the faces are connected to one another.
'''

#Retain these import statements  
import math


def display_options():
    ''' This function displayes the menu of options'''
    
    menu = '''\nPlease choose an option below:
        1- display the information of the first 5 faces
        2- compute face normal
        3- compute face area
        4- check two faces connectivity
        5- use another file
        6- exit
       '''
       
    print(menu)
    
def open_file():
    """This function prompts the user to enter a file name.
        If the file exists and is accessible, it will then open the file.
        If the file is not entered properly or it does not exist, the function
        will return an error message."""
    while True:
        filename = input("Enter a file name: ")
        try:
            fp = open(filename)
            return fp
        except FileNotFoundError:
            print("error")
            #While true loop to make sure that while filename is prompted and inputted,
            #the function will try to open the file unless it returns an error value
            
def check_valid(fp,index,shape):
    """This function checks the validity of the index. The function reads the first line
    and then splits them into vertices or faces. If the shape is a vertex, the index has to be a correct
    value, and if it is a face, the index has to be a correct value. If the index is neither,
    the function returns false."""
    try:
        index= int(index)
    except ValueError:
        return False
    #This tries the index as an int of the user input, and if there is a ValueError,
    #the function returns false and will re-try until it is true.
    fp.seek(0)
    fp.readline()
    line=fp.readline()
    first, second, third= line.split()
    vertices=int(first)
    #This gives a value to vertices
    faces=int(second)
    #This gives a value to faces
    if shape=='vertex':
        return 0<=index<vertices
    elif shape=='face':
        return 0<=index<faces
    else:
        return False
    
    
def read_face_data(fp, index):
    """This function retursn the indices of the 3 vertices. They are returned as integers, in 
    specified areas of the line where data appears. We then strip the spaces at the beginning and end
    of each value. We then return the variables for each value of data."""
    fp.seek(0) # move to the beginning of the file -- necessary for multiple calls to this function
    fp.readline()
    counter = -1
    for line in fp:
        if line[1] == "3":
            counter += 1
            x = int(line[2:7].strip())
            y = int(line[7:12].strip())
            z = int(line[12:17].strip())
        if line[1] == "3" and index == counter:
            return x,y,z
         

def read_vertex_data(fp, index):
    """This function reads the index in range of the user input. We then return the values as floats
    in the correct locations. The function will return the variables for the first, second, and third
    values in each line."""
    fp.seek(0) # move to the beginning of the file -- necessary for multiple calls to this function
#This will be in the form of floats
    fp.readline()
    fp.readline()
    for i in range(index):
        fp.readline()
    line=fp.readline()
    first=float(line[:15])
    second=float(line[15:30])
    third=float(line[30:])#Need to make these variables floats
    return(first, second, third)

    

        
def compute_cross(v1,v2,v3,w1,w2,w3):
    """This function will compute the cross products using 3 variables and the cross product formula.
    It will return the value rounded to 5 decimal places."""
#floats
    cross1=v2*w3-v3*w2
    cross2=v3*w1-v1*w3
    cross3=v1*w2-v2*w1
    return round(cross1, 5),round(cross2, 5), round(cross3, 5)#returns all 3 variables to 5 decimal places

#inputs are v1v2v3 coordinates of the first side
#inputs are w1w2w3 coordinates of the second side
def compute_distance(x1,y1,z1,x2,y2,z2):
    """This function uses the distance formula to return the distance between 2 vertices, rounded
    to 2 decimal places."""
    d=math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
    return round(d, 2)
def compute_face_normal(fp, face_index):
    """This function will compute the normals between faces. We do this using the cross product as well
    as the vertex data. We then round the results to 5 decimal places."""
    first, second, third=read_face_data(fp, face_index)
    x1, y1, z1=read_vertex_data(fp, first)
    x2, y2, z2=read_vertex_data(fp, second)
    x3, y3, z3=read_vertex_data(fp, third)
    A, B, C=(x2-x1, y2-y1, z2-z1)
    A1, B1, C1=(x3-x2, y3-y2, z3-z2)
    A2, B2, C2=compute_cross(A, B, C, A1, B1, C1)
    return round(A2, 5), round(B2, 5), round(C2, 5)

#compute cross is useful here
#index of face as int.,return 3 coordinates rounded to 5 decimal

def compute_face_area(fp, face_index):
    '''.'''
    first, second, third=read_face_data(fp, face_index)
    x1, y1, z1=read_vertex_data(fp, first)
    x2, y2, z2=read_vertex_data(fp, second)
    x3, y3, z3=read_vertex_data(fp, third)
    distance12=compute_distance(x1, y1, z1, x2, y2, z2)
    distance23=compute_distance(x2, y2, z2, x3, y3, z3)
    distance13=compute_distance(x1, y1, z1, x3, y3, z3)
    p=(distance12+distance23+distance13)/2
    area=math.sqrt(p*(p-distance12)*(p-distance13)*(p-distance23))
    return round(area, 2)

#compute distance is useful here
#round to 2 digits


def is_connected_faces(fp, f1_ind, f2_ind):
    """This function will determine if the faces are connected to each other by
    reading the face data from the file and if there is an index, it adds 1 to the counter. If the counter
    is greater than or equal to 2, meaning 2 sides connected, the function will return true."""
    s1= read_face_data(fp, f1_ind)
    s2= read_face_data(fp, f2_ind)
    counter=0
    for i in s1:
        for j in s2:
            if i==j:
                counter+=1
    return counter>=2
#Index of shape in question as a string
    #Either face or vertex, return true or false

        
def main():
    """The main function in this project will bring up a greeting, then promt the user to 
    enter a file. After this, we will bring up a menu of 6 choices, and prompt the user
    to choose a choice. If the choice is 1, the function will display the data of the first
    5 faces. If the choice is 2, we will return the normal of the faces. If the choice is 3,
    the area of the faces is computed. If the choice is 4, we determine if the two faces
    are connected or not. If the choice is 5, it will close the current file and prompt the user to enter a new
    one. If the choise is 6, the file closes and the loop breaks, printing a goodbye message."""
    
    print('''\nWelcome to Computer Graphics!
We are creating and handling shapes. Any shape can be represented by polygon meshes, 
which is a collection of vertices, edges and faces.''')
    run=True
    while True:
        if run:
            fp=open_file()
            run=False
        display_options()
        choice=input(">> Choice: ")
        while (choice.isdigit()==True and 1 <= int(choice) <= 7) == False:
            print("Please choose a valid option number.")
            choice=input(">> Choice: ") 
        choice=int(choice)
        if choice=='1':
            index=1
            face=read_face_data(fp, index)
            vertices=read_face_data(fp, index)
            print("{:^7s}{:^15s}".format(face, vertices))
    
        if choice=='2':
            
            facenormal=input("Enter face index as integer: ")
            while not check_valid(fp, facenormal, 'face'):
                print("This is not a valid face index.")
                facenormal=input("Enter face index as integer: ")
    
                x,y,z=compute_face_normal(fp, facenormal)
                print("The normal of face {}:{:>9.5f}{:>9.5f}{:>9.5f}".format(facenormal, x, y, z))
# Here we will print the normal of the faces using the proper formatting    
        elif choice=='3':
            facenormal=input("Enter face index as integer: ")
            while not check_valid(fp, facenormal, 'face'):
                print("This is not a valid face index.")
                facenormal=input("Enter face index as integer: ")
#Here we will print the area of the faces using the proper formatting
            x,y,z=compute_face_area(fp, facenormal)
            print("The area of face {}:{:>9.2f}{:>9.2f}{:>9.2f}".format(facenormal, x, y, z))
            
            
        elif choice=='4':
            facenormal1=input("Enter face 1 index as integer: ")
            while not check_valid(fp, facenormal1, 'face'):
                print("This is not a valid face index.")
                facenormal1=input("Enter face index 1 as integer: ")
                facenormal2=input("Enter face 2 index as integer: ")
            while not check_valid(fp, facenormal2, 'face'):
                print("This is not a valid face index.")
                facenormal2=input("Enter face 2 index as integer: ")
                if is_connected_faces(fp, facenormal1, facenormal2)==False:
                    print("The two faces are NOT connected.")
                elif is_connected_faces(fp, facenormal1, facenormal2)==True:
                    print("The two faces are conneted.")
        elif choice=='5':
            fp.close()
            #This will close the file and then prompt the user to enter a new one to open
            filename = input("Enter a file name: ")
            try:
                fp = open(filename)
                return fp
            except FileNotFoundError:
                print("error")
                    

#        #op.5 fp.close, fp=open_file()
#        #op. 6, break
        if choice=='6':
            print("Thank you, Goodbye!")
            fp.close()
            break
        #Choice 6 will bring the loop to an end

    ##read_face_data(fp,)
    
# Do not modify the next two lines.
if __name__ == "__main__":
    main()
