import csv
import glob
import os
import threading
import os
# thu tu cac thuoc tinh
# 1. "duration"
# 2. "protocol_type" 
# 3."service"
# 4. "flag"
# 5. "src_bytes"
# 6. "dst_bytes"
# 7. "count"
# 8. "dst_host_count"
# 9. "dst_host_srv_count"
# 10. "dst_host_same_srv_rate"
# 11. "dst_host_diff_srv_rate"
def parse_log():
    # threading.Timer(5.0, parse_log).start()
    list_of_files = glob.glob('/home/phong/log1/conn.2017-07-28-08-00-00.log') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    filename=os.path.basename(latest_file)
    with open(latest_file) as csvfile:
        with open('dataset/'+os.path.splitext(filename)[0]+'.csv','w') as outputfile:
            readCSV = csv.reader(csvfile)
            all_log = []
            count = 0
            index = 0
            check_index = 0
            for row in readCSV:
                count_time = 0
                dst_host_count = 0
                dst_host_srv_count = 0
                count = count+1
                if count >= 9 :
                    sub_array = []
                    a = ''.join(row)        
                    for i in a.split():
                        if i == '-':
                            sub_array.append('0')
                        else:    
                            sub_array.append(i)
                    if len(sub_array) > 6:
                        all_log.append(sub_array)
                        check_index = index-1
                        if check_index > -1:               
                            while True:
                                if check_index > -1:
                                    time = float(all_log[index][0]) - float(all_log[check_index][0])
                                    setip1 = set(all_log[check_index][2].split(' '))
                                    setip11 =  set(all_log[index][2].split(' '))
                                    setip2 = set(all_log[check_index][4].split(' '))
                                    setip21 =  set(all_log[index][4].split(' '))              
                                if time > float(60) or check_index < 0:
                                    break  
                                if setip1 == setip11 and setip2 == setip21:
                                    count_time = count_time+1
                                check_index = check_index -1
                        check_index = index-1
                        if check_index > -1:
                            i = 0
                            while (i < 100):
                                if check_index < 0:
                                    break  
                                if check_index > -1:
                                    srv1 = all_log[check_index][5]
                                    srv2 = all_log[index][5]
                                    setip2 = set(all_log[check_index][4].split(' '))
                                    setip21 =  set(all_log[index][4].split(' '))
                                if setip2 == setip21:
                                    dst_host_count = dst_host_count + 1
                                if setip2 == setip21 and srv1 == srv2:  
                                    dst_host_srv_count =  dst_host_srv_count +1
                                i = i+1  
                                check_index = check_index - 1
                    if  dst_host_srv_count != 0:
                        same_srv_rate = dst_host_srv_count*100/dst_host_count
                        diff_srv_rate = 100 - same_srv_rate             
                    else:
                        same_srv_rate = 0
                        diff_srv_rate = 100 - same_srv_rate                                                                    
                    index = index + 1      
                    if len(sub_array) > 6:
                        outputfile.write(sub_array[8]+","+sub_array[6] + ","+sub_array[5]+"," +sub_array[11] + ","+sub_array[9]+","+sub_array[10]+","+str(count_time)+","+str(dst_host_count)+","+str(dst_host_srv_count)+","+str(same_srv_rate)+","+str(diff_srv_rate)+"\n")

parse_log()                                                