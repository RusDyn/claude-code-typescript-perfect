export default {
  // TypeScript files - full validation
  '*.ts': [
    // Type check entire project (catches cross-file issues)
    () => 'tsc --noEmit',
    
    // Lint and fix issues
    'eslint --fix --max-warnings=0',
    
    // Format with prettier
    'prettier --write',
    
    // Run related tests
    (filenames) => {
      const tests = filenames
        .map(f => f.replace(/\.ts$/, '.test.ts'))
        .filter(f => require('fs').existsSync(f));
      return tests.length ? `vitest run ${tests.join(' ')}` : true;
    }
  ],
  
  // Other files
  '*.{json,md,yml}': ['prettier --write'],
  
  // Package.json changes
  'package.json': [
    'npm audit --audit-level=moderate',
    () => 'npm run typecheck',
  ],
};