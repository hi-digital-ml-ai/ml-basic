-- Glossary shortcodes. Every term lives once, in _glossary.yml, so the box on a page
-- and the Glossary page cannot drift apart.
--
--   {{< new-terms >}}  the terms this page introduces, in a collapsed callout
--   {{< glossary >}}   every term, A to Z, with links to the pages that explain it
--
-- Each entry in _glossary.yml has a `term`, a one-sentence `definition` (markdown,
-- no links: the same text is shown on pages at different depths), the `page` that
-- first explains it, and optionally `more`, a later page that covers it in full.
-- Pages are paths from the project root. Shortcodes run on every render, even for
-- a frozen page, so editing the file updates every box without re-running any R.

local stringify = pandoc.utils.stringify

local function project_dir()
  return quarto.project.directory or "."
end

local function this_page()
  return pandoc.path.make_relative(quarto.doc.input_file, project_dir())
end

local function up_to_root(rel)
  local up = ""
  for _ in rel:gmatch("/") do up = up .. "../" end
  return up
end

local function read_file(path)
  local f = io.open(path, "r")
  if not f then return nil end
  local text = f:read("a")
  f:close()
  return text
end

local terms
local function load_terms()
  if terms then return terms end
  local path = pandoc.path.join({ project_dir(), "_glossary.yml" })
  local text = read_file(path)
  if not text then
    quarto.log.warning("glossary: cannot read " .. path)
    terms = {}
    return terms
  end
  -- Pandoc parses a YAML block as metadata, turning each string into markdown inlines.
  terms = pandoc.read("---\n" .. text .. "\n---\n", "markdown").meta.terms or {}
  return terms
end

-- The title in a page's front matter, for the link text on the Glossary page.
local titles = {}
local function page_title(rel)
  if titles[rel] then return titles[rel] end
  local text = read_file(pandoc.path.join({ project_dir(), rel })) or ""
  local title = text:match('\ntitle:%s*"([^"\n]+)"') or text:match("\ntitle:%s*([^\n]+)") or rel
  titles[rel] = title
  return title
end

local function entry(t)
  local inlines = pandoc.Inlines({ pandoc.Strong(t.term), pandoc.Str(":"), pandoc.Space() })
  inlines:extend(t.definition)
  return inlines
end

local function new_terms()
  local page = this_page()
  local items = {}
  for _, t in ipairs(load_terms()) do
    if stringify(t.page) == page then
      table.insert(items, { pandoc.Plain(entry(t)) })
    end
  end
  if #items == 0 then
    quarto.log.warning("glossary: no terms for " .. page)
    return pandoc.Blocks({})
  end
  local more = pandoc.Para({
    pandoc.Str("Every term in the course is in the"), pandoc.Space(),
    pandoc.Link("Glossary", up_to_root(page) .. "glossary.qmd"), pandoc.Str(".")
  })
  return quarto.Callout({
    type = "note",
    title = "New terms on this page",
    collapse = true,
    content = { pandoc.BulletList(items), more },
  })
end

local function glossary()
  local sorted = {}
  for _, t in ipairs(load_terms()) do table.insert(sorted, t) end
  table.sort(sorted, function(a, b) return stringify(a.term):lower() < stringify(b.term):lower() end)

  local blocks = pandoc.Blocks({})
  local letter, items = nil, {}
  local function flush()
    if #items > 0 then blocks:insert(pandoc.DefinitionList(items)) end
    items = {}
  end
  for _, t in ipairs(sorted) do
    local first = stringify(t.term):sub(1, 1):upper()
    if first:match("%d") then first = "0–9" end
    if first ~= letter then
      flush()
      letter = first
      blocks:insert(pandoc.Header(2, first))
    end
    local where = pandoc.Inlines({ pandoc.Emph("Introduced in"), pandoc.Space(),
      pandoc.Link(page_title(stringify(t.page)), stringify(t.page)) })
    if t.more then
      where:extend({ pandoc.Str(";"), pandoc.Space(), pandoc.Emph("in full in"), pandoc.Space(),
        pandoc.Link(page_title(stringify(t.more)), stringify(t.more)) })
    end
    where:insert(pandoc.Str("."))
    table.insert(items, { t.term, { { pandoc.Para(t.definition), pandoc.Para(where) } } })
  end
  flush()
  return blocks
end

return {
  ["new-terms"] = new_terms,
  ["glossary"] = glossary,
}
