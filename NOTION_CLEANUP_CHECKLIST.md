# Notion Integration Cleanup Checklist
**Track cleanup progress step-by-step**

---

## ✅ Phase 1: Archive Broken Code

### Backend Files (Move to `archive/notion-failed-attempts/backend/`)
- [ ] `backend/notion_sync_service.py` (498 lines)
- [ ] `backend/setup_notion_sync.py` (174 lines)
- [ ] `backend/test_notion_sync.py` (198 lines)
- [ ] `backend/NOTION_SYNC_README.md` (documentation)

### Scripts (Move to `archive/notion-failed-attempts/scripts/`)
- [ ] `scripts/notion_continuous_sync.py` (705 lines)
- [ ] `scripts/notion_github_sync.py` (299 lines)
- [ ] `scripts/create_notion_workspace.py`
- [ ] `scripts/create_notion_workspace_beautiful.py`
- [ ] `scripts/create_notion_workspace_styled.py`
- [ ] `scripts/create_root_workspace.py`
- [ ] `scripts/create_workflow_notion_page.py`
- [ ] `scripts/sync_notion.py`
- [ ] `scripts/setup_github_notion.py`
- [ ] `scripts/export_modules_from_notion.py`

### Batch Files (Delete)
- [ ] `setup_notion_integration.bat`
- [ ] `run_notion_setup.bat`
- [ ] Review `setup_and_run.bat` (keep if non-Notion, delete if Notion-only)

---

## ✅ Phase 2: Update Dependencies

### requirements.txt
- [ ] Add `notionary` to requirements.txt
- [ ] Verify no `notion-client` listed
- [ ] Run `pip install -r requirements.txt` to test

---

## ✅ Phase 3: Clean Environment Variables

### .env File Review
- [ ] Remove `NOTION_PARENT_PAGE_ID` (if exists)
- [ ] Remove all `NOTION_DB_*` variables
- [ ] Remove all `NOTION_DS_*` variables
- [ ] Keep `NOTION_SECRET` or `NOTION_API_KEY`
- [ ] Keep `DATABASE_URL`

---

## ✅ Phase 4: Update Documentation

### Canonical Docs
- [ ] Rewrite `canon/NOTION_INTEGRATION.md` for notionary
- [ ] Update `canon/AGENT_SYSTEM_OVERVIEW.md` (Notion rules)
- [ ] Update `.github/copilot-instructions.md` (remove old sync references)

### Agent Queue
- [ ] Mark Phase 2 unblocked in `agent_work_queues/beta_queue.md`
- [ ] Remove Notion blocker note
- [ ] Add notionary installation as completed task

### Archive Index
- [ ] Add entry to `canon/ARCHIVE_INDEX.md` pointing to failed attempts

---

## ✅ Phase 5: Create New Services (Notionary-based)

### Template Reader
- [ ] Create `backend/notion_template_reader.py`
- [ ] Implement `get_database_schema()` method
- [ ] Implement `get_page_structure()` method
- [ ] Implement `analyze_template()` method
- [ ] Test with "Foundation" page

### Data Display Service
- [ ] Create `backend/notion_data_display.py`
- [ ] Implement `update_team_dashboard()` method
- [ ] Implement safe page retrieval wrapper
- [ ] Add audit logging for all operations
- [ ] Test with one team dashboard

### Module Library Sync
- [ ] Create `backend/notion_module_sync.py`
- [ ] Implement `sync_module_library()` function
- [ ] Add "no creation" safety checks
- [ ] Test with existing module library

---

## ✅ Phase 6: Testing & Validation

### Basic Access Tests
- [ ] Can find "Foundation" page by title
- [ ] Can read page content as Markdown
- [ ] Can get database schema description
- [ ] No 404 errors on any operation

### Template Analysis Tests
- [ ] Successfully document all database schemas
- [ ] Identify property names and types
- [ ] Identify valid select/status options
- [ ] Create `docs/notion/TEMPLATE_STRUCTURE_ANALYSIS.md`

### Data Display Tests
- [ ] Update one Notion page property successfully
- [ ] Append content to page without errors
- [ ] Verify no accidental page creation
- [ ] Audit logs capture all operations

---

## ✅ Phase 7: Human Review Checkpoints

### After Cleanup (Phase 1-3)
- [ ] Review archived files list
- [ ] Confirm safe to delete batch files
- [ ] Approve new requirements.txt

### After Template Analysis (Phase 5.1)
- [ ] Review template structure documentation
- [ ] Approve identified safe zones for agent edits
- [ ] Confirm no page creation occurred

### After Data Display (Phase 5.2)
- [ ] Review sample Notion page update
- [ ] Approve integration approach
- [ ] Confirm safety measures working

---

## 📊 Progress Metrics

**Total Files to Archive**: 14 scripts + 4 docs = 18 files  
**Total Lines Removed**: ~2,800 lines of broken code  
**New Code to Write**: ~500 lines (3 new services)  
**Net Code Reduction**: ~2,300 lines (82% reduction)  

**Estimated Time**:
- Cleanup: 1 hour
- Installation: 30 minutes
- Template Reader: 2 hours
- Data Display: 3 hours
- Testing: 2 hours
- **Total**: ~8.5 hours

---

## 🚨 Safety Checks

Before marking each phase complete:
- [ ] No production code depends on archived files
- [ ] All imports updated (no broken references)
- [ ] Tests still pass (if any exist)
- [ ] Documentation reflects new approach
- [ ] Human approved changes

---

**Status**: Not Started  
**Started**: [Date/Time when cleanup begins]  
**Completed**: [Date/Time when all phases done]  
**Agent**: Beta
