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
setwd("~/Internships/Internship CNN 2017-2018/FormicID/stat/top101")


library(ggplot2) # for plotting
library(cowplot)
library(jpeg)
library(imager) # for reading jpg files
library(reshape2) # for using melt()
library(magick) # for image conversion because jpg files are read
library(plyr)

data_dir <- # Setting the directory that contains all the images
    "~/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean"

top101 <-
    read.csv(file.path(data_dir, 'image_urls.csv')) # spreadsheat containing catalognumber, scientific name,
# shot_type and image url
```

Dataset
=======

``` r
head(top101)
```

    ##   catalog_number      scientific_name shot_type
    ## 1  casent0102125 amblyopone_australis         h
    ## 2  casent0102125 amblyopone_australis         p
    ## 3  casent0102125 amblyopone_australis         d
    ## 4  casent0102148 amblyopone_australis         h
    ## 5  casent0102148 amblyopone_australis         p
    ## 6  casent0102148 amblyopone_australis         d
    ##                                                              image_url
    ## 1 http://www.antweb.org/images/casent0102125/casent0102125_h_1_med.jpg
    ## 2 http://www.antweb.org/images/casent0102125/casent0102125_p_1_med.jpg
    ## 3 http://www.antweb.org/images/casent0102125/casent0102125_d_1_med.jpg
    ## 4 http://www.antweb.org/images/casent0102148/casent0102148_h_1_med.jpg
    ## 5 http://www.antweb.org/images/casent0102148/casent0102148_p_1_med.jpg
    ## 6 http://www.antweb.org/images/casent0102148/casent0102148_d_1_med.jpg

``` r
summary(top101)
```

    ##        catalog_number                   scientific_name shot_type
    ##  anic32-002152:    3   camponotus_maculatus     : 671   d:3405   
    ##  anic32-002153:    3   pheidole_megacephala     : 377   h:3385   
    ##  anic32-002156:    3   tetramorium_sericeiventre: 210   p:3421   
    ##  anic32-063120:    3   hypoponera_punctatissima : 190            
    ##  antweb1008080:    3   dorylus_nigricans        : 183            
    ##  antweb1008081:    3   solenopsis_geminata      : 160            
    ##  (Other)      :10193   (Other)                  :8420            
    ##                                                                 image_url    
    ##  http://www.antweb.org/images/anic32-002152/anic32-002152_d_1_med.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002152/anic32-002152_h_1_med.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002152/anic32-002152_p_1_med.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002153/anic32-002153_d_1_med.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002153/anic32-002153_h_1_med.jpg:    1  
    ##  http://www.antweb.org/images/anic32-002153/anic32-002153_p_1_med.jpg:    1  
    ##  (Other)                                                             :10205

``` r
str(top101)
```

    ## 'data.frame':    10211 obs. of  4 variables:
    ##  $ catalog_number : Factor w/ 3437 levels "anic32-002152",..: 535 535 535 538 538 538 543 543 543 586 ...
    ##  $ scientific_name: Factor w/ 97 levels "amblyopone_australis",..: 1 1 1 1 1 1 1 1 1 1 ...
    ##  $ shot_type      : Factor w/ 3 levels "d","h","p": 2 3 1 2 3 1 2 3 1 2 ...
    ##  $ image_url      : Factor w/ 10211 levels "http://www.antweb.org/images/anic32-002152/anic32-002152_d_1_med.jpg",..: 1586 1587 1585 1595 1596 1594 1610 1611 1609 1738 ...

``` r
species <- data.frame(count(top101$scientific_name))
species[order(species[, 2], decreasing = T),]
```

    ##                             x freq
    ## 14       camponotus_maculatus  671
    ## 64       pheidole_megacephala  377
    ## 92  tetramorium_sericeiventre  210
    ## 39   hypoponera_punctatissima  190
    ## 36          dorylus_nigricans  183
    ## 80        solenopsis_geminata  160
    ## 33           diacamma_rugosum  157
    ## 93     tetramorium_simillimum  154
    ## 63            pheidole_indica  153
    ## 68         pheidole_pallidula  133
    ## 69             pheidole_parva  133
    ## 30  crematogaster_ranavalonae  129
    ## 61           pheidole_fervens  129
    ## 49          mystrium_camillae  125
    ## 21       cardiocondyla_emeryi  123
    ## 57   paratrechina_longicornis  122
    ## 2   anochetus_madagascarensis  117
    ## 3   aphaenogaster_swammerdami  114
    ## 46       monomorium_floricola  114
    ## 86      technomyrmex_pallipes  114
    ## 91    tetramorium_lanuginosum  114
    ## 34             dorylus_fulvus  113
    ## 13        camponotus_irritans  112
    ## 74        pheidole_variabilis  111
    ## 20      camponotus_variegatus  109
    ## 72       pheidole_sculpturata  108
    ## 84    tapinoma_melanocephalum  108
    ## 16     camponotus_punctulatus  107
    ## 11     camponotus_grandidieri  105
    ## 25     crematogaster_castanea  105
    ## 38     gnamptogenys_striatula  105
    ## 65         pheidole_mooreorum  105
    ## 45         monomorium_exiguum  104
    ## 62           pheidole_flavens  104
    ## 7         camponotus_atriceps  103
    ## 17 camponotus_quadrimaculatus  102
    ## 43         lepisiota_capensis  102
    ## 5       bothroponera_cambouei  101
    ## 96     wasmannia_auropunctata  101
    ## 35              dorylus_kohli   99
    ## 66             pheidole_nodus   99
    ## 75      platythyrea_parallela   99
    ## 89    tetramorium_bicarinatum   98
    ## 52            mystrium_rogeri   96
    ## 94    trichomyrmex_destructor   95
    ## 31  crematogaster_rasoherinae   94
    ## 82     strumigenys_louisianae   93
    ## 6   brachyponera_sennaarensis   92
    ## 54      nylanderia_bourbonica   92
    ## 44        leptogenys_diminuta   91
    ## 81          strumigenys_emmae   91
    ## 27      crematogaster_dentata   90
    ## 70        pheidole_punctulata   88
    ## 1        amblyopone_australis   87
    ## 58        pheidole_aurivillii   87
    ## 23       cataulacus_intrudens   84
    ## 71     pheidole_radoszkowskii   84
    ## 79           solenopsis_fugax   84
    ## 85       technomyrmex_albipes   84
    ## 90      tetramorium_caespitum   84
    ## 26      crematogaster_crinosa   82
    ## 8       camponotus_auropubens   81
    ## 32  crematogaster_stadelmanni   81
    ## 51          mystrium_mysticum   81
    ## 56          ochetellus_glaber   81
    ## 53      nomamyrmex_esenbeckii   80
    ## 78        pseudoponera_stigma   78
    ## 88      tetramorium_aculeatum   78
    ## 42             labidus_coecus   77
    ## 19          camponotus_thraso   75
    ## 29      crematogaster_kelleri   75
    ## 67          pheidole_oceanica   75
    ## 73          pheidole_susannae   75
    ## 83         strumigenys_rogeri   75
    ## 95        vollenhovia_oblonga   75
    ## 48     monomorium_termitobium   74
    ## 24          colobopsis_vitrea   72
    ## 28 crematogaster_gerstaeckeri   72
    ## 37          eciton_burchellii   72
    ## 60            pheidole_caffra   72
    ## 76          polyrhachis_dives   71
    ## 47       monomorium_subopacum   70
    ## 59      pheidole_biconstricta   70
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
    ## 9      camponotus_bonariensis   66
    ## 12            camponotus_hova   65
    ## 18     camponotus_rufoglaucus   59
    ## 10         camponotus_christi   54

``` r
levels(top101$shot_type)[levels(top101$shot_type) == 'd'] <- 'Dorsal'
levels(top101$shot_type)[levels(top101$shot_type) == 'h'] <- 'Head'
levels(top101$shot_type)[levels(top101$shot_type) == 'p'] <- 'Profile'

# https://stackoverflow.com/questions/8186436/order-stacked-bar-graph-in-ggplot
top101_transp <- read.csv(file.path(data_dir, 'image_urls_transp.csv'), sep = ';')
top101_transp$total <- NULL # remove total
capitalize <- function(x) {
    first <- toupper(substr(x, start = 1, stop = 1))
    rest <- tolower(substr(x, start = 2, stop = nchar(x)))
    paste0(first, rest)
}
levels(top101_transp$scientific_name) <-
    capitalize(levels(top101_transp$scientific_name))
top101_transp[1] <- sapply(
        top101_transp[1],
        gsub,
        pattern = "_",
        replacement = " "
    )
top101_transp$scientific_name <-
    reorder(top101_transp$scientific_name, rowSums(top101_transp[2:4])) # reorder based on a non-created total
melted <-
    melt(top101_transp, id = 'scientific_name') # melt based on scientific_name
levels(melted$variable)[levels(melted$variable) == 'dorsal'] <- 'Dorsal'
levels(melted$variable)[levels(melted$variable) == 'head'] <- 'Head'
levels(melted$variable)[levels(melted$variable) == 'profile'] <- 'Profile'

shotcount <- data.frame(Dorsal = sapply(melted[,-1], function(x){sum(melted$value[x == 'Dorsal'])}), 
           Head = sapply(melted[,-1], function(x){sum(melted$value[x == 'Head'])}),
           Profile = sapply(melted[,-1], function(x){sum(melted$value[x == 'Profile'])}))
shotcount <- melt(shotcount[(1),])
```

    ## No id variables; using all as measure variables

Shot type plot
--------------

Image distribution per species
==============================

Here we can see how images are distributed per species. Within species there are 3 different shot types. p = profile, d = dorsal, and h = head view.

![](top101script_files/figure-markdown_github/Image-species%20distribution-1.png)

File size distribution
======================

File size is important because it is related to the pixel dimensions of images and therefore it will have an impact on training / validation speed.

    ##                                                                                                                                                                                                                         size
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102125_d.jpg 23934
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102184_d.jpg 15392
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102519_d.jpg 11448
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104575_d.jpg 30954
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104578_d.jpg 28422
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0172212_d.jpg 36524
    ##                                                                                                                                                                                                                        isdir
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102125_d.jpg FALSE
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102184_d.jpg FALSE
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102519_d.jpg FALSE
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104575_d.jpg FALSE
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104578_d.jpg FALSE
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0172212_d.jpg FALSE
    ##                                                                                                                                                                                                                        mode
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102125_d.jpg  666
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102184_d.jpg  666
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102519_d.jpg  666
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104575_d.jpg  666
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104578_d.jpg  666
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0172212_d.jpg  666
    ##                                                                                                                                                                                                                                      mtime
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102125_d.jpg 2018-05-15 10:44:14
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102184_d.jpg 2018-05-15 10:44:18
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102519_d.jpg 2018-05-15 10:44:18
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104575_d.jpg 2018-05-15 10:44:22
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104578_d.jpg 2018-05-15 10:44:26
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0172212_d.jpg 2018-05-15 10:44:30
    ##                                                                                                                                                                                                                                      ctime
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102125_d.jpg 2018-05-30 10:29:06
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102184_d.jpg 2018-05-30 10:29:06
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102519_d.jpg 2018-05-30 10:29:06
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104575_d.jpg 2018-05-30 10:29:06
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104578_d.jpg 2018-05-30 10:29:06
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0172212_d.jpg 2018-05-30 10:29:06
    ##                                                                                                                                                                                                                                      atime
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102125_d.jpg 2018-05-30 14:28:28
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102184_d.jpg 2018-05-30 14:20:40
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102519_d.jpg 2018-05-30 14:28:35
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104575_d.jpg 2018-05-30 14:28:35
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104578_d.jpg 2018-05-30 14:28:35
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0172212_d.jpg 2018-05-30 14:28:35
    ##                                                                                                                                                                                                                        exe
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102125_d.jpg  no
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102184_d.jpg  no
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0102519_d.jpg  no
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104575_d.jpg  no
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0104578_d.jpg  no
    ## //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/amblyopone_australis/amblyopone_australis_casent0172212_d.jpg  no

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

    ## The mean size is  28.62278 kb

Plotting file size
------------------

File size is viewed in Kb's.

![](top101script_files/figure-markdown_github/File%20size%20-%20plotting-1.png)

Image dimensions
================

to inspect if all images are the same dimension and if they are RGB or gray-scale.

    ##  chr [1:10118] "//fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97specie"| __truncated__ ...

    ## Class 'magick-image' <externalptr>

    ## 
    ## Attaching package: 'stringr'

    ## The following object is masked from 'package:imager':
    ## 
    ##     boundary

    ## Using height, width, depth, channel, names, shot_type as id variables

    ##  height          width      depth     channel  
    ##  233:10118   175    : 795   1:10118   3:10118  
    ##              173    : 405                      
    ##              174    : 291                      
    ##              160    : 150                      
    ##              164    : 137                      
    ##              166    : 136                      
    ##              (Other):8204                      
    ##                                                                                                                                                                                                                           names      
    ##  //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/anochetus_madagascarensis/anochetus_madagascarensis_casent0005966_d:    1  
    ##  //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/anochetus_madagascarensis/anochetus_madagascarensis_casent0049282_d:    1  
    ##  //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/anochetus_madagascarensis/anochetus_madagascarensis_casent0101651_d:    1  
    ##  //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/anochetus_madagascarensis/anochetus_madagascarensis_casent0101663_d:    1  
    ##  //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/anochetus_madagascarensis/anochetus_madagascarensis_casent0101674_d:    1  
    ##  //fs-smb-019.ad.naturalis.nl/homedir/Marijn.Boer/Internships/Internship CNN 2017-2018/FormicID/data/top97species_Qmed_def_clean/images/dorsal/1-training/anochetus_madagascarensis/anochetus_madagascarensis_casent0101712_d:    1  
    ##  (Other)                                                                                                                                                                                                                     :10112  
    ##   shot_type        
    ##  Length:10118      
    ##  Class :character  
    ##  Mode  :character  
    ##                    
    ##                    
    ##                    
    ## 

    ## Using shot_type as id variables

Plotting the image dimensions
-----------------------------

    ## Warning: Removed 10838 rows containing non-finite values (stat_boxplot).

![](top101script_files/figure-markdown_github/Image%20dimensions%20-%20Plotting-1.png)

    ## $breaks
    ##  [1]  50  60  70  80  90 100 110 120 130 140 150 160 170 180 190 200 210
    ## [18] 220 230 240 250 260 270 280 290 300 310 320 330 340 350 360 370 380
    ## [35] 390 400 410 420 430
    ## 
    ## $counts
    ##  [1]    1   10   19   34   74  144  247  354  613  820 1105 1274 2200  816
    ## [15]  635  506  390  287  226  117   68   50   37   19   17   13   14    5
    ## [29]    6    7    5    3    1    0    0    0    0    1
    ## 
    ## $density
    ##  [1] 9.883376e-06 9.883376e-05 1.877841e-04 3.360348e-04 7.313698e-04
    ##  [6] 1.423206e-03 2.441194e-03 3.498715e-03 6.058510e-03 8.104368e-03
    ## [11] 1.092113e-02 1.259142e-02 2.174343e-02 8.064835e-03 6.275944e-03
    ## [16] 5.000988e-03 3.854517e-03 2.836529e-03 2.233643e-03 1.156355e-03
    ## [21] 6.720696e-04 4.941688e-04 3.656849e-04 1.877841e-04 1.680174e-04
    ## [26] 1.284839e-04 1.383673e-04 4.941688e-05 5.930026e-05 6.918363e-05
    ## [31] 4.941688e-05 2.965013e-05 9.883376e-06 0.000000e+00 0.000000e+00
    ## [36] 0.000000e+00 0.000000e+00 9.883376e-06
    ## 
    ## $mids
    ##  [1]  55  65  75  85  95 105 115 125 135 145 155 165 175 185 195 205 215
    ## [18] 225 235 245 255 265 275 285 295 305 315 325 335 345 355 365 375 385
    ## [35] 395 405 415 425
    ## 
    ## $xname
    ## [1] "df_good$width"
    ## 
    ## $equidist
    ## [1] TRUE
    ## 
    ## attr(,"class")
    ## [1] "histogram"

![](top101script_files/figure-markdown_github/Image%20dimensions%20-%20Plotting-2.png)

Image examples
--------------
