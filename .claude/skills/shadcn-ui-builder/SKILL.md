---
name: shadcn-ui-builder
description: Build React applications using the full shadcn/ui component library with best practices for code reusability and organization. Use when creating React artifacts, dashboards, forms, data tables, or any UI requiring shadcn/ui components. Focuses on avoiding code duplication through component composition, custom hooks, and reusable patterns. Includes complete component reference, design patterns, and production-ready templates.
---

# shadcn/ui Builder

Comprehensive toolkit for building React applications with shadcn/ui, emphasizing code reusability and clean architecture.

## Related Skills

**Use with:** `design-guide` - For design decisions (colors, spacing, typography) before implementing components. The design-guide skill provides the visual design system while shadcn-ui-builder handles React implementation.

## Core Principles

### 1. Never Duplicate Code

Extract reusable patterns into components, hooks, and utilities.

**❌ Bad:**

```javascript
// Repeated in multiple places
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" />
</div>
```

**✅ Good:**

```javascript
function FormField({ id, label, type, ...props }) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{label}</Label>
      <Input id={id} type={type} {...props} />
    </div>
  );
}

<FormField id="email" label="Email" type="email" />;
```

### 2. Component Composition

Build complex UIs from simple, composable pieces.

```javascript
function SettingsCard({ icon, title, description, action, children }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-4">
          {icon}
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
        </div>
      </CardHeader>
      {children && <CardContent>{children}</CardContent>}
      {action && <CardFooter>{action}</CardFooter>}
    </Card>
  );
}
```

### 3. Custom Hooks for Logic

Extract stateful logic into reusable hooks.

```javascript
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});

  const handleChange = (field) => (e) => {
    setValues((prev) => ({ ...prev, [field]: e.target.value }));
    setErrors((prev) => ({ ...prev, [field]: "" }));
  };

  return { values, errors, handleChange };
}
```

## Quick Start

### Basic Application Structure

```javascript
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function App() {
  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>My Application</CardTitle>
        </CardHeader>
        <CardContent>
          <Button>Click Me</Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

### Import Pattern

All components import from `@/components/ui/[component-name]`:

```javascript
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
```

## Component Categories

### Layout & Structure

- **Card** - Container with header, content, footer sections
- **Accordion** - Collapsible content sections
- **Tabs** - Tabbed navigation interface
- **Separator** - Visual divider
- **ScrollArea** - Custom scrollable container

### Forms & Input

- **Button** - Clickable button (variants: default, destructive, outline, secondary, ghost, link)
- **Input** - Text input field
- **Label** - Form field label
- **Textarea** - Multi-line text input
- **Checkbox** - Boolean checkbox
- **RadioGroup** - Radio button group
- **Select** - Dropdown selection
- **Switch** - Toggle switch
- **Slider** - Numeric slider

### Feedback & Overlay

- **Alert** - Important messages
- **AlertDialog** - Confirmation dialog
- **Dialog** - Modal dialog
- **Popover** - Floating content panel
- **Toast** - Notification message (use with useToast hook)
- **Tooltip** - Hover information
- **Badge** - Status indicator
- **Progress** - Progress bar
- **Skeleton** - Loading placeholder

### Navigation

- **DropdownMenu** - Dropdown menu with items
- **NavigationMenu** - Multi-level navigation
- **Menubar** - Application menu bar
- **ContextMenu** - Right-click menu

### Data Display

- **Table** - Data table with headers
- **Avatar** - User avatar with fallback
- **AspectRatio** - Maintain aspect ratio for media
- **Calendar** - Date picker calendar
- **Command** - Command palette
- **HoverCard** - Hover-triggered card
- **Sheet** - Slide-over panel

## Reference Documentation

### Complete Component Reference

**references/component-library.md** - Full documentation of all shadcn/ui components with:

- Import statements
- Basic usage examples
- All variants and props
- Composition patterns
- Best practices

### Code Organization Guide

**references/code-organization.md** - Strategies for avoiding duplication:

- Component extraction patterns
- Custom hooks for common logic
- Reusable dialog/modal factories
- Form management
- Layout patterns
- Data display patterns
- Project structure recommendations

### Design Patterns

**references/design-patterns.md** - Pre-built UI compositions:

- Authentication (login, signup, profile)
- Dashboards (stats, activity feeds, charts)
- Data management (tables with filters, CRUD operations, kanban)
- Settings panels
- Navigation (sidebar, top nav)
- E-commerce (product cards, checkout)
- Multi-step forms

## Production Templates

### Dashboard Template

**assets/templates/dashboard-template.jsx**

- Complete dashboard layout
- Stats cards
- Tabbed navigation
- Responsive grid
- Recent activity feed
- Ready to customize

### Data Table with CRUD

**assets/templates/data-table-crud.jsx**

- Full CRUD operations (Create, Read, Update, Delete)
- Search and filtering
- Bulk selection and actions
- Edit dialog
- Responsive table
- Reusable form component

## Common Patterns

### Form with Validation

```javascript
function LoginForm() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};
    if (!formData.email.includes("@")) newErrors.email = "Invalid email";
    if (formData.password.length < 6) newErrors.password = "Too short";

    if (Object.keys(newErrors).length === 0) {
      // Submit form
    } else {
      setErrors(newErrors);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <form onSubmit={handleSubmit}>
        <CardHeader>
          <CardTitle>Login</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
            />
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email}</p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={formData.password}
              onChange={(e) =>
                setFormData({ ...formData, password: e.target.value })
              }
            />
            {errors.password && (
              <p className="text-sm text-destructive">{errors.password}</p>
            )}
          </div>
        </CardContent>
        <CardFooter>
          <Button type="submit" className="w-full">
            Sign In
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
```

### Data Table with Actions

```javascript
function UserTable({ users }) {
  const [search, setSearch] = useState("");

  const filtered = users.filter((u) =>
    u.name.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="space-y-4">
      <Input
        placeholder="Search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="max-w-sm"
      />

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <Badge>{user.status}</Badge>
                </TableCell>
                <TableCell>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="sm">
                        •••
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                      <DropdownMenuItem>Edit</DropdownMenuItem>
                      <DropdownMenuItem>Delete</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
```

### Reusable Confirm Dialog

```javascript
function ConfirmDialog({ trigger, title, description, onConfirm }) {
  const [open, setOpen] = useState(false);

  return (
    <AlertDialog open={open} onOpenChange={setOpen}>
      <AlertDialogTrigger asChild>{trigger}</AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{title}</AlertDialogTitle>
          <AlertDialogDescription>{description}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={() => {
              onConfirm();
              setOpen(false);
            }}
          >
            Confirm
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

// Usage
<ConfirmDialog
  trigger={<Button variant="destructive">Delete</Button>}
  title="Delete Item"
  description="This action cannot be undone."
  onConfirm={() => handleDelete(item.id)}
/>;
```

## Best Practices

### Styling

1. Use Tailwind utility classes
2. Apply `className` prop to all components
3. Use consistent spacing (`space-y-4`, `gap-4`)
4. Responsive design with `md:`, `lg:` prefixes

### Accessibility

1. Always use `Label` with form inputs
2. Use `asChild` for custom triggers: `<DialogTrigger asChild><Button>Open</Button></DialogTrigger>`
3. Provide descriptive button text
4. Use semantic HTML elements

### Performance

1. Extract frequently used components
2. Use React.memo for expensive renders
3. Avoid inline function definitions in props
4. Keep component trees shallow

### Code Organization

1. Extract components used 3+ times
2. Create custom hooks for stateful logic
3. Use compound components for complex UIs
4. Keep business logic separate from presentation

## Anti-Patterns to Avoid

❌ Don't copy-paste component blocks
❌ Don't hardcode values that could be props
❌ Don't create overly specific components
❌ Don't nest too deeply (>3 levels)
❌ Don't repeat styling patterns
❌ Don't mix presentation and business logic
❌ Don't forget error and loading states

## Workflow

1. **Identify the UI need** - What are you building?
2. **Check references** - Look in component-library.md and design-patterns.md
3. **Use templates** - Start with dashboard-template or data-table-crud
4. **Extract patterns** - If repeating code 3+ times, extract it
5. **Compose components** - Build complex UIs from simple pieces
6. **Add custom hooks** - Extract stateful logic
7. **Test responsiveness** - Ensure mobile/tablet/desktop work

## Quick Reference

**Common Imports:**

```javascript
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
```

**Button Variants:**
`default`, `destructive`, `outline`, `secondary`, `ghost`, `link`

**Badge Variants:**
`default`, `secondary`, `destructive`, `outline`

**Always provide `asChild` for custom triggers:**

```javascript
<DialogTrigger asChild>
  <Button>Open</Button>
</DialogTrigger>
```

This skill enables building production-quality React UIs with minimal code duplication.
