<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>品牌銷售 & 廣告 Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#ffffff;--bg2:#f5f5f4;--bg3:#eeede9;
  --text:#1a1a18;--text2:#57564f;--text3:#888780;
  --border:rgba(0,0,0,0.12);--border2:rgba(0,0,0,0.2);
  --radius:8px;--radius-lg:12px;
  --mi:#185FA5;--nb:#0F6E56;--ds:#993C1D;
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#1c1c1a;--bg2:#252522;--bg3:#2e2e2b;
    --text:#f0ede8;--text2:#a8a69f;--text3:#706e68;
    --border:rgba(255,255,255,0.1);--border2:rgba(255,255,255,0.2);
  }
}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg3);color:var(--text);font-size:14px;min-height:100vh}
a{color:inherit;text-decoration:none}
/* Layout */
.app{display:flex;flex-direction:column;min-height:100vh}
.topbar{background:var(--bg);border-bottom:0.5px solid var(--border);padding:0 24px;display:flex;align-items:center;gap:0;height:52px;position:sticky;top:0;z-index:100}
.logo{font-size:15px;font-weight:600;color:var(--text);letter-spacing:-0.3px;margin-right:24px;white-space:nowrap}
.nav-tabs{display:flex;gap:0;flex:1}
.nav-tab{padding:0 16px;height:52px;display:flex;align-items:center;font-size:13px;color:var(--text2);cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap;transition:color 0.15s}
.nav-tab:hover{color:var(--text)}
.nav-tab.active{color:var(--text);border-bottom-color:var(--mi);font-weight:500}
.content{flex:1;padding:20px 24px}
/* Pages */
.page{display:none}.page.active{display:block}
/* Metric cards */
.metric-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:16px}
.mcard{background:var(--bg2);border-radius:var(--radius);padding:14px 16px}
.mcard-label{font-size:11px;color:var(--text3);margin-bottom:5px;text-transform:uppercase;letter-spacing:0.04em}
.mcard-val{font-size:22px;font-weight:600;color:var(--text);letter-spacing:-0.5px}
.mcard-sub{font-size:11px;margin-top:3px}
.up{color:#3B6D11}.down{color:#A32D2D}.neutral{color:var(--text3)}
/* Chart cards */
.chart-card{background:var(--bg);border:0.5px solid var(--border);border-radius:var(--radius-lg);padding:16px 20px;margin-bottom:12px}
.chart-title{font-size:13px;font-weight:500;color:var(--text);margin-bottom:12px;display:flex;align-items:center;justify-content:space-between}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
/* Legend */
.legend{display:flex;gap:14px;font-size:12px;color:var(--text2)}
.legend-item{display:flex;align-items:center;gap:5px}
.legend-dot{width:10px;height:10px;border-radius:2px;flex-shrink:0}
/* Tabs */
.tab-group{display:flex;gap:4px;background:var(--bg2);padding:3px;border-radius:var(--radius);margin-bottom:16px;width:fit-content}
.tab-btn{font-size:12px;padding:5px 14px;border-radius:6px;cursor:pointer;color:var(--text2);border:none;background:transparent;font-family:inherit}
.tab-btn.active{background:var(--bg);color:var(--text);font-weight:500;border:0.5px solid var(--border)}
/* ASIN search */
.search-wrap{position:relative;margin-bottom:16px}
.search-row{display:flex;gap:8px}
.search-input{flex:1;padding:10px 14px;border:0.5px solid var(--border2);border-radius:var(--radius);background:var(--bg);color:var(--text);font-size:14px;outline:none;font-family:inherit}
.search-input:focus{border-color:var(--mi);box-shadow:0 0 0 2px rgba(24,95,165,0.15)}
.search-btn{padding:10px 16px;border:0.5px solid var(--border);border-radius:var(--radius);background:var(--bg2);color:var(--text2);cursor:pointer;font-size:13px;font-family:inherit;white-space:nowrap}
.search-btn:hover{background:var(--bg3);color:var(--text)}
.suggest-box{position:absolute;top:calc(100% + 4px);left:0;right:80px;background:var(--bg);border:0.5px solid var(--border2);border-radius:var(--radius-lg);z-index:200;max-height:260px;overflow-y:auto;box-shadow:0 8px 24px rgba(0,0,0,0.12)}
.suggest-item{padding:10px 14px;cursor:pointer;border-bottom:0.5px solid var(--border)}
.suggest-item:last-child{border-bottom:none}
.suggest-item:hover{background:var(--bg2)}
.suggest-top{display:flex;align-items:center;gap:8px;margin-bottom:3px}
.suggest-title{font-size:12px;color:var(--text2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.badge{font-size:11px;padding:2px 8px;border-radius:5px;font-weight:600;white-space:nowrap;flex-shrink:0}
.badge-MI{background:#deeaf7;color:#185FA5}.badge-NB{background:#d6ede5;color:#0F6E56}.badge-DS{background:#f5e0d7;color:#993C1D}
@media(prefers-color-scheme:dark){
  .badge-MI{background:#0c3460;color:#85B7EB}.badge-NB{background:#073826;color:#5DCAA5}.badge-DS{background:#4a1b0c;color:#F0997B}
}
.asin-mono{font-family:monospace;font-size:12px;color:var(--text3)}
/* ASIN detail */
.asin-header{background:var(--bg2);border-radius:var(--radius-lg);padding:14px 18px;margin-bottom:14px}
.asin-title-row{display:flex;align-items:flex-start;gap:10px;margin-bottom:6px}
.asin-title{font-size:14px;font-weight:500;line-height:1.5;flex:1;color:var(--text)}
.asin-meta{font-size:12px;color:var(--text3);font-family:monospace}
/* Table */
.data-table{width:100%;border-collapse:collapse;font-size:12px}
.data-table th{text-align:left;padding:7px 10px;border-bottom:0.5px solid var(--border2);color:var(--text3);font-weight:500;white-space:nowrap}
.data-table td{padding:7px 10px;border-bottom:0.5px solid var(--border);white-space:nowrap}
.data-table tr:last-child td{border-bottom:none}
.data-table tr:hover td{background:var(--bg2)}
.data-table td:first-child{font-weight:500;color:var(--text)}
/* Placeholder */
.placeholder{text-align:center;padding:48px 0;color:var(--text3)}
.placeholder-icon{font-size:36px;margin-bottom:12px;opacity:0.3}
/* Scrollbar */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
/* Responsive */
@media(max-width:768px){
  .topbar{padding:0 12px}
  .content{padding:12px}
  .metric-grid{grid-template-columns:repeat(2,1fr)}
  .two-col{grid-template-columns:1fr}
  .nav-tab{padding:0 10px;font-size:12px}
}
</style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="logo">📊 Brand Dashboard</div>
    <div class="nav-tabs">
      <div class="nav-tab active" onclick="showPage('overview')">總覽</div>
      <div class="nav-tab" onclick="showPage('asin')">ASIN 查詢</div>
    </div>
  </div>

  <div class="content">
    <!-- OVERVIEW PAGE -->
    <div id="page-overview" class="page active">
      <div class="metric-grid" id="overviewMetrics"></div>
      <div class="tab-group">
        <button class="tab-btn active" onclick="setRange(this,'recent')">近 12 個月</button>
        <button class="tab-btn" onclick="setRange(this,'2024')">2024</button>
        <button class="tab-btn" onclick="setRange(this,'all')">全部</button>
      </div>
      <div class="chart-card">
        <div class="chart-title">
          <span>月度銷售額（三品牌）</span>
          <div class="legend">
            <span class="legend-item"><span class="legend-dot" style="background:var(--mi)"></span>MI</span>
            <span class="legend-item"><span class="legend-dot" style="background:var(--nb)"></span>NB</span>
            <span class="legend-item"><span class="legend-dot" style="background:var(--ds)"></span>DS</span>
          </div>
        </div>
        <div style="position:relative;width:100%;height:280px"><canvas id="overviewSalesChart"></canvas></div>
      </div>
      <div class="two-col">
        <div class="chart-card">
          <div class="chart-title">
            <span>Apr 2026 銷售占比</span>
          </div>
          <div style="position:relative;width:100%;height:200px"><canvas id="pieChart"></canvas></div>
          <div class="legend" style="justify-content:center;margin-top:10px">
            <span class="legend-item"><span class="legend-dot" style="background:var(--mi)"></span>MI</span>
            <span class="legend-item"><span class="legend-dot" style="background:var(--nb)"></span>NB</span>
            <span class="legend-item"><span class="legend-dot" style="background:var(--ds)"></span>DS</span>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-title">
            <span>YoY 銷售成長率（%）</span>
          </div>
          <div style="position:relative;width:100%;height:200px"><canvas id="yoyChart"></canvas></div>
        </div>
      </div>
    </div>

    <!-- ASIN PAGE -->
    <div id="page-asin" class="page">
      <div class="search-wrap">
        <div class="search-row">
          <input class="search-input" id="asinInput" placeholder="輸入 ASIN（如 B0BXYKQBDC）或產品關鍵字..." autocomplete="off" />
          <button class="search-btn" onclick="clearAsin()">清除</button>
        </div>
        <div class="suggest-box" id="suggestBox" style="display:none"></div>
      </div>
      <div id="asinContent">
        <div class="placeholder">
          <div class="placeholder-icon">🔍</div>
          <div>輸入 ASIN 或關鍵字搜尋產品數據</div>
          <div style="font-size:12px;margin-top:6px;color:var(--text3)">共 <span id="totalCount">0</span> 個 ASIN · MI / NB / DS 三品牌</div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
/* __DATA_PLACEHOLDER__ */
</script>
<script>
// ── Globals ──────────────────────────────────────────
const ASINS = DASHBOARD_DATA.asins;
const BS = DASHBOARD_DATA.brand_summary;
const MONTHS_ALL = DASHBOARD_DATA.months_order;

const MI_C = '#185FA5', NB_C = '#0F6E56', DS_C = '#993C1D';

// Normalize brand summary months to consistent format
function normMonth(m) {
  const p = m.split('-');
  return p[0] + '-' + p[1].padStart(2,'0');
}

const BS_NORM = {};
for (const brand of ['MI','NB','DS']) {
  BS_NORM[brand] = {};
  for (const [m, v] of Object.entries(BS[brand] || {})) {
    BS_NORM[brand][normMonth(m)] = v;
  }
}

const SORTED_BS_MONTHS = [...new Set(
  Object.values(BS_NORM).flatMap(b => Object.keys(b))
)].sort();

// ── Page navigation ───────────────────────────────────
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  event.currentTarget.classList.add('active');
}

// ── Format helpers ────────────────────────────────────
function fmt$(v) {
  if (v == null || isNaN(v)) return '–';
  if (Math.abs(v) >= 1e6) return '$' + (v/1e6).toFixed(2) + 'M';
  if (Math.abs(v) >= 1e3) return '$' + (v/1e3).toFixed(1) + 'K';
  return '$' + Math.round(v).toLocaleString();
}
function fmtN(v) {
  if (v == null || isNaN(v)) return '–';
  if (v >= 1e6) return (v/1e6).toFixed(2) + 'M';
  if (v >= 1e3) return (v/1e3).toFixed(1) + 'K';
  return Math.round(v).toLocaleString();
}
function pctStr(a, b) {
  if (!a || !b || a === 0) return '<span class="neutral">–</span>';
  const p = (b - a) / Math.abs(a) * 100;
  const cls = p >= 0 ? 'up' : 'down';
  return `<span class="${cls}">${p >= 0 ? '+' : ''}${p.toFixed(1)}%</span>`;
}

// ── Overview ──────────────────────────────────────────
let overviewSalesInst = null, pieInst = null, yoyInst = null;
let currentRange = 'recent';

function initOverview() {
  const lastMonth = SORTED_BS_MONTHS[SORTED_BS_MONTHS.length - 1];
  const prevMonth = SORTED_BS_MONTHS[SORTED_BS_MONTHS.length - 2];
  const mi_last = BS_NORM.MI[lastMonth] || 0;
  const nb_last = BS_NORM.NB[lastMonth] || 0;
  const ds_last = BS_NORM.DS[lastMonth] || 0;
  const tot = mi_last + nb_last + ds_last;
  const mi_prev = BS_NORM.MI[prevMonth] || 0;
  const nb_prev = BS_NORM.NB[prevMonth] || 0;
  const ds_prev = BS_NORM.DS[prevMonth] || 0;
  const tot_prev = mi_prev + nb_prev + ds_prev;

  document.getElementById('overviewMetrics').innerHTML = `
    <div class="mcard"><div class="mcard-label">總銷售（${lastMonth}）</div><div class="mcard-val">${fmt$(tot)}</div><div class="mcard-sub">${pctStr(tot_prev, tot)} vs ${prevMonth}</div></div>
    <div class="mcard"><div class="mcard-label">MI（${lastMonth}）</div><div class="mcard-val">${fmt$(mi_last)}</div><div class="mcard-sub">${pctStr(mi_prev, mi_last)} vs ${prevMonth}</div></div>
    <div class="mcard"><div class="mcard-label">NB（${lastMonth}）</div><div class="mcard-val">${fmt$(nb_last)}</div><div class="mcard-sub">${pctStr(nb_prev, nb_last)} vs ${prevMonth}</div></div>
    <div class="mcard"><div class="mcard-label">DS（${lastMonth}）</div><div class="mcard-val">${fmt$(ds_last)}</div><div class="mcard-sub">${pctStr(ds_prev, ds_last)} vs ${prevMonth}</div></div>
  `;

  // Pie
  if (pieInst) pieInst.destroy();
  pieInst = new Chart(document.getElementById('pieChart'), {
    type: 'doughnut',
    data: { labels: ['MI','NB','DS'], datasets: [{ data: [mi_last, nb_last, ds_last], backgroundColor: [MI_C, NB_C, DS_C], borderWidth: 0, hoverOffset: 4 }] },
    options: { responsive: true, maintainAspectRatio: false, cutout: '60%',
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ctx.label + ': ' + fmt$(ctx.parsed) + ' (' + (ctx.parsed/tot*100).toFixed(1) + '%)' } } }
    }
  });

  buildOverviewCharts('recent');
}

function setRange(btn, range) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  buildOverviewCharts(range);
}

function buildOverviewCharts(range) {
  let months;
  if (range === 'recent') months = SORTED_BS_MONTHS.slice(-12);
  else if (range === '2024') months = SORTED_BS_MONTHS.filter(m => m.startsWith('2024'));
  else months = SORTED_BS_MONTHS;

  const labels = months.map(m => m.replace('20','').replace('-0','-'));
  const miData = months.map(m => BS_NORM.MI[m] || null);
  const nbData = months.map(m => BS_NORM.NB[m] || null);
  const dsData = months.map(m => BS_NORM.DS[m] || null);

  if (overviewSalesInst) overviewSalesInst.destroy();
  overviewSalesInst = new Chart(document.getElementById('overviewSalesChart'), {
    type: 'line',
    data: { labels, datasets: [
      { label: 'MI', data: miData, borderColor: MI_C, borderWidth: 2.5, pointRadius: 3, tension: 0.3, fill: false },
      { label: 'NB', data: nbData, borderColor: NB_C, borderWidth: 2, pointRadius: 2, tension: 0.3, fill: false, borderDash: [6,3] },
      { label: 'DS', data: dsData, borderColor: DS_C, borderWidth: 2, pointRadius: 2, tension: 0.3, fill: false, borderDash: [2,3] }
    ]},
    options: { responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + fmt$(ctx.parsed.y) } } },
      scales: {
        x: { ticks: { font: { size: 11 }, maxRotation: 45 }, grid: { display: false } },
        y: { ticks: { font: { size: 11 }, callback: v => v >= 1e6 ? '$'+(v/1e6).toFixed(0)+'M' : '$'+(v/1e3).toFixed(0)+'K' }, grid: { color: 'rgba(128,128,128,0.08)' } }
      }
    }
  });

  // YoY chart - use last 6 available months with YoY
  const recentMonths = SORTED_BS_MONTHS.slice(-6);
  const yoyLabels = [];
  const yoyMI = [], yoyNB = [], yoyDS = [];
  for (const m of recentMonths) {
    const [yr, mo] = m.split('-');
    const prevYr = String(parseInt(yr) - 1) + '-' + mo;
    if (BS_NORM.MI[prevYr]) {
      yoyLabels.push(m.replace('20','').replace('-0','-'));
      yoyMI.push(((BS_NORM.MI[m] || 0) / BS_NORM.MI[prevYr] - 1) * 100);
      yoyNB.push(BS_NORM.NB[prevYr] ? ((BS_NORM.NB[m] || 0) / BS_NORM.NB[prevYr] - 1) * 100 : null);
      yoyDS.push(BS_NORM.DS[prevYr] ? ((BS_NORM.DS[m] || 0) / BS_NORM.DS[prevYr] - 1) * 100 : null);
    }
  }
  if (yoyInst) yoyInst.destroy();
  yoyInst = new Chart(document.getElementById('yoyChart'), {
    type: 'bar',
    data: { labels: yoyLabels, datasets: [
      { label: 'MI', data: yoyMI, backgroundColor: MI_C + 'aa' },
      { label: 'NB', data: yoyNB, backgroundColor: NB_C + 'aa' },
      { label: 'DS', data: yoyDS, backgroundColor: DS_C + 'aa' }
    ]},
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { font: { size: 11 }, boxWidth: 10, padding: 10 } }, tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + (ctx.parsed.y != null ? ctx.parsed.y.toFixed(1) + '%' : '–') } } },
      scales: {
        x: { ticks: { font: { size: 11 } }, grid: { display: false } },
        y: { ticks: { font: { size: 11 }, callback: v => v.toFixed(0) + '%' }, grid: { color: 'rgba(128,128,128,0.08)' } }
      }
    }
  });
}

// ── ASIN Search ────────────────────────────────────────
const asinInput = document.getElementById('asinInput');
const suggestBox = document.getElementById('suggestBox');
let salesChartI = null, unitChartI = null, cvrChartI = null;

document.getElementById('totalCount').textContent = Object.keys(ASINS).length.toLocaleString();

asinInput.addEventListener('input', onAsinInput);
asinInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    suggestBox.style.display = 'none';
    const q = asinInput.value.trim().toUpperCase();
    if (ASINS[q]) renderAsin(q);
  }
});
document.addEventListener('click', e => {
  if (!e.target.closest('.search-wrap')) suggestBox.style.display = 'none';
});

function onAsinInput() {
  const q = asinInput.value.trim();
  if (q.length < 2) { suggestBox.style.display = 'none'; return; }
  const qu = q.toUpperCase();
  const hits = Object.entries(ASINS).filter(([a, d]) =>
    a.includes(qu) || (d.title || '').toUpperCase().includes(qu)
  ).slice(0, 10);
  if (!hits.length) { suggestBox.style.display = 'none'; return; }
  suggestBox.innerHTML = hits.map(([asin, d]) => `
    <div class="suggest-item" onclick="selectAsin('${asin}')">
      <div class="suggest-top">
        <span class="badge badge-${d.brand}">${d.brand}</span>
        <span style="font-size:12px;font-weight:600">${asin}</span>
      </div>
      <div class="suggest-title">${(d.title || '').substring(0, 90)}${(d.title || '').length > 90 ? '...' : ''}</div>
    </div>`).join('');
  suggestBox.style.display = 'block';
}

function selectAsin(asin) {
  asinInput.value = asin;
  suggestBox.style.display = 'none';
  renderAsin(asin);
}

function clearAsin() {
  asinInput.value = '';
  suggestBox.style.display = 'none';
  document.getElementById('asinContent').innerHTML = `
    <div class="placeholder">
      <div class="placeholder-icon">🔍</div>
      <div>輸入 ASIN 或關鍵字搜尋產品數據</div>
      <div style="font-size:12px;margin-top:6px;color:var(--text3)">共 ${Object.keys(ASINS).length.toLocaleString()} 個 ASIN · MI / NB / DS 三品牌</div>
    </div>`;
}

const MONTHS_ORDERED = [
  '2024-12','2025-01','2025-02','2025-03','2025-04','2025-05','2025-06',
  '2025-07','2025-08','2025-09','2025-10','2025-11','2025-12',
  '2026-01','2026-02','2026-03','2026-04'
];

function renderAsin(asin) {
  const d = ASINS[asin];
  if (!d) { document.getElementById('asinContent').innerHTML = `<div class="placeholder">找不到 ASIN：${asin}</div>`; return; }

  const brandColor = { MI: MI_C, NB: NB_C, DS: DS_C }[d.brand];
  const months = MONTHS_ORDERED.filter(m => d.months[m]);
  const latest = months[months.length - 1];
  const prev = months[months.length - 2];
  const lm = d.months[latest] || {};
  const pm = prev ? d.months[prev] || {} : {};

  const labels = months.map(m => m.replace('20','').replace('-0','-'));
  const salesD = months.map(m => d.months[m]?.total_sales ?? null);
  const spendD = months.map(m => d.months[m]?.spend ?? null);
  const adSalesD = months.map(m => d.months[m]?.ad_sales ?? null);
  const unitD = months.map(m => d.months[m]?.units ?? null);
  const cvrD = months.map(m => d.months[m]?.cvr != null ? +(d.months[m].cvr * 100).toFixed(2) : null);
  const gvD = months.map(m => d.months[m]?.glance_views ?? null);

  const acosL = lm.spend && lm.ad_sales ? lm.spend / lm.ad_sales : null;
  const acosP = pm.spend && pm.ad_sales ? pm.spend / pm.ad_sales : null;

  const tableRows = months.slice(-10).reverse().map(m => {
    const mo = d.months[m];
    const ac = mo.spend && mo.ad_sales ? (mo.spend / mo.ad_sales * 100).toFixed(1) + '%' : '–';
    return `<tr>
      <td>${m}</td>
      <td>${fmtN(mo.units)}</td>
      <td>${fmt$(mo.total_sales)}</td>
      <td>${fmt$(mo.spend)}</td>
      <td>${fmt$(mo.ad_sales)}</td>
      <td>${ac}</td>
      <td>${mo.cvr ? (mo.cvr * 100).toFixed(1) + '%' : '–'}</td>
      <td>${mo.glance_views ? fmtN(mo.glance_views) : '–'}</td>
    </tr>`;
  }).join('');

  document.getElementById('asinContent').innerHTML = `
    <div class="asin-header">
      <div class="asin-title-row">
        <span class="badge badge-${d.brand}">${d.brand}</span>
        <span class="asin-title">${d.title || ''}</span>
      </div>
      <span class="asin-meta">${asin} · 最新資料：${latest}</span>
    </div>
    <div class="metric-grid">
      <div class="mcard"><div class="mcard-label">銷售額（${latest}）</div><div class="mcard-val">${fmt$(lm.total_sales)}</div><div class="mcard-sub">${pctStr(pm.total_sales, lm.total_sales)} vs ${prev || ''}</div></div>
      <div class="mcard"><div class="mcard-label">銷售量（${latest}）</div><div class="mcard-val">${fmtN(lm.units)}</div><div class="mcard-sub">${pctStr(pm.units, lm.units)} vs ${prev || ''}</div></div>
      <div class="mcard"><div class="mcard-label">廣告花費（${latest}）</div><div class="mcard-val">${fmt$(lm.spend)}</div><div class="mcard-sub">${pctStr(pm.spend, lm.spend)} vs ${prev || ''}</div></div>
      <div class="mcard"><div class="mcard-label">ACOS（${latest}）</div><div class="mcard-val">${acosL ? (acosL * 100).toFixed(1) + '%' : '–'}</div><div class="mcard-sub">${acosL && acosP ? pctStr(acosP, acosL) + ' vs ' + prev : '<span class="neutral">–</span>'}</div></div>
    </div>
    <div class="chart-card">
      <div class="chart-title">
        <span>銷售額 · 廣告花費 · 廣告銷售</span>
        <div class="legend">
          <span class="legend-item"><span class="legend-dot" style="background:${brandColor}"></span>總銷售</span>
          <span class="legend-item"><span class="legend-dot" style="background:#E24B4A"></span>廣告花費</span>
          <span class="legend-item"><span class="legend-dot" style="background:#639922"></span>廣告銷售</span>
        </div>
      </div>
      <div style="position:relative;width:100%;height:250px"><canvas id="asinSalesChart"></canvas></div>
    </div>
    <div class="two-col">
      <div class="chart-card">
        <div class="chart-title">銷售量趨勢</div>
        <div style="position:relative;width:100%;height:200px"><canvas id="asinUnitChart"></canvas></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">CVR & Glance Views</div>
        <div style="position:relative;width:100%;height:200px"><canvas id="asinCvrChart"></canvas></div>
      </div>
    </div>
    <div class="chart-card">
      <div class="chart-title">月度明細（最近 10 個月）</div>
      <div style="overflow-x:auto">
        <table class="data-table">
          <thead><tr><th>月份</th><th>銷售量</th><th>總銷售額</th><th>廣告花費</th><th>廣告銷售</th><th>ACOS</th><th>CVR</th><th>Glance Views</th></tr></thead>
          <tbody>${tableRows}</tbody>
        </table>
      </div>
    </div>`;

  if (salesChartI) salesChartI.destroy();
  if (unitChartI) unitChartI.destroy();
  if (cvrChartI) cvrChartI.destroy();

  salesChartI = new Chart(document.getElementById('asinSalesChart'), {
    type: 'bar',
    data: { labels, datasets: [
      { type: 'bar', label: '總銷售額', data: salesD, backgroundColor: brandColor + '33', borderColor: brandColor, borderWidth: 1, yAxisID: 'y1' },
      { type: 'line', label: '廣告花費', data: spendD, borderColor: '#E24B4A', borderWidth: 2, pointRadius: 3, tension: 0.3, fill: false, yAxisID: 'y2' },
      { type: 'line', label: '廣告銷售', data: adSalesD, borderColor: '#639922', borderWidth: 2, pointRadius: 2, tension: 0.3, fill: false, yAxisID: 'y1', borderDash: [4, 3] }
    ]},
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false, callbacks: { label: ctx => ctx.dataset.label + ': ' + fmt$(ctx.parsed.y) } } },
      scales: {
        x: { ticks: { font: { size: 11 }, maxRotation: 45 }, grid: { display: false } },
        y1: { position: 'left', ticks: { font: { size: 11 }, callback: v => v >= 1e6 ? '$'+(v/1e6).toFixed(1)+'M' : '$'+(v/1e3).toFixed(0)+'K' }, grid: { color: 'rgba(128,128,128,0.06)' } },
        y2: { position: 'right', ticks: { font: { size: 11 }, callback: v => '$'+(v/1e3).toFixed(0)+'K' }, grid: { display: false } }
      }
    }
  });

  unitChartI = new Chart(document.getElementById('asinUnitChart'), {
    type: 'bar',
    data: { labels, datasets: [{ label: '銷售量', data: unitD, backgroundColor: brandColor + '66', borderColor: brandColor, borderWidth: 1 }] },
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { ticks: { font: { size: 11 }, maxRotation: 45 }, grid: { display: false } }, y: { ticks: { font: { size: 11 }, callback: v => v >= 1e3 ? (v/1e3).toFixed(1)+'K' : v }, grid: { color: 'rgba(128,128,128,0.06)' } } }
    }
  });

  const hasCvr = cvrD.some(v => v != null);
  const hasGv = gvD.some(v => v != null);
  const cvrDatasets = [];
  if (hasCvr) cvrDatasets.push({ label: 'CVR', data: cvrD, borderColor: brandColor, borderWidth: 2, pointRadius: 3, tension: 0.3, fill: false, yAxisID: 'yc' });
  if (hasGv) cvrDatasets.push({ label: 'Glance Views', data: gvD, borderColor: '#BA7517', borderWidth: 2, pointRadius: 2, tension: 0.3, fill: false, yAxisID: 'yg', borderDash: [5, 3] });
  cvrChartI = new Chart(document.getElementById('asinCvrChart'), {
    type: 'line',
    data: { labels, datasets: cvrDatasets },
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { font: { size: 11 }, boxWidth: 10, padding: 8 } }, tooltip: { callbacks: { label: ctx => ctx.dataset.label === 'CVR' ? 'CVR: ' + ctx.parsed.y.toFixed(1) + '%' : 'GV: ' + fmtN(ctx.parsed.y) } } },
      scales: {
        x: { ticks: { font: { size: 11 }, maxRotation: 45 }, grid: { display: false } },
        yc: { position: 'left', ticks: { font: { size: 11 }, callback: v => v.toFixed(1) + '%' }, grid: { color: 'rgba(128,128,128,0.06)' } },
        yg: { position: 'right', ticks: { font: { size: 11 }, callback: v => v >= 1e3 ? (v/1e3).toFixed(0)+'K' : v }, grid: { display: false } }
      }
    }
  });
}

// ── Init ──────────────────────────────────────────────
initOverview();
</script>
</body>
</html>
