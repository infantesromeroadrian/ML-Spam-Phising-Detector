#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔒 Configurando Branch Protection Rules${NC}"

if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) no está instalado${NC}"
    echo "Instala con: brew install gh (macOS) o https://cli.github.com/"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠️ No estás autenticado en GitHub CLI${NC}"
    echo "Ejecuta: gh auth login"
    exit 1
fi

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo -e "${GREEN}📦 Repositorio: ${REPO}${NC}"

echo -e "\n${YELLOW}Configurando protección para rama 'main'...${NC}"

gh api repos/${REPO}/branches/main/protection \
  --method PUT \
  --header "Accept: application/vnd.github+json" \
  --header "X-GitHub-Api-Version: 2022-11-28" \
  --field required_status_checks='{"strict": true, "contexts": ["lint", "type-check", "test-unit", "test-integration", "test-e2e", "security"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"dismissal_restrictions": {}, "dismiss_stale_reviews": true, "require_code_owner_reviews": true, "required_approving_review_count": 1, "require_last_push_approval": true}' \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field required_conversation_resolution=true

echo -e "${GREEN}✅ Rama 'main' protegida${NC}"

gh api repos/${REPO} \
  --method PATCH \
  --field allow_auto_merge=true \
  --field allow_squash_merge=true \
  --field delete_branch_on_merge=true

echo -e "${GREEN}✅ Auto-merge configurado${NC}"

cat > .github/CODEOWNERS << 'EOF'
# Default code owners for everything
* @adrianinfantes

# Python backend
/src/backend/ @adrianinfantes
*.py @adrianinfantes

# Frontend
/src/frontend/ @adrianinfantes

# ML Models
/models/ @adrianinfantes

# CI/CD
/.github/ @adrianinfantes

# Documentation
*.md @adrianinfantes
/docs/ @adrianinfantes
EOF

echo -e "${GREEN}✅ CODEOWNERS creado${NC}"
echo -e "\n${GREEN}🎉 Branch Protection configurado con éxito!${NC}"
echo -e "${YELLOW}📝 Nota: Ajusta @adrianinfantes en CODEOWNERS a tu username de GitHub${NC}"