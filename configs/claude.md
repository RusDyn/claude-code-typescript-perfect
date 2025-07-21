# CLAUDE.md - Project Intelligence File

## Project Overview
**Name**: [Your Project Name]
**Type**: TypeScript Microservice / React App / CLI Tool
**Stage**: Development / Production
**Team Size**: [Number] developers

## Architecture (CRITICAL - Shapes all responses)
- **Pattern**: Monolith / Microservices / Serverless
- **Database**: PostgreSQL with Prisma ORM
- **API Style**: REST / GraphQL / tRPC
- **Auth**: JWT / OAuth2 / Session-based

## Code Standards (Reduces corrections by 80%)

### TypeScript Mandates
1. **Explicit return types** on ALL functions
2. **No `any` type** - use `unknown` with guards
3. **Result<T,E> pattern** for errors (no throw)
4. **Readonly** for all props interfaces
5. **Branded types** for domain primitives

### Naming Conventions
- Files: `kebab-case.ts`
- Interfaces: `PascalCase` (no I prefix)
- Types: `PascalCase`
- Functions: `camelCase`
- Constants: `UPPER_SNAKE_CASE`

### Import Order (Auto-enforced)
1. Node built-ins
2. External packages
3. Internal aliases (@/...)
4. Relative imports
5. Type imports last

## Common Commands
```bash
npm run dev        # Start with hot-reload
npm run build      # Type-check + compile
npm run test       # Run test suite
npm run lint:fix   # Fix all auto-fixable issues
npm run typecheck  # Validate types only
npm run quality    # Full quality check
```

## Project Structure
```
src/
├── types/       # Shared TypeScript types
├── services/    # Business logic
├── utils/       # Helper functions
├── api/         # API routes/handlers
└── index.ts     # Entry point
```

## Error Handling Pattern
```typescript
// ALWAYS use this pattern, never throw
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

// Example usage
async function getUser(id: string): Promise<Result<User>> {
  const user = await findById(id);
  if (!user) {
    return { success: false, error: new NotFoundError('User', id) };
  }
  return { success: true, data: user };
}
```

## Testing Requirements
- Unit tests for all business logic (>80% coverage)
- Integration tests for API endpoints
- Use describe/it pattern
- Mock external services

## Performance Budgets
- Build time: <30 seconds
- Test suite: <60 seconds  
- Bundle size: <500KB gzipped
- First paint: <1.5 seconds

## Security Patterns
- Input validation with Zod
- SQL injection prevention via Prisma
- XSS prevention (DOMPurify for user content)
- Rate limiting on all endpoints

## Debugging Approach
1. Reproduce with minimal test case
2. Check error logs first
3. Use debugger, not console.log
4. Write test to catch regression

## DO NOT (Common mistakes)
- ❌ Use `as` type assertions without validation
- ❌ Disable TypeScript errors with @ts-ignore
- ❌ Mix async/await with .then()
- ❌ Mutate function parameters
- ❌ Use `var` or undeclared variables
- ❌ Ignore error handling

## External Services
- Sentry for error tracking
- DataDog for metrics
- GitHub Actions for CI/CD
- Vercel for deployment