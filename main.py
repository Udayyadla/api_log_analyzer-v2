# first read csv

import csv
from datetime import datetime

total_valid_request = 0
total_corrupted_rows = 0
error_count = 0
request_per_user = {}
request_path_count = {}
total_response_time = 0
slow_requests = []
status_code_summary = {}

try:
    with open("api_logs.csv","r") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
               timestamp = row["timestamp"]
               user = row["user"]
               method = row["method"]
               path = row["path"]
               status = row["status"]
               response_time = row["response_time"]
               

               if (user == "" or path == "" or timestamp == "" 
                 or method == "" or status == "" or response_time == ""):
                   
                   # validate timestamp
                   total_corrupted_rows += 1
                   continue
               
               datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")   
               status = int(status)
               response_time = int(response_time)
               total_valid_request += 1
               total_response_time += response_time
                # Total valid requests
               print(f"{timestamp} - {user} - {method} - {path} - {status} - {response_time}")

               if status in status_code_summary:
                   status_code_summary[status] += 1
               else:
                   status_code_summary[status] = 1
               
                

               # total error count
               if status >= 400:
                   error_count += 1
                

               # request per user
               if user in request_per_user:
                   request_per_user[user] += 1
               else:
                   request_per_user[user] = 1

               # request per path
               if path in request_path_count:
                   request_path_count[path] += 1

               else:
                   request_path_count[path] = 1

               if response_time >200:
                   slow_requests.append(row)
              

            except (KeyError,ValueError,TypeError):
                 #Total corrupted rows
                total_corrupted_rows += 1
               
               
                

except FileNotFoundError:
    print("File not found")


print("total valid requests: ",total_valid_request)
print("total corrupted rows:", total_corrupted_rows)
print("total error count:", error_count)
if total_valid_request > 0:
    print(f"error_rate {round((error_count/total_valid_request)*100,2)}%")
    print("average response time", round(total_response_time/total_valid_request,2))
else:
    print("average response time: NA")
    print("error_rate : NA")
for user, count in request_per_user.items():
    print(f"{user}:{count}")


for status,count in status_code_summary.items():
    print(f"{status}:{count}")
max_path_count = 0
max_path_name = ""

for path, count in request_path_count.items():
    max_path_count = max(max_path_count, count)
    if count == max_path_count:
        max_path_name = path
print(f"max path count - {max_path_name} :{max_path_count}")
for request in slow_requests:
    print(f"{request['timestamp']} - {request['user']} - {request['method']} - {request['path']} - {request['status']} - {request['response_time']}")

    