# CLAUDE.md - Indie Developer Project Intelligence

## Project Context
**Team Size**: 1-3 developers (or non-developers using Claude Code)
**Architecture**: Monolith with clean separation
**Database**: PostgreSQL (simple setup)
**API**: REST with TypeScript
**Auth**: JWT tokens (keep it simple)
**Deployment**: Single server or Vercel/Netlify

## TypeScript Standards That Matter

### Essential Rules
- Explicit return types on exported functions
- `strict: true` in tsconfig.json
- No `any` types - use `unknown` with type guards
- Use built-in utility types: `Pick`, `Omit`, `Partial`

### Patterns Claude Code Handles Best
```typescript
// Standard async/await pattern
async function getUser(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
}

// Simple API response structure
interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// Clean interface patterns
interface User {
  readonly id: string;
  readonly email: string;
  readonly name: string;
  readonly createdAt: string;
}

type CreateUser = Omit<User, 'id' | 'createdAt'>;
type UpdateUser = Partial<Pick<User, 'name' | 'email'>>;
```

## Project Structure
```
src/
├── types/          # Shared TypeScript types
├── utils/          # Helper functions
├── api/            # API routes/handlers  
├── components/     # React components (if applicable)
├── pages/          # Route handlers
└── index.ts        # Entry point
```

## Quality Checks
```bash
# These run automatically via git hooks
npm run typecheck   # TypeScript validation
npm run lint        # ESLint fixes
npm run test        # Unit tests
npm run build       # Production build
```

## Error Handling Strategy
```typescript
// Keep error handling simple and predictable
async function saveUser(user: CreateUser): Promise<{ success: boolean; error?: string }> {
  try {
    const result = await db.user.create({ data: user });
    return { success: true };
  } catch (error) {
    console.error('Save user failed:', error);
    return { success: false, error: 'Failed to save user' };
  }
}

// For APIs, consistent error responses
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('API Error:', error);
  res.status(500).json({
    success: false,
    message: process.env.NODE_ENV === 'development' ? error.message : 'Internal error'
  });
});
```

## Testing Approach
- **Unit tests**: Test your functions (aim for 80%+ coverage)
- **Integration tests**: Test API endpoints
- **Keep it simple**: Don't over-test, focus on business logic

```typescript
// Simple, effective test patterns
describe('getUser', () => {
  test('returns user when found', async () => {
    const user = await getUser('123');
    expect(user).toMatchObject({ id: '123' });
  });

  test('returns null when not found', async () => {
    const user = await getUser('nonexistent');
    expect(user).toBeNull();
  });
});
```

## Development Workflow
```bash
npm run dev         # Start development server
npm run test:watch  # Run tests in watch mode
npm run build       # Build for production
npm run start       # Start production server
```

## Security Essentials
- Validate all inputs with Zod schemas
- Use parameterized queries (Prisma handles this)
- Hash passwords with bcrypt
- Validate JWT tokens properly
- Rate limit API endpoints (express-rate-limit)

## Performance Guidelines
- Bundle size target: <500KB gzipped
- API responses: <500ms for most endpoints
- Database queries: Use indexes for common queries
- Images: Compress and use WebP when possible

## Common Commands
```bash
# Database
npm run db:migrate  # Apply database changes
npm run db:seed     # Add sample data

# Development
npm run lint:fix    # Fix linting issues
npm run type:check  # Check types only
npm run clean       # Clean build artifacts
```

## Tools That Help Claude Code
- **ESLint**: Catches issues before Claude Code sees them
- **Prettier**: Consistent formatting
- **Husky**: Git hooks for quality
- **TypeScript strict mode**: Better error catching
- **Simple folder structure**: Easy for Claude Code to navigate

## What to Avoid
- Complex architectural patterns (microservices, CQRS, event sourcing)
- Custom build tools (stick to Vite, Next.js, or similar)
- Over-engineering (YAGNI principle)
- Deep inheritance hierarchies
- Overly complex type manipulations

---

*Optimized for solo developers and small teams using Claude Code for maximum productivity with minimal complexity.*