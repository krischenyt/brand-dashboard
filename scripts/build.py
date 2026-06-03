#!/usr/bin/env python3
"""
Build script: reads all *_Difference.xlsx from /data, generates index.html
Run locally:  python scripts/build.py
GitHub Actions runs this automatically on every push to main.
"""
import pandas as pd
import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
TMPL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html')

brand_sheets = {'MI': 'Micro Difference', 'NB': 'NB Difference', 'DS': 'DS Difference'}

MONTH_MAP = {
    'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06',
    'jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'
}

def parse_months_from_filename(fname):
    base = re.sub(r'\.xlsx$', '', fname, flags=re.IGNORECASE).lower()
    base = re.sub(r'_difference$', '', base)
    years = re.findall(r'(202\d)', base)          # no word boundary needed
    months_found = re.findall(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', base)
    if len(months_found) < 2 or not years:
        return None, None
    m1_num = int(MONTH_MAP[months_found[0]])
    m2_num = int(MONTH_MAP[months_found[1]])
    year = int(years[-1])
    if m2_num < m1_num:       # cross-year e.g. Dec→Jan
        y1, y2 = year - 1, year
    else:
        y1 = y2 = year
    return f'{y1}-{m1_num:02d}', f'{y2}-{m2_num:02d}'

# ── Read all Excel files ─────────────────────────────────────────────────────
asin_data = {}
brand_summary_raw = {}
most_recent_file = None
most_recent_date = (0, 0)

xlsx_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.xlsx')])
print(f'Found {len(xlsx_files)} Excel files')

for fname in xlsx_files:
    m1, m2 = parse_months_from_filename(fname)
    if not m1 or not m2:
        print(f'  WARNING: could not parse months from {fname}')
        continue
    print(f'  {fname}  →  {m1} / {m2}')

    m2y, m2mo = int(m2.split('-')[0]), int(m2.split('-')[1])
    if (m2y, m2mo) > most_recent_date:
        most_recent_date = (m2y, m2mo)
        most_recent_file = fname

    fpath = os.path.join(DATA_DIR, fname)
    for brand, sheet in brand_sheets.items():
        try:
            df = pd.read_excel(fpath, sheet_name=sheet, header=None)
            row0 = df.iloc[0].tolist()
            row1 = df.iloc[1].tolist()

            spend_cols, ad_sales_cols, total_sales_cols, glance_cols, cvr_cols = [], [], [], [], []
            for i, v in enumerate(row0):
                sv = str(v).strip()
                if sv == 'Spend': spend_cols.append(i)
                if 'Ad Sales' in sv: ad_sales_cols.append(i)
                if 'Total Sales' in sv or 'Total sales' in sv: total_sales_cols.append(i)
                if 'Glance View' in sv: glance_cols.append(i)
                if sv == 'CVR': cvr_cols.append(i)

            def find_two(cols):
                if not cols: return None, None
                c = cols[0]; a = b = None
                for j in range(c, min(c + 5, len(row1))):
                    lbl = str(row1[j]).strip()
                    if lbl and lbl.lower() != 'nan':
                        if a is None: a = j
                        elif b is None: b = j; break
                return a, b

            sm1, sm2 = find_two(spend_cols)
            ts1, ts2 = find_two(total_sales_cols)
            gv1, gv2 = find_two(glance_cols)
            cv1, cv2 = find_two(cvr_cols)
            ad_m2 = None
            if ad_sales_cols:
                for j in range(ad_sales_cols[0], min(ad_sales_cols[0]+5, len(row1))):
                    if str(row1[j]).strip() and str(row1[j]).strip().lower() != 'nan':
                        ad_m2 = j; break

            def safe(row, col):
                if col is None: return None
                try:
                    v = row.iloc[col]
                    return None if pd.isna(v) else float(v)
                except: return None

            for idx in range(2, len(df)):
                row = df.iloc[idx]
                asin = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else None
                title = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else None
                if not asin or asin == 'nan' or len(asin) < 8: continue
                if asin not in asin_data:
                    asin_data[asin] = {'title': title, 'brand': brand, 'months': {}}
                elif title and asin_data[asin].get('title') == 'nan':
                    asin_data[asin]['title'] = title
                md = asin_data[asin]['months']
                for mo, uc, sc, tsc, gvc, cvc in [(m1,2,sm1,ts1,gv1,cv1),(m2,5,sm2,ts2,gv2,cv2)]:
                    if mo not in md: md[mo] = {}
                    if safe(row,uc) is not None: md[mo]['units'] = round(safe(row,uc))
                    if safe(row,sc) is not None: md[mo]['spend'] = round(safe(row,sc), 2)
                    if safe(row,tsc) is not None: md[mo]['total_sales'] = round(safe(row,tsc), 2)
                    if safe(row,gvc) is not None: md[mo]['glance_views'] = round(safe(row,gvc))
                    if safe(row,cvc) is not None: md[mo]['cvr'] = round(safe(row,cvc), 4)
                if safe(row, ad_m2) is not None:
                    if m2 not in md: md[m2] = {}
                    md[m2]['ad_sales'] = round(safe(row, ad_m2), 2)
        except Exception:
            pass

# ── Brand summary from most recent file ─────────────────────────────────────
print(f'\nUsing {most_recent_file} for brand summary')
try:
    df = pd.read_excel(os.path.join(DATA_DIR, most_recent_file), sheet_name='Sales Summary', header=None)
    months_row = df.iloc[0].tolist()
    for brand_idx, brand in [(1,'MI'),(2,'NB'),(3,'DS')]:
        brand_summary_raw[brand] = {}
        row = df.iloc[brand_idx].tolist()
        for i, m in enumerate(months_row):
            ms = str(m).strip()
            if ms.startswith('20') and '-' in ms:
                val = row[i]
                if pd.notna(val) and val not in (0, ''):
                    parts = ms.split('-')
                    brand_summary_raw[brand][parts[0]+'-'+parts[1].zfill(2)] = float(val)
except Exception as e:
    print(f'WARNING: Sales Summary read failed: {e}')

def month_key(m):
    p = m.split('-'); return (int(p[0]), int(p[1]))

all_bs_months = sorted(
    set(m for b in brand_summary_raw.values() for m in b.keys()),
    key=month_key
)

asins_out = {a: d for a, d in asin_data.items() if len(d['months']) >= 2}
print(f'Total ASINs: {len(asins_out)}')
print(f'Brand summary months: {all_bs_months[-3:]}')

# ── Build index.html ─────────────────────────────────────────────────────────
payload = {'asins': asins_out, 'brand_summary': brand_summary_raw, 'months_order': all_bs_months}
js_data = 'const DASHBOARD_DATA = ' + json.dumps(payload, ensure_ascii=False, separators=(',',':')) + ';'

with open(TMPL_FILE, 'r', encoding='utf-8') as f:
    template = f.read()

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write(template.replace('/* __DATA_PLACEHOLDER__ */', js_data))

print(f'\n✅  Built: index.html  ({os.path.getsize(OUT_FILE)//1024} KB)')
