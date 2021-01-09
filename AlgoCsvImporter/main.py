import os
import sys
import csv
import glob
import time
import pathlib
import datetime

import dotenv
import mysql.connector


def main() -> None:
    # input dir where algo data lays
    input_dir = 'algo-data'

    # Env file
    env_path = pathlib.Path('.') / '.env'
    dotenv.load_dotenv(dotenv_path=env_path)

    print("Will import algo csv files from: {}".format(input_dir))

    # Load up list of files in specified dir
    algo_files = glob.glob("{}/*.csv".format(input_dir))

    try:
        db = mysql.connector.connect(
            host='lps-host',
            user='root',
            passwd=os.getenv('MYSQL_ROOT_PASSWORD'),
            database='last_price_saver'
        )
        cursor = db.cursor()
    except Exception as error:
        print("Unable to create connection to db: {}".format(error))
        sys.exit(-1)

    # Iterate thru each csv and dump data into database
    for algo_file in algo_files:
        with open(algo_file, newline='') as csv_data:
            name_split = algo_file.split("_")
            print(algo_file)
            time.sleep(1)
            i = -1
            for row in csv_data:
                i = i + 1
                if i == 0:
                    continue
                row = row.split(",")
                try:
                    insert_query = """
                        INSERT INTO algo_data (
                            ymd,
                            quote,
                            file_name,
                            total_trades,
                            buy_constraint_ath,
                            buy_constraint_before_timing,
                            buy_constraint_after_timing,
                            buy_algo,
                            sell_algo,
                            canceled_buys_count,
                            insufficient_funds_count,
                            order_size,
                            starting_cash,
                            ending_cash,
                            stock_leftover,
                            total_value,
                            increase_dollars,
                            increase_percent,
                            order_size_cash_percent
                        ) VALUES (
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
                        );
                    """.format(
                        name_split[1],
                        name_split[0].split("/")[1],
                        algo_file,
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9].replace("$", ""),
                        row[10].replace("$", ""),
                        row[11],
                        row[12].replace("$", ""),
                        row[13].replace("$", ""),
                        row[14].replace("%", ""),
                        row[15]
                    )

                    cursor.execute(insert_query)
                except Exception as err:
                    print("Unable to execute insert query: {}; error: {}".format(
                        insert_query, err
                    ))
                    continue

        db.commit()

    return


if __name__ == "__main__":
    main()
