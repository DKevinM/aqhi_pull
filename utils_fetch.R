
# Function to fetch and process data for 4 days for a station
fetchAndProcessWeek <- function(stationName) {  
  base_url <- "https://data.environment.alberta.ca/EdwServices/aqhi/odata/StationMeasurements?$format=json"
  
  # Get the current date and time
  current_datetime <- as.POSIXct(Sys.time(), tz = "America/Edmonton")
  
  # Calculate the datetime 4 days ago
  datetime_7days_ago <- current_datetime - days(7)  # 7 days ago
  
  
  # Format it in the required format: "YYYY-MM-DDTHH:MM:SS-06:00"
  formatted_datetime_7days_ago <- format(datetime_7days_ago, "%Y-%m-%dT%H:%M:%S%z")
  formatted_datetime_7days_ago <- sub("(\\d{2})(\\d{2})$", "\\1:\\2", formatted_datetime_7days_ago)
  
  # Define a helper function to fetch data
  query_params <- list(
    `$format` = "json",
    `$filter` = paste0("StationName eq '", stationName, "' AND ReadingDate gt ", formatted_datetime_7days_ago),
    `$orderby` = "ReadingDate desc",
    `$select` = "StationName,ParameterName,ReadingDate,Value"
  )
  
  api_url <- modify_url(base_url, query = query_params)
  
  # Attempt to fetch the data
  response <- try(GET(api_url, timeout(2500)), silent = TRUE)
  
  if (!inherits(response, "try-error") && response$status_code == 200) {
    content_data <- content(response, "text", encoding = "UTF-8")
    df <- fromJSON(content_data)$value
  } else {
    return(NULL)
  }
  
  # Check if data is available
  if (is.null(df)) {
    return(NULL)
  }
  
  # Process the data
  df$ReadingDate <- as.POSIXct(df$ReadingDate, format = "%Y-%m-%dT%H:%M:%S", tz = "America/Edmonton")
  df$Value <- suppressWarnings(as.numeric(df$Value))
  
  
  # Additional processing as needed (e.g., adding units, abbreviations, etc.)
  df <- df %>%
    mutate(
      ParameterName = if_else(is.na(ParameterName) | ParameterName == "", "AQHI", ParameterName),
      Units = case_when(
        ParameterName == "AQHI" ~ "AQHI",
        ParameterName == "Ozone" ~ "ppb",
        ParameterName == "Total Oxides of Nitrogen" ~ "ppb",
        ParameterName == "Hydrogen Sulphide" ~ "ppb",
        ParameterName == "Total Reduced Sulphur" ~ "ppb",
        ParameterName == "Sulphur Dioxide" ~ "ppb",
        ParameterName == "Fine Particulate Matter" ~ "µg/m³",
        ParameterName == "Total Hydrocarbons" ~ "ppm",
        ParameterName == "Carbon Monoxide" ~ "ppm",
        ParameterName == "Wind Direction" ~ "degrees",
        ParameterName == "Relative Humidity" ~ "%",
        ParameterName == "Outdoor Temperature" ~ "°C",
        ParameterName == "Nitric Oxide" ~ "ppb",
        ParameterName == "Wind Speed" ~ "km/hr",
        ParameterName == "Non-methane Hydrocarbons" ~ "ppm",
        ParameterName == "Nitrogen Dioxide" ~ "ppb",
        ParameterName == "Methane" ~ "ppm",
        TRUE ~ NA_character_
      ),
      Abbreviation = case_when(
        ParameterName == "AQHI" ~ "AQHI",
        ParameterName == "Ozone" ~ "O₃",
        ParameterName == "Total Oxides of Nitrogen" ~ "NOx",
        ParameterName == "Hydrogen Sulphide" ~ "H₂S",
        ParameterName == "Total Reduced Sulphur" ~ "TRS",
        ParameterName == "Sulphur Dioxide" ~ "SO₂",
        ParameterName == "Fine Particulate Matter" ~ "PM2.5",
        ParameterName == "Total Hydrocarbons" ~ "THC",
        ParameterName == "Carbon Monoxide" ~ "CO",
        ParameterName == "Wind Direction" ~ "WD",
        ParameterName == "Relative Humidity" ~ "RH",
        ParameterName == "Outdoor Temperature" ~ "ET",
        ParameterName == "Nitric Oxide" ~ "NO",
        ParameterName == "Wind Speed" ~ "WS",
        ParameterName == "Non-methane Hydrocarbons" ~ "NMHC",
        ParameterName == "Nitrogen Dioxide" ~ "NO₂",
        ParameterName == "Methane" ~ "CH₄",
        TRUE ~ NA_character_
      )
    ) %>%
    arrange(factor(ParameterName, levels = c("AQHI", "Fine Particulate Matter", "Ozone", "Nitrogen Dioxide", "Total Oxides of Nitrogen",
                                             "Nitric Oxide", "Sulphur Dioxide", "Hydrogen Sulphide", "Total Reduced Sulphur",
                                             "Carbon Monoxide", "Total Hydrocarbons", "Methane", "Non-methane Hydrocarbons",
                                             "Outdoor Temperature", "Relative Humidity", "Wind Speed", "Wind Direction")))
  
  # Apply corrections and rounding
  df <- df %>%
    dplyr::select(-contains("__metadata")) %>%
    mutate(Value = if_else(ParameterName == "AQHI" & Value > 10, "10+", as.character(Value))) %>%
    mutate(Value = as.numeric(Value)) %>%
    mutate(Value = case_when(
      ParameterName %in% c("Ozone", "Total Oxides of Nitrogen", "Hydrogen Sulphide", "Total Reduced Sulphur", "Sulphur Dioxide", "Nitric Oxide", "Nitrogen Dioxide") ~ Value * 1000,
      TRUE ~ Value  # Keep original Value if non-numeric or not in the list
    ))
  
  return(df)
}




# scripts/utils_fetch.R ------------------------------------------------
# Load once per R session ---------------------------------------------

if (!exists("..utils_fetch_loaded", inherits = FALSE)) {
  
  suppressPackageStartupMessages({
    library(httr)
    library(jsonlite)
    library(dplyr)
    library(lubridate)
  })
  
  # --------------------------------------------------------------------
  # fetchAndProcessWeek() – returns a tidy tibble for one station
  # --------------------------------------------------------------------
  fetchAndProcessWeek <- function(stationName, lookback_days = 7) {
    
    base_url <- "https://data.environment.alberta.ca/EdwServices/aqhi/odata/StationMeasurements"
    current_datetime   <- Sys.time() |> with_tz("America/Edmonton")
    start_iso <- (current_datetime - days(lookback_days)) |>
      format("%Y-%m-%dT%H:%M:%S%z") |>
      sub("(\\d{2})(\\d{2})$", "\\1:\\2", .)
    
    qry <- list(
      `$format` = "json",
      `$filter` = sprintf("StationName eq '%s' AND ReadingDate gt %s",
                          stationName, start_iso),
      `$orderby` = "ReadingDate desc",
      `$select`  = "StationName,ParameterName,ReadingDate,Value"
    )
    
    resp <- try(httr::GET(httr::modify_url(base_url, query = qry),
                          httr::timeout(45)), silent = TRUE)
    
    if (inherits(resp, "try-error") || httr::status_code(resp) != 200)
      return(NULL)
    
    df <- jsonlite::fromJSON(httr::content(resp, "text", encoding = "UTF-8"))$value
    if (length(df) == 0) return(NULL)
    
    # ---- tidy & enrich ------------------------------------------------
    df <- df |>
      mutate(
        ReadingDate = as.POSIXct(ReadingDate, format = "%Y-%m-%dT%H:%M:%S",
                                 tz = "America/Edmonton"),
        Value = suppressWarnings(as.numeric(Value)),
        ParameterName = if_else(ParameterName == "" | is.na(ParameterName),
                                "AQHI", ParameterName)
      ) |>
      mutate(
        Units = dplyr::case_when(
          ParameterName == "AQHI"                    ~ "AQHI",
          ParameterName == "Fine Particulate Matter" ~ "µg/m³",
          ParameterName %in%
            c("Ozone", "Total Oxides of Nitrogen", "Hydrogen Sulphide",
              "Total Reduced Sulphur", "Sulphur Dioxide",
              "Nitric Oxide", "Nitrogen Dioxide")    ~ "ppb",
          ParameterName == "Carbon Monoxide"         ~ "ppm",
          ParameterName == "Total Hydrocarbons"      ~ "ppm",
          ParameterName == "Non-methane Hydrocarbons"~ "ppm",
          ParameterName == "Wind Speed"              ~ "km/hr",
          ParameterName == "Wind Direction"          ~ "degrees",
          ParameterName == "Relative Humidity"       ~ "%",
          ParameterName == "Outdoor Temperature"     ~ "°C",
          TRUE ~ NA_character_
        ),
        Abbreviation = case_when(
          ParameterName == "Fine Particulate Matter" ~ "PM2.5",
          ParameterName == "Total Oxides of Nitrogen"~ "NOx",
          ParameterName == "Ozone"                   ~ "O₃",
          ParameterName == "Sulphur Dioxide"         ~ "SO₂",
          ParameterName == "Nitrogen Dioxide"        ~ "NO₂",
          ParameterName == "Nitric Oxide"            ~ "NO",
          ParameterName == "Hydrogen Sulphide"       ~ "H₂S",
          ParameterName == "Total Reduced Sulphur"   ~ "TRS",
          ParameterName == "Total Hydrocarbons"      ~ "THC",
          ParameterName == "Carbon Monoxide"         ~ "CO",
          ParameterName == "Non-methane Hydrocarbons"~ "NMHC",
          ParameterName == "Wind Speed"              ~ "WS",
          ParameterName == "Wind Direction"          ~ "WD",
          ParameterName == "Relative Humidity"       ~ "RH",
          ParameterName == "Outdoor Temperature"     ~ "ET",
          TRUE                                       ~ ParameterName
        )
      ) |>
      arrange(ReadingDate)
    
    # Apply unit conversions
    df <- df |>
      mutate(Value = ifelse(ParameterName %in%
                              c("Ozone", "Total Oxides of Nitrogen",
                                "Hydrogen Sulphide", "Total Reduced Sulphur",
                                "Sulphur Dioxide", "Nitric Oxide",
                                "Nitrogen Dioxide"),
                            Value * 1000, Value)) |>
      mutate(Value = ifelse(ParameterName == "AQHI" & Value > 10, "10+", Value))
    
    df
  }
  
  ..utils_fetch_loaded <- TRUE   # prevents double-loading in the same session
}

