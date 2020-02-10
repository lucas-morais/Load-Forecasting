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
library(forecast)

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

statsNA(df$JPS_TIPO_12B1_WATT)
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

df2 <- df %>% select(c(data, JPS_TIPO_12B1_WATT))
auto.arima(df2$JPS_TIPO_12B1_WATT)

df2$imputed <- na_ma(df$JPS_TIPO_12B1_WATT, k = 4*24*7*30, weighting = "exponential")


df2$imputed <- na_kalman(df$JPS_TIPO_12B1_WATT, model = "auto.arima")

glimpse(df2)
grid.arrange(ggplot(df2, aes(df$JPS_TIPO_12B1_WATT))+geom_density(), 
             ggplot(df2, aes(df2$imputed))+geom_density(),
             nrow = 1)

mes_ini = "2009-12-31"
mes_fim ="2010-02-01"
df210 <- df2 %>% filter(data >mes_ini & data <mes_fim)           
statsNA(df210$JPS_TIPO_12B1_WATT)
plotNA.distribution(df210$JPS_TIPO_12B1_WATT)
plotNA.imputations(df210$JPS_TIPO_12B1_WATT ,
                   df210$imputed)
a = auto.arima(df210$JPS_TIPO_12B1_WATT)


df210$imputed <- na_ma(df210$JPS_TIPO_12B1_WATT, k = 4*24, weighting = "exponential")
df210$imputed <- na_kalman(df210$JPS_TIPO_12B1_WATT, model="auto.arima")


mes_ini = "2010-02-28"
mes_fim ="2010-04-01"
df211 <- df2 %>% filter(data >mes_ini & data <mes_fim)           
statsNA(df211$JPS_TIPO_12B1_WATT)
plotNA.distribution(df211$JPS_TIPO_12B1_WATT)

model_ini = "2009-12-31"
model_fim ="2010-04-01"
df2model <- df2 %>% filter(data >mes_ini & data <mes_fim)           
modelo1 = auto.arima(df2model$JPS_TIPO_12B1_WATT)
modelo2 = arima(df211$JPS_TIPO_12B1_WATT, c(2,1,3))

#df211$imputed <- na_ma(df211$JPS_TIPO_12B1_WATT, k = 4, weighting = "exponential")
df211$imputed <- na_kalman(df211$JPS_TIPO_12B1_WATT, model=modelo2$model)

plotNA.imputations(df211$JPS_TIPO_12B1_WATT, df211$imputed)



#misscompare

dfmiss <- clean(df)


str(dfmiss)
miss <- get_data(dfmiss)
miss$Complete_cases
miss$Rows
miss$Corr_matrix
miss$Fraction_missingness
miss$Fraction_missingness_per_variable
miss$MD_Pattern
miss$NA_Correlation_plot
simulated <- simulate(rownum = miss$Rows,
                      colnum = miss$Columns,
                      cormat = miss$Corr_matrix,
                      meanval = 0,
                      sdval = 1)

missCompare::impute_simulated(rownum = miss$Rows,
                              colnum = miss$Columns, 
                              cormat = miss$Corr_matrix,
                              MD_pattern = miss$MD_Pattern,
                              NA_fraction = miss$Fraction_missingness,
                              min_PDM = 10,
                              n.iter = 50, 
                              assumed_pattern = NA)
str(miss)
dfmiss <- get_data(df %>% select(c(JPS_TIPO_12B1_WATT,JPS_TIPO_12B2_WATT)))
dfmiss


poolClose(pool)


