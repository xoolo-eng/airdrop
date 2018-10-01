import os
import sys
PROGECT_ROOT = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
if PROGECT_ROOT not in sys.path:
    sys.path.append(PROGECT_ROOT)
import node
import time
import signal
import psycopg2
import requests
from datetime import datetime
from multiprocessing import Process, Queue


SOCKET_PATH = "get_pool.soc"
PID_FILE = "/var/run/user/1000/get_pool.pid"
INTERVALS = [4, 12, 20]


def get_all_transactions():
    connect = requests.post(
        "http://localhost:8545",
        json={"method": "parity_allTransactions", "params": [], "id": 1, "jsonrpc": "2.0"}
    )
    if connect.status_code == 200:
        return connect.json()["result"]
    raise Exception("Error get transactions.")


def get_start_time():
    last_number = node.get_number_last_block()
    last_block_time = node.get_block_by_number(number=last_number).timestamp
    presios_block_time = node.get_block_by_number(number=last_number-1).timestamp
    difference = last_block_time - presios_block_time
    while INTERVALS[0] == difference:
        start_element = INTERVALS.pop(0)
        INTERVALS.append(start_element)
    return (last_block_time + INTERVALS[1] + INTERVALS[2]) - 1


def daemon_scan(queue):
    time.sleep(
        abs(get_start_time() - int(datetime.timestamp(datetime.now())))
    )
    stop = False
    while not stop:
        queue.put(get_all_transactions())
        time.sleep(INTERVALS[0])
        first_interval = INTERVALS.pop(0)
        INTERVALS.append(first_interval)


def daemon_handler(queue):
    connection_data = {
        "user": "blockchain",
        "password": "LbvfbDbnz2Xfirb",
        "host": "localhost",
        "dbname": "blockchain"
    }
    postgres_connection = psycopg2.connect(**connection_data)
    postgres_connection.autocommit = True
    postgres = postgres_connection.cursor()
    stop = False
    while not stop:
        transaction = queue.get()
        for transaction in transaction:
            if transaction.get("gas"):
                transaction["gas"] = node.node.toInt(hexstr=transaction["gas"])
            if transaction.get("gasPrice"):
                transaction["gasPrice"] = node.node.toInt(hexstr=transaction["gasPrice"])
            if transaction.get("nonce"):
                transaction["nonce"] = node.node.toInt(hexstr=transaction["nonce"])
            if transaction.get("standardV"):
                transaction["standardV"] = node.node.toInt(hexstr=transaction["standardV"])
            if transaction.get("v"):
                transaction["v"] = node.node.toInt(hexstr=transaction["v"])
            if transaction.get("value"):
                transaction["value"] = node.node.toInt(hexstr=transaction["value"])
            if transaction.get("chainId"):
                transaction["chainId"] = node.node.toInt(hexstr=transaction["chainId"])
            fields = '"timestamp",'
            values = "'{}',".format(datetime.now())
            for key in transaction:
                if transaction[key]:
                    fields += '"{}",'.format(key)
                    if type(transaction[key]) == int:
                        values += "{},".format(transaction[key])
                    else:
                        values += "'{}',".format(transaction[key])
            query = "INSERT INTO transactions ({0}) VALUES ({1});".format(
                fields[:-1],
                values[:-1]
            )
            try:
                postgres.execute(query)
            except psycopg2.Error as e:
                print(e)
                print(query)


def daemon_reload():
    connection_data = {
        "user": "blockchain",
        "password": "LbvfbDbnz2Xfirb",
        "host": "localhost",
        "dbname": "blockchain"
    }
    postgres_connection = psycopg2.connect(**connection_data)
    postgres_connection.autocommit = True
    postgres = postgres_connection.cursor()
    stop = False
    query_select = """
        SELECT hash
        FROM transactions
        WHERE "blockHash" is NULL
        AND deleted = FALSE
        ORDER BY "timestamp"
        LIMIT {0} OFFSET {1};
    """
    query_update = """
        UPDATE transactions
        SET
            "blockHash" = '{0}',
            "blockNumber" = {1},
            "transactionIndex" = {2},
            "inBlock" = '{3}'
        WHERE "hash" = '{4}';
    """
    query_not_found = """
        UPDATE transactions
        SET "deleted" = TRUE
        WHERE "hash" = '{}';
    """
    count_records_query = """
        SELECT COUNT(hash)
        FROM transactions
        WHERE "blockHash" is NULL
        AND deleted = FALSE;
    """
    while not stop:
        offset = 0
        count = 100
        count_record = 0
        try:
            postgres.execute(count_records_query)
        except psycopg2.Error as e:
            print(e)
            print(count_records_query)

        try:
            count_record = postgres.fetchone()[0]
        except Exception as e:
            print(e)
            print("No records!!!!")
            continue
        print(count_record)
        while offset <= count_record:
            try:
                postgres.execute(query_select.format(count, offset))
            except psycopg2.Error as e:
                print(e)
                print("select_query")
            offset += count
            transactions_hash = None
            try:
                transactions_hash = postgres.fetchall()
            except Exception:
                continue
            if transactions_hash:
                for hash_transaction in transactions_hash:
                    transaction = None
                    try:
                        transaction = node.get_transaction_by_hash(hash=hash_transaction[0])
                    except ValueError:
                        try:
                            postgres.execute(query_not_found.format(hash_transaction[0]))
                        except psycopg2.Error as e:
                            print(e)
                            print(query_not_found.format(hash_transaction[0]))
                        continue
                    if transaction.blockNumber:
                        blockTimestamp = node.get_block_by_number(number=transaction.blockNumber).timestamp
                        query = query_update.format(
                            node.node.toHex(transaction.blockHash),
                            transaction.blockNumber,
                            transaction.transactionIndex,
                            datetime.fromtimestamp(blockTimestamp),
                            hash_transaction[0]
                        )
                        try:
                            postgres.execute(query)
                        except psycopg2.Error as e:
                            print(e)
                            print(query)
        time.sleep(60)


if __name__ == '__main__':
    try:
        if sys.argv[1] == "stop":
            pids = []
            with open(PID_FILE, "r") as pid_file:
                pids = [int(pid) for pid in pid_file]
                pid_file.close()
            for pid in pids:
                os.kill(pid, signal.SIGKILL)
            os.unlink(PID_FILE)
        else:
            try:
                os.unlink(PID_FILE)
            except Exception:
                pass
    except IndexError:
        pass
    else:
        exit(0)
    queue = Queue()
    pid = os.fork()
    if pid > 0:
        print("start_daemon")
    elif pid == 0:
        d_handler = Process(target=daemon_handler, args=[queue])
        d_scan = Process(target=daemon_scan, args=[queue])
        d_reload = Process(target=daemon_reload, args=[])
        d_handler.start()
        d_scan.start()
        d_reload.start()
        pid_file = open(PID_FILE, "w")
        pid_file.write("{}\n".format(d_scan.pid))
        pid_file.write("{}\n".format(d_handler.pid))
        pid_file.write("{}\n".format(d_reload.pid))
        pid_file.close()
        d_handler.join()
        d_scan.join()
        d_reload.join()
    else:
        raise Exception("Error load daemons.")
