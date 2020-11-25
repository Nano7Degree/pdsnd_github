import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DIC = {'all': 0, 'january': 1, 'febuary': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
WEEKDAY_DIC = {'all': 7, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 0}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to look at: chicago, new york city or washington (written out, lowercase)?  ').lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        print('This city is not within our list. Please enter a valid city.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month (jan-jun) would you like to look at: all or a specific month (written out, lowercase)?  ').lower()
        if month in ('all', 'january', 'febuary', 'march', 'april', 'may', 'june'):
            break
        print('This month is not within our list. Please enter a valid month or all.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you like to look at: all or a specific day (written out, lowercase)?  ').lower()
        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            break
        print('This day is not within our list. Please enter a valid day or all.')

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
    city_csv = CITY_DATA.get(city)
    df = pd.read_csv(city_csv)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[(df['Month'] == MONTH_DIC.get(month))]

    if day != 'all':
        df = df[(df['Weekday'] == WEEKDAY_DIC.get(day))]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    search_key = 'all'
    for key, value in MONTH_DIC.items():
        if popular_month == value:
            search_key = key
            break
    print('  The most common month is: {}'.format(search_key).title())

    # display the most common day of week
    popular_weekday = df['Weekday'].mode()[0]
    search_key = 'all'
    for key, value in WEEKDAY_DIC.items():
        if popular_weekday == value:
            search_key = key
            break
    print('  The most common weekday is: {}'.format(search_key).title())

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('  The most common hour is: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('  The most common Start Station is: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('  The most common End Station is: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Start End Station Combi'] = df['Start Station'] + '  -  ' + df['End Station']
    popular_combination_start_end_station = df['Start End Station Combi'].mode()[0]
    print('  The most common combination of Start and End Station is: {}'.format(popular_combination_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    df['End Time'] = pd.to_datetime(df['End Time'])

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_seconds = df['Trip Duration'].sum()
    days = sum_seconds // 86400
    hours = (sum_seconds % 86400) // 3600
    minutes = (sum_seconds % 3600) // 60
    seconds = sum_seconds % 60
    print('  The total travel time of all (filtered) bikeshare rentals is: {} day(s) {} hour(s) {} minute(s) and {} second(s)'.format(days, hours, minutes, seconds))

    # display mean travel time
    mean_seconds = df['Trip Duration'].mean()
    days = int(mean_seconds // 86400)
    hours = int((mean_seconds % 86400) // 3600)
    minutes = int((mean_seconds % 3600) // 60)
    seconds = int(mean_seconds % 60)
    print('  The mean of the total travel time of all (filtered) bikeshare rentals is:  {} day(s) {} hour(s) {} minute(s) and {} second(s)'.format(days, hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('For the (filtered) data there are the following amount of user types and their counts:\n{}'.format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' not in df:
        print('\nDisplay counts of Gender: \n  Sorry, we do not have this information for the chosen city.')
    else:
        print('\nFor the (filtered) data there are the following genders and their counts:\n{}'.format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('\nDisplay information of year of birth: \n  Sorry, we do not have this information for the chosen city.')
    else:
        print('\nFor the (filtered) data see the following information for the year of birth: \n  Earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('  Most recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('  Most common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Asks user if 5 rows of data should be displayed. As long as the user answers 'yes', 5 additional rows of data are shown. Loop is ended once users says 'no'. """

    view_data = input('\nWould you like to see 5 lines of data for the chosen filters? Enter yes or no.\n')
    start_loc = 0
    while view_data == 'yes':
        if 'Gender' and 'Birth Year' not in df:
            print(df[['Start Time', 'End Time', 'Start Station', 'End Station', 'User Type']].iloc[start_loc:(5+start_loc)])

        else:
            print(df[['Start Time', 'End Time', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year']].iloc[start_loc:(5+start_loc)])
        start_loc += 5
        view_data = input('\nWould you like to see 5 more lines of data for the chosen filters? Enter yes or no.\n').lower()

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
