# 基于深度学习的商品房价格预测系统

本项目是一个基于深度学习的城市暴雨洪涝风险预测系统，通过分析台湾省历史商品房数据（来自kaggle），利用混合模型预测未来商品房价格，并提供三维房价热力图+动态趋势预测。

## 项目特性

1. **多模态预测模型**  
   - 基于LSTM的时间序列预测模型  
   - 基于Transformer的注意力机制模型  
   - 传统机器学习模型（随机森林、梯度提升树）作为基准对比

2. **多维度特征融合**  
   - 房屋属性：面积、房龄、户型、装修等级  
   - 地理位置：周边学校/商圈/交通设施密度、地铁可达性  
   - 经济指标：区域GDP、人口密度、失业率、房贷利率  
   - 时间特征：季节性周期、宏观经济波动

3. **数据源可靠**  
   - 数据量大（百万级样本）  
   - 多维度指标交叉验证

4. **交互式可视化分析**
   - 三维房价热力地图（基于经纬度坐标）
   - 动态趋势对比（按区域/房型/时间维度）
   - SHAP值特征重要性分析
5. **未来价格预测功能**  
   - 支持72小时滚动预测
   - 提供置信区间可视化

---

## 技术栈

| 层级       | 技术选型                  |
|------------|---------------------------|
| **后端**   | Flask + TensorFlow/Keras  |
| **数据库** | MySQL                     |
| **数据预处理** | Pandas + Scikit-learn   |
| **前端**   | React + Ant Design        |
| **部署**   | Docker + Nginx            |

---

## 项目结构
```

住房价格预测系统/

├─ 后端/                 # 后端服务核心代码

│  ├─ app/                # FastAPI应用入口

│  │  └─ main.py          # 主应用文件

│  ├─ config/             # 配置文件目录

│  │  └─ config.py        # 数据库/模型配置

│  ├─ models/             # 预测模型实现

│  │  ├─ lstm_model.py    # LSTM价格预测模型

│  │  ├─ transformer_model.py # Transformer模型

│  │  └─ traditional_models.py # 传统机器学习模型

│  └─ utils/              # 工具模块

│     └─ data_loader.py   # 数据加载器

├─ data/                 # 数据处理模块

│  ├─ raw_data/           # 原始数据目录

│  │  ├─ building_structure.csv # 房屋结构数据

│  │  ├─ economic_indicators.csv # 经济指标数据

│  │  ├─ houseprice.csv   # 历史房价数据

│  │  └─ ...              # 其他子表

│  └─ processed_data/     # 预处理后数据

│     └─ scaled_features.npy # 标准化特征

├─ frontend/             # 前端应用

│  ├─ src/                # 源码目录

│  │  ├─ components/      # React组件

│  │  │  ├─ MapChart.js   # 地图可视化组件

│  │  │  ├─ TrendGraph.js # 价格趋势组件

│  │  │  └─ ComparePanel.js # 多模型对比面板

│  │  ├─ services/        # API调用

│  │  └─ App.js           # 主应用组件

│  ├─ public/             # 静态资源

│  └─ package.json        # 依赖配置

├─ 脚本/                 # 数据处理脚本

│  ├─ data_integration.py # 多源数据融合

│  └─ feature_engineering.py # 特征工程

├─ 模型/                 # 训练好的模型

│  ├─ lstm_model.keras

│  ├─ transformer_model.keras

│  └─ ...                 # 其他模型文件

└─ README.md             # 项目说明文档
```
---

## 环境准备

### 系统要求


Python 3.8+

Node.js 16+

Docker Desktop 4.24+
### 后端环境


pip install flask mysql-connector-python tensorflow pandas scikit-learn
### 前端环境


cd frontend

npm install vue-chart-3 echarts
