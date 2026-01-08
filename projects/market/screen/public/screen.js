// 数据大屏 - 前端逻辑
const API_URL = 'http://localhost:3000/api/v1';

// 更新时间
function updateTime() {
  const now = new Date();
  document.getElementById('currentTime').textContent = 
    now.toLocaleString('zh-CN', { hour12: false });
}
updateTime();
setInterval(updateTime, 1000);

// 加载数据
async function loadData() {
  try {
    const [statsRes, pricesRes, risingRes, fallingRes] = await Promise.all([
      fetch(`${API_URL}/statistics/daily`).then(r => r.json()),
      fetch(`${API_URL}/prices/today`).then(r => r.json()),
      fetch(`${API_URL}/statistics/rankings?type=rising&limit=10`).then(r => r.json()),
      fetch(`${API_URL}/statistics/rankings?type=falling&limit=10`).then(r => r.json())
    ]);

    const stats = statsRes.data || {};
    const prices = pricesRes.data?.prices || [];
    const rising = risingRes.data || [];
    const falling = fallingRes.data || [];

    // 更新统计卡片
    document.getElementById('priceIndex').textContent = stats.price_index || '100.00';
    document.getElementById('priceChange').textContent = 
      `${stats.rising_percent > 0 ? '+' : ''}${stats.rising_percent || 0}%`;
    document.getElementById('totalTurnover').textContent = 
      `${((stats.total_turnover || 0) / 10000).toFixed(1)}万`;
    document.getElementById('totalVolume').textContent = 
      `${((stats.total_volume || 0) / 1000).toFixed(1)}万kg`;
    document.getElementById('totalProducts').textContent = stats.total_products || 0;

    // 更新涨跌分布饼图
    initPieChart(stats);

    // 更新品类均价
    initCategoryChart();

    // 更新排行榜
    initRankingChart('risingChart', rising, 'up');
    initRankingChart('fallingChart', falling, 'down');

    // 更新滚动列表
    updateScrollList(prices);

    // 更新成交额排行
    initVolumeChart(prices);

  } catch (error) {
    console.error('加载数据失败:', error);
  }
}

function initPieChart(stats) {
  const chart = echarts.init(document.getElementById('pieChart'));
  chart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: stats.rising_count || 0, name: '上涨', itemStyle: { color: '#ff4d4f' } },
        { value: stats.falling_count || 0, name: '下跌', itemStyle: { color: '#52c41a' } },
        { value: stats.flat_count || 0, name: '持平', itemStyle: { color: '#1890ff' } }
      ]
    }]
  });
}

function initCategoryChart() {
  const chart = echarts.init(document.getElementById('categoryChart'));
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['散茶', '紧压茶', '年份茶', '陈皮普洱'] },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [285.6, 520.3, 680.5, 420.8],
      itemStyle: { color: '#1890ff' }
    }]
  });
}

function initRankingChart(containerId, data, direction) {
  const chart = echarts.init(document.getElementById(containerId));
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: data.map(d => d.productName?.substring(0, 8) || '') },
    series: [{
      type: 'bar',
      data: data.map(d => d.changePercent),
      itemStyle: { 
        color: direction === 'up' ? '#ff4d4f' : '#52c41a'
      }
    }]
  });
}

function updateScrollList(prices) {
  const container = document.getElementById('scrollList');
  container.innerHTML = prices.slice(0, 15).map(p => `
    <div class="scroll-item">
      <span>${p.productName?.substring(0, 12) || ''}</span>
      <span>¥${p.price?.toFixed(2) || 0}</span>
      <span class="${p.direction === 'up' ? 'up' : p.direction === 'down' ? 'down' : ''}" style="color: ${p.direction === 'up' ? '#ff4d4f' : p.direction === 'down' ? '#52c41a' : '#fff'}">
        ${p.direction === 'up' ? '▲' : p.direction === 'down' ? '▼' : '-'} ${Math.abs(p.changePercent || 0).toFixed(2)}%
      </span>
    </div>
  `).join('');
}

function initVolumeChart(prices) {
  const chart = echarts.init(document.getElementById('volumeChart'));
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: prices.slice(0, 10).map(p => p.productName?.substring(0, 8)) },
    yAxis: { type: 'value' },
    series: [{
      type: 'line',
      data: prices.slice(0, 10).map(p => p.volume),
      smooth: true,
      itemStyle: { color: '#722ed1' }
    }]
  });
}

// 首次加载和定时刷新
loadData();
setInterval(loadData, 30000); // 30秒刷新
