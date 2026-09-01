library(dplyr)
library(plm)
options(scipen = 999)

###Table1
data <- read.csv("~/G_ripple_data27.csv")
View(data)
data$discipline <- factor(data$discipline)
data$genderLabel <- factor(data$genderLabel) 
data$genderLabel <- relevel(data$genderLabel, ref = "female") #female = 0
data <- data %>% mutate(high_prestige = ifelse(pv_group == "High", 1, 0))


lm1<-lm(delta_C_ITE ~ group+ high_prestige + delta_T+ genderLabel+ award_age + award_year+ discipline, data = data)
summary(lm1)
lm2 <- lm(delta_C_ITE ~ group+ high_prestige + award_year+ discipline, data = data)
summary(lm2)
lm3 <- lm(delta_C_ITE ~ group+ high_prestige + group*high_prestige + award_year+ discipline, data = data)
summary(lm3)
lm4 <- lm(delta_C_ITE ~ group+ delta_T+ award_year+ discipline, data = data)
summary(lm4)
lm5 <- lm(delta_C_ITE ~ group+ delta_T+ group*delta_T+ award_year+ discipline, data = data)
summary(lm5)
lm6 <- lm(delta_C_ITE ~ group+ genderLabel+ award_year+ discipline, data = data)
summary(lm6)
lm7 <- lm(delta_C_ITE ~ group+ genderLabel+ group*genderLabel+ award_year+ discipline, data = data)
summary(lm7)
lm8 <- lm(delta_C_ITE ~ group+ award_age + award_year+ discipline, data = data)
summary(lm8)
lm9 <- lm(delta_C_ITE ~ group+ award_age+ group*award_age+ award_year+ discipline, data = data)
summary(lm9)


##Table2 
data1 <- read.csv("~/G_ripple_data28.csv")
View(data1)
data1 <- data1 %>% filter(complete.cases(.))

lm1 <- lm(delta_C_coathor ~ similarity + delta_C_winner +high_prestige+ genderLabel+ award_age+award_year, data = data1)
summary(lm1)
lm2 <- lm(delta_C_coathor ~ strength + delta_C_winner +high_prestige+  genderLabel+ award_age+ award_year, data = data1)
summary(lm2)
lm3 <- lm(delta_C_coathor ~ similarity + strength + delta_C_winner +high_prestige+ genderLabel+ award_age +award_year, data = data1)
summary(lm3)
