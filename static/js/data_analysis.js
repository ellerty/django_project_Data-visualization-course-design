// static/js/data_analysis.js
document.addEventListener('DOMContentLoaded', function () {

    function fetchAndRenderGrowthChart() {
        fetch('/api/growth-top-30/')
            .then(response => response.json())
            .then(data => {
                console.log('Growth Data:', data); // 调试
                var ctx = document.getElementById('growth-chart').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.map(item => item.name),
                        datasets: [{
                            label: '财富增长（美元）',
                            data: data.map(item => item.last_change),
                            backgroundColor: data.map(item => item.last_change >= 0 ? 'rgba(75, 192, 192, 0.6)' : 'rgba(255, 99, 132, 0.6)'),
                            borderColor: data.map(item => item.last_change >= 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)'),
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value, index, values) {
                                        return '$' + value.toLocaleString();
                                    }
                                },
                                title: {
                                    display: true,
                                    text: '财富变化 (USD)'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: '富豪'
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        let value = context.parsed.y;
                                        let formattedValue = value >= 0 ? `+${value.toLocaleString()}` : value.toLocaleString();
                                        return `财富变化: ${formattedValue} USD`;
                                    }
                                }
                            },
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching growth data:', error));
    }

    function fetchAndRenderWealthChart() {
        fetch('/api/wealth-top-30/')
            .then(response => response.json())
            .then(data => {
                console.log('Wealth Data:', data); // 调试
                var ctx = document.getElementById('wealth-chart').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.map(item => item.name),
                        datasets: [{
                            label: '总财富（美元）',
                            data: data.map(item => item.total_net_worth),
                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value, index, values) {
                                        return '$' + value.toLocaleString();
                                    }
                                },
                                title: {
                                    display: true,
                                    text: '总财富 (USD)'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: '富豪'
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        let value = context.parsed.y;
                                        let formattedValue = value.toLocaleString();
                                        return `总财富: ${formattedValue} USD`;
                                    }
                                }
                            },
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching wealth data:', error));
    }

    function fetchAndRenderIndustryChart() {
        fetch('/api/industry-proportion/')
            .then(response => response.json())
            .then(data => {
                console.log('Industry Data:', data); // 调试
                var ctx = document.getElementById('industry-chart').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'pie', // 饼状图
                    data: {
                        labels: data.map(item => item.industry),
                        datasets: [{
                            label: '各行业占比',
                            data: data.map(item => item.count),
                            backgroundColor: generateColorArray(data.length),
                            borderColor: '#ffffff',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        let label = context.label || '';
                                        let value = context.parsed;
                                        let total = context.chart._metasets[context.datasetIndex].total;
                                        let percentage = ((value / total) * 100).toFixed(2) + '%';
                                        return `${label}: ${percentage}`;
                                    }
                                }
                            }
                        }
                    }
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

    fetchAndRenderGrowthChart();
    fetchAndRenderWealthChart();
    fetchAndRenderIndustryChart();
});
