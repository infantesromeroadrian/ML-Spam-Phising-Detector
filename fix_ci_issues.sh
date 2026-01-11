#!/bin/bash

# Script to fix CI issues

echo "🔧 Fixing CI/CD issues..."

# 1. Fix Ruff B904 errors (raise from)
echo "📝 Fixing exception chaining..."
sed -i 's/raise typer.Exit(1)/raise typer.Exit(1) from None/g' src/backend/spam_detector/infrastructure/cli/commands.py

# 2. Ensure assets directory is not empty
echo "📁 Adding placeholder to assets..."
echo "# Keep this directory in git" > src/frontend/assets/.gitkeep

# 3. Fix pytest issues - ensure models directory is available
echo "📦 Checking models directory..."
if [ ! -d "models" ]; then
    echo "❌ Models directory not found!"
else
    echo "✅ Models directory exists"
fi

# 4. Disable some ruff rules that are too strict for FastAPI
echo "🔧 Updating ruff config..."
cat >> src/backend/pyproject.toml << 'EOF'

[tool.ruff.lint.per-file-ignores]
"**/api/routers/*.py" = ["B008"]  # Allow function calls in argument defaults (FastAPI Depends)
EOF

echo "✅ Fixes applied!"
echo ""
echo "Next steps:"
echo "1. Review changes: git diff"
echo "2. Commit: git add -A && git commit -m 'fix: resolve CI/CD issues'"
echo "3. Push: git push origin main"