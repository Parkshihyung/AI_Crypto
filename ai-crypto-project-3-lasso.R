library('stringr')
library('glmnet')
extract <- function(o, s) { 
index <- which(coef(o, s) != 0) 
data.frame(name=rownames(coef(o))[index], coef=coef(o, s)[index]) 
}
options(scipen=999)
args <- c("2024-05-01T000000", "2024-05-01T235900", "upbit", "BTC", "mid5")
filtered = paste(args[1], args[2], args[3], args[4], 'filtered-10-2', args[5], 
sep="-")
model_file = paste(args[2], args[3], args[4], args[5], 'lasso-10s-2std', 
sep='-')
filtered <- str_remove_all(filtered, ":")
model_file <- str_remove_all(model_file, ":")
filtered = "C:/Users/User/Downloads/HAN/2024-05-01T000000-2024-05-01T235900-
upbit-BTC-filtered-5-2-mid5.csv"
model_file = "C:/Users/User/Downloads/HAN/model_output.csv"
filtered = read.csv(filtered)
mid_std = sd(filtered$mid_price)
message(round(mid_std, 0))
filtered_no_time_mid = subset(filtered, select = -c(mid_price, timestamp))
y = filtered_no_time_mid$return
x = subset(filtered_no_time_mid, select = -c(return))
x <- as.matrix(x)
cv_fit <- cv.glmnet(x = x, y = y, alpha = 1, intercept = FALSE, lower.limits =
0, nfolds = 5)
fit <- glmnet(x = x, y = y, alpha = 1, lambda = cv_fit$lambda.1se, intercept =
FALSE, lower.limits = 0)
df <- extract(fit, s = 0.1)
df <- t(df)
write.table(df, file = model_file, sep = ",", col.names = FALSE, row.names =
FALSE, quote = FALSE)
