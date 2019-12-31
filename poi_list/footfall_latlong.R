library(RecordLinkage)
library(tidyverse)


# Read and format geolocation data.
geol <- read.csv("./poi_list/TB_GEOL_POI_DIM.csv", colClasses = "character", sep = ";")
geol <- subset(geol, LATITUDE > 0)
geol <- geol[, -c(1)]

# Read and format 2018 footfall data.
sum_footfall <- read.csv("./poi_list/sum_footfall.csv", colClasses = "character")
sum_footfall <- sum_footfall[, c(2,3)]

# Define function to identify closest match to string from string_vector.
closest_match <- function(string, string_vector) {
  distance <- levenshteinSim(string, string_vector)
  string_vector[which.max(distance)]
}

# Create and populate new df to store extracted data.
matched_df <- data.frame(matrix(ncol = 5, nrow = 0))
names(matched_df) <- c("POI", "POI_DESC", "LATITUDE", "LONGITUDE", "FOOTFALL")

# Looping through every row in footfall.
for (i in 1:dim(sum_footfall)[1]) {
  row <- cbind("POI" = sum_footfall$poi[i],
    subset(geol, POI_DESC == closest_match(sum_footfall$poi[i], geol$POI_DESC))[, c(2, 4, 5)],
    "FOOTFALL" = sum_footfall$`no.of.visitors`[i])
  
  matched_df <- rbind(matched_df, row)
}

# Use POI column as row names.
matched_df <- matched_df %>% 
  remove_rownames %>% 
  column_to_rownames(var = "POI")

# Output as csv.
write.csv(matched_df, "./poi_list/output/footfall_latlong_raw.csv")