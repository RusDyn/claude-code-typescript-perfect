# Layout Patterns & Responsive Design

Modern, mobile-first layout patterns using Tailwind CSS.

## Core Layout Principles

1. **Mobile First**: Design for mobile, enhance for desktop
2. **Consistent Containers**: Use max-width containers
3. **Grid System**: Use CSS Grid for layouts
4. **Flexbox**: Use for component-level alignment
5. **White Space**: Generous padding and margins

## Container Widths

```jsx
{
  /* Full width */
}
;<div className="w-full px-4">Full width with padding</div>

{
  /* Constrained width */
}
;<div className="max-w-7xl mx-auto px-4">{/* 1280px max, centered */}</div>

{
  /* Content width (for reading) */
}
;<div className="max-w-2xl mx-auto px-4">{/* 672px max, centered */}</div>
```

### Standard Container Sizes

```
max-w-sm    - 384px   - Small modals
max-w-md    - 448px   - Forms
max-w-lg    - 512px   - Medium content
max-w-xl    - 576px   - Wider content
max-w-2xl   - 672px   - Reading content
max-w-4xl   - 896px   - Standard page
max-w-6xl   - 1152px  - Wide page
max-w-7xl   - 1280px  - Maximum app width
```

## Page Layout Structure

### Basic Page Template

```jsx
<div className="min-h-screen bg-gray-50">
  {/* Header */}
  <header className="bg-white border-b border-gray-200">
    <div className="max-w-7xl mx-auto px-4 py-4">{/* Navigation */}</div>
  </header>

  {/* Main Content */}
  <main className="max-w-7xl mx-auto px-4 py-8 md:py-12">
    {/* Page content */}
  </main>

  {/* Footer */}
  <footer className="bg-white border-t border-gray-200 mt-auto">
    <div className="max-w-7xl mx-auto px-4 py-8">{/* Footer content */}</div>
  </footer>
</div>
```

### Two-Column Layout (Sidebar)

```jsx
<div className="max-w-7xl mx-auto px-4 py-8">
  <div className="flex flex-col lg:flex-row gap-8">
    {/* Sidebar (full width on mobile, 1/4 on desktop) */}
    <aside className="lg:w-64 flex-shrink-0">
      <nav className="space-y-2">{/* Navigation items */}</nav>
    </aside>

    {/* Main Content (full width on mobile, 3/4 on desktop) */}
    <main className="flex-1 min-w-0">{/* Content */}</main>
  </div>
</div>
```

### Three-Column Layout

```jsx
<div className="max-w-7xl mx-auto px-4 py-8">
  <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
    {/* Left Sidebar */}
    <aside className="lg:col-span-3">{/* Sidebar content */}</aside>

    {/* Main Content */}
    <main className="lg:col-span-6">{/* Main content */}</main>

    {/* Right Sidebar */}
    <aside className="lg:col-span-3">{/* Sidebar content */}</aside>
  </div>
</div>
```

## Grid Layouts

### Equal Columns

```jsx
{
  /* 1 column on mobile, 2 on tablet, 3 on desktop */
}
;<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div className="bg-white p-6 border border-gray-200 rounded-lg">Card 1</div>
  <div className="bg-white p-6 border border-gray-200 rounded-lg">Card 2</div>
  <div className="bg-white p-6 border border-gray-200 rounded-lg">Card 3</div>
</div>
```

### Auto-Fit Grid (Responsive Cards)

```jsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  {/* Cards automatically wrap */}
  <div className="bg-white p-6 border border-gray-200 rounded-lg">Card</div>
  {/* More cards... */}
</div>
```

### Feature Grid

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-8">
  <div className="flex gap-4">
    <div className="flex-shrink-0">
      <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
        {/* Icon */}
      </div>
    </div>
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        Feature Title
      </h3>
      <p className="text-base text-gray-700">Feature description goes here.</p>
    </div>
  </div>
  {/* More features... */}
</div>
```

## Responsive Breakpoints

```
sm:   640px   - Small tablets
md:   768px   - Tablets
lg:   1024px  - Small laptops
xl:   1280px  - Desktops
2xl:  1536px  - Large screens
```

### Breakpoint Usage Examples

```jsx
{
  /* Text size responsive */
}
;<h1 className="text-3xl md:text-4xl lg:text-5xl">Responsive Heading</h1>

{
  /* Spacing responsive */
}
;<div className="p-4 md:p-6 lg:p-8">Responsive padding</div>

{
  /* Layout responsive */
}
;<div className="flex flex-col md:flex-row gap-4">
  Stacked on mobile, row on tablet+
</div>

{
  /* Grid responsive */
}
;<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  Responsive grid
</div>
```

## Common Layout Patterns

### Hero Section

```jsx
<section className="bg-white py-12 md:py-20">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
      Welcome to Our Platform
    </h1>
    <p className="text-lg md:text-xl text-gray-700 mb-8 max-w-2xl mx-auto">
      Build amazing products with our modern design system
    </p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center">
      <button className="px-6 py-3 bg-blue-600 text-white rounded-lg">
        Get Started
      </button>
      <button className="px-6 py-3 bg-gray-100 text-gray-900 rounded-lg">
        Learn More
      </button>
    </div>
  </div>
</section>
```

### Feature Section

```jsx
<section className="py-12 md:py-16">
  <div className="max-w-6xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        Features
      </h2>
      <p className="text-lg text-gray-700 max-w-2xl mx-auto">
        Everything you need to build modern applications
      </p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      {/* Feature cards */}
    </div>
  </div>
</section>
```

### Pricing Section

```jsx
<section className="py-12 md:py-16 bg-gray-50">
  <div className="max-w-6xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-3xl font-bold text-gray-900 mb-4">Simple Pricing</h2>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
      {/* Pricing cards */}
      <div className="bg-white p-8 border border-gray-200 rounded-lg">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Starter</h3>
        <p className="text-4xl font-bold text-gray-900 mb-6">
          $9<span className="text-lg font-normal text-gray-600">/mo</span>
        </p>
        <button className="w-full px-4 py-2 bg-gray-100 text-gray-900 rounded-lg">
          Choose Plan
        </button>
      </div>
      {/* More pricing tiers */}
    </div>
  </div>
</section>
```

### Dashboard Layout

```jsx
<div className="min-h-screen bg-gray-50">
  {/* Top Nav */}
  <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
    <div className="px-4 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-8">
          <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
          <nav className="hidden md:flex gap-6">{/* Nav items */}</nav>
        </div>
        <div className="flex items-center gap-4">{/* User menu */}</div>
      </div>
    </div>
  </header>

  {/* Main Content */}
  <main className="max-w-7xl mx-auto px-4 py-8">
    {/* Stats Grid */}
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {/* Stat cards */}
    </div>

    {/* Content Grid */}
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2">{/* Main chart/content */}</div>
      <div>{/* Sidebar content */}</div>
    </div>
  </main>
</div>
```

### Form Layout (Centered)

```jsx
<div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
  <div className="w-full max-w-md">
    <div className="bg-white p-8 border border-gray-200 rounded-lg shadow-sm">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
        Sign In
      </h2>

      <form className="space-y-6">{/* Form fields */}</form>
    </div>
  </div>
</div>
```

## Spacing Guidelines

### Section Spacing

```jsx
{
  /* Mobile: 48px, Desktop: 64px */
}
;<section className="py-12 md:py-16">Content</section>

{
  /* Mobile: 64px, Desktop: 96px */
}
;<section className="py-16 md:py-24">Hero content</section>
```

### Content Spacing

```jsx
{
  /* Between sections */
}
;<div className="space-y-12 md:space-y-16">
  <section>...</section>
  <section>...</section>
</div>

{
  /* Between components */
}
;<div className="space-y-6">
  <div>...</div>
  <div>...</div>
</div>
```

## Mobile Considerations

### Touch Targets

```jsx
{
  /* Minimum 44px height for touch targets */
}
;<button className="min-h-[44px] px-4">Touchable Button</button>
```

### Mobile Navigation

```jsx
<nav className="md:hidden fixed bottom-0 inset-x-0 bg-white border-t border-gray-200">
  <div className="flex justify-around py-3">
    <button className="flex flex-col items-center gap-1">
      {/* Icon */}
      <span className="text-xs">Home</span>
    </button>
    {/* More nav items */}
  </div>
</nav>
```

### Stack on Mobile

```jsx
{
  /* Always stack on mobile */
}
;<div className="flex flex-col md:flex-row gap-4">
  <div className="flex-1">Left</div>
  <div className="flex-1">Right</div>
</div>
```

## Layout Checklist

- [ ] Mobile-first approach used
- [ ] Consistent max-width containers
- [ ] Responsive breakpoints for all sizes
- [ ] Touch targets are 44px minimum
- [ ] Adequate padding on mobile (16px minimum)
- [ ] Content doesn't touch edges
- [ ] Text has max-width for readability
- [ ] Grid columns collapse on mobile
- [ ] Navigation accessible on all screen sizes
- [ ] Spacing consistent across breakpoints

## Bad Layout Examples

### ❌ No Mobile Consideration

```jsx
{
  /* DON'T: Fixed desktop layout */
}
;<div className="flex">
  <div className="w-64">Sidebar</div>
  <div className="flex-1">Content</div>
</div>
```

### ❌ No Max Width

```jsx
{
  /* DON'T: Full width on large screens */
}
;<div className="w-full p-4">Content spans entire viewport on 4K monitors</div>
```

### ❌ Inconsistent Spacing

```jsx
{
  /* DON'T: Random spacing values */
}
;<div className="space-y-7">
  {' '}
  {/* 28px - off grid */}
  <div className="mb-5">...</div> {/* 20px - off grid */}
  <div className="mt-3">...</div> {/* 12px - okay but inconsistent */}
</div>
```

## Good Layout Example (Complete Page)

```jsx
<div className="min-h-screen bg-gray-50">
  {/* Header */}
  <header className="bg-white border-b border-gray-200">
    <div className="max-w-7xl mx-auto px-4 py-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">App Name</h1>
        <nav className="flex gap-6">
          <a href="#" className="text-gray-700 hover:text-gray-900">
            Home
          </a>
          <a href="#" className="text-gray-700 hover:text-gray-900">
            About
          </a>
        </nav>
      </div>
    </div>
  </header>

  {/* Hero */}
  <section className="bg-white py-16 md:py-24">
    <div className="max-w-4xl mx-auto px-4 text-center">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
        Modern Design System
      </h1>
      <p className="text-lg text-gray-700 mb-8 max-w-2xl mx-auto">
        Build beautiful, professional interfaces with ease
      </p>
      <button className="px-6 py-3 bg-blue-600 text-white rounded-lg">
        Get Started
      </button>
    </div>
  </section>

  {/* Features */}
  <section className="py-16 md:py-24">
    <div className="max-w-6xl mx-auto px-4">
      <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">
        Features
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Feature cards with consistent spacing */}
      </div>
    </div>
  </section>
</div>
```

This layout system ensures your UI looks professional and works beautifully on all devices.
