import pandas as pd
from validations import validations
from extract import extract
from extract import appending_deals
from link_maker import making_link
from date_transform import transforming_to_datetime

# valves to make range in which data going to be downloaded
date1 = "01.01.2020"
date2 = "31.12.2025"
cpv = "all"


def making_dataframe(dataframe):  # use to convert raw data downloaded from server
    try:
        x = pd.DataFrame(dataframe)
        return x
    except ValueError:
        return None


def saving_dataframe(df):  # use to save downloaded from server
    default_location = 'output.csv'

    def saving(location):
        df.to_csv(location, index=False, sep=";")  # in Europe here so ";" instead of ","

    try:  # saving to same location as program
        saving(default_location)
    except PermissionError as e:  # saving to other location
        print(f"{e} at saving\nPlease type new location path without file name:")
        new_location = input()
        new_location = f"{new_location}/output.csv"
        saving(new_location)
    print("save completed")


tenders = []  # declaring empty list of tenders


def main(start_day_str, end_day_str, code):
    # checking if input is in correct forms
    if validations(start_day_str, end_day_str, code):
        print("validation passed")
        # converting string dates from input to datetime formats
        start_date = transforming_to_datetime(start_day_str)
        end_date = transforming_to_datetime(end_day_str)
        total_time_span = end_date - start_date

        # first run:
        print("first connection")
        print(start_date, end_date, code)  # printing input config
        link = making_link(start_date, end_date, code)  # making link to connect DB
        print(link)  # printing link for verification in case of  error
        db = appending_deals(extract(link))  # extracting data from eZam DB and appending it into list

        # dodging empty db
        if db:
            print("first df")
            df = making_dataframe(db)  # creating dataframe with pandas to read data from web

            # picking last num from downloaded data and last id of tender
            # to get next page of data starting from this tender
            last_obj_id = df['ObjectId'].iloc[-1]
            last_num = df['id'].iloc[-1]
            print(last_obj_id, last_num)
            print("entering loop")
            repeat = 0  # numer use to numer loops
            while True:
                # loop which will go on as long as downloaded list of data is not empty
                # used to get all pages form eZam DB
                repeat = repeat + 1
                print(f"\nloop #{repeat}")

                # making link to connect to eZam BD and download data after last_obj_id
                link = making_link(start_date, end_date, code, last_obj_id)
                print(link)

                # extracting data from eZam DB and appending it into list
                db = appending_deals(extract(link), last_num + 1)

                print("next df")
                df = making_dataframe(db)  # creating dataframe with pandas to read data from web

                # picking last num from downloaded data and last id of tender
                # to get next page of data from this tender
                new_last_obj_id = df['ObjectId'].iloc[-1]
                new_last_num = df['id'].iloc[-1]
                last_date = transforming_to_datetime(df['publicationDate'].iloc[-1])

                if new_last_num == last_num:  # if number of obj in DB is the same as it was before this loop its break
                    print("ending loop\n100% completed")
                    break
                else:  # if number of obj is not the same as it was before this loop last_num and last_obj_id is updated
                    last_num = new_last_num
                    last_obj_id = new_last_obj_id
                    remaining_time_span = end_date - last_date
                    remaining_time_span = ((total_time_span - remaining_time_span) / total_time_span) * 100
                    remaining_time_span = round(remaining_time_span, 2)
                    print(last_date, last_num, last_obj_id)
                    print(f"{remaining_time_span}% completed")

            # exporting dataframe to csv file
            print("starting saving data")
            saving_dataframe(df)
        else:
            print("db empty at first run")
    else:
        print("Error at validation stage")
    print("that's all")


if __name__ == '__main__':
    main(date1, date2, cpv)
