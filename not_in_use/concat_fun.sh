awk '(NR == 1) || (FNR > 1)' ~/projects/pict_b/stocks_fundamentals/*.csv > ~/projects/pict_b/fun_concatenations/concat_fun_all.csv
