import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - 'chicago' | 'new york city' | 'washington'
        (str) month - 'all' or one of MONTHS
        (str) day   - 'all' or one of DAYS
    """
    print("Hello! Let's explore some US bikeshare data!")

    # City 
    city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
    while city not in CITY_DATA:
        city = input("Invalid city. Please enter Chicago, New York City, or Washington: ").strip().lower()

    # Month filter (Jan–Jun or 'all')
    month = input("Filter by month? (January..June or 'all'): ").strip().lower()
    while month not in MONTHS + ['all']:
        month = input("Invalid month. Enter January..June or 'all': ").strip().lower()

    # Day of week filter (Mon–Sun or 'all')
    day = input("Filter by day of week? (e.g., Monday or 'all'): ").strip().lower()
    while day not in DAYS + ['all']:
        day = input("Invalid day. Enter Monday..Sunday or 'all': ").strip().lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city  (str): name of the city to analyze
        month (str): month name or 'all'
        day   (str): weekday name or 'all'

    Returns:
        df (pd.DataFrame): filtered data with helper columns added
    """
    path = CITY_DATA[city]
    df = pd.read_csv(path)

    # Parse datetimes and add helper columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # End Time may have NAs across files
    if 'End Time' in df.columns:
        df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

    df['month'] = df['Start Time'].dt.month           # 1..12
    df['day_of_week'] = df['Start Time'].dt.day_name()  # 'Monday'...
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':
        month_idx = MONTHS.index(month) + 1  # Jan=1
        df = df[df['month'] == month_idx]

    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print('-' * 40)
        return

    # Most common month (map number to name)
    common_month_num = df['month'].mode()[0]
    common_month = MONTHS[common_month_num - 1].title()
    print(f"Most common month: {common_month}")

    # Most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of week: {common_day}")

    # Most common start hour
    common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {common_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print('-' * 40)
        return

    # Most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {start_station}")

    # Most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f"Most common end station: {end_station}")

    # Most frequent combination (start -> end)
    combo_series = (df['Start Station'] + " -> " + df['End Station'])
    common_trip = combo_series.mode()[0]
    print(f"Most common trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating the Exact Trip Duration...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print('-' * 40)
        return

    # Total travel time (seconds)
    total_seconds = int(df['Trip Duration'].sum())
    # Mean travel time (seconds)
    mean_seconds = float(df['Trip Duration'].mean())

    def fmt(sec):
        sec = int(sec)
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        parts = []
        if d: parts.append(f"{d}d")
        if h: parts.append(f"{h}h")
        if m: parts.append(f"{m}m")
        parts.append(f"{s}s")
        return " ".join(parts)

    print(f"Total travel time: {fmt(total_seconds)} ({total_seconds:,} seconds)")
    print(f"Average travel time: {fmt(mean_seconds)} ({mean_seconds:,.2f} seconds)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        print('-' * 40)
        return

    # Counts of user types
    if 'User Type' in df.columns:
        print("Counts by user type:")
        print(df['User Type'].value_counts(dropna=False).to_string())

    # Counts of gender (NYC/Chicago only)
    if 'Gender' in df.columns:
        print("\nCounts by gender:")
        print(df['Gender'].value_counts(dropna=False).to_string())
    else:
        print("\nGender data not available for this city.")

    # Birth year stats (NYC/Chicago only)
    if 'Birth Year' in df.columns:
        by = pd.to_numeric(df['Birth Year'], errors='coerce').dropna()
        if not by.empty:
            earliest = int(by.min())
            most_recent = int(by.max())
            most_common = int(by.mode()[0])
            print("\nBirth year stats:")
            print(f"  Earliest: {earliest}")
            print(f"  Most recent: {most_recent}")
            print(f"  Most common: {most_common}")
        else:
            print("\nBirth year data not available.")
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df):
    """Iteratively display raw data 5 rows at a time upon user request."""
    i = 0
    choice = input("\nWould you like to see 5 lines of raw data? (yes/no): ").strip().lower()
    while choice == 'yes':
        if i >= len(df):
            print("No more raw data to display.")
            break
        end = min(i + 5, len(df))
        print(df.iloc[i:end])
        i = end
        if i >= len(df):
            print("No more raw data to display.")
            break
        choice = input("Show 5 more rows? (yes/no): ").strip().lower()


def main():
    print("Welcome to the Bikeshare Data Analysis Tool !")
    print_instruction()

    def print_instruction():
        print("You can explore bikeshare data from here onwards")

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # raw data viewing flow 
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
