import pandas as pd
import re
from IPython.display import display

# Предобработка данных
def dt_head(v_ds):
    """Выводит первые строки списка наборов данных"""
    for ds in v_ds: 
        print("\nОбзор данных:", ds ,"--------")
        display(eval(ds).head(3))
# 
def dt_info(v_ds):
    """Сводная информация по всем столбцам"""
    for ds in v_ds: 
        print("\nЗапрос всех атрибутов:", ds ,"--------")
        print(eval(ds).info())
# 
def dt_rename_pep(ds):
    """Корректирует названия переменных в соответсвии с 'The PEP 8 – Style Guide for Python Code'"""
    v_name = ds.columns.tolist() # get var names as a list
    v_name = [re.sub('(.)([A-Z][a-z]+)', r'\1_\2', i_name) for i_name in v_name]
    ds.columns = [re.sub('([a-z0-9])([A-Z])', r'\1_\2', i_name).lower() for i_name in v_name]
    # print("New names:",v_name)
    return ds
# 
def dt_na_count(v_ds):
    """Посчитать пропуски по всем столбцам"""
    for ds in v_ds: 
        print("\nПропуски в данных:", ds ,"--------")
        print(eval(ds).isna().sum()) 
# 
##### явные дубликаты
def dt_dupl_cnt(v_ds):
    """Посчитать дубликаты по всем столбцам"""
    for ds in v_ds:
        print("Количество явных дубликатов", ds ,":",
              eval(ds).duplicated().sum()) 

def dt_dupl_cat(v_ds, v_var_cat=[]):
    """Проверка дубликатов - разница в написании категорий"""
    for ds in v_ds:
        print("\nПроверка категорий", ds, "------") 
        if len(v_var_cat) == 0:
            v_var_cat = eval(ds).select_dtypes(['object']).columns # categorical
        for col in v_var_cat:
            if col in eval(ds).columns:
                print(col, eval(ds)[col].sort_values().unique())

"""data = pd.read_csv(r"W:\_PRJ\_prj__wrk_ndc\_packages\_datasets\test_personal.csv")
data.head()
v_ds = ['data']
dt_head(v_ds)
dt_rename_pep(data)
dt_na_count(v_ds)
dt_info(v_ds)
dt_dupl_cnt(v_ds)
dt_dupl_cat(v_ds)

v_var_cat=[]
if len(v_var_cat) == 0:
    v_var_cat = ds.select_dtypes(['object']).columns # categorical"""

import rdcpy