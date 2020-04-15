import pandas as pd

# import moea.csv file from moea.py script
moea = pd.read_csv("output/moea.csv")
# convert time to datetime
moea["time"] = pd.to_datetime(moea["time"], yearfirst = True).dt.date

# import epa.csv file from epa.py script
epa = pd.read_csv("output/epa.csv")
# convert time to datetime
epa["time"] = pd.to_datetime(epa["time"], yearfirst = True).dt.date
# replace simplied chinese in city name with traditional chinese
epa["city"] = epa["city"].str.replace("台", "臺")

# import subsidy_amt.csv file from output folder
sub = pd.read_csv("output/subsidy_amt.csv")
# convert time to datetime
sub["time"] = pd.to_datetime(sub["time"], yearfirst = True).dt.date


# Organise moea
# pur
moea["新購"] = (moea["moea_app"] * 0.5).round().astype("int64")
# eli_pur
moea["汰舊換新"] = moea["moea_app"] - moea["新購"]
# eli
moea["汰舊"] = 0

# pivot or transpose the data from wide form to long form
moea_long = pd.melt(
    moea,
    id_vars = ["time", "city"],
    value_vars = ["moea_app", "新購", "汰舊換新", "汰舊"],
    var_name = "type",
    value_name = "moea_app")

# merge with epa on time, city, and type
df = pd.merge(
    left = epa,
    right = moea_long[moea_long["type"] != "moea_app"],
    on = ["time", "city", "type"],
    how = "outer",
    indicator = True)

# before
# slice data
before = (
    df[df["_merge"] == "right_only"]
    .drop(columns=["_merge"])
    .merge(sub[["time", "city", "moea_amt"]], on=["time", "city"]))


# after
# create after for entries from df that are after August 2015. Drop merging indicator and moea_app for now
after = df[df["_merge"] != "right_only"].drop(columns=["moea_app", "_merge"])

# grouped after by time, city, and type with the count of application count for eli_pur and pur
epa_ind = (after[after["type"] != "汰舊"]
    .groupby(by=["time", "city", "type"])["epa_app"].sum())

# divide each category (epa_ind) by sum, 
# reset index to be able to read groupby object
# rename column name of epa_app to epa_ratio
epa_r = (epa_ind
    .div(epa_ind.groupby(["time", "city"])
    .transform("sum"))
    .reset_index()
    .rename(columns={"epa_app": "epa_ratio"}))

# merge epa_ind and epa_r on time, city, and type to get both count and ratio
epa_m = pd.merge(
    left = epa_ind, 
    right = epa_r, 
    on = ["time", "city", "type"], 
    how = "outer")

# merge to obtain moea application count
after = epa_m.merge(
    moea[["city", "time", "moea_app"]], 
    how = "left", 
    on = ["time", "city"], 
    indicator = True)

# multiply ratio with application count
after["moea_app_alloc"] = (after["epa_ratio"] * after["moea_app"]).round()
after.loc[(after["moea_app_alloc"] > 0), "moea_app"] = after["moea_app_alloc"]
after = after.drop(
    columns = ["_merge", "epa_ratio", "moea_app_alloc"]).merge(
    sub, on = ["time", "city", "type"])

data = before.append(after).reset_index().drop(columns = "index")

# translate type and city columns from Mandarin to English
city_name = {}

with open("output/city_name.txt", "r") as f:
    for line in f:
        line = line.strip().split(",")
        city_name.update({line[0]: line[1]})

data = data.replace(city_name).replace(
    {"新購": "New Purchase", 
     "汰舊": "Elimination", 
     "汰舊換新": "Elimination and Purchase"})