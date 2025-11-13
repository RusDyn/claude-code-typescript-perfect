# Code Organization & Reusability

Best practices for avoiding code duplication and maintaining clean React components with shadcn/ui.

## Component Composition Strategy

### 1. Extract Common Patterns

**❌ Bad - Duplicated Code:**

```javascript
// Repeated form fields in multiple places
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" placeholder="Enter email" />
</div>

<div className="space-y-2">
  <Label htmlFor="name">Name</Label>
  <Input id="name" type="text" placeholder="Enter name" />
</div>
```

**✅ Good - Reusable Component:**

```javascript
function FormField({ id, label, type = "text", placeholder, value, onChange }) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{label}</Label>
      <Input
        id={id}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
    </div>
  )
}

// Usage
<FormField id="email" label="Email" type="email" placeholder="Enter email" />
<FormField id="name" label="Name" placeholder="Enter name" />
```

### 2. Create Compound Components

**Pattern: Card-based layouts**

```javascript
function SettingsCard({ icon, title, description, action, children }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-4">
          {icon && <div className="text-2xl">{icon}</div>}
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
        </div>
      </CardHeader>
      {children && <CardContent>{children}</CardContent>}
      {action && <CardFooter>{action}</CardFooter>}
    </Card>
  )
}

// Reuse everywhere
;<SettingsCard
  icon="🔔"
  title="Notifications"
  description="Manage your notification preferences"
  action={<Button>Save Changes</Button>}
>
  <Switch id="email-notifications" />
  <Label htmlFor="email-notifications">Email notifications</Label>
</SettingsCard>
```

### 3. Dialog/Modal Factory

**❌ Bad - Repeated Dialog Structure:**

```javascript
// Each dialog repeats the same structure
<Dialog>
  <DialogTrigger asChild>
    <Button>Delete</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Delete Item</DialogTitle>
      <DialogDescription>Are you sure?</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button variant="destructive">Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

**✅ Good - Reusable Dialog:**

```javascript
function ConfirmDialog({
  trigger,
  title,
  description,
  confirmText = 'Confirm',
  confirmVariant = 'default',
  onConfirm,
}) {
  const [open, setOpen] = useState(false)

  const handleConfirm = () => {
    onConfirm?.()
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button variant={confirmVariant} onClick={handleConfirm}>
            {confirmText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

// Usage
;<ConfirmDialog
  trigger={<Button variant="destructive">Delete</Button>}
  title="Delete Item"
  description="This action cannot be undone."
  confirmText="Delete"
  confirmVariant="destructive"
  onConfirm={() => handleDelete(item.id)}
/>
```

## State Management Patterns

### 4. Custom Hooks for Common Logic

**Extract form logic:**

```javascript
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})

  const handleChange = field => e => {
    setValues(prev => ({ ...prev, [field]: e.target.value }))
    setErrors(prev => ({ ...prev, [field]: '' }))
  }

  const validate = rules => {
    const newErrors = {}
    Object.keys(rules).forEach(field => {
      const error = rules[field](values[field])
      if (error) newErrors[field] = error
    })
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  return { values, errors, handleChange, validate, setValues }
}

// Usage in any form
function LoginForm() {
  const { values, errors, handleChange, validate } = useForm({
    email: '',
    password: '',
  })

  const handleSubmit = () => {
    if (
      validate({
        email: v => (!v.includes('@') ? 'Invalid email' : null),
        password: v => (v.length < 6 ? 'Too short' : null),
      })
    ) {
      // Submit form
    }
  }

  return (
    <div className="space-y-4">
      <FormField
        label="Email"
        value={values.email}
        onChange={handleChange('email')}
        error={errors.email}
      />
      <FormField
        label="Password"
        type="password"
        value={values.password}
        onChange={handleChange('password')}
        error={errors.password}
      />
      <Button onClick={handleSubmit}>Login</Button>
    </div>
  )
}
```

### 5. Toast Notification Hook

```javascript
function useNotification() {
  const { toast } = useToast()

  return {
    success: message =>
      toast({
        title: 'Success',
        description: message,
      }),
    error: message =>
      toast({
        title: 'Error',
        description: message,
        variant: 'destructive',
      }),
    info: message =>
      toast({
        title: 'Info',
        description: message,
      }),
  }
}

// Usage
function Component() {
  const notify = useNotification()

  const handleSave = async () => {
    try {
      await saveData()
      notify.success('Data saved successfully')
    } catch (error) {
      notify.error('Failed to save data')
    }
  }
}
```

## Layout Patterns

### 6. Consistent Page Layouts

```javascript
function PageLayout({ title, description, actions, children }) {
  return (
    <div className="container mx-auto py-8 space-y-8">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">{title}</h1>
          {description && (
            <p className="text-muted-foreground mt-2">{description}</p>
          )}
        </div>
        {actions && <div className="flex gap-2">{actions}</div>}
      </div>
      {children}
    </div>
  )
}

// Reuse for all pages
;<PageLayout
  title="Dashboard"
  description="Welcome back"
  actions={
    <>
      <Button variant="outline">Export</Button>
      <Button>Create New</Button>
    </>
  }
>
  <div className="grid grid-cols-3 gap-4">{/* Page content */}</div>
</PageLayout>
```

### 7. Grid System for Cards

```javascript
function CardGrid({ children, cols = 3 }) {
  const colClasses = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  }

  return <div className={`grid ${colClasses[cols]} gap-6`}>{children}</div>
}

// Usage
;<CardGrid cols={3}>
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</CardGrid>
```

## Data Display Patterns

### 8. Reusable Table with Actions

```javascript
function DataTable({
  data,
  columns,
  actions,
  emptyMessage = 'No data available',
}) {
  if (data.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        {emptyMessage}
      </div>
    )
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          {columns.map(col => (
            <TableHead key={col.key}>{col.label}</TableHead>
          ))}
          {actions && <TableHead>Actions</TableHead>}
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((row, i) => (
          <TableRow key={i}>
            {columns.map(col => (
              <TableCell key={col.key}>
                {col.render ? col.render(row[col.key], row) : row[col.key]}
              </TableCell>
            ))}
            {actions && <TableCell>{actions(row)}</TableCell>}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

// Usage
;<DataTable
  data={users}
  columns={[
    { key: 'name', label: 'Name' },
    { key: 'email', label: 'Email' },
    {
      key: 'status',
      label: 'Status',
      render: value => <Badge>{value}</Badge>,
    },
  ]}
  actions={user => (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm">
          •••
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem onClick={() => editUser(user)}>Edit</DropdownMenuItem>
        <DropdownMenuItem onClick={() => deleteUser(user)}>
          Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )}
/>
```

### 9. Status Badge Helper

```javascript
function StatusBadge({ status }) {
  const variants = {
    active: { variant: 'default', label: 'Active' },
    pending: { variant: 'secondary', label: 'Pending' },
    inactive: { variant: 'outline', label: 'Inactive' },
    error: { variant: 'destructive', label: 'Error' }
  }

  const config = variants[status] || variants.inactive

  return <Badge variant={config.variant}>{config.label}</Badge>
}

// Usage
<StatusBadge status="active" />
<StatusBadge status="error" />
```

## Form Patterns

### 10. Select with Search

```javascript
function SearchableSelect({
  options,
  value,
  onChange,
  placeholder = 'Select option',
  searchPlaceholder = 'Search...',
}) {
  const [search, setSearch] = useState('')

  const filtered = options.filter(opt =>
    opt.label.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-full justify-between">
          {value ? options.find(o => o.value === value)?.label : placeholder}
          <ChevronDown className="ml-2 h-4 w-4" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0">
        <Command>
          <CommandInput
            placeholder={searchPlaceholder}
            value={search}
            onValueChange={setSearch}
          />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup>
              {filtered.map(option => (
                <CommandItem
                  key={option.value}
                  value={option.value}
                  onSelect={() => {
                    onChange(option.value)
                  }}
                >
                  {option.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
```

## Best Practices Summary

1. **Component Extraction**: If you use the same pattern 3+ times, extract it
2. **Props Interface**: Define clear, consistent prop interfaces
3. **Composition**: Build complex UIs from simple, reusable pieces
4. **Custom Hooks**: Extract stateful logic into custom hooks
5. **Layout Components**: Create consistent page/section layouts
6. **Helper Functions**: Extract rendering logic into utility functions
7. **Default Props**: Provide sensible defaults to reduce boilerplate
8. **Children Pattern**: Use `children` prop for flexible composition
9. **Render Props**: Use render props for customizable sections
10. **Type Safety**: Document expected props with JSDoc comments

## Anti-Patterns to Avoid

❌ **Don't copy-paste large component blocks**
❌ **Don't hardcode values that could be props**
❌ **Don't create overly specific components**
❌ **Don't nest too many levels (>3 is usually too much)**
❌ **Don't mix presentation and business logic**
❌ **Don't repeat styling patterns (use Tailwind utilities)**
❌ **Don't create components that do too much**
❌ **Don't forget to handle loading/error states consistently**

## Project Structure

```
/components
  /ui              # shadcn components (don't modify)
  /common          # Reusable app components
    - FormField.jsx
    - DataTable.jsx
    - PageLayout.jsx
    - ConfirmDialog.jsx
  /features        # Feature-specific components
    /dashboard
    /users
    /settings
  /hooks           # Custom hooks
    - useForm.js
    - useNotification.js
    - useDataTable.js
```

This organization prevents duplication and makes components easy to find and reuse.
