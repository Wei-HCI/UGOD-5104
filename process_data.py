import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

# ================= 经过校验的精准 POI 数据 (GCJ-02坐标系) =================
POI_DATA = {
    'subway': [ # 权重 0.3
        {'name': '体育西路', 'lat': 23.1319, 'lng': 113.3213},
        {'name': '珠江新城', 'lat': 23.1192, 'lng': 113.3212},
        {'name': '猎德', 'lat': 23.1186, 'lng': 113.3324},
        {'name': '潭村', 'lat': 23.1190, 'lng': 113.3470},
        {'name': '林和西', 'lat': 23.1416, 'lng': 113.3254},
        {'name': '广州东站', 'lat': 23.1492, 'lng': 113.3260},
        {'name': '华师', 'lat': 23.1400, 'lng': 113.3460},
        {'name': '五山', 'lat': 23.1480, 'lng': 113.3510},
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
        {'name': '植物园', 'lat': 23.1850, 'lng': 113.3620},
        {'name': '长湴', 'lat': 23.1750, 'lng': 113.3520}, 
        {'name': '天河智慧城', 'lat': 23.1780, 'lng': 113.4060}, 
        {'name': '大观南路', 'lat': 23.1680, 'lng': 113.3860}, 
        {'name': '华景路', 'lat': 23.1350, 'lng': 113.3570} 
    ],
    'mall': [ # 权重 0.15
        {'name': '天河城/正佳', 'lat': 23.1315, 'lng': 113.3276},
        {'name': '太古汇', 'lat': 23.1345, 'lng': 113.3330},
        {'name': '天环广场', 'lat': 23.1330, 'lng': 113.3290},
        {'name': 'IGC天汇广场', 'lat': 23.1170, 'lng': 113.3340},
        {'name': 'K11', 'lat': 23.1130, 'lng': 113.3250},
        {'name': '东方宝泰', 'lat': 23.1480, 'lng': 113.3260},
        {'name': '太阳新天地', 'lat': 23.1250, 'lng': 113.3450},
        {'name': '美林M-LIVE', 'lat': 23.1100, 'lng': 113.4180},
        {'name': '维多利广场', 'lat': 23.1320, 'lng': 113.3270},
        {'name': '万菱汇', 'lat': 23.1340, 'lng': 113.3320},
        {'name': '佳兆业广场', 'lat': 23.1420, 'lng': 113.3250},
        {'name': 'YCC!天宜', 'lat': 23.1470, 'lng': 113.3270}, # [已修正] 位于林和中路
        {'name': '时代E-PARK', 'lat': 23.1230, 'lng': 113.3730},
        {'name': '广州SKP（赛马场地块）', 'lat': 23.1185, 'lng': 113.3420}
    ],
    'school': [ # 权重 0.25
        {'name': '华阳小学(天河东)', 'lat': 23.1410, 'lng': 113.3285},
        {'name': '华阳小学(林和东)', 'lat': 23.1450, 'lng': 113.3300},
        {'name': '华南师范附小', 'lat': 23.1380, 'lng': 113.3450},
        {'name': '体育东路小学', 'lat': 23.1350, 'lng': 113.3250},
        {'name': '先烈东小学', 'lat': 23.1200, 'lng': 113.3220},
        {'name': '天府路小学', 'lat': 23.1270, 'lng': 113.3600},
        {'name': '龙口西小学', 'lat': 23.1420, 'lng': 113.3380},
        {'name': '天河外国语学校', 'lat': 23.1760, 'lng': 113.4000},
        {'name': '广州市113中学', 'lat': 23.1320, 'lng': 113.3410},
        {'name': '广州中学', 'lat': 23.1350, 'lng': 113.3300},
        {'name': '长湴小学', 'lat': 23.1750, 'lng': 113.3550},
        {'name': '岑村小学', 'lat': 23.1810, 'lng': 113.3830}
    ],
    'park': [ # 权重 0.15
        {'name': '天河公园', 'lat': 23.1245, 'lng': 113.3650},
        {'name': '珠江公园', 'lat': 23.1180, 'lng': 113.3350},
        {'name': '华南植物园', 'lat': 23.1860, 'lng': 113.3600},
        {'name': '海心沙', 'lat': 23.1090, 'lng': 113.3240},
        {'name': '火炉山森林公园', 'lat': 23.1920, 'lng': 113.3750},
        {'name': '大观湿地公园', 'lat': 23.1710, 'lng': 113.4080},
        {'name': '广东树木公园', 'lat': 23.1830, 'lng': 113.3520},
        {'name': '马场中央公园（规划）', 'lat': 23.1180, 'lng': 113.3430}
    ],
    'public_service': [ # 权重 0.15
        {'name': '中山三院', 'lat': 23.1320, 'lng': 113.3400},
        {'name': '妇儿中心', 'lat': 23.1220, 'lng': 113.3270},
        {'name': '天河体育中心', 'lat': 23.1310, 'lng': 113.3210},
        {'name': '广东省博物馆', 'lat': 23.1140, 'lng': 113.3200},
        {'name': '广州图书馆', 'lat': 23.1150, 'lng': 113.3210},
        {'name': '猎德净水厂', 'lat': 23.1120, 'lng': 113.3370},
        {'name': '华南A谷', 'lat': 23.1470, 'lng': 113.3480}
    ]
}

# ================= 2. 距离计算函数 (不变) =================
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000 
    return c * r

def get_min_distance(house_row, poi_list):
    min_dist = float('inf')
    if pd.isna(house_row['Lng']) or pd.isna(house_row['Lat']):
        return 99999
    for poi in poi_list:
        dist = haversine(house_row['Lng'], house_row['Lat'], poi['lng'], poi['lat'])
        if dist < min_dist:
            min_dist = dist
    return min_dist

# ================= 3. 距离转分数函数 (不变) =================
def score_from_dist(dist, threshold):
    if dist > threshold:
        return 0
    return 100 * (1 - dist / threshold)

# ================= 主程序 =================
if __name__ == "__main__":
    print("1. 正在读取原始数据...")
    try:
        df = pd.read_csv('housePrice_Updated.csv', encoding='gbk')
    except FileNotFoundError:
        print("错误：找不到 'housePrice_Updated.csv'，请确保文件在当前目录下。")
        exit()

    # 范围稍微扩大，以包含智慧城和龙洞北部
    min_lat, max_lat = 23.10, 23.23
    min_lng, max_lng = 113.30, 113.45

    df_tianhe = df[
        (df['Lat'] >= min_lat) & (df['Lat'] <= max_lat) &
        (df['Lng'] >= min_lng) & (df['Lng'] <= max_lng) &
        (df['unit_price'] > 10000)
    ].copy()

    print(f"   筛选出天河区有效房源: {len(df_tianhe)} 条")
    print("2. 正在计算 5 个维度的便利度指标...")

    # --- 逐项计算距离和得分 ---
    
    # 1. 地铁 (1.5km)
    df_tianhe['dist_subway'] = df_tianhe.apply(lambda row: get_min_distance(row, POI_DATA['subway']), axis=1)
    df_tianhe['score_subway'] = df_tianhe['dist_subway'].apply(lambda x: score_from_dist(x, 1500))

    # 2. 商场 (2km)
    df_tianhe['dist_mall'] = df_tianhe.apply(lambda row: get_min_distance(row, POI_DATA['mall']), axis=1)
    df_tianhe['score_mall'] = df_tianhe['dist_mall'].apply(lambda x: score_from_dist(x, 2000))

    # 3. 学校 (1km - 学区房要求严苛)
    df_tianhe['dist_school'] = df_tianhe.apply(lambda row: get_min_distance(row, POI_DATA['school']), axis=1)
    df_tianhe['score_school'] = df_tianhe['dist_school'].apply(lambda x: score_from_dist(x, 1000))

    # 4. 公园 (2km)
    df_tianhe['dist_park'] = df_tianhe.apply(lambda row: get_min_distance(row, POI_DATA['park']), axis=1)
    df_tianhe['score_park'] = df_tianhe['dist_park'].apply(lambda x: score_from_dist(x, 2000))

    # 5. 【新增】公共服务 (2km - 医院/图书馆可以稍微远一点)
    df_tianhe['dist_public'] = df_tianhe.apply(lambda row: get_min_distance(row, POI_DATA['public_service']), axis=1)
    df_tianhe['score_public'] = df_tianhe['dist_public'].apply(lambda x: score_from_dist(x, 2000))

    # 3. 计算综合便利指数 (5项加权)
    # 权重：地铁0.3 + 学校0.25 + 商场0.15 + 公园0.15 + 公共0.15 = 1.0
    df_tianhe['accessibility_index'] = (
        df_tianhe['score_subway'] * 0.30 +
        df_tianhe['score_school'] * 0.25 +
        df_tianhe['score_mall']   * 0.15 +
        df_tianhe['score_park']   * 0.15 +
        df_tianhe['score_public'] * 0.15
    ).round(1)

    # 4. 导出结果 (只保留可视化必需字段，减少文件大小)
    output_cols = ['Lat', 'Lng', 'unit_price', 'accessibility_index']
    df_tianhe[output_cols].to_csv('final_data_tianhe.csv', index=False, float_format='%.4f')
    
    print("3. 处理完成！")
    print(f"   已生成文件: final_data_tianhe.csv")
    print(f"   平均便利指数: {df_tianhe['accessibility_index'].mean():.1f}")
    print(f"   Top3 便利小区: \n{df_tianhe.nlargest(3, 'accessibility_index')[['block','accessibility_index']]}")