from numba.np.arraymath import np_imag

# !pip install geopandas shapely
# !pip install netCDF4
# !pip install h5netcdf
# !pip install xarray
# !pip install shapely
# !pip install geopandas
# !pip install matplotlib
import numpy as np
import xarray as xarray
import shapely as shapely

xmin, xmax = -141, -53 
ymin, ymax = 41.555, 82.68 
grid_size_initial = 0.125  
grid_size_rest = 0.25  


def generate_longitude_vals(xmin, xmax, initial_step, rest_step):
    x_vals = [xmin]
    current_long = xmin + initial_step
    x_vals.append(current_long)
    while current_long < xmax:
        current_long += rest_step
        x_vals.append(current_long)
    return np.array(x_vals)
x_vals = generate_longitude_vals(xmin, xmax, grid_size_initial, grid_size_rest)
y_vals = np.arange(ymin, ymax, grid_size_rest) 
grid_data = []
grid_id = 0  


for x_idx, x in enumerate(x_vals[:-1]):  #the last one not join in
    for y_idx, y in enumerate(y_vals[:-1]):  
        polygon = Polygon([(x, y), (x_vals[x_idx + 1], y), (x_vals[x_idx + 1], y + grid_size_rest), (x, y + grid_size_rest)])
        grid_data.append({'geometry': polygon, 'grid_id': grid_id, 'x_idx': x_idx, 'y_idx': y_idx})
        grid_id += 1  

# transfer to GeoDataFrame
grid_gdf = gpd.GeoDataFrame(grid_data)

grid_gdf.set_crs(epsg=4326, inplace=True)

print(grid_gdf[['grid_id', 'x_idx', 'y_idx']].head())


#%%
import geopandas as gpd
import matplotlib.pyplot as plt


county_map = gpd.read_file("/Users/liujingyi/Desktop/map/2021_cd/data/lcd_000b21a_e.shp")
# county_map = gpd.read_file("/Users/liujingyi/Desktop/map/2021_cd/DLI_2021_Census_CBF_Eng_Nat_cd_GeoPortal/DLI_2021_Census_CBF_Eng_Nat_cd.shp")
# check head
print(county_map.head())


print(county_map.crs)
# print(county_map[['CDUID']])
print(county_map[['CDUID']])
#%%
county_map = county_map.to_crs(epsg=4326)
# 简化几何形状，tolerance 值可根据需要调整
county_map['geometry'] = county_map['geometry'].simplify(tolerance=0.001, preserve_topology=True)

#%%
# set county map size
fig, ax = plt.subplots(figsize=(10, 10))

# draw picture
county_map.plot(ax=ax, color='lightblue', edgecolor='black')

# set title
ax.set_title('Canada CDUID Map')


plt.show()

#%%
# set map size
fig, ax = plt.subplots(figsize=(10, 10))

# draw map
county_map.plot(ax=ax, color='lightblue', edgecolor='black')

# draw fishnet
grid_gdf.boundary.plot(ax=ax, color='red', linewidth=0.5)

# set title
ax.set_title('Canada CDUID Map & 0.25° x 0.25° Fishnet')


plt.show()


#%%
overlay_gdf = gpd.overlay(county_map, grid_gdf, how='intersection')
print(overlay_gdf.head())

#%%
# show GeoDataFrame
grid_gdf = grid_gdf.to_crs(epsg=4326)
county_map = county_map.to_crs(epsg=4326)
fig, ax = plt.subplots(figsize=(10, 10))
overlay_gdf.plot(ax=ax, color='lightgreen', edgecolor='black')
ax.set_title('county map and fishnet')
plt.show()

#%%
print(overlay_gdf.columns)
print(overlay_gdf.head(100))
#%%
# calculate the overlap area
overlay_gdf['intersection_area'] = overlay_gdf.area

print(overlay_gdf.head())

#%%
# check DataFrame column
print(overlay_gdf.columns)
#%%
# calculate the centroid
overlay_gdf['centroid'] = overlay_gdf.centroid

# check longitude and latitude
overlay_gdf['latitude'] = overlay_gdf['centroid'].y
overlay_gdf['longitude'] = overlay_gdf['centroid'].x

grid_gdf['grid_id'] = grid_gdf.index

print(overlay_gdf[['grid_id', 'CDUID', 'intersection_area', 'latitude', 'longitude']].head())
print(len(overlay_gdf))
print(overlay_gdf.head(120))
print(grid_gdf.crs)
print(county_map.crs)
#%%
# calculate county area
# overlay_gdf['county_area'] = overlay_gdf['LANDAREA']
county_map['county_area'] = county_map.area
# check
print(county_map[['CDUID', 'county_area']].head())

# merge into DataFrame
overlay_gdf = overlay_gdf.merge(county_map[['CDUID', 'county_area']], on='CDUID')

print(overlay_gdf[['grid_id', 'CDUID', 'intersection_area', 'county_area']].head())

#%%
# check the ratio
overlay_gdf['grid_area_ratio'] = overlay_gdf['intersection_area'] / overlay_gdf['county_area']

print(overlay_gdf[['grid_id', 'CDUID', 'intersection_area', 'county_area', 'grid_area_ratio']].head())


#%%
# extract grid_id, CDUID, intersection_area, county_area, area_ratio
result = overlay_gdf[['grid_id', 'CDUID', 'intersection_area', 'county_area', 'grid_area_ratio']]

print(result.head())

#%%
print(overlay_gdf.head(100))
#%%
print(county_map[['CDUID']].drop_duplicates().sort_values(by='CDUID'))

#%%
print(overlay_gdf[['CDUID']])

#%%
# check any difference between maps
missing_CDUID = set(county_map['CDUID']) - set(overlay_gdf['CDUID'])
print(f"Missing counties: {missing_CDUID}")

#%%
# check process^^
# 筛选出CDUID为6001的所有行
cduid_6001_df = overlay_gdf[overlay_gdf['CDUID'] == '6001']

# 显示结果
print(cduid_6001_df)


#%%
# calculate sum of all ratio =1
total_grid_ratio = cduid_6001_df['grid_area_ratio'].sum()
print(f"Total grid area ratio for CDUID 6001: {total_grid_ratio}")

#%%
# check total columns
print(cduid_6001_df[['grid_id', 'intersection_area', 'county_area', 'grid_area_ratio']])

#%%
# save to csv
overlay_gdf.to_csv("overlay_result_2021.csv", index=False)
overlay_gdf.to_csv("/Users/liujingyi/Desktop/map/overlay_result_2021.csv", index=False)

#%%

# filter 6001 area
cduid_6001_df = overlay_gdf[overlay_gdf['CDUID'] == '6001']

# check results
print(cduid_6001_df[['grid_id', 'intersection_area', 'county_area', 'grid_area_ratio']].head())

#%%
# import matplotlib.pyplot as plt
# county_6001 = overlay_gdf[overlay_gdf['CDUID'] == '4815']
# fig, ax = plt.subplots(figsize=(10, 10))
# county_6001.plot(ax=ax, color='lightgray', edgecolor='black')
# cduid_6001_df.plot(ax=ax, edgecolor='red', alpha=0.5)
# plt.title('Grid Locations within County CDUID 6001')
# 
# plt.show()
import matplotlib.pyplot as plt

# 筛选出 CDUID 为 4815 的区域
county_4815 = overlay_gdf[overlay_gdf['CDUID'] == '4815']

# 创建图表
fig, ax = plt.subplots(figsize=(10, 10))

# 绘制县区地图
county_4815.plot(ax=ax, color='lightgray', edgecolor='black')

# 如果你有特定的网格数据可以叠加，比如 cduid_4815_df，请确保它已定义
# 否则，以下代码可能需要根据你的数据结构做调整
# cduid_4815_df.plot(ax=ax, edgecolor='red', alpha=0.5)

# 添加标题
plt.title('Grid Locations within County CDUID 4815')

# 显示图像
plt.show()

#%%
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 读取 CSV 数据
csv_path = '/Users/liujingyi/Desktop/map/overlay_result_2021.csv'
grid_ratio_data = pd.read_csv(csv_path)

# 创建地理信息 (geometry)
geometry = [Point(xy) for xy in zip(grid_ratio_data['longitude'], grid_ratio_data['latitude'])]
geo_df = gpd.GeoDataFrame(grid_ratio_data, geometry=geometry)

# 设置坐标系（假设是 WGS84）
geo_df.crs = "EPSG:4326"

# 保存为 Shapefile
shp_path = '/Users/liujingyi/Desktop/map/overlay_result_1986.shp'
geo_df.to_file(shp_path, driver='ESRI Shapefile')

#%%
