# Component Patterns

Professional, modern component designs with Tailwind CSS.

## Buttons

### Primary Button (Accent Color)

```jsx
<button
  className="
  px-4 py-2 
  bg-blue-600 hover:bg-blue-700 active:bg-blue-800
  text-white font-medium
  rounded-lg
  shadow-sm hover:shadow
  transition-all duration-200
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
"
>
  Save Changes
</button>
```

### Secondary Button (Neutral)

```jsx
<button
  className="
  px-4 py-2
  bg-gray-100 hover:bg-gray-200 active:bg-gray-300
  text-gray-900 font-medium
  rounded-lg
  transition-colors duration-200
  focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
"
>
  Cancel
</button>
```

### Ghost/Text Button

```jsx
<button
  className="
  px-4 py-2
  text-gray-700 hover:text-gray-900 hover:bg-gray-100
  font-medium
  rounded-lg
  transition-colors duration-200
  focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2
"
>
  Learn More
</button>
```

### Danger Button

```jsx
<button
  className="
  px-4 py-2
  bg-red-600 hover:bg-red-700
  text-white font-medium
  rounded-lg
  shadow-sm hover:shadow
  transition-all duration-200
"
>
  Delete Account
</button>
```

### Button Sizes

```jsx
{
  /* Small */
}
<button className="px-3 py-1.5 text-sm">Small</button>;

{
  /* Medium (Default) */
}
<button className="px-4 py-2 text-base">Medium</button>;

{
  /* Large */
}
<button className="px-6 py-3 text-lg">Large</button>;
```

### ❌ Bad Button Examples

```jsx
{
  /* DON'T: Gradient */
}
<button className="bg-gradient-to-r from-purple-500 to-blue-500">Bad</button>;

{
  /* DON'T: Heavy shadow */
}
<button className="shadow-2xl">Too Much Shadow</button>;

{
  /* DON'T: Over-rounded */
}
<button className="rounded-full px-12">Too Round</button>;
```

## Cards

### Standard Card

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
  <p className="text-base text-gray-700">Card content goes here.</p>
</div>
```

### Card with Header

```jsx
<div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
  {/* Header */}
  <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
    <h3 className="text-lg font-semibold text-gray-900">Settings</h3>
  </div>

  {/* Body */}
  <div className="p-6">
    <p className="text-base text-gray-700">Card content</p>
  </div>
</div>
```

### Clickable Card

```jsx
<button
  className="
  w-full text-left
  bg-white border border-gray-200
  rounded-lg p-6
  hover:border-gray-300 hover:shadow-md
  transition-all duration-200
  focus:outline-none focus:ring-2 focus:ring-blue-500
"
>
  <h3 className="text-lg font-semibold text-gray-900 mb-2">Select Option</h3>
  <p className="text-sm text-gray-600">Click to choose this option</p>
</button>
```

### ❌ Bad Card Examples

```jsx
{
  /* DON'T: Both border AND heavy shadow */
}
<div className="border-2 border-gray-300 shadow-2xl">Too much</div>;

{
  /* DON'T: No visual separation */
}
<div className="bg-white">No border or shadow - blends with background</div>;

{
  /* DON'T: Too much border radius */
}
<div className="rounded-3xl">Overly rounded</div>;
```

## Forms

### Text Input

```jsx
<div>
  <label
    htmlFor="email"
    className="block text-sm font-medium text-gray-700 mb-2"
  >
    Email Address
  </label>
  <input
    id="email"
    type="email"
    className="
      w-full px-4 py-2
      border border-gray-300
      rounded-lg
      focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
      placeholder:text-gray-400
      disabled:bg-gray-50 disabled:text-gray-500
    "
    placeholder="you@example.com"
  />
</div>
```

### Input with Error State

```jsx
<div>
  <label className="block text-sm font-medium text-gray-700 mb-2">
    Email Address
  </label>
  <input
    className="
      w-full px-4 py-2
      border-2 border-red-300
      rounded-lg
      focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent
    "
    aria-invalid="true"
  />
  <p className="mt-2 text-sm text-red-600">
    Please enter a valid email address
  </p>
</div>
```

### Input with Helper Text

```jsx
<div>
  <label className="block text-sm font-medium text-gray-700 mb-2">
    Username
  </label>
  <input className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
  <p className="mt-2 text-sm text-gray-600">
    Choose a unique username for your account
  </p>
</div>
```

### Textarea

```jsx
<div>
  <label className="block text-sm font-medium text-gray-700 mb-2">
    Description
  </label>
  <textarea
    rows={4}
    className="
      w-full px-4 py-2
      border border-gray-300
      rounded-lg
      focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
      resize-none
    "
  />
</div>
```

### Select Dropdown

```jsx
<div>
  <label className="block text-sm font-medium text-gray-700 mb-2">
    Country
  </label>
  <select
    className="
    w-full px-4 py-2
    border border-gray-300
    rounded-lg
    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
    bg-white
  "
  >
    <option>United States</option>
    <option>Canada</option>
    <option>United Kingdom</option>
  </select>
</div>
```

### Checkbox

```jsx
<label className="flex items-center gap-3 cursor-pointer">
  <input
    type="checkbox"
    className="
      w-4 h-4
      text-blue-600
      border-gray-300
      rounded
      focus:ring-2 focus:ring-blue-500
    "
  />
  <span className="text-sm text-gray-700">
    I agree to the terms and conditions
  </span>
</label>
```

### Radio Button

```jsx
<div className="space-y-3">
  <label className="flex items-center gap-3 cursor-pointer">
    <input
      type="radio"
      name="plan"
      className="
        w-4 h-4
        text-blue-600
        border-gray-300
        focus:ring-2 focus:ring-blue-500
      "
    />
    <span className="text-sm text-gray-700">Free Plan</span>
  </label>

  <label className="flex items-center gap-3 cursor-pointer">
    <input
      type="radio"
      name="plan"
      className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-2 focus:ring-blue-500"
    />
    <span className="text-sm text-gray-700">Pro Plan</span>
  </label>
</div>
```

### Form Layout

```jsx
<form className="space-y-6 max-w-md">
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-2">
      Full Name
    </label>
    <input className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
  </div>

  <div>
    <label className="block text-sm font-medium text-gray-700 mb-2">
      Email
    </label>
    <input
      type="email"
      className="w-full px-4 py-2 border border-gray-300 rounded-lg"
    />
  </div>

  <div className="flex gap-4">
    <button
      type="submit"
      className="px-4 py-2 bg-blue-600 text-white rounded-lg"
    >
      Submit
    </button>
    <button
      type="button"
      className="px-4 py-2 bg-gray-100 text-gray-900 rounded-lg"
    >
      Cancel
    </button>
  </div>
</form>
```

## Badges & Tags

### Status Badge

```jsx
{
  /* Success */
}
<span
  className="
  inline-flex items-center gap-1
  px-3 py-1
  bg-green-50
  text-green-700 text-sm font-medium
  rounded-full
  border border-green-200
"
>
  Active
</span>;

{
  /* Warning */
}
<span className="inline-flex items-center gap-1 px-3 py-1 bg-yellow-50 text-yellow-700 text-sm font-medium rounded-full border border-yellow-200">
  Pending
</span>;

{
  /* Error */
}
<span className="inline-flex items-center gap-1 px-3 py-1 bg-red-50 text-red-700 text-sm font-medium rounded-full border border-red-200">
  Failed
</span>;

{
  /* Neutral */
}
<span className="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-full">
  Draft
</span>;
```

### Tag (Removable)

```jsx
<span
  className="
  inline-flex items-center gap-2
  px-3 py-1
  bg-gray-100
  text-gray-700 text-sm
  rounded-lg
"
>
  Design
  <button className="hover:text-gray-900">
    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path
        fillRule="evenodd"
        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
        clipRule="evenodd"
      />
    </svg>
  </button>
</span>
```

## Navigation

### Tabs

```jsx
<div className="border-b border-gray-200">
  <nav className="flex gap-8">
    <button
      className="
      px-1 py-4
      border-b-2 border-blue-600
      text-sm font-medium text-blue-600
    "
    >
      Overview
    </button>

    <button
      className="
      px-1 py-4
      border-b-2 border-transparent
      text-sm font-medium text-gray-600
      hover:text-gray-900 hover:border-gray-300
    "
    >
      Analytics
    </button>

    <button className="px-1 py-4 border-b-2 border-transparent text-sm font-medium text-gray-600 hover:text-gray-900 hover:border-gray-300">
      Settings
    </button>
  </nav>
</div>
```

### Breadcrumbs

```jsx
<nav className="flex items-center gap-2 text-sm">
  <a href="/" className="text-gray-600 hover:text-gray-900">
    Home
  </a>
  <span className="text-gray-400">/</span>
  <a href="/products" className="text-gray-600 hover:text-gray-900">
    Products
  </a>
  <span className="text-gray-400">/</span>
  <span className="text-gray-900 font-medium">Item Details</span>
</nav>
```

## Lists

### Simple List

```jsx
<ul className="space-y-3">
  <li className="flex items-start gap-3">
    <svg
      className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path
        fillRule="evenodd"
        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
        clipRule="evenodd"
      />
    </svg>
    <span className="text-gray-700">First item in the list</span>
  </li>
  <li className="flex items-start gap-3">
    <svg
      className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path
        fillRule="evenodd"
        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
        clipRule="evenodd"
      />
    </svg>
    <span className="text-gray-700">Second item</span>
  </li>
</ul>
```

## Alerts & Messages

### Info Alert

```jsx
<div
  className="
  p-4
  bg-blue-50
  border-l-4 border-blue-500
  rounded-r-lg
"
>
  <div className="flex gap-3">
    <svg
      className="w-5 h-5 text-blue-500 flex-shrink-0"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path
        fillRule="evenodd"
        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
        clipRule="evenodd"
      />
    </svg>
    <div>
      <p className="text-sm font-medium text-blue-900">Note</p>
      <p className="text-sm text-blue-700 mt-1">
        Your account has been updated successfully.
      </p>
    </div>
  </div>
</div>
```

### Success Alert

```jsx
<div className="p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
  <p className="text-sm font-medium text-green-900">
    Success! Your changes have been saved.
  </p>
</div>
```

### Error Alert

```jsx
<div className="p-4 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
  <p className="text-sm font-medium text-red-900">
    Error: Unable to process your request.
  </p>
</div>
```

## Modals & Overlays

### Modal Structure

```jsx
<div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
  <div
    className="
    bg-white
    rounded-lg
    max-w-md w-full
    shadow-xl
  "
  >
    {/* Header */}
    <div className="px-6 py-4 border-b border-gray-200">
      <h2 className="text-xl font-semibold text-gray-900">Confirm Action</h2>
    </div>

    {/* Body */}
    <div className="px-6 py-4">
      <p className="text-base text-gray-700">
        Are you sure you want to proceed? This action cannot be undone.
      </p>
    </div>

    {/* Footer */}
    <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-end gap-3">
      <button className="px-4 py-2 bg-gray-100 text-gray-900 rounded-lg">
        Cancel
      </button>
      <button className="px-4 py-2 bg-blue-600 text-white rounded-lg">
        Confirm
      </button>
    </div>
  </div>
</div>
```

This component library ensures consistent, professional UI across your entire application.
