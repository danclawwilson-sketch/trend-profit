import urllib.request
import zipfile
import os
import io

BASE_URL = "https://data.binance.vision/data/spot/monthly/klines"
SYMBOLS = ["ETHUSDT", "BTCUSDT"]
MONTHS = []

# 2023-01 to 2025-12
for year in [2023, 2024, 2025]:
    for month in range(1, 13):
        MONTHS.append(f"{year}-{month:02d}")

for symbol in SYMBOLS:
    print(f"\n{'='*50}")
    print(f"下載 {symbol} 1m K線...")
    for m in MONTHS:
        url = f"{BASE_URL}/{symbol}/1m/{symbol}-1m-{m}.zip"
        out_file = f"data/{symbol}_1m_{m}.txt"
        
        if os.path.exists(out_file):
            print(f"  ✅ {m} 已存在，跳過")
            continue
        
        try:
            print(f"  ⬇ {m}...", end=" ", flush=True)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=30)
            data = resp.read()
            
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                csv_name = zf.namelist()[0]
                content = zf.read(csv_name).decode("utf-8")
                
                # 添加表頭
                header = "timestamp,open,high,low,close,volume,close_time,quote_volume,trades,taker_buy_base,taker_buy_quote,ignore"
                with open(out_file, "w") as f:
                    f.write(header + "\n")
                    f.write(content)
                
                lines = content.count("\n")
                print(f"✅ {lines} 根")
        except Exception as e:
            print(f"❌ {e}")

print("\n✅ 全部完成！")
