library(dplyr)
library(e1071)
library(readr)
library(tidyr)

# Load prepared burger-business data
df <- read_csv("burgers_business.csv", show_col_types = FALSE)

# Normalize logical-style attributes and missing values
df <- df %>%
  mutate(across(where(is.character), ~ case_when(
    toupper(.) == "TRUE" ~ "1",
    toupper(.) == "FALSE" ~ "0",
    TRUE ~ .
  ))) %>%
  mutate(across(-c(stars, review_count), ~ as.numeric(.))) %>%
  mutate(across(everything(), ~ replace_na(., 0)))

# Success metric combines rating quality and review volume
df$success_metric <- df$stars * log(df$review_count + 1)

X <- subset(df, select = -c(stars, review_count, success_metric))
y <- df$success_metric

set.seed(42)
train_indices <- sample(seq_len(nrow(df)), 0.8 * nrow(df))
X_train <- X[train_indices, ]
y_train <- y[train_indices]
X_test <- X[-train_indices, ]
y_test <- y[-train_indices]

train_data <- X_train
train_data$success_metric <- y_train
svr_model <- svm(success_metric ~ ., data = train_data)

predictions <- predict(svr_model, X_test)
print(head(predictions))

mse <- mean((predictions - y_test)^2)
r2 <- 1 - sum((predictions - y_test)^2) / sum((y_test - mean(y_test))^2)
cat(sprintf("Test MSE: %.4f\n", mse))
cat(sprintf("Test R2: %.4f\n", r2))

save(svr_model, file = "new_svr_model.RData")

# Example restaurant attribute profile
new_observation <- data.frame(
  BusinessAcceptsCreditCards = 1,
  OutdoorSeating = 0,
  RestaurantsReservations = 0,
  Caters = 1,
  RestaurantsTakeOut = 1,
  GoodForKids = 0,
  RestaurantsGoodForGroups = 1,
  RestaurantsDelivery = 1,
  HasTV = 0,
  BikeParking = 1
)

predicted_value <- predict(svr_model, new_observation)
print(predicted_value)
