import sys

burg = '51660' #FIPS of Harrisonburg City
rock = '51165'  #FIPS of Rockingham County

def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data


def getCountyData(data, fips):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """
    cityData = []
    for entry in data:
        entry_fips = entry[3]
        if entry_fips == fips:
            cityData.append(entry)

    return cityData


def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """
    rockDate = -1
    for entry in data:
        date = entry[0]
        fips = entry[3]
        if fips == rock:
            rockDate = date
            break

    burgDate = -1
    for entry in data:
        date = entry[0]
        fips = entry[3]
        if fips == burg:
            burgDate = date
            break

    answer = f'The first positive COVID case in Rockingham County was on {rockDate} and the first in Harrisonburg was on {burgDate}.'
    print('Question 1: ', answer)

    return

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """
    burgData = getCountyData(data, burg)
    totalCases = 0
    burgCases = 0
    burgDate = -1
    for i in range(len(burgData)):
        date = burgData[i][0]
        newCases = burgData[i][4] - totalCases
        totalCases = burgData[i][4]

        if burgCases < newCases:
            burgCases = newCases
            burgDate = date

    rockData = getCountyData(data, rock)
    totalCases = 0
    rockCases = 0
    rockDate = -1
    for i in range(len(rockData)):
        date = rockData[i][0]
        newCases = rockData[i][4] - totalCases
        totalCases = rockData[i][4]

        if rockCases < newCases:
            rockCases = newCases
            rockDate = date

    answer = f'The day with the greatest number of new daily cases recorded in Harrisonburg was on {burgDate} and in Rockingham County it was on {rockDate}'
    print('Question 2: ', answer)

    return


def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    cityData = getCountyData(data, burg)

    max = 0
    burgDates = -1
    for i in range(7, len(cityData)):
        sum = 0
        for point in range(0, 7):
            newCases = cityData[i-point][4] - cityData[i-point-1][4]
            sum += newCases

        if max < sum:
            max = sum
            burgDates = f'{cityData[i-6][0]} to {cityData[i][0]}'

    rockData = getCountyData(data, rock)

    max = 0
    rockDates = -1
    for i in range(7, len(rockData)):
        sum = 0
        for point in range(0, 7):
            newCases = rockData[i-point][4] - rockData[i-point-1][4]
            sum += newCases

        if max < sum:
            max = sum
            rockDates = f'{rockData[i-6][0]} to {rockData[i][0]}'

    answer = f'The worst 7-day period for new COVID cases in Harrisonburg City was {burgDates} and the worst in Rockingham County was {rockDates}'
    print('Question 3: ', answer)

    return


if __name__ == "__main__":
    file = r'C:\Users\nelms\OneDrive - James Madison University\ENGR 315\ENGR315-sp2026-student\Exams\Assignment 1 - COVID Data\us-counties.csv'
    data = parse_nyt_data(file)

    '''
    #The code below is evil and i refuse to run it.  Feel free to uncomment it if youd like to have python printing for 5 mins strait :)

    for (date,county, state, fips, cases, deaths) in data:
        print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')
    '''

    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What was the worst seven day period in Harrisonburg for new COVID cases (in terms of absolute number of cases)?
    # What was the worst seven day period in Rockingham County for new COVID cases (in terms of absolute number of cases)?
    third_question(data)
