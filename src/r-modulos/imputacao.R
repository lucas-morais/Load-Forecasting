library(dotenv)
library(DBI)
library(rJava)
library(RJDBC)
library(RMySQL)
library(pool)
a = load_dot_env(file = ".env")

user <- Sys.getenv("DATABASE_USER")
passwd <- Sys.getenv("DATABASE_PASSWORD")
host <- "localhost"
bd <- "Subestacoes"

mydrv <- dbDriver("MySQL")
pool <- dbPool(drv = RMySQL::MySQL(), dbname = bd, host = "localhost", username = "root", password = "632584tbj", port = 3306)
df <- dbGetQuery(pool, "SELECT * FROM JPS;")
dbListTables(pool)
str(df)
poolClose(pool)
dbListTables(pool)

