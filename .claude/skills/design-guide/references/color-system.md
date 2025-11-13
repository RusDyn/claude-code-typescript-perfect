# Color System Reference

Modern, professional color palette guidelines using neutral bases with strategic accent colors.

## Core Philosophy

- **Neutral foundation**: Grays and off-whites for 90% of the UI
- **Single accent**: ONE accent color used sparingly for CTAs and emphasis
- **NO gradients**: Especially no generic purple/blue gradients
- **Semantic colors**: Reserve colors for meaning (success, error, warning)

## Neutral Palette (Primary Colors)

Use these for most of your UI:

### Whites and Light Grays (Backgrounds)

```
bg-white           - Pure white (#FFFFFF)
bg-gray-50         - Off-white (#F9FAFB) - Subtle backgrounds
bg-gray-100        - Light gray (#F3F4F6) - Hover states, disabled
```

### Mid Grays (Borders, Dividers)

```
border-gray-200    - Very subtle borders (#E5E7EB)
border-gray-300    - Standard borders (#D1D5DB)
bg-gray-200        - Disabled backgrounds
```

### Dark Grays (Text, Icons)

```
text-gray-600      - Secondary text (#4B5563)
text-gray-700      - Body text (#374151)
text-gray-800      - Headings (#1F2937)
text-gray-900      - Primary text (#111827)
```

## Accent Color (Choose ONE)

Pick ONE accent color for your entire application. Use it only for:

- Primary buttons
- Links
- Active states
- Important icons
- Key metrics/data

### Recommended Accent Options

**Option 1: Blue (Professional, Trust)**

```
bg-blue-600        - Primary (#2563EB)
bg-blue-700        - Hover (#1D4ED8)
text-blue-600      - Links (#2563EB)
```

**Option 2: Emerald (Fresh, Success)**

```
bg-emerald-600     - Primary (#059669)
bg-emerald-700     - Hover (#047857)
text-emerald-600   - Links (#059669)
```

**Option 3: Violet (Modern, Creative)**

```
bg-violet-600      - Primary (#7C3AED)
bg-violet-700      - Hover (#6D28D9)
text-violet-600    - Links (#7C3AED)
```

**Option 4: Rose (Warm, Energetic)**

```
bg-rose-600        - Primary (#E11D48)
bg-rose-700        - Hover (#BE123C)
text-rose-600      - Links (#E11D48)
```

**Option 5: Amber (Attention, Warmth)**

```
bg-amber-500       - Primary (#F59E0B)
bg-amber-600       - Hover (#D97706)
text-amber-600     - Links (#D97706)
```

### How to Use Accent Color

**✅ DO:**

- Primary action buttons
- Active navigation items
- Links
- Icons for primary actions
- Progress indicators
- Badges for important status

**❌ DON'T:**

- Every button
- Every icon
- Backgrounds of entire sections
- Multiple different accent colors
- Text body content

## Semantic Colors (Use Sparingly)

Only for specific feedback/status:

### Success (Green)

```
bg-green-50        - Success background (#F0FDF4)
text-green-700     - Success text (#15803D)
border-green-200   - Success border (#BBF7D0)
```

### Error (Red)

```
bg-red-50          - Error background (#FEF2F2)
text-red-700       - Error text (#B91C1C)
border-red-200     - Error border (#FECACA)
```

### Warning (Yellow/Orange)

```
bg-yellow-50       - Warning background (#FEFCE8)
text-yellow-700    - Warning text (#A16207)
border-yellow-200  - Warning border (#FEF08A)
```

### Info (Blue - different from accent)

```
bg-sky-50          - Info background (#F0F9FF)
text-sky-700       - Info text (#0369A1)
border-sky-200     - Info border (#BAE6FD)
```

## Color Usage Examples

### Example 1: Button Primary (with Blue accent)

```jsx
<button className="bg-blue-600 hover:bg-blue-700 text-white">
  Save Changes
</button>
```

### Example 2: Button Secondary

```jsx
<button className="bg-gray-100 hover:bg-gray-200 text-gray-900">Cancel</button>
```

### Example 3: Card

```jsx
<div className="bg-white border border-gray-200">{/* Content */}</div>
```

### Example 4: Text Hierarchy

```jsx
<h1 className="text-gray-900">Main Heading</h1>
<h2 className="text-gray-800">Subheading</h2>
<p className="text-gray-700">Body text content</p>
<span className="text-gray-600">Secondary text</span>
```

## Prohibited Colors

**❌ NEVER use these patterns:**

### Bad Example 1: Random Colors

```jsx
{/* DON'T: Every element a different color */}
<button className="bg-purple-500">Action 1</button>
<button className="bg-pink-500">Action 2</button>
<button className="bg-indigo-500">Action 3</button>
```

### Bad Example 2: Gradients

```jsx
{
  /* DON'T: Generic gradients */
}
<div className="bg-gradient-to-r from-purple-500 to-blue-500">{/* NO! */}</div>;
```

### Bad Example 3: Too Many Accent Colors

```jsx
{
  /* DON'T: Multiple accent colors */
}
<nav>
  <a className="text-blue-600">Home</a>
  <a className="text-purple-600">About</a>
  <a className="text-green-600">Contact</a>
</nav>;
```

## Color Combinations

### Light Mode (Default)

```
Background:     bg-white or bg-gray-50
Text:           text-gray-900 (primary), text-gray-700 (body)
Borders:        border-gray-200
Accent:         [Your chosen accent] (e.g., bg-blue-600)
```

### Card on Light Background

```
Card:           bg-white
Border:         border-gray-200
Shadow:         shadow-sm
Text:           text-gray-900
```

### Nested Elements

```
Page:           bg-gray-50
Container:      bg-white
Card:           bg-gray-50 (subtle contrast)
```

## Dark Mode (If Needed)

If implementing dark mode, use:

```
Background:     bg-gray-900
Card:           bg-gray-800
Text:           text-gray-100
Border:         border-gray-700
Accent:         [Lighter version of accent] (e.g., bg-blue-500)
```

## Testing Your Colors

### Contrast Ratios

- Text on background: Minimum 4.5:1 ratio
- Large text (18px+): Minimum 3:1 ratio
- Use tools like WebAIM Contrast Checker

### Check Your Design

Ask these questions:

1. Is the page mostly neutral (grays/whites)?
2. Can you identify ONE clear accent color?
3. Are there any gradients? (Remove them)
4. Are semantic colors only used for feedback?
5. Is text readable against backgrounds?

## Quick Reference

**90% of your UI:**

- `bg-white`, `bg-gray-50`, `bg-gray-100`
- `text-gray-900`, `text-gray-700`, `text-gray-600`
- `border-gray-200`, `border-gray-300`

**5% of your UI (Accent):**

- `bg-blue-600`, `hover:bg-blue-700` (or your chosen accent)
- `text-blue-600` for links

**5% of your UI (Semantic):**

- `text-green-700` for success
- `text-red-700` for errors
- `text-yellow-700` for warnings

This color system ensures a clean, professional look that never feels cluttered or overwhelming.
