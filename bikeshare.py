import time
import pandas as pd
import numpy as np
import math
import calendar

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('Incorrect city. Please try again!\n')
            continue
        else:
            break
    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month could you like to filter? All, January, February, March, April, May, or June.\n').lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print('Incorrect month. Please try again!\n')
            continue
        else:
            break
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhich day of the week do you want to filter? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.\n').lower()
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print('Incorrect day. Please try again!\n')
            continue
        else:
            break
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
    # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # Filter by month.
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # create the new dataframe
        df = df[df['month'] == month]
    # Filter by day of week.
    if day != 'all':
        # Create the new dataframe.
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Display the most common month.
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    print('  The most common month is {}'.format(calendar.month_name[most_common_month]))
    # Display the most common day of week.
    most_common_dayofweek = df['Start Time'].dt.weekday_name.mode()[0]
    print('  The most common day of the week is {}'.format(most_common_dayofweek))
    # Display the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('  The most common start hour is {}'.format(most_common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # Display most commonly used start station.
    most_common_start_station = df['Start Station'].mode()[0]
    print('  The most common start station is {}'.format(most_common_start_station))
    # Display most commonly used end station.
    most_common_end_station = df['End Station'].mode()[0]
    print('  The most common end station is {}'.format(most_common_end_station))
    # Display most frequent combination of start station and end station trip.
    start_end_station = df['Start Station'] + ',' + df['End Station']
    most_frequent_trip = start_end_station.mode()[0]
    most_frequent_station = most_frequent_trip.split(',')
    print('  The most frequent trip is from {} to {}'.format(most_frequent_station[0], most_frequent_station[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # Display total travel time.
    total_travel_time = df['Trip Duration'].sum()
    days, hours, mins, secs = convert_sec(total_travel_time)
    print('  The total travel time is {} days {} hours {} minutes {} seconds.'.format(days,hours,mins,secs))
    # Display mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    days, hours, mins, secs = convert_sec(mean_travel_time)
    print('  The total mean travel time is {} days {} hours {} minutes {} seconds.'.format(days,hours,mins,secs))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types.
    if('User Type' in df):
        for value, count in df['User Type'].value_counts().iteritems():
            print('  There are {} {}s'.format(count, value))
    else:
        print('  User Type data is unavailable')
    # Display counts of gender.
    if('Gender' in df):
        for value, count in df['Gender'].value_counts().iteritems():
            print('  There are {} {}s'.format(count, value))
    else:
        print('  Gender data is unavailable')
    # Display earliest, most recent, and most common year of birth.
    if('Birth Year' in df):
        earliest_year_birth = df['Birth Year'].min()
        print('  The earliest year of birth is {}'.format(int(earliest_year_birth)))
        most_recent_year_birth = df['Birth Year'].max()
        print('  The most recent year of birth is {}'.format(int(most_recent_year_birth)))
        most_common_year_birth = df['Birth Year'].mode()[0]
        print('  The most common year of birth is {}'.format(int(most_common_year_birth)))
    else:
        print('  Birth Year data is unavailable')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')


def display_raw_data(df):
    """ Displays RAW data """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display the raw data 5 lines at a time.
    rawdata = input('Would you like to see the raw data?\n').lower()
    # Initialise variable 'count'.
    count = 0
    while (rawdata == 'yes'):
        count += 5
        print(df.iloc[count-5:count])
        rawdata = input('\nWould you like to see another 5 records?\n').lower()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\n')


def convert_sec(seconds):
    """
    Converts seconds to days, hours, minutes and seconds 
    Args:
        (int) seconds - number of seconds to convert
    Returns:
        days - number of days 
        hours - number of hours
        mins - number of minutes
        secs - number of seconds
    """
    seconds = math.floor(seconds)
    days = seconds // (60 * 60 * 24)
    seconds = seconds % (60 * 60 * 24)
    hours = seconds // (60 * 60)
    seconds = seconds % (60 * 60)
    mins = seconds // 60
    secs = seconds % 60
    # Return the values days, hours, mins, secs.
    return days, hours, mins, secs


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()