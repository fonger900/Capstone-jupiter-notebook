import csv
import re
import datetime

list_ips = []
list_timeline = {}
index = 0
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
    
with open('/home/phong/study/capstone_project/log iis/u_ex170228.csv') as csvfile:
    with open('/home/phong/study/capstone_project/log iis/output.csv','w') as outputfile:
        regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        status_list=[' 100 ',' 101 ',' 200 ',' 201 ',' 202 ',' 203 ',' 204 ',' 205 ',' 206 ',' 300 ',' 301 ',' 302 ',' 303 ',' 304 ',' 305 ',' 306 ',' 307 ',
        ' 400 ',' 401 ',' 402 ',' 403 ',' 404 ',' 405 ',' 406 ',' 407 ',' 408 ',' 409 ',' 410 ',' 411 ',' 412 ',' 413 ',' 414 ',' 415 ',' 416 ',' 417 ',
        ' 500 ',' 501 ',' 502 ',' 503 ',' 504 ',' 505 ']
        readCSV = csv.reader(csvfile)
        print(readCSV)
        for row in readCSV:
            sub_array = []
            a = ''.join(row)        
            for i in a.split():
                sub_array.append(i)
            status ="0"
            ip = "0"
            time2 = "0"
            port = "0"
            percentage = '0'   
            match_ip = re.findall( r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[^0-9]", a )       
            if len(match_ip) > 0:
                port = sub_array[6]
                ip = match_ip[0]
                if match_ip[0] not in list_ips:            
                    list_ips.append(match_ip[0])                
        #    time = re.findall( r'\d{2}/[a-zA-Z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}',a)
        #    time1 = re.findall( r'\d{2}/\d{2}-\d{2}:\d{2}:\d{2}.\d{6}',a)
            match_time2 = re.findall( r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',a)
            if len(match_time2) > 0:
                time2 = match_time2[0]
                list_timeline_plus =[ip,time2.split(' ')[0],get_sec(time2.split(' ')[1])]
                list_timeline[str(index)] = list_timeline_plus
                check_index = index - 1
                same_attr_log = 0
                total_log = 0                
                while True:            
                          
                    if str(check_index) in list_timeline:             
                        if (list_timeline[str(index)][2] - list_timeline[str(check_index)][2] <= 180) and list_timeline[str(index)][0] == list_timeline[str(check_index)][0]:
                          same_attr_log += 1 
                          check_index -= 1
                          total_log += 1
                        elif (list_timeline[str(index)][2] - list_timeline[str(check_index)][2] <= 180):
                            total_log += 1 
                            check_index -= 1                   
                        elif (list_timeline[str(index)][2] - list_timeline[str(check_index)][2] > 180):
                            break
                    else:
                        break
                index+=1
                print ("total:" + str(total_log))
                print ("same:" + str(same_attr_log))
                if total_log == 0 or same_attr_log == 0:
                    percentage = '0'
                else:         
                    percentage = str(same_attr_log*100/total_log)                                                        
                print (percentage)
            for s in status_list:
                substring = ''.join(s)
                if substring in a:
                    status = s
            if len(match_ip) > 0:
                outputfile.write(ip + "," +time2+","+port+","+sub_array[-2]+","+sub_array[-3]+","+sub_array[-1]+","+ status +","+str(percentage)+ "\n")    
                    
                   
            
    #    print()        
    #print(list_ips)