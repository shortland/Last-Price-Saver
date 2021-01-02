import os
import pathlib
import datetime

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
            # TODO: $(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' last-price-saver_lps-db_1)
            # Figure out a better way of doing then other than getting host via above...
            # I guess throwing this script into a container then using --link would be best...
            host='172.19.0.2',
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
                SELECT timestamped, price
                FROM (
                    SELECT FROM_UNIXTIME(timestamped) as ts, timestamped, price 
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
