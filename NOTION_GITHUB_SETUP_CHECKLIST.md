# GitHub-Notion Integration Setup Checklist

## Current Status: ✅ Ready for Configuration

Your repository has complete GitHub-Notion integration infrastructure. Follow this checklist to activate it.

---

## Pre-Setup (Already Complete ✅)

- [x] Notion API key obtained
- [x] API key added to `.env` file
- [x] GitHub Actions workflows created
- [x] Python sync scripts written
- [x] Repository structure organized
- [x] Setup wizard created
- [x] Documentation written

---

## Setup Tasks (Do These Now)

### 1. Notion Workspace Setup
- [ ] Create "FRAMES Project Hub" page in Notion
- [ ] Share page with FRAMES integration
  - Click "Share" → "Invite" → Add FRAMES integration
- [ ] Copy page ID from URL
- [ ] Run: `setup_notion_integration.bat`
- [ ] OR manually run: `python scripts\create_notion_workspace.py <PAGE_ID>`

### 2. Verify Databases Created
After running setup, verify these exist in Notion:
- [ ] ✅ Development Tasks database
- [ ] ⚙️ Technical Decisions database
- [ ] 🔗 Integration Checklist database
- [ ] 📚 Module Library database
- [ ] 📘 Project Overview page

### 3. Configure GitHub Secrets
Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`

Add these 3 secrets:
- [ ] `NOTION_API_KEY` = `<YOUR_NOTION_TOKEN>`
- [ ] `NOTION_TASKS_DB_ID` = (from workspace creation output)
- [ ] `NOTION_PARENT_PAGE_ID` = (your FRAMES Project Hub page ID)

### 4. Test Integration
- [ ] Run: `python scripts\test_notion_access.py`
- [ ] Verify connection works
- [ ] Run: `python scripts\notion_github_sync.py`
- [ ] Check for errors in output

### 5. Verify Automation
- [ ] Go to GitHub Actions tab
- [ ] Manually trigger "Notion-GitHub Task Sync" workflow
- [ ] Check workflow logs for success
- [ ] Verify no errors

### 6. Create Test Items
- [ ] Create a test task in Notion Development Tasks database
- [ ] Wait up to 6 hours OR trigger workflow manually
- [ ] Verify GitHub issue was created
- [ ] Create a GitHub issue with `notion-sync` label
- [ ] Verify Notion task was created
- [ ] Close one of the issues
- [ ] Verify the other updates to "Done" status

### 7. Documentation Sync Test
- [ ] Edit a file in `docs/` folder
- [ ] Commit and push to GitHub
- [ ] Verify "Sync Documentation to Notion" workflow runs
- [ ] Check Notion for updated documentation pages

---

## Post-Setup Configuration

### 8. Team Onboarding
- [ ] Share "FRAMES Project Hub" with team members
- [ ] Give them access to GitHub repository
- [ ] Share `NOTION_GITHUB_INTEGRATION_SETUP.md` guide
- [ ] Train team on workflow:
  - Notion for task planning
  - GitHub for development
  - Automatic sync keeps both updated

### 9. Customize Workflows (Optional)
- [ ] Adjust sync frequency in `.github/workflows/notion-github-sync.yml`
- [ ] Add custom task properties in `scripts/create_notion_workspace.py`
- [ ] Configure filters in `scripts/notion_github_sync.py`
- [ ] Set up Notion views (Kanban, Table, Calendar)

### 10. Monitor & Maintain
- [ ] Check GitHub Actions weekly for errors
- [ ] Monitor sync delays
- [ ] Keep Notion database properties consistent with script expectations
- [ ] Don't rename: "Task", "Status", "GitHub Issue URL", "Due" fields

---

## Quick Commands Reference

```bash
# Start interactive setup wizard
setup_notion_integration.bat

# Test Notion connection
python scripts\test_notion_access.py

# Create workspace (manual)
python scripts\create_notion_workspace.py <PAGE_ID>

# Sync tasks manually (for testing)
set NOTION_TASKS_DB_ID=<your_db_id>
python scripts\notion_github_sync.py

# Sync docs manually
python scripts\sync_notion.py <PARENT_PAGE_ID>

# Check GitHub Actions status
# Visit: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

---

## Troubleshooting Quick Fixes

### "Cannot access page" Error
```
Solution: Share the Notion page with FRAMES integration
1. Open page in Notion
2. Click Share → Invite
3. Add FRAMES integration
4. Wait 30 seconds
```

### "Authentication failed"
```
Solution: Verify .env file has correct NOTION_API_KEY
Check: type .env | findstr NOTION
```

### Sync not working
```
Solution: Verify GitHub secrets are set
1. Check all 3 secrets exist in GitHub
2. Verify they match your .env values
3. Trigger workflow manually to see logs
```

### Workflow not running
```
Solution: Check .github/workflows/ files exist
dir .github\workflows\
Should see: notion-github-sync.yml, sync-notion.yml
```

---

## Expected Workflow After Setup

### Daily Use - Notion Side
1. Team member creates task in Notion
2. Fills in Phase, Status, Priority, Due Date
3. Saves task
4. Within 6 hours (or next push), GitHub issue created automatically
5. Issue URL appears in Notion task

### Daily Use - GitHub Side
1. Developer creates issue in GitHub
2. Adds `notion-sync` label
3. Commits code with "Fixes #123"
4. Closes issue when done
5. Notion task automatically marked "Done"

### Daily Use - Documentation
1. Developer updates docs in `docs/` folder
2. Commits to GitHub
3. Push triggers documentation sync workflow
4. Notion pages update automatically
5. Team views updated docs in Notion's beautiful interface

---

## Success Metrics

After setup is complete, you should have:

✅ **Automated Sync Working**
- Tasks sync bidirectionally every 6 hours
- Docs sync when changed
- No manual copying needed

✅ **Team Productivity**
- Non-technical team uses Notion
- Developers use GitHub
- Everyone sees the same information
- No duplicate data entry

✅ **Visibility**
- Project status always up-to-date
- Stakeholders can check Notion anytime
- Developers don't leave their workflow
- Single source of truth (GitHub) with beautiful interface (Notion)

---

## Files You Created

Setup Process Created These:
- `NOTION_GITHUB_INTEGRATION_SETUP.md` - Full documentation
- `QUICK_START_NOTION_INTEGRATION.md` - Quick reference
- `scripts/setup_github_notion.py` - Interactive wizard
- `setup_notion_integration.bat` - Windows launcher
- `NOTION_GITHUB_SETUP_CHECKLIST.md` - This file

Already Existed:
- `.github/workflows/notion-github-sync.yml`
- `.github/workflows/sync-notion.yml`
- `scripts/notion_github_sync.py`
- `scripts/sync_notion.py`
- `scripts/create_notion_workspace.py`
- `scripts/test_notion_access.py`

---

## Next Steps Priority Order

**Priority 1: Get It Working (Today)**
1. Run `setup_notion_integration.bat`
2. Add 3 GitHub secrets
3. Test with one task

**Priority 2: Verify Automation (This Week)**
4. Create test items both directions
5. Verify sync works automatically
6. Check workflow logs for errors

**Priority 3: Team Rollout (Next Week)**
7. Share with team
8. Train on workflow
9. Monitor for issues

**Priority 4: Optimize (Ongoing)**
10. Customize views in Notion
11. Adjust sync frequency if needed
12. Add custom properties as needed

---

## Support Resources

- **Full Setup Guide:** `NOTION_GITHUB_INTEGRATION_SETUP.md`
- **Quick Start:** `QUICK_START_NOTION_INTEGRATION.md`
- **Test Script:** `scripts\test_notion_access.py`
- **Setup Wizard:** `scripts\setup_github_notion.py`
- **Notion API Docs:** https://developers.notion.com/
- **GitHub Actions Docs:** https://docs.github.com/en/actions

---

## Ready to Begin?

Run this command to start:
```bash
setup_notion_integration.bat
```

The wizard will guide you through everything! 🚀

---

*Last Updated: 2025-11-26*
*Status: Ready for setup*


