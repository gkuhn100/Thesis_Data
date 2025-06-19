## The objective of this code is to read in all the relevant data from the decawave experiments
## Perform some
##
import matplotlib.pyplot
import matplotlib.pyplot as plt
import pandas as pd
import statistics
import matplotlib.ticker as tck
import numpy as np
import seaborn as sns
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
    x_coord_theor_list = [] ## an unpacked list of each X_ideal_measurement
    y_coord_theor_list = [] ## an unpacked list of each Y_ideal_measurement
    XY_coord_theor_list = [] ## an unpacked list of each coord_ideal_measurement
    XY_coord_real_list = [] ## an unpacked list of each coord_true_measurement
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
        XY_coord_real_list.append(x_real)
        XY_coord_real_list.append(y_real)
    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(float(y_theor))
        XY_coord_theor_list.append(float(x_theor))
        XY_coord_theor_list.append(float(y_theor))

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

    #fig,(ax0,ax1) = plt.subplots(1,2)
    #ax0.hist(diff_y_list, bins = 20, range = (-1,1), color = 'blue', edgecolor = 'black')
    #ax0.set_title("Mean Error LOS(m) X coordinates")
    #ax0.set(xlabel='Mean Error(m)',ylabel='Occurences')
    #ax1.hist(diff_y_list,bins = 20, color = 'red', edgecolor = 'black')
    #ax1.set_title("Mean Error LOS(m) Y coordinates")
    #ax1.set(xlabel='Mean Error(m)',ylabel='Occurences')
    #fig, axes = plt.subplots(1,2)
    #plt.hist(diff_y_list, bins = 20, range = (-1,1), color = 'blue', edgecolor = 'black')
    #plt.xlabel('Measured Error(m) in Y')
    #plt.ylabel('Frequency')
    #plt.title('Measured Error(m) of Decawave')


    plt.hist(diff_y_list,bins=20, color = 'blue', edgecolor = 'black')
    plt.xlabel('Error (m)')
    plt.ylabel('Frequency')
    plt.title("Frequency of Errors in (m) in LOS scenario")
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
    XY_coord_theor_list = [] ## an unpacked list of each coord_ideal_measurement
    XY_coord_real_list = [] ## an unpacked list of each coord_true_measurement
    XY_diff_list = [] ##A list of the different between the measured versus theoretical coordinate measurements

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
        XY_coord_real_list.append(x_real)
        XY_coord_real_list.append(y_real)

    for tuple in data_theor:
        th+=1
        x_theor,y_theor = tuple
        x_coord_theor_list.append(x_theor)
        y_coord_theor_list.append(y_theor)
        XY_coord_theor_list.append(x_theor)
        XY_coord_theor_list.append(y_theor)

    for i in range(len(x_coord_theor_list)):
        diff_x_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        diff_y_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))
        XY_diff_list.append(x_coord_real_list[i] - float(x_coord_theor_list[i]))
        XY_diff_list.append(y_coord_real_list[i] - float(y_coord_theor_list[i]))

    ## Meant to calculate the errors and standard deviations of the errors for the table, using only the Y_error

    meanLOS = statistics.mean(diff_y_list)
    minLOS = min(diff_y_list)
    maxLOS = max(diff_y_list)
    stdLOS = statistics.stdev(diff_y_list)

    #print("For Decawave in a LOS setting the mean error is {0}, and standard deviation is {1}".format(meanLOS,stdLOS))
    print("For Decawave in a LOS setting the min error is {0}, and max is {1}".format(minLOS,maxLOS))

    error_3 = diff_y_list[:132]## A tuple of every range error from
    error_4 = diff_y_list[132:208]## A tuple of every range error from
    error_5 = diff_y_list[208:]## A tuple of every range error from
    error_6 = diff_x_list[0:132]
    error_7 = diff_x_list[132:208]
    error_8 = diff_x_list[208:]

    #error_3 = error_3 + error_6
    #error_4 = error_4 + error_7
    #error_5 = error_5 + error_8

    st3 =statistics.stdev(error_3)
    st4  = statistics.stdev(error_4)
    st5 = statistics.stdev(error_5)

    ranges = ['0-3', '3.0 - 4.5', '4.5 - 5.5']
    stds = [st3, st4, st5]
    plt.bar(ranges,stds, color = 'green')
    plt.xlabel("Range Intervals (m) ")
    plt.ylabel('Standard Deviation (m)')
    plt.title("Standard Deviation of DecaWave positioning errors in LOS")
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
    plt.title('Cumulative Density Function(CDF) of positioning error in LOS')
    plt.xlabel('Localization Error (m)')
    plt.ylabel('Cumulative Error Distribution')
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
    This function takes as input the nested list KNLOS_data and creates 3 columns in an excel notebook;
    theoertical, observed, and updated. Each represent the Decawave.
    :param KNLOS_data: A P*M list of list with each item containing either the theoretical pos or the
            obs and updated position as a 2D state
    :return: N/A ~ Will write to an excel file
    """
    data_real =  [] ## a list of tuples of real tag measurements in 2D
    data_theor = [] ## a list of tuples of theoretical tag measurements in 2D
    diff_list_obs = [] ## A list containing the differences between theoretical and real measurements
    diff_list_upd = []
    obs_pos_list = []
    upd_state_list = []
    theor_list = [] ## The list of the theoretical position of the tag node; X then Y
    final_obs_list = []## The list of the observed position of the tag node; X then Y
    final_upd_state_list = [] ##The list of the updated position of the tag node; X then Y

    ## Go through the KNLOS data and create two lists, one of theoretical and one of real
    for tag_pos in KNLOS_data:##The total number of positions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append(tag_pos[meas])## Real Data
            data_theor.append(tag_pos[0])## Theoretical Data

    ##Create the list of observed data as a two-dimensional list, this is parsing portion for observed position
    for item in range(len(data_real)):
        data_obs = data_real[item][0]
        data_obs_str = data_obs.replace("[", "")
        data_obs_str = data_obs_str.replace(']', '')
        data_no_c = data_obs_str.replace(',', '')
        data_obs_list = data_no_c.split()
        obs_pos_list.append(data_obs_list)

    ##Create the list of Updated state data as a two-dimensional list, this is parsing portion for Updated State
    for item in range(len(data_real)):
        data_upd = data_real[item][1]
        data_upd_str = data_upd.replace("[", "")
        data_upd_str = data_upd_str.replace(']', '')
        data_no_c = data_upd_str.replace(',', '')
        data_upd_list = data_no_c.split()
        upd_state_list.append(data_upd_list)

    ## Unpack the X and Y coordinates from the list, both theor and observed
    for place, item in enumerate(obs_pos_list):
        X_obs,Y_obs =  obs_pos_list[place]
        X_theor,Y_theor = data_theor[place]
        theor_list.append(X_theor)
        theor_list.append(Y_theor)
        final_obs_list.append(float(X_obs))
        final_obs_list.append(float(Y_obs))

    ## Unpack X and coordinates from update_state_list
    for place, item in enumerate(upd_state_list):
        X_upd_S,Y_upd_S =  upd_state_list[place]
        final_upd_state_list.append(float(X_upd_S))
        final_upd_state_list.append(float(Y_upd_S))

    ## Create the Dataframe and make the excel datasheet
    df = pd.DataFrame({'Theoretical Measurements': theor_list, 'Observed Measurements': final_obs_list, 'Updated State': final_upd_state_list})
    df.to_excel('Mean_Erorr_KNLOS.xlsx', sheet_name='sheet1', index=False)

def hist_KNLOS(KNLOS_data):
    """
    This function receieves as input the KNLOS_data and creates and displays two histograms, one of the observed
    position erros and the other of the Updated State
    :param KNLOS_data: A P*M list of list with each item containing either the theoretical pos or the
            obs and updated position as a 2D state
    :return: N/A
    """
    data_real =  [] ## a list of tuples of real tag measurements in 2D
    data_theor = [] ## a list of tuples of theoretical tag measurements in 2D
    diff_list_obs = [] ## A list containing the differences between theoretical and real measurements
    diff_list_upd = []
    obs_pos_list = []
    upd_state_list = []
    theor_list = [] ## The list of the theoretical position of the tag node; X then Y
    final_obs_list = []## The list of the observed position of the tag node; X then Y
    final_upd_state_list = [] ##The list of the updated position of the tag node; X then Y

    ## Go through the KNLOS data and create two lists, one of theoretical and one of Real
    for tag_pos in KNLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append(tag_pos[meas])## Real Data
            data_theor.append(tag_pos[0])## Theoretical Data

    ##Create the list of observed data as a two-dimensional list this is parsing portion for observed
    for item in range(len(data_real)):
        data_obs = data_real[item][0]
        data_obs_str = data_obs.replace("[", "")
        data_obs_str = data_obs_str.replace(']', '')
        data_no_c = data_obs_str.replace(',', '')
        data_obs_list = data_no_c.split()
        obs_pos_list.append(data_obs_list)

    ##Create the list of Updated state data as a two-dimensional list this is parsing portion for Updated State
    for item in range(len(data_real)):
        data_upd = data_real[item][1]
        data_upd_str = data_upd.replace("[", "")
        data_upd_str = data_upd_str.replace(']', '')
        data_no_c = data_upd_str.replace(',', '')
        data_upd_list = data_no_c.split()
        upd_state_list.append(data_upd_list)

    ## Unpack the X and Y coordinates from the list, both theor and observed
    for place, item in enumerate(obs_pos_list):
        X_obs,Y_obs =  obs_pos_list[place]
        X_theor,Y_theor = data_theor[place]
        theor_list.append(X_theor)
        theor_list.append(Y_theor)
        final_obs_list.append(float(X_obs))
        final_obs_list.append(float(Y_obs))

## Unpack X and coordinates from update_state_list
    for place, item in enumerate(upd_state_list):
        X_upd_S,Y_upd_S =  upd_state_list[place]
        final_upd_state_list.append(float(X_upd_S))
        final_upd_state_list.append(float(Y_upd_S))

    ## Create differences between the observed versus theor
    for i in range(len(theor_list)):
        diff_list_obs.append(final_obs_list[i] - theor_list[i])

    ## Create differences between the observed versus theor
    for i in range(len(theor_list)):
        diff_list_upd.append(final_upd_state_list[i] - theor_list[i])

    ## Histogram Stuff
    plt.hist(diff_list_obs,bins=20, color = 'blue', edgecolor = 'black')
    plt.xlabel('Error (m)')
    plt.ylabel('Frequency')
    plt.title("Frequency of Errors(m) of Updated State of Decawave in NLOS scenario")
    plt.show()
    return()

def range_errorKNLOS(KNLOS_data):
    """
    The objective of this function is to display the standard deviation of errors across different ranges; short,middle,long
    :param NLOS_data: a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return: N/A
    """
    data_real =  [] ## a list of (2d)list of strings of real tag measurements in 2D
    data_theor = [] ## a list of tuples of theoretical tag measurements in 2D
    obs_pos_list = []##A list of the observed positions of the
    upd_state_list = []##A list of the Updated Positioon
    theor_list = [] ## The list of the theoretical position of the tag node; X then Y
    final_obs_list = []## The list of the observed position of the tag node; X then Y
    final_upd_state_list = [] ##The list of the updated position of the tag node; X then Y
    diff_list_obs = [] ## A list containing the differences between theoretical and real measurements; X then Y)
    diff_list_upd = []## A list containing the differences between the updated state and theoretical; X then Y)

    short_error_obs = []## Error of Observed Position of Decawave when placed at GT posititon from 0-3m
    med_error_obs = []## Error of Observed Position of Decawave when placed at GT posititon from 3.5-5.5m
    long_error_obs = []## Error of Observed Position of Decawave when placed at GT position greater than 5.5m

    short_error_up = []## Error of Updated State of Decawave when placed at GT posititon from 0-3m
    med_error_up = []## Error of Updated State of Decawave when placed at GT posititon from 3.5-6m
    long_error_up = []## Error of Updated State of Decawave when placed at GT position greater than 5.5m

    ## Go through the KNLOS data and create two lists, one of theoretical and one of Real
    for tag_pos in KNLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append(tag_pos[meas])## Real Data
            data_theor.append(tag_pos[0])## Theoretical Data

    ##Create the list of observed data as a two-dimensional list this is parsing portion for observed
    for item in range(len(data_real)):
        data_obs = data_real[item][0]
        data_obs_str = data_obs.replace("[", "")
        data_obs_str = data_obs_str.replace(']', '')
        data_no_c = data_obs_str.replace(',', '')
        data_obs_list = data_no_c.split()
        obs_pos_list.append(data_obs_list)

    ##Create the list of Updated state data as a two-dimensional list this is parsing portion for Updated State
    for item in range(len(data_real)):
        data_upd = data_real[item][1]
        data_upd_str = data_upd.replace("[", "")
        data_upd_str = data_upd_str.replace(']', '')
        data_no_c = data_upd_str.replace(',', '')
        data_upd_list = data_no_c.split()
        upd_state_list.append(data_upd_list)

    ## Unpack the X and Y coordinates from the list, both theor and observed (it will be X then Y Coordiante)
    for place, item in enumerate(obs_pos_list):
        X_obs,Y_obs =  obs_pos_list[place]
        X_theor,Y_theor = data_theor[place]
        theor_list.append(X_theor)
        theor_list.append(Y_theor)
        final_obs_list.append(float(X_obs))
        final_obs_list.append(float(Y_obs))


    ## Unpack X and coordinates from update_state_list (it will be X then Y Coordiante)
    for place, item in enumerate(upd_state_list):
        X_upd_S,Y_upd_S =  upd_state_list[place]
        final_upd_state_list.append(float(X_upd_S))
        final_upd_state_list.append(float(Y_upd_S))

    ## Create differences between the observed position versus theor
    for i in range(len(theor_list)):
        diff_list_obs.append(final_obs_list[i] - theor_list[i])

    ## Create differences between the updated state versus theor
    for i in range(len(theor_list)):
        diff_list_upd.append(final_upd_state_list[i] - theor_list[i])

#Calculate The relevant statistical data
    meanNLOS_obs = statistics.mean(diff_list_obs)
    stdNLOS_obs= statistics.stdev(diff_list_obs)
    meanNLOS_upd = statistics.mean(diff_list_upd)
    stdNLOS_upd = statistics.stdev(diff_list_upd)

    print("For Decawave in a NLOS setting the observed mean error is {0}, and standard deviation is {1}".format(meanNLOS_obs,stdNLOS_obs))
    print("For Decawave in a NLOS setting the updated mean error is {0}, and standard deviation is {1}".format(meanNLOS_upd,stdNLOS_upd))

    x_theor =  theor_list[0::2]##Theoertical X Coordinates
    y_theor =  theor_list[1::2]##Theoretical Y Coordinates
    x_obs   =  final_obs_list[0::2]##Observed X coordinates
    y_obs   =  final_obs_list[1::2]##Observed Y coordinates
    x_up    =  final_upd_state_list[0::2]##Updated X Coordinates
    y_up    =  final_upd_state_list[1::2]##Updated Y Coordinates

    diff_X_obs = []##The list of differences between the X coordiantes observed and theoretical Values
    diff_Y_obs = []##The list of differences between the Y coordiantes observed and theoretical Values
    diff_X_upd = []##The list of differences between the X coordiantes updated and theoretical Values
    diff_Y_upd = []##The list of differences between the Y coordiantes updated and theoretical Values

##At long last the differences between the two measurements
    for i in range(len(x_theor)):
        diff_X_obs.append(x_obs[i] - x_theor[i])
        diff_Y_obs.append(y_obs[i] - y_theor[i])
        diff_X_upd.append(x_up[i] - x_theor[i])
        diff_Y_upd.append(y_up[i] - y_theor[i])

    #for place, item in enumerate(x_theor):
    #    print(place, '', item)

##Get the Observed Errors based on the theoeretical distances; will include both X and Y
    short_error_obs.append(diff_X_obs[0:598])
    med_error_obs.append(diff_X_obs[598:676])
    long_error_obs.append(diff_X_obs[676::])

    short_error_obs.append(diff_Y_obs[0:39])
    short_error_obs.append(diff_Y_obs[136:175])
    short_error_obs.append(diff_Y_obs[243:355])
    short_error_obs.append(diff_Y_obs[559:715])

    med_error_obs.append(diff_Y_obs[355:457])
    med_error_obs.append(diff_Y_obs[715:793])

    long_error_obs.append(diff_Y_obs[39:136])
    long_error_obs.append(diff_Y_obs[175:243])
    long_error_obs.append(diff_Y_obs[457:550])
    long_error_obs.append(diff_Y_obs[793::])

    ##Get the Updated State Errors based on the theoeretical distances; will include both X and Y
    short_error_up.append(diff_X_upd[0:598])
    med_error_up.append(diff_X_upd[598:676])
    long_error_up.append(diff_X_upd[676::])

    short_error_up.append(diff_Y_upd[0:39])
    short_error_up.append(diff_Y_upd[136:175])
    short_error_up.append(diff_Y_upd[243:355])
    short_error_up.append(diff_Y_upd[559:715])

    med_error_up.append(diff_Y_upd[355:457])
    med_error_up.append(diff_Y_upd[715:793])

    long_error_up.append(diff_Y_upd[39:136])
    long_error_up.append(diff_Y_upd[175:243])
    long_error_up.append(diff_Y_upd[457:550])
    long_error_up.append(diff_Y_upd[793::])

    ##There is a formatting problem for the STD function; wont take a list as an argument, this removes it
    error_obs_short = short_error_obs[0] + short_error_obs[1] + short_error_obs[2] + short_error_obs[3] + short_error_obs[4]
    error_obs_med = med_error_obs[0] + med_error_obs[1] + med_error_obs[2]
    error_obs_long = long_error_obs[0] + long_error_obs[1] + long_error_obs[2] + long_error_obs[3] + long_error_obs[4]

    error_up_short = short_error_up[0] + short_error_up[1] + short_error_up[2] + short_error_up[3] + short_error_up[4]
    error_up_med = med_error_up[0] + med_error_up[1] + med_error_up[2]
    error_up_long = long_error_up[0] + long_error_up[1] + long_error_up[2] + long_error_up[3] + long_error_up[4]

##Calculate Standard Deviation
    std_short_obs = statistics.stdev(error_obs_short)
    std_med_obs   = statistics.stdev(error_obs_med)
    std_lon_obs   = statistics.stdev(error_obs_long)

    std_short_up = statistics.stdev(error_up_short)
    std_med_up   = statistics.stdev(error_up_med)
    std_lon_up   = statistics.stdev(error_up_long)


    #print("For Decawave in a LOS setting the mean error is {0}, and standard deviation is {1}".format(meanLOS,stdLOS))

## Bar Graph Plotting time
    ranges = ['0-3', '3.5 - 5.0', '5.5 - 8.5']
    stds_obs = [std_short_obs, std_med_obs, std_lon_obs]
    std_upd = [std_short_up, std_med_up, std_lon_up]

    w, x = 0.4, np.arange(len(ranges))
    fig, ax = plt.subplots()
    ax.bar(x - w/2, stds_obs, width=w, label='Observesd')
    ax.bar(x + w/2, std_upd, width=w, label='Sensor Fusion ')

    ax.set_xticks(x)
    ax.set_xticklabels(ranges)
    ax.set_ylabel('Standard Deviation of range error')
    ax.set_title('Ranges')
    ax.legend()
    plt.show()

def cdfKNLOS_data(KNLOS_data):
    """
    This function displays the Culmative Distribution of both the obsrved and updated state errors in a NLOS environment
    :param KNLOS_data:a p*m list of tuples, with  each measurement being a 2D coordinate; and first item always being theoretical
    :return:N/A Kinda a graph of the CDF
    """
    data_real =  [] ## a list of (x2)list of real tag measuremnets in 2D
    data_theor = [] ## a list of tuples of theoretical tag measuremnets in 2D
    theor_list = [] ## list of floats of the theoretical values
    obs_pos_list = []## A parsed list of the obsered position
    upd_state_list = []## A parsed list of the updated state
    final_obs_list = []## The final unpacked and parsed list of all values of observed values; X the nY
    final_upd_state_list = []##The final unpacked and parsed list of all values of updated state; X then Y
    diff_list_obs = [] ## A list containing the differences between theoretical and real measurements
    diff_list_upd = []##A list containing the differences between theoretical and real measurements

    ## Go through the KNLOS data and create two lists, one of theoretical and one of Real
    for tag_pos in KNLOS_data:##The total number of postions the tag is place at each one
        for meas in range(1,len(tag_pos),1):##goes through each measurement line by line
            data_real.append(tag_pos[meas])## Real Data
            data_theor.append(tag_pos[0])## Theoretical Data

    ##Create the list of observed data as a two-dimensional list this is parsing portion for observed
    for item in range(len(data_real)):
        data_obs = data_real[item][0]
        data_obs_str = data_obs.replace("[", "")
        data_obs_str = data_obs_str.replace(']', '')
        data_no_c = data_obs_str.replace(',', '')
        data_obs_list = data_no_c.split()
        obs_pos_list.append(data_obs_list)

    ##Create the list of Updated state data as a two-dimensional list this is parsing portion for Updated State
    for item in range(len(data_real)):
        data_upd = data_real[item][1]
        data_upd_str = data_upd.replace("[", "")
        data_upd_str = data_upd_str.replace(']', '')
        data_no_c = data_upd_str.replace(',', '')
        data_upd_list = data_no_c.split()
        upd_state_list.append(data_upd_list)

    ## Unpack the X and Y coordinates from the list, both theor and observed
    for place, item in enumerate(obs_pos_list):
        X_obs,Y_obs =  obs_pos_list[place]
        X_theor,Y_theor = data_theor[place]
        theor_list.append(X_theor)
        theor_list.append(Y_theor)
        final_obs_list.append(float(X_obs))
        final_obs_list.append(float(Y_obs))

    ## Unpack X and Y coordinates from update_state_list
    for place, item in enumerate(upd_state_list):
        X_upd_S,Y_upd_S =  upd_state_list[place]
        final_upd_state_list.append(float(X_upd_S))
        final_upd_state_list.append(float(Y_upd_S))

    ## Create differences between the observed versus theor
    for i in range(len(theor_list)):
        diff_list_obs.append(final_obs_list[i] - theor_list[i])

    ## Create differences between the updated versus theor
    for i in range(len(theor_list)):
        diff_list_upd.append(final_upd_state_list[i] - theor_list[i])

    cleanedListUpd = [x for x in diff_list_upd if str(x) != 'nan']
    count_upd, bins_count_upd = np.histogram(cleanedListUpd, bins=10)
    pdf_upd = count_upd / sum(count_upd)
    cdf_upd = np.cumsum(pdf_upd)

    cleanedListObs = [x for x in diff_list_obs if str(x) != 'nan']
    count_obs, bins_count_obs = np.histogram(cleanedListObs, bins=10)
    pdf_obs = count_obs / sum(count_obs)
    cdf_obs = np.cumsum(pdf_obs)

    plt.plot(bins_count_upd[1:], cdf_upd, label="CDF Upd")
    plt.plot(bins_count_obs[1:], cdf_obs, label="CDF obs")
    plt.title('Cumulative Density Function(CDF) of Positioning error in KNLOS ')
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
    data_KNLOS = parsedataKNLOS()##Function to return the KNLOS data; then tuples of obs vs predicted_pos in 2d first tuple is theoretical
    listdata = tuple2list(data_KNLOS)
    finalKNLOS = finalKNLOSdata(listdata)
    #mean_errorKNLOS(finalKNLOS)
    #hist_KNLOS(finalKNLOS)
    #range_errorKNLOS(finalKNLOS)
    #cdfKNLOS_data(finalKNLOS)




