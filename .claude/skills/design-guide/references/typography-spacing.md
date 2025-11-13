# Typography & Spacing System

Professional typography and spacing guidelines using Tailwind's 8px grid system.

## Typography Hierarchy

### Font Stack

**Maximum 2 fonts:**

- **UI Font (Body & Interface)**: System font stack or single web font
- **Display Font (Optional)**: For headings only, if needed

### Recommended Font Combinations

**Option 1: System Fonts Only (Fastest)**

```
font-sans = -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
```

**Option 2: Inter (Modern, Clean)**

```
Headings: font-sans (Inter)
Body:     font-sans (Inter)
```

**Option 3: Heading + Body**

```
Headings: font-serif (Lora, Merriweather)
Body:     font-sans (Inter, Open Sans)
```

## Text Sizes

**Minimum body text: 16px**

### Size Scale (Mobile First)

```
text-xs      12px   - Captions, metadata
text-sm      14px   - Secondary text, labels
text-base    16px   - Body text (DEFAULT)
text-lg      18px   - Emphasized body text
text-xl      20px   - Large body text
text-2xl     24px   - H3 headings
text-3xl     30px   - H2 headings
text-4xl     36px   - H1 headings (mobile)
text-5xl     48px   - H1 headings (desktop)
text-6xl     60px   - Hero text (desktop)
```

### Desktop Adjustments

```
<h1 className="text-4xl md:text-5xl">Main Heading</h1>
<h2 className="text-3xl md:text-4xl">Section Heading</h2>
```

## Typography Examples

### Heading Hierarchy

```jsx
{
  /* Page Title */
}
;<h1 className="text-4xl md:text-5xl font-bold text-gray-900">Dashboard</h1>

{
  /* Section Heading */
}
;<h2 className="text-3xl font-semibold text-gray-900">Recent Activity</h2>

{
  /* Subsection */
}
;<h3 className="text-2xl font-semibold text-gray-800">This Week</h3>

{
  /* Body */
}
;<p className="text-base text-gray-700">
  Regular paragraph text goes here. This is readable at 16px.
</p>

{
  /* Secondary Text */
}
;<p className="text-sm text-gray-600">Less important information at 14px.</p>

{
  /* Captions */
}
;<span className="text-xs text-gray-500">Last updated 2 hours ago</span>
```

## Font Weights

Use sparingly for hierarchy:

```
font-normal     400 - Body text
font-medium     500 - Buttons, labels
font-semibold   600 - Subheadings
font-bold       700 - Main headings
```

**❌ DON'T:**

- Use more than 3 different weights
- Use font-light or font-thin (hard to read)
- Use font-black or font-extrabold (too heavy)

## Line Height

```
leading-none      1       - Tight headings
leading-tight     1.25    - Headings
leading-snug      1.375   - Large text
leading-normal    1.5     - Body text (DEFAULT)
leading-relaxed   1.625   - Comfortable reading
leading-loose     2       - Very spacious
```

**Default for body:** `leading-normal` (1.5)

### Examples

```jsx
{
  /* Tight headings */
}
;<h1 className="text-5xl font-bold leading-tight">
  Save 50% on Your First Order
</h1>

{
  /* Normal body */
}
;<p className="text-base leading-normal">
  Regular paragraph with comfortable line spacing.
</p>

{
  /* Relaxed for long-form */
}
;<article className="text-lg leading-relaxed">
  Long-form content with extra breathing room.
</article>
```

## Spacing System (8px Grid)

**All spacing must be multiples of 8px:**

### Spacing Scale

```
space-1     4px    - Rare, very tight
space-2     8px    - Minimum spacing
space-3     12px   - Compact elements
space-4     16px   - DEFAULT spacing
space-6     24px   - Medium spacing
space-8     32px   - Large spacing
space-12    48px   - Section spacing
space-16    64px   - Major sections
space-20    80px   - Page sections
space-24    96px   - Hero sections
```

### Component Spacing Examples

**Button Padding:**

```jsx
{
  /* Small */
}
;<button className="px-3 py-2">
  {' '}
  {/* 12px × 8px */}
  Small
</button>

{
  /* Medium (Default) */
}
;<button className="px-4 py-2">
  {' '}
  {/* 16px × 8px */}
  Medium
</button>

{
  /* Large */
}
;<button className="px-6 py-3">
  {' '}
  {/* 24px × 12px */}
  Large
</button>
```

**Form Field Spacing:**

```jsx
<div className="space-y-6">
  {' '}
  {/* 24px between fields */}
  <div>
    <label className="block mb-2">
      {' '}
      {/* 8px below label */}
      Email
    </label>
    <input className="px-4 py-2" /> {/* 16px × 8px inside */}
  </div>
  <div>
    <label className="block mb-2">Password</label>
    <input className="px-4 py-2" />
  </div>
</div>
```

**Card Padding:**

```jsx
{
  /* Compact card */
}
;<div className="p-4">
  {' '}
  {/* 16px all around */}
  Content
</div>

{
  /* Standard card */
}
;<div className="p-6">
  {' '}
  {/* 24px all around */}
  Content
</div>

{
  /* Spacious card */
}
;<div className="p-8">
  {' '}
  {/* 32px all around */}
  Content
</div>
```

**Section Spacing:**

```jsx
<div className="space-y-12">
  {' '}
  {/* 48px between sections */}
  <section className="mb-8">
    {' '}
    {/* 32px below */}
    <h2 className="mb-4">Section</h2> {/* 16px below heading */}
    <p>Content</p>
  </section>
  <section>
    <h2 className="mb-4">Section</h2>
    <p>Content</p>
  </section>
</div>
```

## Responsive Spacing

Mobile first, increase on larger screens:

```jsx
<div className="px-4 py-8 md:px-8 md:py-12 lg:px-16 lg:py-16">
  {/* 16px/32px → 32px/48px → 64px/64px */}
</div>
```

## Max Width for Readability

Long text should never span full width:

```jsx
{
  /* Readable line length */
}
;<div className="max-w-2xl">
  {' '}
  {/* 672px max */}
  <p className="text-base leading-relaxed">Long-form content stays readable.</p>
</div>

{
  /* Even narrower for optimal reading */
}
;<article className="max-w-prose">
  {' '}
  {/* 65ch ≈ 650px */}
  Long article content
</article>
```

## Common Spacing Patterns

### Stacked Content (Vertical Rhythm)

```jsx
<div className="space-y-4">    {/* 16px between all children */}
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
  <p>Paragraph 3</p>
</div>

<div className="space-y-6">    {/* 24px between all children */}
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

### Inline Spacing (Horizontal)

```jsx
<div className="flex gap-4">   {/* 16px between items */}
  <button>Button 1</button>
  <button>Button 2</button>
</div>

<div className="flex space-x-2"> {/* 8px between items */}
  <span>Tag 1</span>
  <span>Tag 2</span>
</div>
```

### Grid Spacing

```jsx
<div className="grid grid-cols-3 gap-6">
  {' '}
  {/* 24px gap */}
  <div>Item</div>
  <div>Item</div>
  <div>Item</div>
</div>
```

## Typography & Spacing Checklist

**Typography:**

- [ ] Body text is 16px minimum
- [ ] Using 2 fonts or fewer
- [ ] Clear heading hierarchy
- [ ] Line height comfortable (1.5 for body)
- [ ] Max 3 font weights used
- [ ] Long text has max-width constraint

**Spacing:**

- [ ] All spacing uses 8px grid (8, 16, 24, 32, 48, 64)
- [ ] Consistent spacing between similar elements
- [ ] Enough white space (not cramped)
- [ ] Mobile-first responsive spacing
- [ ] Button padding feels comfortable
- [ ] Form fields have clear separation

## Bad Examples (Don't Do This)

### ❌ Too Many Font Sizes

```jsx
<h1 className="text-7xl">Too Big</h1>
<h2 className="text-[33px]">Custom size</h2>  {/* Not on scale */}
<p className="text-[15px]">Weird size</p>     {/* Not on scale */}
<span className="text-[11px]">Too small</span> {/* Below minimum */}
```

### ❌ Inconsistent Spacing

```jsx
<div className="mb-3">
  {' '}
  {/* 12px */}
  <p className="mb-5">...</p> {/* 20px - off grid! */}
  <p className="mb-7">...</p> {/* 28px - off grid! */}
</div>
```

### ❌ No Max Width

```jsx
<p className="text-base">
  This paragraph spans the entire width of the screen making it impossible to
  read comfortably when the browser is maximized on a large monitor because our
  eyes can't track across such long lines of text.
</p>
```

## Good Example (Complete)

```jsx
<div className="max-w-4xl mx-auto px-4 py-12">
  {/* Page heading */}
  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-8">
    Welcome Back
  </h1>

  {/* Section */}
  <section className="mb-12">
    <h2 className="text-2xl font-semibold text-gray-800 mb-4">
      Your Dashboard
    </h2>

    {/* Cards with consistent spacing */}
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-white p-6 border border-gray-200 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Recent Activity
        </h3>
        <p className="text-base text-gray-700">
          Content with proper spacing and readable text size.
        </p>
      </div>
    </div>
  </section>
</div>
```

This creates a clean, professional design with consistent spacing and readable typography.
