import os
import sys
import pathlib
import datetime

import mysql.connector


def main() -> None:
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])

    db_host = sys.argv[4]
    db_pass = sys.argv[5]
    symbols = sys.argv[6]

    try:
        db = mysql.connector.connect(
            host=db_host,
            user='root',
            passwd=db_pass,
            database='last_price_saver'
        )
        cursor = db.cursor()
    except Exception as error:
        print("Unable to create connection to db: {}".format(error))
        return

    for symbol in symbols.split(','):
        try:
            select_query = """
                SELECT timestamped, price
                FROM last_price
                WHERE
                    symbol = '{3}'
                    AND
                    year(FROM_UNIXTIME(timestamped)) = {0}
                    AND
                    month(FROM_UNIXTIME(timestamped)) = {1}
                    AND 
                    day(FROM_UNIXTIME(timestamped)) = {2}
            """.format(
                year,
                month,
                day,
                symbol
            )

            print("Attempting to run select query: {}".format(
                select_query
            ))

            cursor.execute(select_query)
            data_items = cursor.fetchall()

            for item in data_items:
                dir_path = "exported-data/{}".format(symbol)
                pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)

                with open("{}/{}-{}-{}.csv".format(dir_path, year, month, day), 'a') as out:
                    out.write("{},{}\n".format(item[0], item[1]))

        except Exception as error:
            print("Unable to get data for y/m/d [symbol] - {}/{}/{} [{}]: {}".format(
                year,
                month,
                day,
                symbol,
                error
            ))

    return


if __name__ == "__main__":
    main()
