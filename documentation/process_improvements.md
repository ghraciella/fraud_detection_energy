# Process Improvements: 

* using memory profiler to check


## __Reading in the data + merge:__  example output


* read csv files with pandas + merge both, engine = default (python)

    - memory usage = 1987.2MiB

```bash

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
   118    203.0 MiB    203.0 MiB           1   @profile
   119                                         def read_dataset():
   120    254.3 MiB     51.3 MiB           1       client_data = pd.read_csv('../data/raw/client_data.csv')
   121   1306.5 MiB   1052.2 MiB           1       invoice_data = pd.read_csv('../data/raw/invoice_data.csv')
   122   1987.2 MiB    680.7 MiB           1       data = pd.merge(client_data, invoice_data, on="client_id", how="left")
   123   1987.2 MiB      0.0 MiB           1       return data
```

* read csv files with pandas  + merge both, low_memory=True, engine='pyarrow'


    - memory usage = 2037.2MiB

```bash

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    80     55.5 MiB     55.5 MiB           1   @profile
    81                                         def read_combine_dataframe(datapath= None):

    ...    ...          ...               ...  ... 
   115   2037.2 MiB      0.2 MiB           1       return data
```


* read csv files with pandas  + merge both, low_memory=True : 

    - memory usage = 1736.3MiB

```bash

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    80     70.4 MiB     70.4 MiB           1   @profile
    81                                         def read_combine_dataframe(datapath= None):

    ...    ...          ...               ...  ... 
   115   1736.3 MiB      0.1 MiB           1       return data
```

* read csv files with pandas  + merge both, low_memory=True : 

    - memory usage = 1547.3 MiB

```bash

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    80     80.4 MiB     80.4 MiB           1   @profile
    81                                         def read_combine_dataframe(datapath= None):

    ...    ...          ...               ...  ... 
   115   1547.3 MiB      0.1 MiB           1       return data
```








