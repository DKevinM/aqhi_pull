# scripts/fetch_aqhi.R -------------------------------------------------
# Fetch seven-day slices for every station and write individual CSVs.

source("scripts/stations.R")      # brings in `stations` tibble
source("scripts/utils_fetch.R")   # brings in fetchAndProcessWeek()

suppressPackageStartupMessages({
  library(purrr)
  library(readr)
})

dir.create("data", showWarnings = FALSE, recursive = TRUE)

purrr::walk(
  stations$StationName,
  function(stn) {
    cat("Fetching:", stn, "... ")
    dat <- fetchAndProcessWeek(stn)
    if (!is.null(dat) && nrow(dat) > 0) {
      fn <- file.path("data", paste0(gsub("[^A-Za-z0-9]", "_", stn), ".csv"))
      readr::write_csv(dat, fn, progress = FALSE)
      cat("✓ wrote", nrow(dat), "rows\n")
    } else {
      cat("no data returned\n")
    }
  }
)

# Optional combined master CSV (uncomment if you want it) -------------
 all_df <- purrr::map_dfr(stations$StationName, fetchAndProcessWeek)
 readr::write_csv(all_df, "data/all_stations.csv")
