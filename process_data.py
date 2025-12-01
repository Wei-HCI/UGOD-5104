import pandas as pd
import numpy as np

# ================= 1. 学术配置 (Methodology Config) =================

POI_DATA = {
    'subway': [
        {'name': '体育西路', 'lat': 23.1319, 'lng': 113.3213},
        {'name': '珠江新城', 'lat': 23.1192, 'lng': 113.3212},
        {'name': '猎德', 'lat': 23.1186, 'lng': 113.3324},
        {'name': '广州东站', 'lat': 23.1492, 'lng': 113.3260},
        {'name': '华师', 'lat': 23.1400, 'lng': 113.3460},
        {'name': '岗顶', 'lat': 23.1335, 'lng': 113.3390},
        {'name': '石牌桥', 'lat': 23.1330, 'lng': 113.3320},
        {'name': '员村', 'lat': 23.1140, 'lng': 113.3620},
        {'name': '科韵路', 'lat': 23.1190, 'lng': 113.3740},
        {'name': '车陂南', 'lat': 23.1105, 'lng': 113.3954},
        {'name': '车陂', 'lat': 23.1230, 'lng': 113.3960},
        {'name': '天河公园', 'lat': 23.1240, 'lng': 113.3660},
        {'name': '燕塘', 'lat': 23.1560, 'lng': 113.3270},
        {'name': '天河客运站', 'lat': 23.1713, 'lng': 113.3451},
        {'name': '龙洞', 'lat': 23.1930, 'lng': 113.3670},
        {'name': '天河智慧城', 'lat': 23.1780, 'lng': 113.4060},
        {'name': '[Buffer] 动物园', 'lat': 23.1330, 'lng': 113.3080},
        {'name': '[Buffer] 区庄', 'lat': 23.1330, 'lng': 113.2980},
        {'name': '[Buffer] 广州塔', 'lat': 23.1060, 'lng': 113.3240},
        {'name': '[Buffer] 梅花园', 'lat': 23.1650, 'lng': 113.3150},
    ],
    'mall': [
        {'name': '天河城/正佳', 'lat': 23.1315, 'lng': 113.3276},
        {'name': '太古汇', 'lat': 23.1345, 'lng': 113.3330},
        {'name': '天环/IGC/K11', 'lat': 23.1170, 'lng': 113.3340},
        {'name': '东方宝泰', 'lat': 23.1480, 'lng': 113.3260},
        {'name': '美林M-LIVE', 'lat': 23.1100, 'lng': 113.4180},
        {'name': '[Buffer] 友谊商店', 'lat': 23.1380, 'lng': 113.2960},
        {'name': '[Buffer] 丽影广场', 'lat': 23.0970, 'lng': 113.3210}
    ],
    'school': [
        {'name': '华阳/体育东/华附', 'lat': 23.1410, 'lng': 113.3285},
        {'name': '天府路/113中', 'lat': 23.1270, 'lng': 113.3600},
        {'name': '广州中学', 'lat': 23.1350, 'lng': 113.3300},
        {'name': '[Buffer] 执信中学', 'lat': 23.1280, 'lng': 113.2960}
    ],
    'park': [
        {'name': '天河公园', 'lat': 23.1245, 'lng': 113.3650},
        {'name': '珠江公园', 'lat': 23.1180, 'lng': 113.3350},
        {'name': '火炉山/植物园', 'lat': 23.1920, 'lng': 113.3750},
        {'name': '[Buffer] 黄花岗公园', 'lat': 23.1360, 'lng': 113.3000},
        {'name': '[Buffer] 白云山东门', 'lat': 23.1680, 'lng': 113.2980}
    ],
    'public_service': [
        {'name': '中山三院/体育中心', 'lat': 23.1320, 'lng': 113.3400},
        {'name': '珠江新城公建群', 'lat': 23.1150, 'lng': 113.3210},
        {'name': '[Buffer] 中山一院', 'lat': 23.1280, 'lng': 113.2960},
        {'name': '[Buffer] 南方医院', 'lat': 23.1860, 'lng': 113.3280}
    ]
}

BANDWIDTHS = {
    'subway': 1000, 
    'mall': 1500, 
    'school': 800, 
    'park': 2000, 
    'public_service': 3000
}

# ================= 2. 核心算法库 =================

def vectorized_haversine(lat1, lng1, lat2, lng2):
    R = 6371000
    lat1, lng1, lat2, lng2 = map(np.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlng/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return c * R

def gravity_accessibility_score(df_house, poi_list, bandwidth):
    house_lats = df_house['Lat'].values[:, np.newaxis] 
    house_lngs = df_house['Lng'].values[:, np.newaxis]
    poi_lats = np.array([p['lat'] for p in poi_list])[np.newaxis, :] 
    poi_lngs = np.array([p['lng'] for p in poi_list])[np.newaxis, :]
    dists = vectorized_haversine(house_lats, house_lngs, poi_lats, poi_lngs)
    decay_factors = np.exp(-0.5 * (dists / bandwidth)**2)
    raw_scores = np.sum(decay_factors, axis=1)
    return raw_scores

def calculate_entropy_weights(df_scores):
    df_norm = df_scores.copy()
    for col in df_scores.columns:
        min_val = df_scores[col].min()
        max_val = df_scores[col].max()
        if max_val - min_val == 0:
            df_norm[col] = 0
        else:
            df_norm[col] = (df_scores[col] - min_val) / (max_val - min_val)
    P = df_norm / (df_norm.sum(axis=0) + 1e-12)
    k = 1 / np.log(len(df_scores))
    E = -k * (P * np.log(P + 1e-12)).sum(axis=0)
    D = 1 - E
    W = D / D.sum()
    return W

# ================= 主程序 =================
if __name__ == "__main__":
    print("1. Data Loading & Cleaning...")
    try:
        df = pd.read_csv('housePrice_Updated.csv', encoding='gbk', low_memory=False)
    except FileNotFoundError:
        print("Error: 'housePrice_Updated.csv' not found.")
        exit()

    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df['Lat'] = pd.to_numeric(df['Lat'], errors='coerce')
    df['Lng'] = pd.to_numeric(df['Lng'], errors='coerce')
    df.dropna(subset=['unit_price', 'Lat', 'Lng'], inplace=True)

    min_lat, max_lat = 23.10, 23.23
    min_lng, max_lng = 113.30, 113.45
    df_tianhe = df[
        (df['Lat'] >= min_lat) & (df['Lat'] <= max_lat) &
        (df['Lng'] >= min_lng) & (df['Lng'] <= max_lng) & 
        (df['unit_price'] > 10000)
    ].copy().reset_index(drop=True)
    
    print(f"   Analyzing {len(df_tianhe)} raw housing units.")

    print("2. Calculating Gravity Scores...")
    score_cols = []
    for key, pois in POI_DATA.items():
        col_name = f'raw_{key}'
        df_tianhe[col_name] = gravity_accessibility_score(df_tianhe, pois, BANDWIDTHS[key])
        score_cols.append(col_name)

    print("3. Determining Weights (EWM)...")
    weights = calculate_entropy_weights(df_tianhe[score_cols])
    
    print("\n   [Objective Weights]")
    for col, w in weights.items():
        print(f"   {col.replace('raw_', '').title():<15}: {w:.4f}")

    df_tianhe['Accessibility_Index'] = 0
    for col in score_cols:
        min_v, max_v = df_tianhe[col].min(), df_tianhe[col].max()
        norm_score = (df_tianhe[col] - min_v) / (max_v - min_v + 1e-9)
        df_tianhe['Accessibility_Index'] += norm_score * weights[col]

    df_tianhe['Accessibility_Index'] = (df_tianhe['Accessibility_Index'] * 100).round(2)

    # --- [关键修改] Step 4: 聚合与深度清洗 (Aggregation) ---
    print("4. Aggregating by Block & Validating...")
    
    df_clean = df_tianhe[df_tianhe['unit_price'] > 15000].copy()
    df_clean['block'] = df_clean['block'].astype(str).str.strip()
    
    # [FIX] 在这里加入 'Lat' 和 'Lng' 的聚合规则 ('first' 或 'mean')
    df_grouped = df_clean.groupby('block').agg({
        'unit_price': 'mean',
        'Accessibility_Index': 'mean',
        'Lat': 'mean',  # [新增] 计算该小区平均纬度
        'Lng': 'mean',  # [新增] 计算该小区平均经度
        'block': 'count'
    }).rename(columns={'block': 'count'}).reset_index()

    # 保留一位小数
    df_grouped['unit_price'] = df_grouped['unit_price'].round(1)
    df_grouped['Accessibility_Index'] = df_grouped['Accessibility_Index'].round(2)
    df_grouped['Lat'] = df_grouped['Lat'].round(6)
    df_grouped['Lng'] = df_grouped['Lng'].round(6)

    df_result = df_grouped.sort_values(by='Accessibility_Index', ascending=False)

    print("\n   ========== TOP 5 Accessible Blocks (Merged) ==========")
    print(df_result[['block', 'unit_price', 'Accessibility_Index', 'Lat', 'Lng']].head(5).to_string(index=False))

    correlation = df_result['Accessibility_Index'].corr(df_result['unit_price'])
    print(f"\n   --------------------------------------------------------")
    print(f"   [Study Conclusion] Index vs. Price Correlation: {correlation:.3f}")
    print(f"   --------------------------------------------------------")

    # --- Step 6: 导出 ---
    df_result.to_csv('final_academic_tianhe_blocks.csv', index=False, encoding='utf-8')
    print(f"\n5. Done! Aggregated data saved to 'final_academic_tianhe_blocks.csv'.")
    print("   Includes columns: block, unit_price, Accessibility_Index, count, Lat, Lng")