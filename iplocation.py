import csv
import socket
import struct
import redis
from dotenv import load_dotenv
import os
import requests
import gzip
import shutil

load_dotenv()

class RedisConfig:
    HOST = os.getenv('REDIS_HOST', 'localhost')
    PORT = int(os.getenv('REDIS_PORT', 6379))
    DB = int(os.getenv('REDIS_DB', 4))
    PASSWORD = os.getenv('REDIS_PASSWORD')

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=RedisConfig.HOST,
            port=RedisConfig.PORT,
            db=RedisConfig.DB,
            password=RedisConfig.PASSWORD
        )

    def flush_db(self):
        self.client.flushdb()
        print('Redis DB truncated successfully')

    def store_data(self, key, data):
        self.client.hmset(key, data)

    def zadd(self, key, value, score):
        self.client.zadd(key, {value: score})

    def zrangebyscore(self, key, min_score, max_score, start=0, num=1):
        return self.client.zrangebyscore(key, min_score, max_score, start=start, num=num)

    def hgetall(self, key):
        return self.client.hgetall(key)

class IPDataManager:
    @staticmethod
    def ip_to_int(ip_address):
        return struct.unpack("!I", socket.inet_aton(ip_address))[0]

    @staticmethod
    def download_new_db(filename):
        url = f"https://cdn.jsdelivr.net/npm/@ip-location-db/geolite2-city/{filename}"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'{filename} downloaded successfully')
        except Exception as e:
            print(f"Error downloading database: {e}")
            return False
        return True

    @staticmethod
    def extract_csv(filename):
        try:
            with gzip.open(filename, 'rb') as f_in, open('city.csv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                print(f'{filename} extracted successfully')
        except Exception as e:
            print(f"Error extracting CSV file: {e}")
            return False
        return True

def delete_files(*filenames):
    for filename in filenames:
        try:
            os.remove(filename)
            print(f"Deleted file: {filename}")
        except OSError as e:
            print(f"Error deleting file {filename}: {e}")

def main():
    redis_client = RedisClient()
    redis_client.flush_db()
    delete_files('city.csv', 'geolite2-city-ipv4.csv.gz')

    filename = 'geolite2-city-ipv4.csv.gz'
    if IPDataManager.download_new_db(filename):
        if IPDataManager.extract_csv(filename):
            with open('city.csv', newline='') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                for row in csvreader:
                    ip_start = row[0]
                    ip_end = row[1]
                    country_code = row[2]
                    city = row[5]
                    longitude = row[7]
                    latitude = row[8]

                    ip_start_int = IPDataManager.ip_to_int(ip_start)
                    ip_end_int = IPDataManager.ip_to_int(ip_end)
                    unique_key = f"{ip_start_int}-{ip_end_int}"

                    hash_data = {
                        "ip_start": ip_start,
                        "ip_start_int": ip_start_int,
                        "ip_end": ip_end,
                        "ip_end_int": ip_end_int,
                        "country_code": country_code,
                        "city": city,
                        "longitude": longitude,
                        "latitude": latitude
                    }

                    redis_client.zadd("kadmoz_ip_ranges", unique_key, ip_start_int)
                    redis_client.store_data(unique_key, hash_data)

if __name__ == "__main__":
    main()
    
