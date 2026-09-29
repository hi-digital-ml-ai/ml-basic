# Display for the Python tabs, which knitr runs through reticulate.
# Pages with Python tabs load this in their setup chunk:
#   source(here::here("R/python-tabs.R"))
#
# A tibble prints as a table (df-print: kable in _quarto.yml), but reticulate
# prints a pandas DataFrame as plain text. This makes the Python tab match: a
# chunk whose last value is a DataFrame shows it as a Markdown table, through
# pandas' to_markdown() (which needs the Python package tabulate). The default
# 0, 1, 2 ... row index is left out, as a tibble has none; any other index stays.
# Everything else a Python chunk prints is unchanged.
#
# It works by wrapping reticulate's internal eng_python_autoprint(), so check it
# after upgrading reticulate: render a page with a Python table and look.
# Outside a render (a downloaded script, say) it does nothing.

local({
  if (!isTRUE(getOption("knitr.in.progress")) ||
      !requireNamespace("reticulate", quietly = TRUE)) {
    return(invisible())
  }

  ns <- asNamespace("reticulate")
  original <- get("eng_python_autoprint", envir = ns)
  if (isTRUE(attr(original, "mlbasic"))) return(invisible())   # already wrapped
  engine_context <- get(".engine_context", envir = ns)

  # Longer tables stay as text, which pandas shortens; a table this long does
  # not belong on a page anyway.
  max_rows <- 30

  py_last_value <- get("py_last_value", envir = ns)

  autoprint <- function(captured, options) {
    value <- py_last_value()
    is_frame <- inherits(value, c("pandas.core.frame.DataFrame", "pandas.DataFrame"))
    if (!is_frame || !knitr::is_html_output() ||
        reticulate::py_len(value) > max_rows) {
      return(original(captured, options))
    }
    index <- !inherits(value$index, c("pandas.core.indexes.range.RangeIndex",
                                      "pandas.RangeIndex"))
    table <- reticulate::py_to_r(value$to_markdown(index = index))
    engine_context$pending_plots$push(knitr::asis_output(paste0("\n", table, "\n")))
    ""
  }
  attr(autoprint, "mlbasic") <- TRUE

  unlockBinding("eng_python_autoprint", ns)
  assign("eng_python_autoprint", autoprint, envir = ns)
  lockBinding("eng_python_autoprint", ns)
})
