import os
import random
import string
import pandas as pd
import numpy as np
from sklearn import preprocessing

from tpf.link.toolml import pkl_save,pkl_load







def drop_cols(df_all, columns=["dt"]):
    """多余字段删除"""
    # 多了一个dt日期 这里做删除处理
    df_all.drop(columns=columns,inplace=True)
    
def min_max_scaler(X, model_path=f"model/min_max_scaler.pkl",reuse=True):
    """
    params
    ---------------------------
    - reuse:如果有训练就需要利用，无训练就不需要复用，比如一些无监督场景
    
    """
    if reuse:
        if os.path.exists(model_path):
            scaler_train = pkl_load(file_path=model_path,use_joblib=True)
        else:
            # 仅对数值型的特征做标准化处理
            scaler_train = preprocessing.MinMaxScaler().fit(X[[X.columns[(X.dtypes == 'float32') | (X.dtypes == 'float64') | (X.dtypes == 'int64')]][0].tolist()])
            pkl_save(scaler_train,file_path=model_path,use_joblib=True)
    else:
        scaler_train = preprocessing.MinMaxScaler().fit(X[[X.columns[(X.dtypes == 'float32') | (X.dtypes == 'float64') | (X.dtypes == 'int64')]][0].tolist()])
    X[[X.columns[(X.dtypes == 'float32') | (X.dtypes == 'float64') | (X.dtypes == 'int64')]][0].tolist()] = scaler_train.transform(X[[X.columns[(X.dtypes == 'float32') | (X.dtypes == 'float64') | (X.dtypes == 'int64')]][0].tolist()])
    

def read_data():
    file10000 = "data/feature_10000.csv"
    if os.path.exists(file10000):
        df_all = pd.read_csv(file10000)
    else:
        file_path="data/feature.csv"
        df = pd.read_csv(file_path)
        print(df.shape)
        df = df[:10000]
        df_all = df.rename(columns=lambda x: x.lower())
        df_all['is_black_sample'] = np.random.randint(low=0,high=2,size=(df_all.shape[0]))  #随机生成标签
        df_all.to_csv(file10000,index=False)
    return df_all


def make_data(df_all):
    """数据制造
    """
    col_type_int = ['is_team_ip', 'is_self_ml', 'is_ii_metal', 'is_outlier_sum_amt_up_atm',
           'is_lvt_mental', 'is_merch_diff_opp', 'is_empty_id',
           'is_diff_open_location', 'is_cash_then_tran_fore', 'is_fre_fore_cash',
           'is_trans_atm_opp_sus', 'is_outlier_cnt_txn_up_atm',
           'is_free_trade_zone', 'is_salary_fre', 'is_diff_open_state','id_ddl_day_count', 'id_ddl_day_count','trace_day_1','trace_day_3','trace_day_10','trace_day_30']
    
    for ci in col_type_int:
        df_all[ci] = random.choices(string.digits, k=df_all.shape[0])
    
    col_type_cat = ['id_type', 'country_residence', 'occupation', 'industry', 'cur_risk_level','nationality','count_country_trans']
    for cc in col_type_cat:
        df_all[cc] = random.choices(string.digits, k=df_all.shape[0])
    
    col_remove = ['prop_merch_sus_count', 'is_id_expire', 'is_ctoi_sus', 'is_same_corp_tel']
    for cc in col_remove:
        df_all[cc] = random.choices(string.digits, k=df_all.shape[0])
    
    cor_remove_corr = ['out_count', 'third_trans_count', 'count_e_trans', 'sum_of_total_amt_receive', 'sum_of_total_amt_pay', 'sum_e_trans', 'is_non_resident', 'is_fore_open', 'sum_country_trans', 'trans_directcity_count', 'count_of_trans_opp_pay', 'is_rep_is_share', 'prop_merch_special_amt']
    for cc in cor_remove_corr:
        df_all[cc] = random.choices(string.digits, k=df_all.shape[0])
    
    not_in_cols = ['count_multi_open', 'in_count', 'count_of_opp_region', 'trans_city_count', 'count_ii_iii_acct', 'trace_day_10.0', 'trans_directcountry_count', 'trace_day_3.0', 'trans_country_count', 'is_overage', 'trace_day_30.0', 'is_reg_open_intrenal', 'trace_day_1.0']
    for cc in not_in_cols:
        df_all[cc] = np.random.randint(low=0,high=2,size=(df_all.shape[0]))




def data_split(df_all, v_date = '2015-08-01', split=0.8, col_lable="is_black_sample"):
    """
    return
    ---------------------
    - X_train,Y_train,X_test,Y_test,X_valid,Y_valid,df_train,df_test
    - df_train,df_test是正负样本客户分开的训练集与测试集，从中拆分出了X_train,Y_train,X_test,Y_test
    - 
    
    """
    # 本代码中将标签当作了数字而不是类型
    df_all[col_lable]  =df_all[col_lable].astype(int)
    
    # 将回溯日期大于2023-08-26的好样本划分为验证集
    df_validation = df_all[(df_all['target_dt']> v_date) & (df_all[col_lable] == 0) ]
    print("df_validation.shape",df_validation.shape)

    # 对于剩下的数据，按客户号的划分出好样本涉及的客户，与坏样本涉及的客户池
    white_pool = pd.unique(df_all[(df_all['target_dt']<= v_date) & (df_all[col_lable]== 0)]['index_id'])
    black_pool = pd.unique(df_all[df_all[col_lable]== 1]['index_id'])  #这里以全局的角度看客户 如果一个客户出现过坏样本 那它就是坏客户，这两个集合应该会有交集  应该做去重 但这里没有做


    # 从好样本池与坏样本池中分别抽取出80%的客户
    np.random.seed(1)
    white_train = np.random.choice(white_pool,round(len(white_pool)*split),replace = False) # white party_id used for train_set
    black_train = np.random.choice(black_pool,round(len(black_pool)*split),replace = False) # black party_id used for train_set
    

    # 上述客户分别将作为好坏样本加入训练集
    df_train = df_all[(df_all['target_dt'] <= v_date) & 
                      (
                      ((df_all[col_lable] == 0) & df_all['index_id'].isin(white_train)) | 
                      ((df_all[col_lable] == 1) & df_all['index_id'].isin(black_train)) 
                      )
                     ]


    # 将好样本池与坏样本池中余下的20%客户分别作为好坏样本加入测试集
    df_test = df_all[(df_all['target_dt'] <= v_date) & 
                      (
                      ((df_all[col_lable] == 0) & (~df_all['index_id'].isin(white_train))) | 
                      ((df_all[col_lable] == 1) & (~df_all['index_id'].isin(black_train))) 
                      )
                     ]

    # 剔除无关变量，定义训练集、测试集、验证集中的潜在入模特征“X”与目标变量“Y”
    Y_train = df_train[col_lable]
    Y_test = df_test[col_lable]
    df_valid = df_validation
    Y_valid = df_validation[col_lable]
    df_train.drop(columns=[col_lable],inplace=True)
    df_test.drop(columns=[col_lable],inplace=True)
    df_valid.drop(columns=[col_lable],inplace=True)
    return df_train,Y_train,df_test,Y_test,df_valid,Y_valid
        
    


def append_csv(new_data, file_path):
    """追加写csv文件，适合小数据量
    
    """
    if os.path.exists(file_path):
        # 读取现有的 CSV 文件
        existing_df = pd.read_csv(file_path)
    
        # 将新数据追加到现有的 DataFrame
        updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        updated_df = new_data
    
    # 将更新后的 DataFrame 写回到 CSV 文件
    updated_df.to_csv(file_path, index=False)

def random_yyyymmdd():
    """随机生成日期,从2000年起
    - 格式：yyyy-mm-dd
    """
    from datetime import datetime, timedelta
    # 定义日期的起始和结束年份（如果需要）
    start_year = 2000
    end_year = datetime.now().year
    
    # 生成随机的年份
    year = random.randint(start_year, end_year)
    
    # 生成随机的月份
    month = random.randint(1, 12)
    
    # 生成随机的天数（注意每个月的天数不同）
    # 使用calendar模块可以帮助我们确定每个月的天数，但这里为了简单起见，我们使用datetime的date方法结合try-except来处理非法日期
    day = random.randint(1, 28)  # 先假设一个月最多28天
    
    while True:
        try:
            # 尝试创建日期对象
            random_date = datetime(year, month, day)
            # 如果成功，则跳出循环
            break
        except ValueError:
            # 如果日期非法（比如2月30日），则增加天数并重试
            day += 1
            if day > 28:  # 如果超过28天还未成功，则重置为1并从新月的天数开始检查（这里可以更加优化，比如根据月份确定最大天数）
                day = 1
                # 注意：这个简单的重置逻辑在跨月时可能不正确，因为它没有考虑到不同月份的天数差异。
                # 一个更准确的做法是使用calendar模块来确定每个月的最大天数。
                # 但为了简洁起见，这里我们假设用户不会频繁生成跨月的随机日期，或者接受偶尔的非法日期重试。
                # 在实际应用中，应该使用更精确的逻辑来确定每个月的最大天数。
                # 然而，为了这个示例的完整性，我们在这里保留这个简单的重置逻辑，并指出其潜在的不足。
    
    # 实际上，上面的while循环和重置逻辑是不完美的。下面是一个更准确的做法：
    from calendar import monthrange
    
    # 生成随机的天数（使用monthrange来确定每个月的最大天数）
    day = random.randint(1, monthrange(year, month)[1])
    random_date = datetime(year, month, day)
    
    # 格式化日期为"YYYY-MM-DD"
    formatted_date = random_date.strftime("%Y-%m-%d")
    return formatted_date

# import pandas as pd

def append_csv(new_data, file_path):
    """追加写csv文件，适合小数据量
    
    """
    if os.path.exists(file_path):
        # 读取现有的 CSV 文件
        existing_df = pd.read_csv(file_path)
    
        # 将新数据追加到现有的 DataFrame
        updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        updated_df = new_data
    
    # 将更新后的 DataFrame 写回到 CSV 文件
    updated_df.to_csv(file_path, index=False)
    




