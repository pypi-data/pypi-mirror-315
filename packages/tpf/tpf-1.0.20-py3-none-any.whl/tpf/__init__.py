"""
方法直接放tpf的__init__方法中
除以下两个
python基础方法，
data集获取方法 
"""
from tpf.box.base import stp 
from tpf.d1 import DataStat
from tpf.d1 import DataDeal
from tpf.d1 import pkl_load,pkl_save
#from tpf.dl import T 
from tpf.d1 import read,write
from tpf.d2 import mean_by_count
from tpf.ml import MlTrain 
from tpf.db import DbTools
from tpf.db import OracleDb

from tpf.box.fil import log

from tpf.metric import get_psi_bybins

from tpf.llm.openai import chat 
from tpf.llm.openai import chat_stream

from tpf.data import toolml as tml
from tpf.data.toolml import rules_clf2
from tpf.datasets import load_boston

from tpf.data.make import random_str_list

