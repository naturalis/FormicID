-   [Loading data](#loading-data)
-   [Function: getting equation](#function-getting-equation)
    -   [Equation](#equation)
-   [F1 Score](#f1-score)
-   [Plotting](#plotting)

``` r
setwd("~/Internships/Internship CNN 2017-2018/FormicID/stat/hdp")


library(ggplot2) # for plotting
library(cowplot)
library(jpeg)
library(imager) # for reading jpg files
library(reshape2) # for using melt()
library(magick) # for image conversion because jpg files are read
library(plyr)
library(magrittr)
```

Loading data
============

``` r
sp_complex <-
    read.csv("speciescomplexexport.csv", sep=";")
```

Function: getting equation
==========================

``` r
lm_eqn = function(df) {
    m = lm(y ~ x, df)
    eq <- substitute(
        italic(y) == a + b %.% italic(x) * ","
        ~~ italic(r) ^ 2 ~ "=" ~ r2,
        list(
            a = format(coef(m)[1], digits = 2),
            b = format(coef(m)[2], digits = 2),
            r2 = format(summary(m)$r.squared, digits = 3)
        )
    )
    as.character(as.expression(eq))
}
```

Equation
--------

``` r
eq <- ddply(sp_complex,.(Shottypes),lm_eqn)
```

F1 Score
========

F1 Score is needed when you want to seek a balance between Precision and Recall. Right…so what is the difference between F1 Score and Accuracy then? We have previously seen that accuracy can be largely contributed by a large number of True Negatives which in most business circumstances, we do not focus on much whereas False Negative and False Positive usually has business costs (tangible & intangible) thus F1 Score might be a better measure to use if we need to seek a balance between Precision and Recall AND there is an uneven class distribution (large number of Actual Negatives).

Plotting
========

``` r
sp_complex_plot <-
    ggplot(sp_complex, aes(x = x,
                           y = y,
                           col = Shottypes)) +
    geom_point() +
    geom_smooth(method = "lm",
                se = FALSE,
                formula = y ~ x) +
    geom_text(
        data = eq,
        aes(x = 10, y = 0.15, label = V1),
        parse = T,
        inherit.aes = FALSE
    ) +
    facet_grid(~ Shottypes, scales = "free_x", space = "free_x") +
    ggtitle("Species complexity vs F1-score") +
    xlab("Number of species in complex") +
    ylab("F1-score") +
    theme(legend.position = "none")

sp_complex_plot
```

![](sp_complexity_files/figure-markdown_github/unnamed-chunk-4-1.png)