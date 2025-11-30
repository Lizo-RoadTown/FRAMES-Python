# GitHub-Notion Integration Setup Guide

## Overview

Your FRAMES project has **automated bidirectional sync** between GitHub and Notion:
- **GitHub Issues** ↔ **Notion Tasks** (bidirectional)
- **GitHub Documentation** → **Notion Pages** (one-way sync)

## Current Configuration Status

✅ **Already Configured:**
- Notion API key in `.env` file
- GitHub Actions workflows (`.github/workflows/`)
- Python sync scripts (`scripts/`)
- Repository structure ready

🔧 **Needs Configuration:**
1. GitHub repository secrets
2. Notion workspace setup (databases and parent pages)
3. Initial sync execution
4. Team onboarding documentation

---

## Step-by-Step Setup

### Step 1: Set Up Notion Workspace

#### 1.1 Create Parent Page in Notion
1. Open Notion and create a new page titled **"FRAMES Project Hub"**
2. This will be the parent page for all automated content
3. Copy the page ID from the URL:
   ```
   https://www.notion.so/FRAMES-Project-Hub-<THIS_IS_THE_PAGE_ID>
   ```
   Example: `2b76b8ea578a8040b328c8527dedea93`

#### 1.2 Share Page with Integration
1. Click **"Share"** button (top right of the page)
2. Click **"Invite"** 
3. Search for **"FRAMES"** (your integration name)
4. Select it and grant access
5. Wait ~30 seconds for permissions to propagate

#### 1.3 Run Workspace Creation Script
This creates 4 databases and documentation pages automatically:

```bash
cd "c:\Users\LizO5\FRAMES Python"
python scripts\create_notion_workspace.py <YOUR_PAGE_ID>
```

**Created Databases:**
- ✅ **Development Tasks** - Track roadmap and issues
- ⚙️ **Technical Decisions** - Document architecture choices
- 🔗 **Integration Checklist** - Monitor third-party integrations
- 📚 **Module Library** - Catalog learning modules

**Created Pages:**
- 📘 **Project Overview** - Rich formatted project summary

#### 1.4 Copy Database IDs
After running the script, it will output database IDs. Copy the **Tasks Database ID** for the next step.

---

### Step 2: Configure GitHub Secrets

Your GitHub Actions need these secrets to access Notion:

#### 2.1 Go to GitHub Repository Settings
1. Navigate to: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/settings/secrets/actions
2. Click **"New repository secret"**

#### 2.2 Add Required Secrets

| Secret Name | Value | Description |
|------------|-------|-------------|
| `NOTION_API_KEY` | `<YOUR_NOTION_TOKEN>` | Your Notion integration token |
| `NOTION_TASKS_DB_ID` | (from workspace script output) | Tasks database ID |
| `NOTION_PARENT_PAGE_ID` | (your parent page ID) | FRAMES Project Hub page ID |

**How to add each secret:**
1. Click "New repository secret"
2. Enter name exactly as shown above
3. Paste the value
4. Click "Add secret"
5. Repeat for all 3 secrets

---

### Step 3: Test the Integration

#### 3.1 Test Notion Connection Locally
```bash
cd "c:\Users\LizO5\FRAMES Python"
python scripts\test_notion_access.py
```

Expected output:
```
[OK] Authenticated as: FRAMES
[OK] Successfully accessed page!
```

#### 3.2 Run Manual Sync Test
```bash
# Test documentation sync
python scripts\sync_notion.py <YOUR_PARENT_PAGE_ID>

# Test task sync (requires GitHub secrets configured)
python scripts\notion_github_sync.py
```

#### 3.3 Trigger GitHub Actions Manually
1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions
2. Select **"Notion-GitHub Task Sync"** workflow
3. Click **"Run workflow"** → **"Run workflow"** button
4. Check the workflow logs for success

---

### Step 4: Verify Automation

#### Automated Triggers

**Task Sync Workflow** (`notion-github-sync.yml`):
- ⏰ Runs every 6 hours automatically
- 🔄 Runs on every push to main/master
- 🖱️ Can be triggered manually

**What it does:**
- Creates GitHub issues for Notion tasks without links
- Creates Notion tasks for GitHub issues with `notion-sync` label
- Marks Notion tasks "Done" when GitHub issue is closed
- Marks Notion tasks "In Progress" when GitHub issue is open
- Flags overdue tasks

**Documentation Sync Workflow** (`sync-notion.yml`):
- 📝 Runs when files in `docs/` are changed
- 📝 Runs when database models change
- 📝 Runs when backend code changes
- 🖱️ Can be triggered manually

**What it does:**
- Syncs all markdown documentation to Notion pages
- Converts markdown to Notion blocks (headers, lists, code)
- Updates existing pages or creates new ones

---

### Step 5: Using the Integration

#### Create a Task in Notion
1. Open your **Development Tasks** database
2. Click **"New"** to create a task
3. Fill in:
   - **Task name**
   - **Phase** (which development phase)
   - **Status** (Not Started, In Progress, etc.)
   - **Priority**
   - Leave **GitHub Issue URL** blank
4. Save

**Result:** On the next sync (max 6 hours), a GitHub issue will be created automatically and linked!

#### Create a GitHub Issue
1. Create an issue in GitHub
2. Add the label **`notion-sync`**
3. Submit

**Result:** A Notion task will be created automatically in your Tasks database!

#### Update Documentation
1. Edit any file in `docs/` folder
2. Commit and push to GitHub
3. GitHub Action runs automatically
4. Check Notion - pages are updated!

---

### Step 6: Team Onboarding

Share this workflow with your team:

#### For Team Members Using Notion:
1. Create tasks in the **Development Tasks** database
2. Set status, priority, and phase
3. Tasks automatically sync to GitHub Issues
4. When developers close the issue, task status updates to "Done" automatically

#### For Developers Using GitHub:
1. Create issues normally in GitHub
2. Add `notion-sync` label for project tracking
3. Issue appears in Notion for project managers
4. Closing issue automatically updates Notion status

#### For Documentation Writers:
1. Edit markdown files in `docs/` folder
2. Commit to GitHub
3. Documentation automatically publishes to Notion
4. Non-technical team can read in Notion's beautiful interface

---

## Troubleshooting

### "Cannot access page" Error
**Solution:** Make sure you shared the Notion page with the FRAMES integration:
1. Open the page in Notion
2. Click "Share" → "Invite"
3. Add the FRAMES integration
4. Wait 30 seconds

### "Authentication failed" Error
**Solution:** Check that `NOTION_API_KEY` in `.env` is correct and matches GitHub secret.

### Sync Not Running Automatically
**Solution:**
1. Check GitHub Actions tab for errors
2. Verify all 3 secrets are configured correctly
3. Check workflow files are in `.github/workflows/`

### Tasks Not Syncing
**Solution:**
1. Ensure GitHub issues have the `notion-sync` label
2. Ensure Tasks database has the correct property names
3. Check GitHub Action logs for specific errors

---

## Configuration Files Reference

### Environment Variables (`.env`)
```env
NOTION_API_KEY=your_notion_api_key
NOTION_PARENT_PAGE_ID=your_parent_page_id
NOTION_TASKS_DB_ID=your_tasks_database_id
```

### GitHub Secrets Required
- `NOTION_API_KEY`
- `NOTION_TASKS_DB_ID`
- `NOTION_PARENT_PAGE_ID`
- `GITHUB_TOKEN` (automatically provided by GitHub)

### Workflow Files
- `.github/workflows/notion-github-sync.yml` - Task synchronization
- `.github/workflows/sync-notion.yml` - Documentation sync

### Script Files
- `scripts/notion_github_sync.py` - Bidirectional task sync logic
- `scripts/sync_notion.py` - Documentation sync logic
- `scripts/create_notion_workspace.py` - Workspace setup
- `scripts/test_notion_access.py` - Connection testing

---

## Best Practices

### Workflow Direction Recommendations

**GitHub → Notion (Best for):**
- Source code documentation
- Technical specifications
- API references
- Architecture decisions that live in code

**Notion → GitHub (Best for):**
- High-level project planning
- Feature requests from non-technical stakeholders
- Roadmap items
- Task assignments for cross-functional teams

**Bidirectional (Already Configured):**
- Task/issue tracking
- Project status updates
- Development workflow coordination

### Labeling Strategy

Use GitHub labels to control what syncs:
- `notion-sync` - Syncs to Notion automatically
- `internal-only` - Stays in GitHub only
- `notion-created` - Came from Notion (auto-applied)

### Database Property Naming

The sync scripts expect these exact property names in Notion:
- **Task** (title field)
- **Status** (status field)
- **GitHub Issue URL** (URL field)
- **Due** (date field)

Don't rename these or sync will break!

---

## Advanced Configuration

### Custom Sync Schedule

Edit `.github/workflows/notion-github-sync.yml`:
```yaml
schedule:
  - cron: "0 */6 * * *"  # Every 6 hours (change as needed)
```

### Add Custom Task Properties

Edit `scripts/create_notion_workspace.py` to add fields to the Tasks database.

### Filter What Syncs

Edit `scripts/notion_github_sync.py` to add filters:
```python
# Only sync issues with specific labels
SYNC_LABEL = "notion-sync"

# Only sync to specific repository
DEFAULT_REPO = "YOUR_ORG/YOUR_REPO"
```

---

## Quick Reference Commands

```bash
# Test Notion connection
python scripts\test_notion_access.py

# Create Notion workspace
python scripts\create_notion_workspace.py <PAGE_ID>

# Sync documentation manually
python scripts\sync_notion.py <PARENT_PAGE_ID>

# Sync tasks manually (needs GitHub secrets in env)
python scripts\notion_github_sync.py

# Check workflow status
# Visit: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

---

## Summary Checklist

- [ ] Created FRAMES Project Hub page in Notion
- [ ] Shared page with FRAMES integration
- [ ] Ran workspace creation script
- [ ] Copied Tasks Database ID
- [ ] Added 3 GitHub secrets (NOTION_API_KEY, NOTION_TASKS_DB_ID, NOTION_PARENT_PAGE_ID)
- [ ] Tested connection with test script
- [ ] Manually triggered GitHub Actions to verify
- [ ] Created test task in Notion
- [ ] Created test issue in GitHub with `notion-sync` label
- [ ] Verified bidirectional sync works
- [ ] Documented workflow for team

---

## Support

- **Integration Issues:** Check GitHub Actions logs
- **Notion API:** https://developers.notion.com/
- **Project Questions:** eosborn@cpp.edu

*Last Updated: 2025-11-26*


