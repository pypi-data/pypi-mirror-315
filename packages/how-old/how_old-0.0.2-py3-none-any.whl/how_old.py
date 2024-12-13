from datetime import datetime, date
import argparse

def how_old_am_i(year_of_birth: int, month_of_birth: int = 1, day_of_birth: int = 1) -> int:
    """
    Calculate your age given the year of birth.

    By default, this will assume your birthday is January 1st.
    You can optionally specify the month and day of your birth
    to get a more accurate result.

    :param year_of_birth: The year you were born
    :param month_of_birth: The month you were born (default: 1)
    :param day_of_birth: The day of the month you were born (default: 1)
    :return: Your age in years
    """
    try:
        today = date.today()
        birthday = date(year_of_birth, month_of_birth, day_of_birth)
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        print(f"You are {age} years old")
        return age
    except ValueError as e:
        print(f"Invalid date: {e}")
        return -1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate your age based on your date of birth.")
    parser.add_argument("--year_of_birth", type=int, required=True, help="Your birth year (e.g., 1990)")
    parser.add_argument("--month_of_birth", type=int, default=1, help="Your birth month (1-12, default: 1)")
    parser.add_argument("--day_of_birth", type=int, default=1, help="Your birth day (1-31, default: 1)")
    
    args = parser.parse_args()
    how_old_am_i(args.year_of_birth, args.month_of_birth, args.day_of_birth)
