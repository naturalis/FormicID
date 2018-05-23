-   [Reading data](#reading-data)
-   [Reading CMs](#reading-cms)
-   [Plotting](#plotting)

``` r
setwd("~/Internships/Internship CNN 2017-2018/FormicID/stat/hdp")
data_dir <- file.path("shottype training")

library(ggplot2) # for plotting
library(gridExtra)
library(gtable)
library(grid)
library(reshape2)
library(magick)
library(ggpubr)
library(cowplot)
```

Reading data
------------

``` r
needed <- c("epoch", "val_acc", "val_top_k_cat_accuracy")
dorsal <-
    read.csv(
        file.path(data_dir, "dorsal", "20180518_094541_metricslog.csv"),
        header = TRUE,
        sep = ","
    )
dorsal <- dorsal[needed]
dorsal <- melt(dorsal, id = "epoch")
head <-
    read.csv(
        file.path(data_dir, "head", "20180523_084437_metricslog.csv"),
        header = TRUE,
        sep = ","
    )
head <- head[needed]
head <- melt(head, id = "epoch")
profile <-
    read.csv(
        file.path(data_dir, "profile", "20180516_094945_metricslog.csv"),
        header = TRUE,
        sep = ","
    )
profile <- profile[needed]
profile <- melt(profile, id = "epoch")
factor_rename <- factor(c("Validation accuracy","Validation top 3 accuracy"))
levels(dorsal$variable) <- factor_rename
levels(head$variable) <- factor_rename
levels(dorsal$variable) <- factor_rename
```

Reading CMs
-----------

``` r
dorsalcm <- image_read(file.path(data_dir, "dorsal", "cmdorsal.png"))
headcm <- image_read(file.path(data_dir, "head", "cmhead.png"))
profilecm <- image_read(file.path(data_dir, "profile", "cmprofile.png"))
```

``` r
maxd <- max(dorsal$epoch, na.rm = TRUE)
maxh <- max(head$epoch, na.rm = TRUE)
maxp <- max(profile$epoch, na.rm = TRUE)
maxlist <- c(maxd, maxh, maxp)
max_x <- max(maxlist)
roundUp <- function(x, to = 10) {
    to * (x %/% to + as.logical(x %% to))
}
max_x <- roundUp(max_x, to = 25)
```

Plotting
--------

``` r
dd <-
    ggplot(data = dorsal, aes(x = epoch, y = value, colour = variable)) +
    geom_line() +
    scale_x_continuous(breaks = c(0,25,50,75,100, 125), limits = c(0, max_x)) +
    scale_y_continuous(limits = c(0, 1), labels = scales::percent) +
    theme(axis.text.x  = element_text(size = 8)) +
    ylab(NULL) +
    xlab(NULL) +
    ggtitle("Dorsal") +
    theme(legend.position = "none") +
    background_grid(major = c("xy"), minor = ("xy"))
ddlegend <- dd +
    theme(legend.position = "right",
          legend.title = element_blank())


hh <-
    ggplot(data = head, aes(x = epoch, y = value, colour = variable)) +
    geom_line() +
    scale_x_continuous(breaks = c(0,25,50,75,100, 125), limits = c(0, max_x)) +
    scale_y_continuous(limits = c(0, 1), labels = scales::percent) +
    theme(axis.text.x  = element_text(size = 8)) +
    ylab(NULL) +
    xlab(NULL) +
    ggtitle("Head") +
    theme(legend.position = "none") +
    background_grid(major = c("xy"), minor = ("xy"))
pp <-
    ggplot(data = profile, aes(x = epoch, y = value, colour = variable)) +
    geom_line() +
    scale_x_continuous(breaks = c(0,25,50,75,100, 125), limits = c(0, max_x)) +
    scale_y_continuous(limits = c(0, 1), labels = scales::percent) +
    theme(axis.text.x  = element_text(size = 8)) +
    ylab(NULL) +
    xlab(NULL) +
    ggtitle("Profile") +
    theme(legend.position = "none") +
    background_grid(major = c("xy"), minor = ("xy"))
```

``` r
# legend = gtable_filter(ggplotGrob(dd), "guide-box")
# 
# grid.arrange(
#     arrangeGrob(
#         dd + theme(legend.position = "none"),
#         dorsalcm,
#         hh + theme(legend.position = "none"),
#         headcm,
#         pp + theme(legend.position = "none"),
#         profilecm,
#         nrow = 3,
#         top = textGrob(
#             "Validation accuracy",
#             vjust = 1,
#             gp = gpar(fontface = "bold", cex = 1.5)
#         ),
#         left = textGrob("Accuracy (%)", rot = 90, vjust = 1),
#         bottom = textGrob("Epochs", vjust = 1)
#     ),
#     legend,
#     widths = unit.c(unit(1, "npc") - legend$width, legend$width),
#     nrow = 1
# )
```

``` r
# dorsalcm <- rasterGrob(dorsalcm)
# headcm <- rasterGrob(headcm)
# profilecm <- rasterGrob(profilecm)
# 
# p1 <- ggarrange(
#     dd,
#     hh,
#     pp,
#     labels = c("A","B", "C"),
#     common.legend = TRUE,
#     legend = "bottom",
#     align = "v",
#     ncol = 1,
#     nrow = 3
# )
# 
# p2 <- ggarrange(
#     dorsalcm,
#     headcm,
#     profilecm,
#     labels = c("D", "E", "F"),
#     align = "v",
#     ncol = 1,
#     nrow = 3
# )
# ggarrange(p1, p2, align="v", ncol = 2, nrow = 1)
```

``` r
ggdorsal <- ggdraw() + draw_image(dorsalcm, scale = 1)
gghead <- ggdraw() + draw_image(headcm, scale = 1)
ggprofile <- ggdraw() + draw_image(profilecm, scale = 1)
legend <- get_legend(ddlegend)
legend_bottom <- plot_grid(legend, ncol = 2)

graphs <- plot_grid(
    dd,
    ggdorsal,
    hh,
    gghead,
    pp,
    ggprofile,
    ncol = 2,
    nrow = 3,
    labels = "AUTO"
)

plot_grid(
    graphs,
    legend_bottom,
    ncol=1,
    nrow=2,
    rel_heights = c(1,.05)
)
```

![](HDP_experiments_files/figure-markdown_github/unnamed-chunk-4-1.png)
