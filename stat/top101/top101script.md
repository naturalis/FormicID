-   [Dataset](#dataset)
    -   [Shot type plot](#shot-type-plot)
-   [Image distribution per species](#image-distribution-per-species)
-   [File size distribution](#file-size-distribution)
    -   [Plotting file size](#plotting-file-size)
-   [Image dimensions](#image-dimensions)
    -   [Plotting the image dimensions](#plotting-the-image-dimensions)

``` r
setwd(
    "~/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/stat/top101"
)

library(ggplot2) # for plotting
library(jpeg)
library(imager) # for reading jpg files
library(reshape2) # for using melt()
library(magick) # for image conversion because jpg files are read

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

Shot type plot
--------------

![](top101script_files/figure-markdown_github/Shot%20type%20plot-1.png)

Image distribution per species
==============================

Here we can see how images are distributed per species. Within species there are 3 different shot types. p = profile, d = dorsal, and h = head view.

![](top101script_files/figure-markdown_github/Image%20distribution-1.png)

File size distribution
======================

File size is important because it is related to the pixel dimensions of images and therefore it will have an impact on training / validation speed.

``` r
data_dir <- # Setting the directory that contains all the images
    "~/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/data/2018-01-17_top101-images"

files_info <- # Reading all the images in the directory
    file.info(list.files(
        path = data_dir,
        pattern = ".jpg",
        full.names = TRUE
    ))
# head(files_info)

files_info$size2 <-
    files_info$size / 1000 # Convert bytes to kilobytes
size_kb <-
    files_info$size2 # creating a variable containing only the file size in Kb
cat('The mean size is ', mean(size_kb), 'kb') # What is the mean size?
```

    ## The mean size is  19.87619 kb

``` r
# summary(size_kb)
# boxplot(size_kb) 
```

Plotting file size
------------------

File sizes is viewed in Kb's.

![](top101script_files/figure-markdown_github/File%20size%20-%20plotting-1.png)![](top101script_files/figure-markdown_github/File%20size%20-%20plotting-2.png)

Image dimensions
================

to inspect if all images are the same dimension and if they are RGB or gray-scale.

``` r
# Reading all images paths in to a 'list'
images <-
    list.files(path = data_dir,
               pattern = ".jpg",
               full.names = TRUE)
str(images)
```

    ##  chr [1:10204] "/Users/nijram13/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/data"| __truncated__ ...

``` r
x <- image_read(images[1])
str(x)
```

    ## Class 'magick-image' <externalptr>

``` r
# Creates an empty list to be filled in the next function
lst2 <- c()

# Returns dimensions, depth, and channels for the images
for (image in images) {
    # This function creates an error, but it works.
    x <- load.image(image)
    x <- dim(x)
    x <- as.numeric(unlist(x))
    lst2 <- c(lst2, x)
}
```

    ## Error in fun(file): Unsupported file format. Please convert to jpeg/png/bmp or install image magick

``` r
# Converting to a Dataframe and get rid of images without 3 channels (RGB)
df <-
    data.frame(matrix(
        unlist(lst2),
        nrow = 10204,
        byrow = TRUE,
        ncol = 4
    ))
```

    ## Warning in matrix(unlist(lst2), nrow = 10204, byrow = TRUE, ncol = 4):
    ## data length [10136] is not a sub-multiple or multiple of the number of rows
    ## [10204]

``` r
# Changing columnnames and rownames
colnames(df) <- c('hight', 'width', 'depth', 'channel')
rownames(df) <- images

# Removing grayscale images to a different dataframe
df_channel_wrong <- subset(df, channel <= 2)
df_good <- subset(df, channel > 2)
df_good_melt <- melt(df_good[1:2])
```

    ## No id variables; using all as measure variables

``` r
summary(df_good_melt)
```

    ##   variable         value      
    ##  hight:10200   Min.   : 34.0  
    ##  width:10200   1st Qu.: 83.0  
    ##                Median :112.0  
    ##                Mean   : 98.1  
    ##                3rd Qu.:112.0  
    ##                Max.   :206.0

Plotting the image dimensions
-----------------------------

![](top101script_files/figure-markdown_github/Image%20dimensions%20-%20Plotting-1.png)![](top101script_files/figure-markdown_github/Image%20dimensions%20-%20Plotting-2.png)
