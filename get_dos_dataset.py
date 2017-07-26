import pandas as pd
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

train_set=pd.read_csv('~/dataset/kddcup.data',header=None, names=col_names)

dos_col_names = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","serror_rate","rerror_rate","diff_srv_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_srv_serror_rate","label"]

train_set_dos=train_set[dos_col_names]

train_set_dos=train_set_dos[(train_set_dos['label']=='normal.') | (train_set_dos['label']=='back.') | (train_set_dos['label']=='land.') |(train_set_dos['label']=='neptune.') |(train_set_dos['label']=='pod.') |(train_set_dos['label']=='smurf.') |(train_set_dos['label']=='teardrop.')]

train_set_dos.to_csv('~/dataset/dos_kdd99.csv')
