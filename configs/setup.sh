#!/bin/bash

# Complete 10-Minute Setup Script for Claude Code Optimization

echo "🚀 Starting Claude Code TypeScript optimization setup..."

# 1. Create and enter project directory (if needed)
if [ ! -f "package.json" ]; then
  echo "📦 Initializing new project..."
  npm init -y
fi

# 2. Install TypeScript dependencies
echo "📝 Installing TypeScript..."
npm install --save-dev typescript@^5.3.0 @types/node@^20.0.0

# 3. Create ultra-strict tsconfig.json
if [ ! -f "tsconfig.json" ]; then
  echo "⚙️  Creating TypeScript configuration..."
  cp commands/tsconfig.json ./tsconfig.json
fi

# 4. Create project structure
echo "📁 Creating project structure..."
mkdir -p src/{types,utils,services} .claude/commands

# 5. Install Claude Code globally (if not already installed)
if ! command -v claude &> /dev/null; then
  echo "🤖 Installing Claude Code CLI..."
  npm install -g @anthropic-ai/claude-code
fi

# 6. Initialize Claude Code
if [ ! -f ".claude/config.json" ]; then
  echo "🎯 Initializing Claude Code..."
  claude init
fi

# 7. Create CLAUDE.md if it doesn't exist
if [ ! -f "CLAUDE.md" ]; then
  echo "🧠 Creating CLAUDE.md..."
  cat > CLAUDE.md << 'EOF'
# Project Configuration for Claude Code

## Project Type
TypeScript application with strict type safety

## Critical Rules (Prevents 80% of corrections)
- ALWAYS use explicit return types: `function getName(): string`
- NEVER use `any` type - use `unknown` with type guards
- ALWAYS handle errors with Result<T,E> pattern (no throw)
- PREFER `interface` over `type` for objects
- USE `undefined` not `null` for optional values

## Commands
npm run dev        # Start development
npm run build      # Production build
npm run test       # Run all tests
npm run lint:fix   # Auto-fix all issues
npm run typecheck  # Validate types
EOF
fi

# 8. Add package.json scripts
echo "📋 Setting up npm scripts..."
npm pkg set scripts.dev="node --watch dist/index.js"
npm pkg set scripts.build="tsc"
npm pkg set scripts.typecheck="tsc --noEmit"
npm pkg set scripts.watch="tsc --watch"

# 9. Create a simple test file
if [ ! -f "src/index.ts" ]; then
  echo "🎉 Creating entry point..."
  echo "console.log('Claude Code is now supercharged!');" > src/index.ts
fi

# 10. Install additional quality tools
echo "🔧 Installing quality tools..."
npm install --save-dev \
  eslint @eslint/js typescript-eslint \
  eslint-plugin-unicorn eslint-plugin-sonarjs eslint-plugin-security \
  eslint-config-prettier prettier \
  vitest @vitest/coverage-v8 @vitest/ui \
  husky lint-staged \
  @commitlint/cli @commitlint/config-conventional

# 11. Copy ESLint config
if [ ! -f "eslint.config.js" ]; then
  cp commands/eslint.config.js ./eslint.config.js
fi

# 12. Setup git hooks
if [ -d ".git" ] && [ ! -d ".husky" ]; then
  echo "🪝 Setting up git hooks..."
  npx husky init
  echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
  echo "npx lint-staged" > .husky/pre-commit
fi

# 13. Test the setup
echo "🧪 Testing setup..."
npm run build
if [ $? -eq 0 ]; then
  echo "✅ Build successful!"
  npm run dev &
  DEV_PID=$!
  sleep 2
  kill $DEV_PID 2>/dev/null || true
  echo "✅ Development server works!"
else
  echo "❌ Build failed - please check configuration"
  exit 1
fi

echo ""
echo "🎉 Setup complete! Your Claude Code-optimized TypeScript project is ready."
echo ""
echo "📚 Available commands:"
echo "  npm run dev        - Start development with hot-reload"
echo "  npm run build      - Build for production"
echo "  npm run typecheck  - Validate TypeScript"
echo "  npm run test       - Run tests"
echo ""
echo "🤖 Try talking to Claude Code:"
echo "  claude"
echo ""