---
name: design-guide
description: Professional UI design decision-making system for visual consistency. Use when (1) Starting new UI design work, (2) Making design decisions (colors, typography, spacing, shadows), (3) Reviewing UI for consistency and visual quality, (4) Resolving design conflicts or style questions. DO NOT use for React component implementation - use shadcn-ui-builder skill for actual code. Focus: design principles, visual hierarchy, color/spacing systems, and design validation.
---

# Design Guide

Professional, modern UI design system that ensures every interface looks clean, minimal, and polished.

## When to Use This Skill

Use design-guide when you need to:

- **Make design decisions** about colors, typography, spacing, or visual hierarchy
- **Start new UI design** and need design direction before implementation
- **Review existing UI** for consistency and visual quality
- **Resolve design conflicts** or answer "which looks better?" questions
- **Validate design choices** against professional standards

## When NOT to Use This Skill

**DO NOT use design-guide for:**

- **React component implementation** → Use `shadcn-ui-builder` skill instead
- **Writing JSX/TSX code** → Use `shadcn-ui-builder` skill instead
- **Building actual components** → This skill is for DECISIONS, not CODE
- **Debugging component behavior** → Use appropriate debugging tools
- **Data fetching or state management** → This is a design-only skill

**Clear separation:**

- `design-guide` = "What should this look like?" (design decisions)
- `shadcn-ui-builder` = "How do I build this?" (implementation code)

## Core Design Philosophy

**Clean and Minimal**

- Lots of white space
- Not cluttered
- Neutral foundation (grays and off-whites)
- ONE accent color used sparingly

**NO Gradients**

- Especially no generic purple/blue gradients
- Solid colors only

**Consistent System**

- 8px grid for all spacing (8, 16, 24, 32, 48, 64px)
- Maximum 2 fonts
- Clear hierarchy
- Subtle shadows, not heavy

**Mobile-First**

- Design for mobile, enhance for desktop
- Touch-friendly interactions
- Responsive at all breakpoints

## Quick Reference

### Colors (Choose ONE Accent)

```
Base:    bg-white, bg-gray-50, bg-gray-100
Text:    text-gray-900 (headings), text-gray-700 (body)
Border:  border-gray-200
Accent:  bg-blue-600 (or your chosen color) - use sparingly
```

### Typography

```
Body:    text-base (16px minimum)
H1:      text-4xl md:text-5xl font-bold
H2:      text-3xl font-semibold
H3:      text-2xl font-semibold
Small:   text-sm (14px for labels)
```

### Spacing (8px Grid)

```
Tight:   space-2 (8px)
Normal:  space-4 (16px), space-6 (24px)
Large:   space-8 (32px), space-12 (48px)
Huge:    space-16 (64px)
```

### Shadows

```
Subtle:  shadow-sm (use this)
Medium:  shadow (hover states)
Heavy:   shadow-lg (modals only)
```

### Rounded Corners

```
Standard: rounded-lg (8px)
Buttons:  rounded-lg
Cards:    rounded-lg
Inputs:   rounded-lg
```

## The Design Checklist

Before considering any UI complete, verify:

**Colors:**

- [ ] Page is mostly neutral (grays/whites)
- [ ] ONE clear accent color used sparingly
- [ ] NO gradients anywhere
- [ ] Semantic colors only for feedback

**Typography:**

- [ ] Body text is 16px minimum
- [ ] Clear heading hierarchy
- [ ] Using 2 fonts or fewer
- [ ] Text is readable (good contrast)

**Spacing:**

- [ ] All spacing uses 8px grid
- [ ] Consistent spacing between similar elements
- [ ] Generous white space (not cramped)
- [ ] Mobile-first responsive spacing

**Components:**

- [ ] Buttons have clear hover states
- [ ] Cards use border OR shadow, not both
- [ ] Forms have proper labels and spacing
- [ ] All interactive elements have states

**Layout:**

- [ ] Mobile-responsive
- [ ] Proper max-width containers
- [ ] Touch targets are 44px+ on mobile
- [ ] Content doesn't touch edges

## Reference Documentation

Consult these guides for detailed implementation:

**references/color-system.md** - Complete color palette:

- Neutral grays and whites
- Accent color options and usage
- Semantic colors (success, error, warning)
- Bad examples to avoid

**references/typography-spacing.md** - Text and spacing:

- Typography scale and hierarchy
- Font weights and line heights
- 8px spacing system
- Responsive spacing patterns

**references/component-patterns.md** - UI components:

- Buttons (primary, secondary, ghost, danger)
- Cards (standard, with header, clickable)
- Forms (inputs, errors, validation)
- Badges, navigation, alerts, modals

**references/layout-patterns.md** - Page layouts:

- Container widths
- Grid systems
- Responsive breakpoints
- Common page patterns (hero, features, pricing)

## Common Patterns

### Button Pattern

```jsx
{
  /* Primary - Use accent color */
}
;<button
  className="
  px-4 py-2
  bg-blue-600 hover:bg-blue-700
  text-white font-medium
  rounded-lg
  shadow-sm hover:shadow
  transition-all duration-200
"
>
  Save Changes
</button>

{
  /* Secondary - Use neutral */
}
;<button
  className="
  px-4 py-2
  bg-gray-100 hover:bg-gray-200
  text-gray-900 font-medium
  rounded-lg
  transition-colors duration-200
"
>
  Cancel
</button>
```

### Card Pattern

```jsx
<div
  className="
  bg-white
  border border-gray-200
  rounded-lg
  p-6
  shadow-sm hover:shadow-md
  transition-shadow duration-200
"
>
  <h3 className="text-lg font-semibold text-gray-900 mb-2">Card Title</h3>
  <p className="text-base text-gray-700">Card content</p>
</div>
```

### Form Field Pattern

```jsx
<div>
  <label className="block text-sm font-medium text-gray-700 mb-2">
    Email Address
  </label>
  <input
    type="email"
    className="
      w-full px-4 py-2
      border border-gray-300
      rounded-lg
      focus:outline-none
      focus:ring-2 focus:ring-blue-500
      focus:border-transparent
    "
    placeholder="you@example.com"
  />
</div>
```

### Page Layout Pattern

```jsx
<div className="min-h-screen bg-gray-50">
  {/* Header */}
  <header className="bg-white border-b border-gray-200">
    <div className="max-w-7xl mx-auto px-4 py-4">{/* Navigation */}</div>
  </header>

  {/* Main */}
  <main className="max-w-7xl mx-auto px-4 py-8">{/* Page content */}</main>
</div>
```

## Good vs Bad Examples

### ✅ GOOD: Clean Button

```jsx
<button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-sm">
  Save
</button>
```

### ❌ BAD: Gradient Button

```jsx
<button className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500">
  Save
</button>
```

---

### ✅ GOOD: Simple Card

```jsx
<div className="bg-white border border-gray-200 rounded-lg p-6">Content</div>
```

### ❌ BAD: Over-styled Card

```jsx
<div className="bg-white border-4 border-purple-500 shadow-2xl rounded-3xl p-6">
  Content
</div>
```

---

### ✅ GOOD: Clear Form

```jsx
<div className="space-y-6">
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-2">
      Email
    </label>
    <input className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
  </div>
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-2">
      Password
    </label>
    <input
      type="password"
      className="w-full px-4 py-2 border border-gray-300 rounded-lg"
    />
  </div>
</div>
```

### ❌ BAD: Cramped Form

```jsx
<div>
  <div className="mb-1">
    <span className="text-xs text-gray-400">Email</span> {/* Too small */}
    <input className="w-full p-1" /> {/* Too tight */}
  </div>
  <div className="mb-1">
    <span className="text-xs text-gray-400">Password</span>
    <input type="password" className="w-full p-1" />
  </div>
</div>
```

---

### ✅ GOOD: Consistent Spacing

```jsx
<div className="space-y-6">
  <section className="mb-8">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Section</h2>
    <p>Content</p>
  </section>
  <section className="mb-8">
    <h2 className="text-2xl font-bold text-gray-900 mb-4">Section</h2>
    <p>Content</p>
  </section>
</div>
```

### ❌ BAD: Random Spacing

```jsx
<div>
  <section className="mb-3">
    {' '}
    {/* 12px - off grid */}
    <h2 className="mb-5">Section</h2> {/* 20px - off grid */}
    <p>Content</p>
  </section>
  <section className="mb-7">
    {' '}
    {/* 28px - off grid */}
    <h2 className="mb-2">Section</h2> {/* Inconsistent */}
    <p>Content</p>
  </section>
</div>
```

## Complete Example

See **assets/examples/dashboard-complete.md** for a full dashboard implementation showing all principles in action:

- Neutral color scheme with blue accent
- Clear typography hierarchy
- Consistent 8px grid spacing
- Subtle shadows
- Mobile-responsive layout
- Clean component designs

## Design Decision Framework

When building any UI component, ask:

1. **Is it clean?**
   - Lots of white space?
   - Not cluttered?
   - Mostly neutral colors?

2. **Is it consistent?**
   - Using 8px spacing grid?
   - Same accent color throughout?
   - Same component styles?

3. **Is it readable?**
   - Body text 16px minimum?
   - Good contrast?
   - Clear hierarchy?

4. **Is it professional?**
   - No gradients?
   - Subtle shadows?
   - Clear interactions?

5. **Is it mobile-friendly?**
   - Responsive design?
   - Touch-friendly buttons?
   - Proper spacing on small screens?

If the answer to any is "no", revise the design.

## Common Mistakes to Avoid

1. **Multiple accent colors** - Pick ONE and stick with it
2. **Gradients** - Just don't use them
3. **Tiny text** - Never go below 14px, prefer 16px+
4. **Inconsistent spacing** - Always use 8px grid
5. **Heavy shadows** - Keep them subtle
6. **Over-rounded corners** - rounded-lg is enough
7. **Too many font weights** - Max 3 weights
8. **No white space** - Give elements room to breathe
9. **Ignoring mobile** - Always design mobile-first
10. **Inconsistent states** - All interactive elements need hover/active

## Applying This Skill

When I build any UI for you, I will:

1. ✅ Use the neutral color palette from references/color-system.md
2. ✅ Apply ONE accent color sparingly
3. ✅ Follow the 8px spacing grid from references/typography-spacing.md
4. ✅ Use component patterns from references/component-patterns.md
5. ✅ Apply layout patterns from references/layout-patterns.md
6. ✅ Ensure mobile-first responsive design
7. ✅ Keep everything clean and minimal
8. ✅ Avoid all prohibited patterns (gradients, inconsistent spacing, etc.)

This ensures every UI component is modern, professional, and consistent.
