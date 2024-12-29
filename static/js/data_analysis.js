// static/js/data_analysis.js
document.addEventListener('DOMContentLoaded', function () {

    // 初始化所有图表
    function initCharts() {
        fetchAndRenderGrowthChart();
        fetchAndRenderWealthChart();
        fetchAndRenderIndustryChart();
    }

    // 使用 ECharts 渲染财富增长柱状图
    function fetchAndRenderGrowthChart() {
        fetch('/api/growth-top-30/')
            .then(response => response.json())
            .then(data => {
                console.log('Growth Data:', data); // 调试

                // 获取图表容器
                var chartDom = document.getElementById('growth-chart');
                var myChart = echarts.init(chartDom);

                // 准备数据
                var names = data.map(item => item.name);
                var growthData = data.map(item => item.last_change);
                var colors = growthData.map(value => value >= 0 ? 'rgba(75, 192, 192, 0.6)' : 'rgba(255, 99, 132, 0.6)');
                var borderColors = growthData.map(value => value >= 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)');

                // 配置图表选项
                var option = {
                    title: {
                        text: '财富增长（美元）',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            var param = params[0];
                            var value = param.data;
                            var formattedValue = value >= 0 ? `+${value.toLocaleString()}` : value.toLocaleString();
                            return `${param.name}<br/>财富变化: ${formattedValue} USD`;
                        },
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    xAxis: {
                        type: 'category',
                        data: names,
                        name: '富豪',
                        axisLabel: {
                            interval: 0,
                            rotate: 45
                        }
                    },
                    yAxis: {
                        type: 'value',
                        name: '财富变化 (USD)',
                        axisLabel: {
                            formatter: function (value) {
                                return '$' + value.toLocaleString();
                            }
                        },
                        min: 0
                    },
                    series: [{
                        data: growthData,
                        type: 'bar',
                        itemStyle: {
                            color: function (params) {
                                return colors[params.dataIndex];
                            },
                            borderColor: function (params) {
                                return borderColors[params.dataIndex];
                            },
                            borderWidth: 1
                        }
                    }],
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '15%',
                        containLabel: true
                    }
                };

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);

                // 使图表自适应大小
                window.addEventListener('resize', function () {
                    myChart.resize();
                });
            })
            .catch(error => console.error('Error fetching growth data:', error));
    }

    // 使用 ECharts 渲染总财富柱状图
    function fetchAndRenderWealthChart() {
        fetch('/api/wealth-top-30/')
            .then(response => response.json())
            .then(data => {
                console.log('Wealth Data:', data); // 调试

                // 获取图表容器
                var chartDom = document.getElementById('wealth-chart');
                var myChart = echarts.init(chartDom);

                // 准备数据
                var names = data.map(item => item.name);
                var wealthData = data.map(item => item.total_net_worth);
                var colors = 'rgba(255, 99, 132, 0.6)';

                // 配置图表选项
                var option = {
                    title: {
                        text: '总财富（美元）',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            var param = params[0];
                            var value = param.data;
                            var formattedValue = value.toLocaleString();
                            return `${param.name}<br/>总财富: ${formattedValue} USD`;
                        },
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    xAxis: {
                        type: 'category',
                        data: names,
                        name: '富豪',
                        axisLabel: {
                            interval: 0,
                            rotate: 45
                        }
                    },
                    yAxis: {
                        type: 'value',
                        name: '总财富 (USD)',
                        axisLabel: {
                            formatter: function (value) {
                                return '$' + value.toLocaleString();
                            }
                        },
                        min: 0
                    },
                    series: [{
                        data: wealthData,
                        type: 'bar',
                        itemStyle: {
                            color: colors,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1
                        }
                    }],
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '15%',
                        containLabel: true
                    }
                };

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);

                // 使图表自适应大小
                window.addEventListener('resize', function () {
                    myChart.resize();
                });
            })
            .catch(error => console.error('Error fetching wealth data:', error));
    }

    // 使用 ECharts 渲染行业占比饼图
    function fetchAndRenderIndustryChart() {
        fetch('/api/industry-proportion/')
            .then(response => response.json())
            .then(data => {
                console.log('Industry Data:', data); // 调试

                // 获取图表容器
                var chartDom = document.getElementById('industry-chart');
                var myChart = echarts.init(chartDom);

                // 准备数据
                var industryData = data.map(item => ({
                    name: item.industry,
                    value: item.count
                }));

                // 生成颜色数组
                var colors = generateColorArray(industryData.length);

                // 配置图表选项
                var option = {
                    title: {
                        text: '各行业占比',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: function (params) {
                            var percentage = ((params.value / params.total) * 100).toFixed(2) + '%';
                            return `${params.name}: ${percentage}`;
                        }
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left'
                    },
                    series: [
                        {
                            name: '行业占比',
                            type: 'pie',
                            radius: '50%',
                            data: industryData,
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            },
                            label: {
                                formatter: '{b}: {d}%',
                                color: '#000'
                            },
                            itemStyle: {
                                borderColor: '#ffffff',
                                borderWidth: 1
                            },
                            color: colors
                        }
                    ]
                };

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);

                // 使图表自适应大小
                window.addEventListener('resize', function () {
                    myChart.resize();
                });
            })
            .catch(error => console.error('Error fetching industry data:', error));
    }

    // 预定义颜色数组，循环使用
    function generateColorArray(num) {
        const predefinedColors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)',
            'rgba(199, 199, 199, 0.6)',
            'rgba(83, 102, 255, 0.6)',
            'rgba(255, 99, 71, 0.6)',
            'rgba(60, 179, 113, 0.6)'
        ];
        let colors = [];
        for (let i = 0; i < num; i++) {
            colors.push(predefinedColors[i % predefinedColors.length]);
        }
        return colors;
    }

    // 初始化所有图表
    initCharts();
});
