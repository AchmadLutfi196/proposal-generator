-- docx.lua: Filter Pandoc untuk proposal skripsi FT UTM
-- Menangani Cover Page resmi, Abstrak, DAFTAR ISI, DAFTAR GAMBAR, DAFTAR TABEL,
-- penomoran bab (BAB I, 1.1, 1.1.1 tanpa titik akhir), serta caption otomatis.

local bab = 0
local sub = 0
local subsub = 0
local fig_count = 0
local tbl_count = 0
local toc_entries = {}
local fig_entries = {}
local tbl_entries = {}

local chapter_prefix = "BAB "
local chapter_num_fmt = "roman"
local sub_dot = false
local subsub_dot = false

local function is_unnumbered(el)
  for _, cls in ipairs(el.attr.classes or {}) do
    if cls == "unnumbered" then
      return true
    end
  end
  return false
end

local function roman(n)
  local map = {
    {1000, "M"}, {900, "CM"}, {500, "D"}, {400, "CD"},
    {100, "C"}, {90, "XC"}, {50, "L"}, {40, "XL"},
    {10, "X"}, {9, "IX"}, {5, "V"}, {4, "IV"}, {1, "I"},
  }
  local out = ""
  for _, pair in ipairs(map) do
    while n >= pair[1] do
      out = out .. pair[2]
      n = n - pair[1]
    end
  end
  return out
end

local function balance_title(text)
  local words = {}
  for w in text:gmatch("%S+") do
    words[#words + 1] = w
  end
  local n = #words
  if n <= 1 or #text <= 45 then
    return { text }
  end
  local function best_for(k)
    local best, best_cost = nil, math.huge
    local function rec(i, kk, cur, mx)
      if kk == 1 then
        local line = table.concat(words, " ", i, n)
        local lines = {}
        for _, l in ipairs(cur) do lines[#lines + 1] = l end
        lines[#lines + 1] = line
        local m = math.max(mx, #line)
        local cost = m
        if cost < best_cost then
          best, best_cost = lines, cost
        end
        return
      end
      for j = i, n - kk + 1 do
        local line = table.concat(words, " ", i, j)
        local nxt = {}
        for _, l in ipairs(cur) do nxt[#nxt + 1] = l end
        nxt[#nxt + 1] = line
        rec(j + 1, kk - 1, nxt, math.max(mx, #line))
      end
    end
    rec(1, k, {}, 0)
    return best
  end
  local two = best_for(2)
  if #two[1] >= #two[2] then
    return two
  end
  return best_for(3) or two
end

local function para(content, style)
  return pandoc.Div(
    { pandoc.Para(content) },
    pandoc.Attr("", {}, { ["custom-style"] = style })
  )
end

local function pagebreak()
  return pandoc.RawBlock("openxml", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
end

local function spacer(before)
  return pandoc.RawBlock(
    "openxml",
    '<w:p><w:pPr><w:spacing w:before="' .. before .. '"/></w:pPr></w:p>'
  )
end

local function meta_str(meta, key)
  local v = meta[key]
  if v == nil then return "" end
  return pandoc.utils.stringify(v)
end

local function Meta(meta)
  if meta["heading_sub_dot"] ~= nil then
    sub_dot = (meta_str(meta, "heading_sub_dot") == "true")
  end
  if meta["heading_subsub_dot"] ~= nil then
    subsub_dot = (meta_str(meta, "heading_subsub_dot") == "true")
  end
end

function Header(el)
  if FORMAT ~= "docx" then return nil end
  local title = pandoc.utils.stringify(el.content)
  if is_unnumbered(el) then
    if el.level == 1 then
      toc_entries[#toc_entries + 1] = {
        level = 1,
        id = el.identifier,
        text = string.upper(title),
      }
    end
    return nil
  end

  if el.level == 1 then
    bab = bab + 1
    sub = 0
    subsub = 0
    fig_count = 0
    tbl_count = 0
    local bnum = roman(bab)
    local full_bab = chapter_prefix .. bnum
    toc_entries[#toc_entries + 1] = {
      level = 1,
      id = el.identifier,
      text = full_bab .. " " .. string.upper(title),
    }
    el.content = pandoc.List{
      pandoc.Str(full_bab),
      pandoc.LineBreak(),
      pandoc.Str(string.upper(title)),
    }
  elseif el.level == 2 then
    sub = sub + 1
    subsub = 0
    local sdot = sub_dot and ". " or " "
    local full_title = bab .. "." .. sub .. sdot .. title
    toc_entries[#toc_entries + 1] = {
      level = 2,
      id = el.identifier,
      text = full_title,
    }
    el.content = pandoc.Str(full_title)
  elseif el.level == 3 then
    subsub = subsub + 1
    local ssdot = subsub_dot and ". " or " "
    local full_title = bab .. "." .. sub .. "." .. subsub .. ssdot .. title
    toc_entries[#toc_entries + 1] = {
      level = 3,
      id = el.identifier,
      text = full_title,
    }
    el.content = pandoc.Str(full_title)
  end
  return el
end

local function toc_entry(e)
  local style, ind, bold, spacing = "TOC1", 0, "<w:rPr><w:b/></w:rPr>", '<w:spacing w:before="120" w:after="40" w:line="260" w:lineRule="auto"/>'
  if e.level == 2 then
    style, ind, bold, spacing = "TOC2", 360, "", '<w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
  elseif e.level == 3 then
    style, ind, bold, spacing = "TOC3", 720, "", '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
  end
  return '<w:p><w:pPr><w:pStyle w:val="' .. style .. '"/>' ..
    spacing ..
    '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9072"/></w:tabs>' ..
    '<w:ind w:left="' .. ind .. '" w:right="0"/></w:pPr>' ..
    '<w:hyperlink w:anchor="' .. e.id .. '" w:history="1">' ..
    '<w:r>' .. bold .. '<w:t xml:space="preserve">' .. e.text .. '</w:t></w:r>' ..
    '</w:hyperlink>' ..
    '<w:r><w:tab/></w:r>' ..
    '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>' ..
    '<w:r><w:instrText xml:space="preserve"> PAGEREF ' .. e.id .. ' \\h </w:instrText></w:r>' ..
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' ..
    '<w:r><w:t>0</w:t></w:r>' ..
    '<w:r><w:fldChar w:fldCharType="end"/></w:r>' ..
    '</w:p>'
end

local function build_toc()
  local out = pandoc.List{}
  out[#out + 1] = pagebreak()
  out[#out + 1] = pandoc.RawBlock(
    "openxml",
    '<w:p><w:pPr><w:pStyle w:val="TOCHeading"/><w:jc w:val="center"/><w:outlineLvl w:val="9"/></w:pPr>' ..
      '<w:r><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr><w:t>DAFTAR ISI</w:t></w:r></w:p>'
  )
  out[#out + 1] = pandoc.RawBlock(
    "openxml",
    '<w:p><w:pPr><w:pStyle w:val="TOC1"/></w:pPr>' ..
      '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>' ..
      '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>' ..
      '<w:r><w:fldChar w:fldCharType="separate"/></w:r></w:p>'
  )
  for _, e in ipairs(toc_entries) do
    out[#out + 1] = pandoc.RawBlock("openxml", toc_entry(e))
  end
  out[#out + 1] = pandoc.RawBlock(
    "openxml",
    '<w:p><w:pPr><w:pStyle w:val="TOC1"/></w:pPr>' ..
      '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
  )
  return out
end

function Pandoc(doc)
  if FORMAT ~= "docx" then return doc end
  local meta = doc.meta
  local title = meta_str(meta, "title")
  local student_name = meta_str(meta, "author_name")
  if student_name == "" then
    local a = meta["author"]
    if a ~= nil then
      if a[1] ~= nil then student_name = pandoc.utils.stringify(a[1]["name"] or a[1])
      else student_name = pandoc.utils.stringify(a["name"] or a) end
    end
  end
  local student_nim = meta_str(meta, "author_nim")
  if student_nim == "" and meta["author"] ~= nil then
    local a = meta["author"]
    if a[1] ~= nil then student_nim = pandoc.utils.stringify(a[1]["nim"] or "")
    else student_nim = pandoc.utils.stringify(a["nim"] or "") end
  end

  local d1_name = meta_str(meta, "advisor_1_name")
  local d1_nip = meta_str(meta, "advisor_1_nip")
  local d2_name = meta_str(meta, "advisor_2_name")
  local d2_nip = meta_str(meta, "advisor_2_nip")

  local study_prog = meta_str(meta, "study_program")
  if study_prog == "" then study_prog = "PROGRAM STUDI TEKNIK INFORMATIKA" end
  local dept = meta_str(meta, "department")
  if dept == "" then dept = "JURUSAN TEKNIK INFORMATIKA" end
  local fac = meta_str(meta, "faculty")
  if fac == "" then fac = "FAKULTAS TEKNIK" end
  local inst = meta_str(meta, "institution")
  if inst == "" then inst = "UNIVERSITAS TRUNOJOYO MADURA" end
  local city = meta_str(meta, "city")
  if city == "" then city = "BANGKALAN" end
  local year = meta_str(meta, "year")
  if year == "" then year = "2026" end

  local blocks = pandoc.List{}

  -- 1. Halaman Cover
  if title ~= "" then
    local tlines = balance_title(string.upper(title))
    local content = {}
    for i, l in ipairs(tlines) do
      if i > 1 then content[#content + 1] = pandoc.LineBreak() end
      content[#content + 1] = pandoc.Str(l)
    end
    blocks[#blocks + 1] = para(content, "CoverTitle")
    blocks[#blocks + 1] = spacer(200)
    blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str("PROPOSAL SKRIPSI")) }, "CoverTitle")
    blocks[#blocks + 1] = spacer(400)

    -- Logo pentagon 4 cm
    local logo_path = meta_str(meta, "cover_logo")
    if logo_path == "" then logo_path = "logo.jpg" end
    blocks[#blocks + 1] = pandoc.Div(
      { pandoc.Para({ pandoc.Image({}, logo_path, "", pandoc.Attr("", {}, { width = "4cm" })) }) },
      pandoc.Attr("", {}, { ["custom-style"] = "CoverImage" })
    )
    blocks[#blocks + 1] = spacer(400)

    -- Penulis & NIM
    blocks[#blocks + 1] = para({ pandoc.Str("Oleh:") }, "CoverLine")
    blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(student_name:upper())) }, "CoverName")
    blocks[#blocks + 1] = para({ pandoc.Str(student_nim) }, "CoverLine")
    blocks[#blocks + 1] = spacer(300)

    -- Dosen Pembimbing
    local show_lecturer = meta_str(meta, "cover_show_lecturer") ~= "false"
    if show_lecturer and d1_name ~= "" then
      local d1_text = "Dosen Pembimbing I: " .. d1_name .. (d1_nip ~= "" and (" (" .. d1_nip .. ")") or "")
      blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(d1_text)) }, "CoverLine")
    end
    if show_lecturer and d2_name ~= "" then
      local d2_text = "Dosen Pembimbing II: " .. d2_name .. (d2_nip ~= "" and (" (" .. d2_nip .. ")") or "")
      blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(d2_text)) }, "CoverLine")
    end
    blocks[#blocks + 1] = spacer(400)

    -- Institusi
    blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(study_prog:upper())) }, "CoverInstitution")
    blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(dept:upper())) }, "CoverInstitution")
    blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(fac:upper())) }, "CoverInstitution")
    blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(inst:upper())) }, "CoverInstitution")
    blocks[#blocks + 1] = para({ pandoc.Strong(pandoc.Str(year)) }, "CoverInstitution")

    -- Penutup Section Cover (tanpa footer)
    blocks[#blocks + 1] = pandoc.RawBlock(
      "openxml",
      '<w:p><w:pPr><w:sectPr><w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1701" w:right="1701" w:bottom="1701" w:left="2268" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:pPr></w:p>'
    )
  end

  -- Sisipkan DAFTAR ISI sebelum BAB I
  local body = pandoc.List{}
  local inserted = false
  for _, blk in ipairs(doc.blocks) do
    if not inserted and blk.tag == "Header" and blk.level == 1 and not is_unnumbered(blk) then
      for _, b in ipairs(build_toc()) do
        body[#body + 1] = b
      end
      inserted = true
    end
    body[#body + 1] = blk
  end

  doc.blocks = blocks .. body
  return doc
end

return {
  { Meta = Meta },
  { Header = Header, Pandoc = Pandoc }
}
