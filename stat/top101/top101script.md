-   [Dataset](#dataset)
    -   [Shot type plot](#shot-type-plot)
-   [Image distribution per species](#image-distribution-per-species)
-   [File size distribution](#file-size-distribution)
    -   [What is the mean size in kilobytes?](#what-is-the-mean-size-in-kilobytes)
    -   [Plotting file size](#plotting-file-size)
-   [Image dimensions](#image-dimensions)
    -   [Plotting the image dimensions](#plotting-the-image-dimensions)
    -   [Image examples](#image-examples)

``` r
setwd(
    "~/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/stat/top101"
)

library(ggplot2) # for plotting
library(jpeg)
library(imager) # for reading jpg files
library(reshape2) # for using melt()
library(magick) # for image conversion because jpg files are read

data_dir <- # Setting the directory that contains all the images
    "~/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/data/2018-01-17_top101-images"

top101 <-
    read.csv('top101.csv') # spreadsheat containing catalognumber, scientific name,
# shot_type and image url
```

Dataset
=======

``` r
# head(top101)
summary(top101)
```

    ##        catalog_number                   scientific_name shot_type
    ##  anic32-002152:    3   camponotus_maculatus     : 462   d:3409   
    ##  anic32-002153:    3   pheidole_megacephala     : 377   h:3392   
    ##  anic32-002156:    3   camponotus_hova          : 269   p:3424   
    ##  anic32-063120:    3   tetramorium_sericeiventre: 192            
    ##  antweb1008080:    3   hypoponera_punctatissima : 190            
    ##  antweb1008081:    3   dorylus_nigricans        : 183            
    ##  (Other)      :10207   (Other)                  :8552            
    ##                                                                 image_url    
    ##  http://www.antweb.org/images/anic32-002152/anic32-002152_d_1_low.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002152/anic32-002152_h_1_low.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002152/anic32-002152_p_1_low.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002153/anic32-002153_d_1_low.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002153/anic32-002153_h_1_low.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002153/anic32-002153_p_1_low.jpg:    1  
    ##  (Other)                                                             :10219

``` r
str(top101)
```

    ## 'data.frame':    10225 obs. of  4 variables:
    ##  $ catalog_number : Factor w/ 3441 levels "anic32-002152",..: 544 544 544 547 547 547 552 552 552 595 ...
    ##  $ scientific_name: Factor w/ 97 levels "amblyopone_australis",..: 1 1 1 1 1 1 1 1 1 1 ...
    ##  $ shot_type      : Factor w/ 3 levels "d","h","p": 2 3 1 2 3 1 2 3 1 2 ...
    ##  $ image_url      : Factor w/ 10225 levels "http://www.antweb.org/images/anic32-002152/anic32-002152_d_1_low.jpg",..: 1615 1616 1614 1624 1625 1623 1639 1640 1638 1768 ...

``` r
species <- data.frame(count(top101$scientific_name))
species[order(species[, 2], decreasing = T),]
```

    ##                             x freq
    ## 14       camponotus_maculatus  462
    ## 64       pheidole_megacephala  377
    ## 12            camponotus_hova  269
    ## 92  tetramorium_sericeiventre  192
    ## 39   hypoponera_punctatissima  190
    ## 36          dorylus_nigricans  183
    ## 80        solenopsis_geminata  157
    ## 33           diacamma_rugosum  154
    ## 63            pheidole_indica  153
    ## 93     tetramorium_simillimum  145
    ## 69             pheidole_parva  134
    ## 68         pheidole_pallidula  133
    ## 30  crematogaster_ranavalonae  129
    ## 61           pheidole_fervens  129
    ## 49          mystrium_camillae  125
    ## 57   paratrechina_longicornis  122
    ## 21       cardiocondyla_emeryi  120
    ## 2   anochetus_madagascarensis  117
    ## 3   aphaenogaster_swammerdami  114
    ## 46       monomorium_floricola  114
    ## 86      technomyrmex_pallipes  114
    ## 91    tetramorium_lanuginosum  114
    ## 34             dorylus_fulvus  113
    ## 13        camponotus_irritans  112
    ## 74        pheidole_variabilis  111
    ## 72       pheidole_sculpturata  108
    ## 84    tapinoma_melanocephalum  108
    ## 16     camponotus_punctulatus  107
    ## 18     camponotus_rufoglaucus  107
    ## 44        leptogenys_diminuta  106
    ## 11     camponotus_grandidieri  105
    ## 25     crematogaster_castanea  105
    ## 38     gnamptogenys_striatula  105
    ## 43         lepisiota_capensis  105
    ## 65         pheidole_mooreorum  105
    ## 62           pheidole_flavens  104
    ## 7         camponotus_atriceps  103
    ## 17 camponotus_quadrimaculatus  102
    ## 5       bothroponera_cambouei  101
    ## 96     wasmannia_auropunctata  101
    ## 20      camponotus_variegatus  100
    ## 35              dorylus_kohli   99
    ## 66             pheidole_nodus   99
    ## 75      platythyrea_parallela   99
    ## 52            mystrium_rogeri   96
    ## 89    tetramorium_bicarinatum   95
    ## 94    trichomyrmex_destructor   95
    ## 31  crematogaster_rasoherinae   94
    ## 10         camponotus_christi   93
    ## 54      nylanderia_bourbonica   93
    ## 81          strumigenys_emmae   91
    ## 27      crematogaster_dentata   90
    ## 82     strumigenys_louisianae   90
    ## 6   brachyponera_sennaarensis   89
    ## 45         monomorium_exiguum   88
    ## 70        pheidole_punctulata   88
    ## 1        amblyopone_australis   87
    ## 58        pheidole_aurivillii   87
    ## 71     pheidole_radoszkowskii   84
    ## 79           solenopsis_fugax   84
    ## 85       technomyrmex_albipes   84
    ## 26      crematogaster_crinosa   82
    ## 8       camponotus_auropubens   81
    ## 23       cataulacus_intrudens   81
    ## 32  crematogaster_stadelmanni   81
    ## 51          mystrium_mysticum   81
    ## 53      nomamyrmex_esenbeckii   80
    ## 56          ochetellus_glaber   78
    ## 78        pseudoponera_stigma   78
    ## 88      tetramorium_aculeatum   78
    ## 42             labidus_coecus   77
    ## 29      crematogaster_kelleri   75
    ## 67          pheidole_oceanica   75
    ## 73          pheidole_susannae   75
    ## 83         strumigenys_rogeri   75
    ## 95        vollenhovia_oblonga   75
    ## 48     monomorium_termitobium   74
    ## 19          camponotus_thraso   72
    ## 24          colobopsis_vitrea   72
    ## 28 crematogaster_gerstaeckeri   72
    ## 37          eciton_burchellii   72
    ## 60            pheidole_caffra   72
    ## 90      tetramorium_caespitum   72
    ## 76          polyrhachis_dives   71
    ## 47       monomorium_subopacum   70
    ## 59      pheidole_biconstricta   70
    ## 9      camponotus_bonariensis   69
    ## 22           carebara_diversa   69
    ## 40         iridomyrmex_anceps   69
    ## 41       kalathomyrmex_emeryi   69
    ## 50            mystrium_mirror   69
    ## 55 nylanderia_madagascarensis   69
    ## 77      pseudomyrmex_gracilis   69
    ## 97      zasphinctus_imbecilis   69
    ## 4               azteca_alfari   68
    ## 15          camponotus_planus   68
    ## 87     technomyrmex_vitiensis   68

``` r
levels(top101$shot_type)[levels(top101$shot_type) == 'd'] <-
    'dorsal'
levels(top101$shot_type)[levels(top101$shot_type) == 'h'] <- 'head'
levels(top101$shot_type)[levels(top101$shot_type) == 'p'] <-
    'profile'

# https://stackoverflow.com/questions/8186436/order-stacked-bar-graph-in-ggplot
top101_transp <- read.csv('top101_transp.csv', sep = ';')
top101_transp$total <- NULL # remove total
top101_transp$scientific_name <-
    reorder(top101_transp$scientific_name, rowSums(top101_transp[-1])) # reorder based on a non-created total
melted <-
    melt(top101_transp, id = 'scientific_name') # melt based on scientific_name
```

Shot type plot
--------------

![](top101script_files/figure-markdown_github/Shot%20type%20plot-1.png)

Image distribution per species
==============================

Here we can see how images are distributed per species. Within species there are 3 different shot types. p = profile, d = dorsal, and h = head view.

![](top101script_files/figure-markdown_github/Image-species%20distribution-1.png)

File size distribution
======================

File size is important because it is related to the pixel dimensions of images and therefore it will have an impact on training / validation speed.

What is the mean size in kilobytes?
-----------------------------------

``` r
files_info$size2 <-
    files_info$size / 1000 # Convert bytes to kilobytes
size_kb <-
    files_info$size2 # Creating a variable containing only the file size in Kb
# summary(size_kb)
# boxplot(size_kb) 
cat('The mean size is ', mean(size_kb), 'kb') # What is the mean size?
```

    ## The mean size is  19.87619 kb

Plotting file size
------------------

File size is viewed in Kb's.

![](top101script_files/figure-markdown_github/File%20size%20-%20plotting-1.png)

Image dimensions
================

to inspect if all images are the same dimension and if they are RGB or gray-scale.

    ##  chr [1:10204] "/Users/nijram13/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/data"| __truncated__ ...

    ## Class 'magick-image' <externalptr>

    ## Error in fun(file): Unsupported file format. Please convert to jpeg/png/bmp or install image magick

    ## Warning in matrix(unlist(lst2), nrow = 10204, byrow = TRUE, ncol = 4):
    ## data length [10136] is not a sub-multiple or multiple of the number of rows
    ## [10204]

    ## 
    ## Attaching package: 'stringr'

    ## The following object is masked from 'package:imager':
    ## 
    ##     boundary

    ## Using height, width, depth, channel, names, shot_type as id variables

    ##  height          width      depth     channel  
    ##  112:10200   84     :1265   1:10200   3:10200  
    ##              83     : 588                      
    ##              77     : 317                      
    ##              79     : 281                      
    ##              73     : 277                      
    ##              76     : 262                      
    ##              (Other):7210                      
    ##                                   names        shot_type        
    ##  amblyopone_australis_casent0102125_d:    1   Length:10200      
    ##  amblyopone_australis_casent0102125_h:    1   Class :character  
    ##  amblyopone_australis_casent0102125_p:    1   Mode  :character  
    ##  amblyopone_australis_casent0102148_d:    1                     
    ##  amblyopone_australis_casent0102148_h:    1                     
    ##  amblyopone_australis_casent0102148_p:    1                     
    ##  (Other)                             :10194

    ## Using shot_type as id variables

Plotting the image dimensions
-----------------------------

![](top101script_files/figure-markdown_github/Image%20dimensions%20-%20Plotting-1.png)![](top101script_files/figure-markdown_github/Image%20dimensions%20-%20Plotting-2.png)

Image examples
--------------

    ##   format width height colorspace matte filesize
    ## 1   JPEG   112    118       sRGB FALSE    21553
    ## 2   JPEG   112     52       sRGB FALSE    11856
    ## 3   JPEG   112     58       sRGB FALSE    10240

    ## 'data.frame':    291 obs. of  4 variables:
    ##  $ catalog_number : Factor w/ 3441 levels "anic32-002152",..: 544 544 544 83 83 83 43 43 43 1118 ...
    ##  $ scientific_name: Factor w/ 97 levels "amblyopone_australis",..: 1 1 1 2 2 2 3 3 3 4 ...
    ##  $ shot_type      : Factor w/ 3 levels "dorsal","head",..: 2 3 1 2 3 1 2 3 1 2 ...
    ##  $ image_url      : chr  "http://www.antweb.org/images/casent0102125/casent0102125_h_1_low.jpg" "http://www.antweb.org/images/casent0102125/casent0102125_p_1_low.jpg" "http://www.antweb.org/images/casent0102125/casent0102125_d_1_low.jpg" "http://www.antweb.org/images/casent0005966/casent0005966_h_1_low.jpg" ...

    ## [[1]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[2]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[3]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[4]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[5]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[6]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[7]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[8]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[9]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[10]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[11]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[12]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[13]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[14]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[15]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[16]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[17]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[18]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[19]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[20]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[21]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[22]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[23]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[24]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
    ## 
    ## [[25]]
    ##    format width height colorspace matte filesize
    ## 1    JPEG   112    118       sRGB FALSE    21553
    ## 2    JPEG   112     58       sRGB FALSE    10240
    ## 3    JPEG   112     52       sRGB FALSE    11856
    ## 4    JPEG   112     95       sRGB FALSE    10695
    ## 5    JPEG   112     76       sRGB FALSE    10139
    ## 6    JPEG   112     77       sRGB FALSE     9750
    ## 7    JPEG   112     99       sRGB FALSE    15762
    ## 8    JPEG   112     84       sRGB FALSE    16154
    ## 9    JPEG   112     84       sRGB FALSE    17058
    ## 10   JPEG   112     91       sRGB FALSE    19619
    ## 11   JPEG   112     80       sRGB FALSE    18675
    ## 12   JPEG   112     74       sRGB FALSE    17959
    ## 13   JPEG   112     84       sRGB FALSE     8182
    ## 14   JPEG   112     84       sRGB FALSE     8637
    ## 15   JPEG   112     84       sRGB FALSE     8642
    ## 16   JPEG   112     93       sRGB FALSE    30927
    ## 17   JPEG   112    100       sRGB FALSE    31037
    ## 18   JPEG   112     86       sRGB FALSE    28624
    ## 19   JPEG   112     82       sRGB FALSE    36229
    ## 20   JPEG   112     75       sRGB FALSE    35097
    ## 21   JPEG   112     61       sRGB FALSE    32989
    ## 22   JPEG   112     79       sRGB FALSE     7963
    ## 23   JPEG   112     79       sRGB FALSE     8914
    ## 24   JPEG   112     82       sRGB FALSE     9321
    ## 25   JPEG   112     95       sRGB FALSE    19890
