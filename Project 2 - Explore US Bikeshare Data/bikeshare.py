import time
import pandas as pd
import numpy as np
import os  


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#create a list for cities, months and days
cities = list(CITY_DATA.keys())
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def raw_data_prompt_handler(raw_data_choice = True, continue_choice = False):
    '''
    prompts the user if they want to see raw data, this function handles both prompts:
    1. The promot asking if user wants to display raw data
    2. The prompt asking if they'd like to continue viewing data.
    
    inputs:
    (bool) raw_data_choice - if set to true, will use raw_data_prompt
    (bool) continue_choice - if set to true, will use keep_going_prompt
    
    return:
    (str) - a yes or no answer in lower case
    
    '''
    choices = ['yes', 'no']
    #two variables to store the specific prompt
    raw_data_prompt = '\nWould you like to display more data? Enter Yes or No: '
    keep_going_prompt = '\nContinue? Enter Yes or No: '
    
    #continually prompt the user asking if they would like to view raw data; until answer is yes or no
    if raw_data_choice == True:
        choice = input(raw_data_prompt)
        while choice.lower().strip() not in choices:
            print('Invalid Input. Please Enter Yes or No: ')
            choice = input(raw_data_prompt)
        return choice.lower()
    #continually prompt the user asking if they want to continue viewing data; until answer is yes or no
    if continue_choice == True:
        choice = input(keep_going_prompt)
        while choice.lower().strip() not in choices:
            print('Invalid Input. Please Enter Yes or No: ')
            choice = input(keep_going_prompt)
        return choice.lower()
   
def raw_data_handler(df):
    '''
    Handles the task of displaying more records 5 rows at a time.
    
    Input:
    (Dataframe) df - the datafame to iterate over
    
    Returns:
    This function does not return a value
    '''
    start_index = 0
    increment = 5
    
    while True:
        #call the raw_data_prompt_handler function to handle user prompts
        #first argument is set to True to display prompt for raw data input
        if raw_data_prompt_handler(True,False) == 'no':
            break
        print(df.iloc[start_index:increment])
        start_index = increment
        increment += 5
        #call the raw_data_prompt_handler function to handle user prompts
        #second argument is set to True to display prompt for continuing to view more data.
        while raw_data_prompt_handler(False,True) != 'no':
            print(df.iloc[start_index:increment])
            start_index = increment
            increment += 5
        break;
      

def to_12hour_format(hour):
    '''
    converts a 24 hour format to 12 hour
    
    returns:
    str - the hour in 12 hour format
    '''
    if hour == 12:
        return '12PM'
    elif hour == 24:
        return '12AM'
    elif hour > 12:
        return str(hour - 12) + 'PM'
    return str(hour) + 'AM'
    

def get_city():
    ''' asks user to specify city to analyze 
    
        returns:
        list - name of the city contained in the cities list
    '''
    #clear the console screen (keeps things cleaner)
    os.system('clear')
    print('Hello! Let\'s explore some US bikeshare data!')
    # prompt user to select a city  
    selection = input('Enter a city from the following:\n' + '\n'.join(cities).title()+'\nEnter City: ').strip().lower()
    # loop continously until a valid selection is made.
    while selection not in cities:
        print('Invalid city, please try again.')
        selection = input('Enter a city from the following:\n' + '\n'.join(cities).title()+'\nEnter City: ').strip().lower()
    else:
        # if selection is valid, assign selection to city
        city = selection
    #return the users' selection
    return city

def get_month():
    ''' asks user to specify month to analyze 
    
        returns:
        list - name of the month contained in the months list
    '''
    #clear the console screen (keeps things cleaner)
    os.system('clear')
    #prompt the user to select a month from a list of months
    print('Hello! Let\'s explore some US bikeshare data!')
    selection = input('Enter a month from the following:\n' + '\n'.join(months).title()+'\nEnter Month: ').strip().lower()
    #loop continously until a valid selection is made.
    while selection not in months:
        print('Invalid month, please try again.')
        selection = input('Enter a month from the following:\n' + '\n'.join(months).title()+'\nEnter Month: ').strip().lower()
    #if selection is 'all' build a return a list of the index numbers in the months list
    if selection == 'all':
        #build and return a list of the index numbers for all items (except 'all') in the months list
        return [i+1 for i,j in enumerate(months[1:])]
    else:
        #if users' selection is not 'all' then just return the index of the month they selected from the months list.
        month = [months.index(selection)]
    #return the users' selection
    return month
    
def get_day():
    ''' asks user to specify day to analyze 
    
        returns:
        list - day of the week contained in the days list
    '''
    #clear the console (keeps things cleaner)
    os.system('clear')
    print('Hello! Let\'s explore some US bikeshare data!')
    #prompt the user the select a day from a list of days 
    selection = input('Enter a day from the following:\n' + '\n'.join(days).title()+'\nEnter Day: ').strip().lower()
    # loop continously until a valid selection is made.
    while selection not in days:
        print('Invalid day, please try again.')
        selection = input('Enter a day from the following:\n' + '\n'.join(days).title()+'\nEnter Day: ').strip().lower()
    #if selection is 'all' build a return a list of all items in the days list
    if selection == 'all':
        return [i.title() for i in days[1:]]
    else:
        #return the users' selection
        return [selection.title()]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (list) month - name of the month to filter by, or "all" to apply no month filter
        (list) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # call the get_city function to return the chosen city
    city = get_city()

    # TO DO: get user input for month (all, january, february, ... , june)
    # call the get_month function to return the chosen month/s
    month = get_month()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # call the get_month function to return the chosen day/s
    day = get_day()
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (list) month - name of the month to filter by, or "all" to apply no month filter
        (list) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #read in the csv file for the chosen city    
    df = pd.read_csv(CITY_DATA[city])
           
    #Convery Start Time column to a datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #apply filter for chosen month/s
    df = df[df['Start Time'].dt.month.isin(month)]
    
    #apply filter for chosen day/s
    df = df[df['Start Time'].dt.weekday_name.isin(day)] 
    
    #return the filtered dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['Start Time'].dt.month.mode()[0]   
    print('Most common month is:', months[most_common_month].title())
    
    # TO DO: display the most common day of week
    most_common_day = df['Start Time'].dt.weekday_name.mode()[0]
    print('Most common day of week is:', most_common_day)
    
    # TO DO: display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    
    #convert the hour to a 12 hour format if the hour returned is greater than 12
    #hour is being converted for easier readability.
    if most_common_start_hour > 12:
        print('Most common start hour is: {} ({})'.format(most_common_start_hour, to_12hour_format(most_common_start_hour)))
    else:
        print('Most common start hour is: {}'.format(most_common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
  
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
   
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most common Start Station is: {}'.format(most_common_start_station))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common End Station is: {}'.format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    # concat the start station and end station columns
    df['Most Frequent Combination'] = df['Start Station'] + ' ' + df['End Station']
    # apply mode function to find the most common occurence 
    most_frequent_combination = df['Most Frequent Combination'].mode()[0]
    print('Most frequent combination of Start Station and End Station is: \n{}'.format(most_frequent_combination))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is: {}'.format(total_travel_time))
    
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_of_user_types = df['User Type'].value_counts()
    print('Count of User Types is:\n{}'.format(count_of_user_types))
    
    # TO DO: Display counts of gender
    # Gender column is not in Washington.csv dataset.
    # Check if City chosen is Washington before finding the gender counts.
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nCount of Gender is:\n{}'.format(gender_count))
    else:
        print('\nThere is no gender information in this dataset.\n')
    
    # TO DO: Display earliest year of birth
    # Birth Year column is not in Washington.csv dataset.
    # Check if City chosen is Washington before finding birth year information.
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min().astype(int)
        print('\nEarliest Birth Year is: {}'.format(earliest))
    
        # TO DO: Display  most recent year of birth
        latest = df['Birth Year'].max().astype(int)
        print('Latest Birth Year is: {}'.format(latest))
    
        # TO DO: Display most common year of birth    
        most_common_birth_year =  df['Birth Year'].mode()[0]
        print('Most Common Birth Year is: {}'.format(int(most_common_birth_year)))
    else:
        print('\nThere is no birth year information in this dataset.\n')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        
        #Pass the dataframe to raw_data_handler function to handle task of displaying more data
        raw_data_handler(df)
                
        restart = input('\nWould you like to restart? Enter Yes or No: ')
        if restart.lower().strip() != 'yes':
            print('\nGoodbye!\n')
            break


if __name__ == "__main__":
	main()
