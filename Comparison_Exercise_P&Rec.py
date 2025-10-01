### Comparison Exercise, Parks & Recreation Dataset


# 1. Import libraries
import os
import pandas as pd
import folium
import json
import geopandas as gpd
import matplotlib.pyplot as plt
import pgeocode
import contextily as ctx
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib as mpl


# 2. Folder address
os.chdir(r"C:\..._Files\Folder") 
parent_folder_path = os.path.join(os.getcwd(), 'C:\..._Files\Folder')  #Please change this directory to the parent local directory

# 3. Reading registered programs data
# rp = registered Programs
registered_programs_file_directory = os.path.join(parent_folder_path, 'Registered_Programs\Registered_Programs.csv')
rp = pd.read_csv(registered_programs_file_directory)



# 4. Calaculating hours of all programs
# 4.1 Calculating daily program duration from 'Start Hour' and 'End Hour' columns.
rp["start_time"] = pd.to_datetime(rp['Start Hour'].astype(str) + ':' + rp['Start Min'].astype(str), format='%H:%M')
rp["end_time"] = pd.to_datetime(rp['End Hour'].astype(str) + ':' + rp['End Min'].astype(str), format='%H:%M')
rp["daily_hours"] = rp["end_time"]  - rp["start_time"]

# 4.2 Calculating weekly hours from 'Days of The Week' column. 
# 4.2.1 Calculating number of days in a week 
rp['weekly_number_days'] = rp['Days of The Week'].str.split(',').str.len()
# 4.2.2 Calcualting weekly hours of programs
rp['weekly_hour'] = round(pd.to_timedelta(rp['weekly_number_days'] * rp["daily_hours"]).dt.total_seconds()/3600, 1)

# 4.3 Calculating annual hours of each program
# 4.3.1 Calculating annual ruuning weeks of each program
program_dates = pd.DataFrame()
program_dates[['start_date_str', 'end_date_str']] = rp['From To'].str.split(' to ', expand=True)
rp['start_date'] = pd.to_datetime(program_dates['start_date_str'], format='%b-%d-%Y')
rp['end_date'] = pd.to_datetime(program_dates['end_date_str'], format='%b-%d-%Y')

# Define day name to number mapping
day_map = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
# Step 3: Function to calculate total program days
def count_program_days(row):
    # Get list of allowed weekday numbers
    days = [day_map[d.strip()] for d in row['Days of The Week'].split(',')]
    
    # Create date range
    all_days = pd.date_range(start=row['start_date'], end=row['end_date'])
    
    # Filter based on weekday
    matching_days = [d for d in all_days if d.weekday() in days]
    
    return len(matching_days)

rp['program_day_count'] = rp.apply(count_program_days, axis=1)



# 4.3.2 Calcualting annual hours of each program
rp['total_program_hours'] = round(pd.to_timedelta(rp['program_day_count'] * rp['daily_hours']).dt.total_seconds()/3600, 1)
rp = rp[rp['total_program_hours'] >= 0.2] 

# 5. Calculating hours of all programs for each location and program category
loc = pd.Series(rp['Location ID']).unique()
cat = pd.Series(rp['Program Category']).unique()

new_rows_all = []

for i in loc:
    for n in cat:
        # Filter the matching rows in above60 and below14
        match = rp[(rp['Location ID'] == i) & (rp['Program Category'] == n)]
        
        # Calculate total hour values
        # Above 60
        total_weekly_hours = match['weekly_hour'].sum()
        total_program_hours = match['total_program_hours'].sum()

        # Append a new row to the results
        new_rows_all.append({'Location ID': i, 'Program Category': n, 'total_weekly_hours': total_weekly_hours, 'total_program_hours': total_program_hours})

# Create a new DataFrame from the collected rows
categorized_hours = pd.DataFrame(new_rows_all)



### 5. Selecting Age Categories
rp['Max Age']  = rp['Max Age'].fillna(200) #Filling empty max age range to 200.
below14 = rp[rp['Max Age'] < 14]
above60 = rp[rp['Min Age'] > 59]




# 6. Categorizing the programs for each program category and location IDs
new_rows_ages = []

for i in loc:
    for n in cat:
        # Filter the matching rows in above60 and below14
        match60 = above60[(above60['Location ID'] == i) & (above60['Program Category'] == n)]
        match14 = below14[(below14['Location ID'] == i) & (below14['Program Category'] == n)]
        
        # Calculate total hour values
        # Above 60
        total_weekly_hours60 = match60['weekly_hour'].sum()
        total_program_hours60 = match60['total_program_hours'].sum()
        # Under 14
        total_weekly_hours14 = match14['weekly_hour'].sum()
        total_program_hours14 = match14['total_program_hours'].sum()
        
        # Append a new row to the results
        new_rows_ages.append({'Location ID': i, 'Program Category': n, 
                           'total_weekly_hours_60': total_weekly_hours60, 'total_program_hours_60': total_program_hours60,
                           'total_weekly_hours_14': total_weekly_hours14, 'total_program_hours_14': total_program_hours14})

ages_categorized = pd.DataFrame(new_rows_ages)

# Calcualting the % of program hours
merged_categorized = pd.merge(categorized_hours, ages_categorized, left_on=['Location ID', 'Program Category'], right_on=['Location ID', 'Program Category'], how='inner')

merged_categorized['Hours_% Over60_Weekly'] = round(merged_categorized['total_weekly_hours_60']/merged_categorized['total_weekly_hours']*100, 1)
merged_categorized['Hours_% Over60_Total'] = round(merged_categorized['total_program_hours_60']/merged_categorized['total_program_hours']*100, 1)
merged_categorized['Hours_% Under14_Weekly'] = round(merged_categorized['total_weekly_hours_14']/merged_categorized['total_weekly_hours']*100, 1)
merged_categorized['Hours_% Under14_Total'] = round(merged_categorized['total_program_hours_14']/merged_categorized['total_program_hours']*100, 1)

merged_categorized = merged_categorized.fillna(0) #Filling all empty values with 0

### 7. Joining with the location file
location_file_directory = os.path.join(parent_folder_path, 'Registered_Programs\Locations.csv')
locations = pd.read_csv(location_file_directory)
locations_with_pc = locations[(locations['Postal Code'] != 'None') & (locations['Postal Code'].notna())]
locations_with_pc['PC'] = locations_with_pc['Postal Code'].str.split(' ').str[0] #Selecting the first section of the Postal Code

# Merging the Location with the calculated file 
program_locations_ages = pd.merge(merged_categorized, locations_with_pc, on='Location ID', how='inner')

# Connecting with the postal codes and spatial library to add lat/lon specifications
postal_codes = locations_with_pc['PC'].tolist()
nomi = pgeocode.Nominatim('ca')
toronto_pc = nomi.query_postal_code(postal_codes).drop_duplicates()

programs_spatial_ages = pd.merge(program_locations_ages, toronto_pc, left_on='PC', right_on='postal_code', how='inner')

#programs_spatial_ages.to_csv('program_locations_all.csv', index=False)
#toronto_pc.to_csv('toronto_post.csv', index=False)



### 8. Reading Neighbourhood Profiles File
profile_file_directory = os.path.join(parent_folder_path, 'Neighbourhood_Profiles\\neighbourhood-profiles-2021-158-model_added.xlsx')
profile = pd.read_excel(profile_file_directory, sheet_name='Considered_Rows')

# Transposing the columns and rows
profile_t = profile.transpose().reset_index()
profile_t.columns = profile_t.iloc[0]
profile_t = profile_t.drop(index=0)
profile_t['Total - Distribution (%) 0 to 14 years']= profile_t['Total - Distribution (%) 0 to 14 years'].astype(float)
profile_t['Total - Distribution (%) 60 years and over (calculated)']= round(profile_t['Total - Distribution (%) 60 years and over (calculated)'].astype(float), 1)



### 9. Reading and merging Neighbourhood Spatial File
neighbourhood_file_directory = os.path.join(parent_folder_path, 'Neighbourhoods\\Neighbourhoods - 4326.geojson')

# Read the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file(neighbourhood_file_directory)
gdf['AREA_SHORT_CODE'] = gdf['AREA_SHORT_CODE'].astype(int)
gdf.rename(columns={'AREA_SHORT_CODE': 'Neighbourhood Number'}, inplace=True)
merged_gdf = gdf.merge(profile_t, on="Neighbourhood Number", how="left")



#### 10. Plotting the Maps of Ppoulation Distribution
gdf = merged_gdf
# Checking to ensure it's in Web Mercator for contextily basemap
gdf = gdf.to_crs(epsg=3857)

# Setup color mapping
group = 'Total - Distribution (%) 0 to 14 years' #or'Total - Distribution (%) 60 years and over (calculated)'

column = group
cmap = plt.cm.coolwarm
vmin = gdf[column].min()
vmax = gdf[column].max()

norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Map Setting
fig, ax = plt.subplots(figsize=(24, 20))

gdf.plot(column= group,  #changing for each map
         cmap='coolwarm',
         linewidth=0.9,
         edgecolor='black',
         ax=ax,
         alpha=0.8,
         legend=False)

# Add custom colorbar with control
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.6, pad=0.02)
cbar.set_label("Population %", fontsize=30) #changing for each map
cbar.ax.tick_params(labelsize=18)

# Selecting areas to only show areas with high %
for idx, row in gdf.iterrows():
    if row[group] > 17.5:  #and 30% for 60+
        centroid = row.geometry.centroid
        ax.annotate(row['AREA_NAME'],
                    xy=(centroid.x, centroid.y),
                    ha='center', fontsize=11, color='black')

# Adding basemap
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, alpha=0.85)

# Adding scale bar
scalebar = ScaleBar(dx=1,
                    units="km",
                    location='lower right',
                    scale_loc='bottom',
                    length_fraction=0.2,
                    scale_formatter=lambda value, unit: f' {value} km ',
                    box_alpha=1)

ax.add_artist(scalebar)

# Adding north arrow
arrow_x, arrow_y = ax.get_xlim()[1] - 1000, ax.get_ylim()[1] - 1000
ax.annotate('N', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y - 5000),
            arrowprops=dict(facecolor='black', width=20, headwidth=50),
            ha='center', fontsize=40, color='black')
# Axis titles
ax.set_title("Toronto Population % of Under 14", fontsize=40) # Under 14/60 and Over

# Remove axes
ax.set_axis_off()
plt.tight_layout()
plt.show()

### Mapping Program and Neighbourhoods Boundaries from joined file in QGIS
joined = os.path.join(parent_folder_path, 'QGIS\programs_nb_joined.geojson')

# Read the GeoJSON file into a GeoDataFrame
jn = gpd.read_file(joined)
column_names = jn.columns

# Removing epmty rows and columns
jn = jn[jn['Location Name'].notna()]

# Summing Over Neighbourhoods
jn['AREA_SHORT_CODE'] = jn['AREA_SHORT_CODE'].astype(int)
neig_num = pd.Series(jn['AREA_SHORT_CODE']).unique()
new_rows_neigh = []

for i in neig_num:
    for n in cat:
        # Filter the matching rows in above60 and below14
        match_neigh = jn[(jn['AREA_SHORT_CODE'] == i) & (jn['Program Category'] == n)]

        # Calculate sum of percentage hours in each category for each neighbourhood
        weekly_hours60 = match_neigh['Hours_% Over60_Weekly'].mean()
        total_hours60 = match_neigh['Hours_% Over60_Total'].mean()
        weekly_hours14 = match_neigh['Hours_% Under14_Weekly'].mean()
        total_hours14 = match_neigh['Hours_% Under14_Total'].mean()
        
        # Append a new row to the results
        new_rows_neigh.append({'Neighbourhood Number': i, 'Program Category': n, 
                           'Avg_Hours%_Over60_Weekly': weekly_hours60, 'Avg_Hours_%_Over60_Total': total_hours60,
                           'Avg_Hours_%_Under14_Weekly': weekly_hours14, 'Avg_Hours_%_Under14_Total': total_hours14})

cat_neigh = pd.DataFrame(new_rows_neigh)

# Joining with the Neighbourhood file for mapping 
merged_cat_hours = gdf.merge(cat_neigh, on="Neighbourhood Number", how="left")

merged_cat_hours = merged_cat_hours.rename(columns={'Avg_Hours%_Over60_Weekly': 'Average Weekly Hour % - 60 years and over', 
                                                    'Avg_Hours_%_Over60_Total': 'Average Total Hour % - 60 years and over',
                                                    'Avg_Hours_%_Under14_Weekly': 'Average Weekly Hour % - 0 to 14 years',
                                                    'Avg_Hours_%_Under14_Total': 'Average Total Hour % - 0 to 14 years'})

# Creating separate datasets for easier visualisation
camp = merged_cat_hours.loc[merged_cat_hours['Program Category'] == 'Camps']
fit = merged_cat_hours.loc[merged_cat_hours['Program Category'] == 'Fitness']
sport = merged_cat_hours.loc[merged_cat_hours['Program Category'] == 'Sports']
gen = merged_cat_hours.loc[merged_cat_hours['Program Category'] == 'General']
art = merged_cat_hours.loc[merged_cat_hours['Program Category'] == 'Arts']
swim = merged_cat_hours.loc[merged_cat_hours['Program Category'] == 'Swimming']
skt = merged_cat_hours.loc[merged_cat_hours['Program Category'] == 'Skating']



# 11. Creating Interactive Maps for each category
# Converting each category dataset to json data to create interactive maps
geojson_data = json.loads(skt.to_json()) #changing the data for creating each map, 
                                         #(A loop can be added for creating all the maps too)

# Create a map object
m = folium.Map(location=[43.70011, -79.4163], zoom_start=11, tiles=None) #Toronto mid-point lon/lat

# Adding custom tiles (Stadia Maps - Alidade Smooth)
folium.TileLayer(
    tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by Humanitarian OpenStreetMap Team',
    name='OSM HOT',
    overlay=False,
    control=True).add_to(m)

# Define the tooltip fields from GeoJSON properties
tooltip_fields = ['Neighbourhood Name', 'Program Category','Total - Distribution (%) 0 to 14 years', 
                  'Average Weekly Hour % - 0 to 14 years',
                  'Average Total Hour % - 0 to 14 years',  
                  'Total - Distribution (%) 60 years and over (calculated)',
                  'Average Weekly Hour % - 60 years and over',
                  'Average Total Hour % - 60 years and over']
tooltip_aliases = [f'{field.title()}: ' for field in tooltip_fields]

# Choosing a property to base style on (differentiating areas including data and NA)
# Here it won't be used since the category sub-datasets only include 62 areas and not all
style_field = 'Total - Distribution (%) 0 to 14 years'

# Adding styling feature
def style_function(feature):
    value = feature['properties'].get(style_field)
    if value is None:
        # Style for null values
        return {
            'fillColor': 'gray',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.4
        }
    else:
        # Style for non-null values
        return {
            'fillColor': 'purple',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        }

# Adding styled GeoJSON layer with tooltip
folium.GeoJson(
    geojson_data,
    name='Styled GeoJSON',
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=tooltip_fields,
        aliases=tooltip_aliases,
        sticky=True,
        localize=True)).add_to(m)

# Adding layer control
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('skating_map.html')



# 12. Plotting maps of hours % for each category
gdf = fit #change for each category
cat_name = ' Fitness ' #change for each category
parameter = 'Average Total Hour % - 60 years and over' #change for weekly/total, and 14/60+
par_title = 'Average Total Hour %, Age Range: 60 and Over, Category:' #change for weekly/total, and 14/60+

# Setup color mapping
column = parameter
cmap = plt.cm.coolwarm
vmin = gdf[column].min()
vmax = gdf[column].max()

# Create color norm and scalar mappable for legend
norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Figure Setting
fig, ax = plt.subplots(figsize=(24, 20))

# Plotting choropleth: graduated coloring
gdf.plot(column= parameter,
         cmap='coolwarm',          # choose suitable color map
         linewidth=0.9,
         edgecolor='black',
         ax=ax,
         alpha=0.8,
         legend=False
         )

# Adding custom colorbar with control
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.6, pad=0.02)
cbar.set_label('Average Hours %', fontsize=30) #changing for each map
cbar.ax.tick_params(labelsize=18)

# Adding greyscale basemap
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, alpha=0.85)

# Adding scale bar
scalebar = ScaleBar(dx=1,        # meters per pixel
                    units="km",
                    location='lower right',
                    scale_loc='bottom',
                    length_fraction=0.2,
                    scale_formatter=lambda value, unit: f' {value} km ',
                    box_alpha=1)
ax.add_artist(scalebar)

# Adding north arrow
arrow_x, arrow_y = ax.get_xlim()[1] - 1000, ax.get_ylim()[1] - 1000
ax.annotate('N', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y - 5000),
            arrowprops=dict(facecolor='black', width=20, headwidth=50),
            ha='center', fontsize=40, color='black')

# Axis titles
ax.set_title(par_title + cat_name, fontsize=30)
ax.set_axis_off()
plt.tight_layout()
plt.show()

### END OF SCRIPT ###