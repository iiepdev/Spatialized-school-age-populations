# Spatialized school age populations

- [English version](#english-version)
- [Versión en Español](#version-espanol)
- [Version en Français](#version-en-français)

## English version
 
This is the package related to the IIEP 2021 paper "Estimating school-age populations by applying Sprague multipliers to raster data" (https://unesdoc.unesco.org/ark:/48223/pf0000379198). This methodology uses Sprague multipliers to interpolate data and obtain population estimates by single years of age for different administrative boundaries (polygons), that are then reassembled according to any official school-age groups for any territory. 

This approach can be applied to other types of polygons, any country or administrative division, by simply changing the corresponding population estimates' raster files, and changing the names to the territory in question. The methodology is illustrated with Bangladesh, and robustness checks are performed on Canada, Colombia, Rwanda, Seychelles, and Uganda. 

The information needed to run this model (gridded population count datasets, by axe and sex) can be downloaded freely from the WorldPop webpage (https://www.worldpop.org/project/categories?id=8). The model supports unconstrained, constrained, and UN-adjusted constrained population estimates. All databases from 0 to 39 years of age must be downloaded for Males and Females for the country of interest, and stored in a single local folder. The QGIS model, called "Spatialized-school-age-populations-QGIS-model.model3" must be opened from QGIS, and then run following the instrusctions included in the model. A detailed explanation of the methodology can be found in the forthcoming paper. 

To allow for maximum transparency and replicability, all supporting documents, calculations, codes, databases, and images are available to the public . This includes  commented Jupyter notebooks for all mentioned countries. In order to open the files included on these folders, the user will need to have QGIS 3.X installed on their computer, and Jupyter notebook to view the Robustness checks. The databases used can be downloaded from https://box.iiep.unesco.org/s/TkPrnQyXYr6Qtjd under the Data folder.

IIEPdev work is available under the Open Access under the Attribution-ShareAlike 3.0 IGO (CC-BY-SA 3.0 IGO) licence (http://creativecommons.org/licenses/by-sa/3.0/igo/). By using the content of this repository, the users accept to be bound by the terms of use of the UNESCO Open Access Repository (http://www.unesco.org/open-access/terms-use-ccbysa-en).

Designations employed and the presentation of the materials resulting from the use of this code do not imply the expression of any opinion whatsoever from the UN, UNESCO, or IIEP-UNESCO concerning the legal status of any country, territory, city, area, authorities, concerning the delimitation of frontiers or boundaries.

This material has been partly funded by UK aid from the UK government; however the views expressed do not necessarily reflect the UK government’s official policies.

Was this tool helpful? Let us know how you used it, and suggest improvements by contacting us development@iiep.unesco.org

### Metadata

#### Spatialized school age populations - Didactic example.xlsx

Excel file that allows users to explore the internal functioning of the Sprague multipliers, as well as obtaining disaggregated single years of age for any group of 5-year age groups.

#### Spatialized school age populations -Canada.ipynb

This Jupyter notebook uses the Sprague multipliers' methodology to estimate the population by single years of age for different polygons from raster data" for the Canadian Census of 2016. It uses raster data from WorldPop (https://www.worldpop.org/geodata/summary?id=15778), and the information on the Census was obtained from Statistics Canada (https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/dt-td/Rp-eng.cfm?TABID=4&LANG=E&A=R&APATH=3&DETAIL=0&DIM=0&FL=A&FREE=0&GC=10&GL=-1&GID=1235626&GK=1&GRP=1&O=D&PID=109523&PRID=10&PTYPE=109445&S=0&SHOWALL=0&SUB=0&Temporal=2016&THEME=115&VID=0&VNAMEE=&VNAMEF=&D1=0&D2=0&D3=0&D4=0&D5=0&D6=0), from the 2016 National Census, particularly for Census Metropolitan Areas and Census Agglomerations. The information on the starting age and duration of each educational level, used for the reconstruction of the educational level populations for both census and projection data was obtained from data.uis.unesco.org.

#### Spatialized school age populations -Colombia.ipynb

This Jupyter notebook uses the Sprague multipliers' methodology to estimate the population by single years of age for different polygons from raster data" for the Colombian Census of 2018. It uses raster data from WorldPop (https://www.worldpop.org/geodata/summary?id=16325), and the information on the Census was obtained from the National Bureau of Statistics of Colombia - DANE (http://microdatos.dane.gov.co/index.php/catalog/643/data_dictionary), from the 2018 National Census, for all 1118 municipalities. The information on the starting age and duration of each educational level, used for the reconstruction of the educational level populations for both census and projection data was obtained from data.uis.unesco.org. The shapefiles for the municipalities was obtained from HDX (https://data.humdata.org/dataset/colombia-administrative-boundaries-levels-0-3)

#### Spatialized-school-age-populations-Rwanda.ipynb

This Jupyter notebook uses the Sprague multipliers' methodology to estimate the population by single years of age for different polygons from raster data" for the Rwandan Census of 2012. It uses raster data from WorldPop (https://www.worldpop.org/geodata/summary?id=14905), and the information on the Census was obtained from the National Bureau of Statistics of Rwanda (https://microdata.statistics.gov.rw/index.php/catalog/65), from the 2012 National Census. The information on the starting age and duration of each educational level, used for the reconstruction of the educational level populations for both census and projection data was obtained from data.uis.unesco.org. The shapefiles for the municipalities was obtained from HDX (https://data.humdata.org/dataset/rwanda-administrative-boundaries-level-1-4)

#### Spatialized-school-age-populations-Seychelles.ipynb

This Jupyter notebook uses the Sprague multipliers' methodology to estimate the population by single years of age for different polygons from raster data" for the Seychelles Census of 2019. It uses raster data from WorldPop (https://www.worldpop.org/geodata/summary?id=16736), and the information on the Census was obtained from the National Bureau of Statistics of Seychelles (https://data.humdata.org/dataset/seychelles-subnational-population-statistics), from the 2019 National Census. The information on the starting age and duration of each educational level, used for the reconstruction of the educational level populations for both census and projection data was obtained from data.uis.unesco.org. The shapefiles for the municipalities was obtained from HDX (https://data.humdata.org/dataset/seychelles-subnational-administrative-boundaries)

#### Spatialized-school-age-populations-Uganda.ipynb

This Jupyter notebook uses the Sprague multipliers' methodology to estimate the population by single years of age for different polygons from raster data" for the Ugandan Census of 2020. It uses raster data from WorldPop (https://www.worldpop.org/geodata/summary?id=16920), and the information on the Census was obtained from the National Bureau of Statistics of Uganda (https://data.humdata.org/dataset/uganda-administrative-level-population-statistics), from the 2020 National Census. The information on the starting age and duration of each educational level, used for the reconstruction of the educational level populations for both census and projection data was obtained from data.uis.unesco.org. The shapefiles for the municipalities was obtained from HDX (https://data.humdata.org/dataset/uganda-administrative-boundaries-admin-1-admin-3)

#### Spatialized-school-age-populations-QGIS-model.model3

This QGIS model is a ready-made methodology to estimate the single years of age by sex from 0 to 39 years old for any administrative division or polygon layer. It requires population estimates  to be downloaded from WorldPop, and is adaptable to unconstrained, constrained, and UN-adjusted constrained population estimates. The model can also reconstruct all levels of education up to Upper secondary education. 

#### Spatialized-school-age-populations.py

This Python model is the export of the QGIS model presented above. It contains the same functionalities, but is more easily modifiable. 

<h2 id="version-espanol">
Versión en Español
</h2>

## Version en Français 
