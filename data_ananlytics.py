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
file_locNLOS = r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test2NLOS\BS_Data'
file_locKFNLOS = r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test3NLOS\BS_Data'

def read_file(ffp):
    """
    This function takes in a ffp of each file in the directory and outputs the experimental coordinates
    :param ffp: (a string) the full file path of each file in a directory
    :return data: data list of tuples each of which contain all the experimental x and y_coordinate
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
    text file; calling read_file to get the experimental data, while determining the
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
            data_exp = read_file(file_path)##The experimental measurements
            exp_coord.append(data_exp)
            new_file = file.replace('dot', '.')
            new_file  = new_file.rstrip('Y.txt')
            coords = new_file.split('X')
            theor_coord.append((coords[0], coords[1]))##Theoretical Coordinates
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
    for file in os.listdir(r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test2NLOS\BS_Data'):
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

def rangerror_LOS(LOS_data):
    """
    Ths Function takes in as input the theoretical and measured Decawave values and
    outputs a chart of the meausured vs theroetical LOS error
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
    ydf.to_excel('RangeError_LOS.xlsx', sheet_name='sheet1', index=False)

def hist_LOS(LOS_data):
    """
    This function seeks to display two histograms(x,y) of the LOS_data
    Ass well as a singular histogram with both errors together
    :param LOS_data: a P*M list of tuples
    :return:N/A
    """
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    x_coord_real_list = [] ## an unpacked list of each X_real_measurement
    y_coord_real_list = [] ## an unpacked list of each Y_real_measurement
    x_coord_theor_list = [] ## an unpacked list of each X_real_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_real_measurement
    diff_x_list = []
    diff_y_list = []
    diff_tot_list = []
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

    diff_tot_list = diff_y_list + diff_x_list

    fig,(ax0,ax1) = plt.subplots(1,2)
    ax0.hist(diff_y_list, bins = 20, range = (-1,1), color = 'blue', edgecolor = 'black')
    ax0.set_title("Mean Error LOS(m) X coordinates")
    ax0.set(xlabel='Mean Error(m)',ylabel='Occurences')
    ax1.hist(diff_y_list,bins = 20, color = 'red', edgecolor = 'black')
    ax1.set_title("Mean Error LOS(m) Y coordinates")
    ax1.set(xlabel='Mean Error(m)',ylabel='Occurences')
    fig, axes = plt.subplots(1,2)
    plt.hist(diff_y_list, bins = 20, range = (-1,1), color = 'blue', edgecolor = 'black')
    plt.xlabel('Measured Error(m) in Y')
    plt.ylabel('Frequency')
    plt.title('Measured Error(m) of Decawave')

    #plt.hist(diff_tot_list,bins=20, color = 'blue', edgecolor = 'black')
    #plt.xlabel('Error (m)')
    #plt.ylabel('Frequency')
    #plt.title("Frequency of Errors in (m) in LOS scenario")
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
    error_3 = diff_y_list[:132]## A tuple of every range error from
    error_4 = diff_y_list[132:208]## A tuple of every range error from
    error_5 = diff_y_list[208:]## A tuple of every range error from
    st3 =statistics.stdev(error_3)
    st4  = statistics.stdev(error_4)
    st5 = statistics.stdev(error_5)
    ranges = ['0-3', '3.25 - 4.5', '5.0 - 5.5']
    stds = [st3, st4, st5]
    plt.bar(ranges,stds, color = 'green')
    plt.xlabel("Range Intervals (m) ")
    plt.ylabel('Standard Deviation (m)')
    plt.title("Standard deviation of Decawave Positioning errors in LOS")
    plt.show()

def cdf_dataLOS(LOS_data):
    """
    This function calculates and displays the CDF of range errors in LOS
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
    cleanedList = [x for x in diff_x_list if str(x) != 'nan']##Removes undefined item
    count, bins_count = np.histogram(cleanedList, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.title('Cumulative Density Function(CDF) of Positioning error in LOS')
    plt.xlabel('Localization Error(m)')
    plt.ylabel('Probability')
    plt.legend()
    plt.show()

def rangeerrorNLOS(NLOS_data):
    """
    Ths Function takes in as input the NLOS data and graphs the measured vs. theoretical error of each point
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    ctr = 0
    i = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    data_final = [] ## a list of tuples of
    theor_list = [] ## list of floats
    real_list = []  ## list of floats
    for tag_pos in NLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_theor:
        X_real,Y_real = data_real[ctr]
        X_theor,Y_theor = data_theor[ctr]
        X_coord = (X_real,X_theor)
        Y_coord = (Y_real,Y_theor)
        data_final.append(X_coord)
        data_final.append(Y_coord)
        ctr+=1
    for tuple in data_final:
        real,theor = tuple
        theor_list.append(theor)
        real_list.append(real)
    df = pd.DataFrame({'Theoretical Measurements': theor_list, 'Experimental Measurements': real_list})
    df.to_excel('Mean_Erorr_NLOS.xlsx', sheet_name='sheet1', index=False)

def hist_NLOS(NLOS_data):
    """
    This function takes as input the NLOS data and displays one histogram of the measured error vs. frequency
     for both X and Y measurements combined
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    ctr = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    data_final = [] ## a list of tuples of
    theor_list = [] ## list of floats
    real_list = []  ## list of floats
    diff_list = [] ## A list containing the differences between theoretical and real measurements

    ##Going through the data and creating real and theor
    for tag_pos in NLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])

    ##Create list of tuples of theor vs experimental X,Y and cordiantes
    for tuple in data_theor:
        X_real,Y_real = data_real[ctr]
        X_theor,Y_theor = data_theor[ctr]
        X_coord = (X_real,X_theor)
        Y_coord = (Y_real,Y_theor)
        data_final.append(X_coord)
        data_final.append(Y_coord)
        ctr+=1

    ##Seperate into two distinct lists theoretical and real; every other one should be an X or Y coordiant shoud go X,Y,X,Y
    for tuple in data_final:
        real,theor = tuple
        theor_list.append(theor)
        real_list.append(real)

    ## Create differences between the two
    for i in range(len(theor_list)):
        diff_list.append(real_list[i] - theor_list[i])

    ## Histogram Stuff
    plt.hist(diff_list,bins=20, color = 'blue', edgecolor = 'black')
    plt.xlabel('Error (m)')
    plt.ylabel('Frequency')
    plt.title("Frequency of Errors in (m) in NLOS scenario")
    plt.show()
    plt.ylabel()

def range_errorNLOS(NLOS_data):
    """
    The objective of this function is to display the standard deviation of errors across different ranges; short,middle,long
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    ctr = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    data_final = [] ## a list of tuples of
    theor_list = [] ## list of floats
    real_list = []  ## list of floats
    diff_list = [] ## list of difference between the two
    short_error = []##list of errors from 0-3m
    med_error = []##list of errors from 3.5-5.0.
    long_error = []## list of errors from 5.5 - 7.5m

    for tag_pos in NLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_theor:
        X_real,Y_real = data_real[ctr]
        X_theor,Y_theor = data_theor[ctr]
        X_coord = (X_real,X_theor)
        Y_coord = (Y_real,Y_theor)
        data_final.append(X_coord)
        data_final.append(Y_coord)
        ctr+=1
    for tuple in data_final:
        real,theor = tuple
        theor_list.append(theor)
        real_list.append(real)
    for i in range(len(real_list)):
        diff_list.append(real_list[i] - theor_list[i])

    x_theor = theor_list[0::2]
    y_theor = theor_list[1::2]
    x_exp   = real_list[0::2]
    y_exp   = real_list[1::2]
    diff_x = []
    diff_y = []
    ## Getting the differences between theoretical and experimental values
    for i in range(len(x_theor)):
        diff_y.append(y_theor[i] - y_exp[i])
        diff_x.append(x_theor[i] - x_exp[i])
    short_error.append(diff_x[0:258])
    med_error.append(diff_x[258::])
    short_error.append(diff_y[0:84])
    short_error.append(diff_y[171:200])
    short_error.append(diff_y[258:345])##1.5
    short_error.append(diff_y[345:374])##2.5
    med_error.append(diff_y[374:403])##3.5
    med_error.append(diff_y[403:432])##4.5
    long_error.append(diff_y[432:461])##4.5
    long_error.append(diff_y[200:229])##6.0
    long_error.append(diff_y[84:113])#6.5
    long_error.append(diff_y[461:490])#6.5
    long_error.append(diff_y[200:229])#7.0
    long_error.append(diff_y[229:258])#7.0
    long_error.append(diff_y[490])#7.5

    error_short = short_error[0] + short_error[1] + short_error[2] + short_error[3] + short_error[4]
    error_med = med_error[0] + med_error[1] + med_error[2]
    error_lon = long_error[0] + long_error[1] + long_error[2] + long_error[3] + long_error[4] + long_error[5]
    error_lon.append(long_error[6])

    std_short = statistics.stdev(error_short)
    std_med   = statistics.stdev(error_med)
    std_lon   = statistics.stdev(error_lon)

    ranges = ['0-3', '3.5 - 5.0', '5.5 - 7.5']
    stds = [std_short, std_med, std_lon]
    plt.bar(ranges,stds, color = 'green')
    plt.xlabel("Range Intervals (m) ")
    plt.ylabel('Standard Deviation (M)')
    plt.title("Standard deviation of Decawave Positioning errors in NLOS")
    plt.show()

def cdfNLOS_data(NLOS_data):
    """
    The objective of this function is to display the cdf of the localization errors
    :param NLOS_data: NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return:  N/A
    """
    ctr = 0
    i = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    data_final = [] ## a list of tuples of
    theor_list = [] ## list of floats
    real_list = []  ## list of floats
    diff_list = [] ## A list containing the differences between theoretical and real measurements

    for tag_pos in NLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_theor:
        X_real,Y_real = data_real[ctr]
        X_theor,Y_theor = data_theor[ctr]
        X_coord = (X_real,X_theor)
        Y_coord = (Y_real,Y_theor)
        data_final.append(X_coord)
        data_final.append(Y_coord)
        ctr+=1
    for tuple in data_final:
        real,theor = tuple
        theor_list.append(theor)
        real_list.append(real)
    for i in range(len(theor_list)):
        diff_list.append(real_list[i] - theor_list[i])
    cleanedList = [x for x in diff_list if str(x) != 'nan']
    count, bins_count = np.histogram(cleanedList, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.title('Cumulative Density Function(CDF) of Positioning error in NLOS')
    plt.xlabel('Localization Error(m)')
    plt.ylabel('Probability')
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

    for file in os.listdir(r'C:\Users\GregK\Desktop\Thesis_Data_analytics\Data_Analytics\Results\Test3NLOS\BS_Data'):
        ffp = file_locKFNLOS + '/' + file
        file = file.rstrip('.csv')
        file = file.replace('dot','.')
        pars_exp = file.split('X')
        X = float(pars_exp[0])
        Y = pars_exp[1].rstrip('Y')
        Y = float(Y)
        theor_coord.append((X,Y))## The theoretical
        df = pd.read_csv(ffp, header = 0)
        obs_pos = df.loc[:,'Obs_Position'].tolist()
        up_state = df.loc[:,'Updated_State'].tolist()
        KF = parse_KNLOS(obs_pos,up_state)
        KF.insert(0,(X,Y))##Adds the theroritical X and Y coordinates
        data_tot.append(KF)
    return data_tot

def parse_KNLOS(obs,upd):
    """
    Is called in the parsedataKNLOS function and appends every observed and updated position to a nice list
    Returns list called final which contains the observed and updated position
    :param obs -  The observed position; a 2d list
           upd  - The predicted position; a 2d list
    :return:final - a list of each and every obs and upd position
    """
    final = []
    for i in range(len(obs)):
        final.append((obs[i], upd[i]))
    return(final)

def tuple2list(final):
    """
    This function iterates through the tuple of measurements and converts them to a list
    :param final: The final data set of each measurement; a list of list
    :return: Final List - A P*M lists of list with each granular item being a list of both the obs vs upd pos
    """
    oc = 0
    final_list = []
    temp = []
    for pos in final:##outer loop position of tag
        ic = 0 ## resets the inner count variable to 0; used to elimnate theoretical measurements
        for meas in pos:##inner loop
            if ic  == 0:
                temp.append(meas)
            if ic > 0:
                measlist = list(meas)
                temp.append(measlist)
            ic+=1
        final_list.append(temp)
        temp = []
        oc+=1
    return(final_list)

def finalKNLOSdata(listdata):
    """
    This function parses through some of the additional and unneccesary text, namely '\n'
    :param: listdata A P*M lists of list with each granular item being a list of both the obs vs upd pos
    :return: finaldata - A P*M list of list with each item containing either the theoretical pos or the
            obs and updated position as a 2D state
    """
    finaldata = []
    tempdata = []
    for pos in listdata:
        ic = 0
        for meas in pos:
            ic+=1
            if ic  == 1:
                tempdata.append(meas)
            elif ic > 1:
                if '\n' in meas[1]:
                    for place,item in enumerate(meas[1]):
                        if item == '\n':
                            tp = place
                    meas[1] = meas[1][:tp]
                tempdata.append(meas)
        finaldata.append(tempdata)
        tempdata = []
    return(finaldata)

def mean_errorKNLOS(KNLOS_data):
    """

    :param KNLOS_data: A P*M list of list with each item containing either the theoretical pos or the
            obs and updated position as a 2D state
    :return: N/A Will write ot an excel fil
    """

    ctr = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    data_final = [] ## a list of tuples of
    theor_list = [] ## list of floats
    real_list = []  ## list of floats
    for tag_pos in KNLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            print(tag_pos[meas])
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_theor:
        X_real,Y_real = data_real[ctr]
        X_theor,Y_theor = data_theor[ctr]
        X_coord = (X_real,X_theor)
        Y_coord = (Y_real,Y_theor)
        data_final.append(X_coord)
        data_final.append(Y_coord)
        ctr+=1
    for tuple in data_final:
        real,theor = tuple
        theor_list.append(theor)
        real_list.append(real)
    df = pd.DataFrame({'Theoretical Measurements': theor_list, 'Experimental Measurements': real_list})
    df.to_excel('Mean_Erorr_KNLOS.xlsx', sheet_name='sheet1', index=False)

def hist_KNLOS(KNLOS_data):
    """
    This function receieves as input the KNLOS_data and creates and displays two histograms, one of the observed
    position erros and the other of the Updated State
    :param KNLOS_data: A P*M list of list with each item containing either the theoretical pos or the
            obs and updated position as a 2D state
    :return: N/A
    """

    ctr = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    obs_list = []  ## list of floats
    theor_list = [] ## list of floats
    finallist = []
    diff_list = [] ## A list containing the differences between theoretical and real measurements
    Obs_Pos_list = []
    UPd_State_list = []

    ## Go through the KNLOS data and create two lists, one of theoretical and one of real data
    for tag_pos in KNLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])## Theoretical Data

    ##Create the lsit of observed data as a two-dimensional list
    for item in range(len(data_real)):
        data_upd = data_real[item][1]
        data_upd_str = data_upd.replace("[", "")
        data_upd_str = data_upd_str.replace(']', '')
        data_no_c = data_upd_str.replace(',', '')
        data_obs_list = data_no_c.split()
        obs_list.append(data_obs_list)

    ## Unpack the X and Y coordinates from the list, both theor and observed
    for place, item in enumerate(obs_list):
        X_obs,Y_obs =  obs_list[place]
        X_theor,Y_theor = data_theor[place]
        theor_list.append(X_theor)
        theor_list.append(Y_theor)
        finallist.append(float(X_obs))
        finallist.append(float(Y_obs))

    ## Create differences between the two
    for i in range(len(theor_list)):
        diff_list.append(finallist[i] - theor_list[i])

    ## Histogram Stuff
    plt.hist(diff_list,bins=20, color = 'blue', edgecolor = 'black')
    plt.xlabel('Error (m)')
    plt.ylabel('Frequency')
    plt.title("Frequency of Errors in (m) in NLOS scenario")
    plt.show()
    plt.ylabel()

def range_errorKNLOS(KNLOS_data):
    """
    The objective of this function is to display the standard deviation of errors across different ranges; short,middle,long
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    ctr = 0
    i = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    data_final = [] ## a list of tuples of
    theor_list = [] ## list of floats
    real_list = []  ## list of floats
    diff_list = [] ## list of difference between the two
    short_error = []##list of errors from 0-3m
    med_error = []##list of errors from 3.5-5.0.
    long_error = []## list of errors from 5.5 - 7.5m
    for tag_pos in KNLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_theor:
        X_real,Y_real = data_real[ctr]
        X_theor,Y_theor = data_theor[ctr]
        X_coord = (X_real,X_theor)
        Y_coord = (Y_real,Y_theor)
        data_final.append(X_coord)
        data_final.append(Y_coord)
        ctr+=1
    for tuple in data_final:
        real,theor = tuple
        theor_list.append(theor)
        real_list.append(real)
    for i in range(len(real_list)):
        diff_list.append(real_list[i] - theor_list[i])
    print(diff_list)
    x_theor = theor_list[0::2]
    y_theor = theor_list[1::2]
    x_exp   = real_list[0::2]
    y_exp   = real_list[1::2]
    diff_x = []
    diff_y = []
    ## Getting the differences between theoretical and experimental values
    for i in range(len(x_theor)):
        diff_y.append(y_theor[i] - y_exp[i])
        diff_x.append(x_theor[i] - x_exp[i])
    short_error.append(diff_x[0:258])
    med_error.append(diff_x[258::])
    short_error.append(diff_y[0:84])
    short_error.append(diff_y[171:200])
    short_error.append(diff_y[258:345])##1.5
    short_error.append(diff_y[345:374])##2.5
    med_error.append(diff_y[374:403])##3.5
    med_error.append(diff_y[403:432])##4.5
    long_error.append(diff_y[432:461])##4.5
    long_error.append(diff_y[200:229])##6.0
    long_error.append(diff_y[84:113])#6.5
    long_error.append(diff_y[461:490])#6.5
    long_error.append(diff_y[200:229])#7.0
    long_error.append(diff_y[229:258])#7.0
    long_error.append(diff_y[490])#7.5

    error_short = short_error[0] + short_error[1] + short_error[2] + short_error[3] + short_error[4]
    error_med = med_error[0] + med_error[1] + med_error[2]
    error_lon = long_error[0] + long_error[1] + long_error[2] + long_error[3] + long_error[4] + long_error[5]
    error_lon.append(long_error[6])

    std_short = statistics.stdev(error_short)
    std_med   = statistics.stdev(error_med)
    std_lon   = statistics.stdev(error_lon)

    ranges = ['0-3', '3.5 - 5.0', '5.5 - 7.5']
    stds = [std_short, std_med, std_lon]
    plt.bar(ranges,stds, color = 'green')
    plt.xlabel("Range Intervals (m) ")
    plt.ylabel('Standard Deviation Errors(M)')
    plt.title("Standard deviation of Decawave Positioning errors in NLOS")
    plt.show()

def cdfKNLOS_data(KNLOS_data):
    """
    :param KNLOS_data:
    :return:
    """
    ctr = 0
    data_real =  [] ## a list of tuples of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    data_final = [] ## a list of tuples of
    theor_list = [] ## list of floats
    real_list = []  ## list of floats
    diff_list = [] ## A list containing the differences between theoretical and real measurements

    for tag_pos in KNLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append((tag_pos[meas]))
            data_theor.append(tag_pos[0])
    for tuple in data_theor:
        X_real,Y_real = data_real[ctr]
        X_theor,Y_theor = data_theor[ctr]
        X_coord = (X_real,X_theor)
        Y_coord = (Y_real,Y_theor)
        data_final.append(X_coord)
        data_final.append(Y_coord)
        ctr+=1
    for tuple in data_final:
        real,theor = tuple
        theor_list.append(theor)
        real_list.append(real)
    for i in range(len(theor_list)):
        diff_list.append(real_list[i] - theor_list[i])
    cleanedList = [x for x in diff_list if str(x) != 'nan']
    count, bins_count = np.histogram(cleanedList, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.title('Cumulative Density Function(CDF) of Positioning error in NLOS')
    plt.xlabel('Localization Error(m)')
    plt.ylabel('Probability')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    #theor_los,exp_los = getdataLOS() ## Function returns theoretical and experiment Y_coordinates as a list
    #data_LOS = parsedataLOS()##Function to return the LOS data's coordinates as tuple w/ theor_first
    #rangerror_LOS(data_LOS)
    #hist_LOS(data_LOS)
    #range_errorLOS(data_LOS)
    #cdf_dataLOS(data_LOS)
    #data_NLOS = parsedataNLOS()##Function to return the NLOS data coordinates as List of tuples w/theoretical first
    #rangeerrorNLOS(data_NLOS)##Mean error of NLOS data
    #hist_NLOS(data_NLOS)##histogram of NLOS data
    #range_errorNLOS(data_NLOS)##range error of NLOS data
    #cdfNLOS_data(data_NLOS)
    data_KNLOS = parsedataKNLOS()##Function to return the KNLOS data; then tuples of obs vs predicted_pos in 2d first tuple is theoretical
    listdata = tuple2list(data_KNLOS)
    finalKNLOS = finalKNLOSdata(listdata)
    #mean_errorKNLOS(finalKNLOS)
    hist_KNLOS(finalKNLOS)
    #range_errorKNLOS(finalKNLOS)
    #cdfKNLOS_data(finalKNLOS)
