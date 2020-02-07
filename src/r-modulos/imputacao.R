setwd("~/Workspace/Github/Load-Forecasting")
library(dotenv)
library(DBI)
library(rJava)
library(RJDBC)
library(RMySQL)
library(pool)
library (dplyr)
library(ggplot2)
library (imputeTS)
library(missCompare)
library(lubridate)
library (gridExtra)
library(data.table)
a = load_dot_env(file = ".env")

user <- Sys.getenv("DATABASE_USER")
passwd <- Sys.getenv("DATABASE_PASSWORD")
host <- "localhost"
bd <- "Subestacoes"

mydrv <- dbDriver("MySQL")
pool <- dbPool(drv = RMySQL::MySQL(), dbname = bd, host = "localhost", username = "root", password = "632584tbj", port = 3306)
df <- data.table(dbGetQuery(pool, "SELECT * FROM JPS;"))
df$data <- ymd_hms(df$data)
str(df)

#Subistituindo Zeros por NA
df[df==0] <- NA

#Contando NAs por colunas
df  %>%  summarise_all(list(~sum(is.na(.))))

st <- statsNA(df$JPS_TIPO_12B1_WATT)
plotNA.gapsize(df$JPS_TIPO_12B1_WATT)
#plotNA.distribu(df$JPS_TIPO_12B1_WATT)

#p1 <- ggplot(df, aes(df$JPS_TIPO_12B1_WATT))+geom_density()
#p2 <- ggplot(df, aes(df$JPS_TIPO_12B1_WATT))+geom_density() 

grid.arrange(ggplot(df, aes(df$JPS_TIPO_12B1_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_12B2_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_11B1_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_11B2_WATT))+geom_density(),
             nrow = 2)


grid.arrange(ggplot(df, aes(df$JPS_TIPO_21L1_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_21L2_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_21L3_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_21L4_WATT))+geom_density(),
             ggplot(df, aes(df$JPS_TIPO_21L5_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_21L6_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_21L7_WATT))+geom_density(), 
             ggplot(df, aes(df$JPS_TIPO_21L8_WATT))+geom_density(),
             ggplot(df, aes(df$JPS_TIPO_21L9_WATT))+geom_density(),
             nrow = 3)

df2 <- df %>% select(c(data))
df2$imputed <- na_kalman(df$JPS_TIPO_12B1_WATT)

glimpse(df2)
grid.arrange(ggplot(df, aes(df$JPS_TIPO_12B1_WATT))+geom_density(), 
             ggplot(df2, aes(df2$imputed))+geom_density(),
             nrow = 1)
             

poolClose(pool)


dfmiss <- get_data(df %>% select(c(JPS_TIPO_12B1_WATT,JPS_TIPO_12B2_WATT)))

  dfmiss

