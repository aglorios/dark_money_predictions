
# coding: utf-8

import pandas as pd
import glob

paths = glob.glob("Non_Candidate_files_2012/*")

advertiser_files= []
for path in paths:
    contents = open(path).read()
    contents = contents.decode("ascii", "ignore")
    contents = contents.lower()
    
    my_data = {}
    filename = path[20:] 
    df_name = filename[:-4] + '_df'
    my_data[df_name] = pd.io.excel.read_excel(path, sheetname=0, header=7)
    advertiser_files.append(my_data)

print len(advertiser_files)


# In[3]:

import re
advertiser_file_list = []
advertiser_files_2012_df = pd.DataFrame()
for advertiser_file in advertiser_files:
    for key, value in advertiser_file.iteritems():
        temp = [key,value]
        advertiser_file_list.append(temp)
        advertiser_files_2012_df = pd.DataFrame(advertiser_file_list)


# In[4]:

advertiser_files_2012_df.head()


# In[5]:

tuple_file = tuple(map(tuple, advertiser_files_2012_df.values))


# In[6]:

tuple_file[4][1].ix[2]


# In[7]:
list_test = []
for df_name, df_content in tuple_file:
    df_content['advertiser_name'] = df_name
    for index, row in df_content.iterrows():
        row_list = row.tolist()
        list_test.append(row_list)


# In[8]:

list_test


# In[9]:

non_candidate_2012_df = pd.DataFrame(list_test, columns = ['Mod_Code', 'Buy_Line', 'Day/Time', 'Length', 'Rate', 'Starting_Date', 'Ending_Date', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Program_Name', 'Rating_RA35+', 'Rep:_RA35+', 'Last_Activity', 'Last_Mod/Rev', 'Advertiser_Name'])


# In[10]:

non_candidate_2012_df


# In[11]:

none_advertiser_2012_df = non_candidate_2012_df[non_candidate_2012_df['Advertiser_Name'].isnull()]


none_advertiser_2012_df['Advertiser_Name'] = none_advertiser_2012_df['Last_Mod/Rev']


# In[17]:

none_advertiser_2012_df['Last_Mod/Rev'] = none_advertiser_2012_df['Last_Activity']


# In[18]:

none_advertiser_2012_df['Last_Activity'] = none_advertiser_2012_df['Rep:_RA35+']


# In[19]:

none_advertiser_2012_df['Rep:_RA35+'] = 0.0



# In[21]:

non_candidate_2012_df[non_candidate_2012_df['Advertiser_Name'].isnull()] = none_advertiser_2012_df


# In[22]:

non_candidate_2012_df['Rep:_RA35+'].value_counts()


# In[23]:

len(non_candidate_2012_df)


# In[24]:

import re
def clean_totals(row_df):
    temp_string = str(row_df)
    total_sub = re.sub(r"(.*Total )(.*)$", r"", temp_string)
    if total_sub:
        return total_sub
        return temp_string


# In[25]:

clean_totals("   Total babe in the place                  .lclcijef9871209  dkdk")


# In[26]:

import re
for index, row in non_candidate_2012_df.iterrows():
    temp_string = str(row['Day/Time'])
    re.sub(r"(.*Total )(.*)$", r" ", temp_string)
    print temp_string


# In[27]:

non_candidate_2012_df[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Total )(.*)$")==True]


# In[28]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Total )(.*)$")==True])


# In[29]:

non_candidate_2012_df[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Total )(.*)$")==True]


# In[30]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Monthly )(.*)$")==True])


# In[31]:

non_candidate_2012_df[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Monthly )(.*)$")==True]


# In[32]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Contract )(.*)$")==True])


# In[33]:

non_candidate_2012_df[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Contract )(.*)$")==True]


# In[34]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Buy_Line'].str.contains(r"(.*##)(.*)$")==True])


# In[35]:

non_candidate_2012_df[non_candidate_2012_df['Day/Time'].str.contains(r"(.*##)(.*)$")==True]



# In[40]:

non_candidate_2012_df['Day/Time']


# In[41]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Day/Time'].isnull()])


# In[42]:

non_candidate_2012_df['Program_Name'].value_counts()


# In[43]:

import re
def split_day(row_df):
    temp_string = str(row_df)
    match = re.match(r"(^.*)(/)(.*)", temp_string)
    if match:
        return match.group(1)


# In[44]:

split_day('Sun-Mon/7')


# In[45]:

import re
def split_time(row_df):
    temp_string = str(row_df)
    match = re.match(r"(^.*)(/)(.*)", temp_string)
    if match:
        return match.group(3)


# In[46]:

split_time('Sun-Mon/7')


# In[47]:

non_candidate_2012_df['Day'] = non_candidate_2012_df['Day/Time'].apply(split_day)


# In[48]:

non_candidate_2012_df['Time'] = non_candidate_2012_df['Day/Time'].apply(split_time)


# In[49]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Buy_Line'].str.contains(r"(.*##)(.*)$")==True])


# In[50]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Day'].isnull()==True])


# In[51]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Day/Time'].str.contains(r"(.*Order)(.*)$")==True])


# In[52]:

non_candidate_2012_df = non_candidate_2012_df.drop(non_candidate_2012_df.index[non_candidate_2012_df['Day/Time'].str.contains(r"(.*This)(.*)$")==True])


# In[53]:

len(non_candidate_2012_df)


# In[54]:

non_candidate_2012_df['Day'] = non_candidate_2012_df['Day/Time'].apply(split_day)


# In[55]:

non_candidate_2012_df['Time'] = non_candidate_2012_df['Day/Time'].apply(split_time)


# In[56]:

non_candidate_2012_df['Day'].value_counts()


# In[57]:

def monday(row_df):
    mon = re.match(r"(.*)(M)(.*)", row_df)
    if mon:
        return 1
    else:
        return 0
    
def tues(row_df):
    tues = re.match(r"(.*)(Tu)(.*)", row_df)
    if tues:
        return 1
    else:
        return 0
    
def wed(row_df):
    wed = re.match(r"(.*)(W)(.*)", row_df)
    if wed:
        return 1
    else:
        return 0

def thursday(row_df):
    thurs = re.match(r"(.*)(Th)(.*)", row_df)
    if thurs:
        return 1
    else:
        return 0

def friday(row_df):
    fri = re.match(r"(.*)(F)(.*)", row_df)
    if fri:
        return 1
    else:
        return 0
    
def saturday(row_df):
    sat = re.match(r"(.*)(Sa)(.*)", row_df)
    if sat:
        return 1
    else:
        return 0
    
def sunday(row_df):
    sun = re.match(r"(.*)(Su)(.*)", row_df)
    if sun:
        return 1
    else:
        return 0
    


# In[58]:

non_candidate_2012_df['Monday'] = non_candidate_2012_df['Day'].apply(monday)
non_candidate_2012_df['Tuesday'] = non_candidate_2012_df['Day'].apply(tues)
non_candidate_2012_df['Wednesday'] = non_candidate_2012_df['Day'].apply(wed)
non_candidate_2012_df['Thursday'] = non_candidate_2012_df['Day'].apply(thursday)
non_candidate_2012_df['Friday'] = non_candidate_2012_df['Day'].apply(friday)
non_candidate_2012_df['Saturday'] = non_candidate_2012_df['Day'].apply(saturday)
non_candidate_2012_df['Sunday'] = non_candidate_2012_df['Day'].apply(sunday)


# In[59]:

def time(row_df):
    match = re.match(r"(.*)([APN])", row_df)
    if match:
        return match.group(1)


# In[60]:

time('9-10A')


# In[61]:

non_candidate_2012_df['Time_Clean'] = non_candidate_2012_df['Time'].apply(time)


# In[62]:

non_candidate_2012_df


# In[63]:

non_candidate_2012_df['Time_Clean'].value_counts()


# In[64]:

def start_time_hyphen(row_df):
    match = re.match(r"(.*)(-)(.*)", row_df)
    if match:
        return match.group(1)
    
def end_time_hyphen(row_df):
    match = re.match(r"(.*)(-)(.*)", row_df)
    if match:
        return match.group(3)
    
def start_time(row_df):
    match = re.match(r"(\d*)", row_df)
    if match:
        return match.group(0)


# In[65]:

non_candidate_2012_df


# In[66]:

non_candidate_2012_df['Start_Time'] = non_candidate_2012_df['Time_Clean'].apply(start_time_hyphen)
non_candidate_2012_df['Start_Time'] = non_candidate_2012_df['Time_Clean'].apply(start_time)
non_candidate_2012_df['End_Time'] = non_candidate_2012_df['Time_Clean'].apply(end_time_hyphen)



# In[68]:

non_candidate_2012_df['End_Time'] = non_candidate_2012_df['End_Time'].replace([None], "00")



# In[71]:

import re
def add_min(row_df):
    if row_df == '1' or row_df == '2':
        return row_df + '0'
    if row_df == '12':
        return '00'
    if row_df == '1205':
        return '05'
    if row_df == '1230':
        return '0030'
    if row_df == '1235':
        return '0035'
    if row_df == '105':
        return '15'
    elif len(row_df) <= 2:
        return row_df + '00'
    else:
        return row_df


# In[72]:

add_min('2')


# In[73]:

add_min('6')


# In[74]:

add_min('666')


# In[79]:

non_candidate_2012_df


# In[80]:

non_candidate_2012_df['Start_Time'] = non_candidate_2012_df['Start_Time'].apply(add_min)
non_candidate_2012_df['End_Time'] = non_candidate_2012_df['End_Time'].apply(add_min)



# In[82]:

non_candidate_2012_df


# In[83]:

def am(row_df):
    match = re.match(r"(.*)(A)", row_df)
    if match:
        return 1
    else:
        return 0
    
def pm(row_df):
    match = re.match(r"(.*)([NP])", row_df)
    if match:
        return 1
    else:
        return 0


# In[84]:

non_candidate_2012_df['AM'] = non_candidate_2012_df['Time'].apply(am)
non_candidate_2012_df['PM'] = non_candidate_2012_df['Time'].apply(pm)


# In[85]:

def change_12(row_df1, row_df2):
    if row_df1 == '1100':
        sub = re.sub('00', '1200', row_df2)
        return sub
    if row_df1 == '1130':
        sub = re.sub('0030', '1230', row_df2)
        return sub
    if row_df1 == '1135':
        sub = re.sub('0035', '1235', row_df2)
        return sub
    else:
        return row_df2
    


# In[86]:

import datetime
import time

def convert_times(dt1, dt2):
    FMT = '%H%M'
    res1 = datetime.datetime(*time.strptime(dt1, FMT)[:6])
    res2 = datetime.datetime(*time.strptime(dt2, FMT)[:6])

    duration = res2 - res1
    return duration
    
# In[87]:

change_12('1135', '1235')


# In[88]:

non_candidate_2012_df['End_Time'] = non_candidate_2012_df.apply(lambda row: change_12(row['Start_Time'], row['End_Time']), axis = 1)


# In[90]:

non_candidate_2012_df['Time'].value_counts()


# In[91]:

non_candidate_2012_df[(non_candidate_2012_df['Start_Time'] == '1100')]


# In[96]:

FMT = '%H%M'
time.strptime('10', FMT)


# In[97]:

FMT = '%H%M'
time.strptime('400', FMT)


# In[98]:

FMT = '%H%M'
time.strptime('20', FMT)


# In[99]:

FMT = '%H%M'
time.strptime('300', FMT)


# In[100]:

FMT = '%H%M'
time.strptime('05', FMT)


# In[101]:

FMT = '%H%M'
time.strptime('105', FMT)


# In[102]:

FMT = '%H%M'
time.strptime('10', FMT)


# In[103]:

FMT = '%H%M'
time.strptime('430', FMT)


# In[104]:

FMT = '%H%M'
time.strptime('0030', FMT)


# In[105]:

non_candidate_2012_df['Duration'] = non_candidate_2012_df.apply(lambda row: convert_times(row['Start_Time'], row['End_Time']), axis = 1)


# In[106]:

non_candidate_2012_df[(non_candidate_2012_df['AM'] == 1) & (non_candidate_2012_df['PM'] == 1)]


# In[107]:

non_candidate_2012_df[non_candidate_2012_df['Duration']<1]['Time_Clean'].value_counts()



time_df = pd.concat([non_candidate_2012_df['End_Time'].value_counts(), non_candidate_2012_df['Start_Time'].value_counts()], axis = 1)

time_df.index


# In[110]:

def twelve(row1, row2):
    match1 = re.match(r"00", row1)
    match2 = re.match(r"1200", row1)
    match3 = re.match(r"00", row2)
    match4 = re.match(r"1200", row2)
    if match1 or match2 or match3 or match4:
        return 1
    else:
        return 0
    
def twelve_thirty(row1, row2):
    match1 = re.match(r"0030", row1)
    match2 = re.match(r"0030", row2)
    match3 = re.match(r"1230", row1)
    match4 = re.match(r"1230", row2)
    if match1 or match2 or match3 or match4:
        return 1
    else:
        return 0
    
def twelve_thirty_five(row1, row2):
    match1 = re.match(r"0035", row1)
    match2 = re.match(r"1235", row2)
    match3 = re.match(r"0035", row1)
    match4 = re.match(r"1235", row2)
    if match1 or match2 or match3 or match4:
        return 1
    else:
        return 0
    
def twelve_o_five(row1, row2):
    match1 = re.match(r"05", row1)
    match2 = re.match(r"05", row2)
    if match1 or match2:
        return 1
    else:
        return 0

def one(row1, row2):
    match1 = re.match(r"10", row1)
    match2 = re.match(r"10", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def ten(row1, row2):
    match1 = re.match(r"1000", row1)
    match2 = re.match(r"1000", row2)
    if match1 or match2:
        return 1
    else:
        return 0

def ten_thirty(row1, row2):
    match1 = re.match(r"1030", row1)
    match2 = re.match(r"1030", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def eleven(row1, row2):
    match1 = re.match(r"1100", row1)
    match2 = re.match(r"1100", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def eleven_thirty(row1, row2):
    match1 = re.match(r"1130", row1)
    match2 = re.match(r"1130", row2)
    if match1 or match2:
        return 1
    else:
        return 0    
    
def eleven_thirty_five(row1, row2):
    match1 = re.match(r"1135", row1)
    match2 = re.match(r"1135", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def one_thirty(row1, row2):
    match1 = re.match(r"130", row1)
    match2 = re.match(r"130", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def one_thirty_five(row1, row2):
    match1 = re.match(r"135", row1)
    match2 = re.match(r"135", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def one_o_five(row1, row2):
    match1 = re.match(r"15", row1)
    match2 = re.match(r"15", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def two(row1, row2):
    match1 = re.match(r"20", row1)
    match2 = re.match(r"20", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def three(row1, row2):
    match1 = re.match(r"300", row1)
    match2 = re.match(r"300", row2)
    if match1 or match2:
        return 1
    else:
        return 0

def three_thirty(row1, row2):
    match1 = re.match(r"330", row1)
    match2 = re.match(r"330", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def four(row1, row2):
    match1 = re.match(r"400", row1)
    match2 = re.match(r"400", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def four_thirty(row1, row2):
    match1 = re.match(r"430", row1)
    match2 = re.match(r"430", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def four_fifty_nine(row1, row2):
    match1 = re.match(r"459", row1)
    match2 = re.match(r"459", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def five(row1, row2):
    match1 = re.match(r"500", row1)
    match2 = re.match(r"500", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def five_thirty(row1, row2):
    match1 = re.match(r"530", row1)
    match2 = re.match(r"530", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def six(row1, row2):
    match1 = re.match(r"600", row1)
    match2 = re.match(r"600", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def six_thirty(row1, row2):
    match1 = re.match(r"630", row1)
    match2 = re.match(r"630", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def seven(row1, row2):
    match1 = re.match(r"700", row1)
    match2 = re.match(r"700", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def seven_thirty(row1, row2):
    match1 = re.match(r"730", row1)
    match2 = re.match(r"730", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def seven_fifty_eight(row1, row2):
    match1 = re.match(r"758", row1)
    match2 = re.match(r"758", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def eight(row1, row2):
    match1 = re.match(r"800", row1)
    match2 = re.match(r"800", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def eight_thirty(row1, row2):
    match1 = re.match(r"830", row1)
    match2 = re.match(r"830", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def nine(row1, row2):
    match1 = re.match(r"900", row1)
    match2 = re.match(r"900", row2)
    if match1 or match2:
        return 1
    else:
        return 0
    
def nine_thirty(row1, row2):
    match1 = re.match(r"930", row1)
    match2 = re.match(r"930", row2)
    if match1 or match2:
        return 1
    else:
        return 0


# In[111]:

def double_day(row1, row2, row3):
    match1 = re.match(r"(.*)(A)(.*)", row3)
    if match1:
        if row1 ==1 and row2 ==1:
            return 1
    match2 = re.match(r"(.*)(P)(.*)", row3)
    if match2:
        if row1 ==1 and row2 ==1:
            return 1
        

# In[112]:

non_candidate_2012_df['10:00'] = non_candidate_2012_df.apply(lambda row: ten(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['10:30'] = non_candidate_2012_df.apply(lambda row: ten_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['11:00'] = non_candidate_2012_df.apply(lambda row: eleven(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['11_AM'] = non_candidate_2012_df.apply(lambda row: double_day(row['AM'], row['PM'], row['Time_Clean']), axis = 1)

non_candidate_2012_df['11_PM'] = non_candidate_2012_df.apply(lambda row: double_day(row['AM'], row['PM'], row['Time_Clean']), axis = 1)

non_candidate_2012_df['11:30'] = non_candidate_2012_df.apply(lambda row: eleven_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['11:35'] = non_candidate_2012_df.apply(lambda row: eleven_thirty_five(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['12:00'] = non_candidate_2012_df.apply(lambda row: twelve(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['12:05'] = non_candidate_2012_df.apply(lambda row: twelve_o_five(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['12:30'] = non_candidate_2012_df.apply(lambda row: twelve_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['12:35'] = non_candidate_2012_df.apply(lambda row: twelve_thirty_five(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['1:00'] = non_candidate_2012_df.apply(lambda row: one(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['1:05'] = non_candidate_2012_df.apply(lambda row: one_o_five(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['1:30'] = non_candidate_2012_df.apply(lambda row: one_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['1:35'] = non_candidate_2012_df.apply(lambda row: one_thirty_five(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['2:00'] = non_candidate_2012_df.apply(lambda row: two(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['3:00'] = non_candidate_2012_df.apply(lambda row: three(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['3:30'] = non_candidate_2012_df.apply(lambda row: three_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['4:00'] = non_candidate_2012_df.apply(lambda row: four(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['4:30'] = non_candidate_2012_df.apply(lambda row: four_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['4:59'] = non_candidate_2012_df.apply(lambda row: four_fifty_nine(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['5:00'] = non_candidate_2012_df.apply(lambda row: five(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['5:30'] = non_candidate_2012_df.apply(lambda row: five_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['6:00'] = non_candidate_2012_df.apply(lambda row: six(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['6:30'] = non_candidate_2012_df.apply(lambda row: six_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['7:00'] = non_candidate_2012_df.apply(lambda row: seven(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['7:30'] = non_candidate_2012_df.apply(lambda row: seven_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['7:58'] = non_candidate_2012_df.apply(lambda row: seven_fifty_eight(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['8:00'] = non_candidate_2012_df.apply(lambda row: eight(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['8:30'] = non_candidate_2012_df.apply(lambda row: eight_thirty(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['9:00'] = non_candidate_2012_df.apply(lambda row: nine(row['Start_Time'], row['End_Time']), axis = 1)

non_candidate_2012_df['9:30'] = non_candidate_2012_df.apply(lambda row: nine_thirty(row['Start_Time'], row['End_Time']), axis = 1)


# In[113]:

non_candidate_2012_df.columns


# In[114]:

import re
def split_length(row_df):
    temp_string = str(row_df)
    match = re.match(r"(^.*)(S)", temp_string)
    if match:
        return match.group(1)


# In[115]:

non_candidate_2012_df['Length_in_Sec'] = non_candidate_2012_df['Length'].apply(split_length)


# In[116]:

non_candidate_2012_df[(non_candidate_2012_df['AM'] == 1) & (non_candidate_2012_df['PM'] == 1)]['Time_Clean'].value_counts()


# In[117]:

non_candidate_2012_df.columns


# In[118]:

non_candidate_2012_df = non_candidate_2012_df[['Advertiser_Name', 'Mod_Code', 'Buy_Line', 'Rate', 'Starting_Date', 'Ending_Date', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Program_Name', 'Rating_RA35+', 'Rep:_RA35+', 'Last_Activity', 'Last_Mod/Rev', 'Length_in_Sec', 'AM', 'PM', 'Duration', '10:00', '10:30', '11:00', '11_AM', '11_PM', '11:30', '11:35', '12:00', '12:05', '12:30', '12:35', '1:00', '1:05', '1:30', '1:35', '2:00', '3:00', '3:30', '4:00', '4:30', '4:59', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '7:58', '8:00', u'8:30', '9:00', '9:30']]


# In[119]:

non_candidate_2012_df['Advertiser_Name'].value_counts()


# In[120]:

def advertiser(row_df):
    match = re.match(r"(^.*\/)(.*)([\. ])(\()(.*)(\))(_df)", row_df)
    if match:
        return match.group(2)


# In[121]:

def contract(row_df):
    match = re.match(r"(^.*\/)(.*)([\. ])(\()(.*)(\))(_df)", row_df)
    if match:
        return match.group(5)


# In[122]:

advertiser('2012/MDSCC-HD91.3 (13517054721474)_df')


# In[123]:

non_candidate_2012_df['Advertiser'] = non_candidate_2012_df['Advertiser_Name'].apply(advertiser)


# In[124]:

non_candidate_2012_df['Contract'] = non_candidate_2012_df['Advertiser_Name'].apply(contract)


# In[125]:

non_candidate_2012_df.columns


# In[126]:

non_candidate_2012_df = non_candidate_2012_df[['Advertiser', 'Contract', 'Buy_Line', 'Rate', 'Starting_Date', 'Ending_Date', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Program_Name', 'Rating_RA35+', 'Rep:_RA35+', 'Last_Activity', 'Last_Mod/Rev', 'Length_in_Sec', 'AM', 'PM', 'Duration', '10:00', '10:30', '11:00', '11_AM', '11_PM', '11:30', '11:35', '12:00', '12:05', '12:30', '12:35', '1:00', '1:05', '1:30', '1:35', '2:00', '3:00', '3:30', '4:00', '4:30', '4:59', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '7:58', '8:00', '8:30', '9:00', '9:30']]


# In[127]:

non_candidate_2012_df['Advertiser'].value_counts()


# In[128]:

def advertiser2(row_df):
    return row_df[:-2]


# In[129]:

non_candidate_2012_df['Advertiser_Clean'] = non_candidate_2012_df['Advertiser'].apply(advertiser2)


# In[130]:

non_candidate_2012_df = non_candidate_2012_df[['Advertiser', 'Advertiser_Clean', 'Contract', 'Buy_Line', 'Rate', 'Starting_Date', 'Ending_Date', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Program_Name', 'Rating_RA35+', 'Rep:_RA35+', 'Last_Activity', 'Last_Mod/Rev', 'Length_in_Sec', 'AM', 'PM', 'Duration', '10:00', '10:30', '11:00', '11_AM', '11_PM', '11:30', '11:35', '12:00', '12:05', '12:30', '12:35', '1:00', '1:05', '1:30', '1:35', '2:00', '3:00', '3:30', '4:00', '4:30', '4:59', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '7:58', '8:00', '8:30', '9:00', '9:30']]


# In[131]:

non_candidate_2012_df['Advertiser_Clean'].value_counts()


# In[132]:

non_candidate_2012_df.columns


# In[133]:

shows_df = pd.DataFrame(non_candidate_2012_df['Program_Name'].value_counts())


# In[134]:

#shows_df.to_csv('/home/admin/shows.csv')


# In[135]:

shows_df


# In[136]:

non_candidate_2012_df['Program_Name'].value_counts()


# In[137]:

def advertiser3(row_df):
    match1 = re.match(r"(.*)(CARE FOR MICHIG.*)(.*)", str(row_df))
    if match1:
        return 'CARE FOR MICHIGAN'
    
    match2 = re.match(r"(.*)(CARE OF MICHIG.*)(.*)", str(row_df))
    if match2:
        return 'CARE FOR MICHIGAN'
    
    match3 = re.match(r"(.*)(CIT 4.*)(.*)", str(row_df))
    if match3:
        return 'CIT 4 AFF QUALITY HOMECARE'
    
    match4 = re.match(r"(.*)(CIT FOR AFFORD.*)(.*)", str(row_df))
    if match4:
        return 'CIT 4 AFF QUALITY HOMECARE'
    
    match5 = re.match(r"(.*)(CITIZEN PROTECT.*)(.*)", str(row_df))
    if match5:
        return 'CITIZEN PROTECT MI'
    
    match6 = re.match(r"(.*)(Citizen Protect.*)(.*)", str(row_df))
    if match6:
        return 'CITIZEN PROTECT MI'
    
    match7 = re.match(r"(.*)(DETROIT BRI.*)(.*)", str(row_df))
    if match7:
        return 'DETROIT INTERNATIONAL BRIDGE CO'
    
    match8 = re.match(r"(.*)(Detroit Bri.*)(.*)", str(row_df))
    if match8:
        return 'DETROIT BRIDGE'
    
    match9 = re.match(r"(.*)(DIBC.*)(.*)", str(row_df))
    if match9:
        return 'DETROIT INTERNATIONAL BRIDGE CO'
    
    match10 = re.match(r"(.*)(MDSCC.*)(.*)", str(row_df))
    if match10:
        return 'MI DEM ST CENTRAL' #how can they do non-candidate issue ads?
    
    match11 = re.match(r"(.*)(MI DEM ST.*)(.*)", str(row_df))
    if match11:
        return 'MI DEM ST CENTRAL'
    
    match12 = re.match(r"(.*)(MI Dem St.*)(.*)", str(row_df))
    if match12:
        return 'MI DEM ST CENTRAL'
    
    match13 = re.match(r"(.*)(MI Energy.*)(.*)", str(row_df))
    if match13:
        return 'MI ENERGY MI JOBS'
    
    match14 = re.match(r"(.*)(MI ENERGY.*)(.*)", str(row_df))
    if match14:
        return 'MI ENERGY MI JOBS'
    
    match15 = re.match(r"(.*)(Michigan Energy.*)(.*)", str(row_df))
    if match15:
        return 'MI ENERGY MI JOBS'
    
    match16 = re.match(r"(.*)(PROTECT MI T.*)(.*)", str(row_df))
    if match16:
        return 'PROTECT MI TAXPAYERS'
    
    match17 = re.match(r"(.*)(PROTECTING MI T.*)(.*)", str(row_df))
    if match17:
        return 'PROTECT MI TAXPAYERS'
    
    match18 = re.match(r"(.*)(Protecting MI T.*)(.*)", str(row_df))
    if match18:
        return 'PROTECT MI TAXPAYERS'
    
    match19 = re.match(r"(.*)(Protect our.*)(.*)", str(row_df))
    if match19:
        return 'PROTECT OUR JOBS'
    
    match20 = re.match(r"(.*)(PROTECT OUR.*)(.*)", str(row_df))
    if match20:
        return 'PROTECT OUR JOBS'
    
    match21 = re.match(r"(.*)(PROTECT WORKING.*)(.*)", str(row_df))
    if match21:
        return 'PROTECT WORKING FAMILIES'
    
    match22 = re.match(r"(.*)(Protect Working.*)(.*)", str(row_df))
    if match22:
        return 'PROTECT WORKING FAMILIES'
    
    match23 = re.match(r"(.*)(RESTORE.*)(.*)", str(row_df))
    if match23:
        return 'RESTORE OUR FUTURE'
    
    match24 = re.match(r"(.*)(Restore.*)(.*)", str(row_df))
    if match24:
        return 'RESTORE OUR FUTURE'
    
    match25 = re.match(r"(.*)(STAND UP.*)(.*)", str(row_df))
    if match25:
        return 'STAND UP FOR DEMOCRACY'
    
    match26 = re.match(r"(.*)(Stand up.*)(.*)", str(row_df))
    if match26:
        return 'STAND UP FOR DEMOCRACY'
    
    match20 = re.match(r"(.*)(protect our.*)(.*)", str(row_df))
    if match20:
        return 'PROTECT OUR JOBS'
    
    else:
        return row_df


# In[138]:

non_candidate_2012_df = non_candidate_2012_df[['Advertiser_Clean', 'Contract', 'Buy_Line', 'Rate', 'Starting_Date', 'Ending_Date', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Program_Name', 'Rating_RA35+', 'Rep:_RA35+', 'Last_Activity', 'Last_Mod/Rev', 'Length_in_Sec', 'AM', 'PM', 'Duration', '10:00', '10:30', '11:00', '11_AM', '11_PM', '11:30', '11:35', '12:00', '12:05', '12:30', '12:35', '1:00', '1:05', '1:30', '1:35', '2:00', '3:00', '3:30', '4:00', '4:30', '4:59', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '7:58', '8:00', '8:30', '9:00', '9:30']]


# In[139]:

non_candidate_2012_df['Advertiser_Clean2'] = non_candidate_2012_df['Advertiser_Clean'].apply(advertiser3)


# In[140]:

non_candidate_2012_df['Advertiser_Clean2'].value_counts()


# In[141]:

non_candidate_2012_df = non_candidate_2012_df[['Advertiser_Clean2', 'Contract', 'Buy_Line', 'Rate', 'Starting_Date', 'Ending_Date', 'Number_of_Wks', 'Spt/Week', 'Total_Spots', 'Total_Dollars', 'Program_Name', 'Rating_RA35+', 'Rep:_RA35+', 'Last_Activity', 'Last_Mod/Rev', 'Length_in_Sec', 'AM', 'PM', 'Duration', '10:00', '10:30', '11:00', '11_AM', '11_PM', '11:30', '11:35', '12:00', '12:05', '12:30', '12:35', '1:00', '1:05', '1:30', '1:35', '2:00', '3:00', '3:30', '4:00', '4:30', '4:59', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30', '7:58', '8:00', '8:30', '9:00', '9:30']]


# In[142]:

def liberal(row1):
    if row1 == 'MI ENERGY MI JOBS':
        return 1
    
    if row1 == 'PROTECT MI TAXPAYERS':
        return 0
    
    if row1 == 'CARE FOR MICHIGAN':
        return 0
    
    if row1 == 'PROTECT WORKING FAMILIES':
        return 1
    
    if row1 == 'PROTECT MI VOTE':
        return 1
    
    if row1 == 'DETROIT INTERNATIONAL BRIDGE CO':
        return 0
    
    if row1 == 'CIT 4 AFF QUALITY HOMECARE':
        return 1
    
    if row1 == 'PROTECT OUR JOBS':
        return 1
    
    if row1 == 'RESTORE OUR FUTURE': #Romney presidential PAC created by aids.
        return 0
    
    if row1 == 'CITIZEN PROTECT MI':
        return 0
    
    if row1 == 'MICH EDU. ASS':
        return 1
    
    if row1 == 'TAXPAYER AGAINST MONOPOLI':
        return 1
    
    if row1 == 'STAND UP FOR DEMOCRACY': #marking conservative because they are against Public Act 4, which enables emergency fund managers.
        return 0                        #Defining liberal as pro big government and conservative as anti big government.
    
    if row1 == 'JUDICIAL CRISIS NETWO':
        return 0
    
    if row1 == '60 PLU':
        return 0
    
    if row1 == 'AMER. FUTURE FU':
        return 0
    
    if row1 == 'HARD WORKING AMERICA':
        return 0
    
    
def dark_money(row1):
    if row1 == 'JUDICIAL CRISIS NETWO':
        return 1
    
    if row1 == '60 PLU':
        return 1
    
    if row1 == 'AMER. FUTURE FU':
        return 1
    
    else:
        return 0
    
    
def local(row1):
    if row1 == 'MI ENERGY MI JOBS':
        return 1
    
    if row1 == 'PROTECT MI TAXPAYERS':
        return 1
    
    if row1 == 'CARE FOR MICHIGAN':
        return 1
    
    if row1 == 'PROTECT WORKING FAMILIES':
        return 1
    
    if row1 == 'PROTECT MI VOTE':
        return 1
    
    if row1 == 'DETROIT INTERNATIONAL BRIDGE CO':
        return 1
    
    if row1 == 'CIT 4 AFF QUALITY HOMECARE':
        return 1
    
    if row1 == 'PROTECT OUR JOBS':
        return 1
    
    if row1 == 'RESTORE OUR FUTURE': #Romney presidential PAC created by aids.
        return 0
    
    if row1 == 'CITIZEN PROTECT MI':
        return 1
    
    if row1 == 'MICH EDU. ASS':
        return 1
    
    if row1 == 'TAXPAYER AGAINST MONOPOLI':
        return 1
    
    if row1 == 'STAND UP FOR DEMOCRACY': #marking conservative because they are against Public Act 4, which enables emergency fund managers.
        return 1
    
    if row1 == 'JUDICIAL CRISIS NETWO':
        return 0
    
    if row1 == '60 PLU':
        return 0
    
    if row1 == 'AMER. FUTURE FU ':
        return 0
    
    if row1 == 'HARD WORKING AMERICA':
        return 1

# 0 = not relevant, 1 = for the issue, 2 = against the issue

def energy(row1):
    if row1 == 'MI ENERGY MI JOBS':
        return 1

    if row1 == 'CARE FOR MICHIGAN':
        return -1
    
    if row1 == 'CITIZEN PROTECT MI':
        return -1
    
    else:
        return 0

def bargaining(row1):
    if row1 == 'PROTECT WORKING FAMILIES':
        return 1
    
    if row1 == 'PROTECT OUR JOBS':
        return 1
    
    if row1 == 'CITIZEN PROTECT MI':
        return -1
    
    if row1 == 'MICH EDU. ASS':
        return 'Pro Prop 2 (Collective Bargaining)'
    
    if row1 == 'PROTECT MI TAXPAYERS':
        return -1
    
    if row1 == 'CITIZEN PROTECT MI':
        return -1
    
    else:
        return 0

    
def casino(row1):
    if row1 == 'PROTECT MI VOTE':
        return -1
    
    else:
        return 0

def bridge(row1):
    if row1 == 'DETROIT INTERNATIONAL BRIDGE CO':
        return 1
    
    if row1 == 'CITIZEN PROTECT MI':
        return -1
    
    if row1 == 'TAXPAYER AGAINST MONOPOLI':
        return -1
    
    else:
        return 0

def homecare(row1):
    if row1 == 'CIT 4 AFF QUALITY HOMECARE':
        return 1
    
    if row1 == 'CITIZEN PROTECT MI':
        return -1
    
    else:
        return 0
    

def romney(row1):
    if row1 == 'RESTORE OUR FUTURE': #Romney presidential PAC created by aids.
        return 1
    
    else:
        return 0
    
 
def emergency_fund(row1):
    if row1 == 'STAND UP FOR DEMOCRACY':
        return 1
    
    else:
        return 0
    
    
def mccormack(row1):
    if row1 == 'JUDICIAL CRISIS NETWO':
        return -1
    
    else:
        return 0
    
def uni_healthcare(row1):
    if row1 == '60 PLU':
        return -1
    
    else:
        return 0
    
def stabenow(row1):
    if row1 == 'AMER. FUTURE FU':
        return -1
    
    if row1 == 'HARD WORKING AMERICA':
        return -1
    
    else:
        return 0
    
def issues_for_transpose(row1):
    if row1 == 'MI ENERGY MI JOBS':
        return 'Prop 3 (Renewable Energy)'
    
    if row1 == 'PROTECT MI TAXPAYERS':
        return 'Prop 2 (Collective Bargaining)'
    
    if row1 == 'CARE FOR MICHIGAN':
        return 'Prop 3 (Renewable Energy)'
    
    if row1 == 'PROTECT WORKING FAMILIES':
        return 'Prop 2 (Collective Bargaining)'
    
    if row1 == 'PROTECT MI VOTE':
        return 'Casino Expansion'
    
    if row1 == 'DETROIT INTERNATIONAL BRIDGE CO':
        return 'Prop 6 (Michigan International Bridge Initiative)'
    
    if row1 == 'CIT 4 AFF QUALITY HOMECARE':
        return 'Prop 4 (MI Qaulity Care on State Level)'
    
    if row1 == 'PROTECT OUR JOBS':
        return 'Prop 2 (Collective Bargaining)'
    
    if row1 == 'RESTORE OUR FUTURE': #Romney presidential PAC created by aids.
        return 'Romney Presidential Campaign'
    
    if row1 == 'CITIZEN PROTECT MI':
        return 'Prop 2 (Collective Bargaining)'
        return 'Prop 3 (Renewable Energy)'
        return 'Prop 4 (MI Qaulity Care on State Level)'
        return 'Prop 6 (Michigan International Bridge Initiative)'
    
    if row1 == 'MICH EDU. ASS':
        return 'Prop 2 (Collective Bargaining)'
    
    if row1 == 'TAXPAYER AGAINST MONOPOLI':
        return 'Prop 6 (Michigan International Bridge Initiative)'
    
    if row1 == 'STAND UP FOR DEMOCRACY':
        return 'Prop 1 (Referendum against Public Act 4, Emergency Manager Fund)'
    
    if row1 == 'JUDICIAL CRISIS NETWO':
        return 'Supreme Court Justice Bridget McCormack'
    
    if row1 == '60 PLU':
        return 'Universal Healthcare'
    
    if row1 == 'AMER. FUTURE FU':
        return 'Dem Senator Debbie Stabenow'
    
    if row1 == 'HARD WORKING AMERICA':
        return 'Dem Senator Debbie Stabenow'    

     
def issues(row1):
    if row1 == 'MI ENERGY MI JOBS':
        return 'Pro Prop 3 (Renewable Energy)'
    
    if row1 == 'PROTECT MI TAXPAYERS':
        return 'Anti Prop 2 (Collective Bargaining)'
    
    if row1 == 'CARE FOR MICHIGAN':
        return 'Anti Prop 3 (Renewable Energy)'
    
    if row1 == 'PROTECT WORKING FAMILIES':
        return 'Pro Prop 2 (Collective Bargaining)'
    
    if row1 == 'PROTECT MI VOTE':
        return 'Anti-Casino Expansion'
    
    if row1 == 'DETROIT INTERNATIONAL BRIDGE CO':
        return 'Prop 6 (Michigan International Bridge Initiative)'
    
    if row1 == 'CIT 4 AFF QUALITY HOMECARE':
        return 'Pro Prop 4 (MI Qaulity Care on State Level)'
    
    if row1 == 'PROTECT OUR JOBS':
        return 'Pro Prop 2 (Collective Bargaining)'
    
    if row1 == 'RESTORE OUR FUTURE': #Romney presidential PAC created by aids.
        return 'Romney Presidential Campaign'
    
    if row1 == 'CITIZEN PROTECT MI':
        return 'Anti Props 2-6'
    
    if row1 == 'MICH EDU. ASS':
        return 'Pro Prop 2 (Collective Bargaining)'
    
    if row1 == 'TAXPAYER AGAINST MONOPOLI':
        return 'Anti Prop 6 (Michigan International Bridge Initiative)'
    
    if row1 == 'STAND UP FOR DEMOCRACY':
        return 'Pro Prop 1 (Referendum against Public Act 4, Emergency Manager Fund)'
    
    if row1 == 'JUDICIAL CRISIS NETWO':
        return 'Anti- Supreme Court Justice Bridget McCormack'
    
    if row1 == '60 PLU':
        return 'Anti Universal Healthcare'
    
    if row1 == 'AMER. FUTURE FU ':
        return 'Anti Dem Senator Debbie Stabenow'
    
    if row1 == 'HARD WORKING AMERICA':
        return 'Anti Dem Senator Debbie Stabenow'
    
    
    
    
def relevant_issue_success(row1):
    if row1 == 'Prop 3 (Renewable Energy)':
        return 0
    
    if row1 == 'Prop 2 (Collective Bargaining)':
        return 0
    
    if row1 == 'Casino Expansion Off Ballot':
        return 1
    
    if row1 == 'Prop 6 (Michigan International Bridge Initiative)':
        return 0
    
    if row1 == 'Prop 4 (MI Qaulity Care on State Level)':
        return 0
    
    if row1 == 'Romney Presidential Campaign':
        return 0
    
    if row1 == 'Prop 1 (Referendum against Public Act 4, Emergency Manager Fund)':
        return 0
    
    if row == 'Supreme Court Justice Bridget McCormack':
        return 1
    
    if row1 == 'Universal Healthcare':
        return 0
    
    if row1 == 'Dem Senator Debbie Stabenow':
        return 1
    


# In[143]:

non_candidate_2012_df.head()


# In[144]:

non_candidate_2012_df['Dark_Money'] = non_candidate_2012_df['Advertiser_Clean2'].apply(dark_money)


# In[145]:

non_candidate_2012_df['Liberal'] = non_candidate_2012_df['Advertiser_Clean2'].apply(liberal)


# In[146]:

non_candidate_2012_df['Local'] = non_candidate_2012_df['Advertiser_Clean2'].apply(local)


# In[147]:

non_candidate_2012_df['Ad_Focus'] = non_candidate_2012_df['Advertiser_Clean2'].apply(issues)


# In[148]:

non_candidate_2012_df['Ad_Issue'] = non_candidate_2012_df['Advertiser_Clean2'].apply(issues_for_transpose)


# In[149]:

non_candidate_2012_df['Renewable_Energy'] = non_candidate_2012_df['Advertiser_Clean2'].apply(energy)


# In[150]:

non_candidate_2012_df['Total_Dollars'].mode()

# In[152]:

non_candidate_2012_df['Pro_Collective_Bargaining'] = non_candidate_2012_df['Advertiser_Clean2'].apply(bargaining)


# In[153]:

non_candidate_2012_df['Casino_Expansion'] = non_candidate_2012_df['Advertiser_Clean2'].apply(casino)


# In[154]:

non_candidate_2012_df['Anti_2nd_Detroit_Bridge'] = non_candidate_2012_df['Advertiser_Clean2'].apply(bridge)


# In[155]:

non_candidate_2012_df['Homecare_in_State_Constitution'] = non_candidate_2012_df['Advertiser_Clean2'].apply(homecare)


# In[156]:

non_candidate_2012_df['Romney_for_President'] = non_candidate_2012_df['Advertiser_Clean2'].apply(romney)


# In[157]:

non_candidate_2012_df['Govt_Emergency_Fund'] = non_candidate_2012_df['Advertiser_Clean2'].apply(emergency_fund)


# In[158]:

non_candidate_2012_df['McCormack_for_Supreme_Ct_D'] = non_candidate_2012_df['Advertiser_Clean2'].apply(mccormack)


# In[159]:

non_candidate_2012_df['Universal_Healthcare'] = non_candidate_2012_df['Advertiser_Clean2'].apply(uni_healthcare)


# In[160]:

non_candidate_2012_df['Stabenow_for_Senate_D_I'] = non_candidate_2012_df['Advertiser_Clean2'].apply(stabenow)


# In[161]:

energy_df = non_candidate_2012_df[(non_candidate_2012_df['Renewable_Energy'] ==1)
                                  | (non_candidate_2012_df['Renewable_Energy'] ==-1)]


# In[162]:

mccormack_df = non_candidate_2012_df[(non_candidate_2012_df['McCormack_for_Supreme_Ct_D'] == 1)
                                  | (non_candidate_2012_df['McCormack_for_Supreme_Ct_D'] == -1)]


# In[163]:

bargaining_df = non_candidate_2012_df[(non_candidate_2012_df['Pro_Collective_Bargaining'] == 1)
                                      | (non_candidate_2012_df['Pro_Collective_Bargaining'] == -1)]


# In[164]:

casino_df = non_candidate_2012_df[(non_candidate_2012_df['Casino_Expansion'] == 1)
                                  | (non_candidate_2012_df['Casino_Expansion'] == -1)]


# In[165]:

bridge_df = non_candidate_2012_df[(non_candidate_2012_df['Anti_2nd_Detroit_Bridge'] == 1)
                                  | (non_candidate_2012_df['Anti_2nd_Detroit_Bridge'] == -1)]


# In[166]:

homecare_df = non_candidate_2012_df[(non_candidate_2012_df['Homecare_in_State_Constitution'] == 1)
                                    | (non_candidate_2012_df['Homecare_in_State_Constitution'] == -1)]


# In[167]:

romney_df = non_candidate_2012_df[(non_candidate_2012_df['Romney_for_President'] == 1)
                                   | (non_candidate_2012_df['Romney_for_President'] == -1)]


# In[168]:

emergency_fund_df = non_candidate_2012_df[(non_candidate_2012_df['Govt_Emergency_Fund'] == 1) 
                                          | (non_candidate_2012_df['Govt_Emergency_Fund'] == -1)]


# In[169]:

healthcare_df = non_candidate_2012_df[(non_candidate_2012_df['Universal_Healthcare'] == 1)
                                       | (non_candidate_2012_df['Universal_Healthcare'] == -1)]


# In[170]:

stabenow_df = non_candidate_2012_df[(non_candidate_2012_df['Stabenow_for_Senate_D_I'] == 1) 
                                    | (non_candidate_2012_df['Stabenow_for_Senate_D_I'] == -1)]

stabenow_df['Ad_Issue']


# In[171]:
#THIS IS WHERE I AM CHANGING THE CODE. I CHANGE PERCENTAGE OF VOTE TO WIN OR LOSE. I ALSO INCLUDE ITEMS IN RACE. *CHANGE CANDIDATES TO ITEMS.* I ALSO INCLUDE WHETHER IT IS A CANDIDATE OR ISSUE. I HAVE FINISHED THIS FOR DEBBIE STABENOW — THE FIRST ITEM.  

results_list = []

results = {'In_Place': 1, 'Win': 1, 'Ad_Issue': 'Dem Senator Debbie Stabenow', 'Candidates_in_Race': 6, 'Candidate': 1}

results_list.append(results)

stabenow_df2 = pd.DataFrame(results_list, columns = ['In_Place', 'Win', 'Ad_Issue', 'Candidate'])

stabenow_df2.columns

stabenow_both_df = stabenow_df.merge(stabenow_df2, on = ['Ad_Issue'], how = 'inner')

stabenow_both_df.columns


stabenow_both_df


# In[172]:

energy_df['Ad_Issue'] = 'Prop 3 (Renewable Energy)'


# In[173]:

energy_df['Ad_Issue'].value_counts()


# In[174]:

results_list2 = []

results2 = {'In_Place': 0, 'Percentage_of_Vote': 38.00, 'Ad_Issue': 'Prop 3 (Renewable Energy)'}

results_list2.append(results2)

energy_df2 = pd.DataFrame(results_list2, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue' ])

#energy_df2

energy_both_df = energy_df.merge(energy_df2, on = ['Ad_Issue'], how = 'inner')

energy_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate


# In[175]:

bargaining_df['Ad_Issue'].value_counts()


# In[176]:

results_list3 = []

results3 = {'In_Place': 0, 'Percentage_of_Vote': 42.00, 'Ad_Issue': 'Prop 2 (Collective Bargaining)'}

results_list3.append(results3)

bargaining_df2 = pd.DataFrame(results_list3, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue' ])

#energy_df2

bargaining_both_df = bargaining_df.merge(bargaining_df2, on = ['Ad_Issue'], how = 'inner')

bargaining_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate


# In[177]:

casino_df['Ad_Issue'].value_counts()


# In[178]:

results_list4 = []

results4 = {'In_Place': 1, 'Percentage_of_Vote': 100.00, 'Ad_Issue': 'Casino Expansion'}

results_list4.append(results4)

casino_df2 = pd.DataFrame(results_list4, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue' ])

#energy_df2

casino_both_df = casino_df.merge(casino_df2, on = ['Ad_Issue'], how = 'inner')

casino_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate


# In[179]:

bridge_df['Ad_Issue'].value_counts()


# In[180]:

bridge_df['Ad_Issue'] = 'Prop 6 (Michigan International Bridge Initiative)'


# In[181]:

bridge_df['Ad_Issue'].value_counts()


# In[182]:

results_list5 = []

results5 = {'In_Place': 0, 'Percentage_of_Vote': 41.00, 'Ad_Issue': 'Prop 6 (Michigan International Bridge Initiative)'}

results_list5.append(results5)

bridge_df2 = pd.DataFrame(results_list5, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue' ])

#energy_df2

bridge_both_df = bridge_df.merge(bridge_df2, on = ['Ad_Issue'], how = 'inner')

bridge_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate


# In[183]:

homecare_df['Ad_Issue'].value_counts()


# In[184]:

homecare_df['Ad_Issue'] = 'Prop 4 (MI Qaulity Care on State Level)'


# In[185]:

homecare_df['Ad_Issue'].value_counts()


# In[186]:

results_list6 = []

results6 = {'In_Place': 0, 'Percentage_of_Vote': 44.00, 'Ad_Issue': 'Prop 4 (MI Qaulity Care on State Level)'}

results_list6.append(results6)

homecare_df2 = pd.DataFrame(results_list6, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue' ])

#energy_df2

homecare_both_df = homecare_df.merge(homecare_df2, on = ['Ad_Issue'], how = 'inner')

homecare_both_df

#1 for positive, 2 for negative for Stabenow_for_Senate


# In[187]:

romney_df['Ad_Issue'].value_counts()


# In[188]:

results_list7 = []

results7 = {'In_Place': 0, 'Percentage_of_Vote': 47.20, 'Ad_Issue': 'Romney Presidential Campaign'}

results_list7.append(results7)

romney_df2 = pd.DataFrame(results_list7, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue' ])

#energy_df2

romney_both_df = romney_df.merge(romney_df2, on = ['Ad_Issue'], how = 'inner')

romney_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate

# In[189]:

emergency_fund_df['Ad_Issue'].value_counts()


# In[190]:

results_list8 = []

results8 = {'In_Place': 0, 'Percentage_of_Vote': 47.00, 'Ad_Issue': 'Prop 1 (Referendum against Public Act 4, Emergency Manager Fund)'}

results_list8.append(results8)

emergency_fund_df2 = pd.DataFrame(results_list8, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue'])

#energy_df2

emergency_fund_both_df = emergency_fund_df.merge(emergency_fund_df2, on = ['Ad_Issue'], how = 'inner')

emergency_fund_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate

# In[191]:

healthcare_df['Ad_Issue'].value_counts()


# In[192]:

results_list9 = []

results9 = {'In_Place': 0, 'Percentage_of_Vote': 51.10, 'Ad_Issue': 'Universal Healthcare'}

results_list9.append(results9)

healthcare_df2 = pd.DataFrame(results_list9, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue'])

#energy_df2

healthcare_both_df = healthcare_df.merge(healthcare_df2, on = ['Ad_Issue'], how = 'inner')

healthcare_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate

# In[193]:

mccormack_df['Ad_Issue'].value_counts()


# In[194]:

results_list10 = []

results10 = {'In_Place': 0, 'Percentage_of_Vote': 23.50, 'Ad_Issue': 'Supreme Court Justice Bridget McCormack'}

results_list10.append(results10)

mccormack_df2 = pd.DataFrame(results_list10, columns = ['In_Place','Percentage_of_Vote', 'Ad_Issue'])

#energy_df2

mccormack_both_df = mccormack_df.merge(mccormack_df2, on = ['Ad_Issue'], how = 'inner')

mccormack_both_df.columns

#1 for positive, 2 for negative for Stabenow_for_Senate


# In[195]:

len(mccormack_both_df)


# In[196]:

len(healthcare_both_df)


# In[197]:

len(emergency_fund_both_df)


# In[198]:

len(romney_both_df)


# In[199]:

len(homecare_both_df)


# In[200]:

len(bridge_both_df)


# In[202]:

len(bargaining_both_df)


# In[203]:

len(energy_both_df)


# In[204]:

len(stabenow_both_df)


# In[205]:

issues_all_df = mccormack_both_df.append(healthcare_both_df)


# In[206]:

issues_all_df


# In[207]:

issues_all_df = issues_all_df.append(emergency_fund_both_df)


# In[208]:

issues_all_df = issues_all_df.append(romney_both_df)


# In[209]:

issues_all_df = issues_all_df.append(homecare_both_df)


# In[210]:

len(issues_all_df)


# In[211]:

issues_all_df = issues_all_df.append(bridge_both_df)


# In[213]:

issues_all_df = issues_all_df.append(energy_both_df)


# In[214]:

issues_all_df = issues_all_df.append(stabenow_both_df)


# In[215]:

issues_all_df = issues_all_df.append(bargaining_both_df)


# In[216]:

issues_all_df = issues_all_df.fillna(0)


# In[217]:

issues_all_df = issues_all_df.drop('Ad_Issue', 1)


# In[218]:

issues_all_df = issues_all_df.drop('Rating_RA35+', 1)


# In[219]:

issues_all_df = issues_all_df.drop('Rep:_RA35+', 1)

# In[224]:

issues_all_df.columns


# In[225]:

issues_all_df = issues_all_df.drop('Advertiser_Clean2', 1)


# In[226]:

issues_all_df = issues_all_df.drop('Buy_Line', 1)


# In[227]:

issues_all_df = issues_all_df.drop('Starting_Date', 1)


# In[228]:

issues_all_df = issues_all_df.drop('Program_Name', 1)


# In[229]:

issues_all_df = issues_all_df.drop('Last_Activity', 1)


# In[230]:

issues_all_df = issues_all_df.drop('Last_Mod/Rev', 1)


# In[231]:

issues_all_df.head()


# In[232]:

issues_all_df = issues_all_df.drop('Contract', 1)


# In[233]:

issues_all_df = issues_all_df.drop('Duration', 1)


# In[234]:

issues_all_df = issues_all_df.drop('Ad_Focus', 1)


# In[235]:

issues_all_df['Rate'] = issues_all_df['Rate'].astype(float)


# In[236]:

issues_all_df['Length_in_Sec'] = issues_all_df['Length_in_Sec'].astype(float)


# In[237]:

issues_all_df['Ending_Date'] = issues_all_df['Length_in_Sec'].astype(float)


# In[238]:

issues_all_df.columns


# In[242]:

issues_all_df['Rate'] = issues_all_df['Rate'].astype(float)


# In[243]:

issues_all_df['Length_in_Sec'] = issues_all_df['Length_in_Sec'].astype(float)


# In[244]:

non_candidate_2012_df[non_candidate_2012_df['Dark_Money'] == 1]['Ad_Issue'].value_counts()


# In[245]:

mccormack_both_df.columns


# In[246]:

bargaining_both_df.head()

