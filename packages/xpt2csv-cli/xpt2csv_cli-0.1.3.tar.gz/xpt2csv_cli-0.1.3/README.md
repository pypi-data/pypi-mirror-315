# Install

```{shell}
pip install xpt2csv-cli
```

# convert xpt files to csv
 
Let's assume user have one directory that have xpt files

```

- study_one/
    - bw.xpt
    - dm.xpt
    - lb.xpt
    - mi.xpt
    - om.xpt
    - ts.xpt
    - tx.xpt
```

make a directory where to save csv files

```{shell}
mkdir directory_to_save_csv/
```

now convert xpt files to csv files using 'to_csv' command

```{shell}
to_csv study_one/ directory_to_save_csv/
```

this command will convert all xpt files to csv files and will save in following directory structure

```
- directory_to_save_csv/
    - study_one/
        - bw.csv
        - dm.csv
        - lb.csv
        - mi.csv
        - om.csv
        - ts.csv
        - tx.csv
```


 Let's say user have few study in a directory `all_study/`. 

```
- all_study/
    - study_one/
        - bw.xpt
        - dm.xpt
        - lb.xpt
        - mi.xpt
        - om.xpt
        - ts.xpt
        - tx.xpt
    - study_one/
        - bw.xpt
        - dm.xpt
        - lb.xpt
        - mi.xpt
        - om.xpt
        - ts.xpt
        - tx.xpt
```

```{shell}
to_csv all_study/ directory_to_save_csv/
```

this will convert and save all xpt files in following directory structure

```
- directory_to_save_csv/
        - study_one/
            - bw.csv
            - dm.csv
            - lb.csv
            - mi.csv
            - om.csv
            - ts.csv
            - tx.csv
        - study_one/
            - bw.csv
            - dm.csv
            - lb.csv
            - mi.csv
            - om.csv
            - ts.csv
            - tx.csv
```


project in [github](https://github.com/Yousuf28/xpt2csv)  
pypi [link](https://pypi.org/project/xpt2csv-cli/)
