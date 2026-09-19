-- Put a download line at the top of every page that has code.
--
-- The scripts themselves are written by tools/extract-code.py before the render.
-- This filter only decides which links a page gets, and it decides from the
-- document itself: a page shows an R link when it has an R chunk and a Python
-- link when it has a Python block, so a page that gains or loses a language
-- gets the right links without anyone editing it.

local has_r, has_py = false, false

function CodeBlock(block)
  if block.classes:includes("r") then has_r = true end
  if block.classes:includes("python") then has_py = true end
end

-- "chapters/07-validation/cross-validation.qmd" -> "07-validation/cross-validation",
-- "toolkit/r-with-tidymodels.qmd" -> "toolkit/r-with-tidymodels". Both sit two
-- levels under downloads/code/, which is what lets the Python scripts find the
-- bundle root with parents[2].
local function code_stem(rel)
  local stem = rel:gsub("%.qmd$", "")
  return (stem:gsub("^chapters/", ""))
end

local function up_to_root(rel)
  local up = ""
  for _ in rel:gmatch("/") do up = up .. "../" end
  return up
end

-- Real pandoc links, not raw HTML: extract-code.py runs before the render, so the
-- targets exist and Quarto resolves them. A download link that ever breaks then
-- shows up as a build warning rather than as a 404 for a reader.
local function anchor(text, href, class)
  local classes = class and { class } or {}
  return pandoc.Link(pandoc.Str(text), href, "", pandoc.Attr("", classes, { download = "" }))
end

function Pandoc(doc)
  if not (has_r or has_py) then return nil end
  if not quarto.doc.is_format("html") then return nil end

  local project = quarto.project.directory
  local input = quarto.doc.input_file
  if not (project and input) then return nil end

  local rel = input:sub(#project + 2)
  if not (rel:match("^chapters/") or rel:match("^toolkit/") or rel:match("^contributed/")) then
    return nil
  end
  -- Must match what extract-code.py skips, or a page would link to a file that
  -- was never written. index.qmd is a listing and _ files are Quarto partials.
  local name = rel:match("([^/]+)$")
  if name == "index.qmd" or name:match("^_") then return nil end

  local up = up_to_root(rel)
  local stem = code_stem(rel)
  local base = stem:match("([^/]+)$")

  local items = pandoc.List({ pandoc.Str("Code from this page:") })
  local function add(link)
    items:insert(pandoc.Space())
    items:insert(link)
  end
  local dl = up .. "downloads/"
  if has_r then add(anchor(base .. ".R", dl .. "code/" .. stem .. ".R")) end
  if has_py then add(anchor(base .. ".py", dl .. "code/" .. stem .. ".py")) end
  -- Not a filename, so not in the monospace the two script links use.
  add(anchor("whole course, with the data", dl .. "ml-basic-code.zip", "bundle"))

  doc.blocks:insert(1, pandoc.Div(pandoc.Plain(items), pandoc.Attr("", { "code-downloads" })))
  return doc
end
