import glob
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import copy
from mpl_toolkits.mplot3d import Axes3D


def plot2d(input_dictionary,sample_dictionary):
    '''to create a 2D plot based in the input argument
    where the user specifies the elements, metalicity,
    the rotation, C13 pockets, and the legend type with
    masses on x axis and yield on the y axis '''
    Yield_values=[]
    Masses=[]
    dictionary={}
    data_dictionary={}
    temp_input_dictionary=copy.deepcopy(input_dictionary)
    #dictionary format {element1:{C13_Pocket:{Rotation1:{Metalicity:[[Masses][Yield_Values]]},Rotation2:{Metalicity:[[Masses][Yield_Values]]}}},element2:{C13_Pocket:{Rotation1:{Metalicity:[[Masses][Yield_Values]]},Rotation2:{Metalicity:[[Masses][Yield_Values]]}}}}

    #creating an empty dictionary template in the above written format which will contain data
    
    for i in range (len(input_dictionary.get('Elements:'))):
        element= input_dictionary.get('Elements:')[i]
        #getting the element information form the reference file
        if element in sample_dictionary:
            p=sample_dictionary.get(element)
            a=p[0]
            z=p[1]
        else:
            print("The element does not exist in the reference file")
        data_dictionary[input_dictionary.get('Elements:')[i]]={}

        for j in range(len(input_dictionary.get('C13_Pocket:'))):
            '''changing the values of C13_Pocket in the temporary dictionary keeping the input_dictionary unchanged'''
            if input_dictionary.get('C13_Pocket:')[j]=='T':
                temp_input_dictionary.get('C13_Pocket:')[j]='Extended'
            elif input_dictionary.get('C13_Pocket:')[j]=='0':
                temp_input_dictionary.get('C13_Pocket:')[j]='Standard'
            data_dictionary[input_dictionary.get('Elements:')[i]][input_dictionary.get('C13_Pocket:')[j]]={}

            for k in range(len(input_dictionary.get('Rotation:'))):
                data_dictionary[input_dictionary.get('Elements:')[i]][input_dictionary.get('C13_Pocket:')[j]][input_dictionary.get('Rotation:')[k]]={}

                for l in range (len(input_dictionary.get('Metalicities:'))):
                    if input_dictionary.get('Metalicities:')[l]=='zsun':
                        temp_input_dictionary.get('Metalicities:')[l]='0.014'
                    elif input_dictionary.get('Metalicities:')[l]!='zsum':
                        met=re.split('z|m',input_dictionary.get('Metalicities:')[l])

                        #changing the metalicity from string to a numerical value
                        temp_input_dictionary.get('Metalicities:')[l]=str(round(float(met[1])*0.1**float(met[2]),6))

                    #search for files containg the specified values of metalicity, rotation and C13_Pocket
                    files = glob.glob("Yield Data/*%s_%s%s_*"%(input_dictionary.get('Metalicities:')[l],input_dictionary.get('C13_Pocket:')[j],input_dictionary.get('Rotation:')[k]))        

                    for file in files:
                        with open(file) as f:
                            m=f.readlines()
                            for string in m[1:]:
                                u=string.split()
                                dictionary[(int(u[1]),int(u[2]))]=u[3]
                                u=[]
                        '''removing the extra elements from the file name and
                        converting the mass into numercal form and saving it in a file'''
                        #adding the yield value in a table which would then be added to the data_dictionary
                        Yield_values.append(float(dictionary.get((a,z))))
                        #obtain the meta data of the data using the file name
                        values=file.replace("Yield Data\yields_tot_m","")
                        values=values.replace('sun','14m3')
                        values=values[0:11]
                        values=re.split('p|z|m|_', values)
                        mass=float(values[0])+float(values[1])*0.1
                        Masses.append(float(mass))
                        dictionary={}
                        #print(file)

                    '''adding the masses and their corresponding yield into the data_dictionary for their respective, Elements, C13_Pockets, Rotation and Metalicity'''
                    data_dictionary[input_dictionary.get('Elements:')[i]][input_dictionary.get('C13_Pocket:')[j]][input_dictionary.get('Rotation:')[k]][input_dictionary.get('Metalicities:')[l]]=[Masses,Yield_values]
                    Masses=[]
                    Yield_values=[]
    #print(data_dictionary)
    #dictionary format {element1:{C13_Pocket:{Rotation1:{Metalicity:[[Masses][Yield_Values]]},Rotation2:{Metalicity:[[Masses][Yield_Values]]}}},element2:{C13_Pocket:{Rotation1:{Metalicity:[[Masses][Yield_Values]]},Rotation2:{Metalicity:[[Masses][Yield_Values]]}}}}
    
    
    #ploting 2d graph
    '''creaing a list of paramenter and then switiching the elements so the the
    parameter chosen for comparison is placed at the 0th position of the list'''
    order=['Metalicities:', 'Rotation:', 'C13_Pocket:', 'Elements:']
    pointer=order.index(input_dictionary.get('Compare:')[0]+':')
    order[0],order[pointer]=input_dictionary.get('Compare:')[0]+':',order[0]
    #print(order)


    '''reading the data from the data_dictionary in the order of the order list
    so that the parameter representing the first element of the order list be
    the last loop in the following nested loop in order to itterate through the
    data_dictionary according to the parameter specified in the Compare: line of
    the input file'''
        
    for q in range (len(input_dictionary.get(order[3]))):
        for w in range (len(input_dictionary.get(order[2]))):
            for e in range (len(input_dictionary.get(order[1]))):
                fig=plt.figure()
                plt.xlabel('Initial Mass [$M_{\odot}$]')
                plt.ylabel('Yields [$M_{\odot}$]')

                for r in range (len(input_dictionary.get(order[0]))):
                    sequence=[r,e,w,q]
                    if input_dictionary.get('Compare:')[0]=='Rotation':
                        sequence[1],sequence[0]=sequence[0],sequence[1]
                    elif input_dictionary.get('Compare:')[0]=='C13_Pocket':
                        sequence[2],sequence[0]=sequence[0],sequence[2]
                    elif input_dictionary.get('Compare:')[0]=='Elements':
                        sequence[3],sequence[0]=sequence[0],sequence[3]
                    Data=(data_dictionary[input_dictionary.get('Elements:')[sequence[3]]][input_dictionary.get('C13_Pocket:')[sequence[2]]][input_dictionary.get('Rotation:')[sequence[1]]][input_dictionary.get('Metalicities:')[sequence[0]]])
                    print(Data)
                    plt.plot(Data[0],Data[1],label=temp_input_dictionary.get(order[0])[r])
                    plt.scatter(Data[0],Data[1])
                ax = plt.gca()
                ax.set_yscale('log')
                plt.tick_params(axis='y', which='minor')
                plt.grid(which='minor',linestyle=':')
                plt.grid(which='major',linestyle='-')
                title=('%s %s, %s %s, %s %s'%(order[3],temp_input_dictionary.get(order[3])[q],order[2],temp_input_dictionary.get(order[2])[w],order[1],temp_input_dictionary.get(order[1])[e]))
                print(title)
                plt.title(title)
                plt.legend()
                    
    plt.show()


def plot3d(input_dictionary,sample_dictionary):
    '''to create a 3D plot based on the input argument
    where the user specifies the elements,the rotation,
    C13 pockets and the masses. X axis contains the Masses,
    y axis contains the metalicity and the z axis contains
    the Yields'''
    
    dictionary={}  
    '''collecting on the element from the reference file'''
    
    for i in range (len(input_dictionary.get('Elements:'))):
        element= input_dictionary.get('Elements:')[i]
        if element in sample_dictionary:
            p=sample_dictionary.get(element)
        else:
            print("The element does not exist in the reference file")
        a=p[0]
        z=p[1]                                       #adding the element in 'El40' formt as key and the A and Z value as its value in a tuple

        '''choosing the values of C13_Pockets, Rotation and
        elements from input file'''
        
        for j in range (len(input_dictionary.get('C13_Pocket:'))):
            if input_dictionary.get('C13_Pocket:')[j]=='T':
                pocket='Extended'
            elif input_dictionary.get('C13_Pocket:')[j]=='0':
                pocket='Standard'

            for k in range (len(input_dictionary.get('Rotation:'))):
                fig=plt.figure()
                ax = plt.axes(projection="3d")

                for l in range (len(input_dictionary.get('Mass:'))):
                    Yield_values=[]
                    Masses=[]
                    Metalicities=[]
                    temp_Yield=[]
                    temp_Metalicity=[]
                    files = glob.glob("Yield Data/*%s*%s%s_*"%(input_dictionary.get('Mass:')[l],input_dictionary.get('C13_Pocket:')[j],input_dictionary.get('Rotation:')[k]))
                    for file in files:
                        values=file.replace("Yield Data\yields_tot_m","")
                        values=values.replace('sun','14m3')
                        values=values[0:11]
                        values=re.split('p|z|m|_', values)
                        mass=float(values[0])+float(values[1])*0.1
                        Masses.append(float(mass))
                        metalicity=float(values[2])*10**(-float(values[3]))
                        temp_Metalicity.append(metalicity)
                        with open(file) as f:
                                i = f.readlines()
                                for string in i[1:]:
                                    u=string.split()                                                                     #list of all the elements seperated by spaces 
                                    dictionary[(int(u[1]),int(u[2]))]=u[3]                                         #adding the A and Z in tupple format as key with yield value as the value
                                    u=[]
                        temp_Yield.append(float(dictionary.get((a,z))))
                        dictionary={}
                    Yield_values=[x for y, x in sorted(zip(temp_Metalicity,temp_Yield))]
                    Metalicities=sorted(temp_Metalicity)
                    ax.plot3D(Masses, Metalicities, Yield_values)
                    ax.scatter3D(Masses, Metalicities, Yield_values)
                    plt.minorticks_on()
                    ax.set_xlabel('Initial Mass [$M_{\odot}$]')
                    ax.set_ylabel('Metalicity')
                    ax.set_zlabel('Yields [$M_{\odot}$]')
                title=('Element: %s, C13_Pocket: %s, Rotation: %s'%(element,pocket,input_dictionary.get('Rotation:')[k]))
                ax.set_title(title)
    plt.show()



def supernova(input_dictionary):
    '''to create a 2D plot based on the input argument
    where the user specifies the elements,the velocity
    and the metalicity. X axis contains the Masses,
    y axis contains the yields'''
    
    data_dictionary={}
    file='Yield Data/Supernova/supernova_yield.txt'
    with open(file) as q:
        w=q.readlines()
        Mass=list(map(int,w[0].split()))
        w=w[1:]
        Z=input_dictionary.get('Z:')
        Vel=input_dictionary.get('Vel:')


        for  i in range (len(Vel)):
            Vel[i]=int(int(Vel[i])/150)+1
        for i in range (len(Z)):
            Z[i]=-(int(Z[i]))+1
        '''using the value of the vel and Z, going to the the
        from where a new data set begins having velocity value
        Vel and Z value, this exists after every 336 lines, if
        new elements are added, then this number needs to be updated'''
        
        for m in range (len(input_dictionary.get('Elements:'))):
            data_dictionary[input_dictionary.get('Elements:')[m]]=[]
            for i in Z:
                for j in  Vel:
                    
                    index =((i-1)*3+(j-1))*336
                    for k in range (index+1,index+336):
                        data= w[k].split(' & ')
                        data[-1]=data[-1].split(' ')[0]
                        for l in range (1,len(data)):        #checking whether the line containd the data fo rthe chosen element
                            data[l]=float(data[l])
                        data[0]=data[0].split(' ')[0]
                        if input_dictionary.get('Elements:')[m]==data[0]:
                            data_dictionary[input_dictionary.get('Elements:')[m]].append([['v=%s, Z=%s'%((j-1)*150, -(i)+1)],data[1:]])





#data plotting
    #print(input_dictionary.get('Compare:')[0])

    '''plotting data for different values of Compare in the infut file'''
    
    if input_dictionary.get('Compare:')[0]=='Elements':

        for i in range (len(Vel)*len(Z)):
            fig=plt.figure()
            plt.xlabel('Initial Mass [$M_{\odot}$]')
            plt.ylabel('Yields [$M_{\odot}$]')
            plt.title(data_dictionary[input_dictionary.get('Elements:')[i]][j][0][0])
            for j in range (len(input_dictionary.get('Elements:'))):
                plt.plot(Mass,data_dictionary[input_dictionary.get('Elements:')[j]][i][1],label=input_dictionary.get('Elements:')[j])

            ax = plt.gca()
            ax.set_yscale('log')
            plt.tick_params(axis='y', which='minor')
            plt.grid(which='minor',linestyle=':')
            plt.grid(which='major',linestyle='-')
        plt.legend()


    else:
        for i in range (len(input_dictionary.get('Elements:'))):
            fig=plt.figure()
            plt.xlabel('Initial Mass [$M_{\odot}$]')
            plt.ylabel('Yields [$M_{\odot}$]')
            plt.title(input_dictionary.get('Elements:')[i])
            for j in range(len(Vel)*len(Z)):
                lab=data_dictionary[input_dictionary.get('Elements:')[i]][j][0][0]
                plt.plot(Mass,data_dictionary[input_dictionary.get('Elements:')[i]][j][1],label=lab)
            plt.legend()
            ax = plt.gca()
            ax.set_yscale('log')
            plt.tick_params(axis='y', which='minor')
            plt.grid(which='minor',linestyle=':')
            plt.grid(which='major',linestyle='-')
    
    plt.show()



                            
                    
sample_dictionary={}
sample_file='Reference_Data.txt'
with open(sample_file) as q:
        o=q.readlines()
        for values in o:
            line=values.split()
            sample_dictionary[line[0]]=(int(line[1]),int(line[2]))
            


inputfile='C:/Users/Akshat Garg/Desktop/Konkoly Project/Data Visualisation\inputfile.txt'
input_dictionary={}
with open(inputfile) as input_file:
    r=input_file.readlines()
    for i in range(1,len(r)):
        input_dictionary[r[i].split()[0]]=r[i].split()[1:]
    if input_dictionary.get('Plot_type:')[0]=='supernova':
        supernova(input_dictionary)
    else:
        if int(input_dictionary.get('Axis:')[0])==3:
            plot3d(input_dictionary,sample_dictionary)
        elif int(input_dictionary.get('Axis:')[0])==2:
            plot2d(input_dictionary,sample_dictionary)
        else:
            print("Error with number of Axis")
