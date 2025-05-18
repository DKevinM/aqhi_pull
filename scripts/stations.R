# scripts/stations.R ---------------------------------------------------
# A master list of stations + metadata.  Update here; nowhere else. ----

stations <- tibble::tribble(
  ~StationName,              ~Lat,          ~Lon,          ~zone, ~Monitor,
  "Edmonton McCauley",       53.549483,  -113.485964, "ACA",  "Tr",
  "St. Albert",              53.626969,  -113.611905, "ACA",  "Tr",
  "Woodcroft",               53.564660,  -113.562667, "ACA",  "Tr",
  "Edmonton East",           53.548008,  -113.367969, "ACA",  "Tr",
  "Edmonton Lendrum",        53.497784,  -113.527011, "ACA",  "Tr",
  "Ardrossan",               53.547200,  -113.100100, "ACA",  "Tr",
  "Sherwood Park",           53.511400,  -113.295900, "ACA",  "Tr",
  "O’Morrow Station 1",      54.903678,  -112.843336, "ACA",  "Tr",
  "Poacher’s Landing Station 2", 54.945779, -112.816541, "ACA", "Tr",
  "Leduc Sensor",            53.241439,  -113.503769, "ACA",  "Se",
  "Breton",                  53.090262,  -114.460604, "WCAS", "Tr",
  "Carrot Creek",            53.620913,  -115.870659, "WCAS", "Tr",
  "Drayton Valley",          53.220024,  -114.983974, "WCAS", "Tr",
  "Edson",                   53.593824,  -116.395877, "WCAS", "Tr",
  "Genesee",                 53.301561,  -114.201572, "WCAS", "Tr",
  "Hinton-Drinnan",          53.427232,  -117.543983, "WCAS", "Tr",
  "Meadows",                 53.530120,  -114.636265, "WCAS", "Tr",
  "Powers",                  53.633122,  -114.420047, "WCAS", "Tr",
  "Steeper",                 53.132599,  -117.091395, "WCAS", "Tr",
  "Wagner2",                 53.424416,  -114.374886, "WCAS", "Tr",
  "Hinton-Hillcrest",        53.392740,  -117.584600, "WCAS", "Tr",
  "Jasper",                  52.873472,  -118.091417, "WCAS", "Se",
  "Enoch",                   53.498039,  -113.760693, "ACA",  "Tr"
)
