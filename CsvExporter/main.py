import os
import pathlib

import dotenv
import mysql.connector


def main() -> None:
    env_path = pathlib.Path('.') / '.env'
    dotenv.load_dotenv(dotenv_path=env_path)

    print("You'll be prompted for the specified date & data you wish to export.")
    year = int(input("Data for which year?:"))
    month = int(input("Data for which month? (numerical):"))
    day = int(input("Data for which day?:"))
    # ticker = input(
    #     "Data for which stock? (one ticker symbol):"
    # )

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
                SELECT * 
                FROM (
                    SELECT FROM_UNIXTIME(timestamped) as ts, price 
                    FROM last_price 
                    WHERE 
                        symbol = '{3}'
                ) as t 
                WHERE 
                    year(t.ts) = {0}
                    AND
                    month(t.ts) = {1}
                    AND 
                    day(t.ts) = {2}
                LIMIT 10;
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
                print(item)

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
