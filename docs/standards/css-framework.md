# CSS Framework

Tailwind 3.x via PostCSS build pipeline. No CDN. No raw utility chains in templates for defined patterns.

## Build Pipeline

PostCSS with three plugins, in order:

1. `postcss-import` — resolves `@import` statements
2. `tailwindcss` — generates utility classes, processes `@apply`
3. `autoprefixer` — adds vendor prefixes

`postcss.config.js`:
```js
module.exports = {
  plugins: [
    require('postcss-import'),
    require('tailwindcss'),
    require('autoprefixer'),
  ],
};
```

Build command: `npm run build:css` (defined in `package.json`). Run after any CSS change. In development, use `--watch`.

## File Structure

```
static/
  css/
    main.css          # entry point — imports and global resets only
    <appname>.css     # component classes for this app
    dist/
      main.css        # compiled output — what templates reference
```

`main.css` example:
```css
@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";
@import "./myapp.css";
```

Templates always link `static/css/dist/main.css`. Never link source files directly.

## Component Class Convention

Create a component class when a utility pattern repeats more than twice across templates.

Rule: if you find yourself writing `class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"` in three places, it becomes `.btn-primary`.

When NOT to create a component class: one-off layout, page-specific spacing, or anything that varies per context.

## How to Add a Component

1. Write the class in `static/css/<appname>.css` using `@apply`:

```css
/* static/css/myapp.css */
.btn-primary {
  @apply px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 font-medium;
}

.card {
  @apply bg-white rounded-lg shadow p-6;
}

.form-input {
  @apply w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500;
}
```

2. Rebuild: `npm run build:css`

3. Use the class in templates:

```html
<button class="btn-primary">Save Farm</button>
<div class="card">...</div>
<input class="form-input" type="text" name="name">
```

## Template Rules

- Use component classes for all defined patterns — never repeat raw utility chains
- Raw utilities are fine for one-off layout and spacing that won't repeat
- Form fields use `.form-input`, buttons use `.btn-primary` / `.btn-secondary`, containers use `.card`
- Never reference `static/css/main.css` or `static/css/<appname>.css` directly from templates — only `static/css/dist/main.css`
