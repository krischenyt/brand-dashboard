# Brand Sales Dashboard

三品牌（MI / NB / DS）銷售 & 廣告數據 Dashboard，部署於 GitHub Pages。

## 🌐 網址
> 建立 repo 後前往 **Settings → Pages → Source: main branch / root** 即可取得網址
> 格式：`https://<你的帳號>.github.io/<repo名稱>/`

---

## 📅 每月更新流程（只需要 3 步）

1. **把新的 Excel 檔**（例如 `May_-_Jun_2026_Difference.xlsx`）拖進 GitHub 的 `data/` 資料夾
2. 點 **Commit changes**
3. GitHub Actions 自動跑 → 約 1 分鐘後網站更新完成 ✅

> 可在 repo 的 **Actions** 頁籤確認執行狀態

---

## 📁 檔案結構

```
├── data/                        ← 把每月 Excel 放這裡
│   ├── Apr_-_May_2026_Difference.xlsx
│   └── ...
├── scripts/
│   ├── build.py                 ← 讀取 Excel，產生 index.html
│   └── template.html            ← Dashboard HTML 模板
├── .github/workflows/
│   └── build.yml                ← GitHub Actions 自動觸發
├── index.html                   ← 自動產生，請勿手動編輯
└── README.md
```

---

## 💻 本地執行（選用）

```bash
pip install pandas openpyxl
python scripts/build.py
# 開啟 index.html 即可預覽
```

## ⚠️ Excel 命名規則

腳本自動從檔名解析月份，**只要包含兩個月份名稱 + 年份**即可：

| 範例檔名 | 解析結果 |
|---|---|
| `May_-_Jun_2026_Difference.xlsx` | 2026-05 / 2026-06 |
| `Dec_-_Jan_2027_Difference.xlsx` | 2026-12 / 2027-01 |
| `Aug-Sep_2026_Difference.xlsx` | 2026-08 / 2026-09 |
