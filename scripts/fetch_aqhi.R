# scripts/fetch_aqhi.R -----------------------------------------------
source("scripts/stations.R")
source("scripts/utils_fetch.R")

suppressPackageStartupMessages({
  library(purrr)
  library(readr)
  library(fs)  # for path and dir_create
})

# Create subfolders by zone
unique_zones <- unique(stations$zone)
walk(unique_zones, ~ dir_create(path("data", .x)))

walk(seq_len(nrow(stations)), function(i) {
  stn <- stations$StationName[i]
  zone <- stations$zone[i]

  cat("Fetching:", stn, "in", zone, "... ")
  dat <- fetchAndProcessWeek(stn)

  if (!is.null(dat) && nrow(dat) > 0) {
    file_name <- paste0(gsub("[^A-Za-z0-9]", "_", stn), ".csv")
    file_path <- path("data", zone, file_name)
    write_csv(dat, file_path, progress = FALSE)
    cat("✓ wrote", nrow(dat), "rows to", file_path, "\n")
  } else {
    cat("no data returned\n")
  }
})

# Optional combined master CSV (uncomment if you want it) -------------
 all_df <- purrr::map_dfr(stations$StationName, fetchAndProcessWeek)
 readr::write_csv(all_df, "data/all_stations.csv")
