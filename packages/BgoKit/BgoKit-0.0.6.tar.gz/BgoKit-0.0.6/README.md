
__description__ = 'BgoKit, A tool package for Bgolearn'
__documents__ = 'https://bgolearn.netlify.app/'
__author__ = 'Bin Cao, Advanced Materials Thrust, Hong Kong University of Science and Technology (Guangzhou)'
__author_email__ = 'binjacobcao@gmail.com'
__url__ = 'https://github.com/Bin-Cao/Bgolearn'

# 安装后, 通过此命令调用BGOsampling类
import Bgolearn.BGOsampling as BGOS
import pandas as pd

# 读入我们使用的数据
data = pd.read_csv('./data/data.csv') 
vs = pd.read_csv('./data/Visual_samples.csv')


# 在此研究中，变量是元素含量 ： Sn, Bi, In, Ti, 也就是前四列
x = data.iloc[:,:-2] # 这行代码读取前四列，是特征

y_T = data.iloc[:,-2] # 这行代码读取倒数第二列，是目标, 抗拉强度 T
y_E = data.iloc[:,-1] # 这行代码读取倒数第一列，是目标, 断裂延伸率 E

# 执行Bgolearn
Bgolearn = BGOS.Bgolearn() 


Mymodel_T = Bgolearn.fit(data_matrix = x, Measured_response = y_T, virtual_samples = vs, min_search=False)
score_T, rec_T = Mymodel_T.UCB() 

Mymodel_E = Bgolearn.fit(data_matrix = x, Measured_response = y_E, virtual_samples = vs, min_search=False)
score_E, rec_E = Mymodel_E.UCB() 

# 执行BgoKit
from BgoKit import ToolKit

Model = ToolKit.MultiOpt(vs,[score_T,score_E])
Model.BiSearch()
Model.plot_distribution()