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
                    a.quote, 
                    a.buy_constraint_ath, 
                    a.buy_constraint_before_timing, 
                    a.buy_constraint_after_timing, 
                    a.buy_algo, 
                    a.sell_algo, 
                    a.starting_cash, 
                    a.order_size_cash_percent, 
                    AVG(a.increase_percent) as increase_percent_avg,
                    GROUP_CONCAT(DISTINCT CONCAT(ymd, ',', increase_percent))
                FROM 
                    algo_data a
                WHERE 
                    quote = '{}' 
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
                    increase_percent_avg
                DESC
            """.format(
                symbol
            )

            print("Attempting to run select query: {}".format(
                select_query
            ))

            cursor.execute(select_query)
            data_items = cursor.fetchall()
            
            with open("{}/{}.csv".format(dir_path, symbol), 'w') as out:
                out.write("Quote,Buy Constraint ATH,Buy Constraint Before Timing,Buy Constraint After Timing,Buy Algo,Sell Algo,Starting Cash,Order Size Cash Percent,Average Percent Increase, ... ind. values ...\n")

            for item in data_items:
                with open("{}/{}.csv".format(dir_path, symbol), 'a') as out:
                    out.write("{}\n".format(
                        ','.join(map(str, item))
                    ))

        except Exception as error:
            print("Unable to get data for [{}]: {}".format(
                symbol,
                error
            ))

    return


if __name__ == "__main__":
    main()
