## The objective of this code is to read in all the relevant data from the decawave experiments
## Perform some
##
import matplotlib.pyplot
import matplotlib.pyplot as plt
import pandas as pd
import statistics
import matplotlib.ticker as tck
import numpy as np
import os

#file_locLOS_listner = r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test1LOS\BS_data'
file_locLOS = r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test1LOS\BS_data'
file_locNLOS = r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test2NLOS\QLAB'
file_locKFNLOS = r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test3NLOS\Test03_QLAB'

def read_file(ffp):
    """
    This function takes in a ffp of each file in the directory and outputs the experimental coordinates
    :param ffp: (a string) the full file path of each file in a directory
    :return data: data list of tuples each of which contain the experimental x and y_coordinate
    """
    i = 0
    x_parsed = []
    y_parsed = []
    x_coord_string = ""
    y_coord_string = ""
    with open(ffp, 'r') as file:
        for line in file:
            if ( (i % 3) == 0 and len(line) > 20 ):
                parse = line.split(' ')
                for item in parse:
                    if (item.startswith(',x')):
                        x_coord = item.split(':')[1].lstrip(',').rstrip(',')
                        for char in x_coord:
                            if ( (char).isalnum() or char =='.'):
                                x_coord_string +=char
                        x_coord_float = float(x_coord_string)
                        x_parsed.append(x_coord_float)
                        x_coord_string = ""
                    elif item.startswith(',y'):
                        y_coord = item.split(':')[1].lstrip(',').rstrip(',')
                        for char in y_coord:
                            if ( (char).isalnum() or char =='.'):
                                y_coord_string +=char
                        y_coord_float = float(y_coord_string)
                        y_parsed.append(y_coord_float)
                        y_coord_string = ""
            i+=1
    data = list(zip(x_parsed,y_parsed))
    return(data)

def getdataLOS():
    """
    this function reads in the .xlsx file where all the data is stored
    and returns the theoretical and experimental results
    :return:
        theor_result: A list of theoretical results Y_coordinates of Decawave Tag
        exp_result: a list of the experimental Y_coordinates of Decawave tag
    """
    df = pd.read_excel(r'Test01_LOS_IDEAS_TEK_4_22.xlsx', header = 0)
    anc_loc = df.loc[:,'Anchor Location(M)'].tolist()
    theor_result = df.loc[:,'Physical Tag Measurements(M)'].tolist()
    exp_result = df.loc[:,'Decawave Tag Measurements(M)'].tolist()
    return(theor_result,exp_result)

def parsedataLOS():
    """
    reads the file directory where the LOS data is stored and goes through every
    text file calling read_file to get the experimental data, while determining the
    theoretical measurements via text file names
    :return: LOS_Data: data containing both the theoretical and experimental data
            stored as an P*M(Number of tag positions by measurements) dimensions list of two tuples of two elements
             with the theoretical tuple being the first in each list
    """
    theor_coord = []
    exp_coord = []
    LOS_data = []
    for file in os.listdir(r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test1LOS\BS_data'):
        if file.endswith('.txt'):
            file_path = f"{file_locLOS}\{file}"
            data_exp = read_file(file_path)
            exp_coord.append(data_exp)
            new_file = file.replace('dot', '.')
            new_file  = new_file.rstrip('Y.txt')
            coords = new_file.split('X')
            theor_coord.append((coords[0], coords[1]))
    for x in range(len(theor_coord)):
        exp_coord[x].insert(0,theor_coord[x])
        LOS_data.append(exp_coord[x])
    return LOS_data

def readexpNLOSCoor(X,Y):
    """
    This function takes as input the x_and Y coordinates for each tag position
    and creates a tuple in (X,Y) form ultimately returning a list of tuples
    with each tuple being the X,Y coordinate of each tag per second per position
    :param X: Experimental X_Values for each data sheet(tag) position
              stored as a list
    :param Y:  Experimental Y_Values for each data sheet(tag) position
              stored as a list
    :return:Temp: A list containing the X,Y coordinates of each tag measurement per tag position 
    """
    temp = []
    for i in range(len(X)):
        temp.append((X[i], Y[i]))
    return temp

def parsedataNLOS():
    """
    This function Parses through every file in the NLOS directory and returns N-dimensional list equivalent to number of
    files in directory with each dimension containing a list of tuples of the experimental coordinates and theoretical
    as the last element in each R list
    :return: exp_data an N*R list of tuples with each tuple being either an experimental X*Y coord, the theor is first
    """
    exp_data = []
    theor_coord = []
    fctr = 0#file counter
    for file in os.listdir(r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test2NLOS\QLAB'):
        ffp = file_locNLOS + '/' + file
        file = file.rstrip('.csv')
        file = file.replace('dot','.')
        pars_exp = file.split('y')
        X_coord = float(pars_exp[0].lstrip('x'))##Theoretical X_Coordinate
        Y_coord = float(pars_exp[1])##Theoretical Y_Coordinate
        theor_coord.append((X_coord,Y_coord))
        df = pd.read_csv(ffp, header = 0)
        x_exp = df.loc[:,'x_pos'].tolist()##X coordinate per each tag position
        y_exp = df.loc[:,'y_pos'].tolist()##Y coordinate per each tag position
        exp_coord = readexpNLOSCoor(x_exp,y_exp)
        exp_coord.insert(0,(X_coord,Y_coord))
        exp_data.append(exp_coord)
        fctr+=1
    return(exp_data)

def return_LOSarray():
    """
    :return:
    """
    pass

def meanerrorLOS(LOS_data):
    """
    Ths Function takes in as input the theoretical and measured Decawave values and
    outputs a chart of the meausured vs
    :param tag_loc_LOS: a list of the theoretical y_values of the tag
    :param dec_loc_LOS: a list of the measured/experimental y_values of the tag
    :param los_data:
    :return:
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    tc = 0
    th = 0
    #print(len(LOS_data))
    for tag_pos in LOS_data:
        i = 1#measures every line in new document starts at first experimental measurement after new tag_pos,doc
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        tc+=1
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(float(y_theor))
    ydf = pd.DataFrame({'Theoretical Measurements': y_coord_theor_list, 'Experimental Measurements': y_coord_real_list})
    ydf.to_excel('Mean_Erorr_LOS.xlsx', sheet_name='sheet1', index=False)

def hist_LOS(LOS_data):
    """
    This function seeks to display two histograms(x,y) of the LOS_data
    :param LOS_data: a P*M list of tuples
    :return:
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    diff_x_list = []
    diff_y_list = []
    tc = 0
    th = 0
    for tag_pos in LOS_data:
        i = 1#measures every line in new document starts at first experimental measurement after new tag_pos,doc
        for meas in range(1,len(tag_pos),1):##goes through each measurement5 line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        tc+=1
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
    for i in range(len(x_coord_theor_list)):
        diff_x_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        diff_y_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))

    fig,(ax0,ax1) = plt.subplots(1,2)
    ax0.hist(diff_y_list, bins = 20, range = (-1,1), color = 'blue', edgecolor = 'black')
    ax0.set_title("Mean Error LOS(m) X coordinates")
    ax0.set(xlabel='Mean Error(m)',ylabel='Occurences')
    ax1.hist(diff_y_list,bins = 20, color = 'red', edgecolor = 'black')
    ax1.set_title("Mean Error LOS(m) Y coordinates")
    ax1.set(xlabel='Mean Error(m)',ylabel='Occurences')
    #fig, axes = plt.subplots(1,2)
    #plt.hist(diff_y_list, bins = 20, range = (-1,1), color = 'blue', edgecolor = 'black')
    #plt.xlabel('Measured Error(m) in Y')
    #plt.ylabel('Frequency')
    #plt.title('Measured Error(m) of Decawave')
    plt.show()

def range_errorLOS(LOS_data):
    """
    This function takes as input LOS_data and displays a bar graph of the standard deviations of range errors by distance
    :param parsed_LOS:A P*M nested list of tuples that contains 2D positioning information of each tag
    The first element in each list is a theoretical and the rest are experimental
    :return:N/A
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    diff_x_list = []## A list of the different between the measured versus theoretical X measurements
    diff_y_list = []## A list of the different between the measured versus theoretical Y measurements
    error_3 = []
    error_4 = []
    error_5 = []
    tc = 0
    th = 0
    for tag_pos in LOS_data:
        i = 1#measures every line in new document starts at first experimental measurement after new tag_pos,doc
        for meas in range(1,len(tag_pos),1):##goes through each measurement5 line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        tc+=1
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
    for i in range(len(x_coord_theor_list)):
        diff_x_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        diff_y_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))
    error_3 = diff_y_list[:131]## A tuple of every range error from
    error_4 = diff_y_list[131:211]## A tuple of every range error from
    error_5 = diff_y_list[211:]## A tuple of every range error from
    st3 =statistics.stdev(error_3)
    st4  = statistics.stdev(error_4)
    st5 = statistics.stdev(error_5)
    ranges = ['low', 'med', 'high']
    stds = [st3, st4, st5]
    plt.bar(ranges,stds, color = 'green')
    plt.xlabel("Ranges")
    plt.ylabel('Standard Deviation Errors(M)')
    plt.title("Standard deviation of Decawave Positioning errors in Meters")
    plt.show()

def cdf_dataLOS(LOS_data):
    """
    :param LOS_data: A P*M nested list of tuples that contains 2D positioning information of each tag
    The first element in each list is a theoretical and the rest are experimental
    :return: NA
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    diff_x_list = []## A list of the different between the measured versus theoretical X measurements
    diff_y_list = []## A list of the different between the measured versus theoretical Y measurements
    tc = 0
    th = 0
    for tag_pos in LOS_data:
        i = 1#measures every line in new document starts at first experimental measurement after new tag_pos,doc
        for meas in range(1,len(tag_pos),1):##goes through each measurement5 line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        tc+=1
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
    for i in range(len(x_coord_theor_list)):
        diff_x_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        diff_y_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))
    print(diff_y_list)
    cleanedList = [x for x in diff_x_list if str(x) != 'nan']
    count, bins_count = np.histogram(cleanedList, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.legend()
    plt.show()

def mean_errorNLOS(NLOS_data):
    """
    Ths Function takes in as input the NLOS data and graphs the measured vs. theoretical error of each point
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    for tag_pos in NLOS_data:
        for meas in range(1,len(tag_pos),1):##goes through each measurement5 line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
    ydf = pd.DataFrame({'Theoretical Measurements': y_coord_theor_list, 'Experimental Measurements': y_coord_real_list})
    ydf.to_excel('Mean_Erorr_NLOS.xlsx', sheet_name='sheet1', index=False)

def hist_NLOS(NLOS_data):
    """
    This function takes as input the NLOS data and displays two histograms of the measured error vs. frequency
     for both X and Y measurments
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    diff_x_list = []
    diff_y_list = []
    tc = 0
    th = 0
    for tag_pos in NLOS_data:
        i = 1#measures every line in new document starts at first experimental measurement after new tag_pos,doc
        for meas in range(1,len(tag_pos),1):##goes through each measurement5 line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        tc+=1
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
    for i in range(len(x_coord_theor_list)):
        diff_x_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        diff_y_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))
    fig,(ax0,ax1) = plt.subplots(1,2)
    ax0.hist(diff_x_list)
    ax1.hist(diff_y_list)
    matplotlib.pyplot.hist(diff_x_list)
    matplotlib.pyplot.hist(diff_y_list)
    plt.show()

def range_errorNLOS(NLOS_data):
    """
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    diff_x_list = []## A list of the different between the measured versus theoretical X measurements
    diff_y_list = []## A list of the different between the measured versus theoretical Y measurements
    error_3 = []
    error_4 = []
    error_5 = []
    tc = 0
    th = 0
    for tag_pos in NLOS_data:
        i = 1#measures every line in new document starts at first experimental measurement after new tag_pos,doc
        for meas in range(1,len(tag_pos),1):##goes through each measurement5 line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        tc+=1
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
    for i in range(len(x_coord_theor_list)):
        diff_x_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        diff_y_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))

    error_3 = diff_y_list[:131]
    error_4 = diff_y_list[131:211]
    error_5 = diff_y_list[211:]
    st3 = statistics.stdev(error_3)
    st4  = statistics.stdev(error_4)
    st5 = statistics.stdev(error_5)
    std = [st3,st4,st5]
    names = ['3m', '4m', '5']
    plt.bar(names,std)
    plt.show()

def cdfNLOS_data(NLOS_data):
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    diff_x_list = []## A list of the different between the measured versus theoretical X measurements
    diff_y_list = []## A list of the different between the measured versus theoretical Y measurements
    error_3 = []
    error_4 = []
    error_5 = []
    tc = 0
    th = 0
    for tag_pos in NLOS_data:
        i = 1#measures every line in new document starts at first experimental measurement after new tag_pos,doc
        for meas in range(1,len(tag_pos),1):##goes through each measurement5 line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_real:
        tc+=1
        x_real,y_real = tuple
        x_coord_real_list.append(x_real)
        y_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
    for i in range(len(x_coord_theor_list)):
        diff_x_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        diff_y_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))
    cleanedList = [x for x in diff_x_list if str(x) != 'nan']
    count, bins_count = np.histogram(cleanedList, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    # plotting PDF and CDF
    plt.plot(bins_count[1:], pdf, color="red", label="PDF")
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.legend()
    plt.show()

def parsedataKNLOS():
    """
    This function Parses through every file in the KNLOS directory and returns P*M-dimensional list equivalent to number
     of files in directory with each dimension containing a list of tuples of the observed vs updated position
      and theoretical as the first element in each P_list
    :return: data_tot an N*R list of tuples with each tuple being either the theoretical pos, or obs vs updated_pos
    """
    theor_coord = []
    data_tot = []
    complete_data = []
    i = 0
    c = 0
    for file in os.listdir(r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test3NLOS\Test03_QLAB'):
        ffp = file_locKFNLOS + '/' + file
        file = file.rstrip('.csv')
        file = file.replace('dot','.')
        pars_exp = file.split('X')
        X = float(pars_exp[0])
        Y = pars_exp[1].rstrip('Y')
        Y = float(Y)
        theor_coord.append((X,Y))
        df = pd.read_csv(ffp, header = 0)
        obs_pos = df.loc[:,'Obs_Position'].tolist()
        up_state  = df.loc[:,'Updated_State'].tolist()
        KF = readexpNLOSCoor(obs_pos,up_state)
        for meas in KF:
            final_data = parse_KNLOS(meas)
        KF.insert(0,(X,Y))##Adds the theroritical X and Y coordinates
        data_tot.append(KF)
    return data_tot


def KLEANNLOS(data_tot):
    """
    :param data_tot: data_tot an N*R list of tuples with each tuple being either the theoretical pos, or obs vs updated_pos
    :return:
    """
    print(data_tot)
    i = 0 #outer loop counter
    j = 0 #inner loop counter resets after each tag position
    for pos in data_tot:##The outer loop that goes through every position where the tag was placed
        print('')
        i+=1
        j = 0
        for meas in pos:##The inner loop, every measurement in the postion
            if (j == 0):##This should be the 2D theoretical coordinate
                pass
            else:##The various measurements at each interval
                ## Try to split the updates state to two seperate measurments
                print(meas)
            j+=1

def parse_KNLOS(measure):
    """
    :param measure:
    :return:
    """
    obs = measure[0]

    return(obs)


if __name__ == '__main__':
    theor_los,exp_los = getdataLOS() ## Function returns theoretical and experiment Y_coordinates as a list
    data_LOS = parsedataLOS()##Function to return the LOS data's coordinates as tuple w/ theor_first
    #meanerrorLOS(data_LOS)
    #hist_LOS(data_LOS)
    #range_errorLOS(data_LOS)
    cdf_dataLOS(data_LOS)
    #data_NLOS = parsedataNLOS()##Function to return the NLOS data coordinates as List of tuples w/theoretical first
    #print(data_NLOS[0][0])
    #mean_errorNLOS(data_NLOS)##Mean error of NLOS data
    #hist_NLOS(data_NLOS)##histogram of NLOS data
    #range_errorNLOS(data_NLOS)##range error of NLOS data
    #cdfNLOS_data(data_NLOS)
    #data_KNLOS = parsedataKNLOS()##Function to return the KNLOS data; then tuples of obs vs predicted_pos in 2d first tuple is theoretical
    #parse_KNLOS(data_KNLOS)
    #KLEANNLOS(data_KNLOS)
