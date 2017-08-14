import pandas as pd

def get_dos_set():
    col_names = ["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]
    dos_colname = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","serror_rate","rerror_rate","diff_srv_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_srv_serror_rate","label"]
    #colname = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","label"]
    
    dos_set = pd.read_csv('~/dataset/kddcup.data',header=None, names=col_names)
    dos_set = dos_set[dos_colname]
    dos_set=dos_set[(dos_set['label']=='normal.') | (dos_set['label']=='back.') | (dos_set['label']=='land.') |(dos_set['label']=='neptune.') |(dos_set['label']=='pod.') |(dos_set['label']=='smurf.') |(dos_set['label']=='teardrop.')]
    dos_set.to_csv('~/dataset/kdd_dos_data.csv')
    print "save to dataset/kdd_dos_data.csv"
    
get_dos_set()