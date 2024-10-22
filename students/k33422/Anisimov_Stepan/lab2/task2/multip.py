from multiprocessing import Process
import psycopg2
from time import time
import requests


def parse_url(url, session):
    with psycopg2.connect(host='localhost', database='hackathon_db', user='postgres', password=123, port=5432) as conn:
        with conn.cursor() as cur:
            conn.autocommit = True

            response = session.get(url=url, headers={'User-Agent': 'Mozilla/129.0.2'}).json()

            for post in response['posts']:
                title = post['title']
                descr = post['descr'].replace("<br />", "").replace("&nbsp;", " ")

                try:
                    data = title, descr
                    cur.execute("INSERT INTO competition (name, description) VALUES ('%s', '%s')" % data)
                    
                except Exception as e:
                    conn.rollback()
                    print(e)

            conn.rollback()


def main():
    urls = ["https://feeds.tildacdn.com/api/getfeed/?feeduid=131632209651-986950497851",
        "https://feeds.tildacdn.com/api/getfeed/?feeduid=617755803461"]

    process_count = len(urls)
    processes = []

    with requests.Session() as session:
        for i in range(process_count):
            p = Process(target=parse_url, args=(urls[i], session))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()


if __name__=="__main__":
    start_time = time()

    main()

    end_time = time()
    print(end_time - start_time)


    