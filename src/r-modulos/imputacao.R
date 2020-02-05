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
a = load_dot_env(file = ".env")

user <- Sys.getenv("DATABASE_USER")
passwd <- Sys.getenv("DATABASE_PASSWORD")
host <- "localhost"
bd <- "Subestacoes"

mydrv <- dbDriver("MySQL")
pool <- dbPool(drv = RMySQL::MySQL(), dbname = bd, host = "localhost", username = "root", password = "632584tbj", port = 3306)
df <- dbGetQuery(pool, "SELECT * FROM JPS;")

str(df)

#Subistituindo Zeros por NA
df[df==0] <- NA

#Contando NAs por colunas
df  %>%  summarise_all(list(~sum(is.na(.))))

st <- statsNA(df$JPS_TIPO_12B1_WATT)
plotNA.gapsize(df$JPS_TIPO_12B1_WATT)
plotNA.distribu(df$JPS_TIPO_12B1_WATT)
poolClose(pool)


