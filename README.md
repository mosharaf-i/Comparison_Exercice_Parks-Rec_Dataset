# Comparison Excercise
#### Parks and Recreation Dataset, City of Toronto
**For checking the final analytics and GIS results in interactive maps, please see [Interactive Maps folder](./Interactive_Maps/)**
 
 ## 1.	Introduction

The City of Toronto maintains significant datasets of registered and drop-in programs offered by Parks and Recreation throughout the city.  
As part of this exercise, I gathered available open data related to Parks and Recreation programs, along with geospatial and neighbourhood profile data, 
to perform an analysis and present a comparison of population and programs distribution offered, based on my findings.  
The datasets, demographic groups, and methods of analysis considered are described in Section 2. Results of my study is then discussed in Section 3. The conclusion is then presented in Section 4, 
and finally, Section 5 outlines limitations and future work.


  
## 2.	Data and Methodology

The available open data from Parks and Recreation datasets used for analysis are as follows:
1.	Registered and drop-in programs [(Link)](https://open.toronto.ca/dataset/registered-programs-and-drop-in-courses-offering/);
2.	Neighborhoods’ boundaries [(Link)](https://open.toronto.ca/dataset/neighbourhoods/);
3.	Neighborhoods’ population demographic profiles [(Link)](https://open.toronto.ca/dataset/neighbourhood-profiles/).

The program datasets included information on registered and drop-in programs, their locations, and the facilities available at each site.
In this exercise, I was trying to find gaps in the programs offered by parks and recreation to the public. After reviewing the datasets and reflecting from personal and family experiences, 
I selected programs designed for young children and seniors for further investigation.

This is based on the observation that children and seniors tend to participate more in various programs at parks and community centres, as they generally have more free time than other age groups. 
They also benefit significantly from social interaction with peers in their community. 
As such, the analysis focused on understanding the distribution and percentage of hours dedicated to these two age groups at community recreation centres in Toronto.  
The first age group was selected based on the Government of Ontario's employment regulations, which state that the minimum age to work in any environment is 14 years [(Link)]( https://www.ontario.ca/page/minimum-age-work).
Additionally, the highest minimum age requirement in Parks and Recreation programs was found to be 60 years and over. Therefore, I chose programs with a maximum age of 14 and a minimum age of 60 for further study.  
In this process, however, it was noted that this filtering excludes some other programs that allow the possibility of this age range for participate, for example programs with no age limitation. This limitation, along
with others, is further discussed in Section 5.  
To understand how many programs were offered to these demographics, weekly and total program hours were calculated using Python. For each Program Category and Location ID,
weekly and total hours were computed. Programs that met the age restrictions were selected, and their weekly and total hours were divided by the overall hours in each category.

This calculation provided the percentage of program hours dedicated to the target demographic in each category. These results were then joined with the location dataset using the ‘Location ID’ column.
It was found that the location dataset did not include a direct key to join with the neighbourhood boundary dataset. 
To address this, the pgeocode library was used to connect location data via postal codes of community centres in Toronto. 
This enabled latitude and longitude information to be added and spatially joined with neighbourhood boundaries using QGIS.

Subsequentially all category hours percentages calculated were averaged for their corresponding neighbourhood.
Furthermore, to better understand how these distributions aligned with population demographics, the percentage of each age group in the population was extracted from the Neighbourhood Profile dataset. 

As population data for those aged 60 and over was not directly available, it was calculated by summing the 60–64 and 65+ age groups, then dividing by the total population of each neighbourhood using Excel.
Finally, the spatial distributions of populations under 14 and over 60, along with percentage of hours dedicated to these groups, were mapped and visualised using the geopandas, json, and pgeocode libraries 
in Python.
During the analysis, some records with incorrect data entries were identified and removed. These included:

•	2 records where start and end times were reversed (duration was negative);   
•	8 records with identical start and end times;  
•	1 record with a duration of only one minute.  

As the analysis considered only neighbourhoods that included community recreation centres and matching postal codes, only 62 of the 158 neighbourhoods had relevant data and were included in the final 
mapping and evaluation. The results and discussion are presented in the following section.

## 3.	Results and Discussion

This section presents and discusses the results of the analysis. After mapping both weekly and total program hour percentages across the city, it was found that the two metrics were similar. 
Therefore, only the total program hour percentages are discussed here. Also, to facilitate the comparing of findings, interactive maps for each category were created using folium library, and maps are included in the [Interactive Maps folder](./Interactive_Maps/). These maps also include the average weekly hours for comparison.  

### 3.1	Demographic: Under 14 years of age

This section presents visualised maps and discusses the comparison between neighbourhood population distribution and program hours dedicated to this demographic, identifying potential service gaps.
Figure 1 shows the distribution of the under-14 population. Thorncliffe Park has the highest proportion (24.4%), and several downtown, west, and northwest neighbourhoods also have notably younger populations. 
While camping programs appear to be well-distributed across the city (Figure 2), categories such as fitness (Figure 5), skating (Figure 8), and arts (Figure 7) have lower hours allocated for this group in 
neighbourhoods like Runnymede–Bloor West Village and Woodbine Corridor which can be increased. Sports activities can be also considered for extension in west of the city, areas such as Black Creek, 
Mount Olive-Silverstone-Jamestown, and Humbermede (Figure 4). These areas also lack swimming program distribution on the west and northwest of the city.

<p align="center">
<img width="984" height="670" alt="image" src="https://github.com/user-attachments/assets/ca90f9ad-5300-48ea-b09c-b1ef9590b35b" />
</p>
<p align="center">Figure 1: Population distribution of ages under 14, neighbourhoods’ name with higher than 17.5% are mentioned on the map.  </p>
    
<p align="center">
<img width="581" height="400" alt="image" src="https://github.com/user-attachments/assets/c0b49802-1877-4149-a827-cc85bfc9c802" />
</p>
<p align="center">Figure 2: Average Camp Total Hours %, Under 14  </p>

<p align="center">
<img width="579" height="401" alt="image" src="https://github.com/user-attachments/assets/0607a4e7-3217-4fa7-bee7-037d73fbba1b" />
</p>
<p align="center">Figure 3: Average Swimming Total Hours %, Under 14</p>

<p align="center">
<img width="581" height="400" alt="image" src="https://github.com/user-attachments/assets/eeae1452-9626-4f92-96b8-651a7ce61bdd" />
</p>
<p align="center">Figure 4: Average Sports Total Hours %, Under 14</p>

<p align="center">
<img width="581" height="403" alt="image" src="https://github.com/user-attachments/assets/f88c3944-f96f-4a5c-8e99-4134bbc5f6ba" />
</p>
<p align="center">Figure 5: Average Fitness Total Hours %, Under 14</p>

<p align="center">
<img width="582" height="400" alt="image" src="https://github.com/user-attachments/assets/63f3cae7-0af7-40cf-afee-a4671d361fb7" />
</p>
<p align="center">Figure 6: Average General Total Hours %, Under 14</p>

<p align="center">
<img width="582" height="400" alt="image" src="https://github.com/user-attachments/assets/2b7eb71d-a20f-4abf-85c6-c93d6e96aa29" />
</p>
<p align="center">Figure 7: Average Arts Total Hours %, Under 14</p>

<p align="center">
<img width="577" height="397" alt="image" src="https://github.com/user-attachments/assets/7afbd782-83a2-4d94-a8b5-309447aa361a" />
</p>
<p align="center">Figure 8: Average Skating Total Hours %, Under 14  </p>

Also, regarding Figure 8 and comparing to the rest of the program categories, skating programs are the least distributed program category around Toronto, with only 2 neighborhoods to include this category. 
In summary, neighbourhoods in the west and northwest of the city appear to have fewer programs designed for children under 14, despite having a considerable young population. These areas can be examined for further consideration.

### 3.2	Demographic: 60 and Over

After extracting the results, it was observed that there are no programs for individuals aged 60 and over in three categories: Camp, Swimming, and Skating. 
While it is understandable that camp and skating programs may not suit this age group, the absence of swimming programs specifically designed for seniors is unusual. 
Activities such as aqua therapy or water-walking classes tailored for older adults could be valuable additions to the programs. 

The other four categories were mapped and are presented in Figures 10 to 13. Regarding the population distribution of individuals aged 60 and over (Figure 9), 
several neighbourhoods with high proportions are visible, such as Hillcrest Village, Banbury–Don Mills, Agincourt North, Kingsway South, and Edenbridge–Humber Valley.
 
<p align="center">
<img width="1001" height="689" alt="image" src="https://github.com/user-attachments/assets/82786900-f7d7-4df2-86f7-337827855030" />
</p>
<p align="center">Figure 9: Population distribution of ages 60 and over, neighbourhoods’ name with higher than 30% are mentioned on the map</p>

<p align="center">
<img width="580" height="399" alt="image" src="https://github.com/user-attachments/assets/73097509-e1c5-4fd1-9559-c89164b018dc" />
</p>
<p align="center">Figure 10: Average Sports Total Hours %, 60 and over</p>                               

<p align="center">
<img width="580" height="399" alt="image" src="https://github.com/user-attachments/assets/8373e480-00f5-47b5-9ea3-777d45a1ae36" />
</p>
<p align="center">Figure 11: Average General Total Hours %, 60 and over</p>

<p align="center">
<img width="572" height="393" alt="image" src="https://github.com/user-attachments/assets/deba4aa0-02d3-4834-ab3e-18671fb949d6" />
</p>
<p align="center">Figure 12: Average Arts Total Hours %, 60 and over</p>

<p align="center">
<img width="569" height="393" alt="image" src="https://github.com/user-attachments/assets/7b560701-e571-4326-a960-8c068bbb3480" /></p>
<p align="center">Figure 13: Average Fitness Total Hours %, 60 and over  </p>

Although present in relatively low percentages, fitness programs are the most evenly distributed category across the city. The other three program categories of sports, arts, 
and general are less evenly spread, with sports and general programs being the least distributed. Furthermore, although the arts category appears more widely distributed, its 
availability in neighbourhoods with higher senior populations is minimal or nonexistent. These areas, including aforementioned areas with higher senior residents, should be considered 
for expansion of all four categories programming targeted at older adults as well as swimming programs.

## 4.	Conclusion

This study was conducted as part of an excercise with the Parks and Recreation dataset, with the goal of analysing available open datasets to examine and propose 
improvements to programming across the City of Toronto. To achieve this, programs for two age demographics of under 14 and over 60 were selected, and the average percentages of 
program hours dedicated to these groups were calculated. The population distribution of these age groups across the city was also analysed and compared with program data across 
62 Toronto neighbourhoods. Neighbourhoods with high concentrations of children and seniors were further examined in relation to the seven program categories. Areas with lower 
program hours dedicated to these age groups were identified, and opportunities for expanding relevant programming in those areas were highlighted. For seniors, lack of swimming, 
arts, general, and sport programs were identified throughout the city. For children also, west and northwest areas were found for expanding programs in various categories. 

## 5.	Limitations and Future Work

1.	When selecting programs with a maximum age of 14 and a minimum age of 60, some other programs that may also be suitable for these age groups were also excluded.
These include, but are not limited to, Swim to Survive and private music lessons. This limitation hinders the ability to fully capture the number of hours allocated to the target age groups.
2.	The location dataset did not include a key or identifier linking each location to a specific neighbourhood. As a result, many locations and associated programs were excluded from the analysis
if they lacked postal code data. These locations are such as parks and gardens. 
3.	After initial review of the datasets, no data on the participation or registration number of the programs was found. Access to participation data would enable analysis to model
and study different correlations between various parameters, like demographic and land-use parameters. This would provide a deeper understanding of how Parks and Recreation programming can be improved.
Therefore, it is recommended that participation data and survey results be included in future phases of this study. 
4.	During the review of the demographic profile datasets, some data inconsistencies were identified. For example, the population total for those aged 85 and older did not match the
sum of age subgroups (85–89, 90–94, 95–99, and 100+). Although further investigation was beyond the time constraints of this project, a more in-depth examination would improve data quality
and the resulting analysis. 
5.	Future Work:
The City of Toronto maintains a wide range of datasets that could support further analysis of Parks and Recreation programming. Several areas of focus could be explored in greater depth, such as including:  
 • Emerging Neighbourhoods and neighbourhood improvement areas;  
 • Household income and its effect on participation rates;  
 • Additional demographic and geographic breakdowns to tailor programming more equitably.


