import time
import pandas as pd
import numpy as np
import bikeshare_inputs as bsi

months = ['january', 'february','march','april','may','june','july','august','september','october','november','december']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter City:').lower()
    while city not in ['chicago','new york city','washington']:
        city = bsi.city_input()

    # get user input for month (all, january, february, ... , june)
    month = input('Enter Month:').lower()
    while month not in ['all','january', 'february','march','april','may','june','july','august','september','october','november','december']:
        month = bsi.month_input()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter Day:').lower()
    while day not in ['all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        day = bsi.day_input()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week, hour and station combo from dataframe to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['station_combo'] = 'Start Station: ' + df['Start Station'] + ' End Station: ' + df['End Station']
    df['travel_time'] = df['End Time'] - df['Start Time']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        day = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is:',months[df['month'].mode()[0] - 1])

    # display the most common day of week
    print('The most common day of week is:',days[df['day_of_week'].mode()[0] - 1])

    # display the most common start hour
    print('The most common hour is:',df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most common end station is:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most common station combination is:', df['station_combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is:', df['travel_time'].sum())

    # display mean travel time
    print('The average travel time is:', df['travel_time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nThe user type counts are:\n',pd.DataFrame(df['User Type'].value_counts()))

    # Display counts of gender
    if "Gender" in df.columns:
        print('\nThe gender type counts are:\n',pd.DataFrame(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print('\nThe earliest birthyear is:',df['Birth Year'].min())
        print('The most recent birthyear is:',df['Birth Year'].max())
        print('The most common birthyear is:',df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
