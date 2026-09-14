source("renv/activate.R")

# Prefer Posit Package Manager's prebuilt Linux binaries when they match this
# machine; fall back to CRAN source packages everywhere else. This is purely an
# install-speed choice -- renv.lock pins the versions either way.
local({
  repo <- "https://cloud.r-project.org"
  if (Sys.info()[["sysname"]] == "Linux" && file.exists("/etc/os-release")) {
    os <- readLines("/etc/os-release", warn = FALSE)
    id <- sub("^ID=", "", grep("^ID=", os, value = TRUE))
    codename <- sub("^VERSION_CODENAME=", "", grep("^VERSION_CODENAME=", os, value = TRUE))
    if (length(id) == 1L && id == "ubuntu" && length(codename) == 1L && nzchar(codename)) {
      repo <- sprintf("https://packagemanager.posit.co/cran/__linux__/%s/latest", codename)
    }
  }
  options(repos = c(CRAN = repo))
})
