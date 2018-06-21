``` r
setwd("~/Internships/Internship CNN 2017-2018/FormicID/stat/top101")


library(ggplot2) # for plotting
library(cowplot)
library(jpeg)
library(imager) # for reading jpg files
library(reshape2) # for using melt()
library(magick) # for image conversion because jpg files are read
library(plyr)
library(magrittr)
```

``` r
examples <- image_read("dataset_example2.png")
augmentation <- image_read("Augmentation_eciton_burchellii_casent0009221_h.png")
image1 <-  ggdraw() + draw_image(examples, scale = 0.8)
image2 <-  ggdraw() + draw_image(augmentation, scale = 1)
```

``` r
final <- plot_grid(image1, image2,labels = "AUTO", nrow=2) 
final
```

![](visualization_files/figure-markdown_github/unnamed-chunk-2-1.png)

``` r
save_plot("visualization.pdf",
          final,
          base_width = 8.27,
          base_height = 12.69)
```
