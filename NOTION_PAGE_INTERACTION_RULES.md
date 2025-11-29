# NOTION PAGE INTERACTION RULES – V2 (TEMPLATE PAGES)

## Scope
These rules apply when you are asked to work on any Notion template page (the "target page").
This includes dashboards, team pages, project templates, and other structured pages that maintain consistent formatting.
Your job is to add or lightly edit content without damaging the template structure.

## 0. Core Principle

**You are editing a structured template, not a blank document.**
- You may only change content inside safe regions.
- You must never change the page's structure.

**If you are unsure whether something is safe to edit → do nothing and ask for clarification instead of guessing.**

## 1. Page Model You Must Assume

On the target page, assume there are three types of blocks:

### Structural blocks (PROTECTED)
- Page title
- Top navigation sections (e.g., "Launch Readiness Dashboard", "Documentation", "Team Management", etc.)
- Section headings (e.g., "Mission Objectives", "Mission Snapshot", "Navigation", "Subsystem Workspaces")
- Linked database views (tables, boards, timelines)
- Any block whose main purpose is navigation or layout

### Content blocks (EDITABLE)
- Paragraph text under a heading
- Bullet / numbered lists under a heading
- Checklists under a heading
- Text inside toggles (but not the toggle title itself)
- Callout body text (but not the title or icon)

### Database data (EDITABLE VIA PROPERTIES, NOT BY TYPING ON PAGE)
- Rows in a linked Tasks/Modules/People/Launch_Readiness database
- Properties such as Status, Owner, Subsystem, Tier, Domain, etc.

## 2. Allowed vs Forbidden Actions

### 2.1 Allowed Actions (on this single page)

You may:

1. **Append content under an existing heading**
   - Add bullet items to an existing list
   - Add a new paragraph under a heading
   - Add checklist items under an existing checklist

2. **Lightly update existing content only if explicitly asked**
   - Fix wording in a paragraph
   - Rephrase a bullet item
   - Correct typos

3. **Update database rows via properties** (if you have MCP tools for that)
   - Change Status, Owner, Subsystem, etc.
   - Create a new row in an existing database

**When you change database rows, do it through the database API / MCP method, not by typing into the linked view on the page.**

### 2.2 Forbidden Actions (always)

You must NOT:

1. **Change the structure of the page**
   - Do not delete headings or rename them
   - Do not reorder major sections
   - Do not change navigation lists ("Launch Readiness Dashboard", "Documentation", etc.)
   - Do not delete or recreate linked database views

2. **Replace structural blocks with plain text**
   - Do not convert navigation items into paragraphs
   - Do not rewrite "Subsystem Workspaces" or "Knowledge Management" as a narrative

3. **Create new major sections**
   - Do not add new H1/H2 headings unless explicitly told
   - Do not invent new nav categories

4. **Summarize or duplicate the entire page**
   - Do not copy the structure into new text on the same page
   - Do not "rebuild" the template in your own style

5. **Blindly overwrite existing content**
   - Never delete existing content unless the user explicitly says "replace" or "remove"

## 3. Required Algorithm Before You Edit

Whenever you are asked to modify this page, follow this checklist:

1. **Fetch the full page/block tree** using the Notion MCP tools.

2. **Locate the relevant section** based on the user's request.
   - Example: "Add a mission objective" → find the heading "Mission Objectives".

3. **Classify the target block:**
   - If it's a heading, navigation item, linked view, or similar → **PROTECTED**.
   - If it's a paragraph / bullet list / checklist under a heading → **EDITABLE CONTENT**.

4. **If PROTECTED:**
   - Do not edit it.
   - Instead, append new content under that heading in a new paragraph/list item.

5. **If EDITABLE CONTENT:**
   - Append or edit as requested, without changing the heading or surrounding structure.

6. **If the request implies a database change** (e.g., "mark the Avionics subsystem as Ready"):
   - Use the appropriate MCP method to update the database row (e.g., `update_database_item`), not text on the page.

7. **If you are not certain where to write:**
   - Do not guess.
   - Return a clarifying message like:
     > "I found multiple possible locations for this change and I am not allowed to modify the page structure. Please specify which section I should use."

## 4. Summary

- **Fetch first, classify second, edit last.**
- **When in doubt, ask.**
- **Preserve the template structure at all costs.**

## 10. New Page / Subpage Restrictions

When working with template pages, you must obey these rules:

- **Do NOT create any new pages or subpages under any template page.**
- **Do NOT move content into a new page.**
- **Do NOT duplicate template pages, or "archive" the old one and make a new one.**

Your only allowed operations are:

1. Append or lightly edit content in existing editable regions
2. Update existing database rows / properties (via tools), if available

If you think "maybe this should be a new page" → you are required to STOP and instead return a message such as:

> "I am not allowed to create new pages or subpages when working with template pages. I don't see a clearly designated region for this content. Please tell me exactly where it should go or confirm that I should create a new page."

**Creating a new subpage as a fallback when you are stuck is always forbidden when working with template pages.**
