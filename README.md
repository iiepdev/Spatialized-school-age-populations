# Spatialized school age populations
 
This is the package related to the IIEP (2021, forthcoming) paper "Estimating school-age populations by applying Sprague multipliers to raster data". 
This methodology uses Sprague multipliers to interpolate data and obtain population estimates by single years of age for different administrative boundaries (polygons), that are then reassembled according to any official school-age groups for any territory. 

This approach can be applied to other types of polygons, any country or administrative division, by simply changing the corresponding population estimates' raster files, and changing the names to the territory in question. The methodology is illustrated with Bangladesh, and robustness checks are performed on Canada, Colombia, Rwanda, Seychelles, and Uganda. 

The information needed to run this model can be downloaded freely from the WorldPop webpage (https://www.worldpop.org/project/categories?id=8). It supports unconstrained, constrained, and UN-adjusted constrained population estimates. All databases from 0 to 39 years of age must be downloaded for Males and Females for the country of interest, and stored in a single local folder. The QGIS model, called "Spatialized-school-age-populations-QGIS-model.model3" must be opened from QGIS, and then run following the instrusctions included in the model. A detailed explanation of the methodology can be found in the forthcoming paper. 

To allow for maximum transparency and replicability, all supporting documents, calculations, codes, databases, and images are available to the public . This includes  commented Jupyter notebooks for all mentioned countries. In order to open the files included on these folders, the user will need to have QGIS 3.X installed on their computer, and Jupyter notebook to view the Robustness checks. The databases used can be downloaded from https://box.iiep.unesco.org/s/TkPrnQyXYr6Qtjd under the Data folder.

IIEPdev work is available under the Open Access under the Attribution-ShareAlike 3.0 IGO (CC-BY-SA 3.0 IGO) licence (http://creativecommons.org/licenses/by-sa/3.0/igo/). By using the content of this repository, the users accept to be bound by the terms of use of the UNESCO Open Access Repository (http://www.unesco.org/open-access/terms-use-ccbysa-en).

This material has been partly funded by UK aid from the UK government; however the views expressed do not necessarily reflect the UK government’s official policies.

Was this tool helpful? Let us know how you used it, and suggest improvements by contacting us development@iiep.unesco.org
