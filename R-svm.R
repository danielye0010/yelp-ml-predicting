library(dplyr)
library(tidyr)
library(e1071)
library(readr)

# 读取数据
df <- read_csv('burgers_business.csv')

# 根据列的数据类型填充缺失值
df <- df %>% mutate(across(where(is.character), ~ifelse(. == "TRUE", TRUE, FALSE)))
# True/False 转换为 1/0
df <- df %>% mutate(across(where(is.logical), as.integer))

# 创建success_metric列
df$success_metric <- df$stars * log(df$review_count + 1)

# 选择变量
X <- subset(df, select = -c(stars, review_count, success_metric))
y <- df$success_metric

# 划分训练和测试集
set.seed(42)
train_indices <- sample(1:nrow(df), 0.8 * nrow(df))
X_train <- X[train_indices, ]
y_train <- y[train_indices]
X_test <- X[-train_indices, ]
y_test <- y[-train_indices]

# 训练SVR模型
svr_model <- svm(y_train ~ ., data = X_train)

save(svr_model, file = 'new_svr_model.RData')

# 打印前几个预测值作为示例
print(head(predictions))

new_observation <- data.frame(
  BusinessAcceptsCreditCards = 1,  # 假设接受信用卡
  OutdoorSeating = 0,              # 没有户外座位
  RestaurantsReservations = 0,      # 不接受预订
  Caters = 1,                       # 提供餐饮服务
  RestaurantsTakeOut = 1,           # 提供外卖
  GoodForKids = 0,                  # 不适合儿童
  RestaurantsGoodForGroups = 1,     # 适合团体
  RestaurantsDelivery = 1,          # 提供送餐服务
  HasTV = 0,                        # 没有电视
  BikeParking = 1                   # 有自行车停车位
)

# 使用模型进行预测
predicted_value <- predict(svr_model, new_observation)

# 打印预测结果
print(predicted_value)
