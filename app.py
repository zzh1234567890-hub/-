<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>房价分析系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        .nav-pills .nav-link.active {
            background-color: #0d6efd;
        }
        .card {
            box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
            border: 1px solid rgba(0, 0, 0, 0.125);
        }
        #map {
            height: 500px;
            width: 100%;
        }
        .chart-container {
            position: relative;
            height: 400px;
            width: 100%;
        }
        .table-responsive {
            max-height: 600px;
            overflow-y: auto;
        }
        .prediction-result {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .model-comparison {
            max-height: 400px;
            overflow-y: auto;
        }
        .loading {
            text-align: center;
            padding: 20px;
        }
        .spinner-border {
            width: 3rem;
            height: 3rem;
        }
        .feature-group {
            border: 1px solid #dee2e6;
            border-radius: 0.375rem;
            padding: 15px;
            margin-bottom: 15px;
        }
        .prediction-models {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .model-result {
            flex: 1;
            min-width: 200px;
            padding: 10px;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            text-align: center;
        }
        .best-model {
            border-color: #28a745;
            background-color: #f8fff9;
        }
        .deep-learning-model {
            border-color: #007bff;
            background-color: #f0f8ff;
        }
        .user-info {
            color: white;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
            <div class="container">
                <a class="navbar-brand" href="#">🏠 房价分析系统</a>
                <div class="navbar-nav ms-auto">
                    <span class="navbar-text user-info me-3">
                        欢迎，{{ session.full_name or session.username }}！
                    </span>
                    <a class="btn btn-outline-light btn-sm" href="{{ url_for('logout') }}">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container">
            <ul class="nav nav-pills mb-4" id="mainTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="predict-tab" data-bs-toggle="pill" data-bs-target="#predict" type="button">房价预测</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="data-tab" data-bs-toggle="pill" data-bs-target="#data" type="button">数据管理</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="map-tab" data-bs-toggle="pill" data-bs-target="#map-section" type="button">地图展示</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="trend-tab" data-bs-toggle="pill" data-bs-target="#trend" type="button">价格走势</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="volume-tab" data-bs-toggle="pill" data-bs-target="#volume" type="button">成交量分析</button>
                </li>
            </ul>

            <div class="tab-content" id="mainTabContent">
                <!-- 房价预测模块 -->
                <div class="tab-pane fade show active" id="predict" role="tabpanel">
                    <div class="row">
                        <div class="col-md-8">
                            <div class="card">
                                <div class="card-header">
                                    <h5>房价预测输入</h5>
                                </div>
                                <div class="card-body">
                                    <form id="predictForm">
                                        <div class="feature-group">
                                            <h6>基本信息</h6>
                                            <div class="row">
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">土地面积(平方米)</label>
                                                    <input type="number" class="form-control" id="landArea" step="0.01" value="10">
                                                </div>
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">建物面积(平方米)</label>
                                                    <input type="number" class="form-control" id="buildingArea" step="0.01" value="80">
                                                </div>
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">房龄(年)</label>
                                                    <input type="number" class="form-control" id="age" value="10">
                                                </div>
                                            </div>
                                        </div>

                                        <div class="feature-group">
                                            <h6>房屋格局</h6>
                                            <div class="row">
                                                <div class="col-md-3 mb-3">
                                                    <label class="form-label">房间数</label>
                                                    <input type="number" class="form-control" id="rooms" value="3">
                                                </div>
                                                <div class="col-md-3 mb-3">
                                                    <label class="form-label">客厅数</label>
                                                    <input type="number" class="form-control" id="halls" value="2">
                                                </div>
                                                <div class="col-md-3 mb-3">
                                                    <label class="form-label">卫生间数</label>
                                                    <input type="number" class="form-control" id="bathrooms" value="2">
                                                </div>
                                                <div class="col-md-3 mb-3">
                                                    <label class="form-label">总楼层数</label>
                                                    <input type="number" class="form-control" id="totalFloors" value="10">
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-6 mb-3">
                                                    <label class="form-label">所在楼层</label>
                                                    <input type="number" class="form-control" id="floor" value="5">
                                                </div>
                                            </div>
                                        </div>

                                        <div class="feature-group">
                                            <h6>周边设施 (500米内)</h6>
                                            <div class="row">
                                                <div class="col-md-3 mb-3">
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="checkbox" id="schoolNearby">
                                                        <label class="form-check-label" for="schoolNearby">学校</label>
                                                    </div>
                                                </div>
                                                <div class="col-md-3 mb-3">
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="checkbox" id="parkNearby">
                                                        <label class="form-check-label" for="parkNearby">公园</label>
                                                    </div>
                                                </div>
                                                <div class="col-md-3 mb-3">
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="checkbox" id="busNearby">
                                                        <label class="form-check-label" for="busNearby">公交站</label>
                                                    </div>
                                                </div>
                                                <div class="col-md-3 mb-3">
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="checkbox" id="mrtNearby">
                                                        <label class="form-check-label" for="mrtNearby">捷运站</label>
                                                    </div>
                                                </div>
                                                <div class="col-md-3 mb-3">
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="checkbox" id="badFacilityNearby">
                                                        <label class="form-check-label" for="badFacilityNearby">嫌恶设施</label>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <div class="feature-group">
                                            <h6>经济指标</h6>
                                            <div class="row">
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">房贷利率(%)</label>
                                                    <input type="number" class="form-control" id="loanRate" step="0.01" value="2.5">
                                                </div>
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">失业率(%)</label>
                                                    <input type="number" class="form-control" id="unemploymentRate" step="0.01" value="3.5">
                                                </div>
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">便利设施指数</label>
                                                    <input type="number" class="form-control" id="convenienceIndex" step="0.1" value="3">
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">房价所得比</label>
                                                    <input type="number" class="form-control" id="priceIncomeRatio" step="0.1" value="15">
                                                </div>
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">贷款负担率(%)</label>
                                                    <input type="number" class="form-control" id="loanBurdenRatio" step="0.1" value="35">
                                                </div>
                                                <div class="col-md-4 mb-3">
                                                    <label class="form-label">平均收入(万元)</label>
                                                    <input type="number" class="form-control" id="averageIncome" step="1" value="100">
                                                </div>
                                            </div>
                                        </div>

                                        <div class="feature-group">
                                            <h6>时间信息</h6>
                                            <div class="row">
                                                <div class="col-md-6 mb-3">
                                                    <label class="form-label">年份</label>
                                                    <input type="number" class="form-control" id="year" value="2023" min="2010" max="2030">
                                                </div>
                                                <div class="col-md-6 mb-3">
                                                    <label class="form-label">月份</label>
                                                    <input type="number" class="form-control" id="month" value="6" min="1" max="12">
                                                </div>
                                            </div>
                                        </div>

                                        <button type="submit" class="btn btn-primary w-100">预测房价</button>
                                    </form>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-header">
                                    <h5>预测结果</h5>
                                </div>
                                <div class="card-body">
                                    <div id="predictionResults" style="display: none;">
                                        <div class="prediction-models" id="modelPredictions">
                                        </div>
                                    </div>

                                    <div id="modelInfo" class="mt-3">
                                        <h6>模型性能对比</h6>
                                        <div class="model-comparison">
                                            <div id="modelComparison"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 数据管理模块 -->
                <div class="tab-pane fade" id="data" role="tabpanel">
                    <div class="card">
                        <div class="card-header">
                            <div class="row align-items-center">
                                <div class="col-md-6">
                                    <h5>数据管理</h5>
                                </div>
                                <div class="col-md-6">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <select class="form-select" id="cityFilter">
                                                <option value="">所有城市</option>
                                            </select>
                                        </div>
                                        <div class="col-md-6">
                                            <input type="text" class="form-control" id="searchInput" placeholder="搜索地址...">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped table-hover">
                                    <thead class="table-dark">
                                        <tr>
                                            <th>ID</th>
                                            <th>交易日期</th>
                                            <th>县市</th>
                                            <th>乡镇市区</th>
                                            <th>地址</th>
                                            <th>建物面积</th>
                                            <th>总价</th>
                                            <th>单价</th>
                                            <th>房龄</th>
                                            <th>格局</th>
                                            <th>操作</th>
                                        </tr>
                                    </thead>
                                    <tbody id="dataTable">
                                    </tbody>
                                </table>
                            </div>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <div id="dataInfo"></div>
                                <nav>
                                    <ul class="pagination justify-content-center" id="pagination">
                                    </ul>
                                </nav>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 地图展示模块 -->
                <div class="tab-pane fade" id="map-section" role="tabpanel">
                    <div class="card">
                        <div class="card-header">
                            <div class="row align-items-center">
                                <div class="col-md-6">
                                    <h5>房价地图分布</h5>
                                </div>
                                <div class="col-md-6">
                                    <select class="form-select" id="mapCityFilter">
                                        <option value="">所有城市</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="mapLoading" class="loading">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">加载中...</span>
                                </div>
                                <p>正在加载地图数据...</p>
                            </div>
                            <div id="map" style="display: none;"></div>
                        </div>
                    </div>
                </div>

                <!-- 价格走势模块 -->
                <div class="tab-pane fade" id="trend" role="tabpanel">
                    <div class="card">
                        <div class="card-header">
                            <div class="row align-items-center">
                                <div class="col-md-6">
                                    <h5>房价走势分析</h5>
                                </div>
                                <div class="col-md-6">
                                    <select class="form-select" id="trendCityFilter">
                                        <option value="">所有城市</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="trendLoading" class="loading">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">加载中...</span>
                                </div>
                                <p>正在加载价格走势数据...</p>
                            </div>
                            <div class="chart-container">
                                <canvas id="trendChart" style="display: none;"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 成交量模块 -->
                <div class="tab-pane fade" id="volume" role="tabpanel">
                    <div class="card">
                        <div class="card-header">
                            <div class="row align-items-center">
                                <div class="col-md-6">
                                    <h5>成交量分析</h5>
                                </div>
                                <div class="col-md-6">
                                    <select class="form-select" id="volumeCityFilter">
                                        <option value="">所有城市</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="volumeLoading" class="loading">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">加载中...</span>
                                </div>
                                <p>正在加载成交量数据...</p>
                            </div>
                            <div class="chart-container">
                                <canvas id="volumeChart" style="display: none;"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 编辑模态框 -->
    <div class="modal fade" id="editModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">编辑记录</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="editForm">
                        <input type="hidden" id="editId">
                        <div class="mb-3">
                            <label class="form-label">总价(元)</label>
                            <input type="number" class="form-control" id="editTotalPrice">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">单价(元/平方米)</label>
                            <input type="number" class="form-control" id="editUnitPrice">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">建物面积(平方米)</label>
                            <input type="number" class="form-control" id="editBuildingArea" step="0.01">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">房龄(年)</label>
                            <input type="number" class="form-control" id="editAge">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" onclick="saveEdit()">保存</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentPage = 1;
        let map = null;
        let trendChart = null;
        let volumeChart = null;
        let cities = [];

        // 初始化
        document.addEventListener('DOMContentLoaded', function() {
            loadCities();
            loadModelInfo();

            // 搜索功能
            document.getElementById('searchInput').addEventListener('input', debounce(function() {
                currentPage = 1;
                loadData();
            }, 500));

            // 城市筛选
            document.getElementById('cityFilter').addEventListener('change', function() {
                currentPage = 1;
                loadData();
            });

            // 地图城市筛选
            document.getElementById('mapCityFilter').addEventListener('change', function() {
                if (map) {
                    initMap();
                }
            });

            // 走势图城市筛选
            document.getElementById('trendCityFilter').addEventListener('change', function() {
                if (trendChart) {
                    trendChart.destroy();
                    trendChart = null;
                }
                initTrendChart();
            });

            // 成交量城市筛选
            document.getElementById('volumeCityFilter').addEventListener('change', function() {
                if (volumeChart) {
                    volumeChart.destroy();
                    volumeChart = null;
                }
                initVolumeChart();
            });
        });

        // 防抖函数
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // 加载城市列表
        async function loadCities() {
            try {
                const response = await fetch('/api/cities');
                const result = await response.json();

                if (result.success) {
                    cities = result.cities;

                    // 更新所有城市选择器
                    const selectors = ['cityFilter', 'mapCityFilter', 'trendCityFilter', 'volumeCityFilter'];
                    selectors.forEach(selectorId => {
                        const selector = document.getElementById(selectorId);
                        selector.innerHTML = '<option value="">所有城市</option>';
                        cities.forEach(city => {
                            selector.innerHTML += `<option value="${city}">${city}</option>`;
                        });
                    });
                }
            } catch (error) {
                console.error('加载城市列表失败:', error);
            }
        }

        // 房价预测
        document.getElementById('predictForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const data = {
                land_area: document.getElementById('landArea').value,
                building_area: document.getElementById('buildingArea').value,
                age: document.getElementById('age').value,
                rooms: document.getElementById('rooms').value,
                halls: document.getElementById('halls').value,
                bathrooms: document.getElementById('bathrooms').value,
                total_floors: document.getElementById('totalFloors').value,
                floor: document.getElementById('floor').value,
                school_nearby: document.getElementById('schoolNearby').checked ? 1 : 0,
                park_nearby: document.getElementById('parkNearby').checked ? 1 : 0,
                bus_nearby: document.getElementById('busNearby').checked ? 1 : 0,
                mrt_nearby: document.getElementById('mrtNearby').checked ? 1 : 0,
                bad_facility_nearby: document.getElementById('badFacilityNearby').checked ? 1 : 0,
                loan_rate: document.getElementById('loanRate').value,
                unemployment_rate: document.getElementById('unemploymentRate').value,
                convenience_index: document.getElementById('convenienceIndex').value,
                price_income_ratio: document.getElementById('priceIncomeRatio').value,
                loan_burden_ratio: document.getElementById('loanBurdenRatio').value,
                average_income: document.getElementById('averageIncome').value,
                year: document.getElementById('year').value,
                month: document.getElementById('month').value
            };

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    displayPredictionResults(result);
                } else {
                    alert('预测失败: ' + result.error);
                }
            } catch (error) {
                alert('预测失败: ' + error.message);
            }
        });

        function displayPredictionResults(result) {
            const container = document.getElementById('modelPredictions');
            container.innerHTML = '';

            // 显示所有模型的预测结果
            for (const [modelName, prediction] of Object.entries(result.predictions)) {
                const isBest = modelName === result.best_traditional_model || modelName === result.best_deep_learning_model;
                const isDeepLearning = prediction.type === 'deep_learning';
                const modelDiv = document.createElement('div');

                let className = 'model-result';
                if (isBest) className += ' best-model';
                if (isDeepLearning) className += ' deep-learning-model';

                modelDiv.className = className;
                modelDiv.innerHTML = `
                    <h6>${getModelDisplayName(modelName)} ${isBest ? '(最佳)' : ''}</h6>
                    <h4>NT$ ${prediction.formatted}</h4>
                    <small>${isDeepLearning ? '深度学习' : '传统ML'}</small>
                `;
                container.appendChild(modelDiv);
            }

            document.getElementById('predictionResults').style.display = 'block';
        }

        function getModelDisplayName(modelName) {
            const names = {
                'random_forest': '随机森林',
                'gradient_boosting': '梯度提升',
                'linear_regression': '线性回归',
                'svr': '支持向量回归',
                'neural_network': '神经网络'
            };
            return names[modelName] || modelName;
        }

        // 加载模型信息
        async function loadModelInfo() {
            try {
                const response = await fetch('/api/model_info');
                const result = await response.json();

                if (result.success) {
                    const container = document.getElementById('modelComparison');
                    container.innerHTML = '';

                    // 显示传统机器学习模型
                    if (result.model_scores.traditional) {
                        container.innerHTML += '<h6 class="text-primary">传统机器学习模型</h6>';
                        for (const [modelName, scores] of Object.entries(result.model_scores.traditional)) {
                            const isBest = modelName === result.best_traditional_model;
                            container.innerHTML += `
                                <div class="mb-2 p-2 ${isBest ? 'bg-light border' : ''}">
                                    <strong>${getModelDisplayName(modelName)} ${isBest ? '(最佳)' : ''}</strong><br>
                                    <small>R²: ${scores.r2_score.toFixed(4)} | RMSE: ${scores.rmse.toFixed(0)}</small>
                                </div>
                            `;
                        }
                    }

                    // 显示深度学习模型
                    if (result.model_scores.deep_learning && Object.keys(result.model_scores.deep_learning).length > 0) {
                        container.innerHTML += '<h6 class="text-info mt-3">深度学习模型</h6>';
                        for (const [modelName, scores] of Object.entries(result.model_scores.deep_learning)) {
                            const isBestDL = modelName === result.best_deep_learning_model;
                            container.innerHTML += `
                                <div class="mb-2 p-2 ${isBestDL ? 'bg-info bg-opacity-10 border border-info' : ''}">
                                    <strong>${getModelDisplayName(modelName)} ${isBestDL ? '(最佳DL)' : ''}</strong><br>
                                    <small>R²: ${scores.r2_score.toFixed(4)} | RMSE: ${scores.rmse.toFixed(0)} | Epochs: ${scores.epochs_trained || 'N/A'}</small>
                                </div>
                            `;
                        }
                    }

                    if (!result.tensorflow_available) {
                        container.innerHTML += '<div class="alert alert-warning mt-2"><small>TensorFlow 不可用，无法使用深度学习模型</small></div>';
                    }
                }
            } catch (error) {
                console.error('加载模型信息失败:', error);
            }
        }

        // 数据管理
        async function loadData(page = 1) {
            try {
                const search = document.getElementById('searchInput').value;
                const city = document.getElementById('cityFilter').value;

                const params = new URLSearchParams({
                    page: page,
                    limit: 20
                });

                if (search) params.append('search', search);
                if (city) params.append('city', city);

                const response = await fetch(`/api/data?${params}`);
                const result = await response.json();

                if (result.success) {
                    const tbody = document.getElementById('dataTable');
                    tbody.innerHTML = '';

                    result.data.forEach(row => {
                        const tr = document.createElement('tr');

                        const getValue = (row, key, defaultValue = '-') => {
                            const value = row[key];
                            if (value === null || value === undefined) return defaultValue;
                            return value;
                        };

                        const formatNumber = (value) => {
                            if (value === null || value === undefined || value === '-') return '-';
                            if (value === 0) return '0';
                            return typeof value === 'number' ? value.toLocaleString() : value;
                        };

                        const ageValue = getValue(row, '房龄', 0);
                        const displayAge = ageValue === 0 ? '0' : ageValue;

                        tr.innerHTML = `
                            <td>${getValue(row, 'ID')}</td>
                            <td>${getValue(row, '交易年月日')}</td>
                            <td>${getValue(row, '县市')}</td>
                            <td>${getValue(row, '乡镇市区')}</td>
                            <td title="${getValue(row, '土地位置建物门牌')}">
                                ${getValue(row, '土地位置建物门牌').toString().substring(0, 20)}...
                            </td>
                            <td>${formatNumber(getValue(row, '建物移转总面积平方公尺'))}</td>
                            <td>${formatNumber(getValue(row, '总价元'))}</td>
                            <td>${formatNumber(getValue(row, '单价元平方公尺'))}</td>
                            <td>${displayAge}</td>
                            <td>${getValue(row, '建物现况格局_房', 0)}房${getValue(row, '建物现况格局_厅', 0)}厅${getValue(row, '建物现况格局_卫', 0)}卫</td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button class="btn btn-sm btn-outline-primary"
                                        onclick="editRecord(${getValue(row, 'ID')}, '${getValue(row, '总价元')}', '${getValue(row, '单价元平方公尺')}', '${getValue(row, '建物移转总面积平方公尺')}', '${ageValue}')">
                                        编辑
                                    </button>
                                    <button class="btn btn-sm btn-outline-danger"
                                        onclick="deleteRecord(${getValue(row, 'ID')})">
                                        删除
                                    </button>
                                </div>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });

                document.getElementById('dataInfo').innerHTML = `
                    <small class="text-muted">
                        显示第 ${(page-1)*20 + 1}-${Math.min(page*20, result.total)} 条，共 ${result.total} 条记录
                    </small>
                `;
                updatePagination(result.page, Math.ceil(result.total / result.limit));
                currentPage = result.page;
            }
        } catch (error) {
            console.error('加载数据失败:', error);
            document.getElementById('dataTable').innerHTML = `
                <tr><td colspan="11" class="text-center text-danger">加载数据失败: ${error.message}</td></tr>
            `;
        }
    }

        function updatePagination(currentPage, totalPages) {
            const pagination = document.getElementById('pagination');
            pagination.innerHTML = '';

            if (currentPage > 1) {
                const li = document.createElement('li');
                li.className = 'page-item';
                li.innerHTML = `<a class="page-link" href="#" onclick="loadData(${currentPage - 1})">上一页</a>`;
                pagination.appendChild(li);
            }

            const start = Math.max(1, currentPage - 2);
            const end = Math.min(totalPages, currentPage + 2);

            for (let i = start; i <= end; i++) {
                const li = document.createElement('li');
                li.className = `page-item ${i === currentPage ? 'active' : ''}`;
                li.innerHTML = `<a class="page-link" href="#" onclick="loadData(${i})">${i}</a>`;
                pagination.appendChild(li);
            }

            if (currentPage < totalPages) {
                const li = document.createElement('li');
                li.className = 'page-item';
                li.innerHTML = `<a class="page-link" href="#" onclick="loadData(${currentPage + 1})">下一页</a>`;
                pagination.appendChild(li);
            }
        }

        function editRecord(id, totalPrice, unitPrice, buildingArea, age) {
            document.getElementById('editId').value = id;
            document.getElementById('editTotalPrice').value = totalPrice;
            document.getElementById('editUnitPrice').value = unitPrice;
            document.getElementById('editBuildingArea').value = buildingArea;
            document.getElementById('editAge').value = age;

            new bootstrap.Modal(document.getElementById('editModal')).show();
        }

        async function saveEdit() {
            try {
                const data = {
                    id: document.getElementById('editId').value,
                    total_price: document.getElementById('editTotalPrice').value,
                    unit_price: document.getElementById('editUnitPrice').value,
                    building_area: document.getElementById('editBuildingArea').value,
                    age: document.getElementById('editAge').value
                };

                const response = await fetch('/api/update_record', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                if (result.success) {
                    bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
                    loadData(currentPage);
                    alert('更新成功');
                } else {
                    alert('更新失败');
                }
            } catch (error) {
                alert('更新失败: ' + error.message);
            }
        }

        async function deleteRecord(id) {
            if (confirm('确定要删除这条记录吗？')) {
                try {
                    const response = await fetch('/api/delete_record', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({id: id})
                    });

                    const result = await response.json();
                    if (result.success) {
                        loadData(currentPage);
                        alert('删除成功');
                    } else {
                        alert('删除失败');
                    }
                } catch (error) {
                    alert('删除失败: ' + error.message);
                }
            }
        }

        // 地图展示
        async function initMap() {
            document.getElementById('mapLoading').style.display = 'block';
            document.getElementById('map').style.display = 'none';

            if (map) {
                map.remove();
                map = null;
            }

            try {
                const city = document.getElementById('mapCityFilter').value;
                const params = city ? `?city=${encodeURIComponent(city)}` : '';

                const response = await fetch(`/api/map_data${params}`);
                const result = await response.json();

                if (result.success && result.data && result.data.length > 0) {
                    const validData = result.data.filter(point =>
                        point.纬度 && point.经度 &&
                        !isNaN(point.纬度) && !isNaN(point.经度) &&
                        point.纬度 > 20 && point.纬度 < 30 &&
                        point.经度 > 115 && point.经度 < 125
                    );

                    if (validData.length > 0) {
                        const lats = validData.map(p => parseFloat(p.纬度));
                        const lngs = validData.map(p => parseFloat(p.经度));

                        const centerLat = lats.reduce((a, b) => a + b, 0) / lats.length;
                        const centerLng = lngs.reduce((a, b) => a + b, 0) / lngs.length;

                        map = L.map('map').setView([centerLat, centerLng], 11);

                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            attribution: '© OpenStreetMap contributors',
                            maxZoom: 18
                        }).addTo(map);

                        validData.forEach(point => {
                            const lat = parseFloat(point.纬度);
                            const lng = parseFloat(point.经度);

                            const price = point.总价元 ? parseFloat(point.总价元).toLocaleString() : '未知';
                            const unitPrice = point.单价元平方公尺 ? parseFloat(point.单价元平方公尺).toLocaleString() : '未知';
                            const age = point.房龄 || '未知';

                            L.marker([lat, lng])
                                .addTo(map)
                                .bindPopup(`
                                    <div style="min-width: 200px;">
                                        <b>${point.县市} ${point.乡镇市区}</b><br>
                                        地址: ${point.土地位置建物门牌 || '未知'}<br>
                                        总价: NT$ ${price}<br>
                                        单价: NT$ ${unitPrice}/㎡<br>
                                        建物面积: ${point.建物移转总面积平方公尺 || '-'} ㎡<br>
                                        房龄: ${age} 年
                                    </div>
                                `);
                        });

                        document.getElementById('map').style.display = 'block';

                        setTimeout(() => {
                            map.invalidateSize();
                        }, 100);

                    } else {
                        document.getElementById('map').innerHTML = '<div class="text-center p-4">没有找到有效的地图数据</div>';
                        document.getElementById('map').style.display = 'block';
                    }
                } else {
                    document.getElementById('map').innerHTML = '<div class="text-center p-4">没有找到地图数据</div>';
                    document.getElementById('map').style.display = 'block';
                }
            } catch (error) {
                console.error('加载地图数据失败:', error);
                document.getElementById('map').innerHTML = `<div class="text-center p-4 text-danger">加载地图数据失败: ${error.message}</div>`;
                document.getElementById('map').style.display = 'block';
            } finally {
                document.getElementById('mapLoading').style.display = 'none';
            }
        }

        // 价格走势图
        async function initTrendChart() {
            document.getElementById('trendLoading').style.display = 'block';
            document.getElementById('trendChart').style.display = 'none';

            try {
                const city = document.getElementById('trendCityFilter').value;
                const params = city ? `?city=${encodeURIComponent(city)}` : '';

                const response = await fetch(`/api/price_trend${params}`);
                const result = await response.json();

                if (result.success && result.data && Object.keys(result.data).length > 0) {
                    const ctx = document.getElementById('trendChart').getContext('2d');
                    const datasets = [];
                    const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];

                    let colorIndex = 0;
                    for (const [cityName, data] of Object.entries(result.data)) {
                        if (data && data.length > 1) {
                            datasets.push({
                                label: cityName,
                                data: data.map(d => ({
                                    x: d.date,
                                    y: parseFloat(d.price)
                                })),
                                borderColor: colors[colorIndex % colors.length],
                                backgroundColor: colors[colorIndex % colors.length] + '20',
                                fill: false,
                                tension: 0.1
                            });
                            colorIndex++;
                        }
                    }

                    if (datasets.length > 0) {
                        if (trendChart) {
                            trendChart.destroy();
                        }

                        trendChart = new Chart(ctx, {
                            type: 'line',
                            data: { datasets: datasets },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                interaction: {
                                    intersect: false,
                                    mode: 'index'
                                },
                                scales: {
                                    x: {
                                        type: 'time',
                                        time: {
                                            parser: 'yyyy-MM-dd',
                                            displayFormats: {
                                                month: 'yyyy-MM'
                                            }
                                        },
                                        title: {
                                            display: true,
                                            text: '时间'
                                        }
                                    },
                                    y: {
                                        title: {
                                            display: true,
                                            text: '单价 (元/平方米)'
                                        },
                                        beginAtZero: false
                                    }
                                },
                                plugins: {
                                    title: {
                                        display: true,
                                        text: city ? `${city} 房价走势` : '各城市房价走势'
                                    },
                                    legend: {
                                        display: true,
                                        position: 'top'
                                    }
                                }
                            }
                        });

                        document.getElementById('trendChart').style.display = 'block';
                    } else {
                        document.getElementById('trendChart').parentElement.innerHTML = '<div class="text-center p-4">没有足够的数据显示走势图</div>';
                    }
                } else {
                    document.getElementById('trendChart').parentElement.innerHTML = '<div class="text-center p-4">没有找到价格走势数据</div>';
                }
            } catch (error) {
                console.error('加载价格走势失败:', error);
                document.getElementById('trendChart').parentElement.innerHTML = `<div class="text-center p-4 text-danger">加载价格走势数据失败: ${error.message}</div>`;
            } finally {
                document.getElementById('trendLoading').style.display = 'none';
            }
        }

        // 成交量图表
        async function initVolumeChart() {
            document.getElementById('volumeLoading').style.display = 'block';
            document.getElementById('volumeChart').style.display = 'none';

            try {
                const city = document.getElementById('volumeCityFilter').value;
                const params = city ? `?city=${encodeURIComponent(city)}` : '';

                const response = await fetch(`/api/transaction_volume${params}`);
                const result = await response.json();

                if (result.success && result.data.length > 0) {
                    const ctx = document.getElementById('volumeChart').getContext('2d');
                    const labels = result.data.map(d => `${d.县市} ${d.乡镇市区}`);
                    const volumes = result.data.map(d => d.volume);
                    const avgPrices = result.data.map(d => d.avg_price || 0);

                    volumeChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: '成交量',
                                data: volumes,
                                backgroundColor: '#36A2EB',
                                borderColor: '#36A2EB',
                                borderWidth: 1,
                                yAxisID: 'y'
                            }, {
                                label: '平均单价 (元/㎡)',
                                data: avgPrices,
                                type: 'line',
                                borderColor: '#FF6384',
                                backgroundColor: '#FF6384',
                                yAxisID: 'y1',
                                fill: false
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            interaction: {
                                intersect: false,
                                mode: 'index'
                            },
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: '地区'
                                    }
                                },
                                y: {
                                    type: 'linear',
                                    display: true,
                                    position: 'left',
                                    title: {
                                        display: true,
                                        text: '成交量'
                                    },
                                    beginAtZero: true
                                },
                                y1: {
                                    type: 'linear',
                                    display: true,
                                    position: 'right',
                                    title: {
                                        display: true,
                                        text: '平均单价 (元/㎡)'
                                    },
                                    grid: {
                                        drawOnChartArea: false,
                                    },
                                }
                            },
                            plugins: {
                                title: {
                                    display: true,
                                    text: city ? `${city} 成交量统计` : '各地区成交量统计'
                                },
                                legend: {
                                    display: true,
                                    position: 'top'
                                }
                            }
                        }
                    });

                    document.getElementById('volumeChart').style.display = 'block';
                } else {
                    document.getElementById('volumeChart').parentElement.innerHTML = '<div class="text-center p-4">没有找到成交量数据</div>';
                }
            } catch (error) {
                console.error('加载成交量数据失败:', error);
                document.getElementById('volumeChart').parentElement.innerHTML = '<div class="text-center p-4 text-danger">加载成交量数据失败</div>';
            } finally {
                document.getElementById('volumeLoading').style.display = 'none';
            }
        }

        // 标签页切换事件
        const tabTriggerList = [].slice.call(document.querySelectorAll('#mainTabs button'));
        tabTriggerList.forEach(function(tabTrigger) {
            tabTrigger.addEventListener('shown.bs.tab', function(event) {
                const target = event.target.getAttribute('data-bs-target');

                switch(target) {
                    case '#predict':
                        break;
                    case '#data':
                        if (document.getElementById('dataTable').children.length === 0) {
                            loadData();
                        }
                        break;
                    case '#map-section':
                        if (!map) {
                            setTimeout(initMap, 100);
                        }
                        break;
                    case '#trend':
                        if (!trendChart) {
                            setTimeout(initTrendChart, 100);
                        }
                        break;
                    case '#volume':
                        if (!volumeChart) {
                            setTimeout(initVolumeChart, 100);
                        }
                        break;
                }
            });
        });
    </script>
</body>
</html>
