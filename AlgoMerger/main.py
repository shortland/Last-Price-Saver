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
    dir_path = 'merged-data'

    # Env file
    env_path = pathlib.Path('.') / '.env'
    dotenv.load_dotenv(dotenv_path=env_path)

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
        return

    for symbol in (os.getenv('QUOTE_SYMBOLS')).split(','):
        try:
            select_query = """
                SELECT 
                    quote, 
                    buy_constraint_ath, 
                    buy_constraint_before_timing, 
                    buy_constraint_after_timing, 
                    buy_algo, 
                    sell_algo, 
                    starting_cash, 
                    order_size_cash_percent, 
                    AVG(increase_percent) as increase_percent_avg 
                FROM 
                    algo_data 
                WHERE 
                    quote = '{0}' 
                GROUP BY 
                    quote, 
                    buy_constraint_ath, 
                    buy_constraint_before_timing, 
                    buy_constraint_after_timing, 
                    buy_algo, 
                    sell_algo, 
                    starting_cash, 
                    order_size_cash_percent
                ORDER BY 
                    increase_percent_avg DESC
            """.format(
                symbol
            )

            print("Attempting to run select query: {}".format(
                select_query
            ))

            cursor.execute(select_query)
            data_items = cursor.fetchall()

            for item in data_items:
                with open("{}/{}.csv".format(dir_path, symbol), 'a') as out:
                    out.write("{}\n".format(item))

        except Exception as error:
            print("Unable to get data for [{}]: {}".format(
                symbol,
                error
            ))

    return


if __name__ == "__main__":
    main()
