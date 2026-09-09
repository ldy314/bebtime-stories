#!/bin/bash
# ============================================================
# GitHub 仓库一键设置脚本
# 使用前请先运行: gh auth login
# ============================================================

set -e

REPO_NAME="bedtime-stories"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Add gh to PATH if not found
if ! command -v gh &> /dev/null; then
  export PATH="$PATH:/c/Program Files/GitHub CLI"
fi

# Verify gh is installed
if ! command -v gh &> /dev/null; then
  echo "ERROR: gh CLI not found. Please install it first:"
  echo "  choco install gh -y"
  exit 1
fi

# Check auth
echo "=== Checking GitHub authentication ==="
if ! gh auth status &> /dev/null; then
  echo "ERROR: You are not logged in to GitHub."
  echo "Please run: gh auth login"
  echo "Follow the prompts to authenticate (choose GitHub.com -> HTTPS -> Login with browser)."
  exit 1
fi

echo "Authenticated as: $(gh api user --jq .login)"

# Create repo and push
echo ""
echo "=== Creating GitHub repository: $REPO_NAME ==="
cd "$PROJECT_DIR"

# Check if repo already exists
USERNAME=$(gh api user --jq .login)
if gh repo view "$USERNAME/$REPO_NAME" &> /dev/null 2>&1; then
  echo "Repository $USERNAME/$REPO_NAME already exists."
  echo "Pushing files to existing repo..."
  git remote remove origin 2>/dev/null || true
  git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"
  git push -u origin main --force
else
  echo "Creating new public repository..."
  gh repo create "$REPO_NAME" --public --source=. --push
fi

echo ""
echo "Repository created: https://github.com/$USERNAME/$REPO_NAME"

# Set up Zhipu API key secret
echo ""
echo "=== DeepSeek API Key ==="
echo "To generate stories, you need a DeepSeek API key."
echo "Get one at: https://platform.deepseek.com"
echo ""
read -p "Do you have a DeepSeek API key? (y/n): " HAS_KEY

if [[ "$HAS_KEY" == "y" || "$HAS_KEY" == "Y" ]]; then
  read -s -p "Paste your API key: " API_KEY
  echo ""
  echo "Setting DEEPSEEK_API_KEY secret..."
  echo "$API_KEY" | gh secret set DEEPSEEK_API_KEY --repo "$USERNAME/$REPO_NAME"
  echo "Secret set successfully!"
else
  echo "Skipping secret setup. You can set it later:"
  echo "  echo 'YOUR_KEY' | gh secret set DEEPSEEK_API_KEY --repo $USERNAME/$REPO_NAME"
fi

# Enable GitHub Pages
echo ""
echo "=== Enabling GitHub Pages ==="
gh api "repos/$USERNAME/$REPO_NAME/pages" \
  -X POST \
  -f "source[branch]=main" \
  -f "source[path]=/" \
  2>/dev/null || echo "Pages may already be enabled or need manual setup."

# Get Pages URL
echo ""
echo "=== Waiting for Pages to build (this may take 1-2 minutes) ==="
sleep 5

PAGES_URL=$(gh api "repos/$USERNAME/$REPO_NAME/pages" --jq '.html_url' 2>/dev/null || echo "")

if [ -z "$PAGES_URL" ]; then
  PAGES_URL="https://$(echo $USERNAME | tr '[:upper:]' '[:lower:]').github.io/$REPO_NAME/"
fi

echo ""
echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
echo "GitHub Pages URL: $PAGES_URL"
echo "  (may take a few minutes to be available)"
echo ""
echo "GitHub Repo:      https://github.com/$USERNAME/$REPO_NAME"
echo ""
echo "Next steps:"
echo "  1. Wait 2-3 minutes, then open the Pages URL"
echo "  2. Test the Action: go to the repo -> Actions -> Run workflow"
echo "  3. Set up phone shortcut (see README.md)"
echo ""
echo "To manually trigger story generation from command line:"
echo "  gh workflow run generate-stories.yml --repo $USERNAME/$REPO_NAME"
echo ""
