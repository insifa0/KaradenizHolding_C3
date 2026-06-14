---
name: Cognitive Studio
colors:
  surface: '#fdf8f6'
  surface-dim: '#ddd9d7'
  surface-bright: '#fdf8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f7f3f1'
  surface-container: '#f1edeb'
  surface-container-high: '#ebe7e5'
  surface-container-highest: '#e6e2e0'
  on-surface: '#1c1b1b'
  on-surface-variant: '#414750'
  inverse-surface: '#31302f'
  inverse-on-surface: '#f4f0ee'
  outline: '#727782'
  outline-variant: '#c1c7d2'
  surface-tint: '#1260a5'
  primary: '#004277'
  on-primary: '#ffffff'
  primary-container: '#005a9e'
  on-primary-container: '#b1d1ff'
  inverse-primary: '#a2c9ff'
  secondary: '#5e5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e0dfde'
  on-secondary-container: '#626362'
  tertiary: '#004279'
  on-tertiary: '#ffffff'
  tertiary-container: '#005aa1'
  on-tertiary-container: '#b3d1ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d3e4ff'
  primary-fixed-dim: '#a2c9ff'
  on-primary-fixed: '#001c38'
  on-primary-fixed-variant: '#004881'
  secondary-fixed: '#e3e2e1'
  secondary-fixed-dim: '#c7c6c5'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#464746'
  tertiary-fixed: '#d3e3ff'
  tertiary-fixed-dim: '#a3c9ff'
  on-tertiary-fixed: '#001c39'
  on-tertiary-fixed-variant: '#004883'
  background: '#fdf8f6'
  on-background: '#1c1b1b'
  surface-variant: '#e6e2e0'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-code:
    fontFamily: jetbrainsMono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  sidebar-width: 240px
  test-panel-width: 360px
  gutter: 24px
  stack-gap: 16px
  inline-gap: 8px
  container-padding: 32px
---

## Brand & Style

The design system focuses on a **Corporate Modern** aesthetic tailored for enterprise-grade AI orchestration. The brand personality is professional, reliable, and utilitarian, positioning the platform as a high-stakes productivity tool rather than a novelty. It avoids typical "AI tropes" like neon glows or dark-mode-centric sci-fi elements in favor of a bright, airy, and high-clarity environment.

The visual narrative relies on **Minimalism** with a focus on depth through structural layering rather than decoration. It draws inspiration from modern enterprise software where content clarity is paramount. By using generous whitespace and a restricted color palette, the system ensures that complex chatbot configurations remain scannable and manageable.

## Colors

The palette is anchored by a high-trust **Corporate Blue** primary, used intentionally for calls to action and active states. The foundation of the UI is strictly light-mode, utilizing various shades of off-white and cool gray to differentiate between functional zones without introducing visual noise.

- **Primary:** A deep, authoritative blue for critical interactions.
- **Secondary/Surface:** A subtle light gray used for sidebar backgrounds and container fills to create a "recessed" feel.
- **Neutral:** Dark charcoal for text to maintain high contrast and accessibility.
- **Border:** A consistent, light gray used to define boundaries in lieu of shadows.

## Typography

This design system utilizes **Inter** for its neutral, highly legible character, which excels in data-heavy SaaS environments. The hierarchy is tight, with small step increments to accommodate dense information displays typical of analytics and configuration screens.

For developer-centric areas (API keys, JSON previews), **JetBrains Mono** provides technical clarity. Mobile scaling is handled by reducing the `display-lg` to 24px to ensure headers do not wrap excessively in the bot testing panel.

## Layout & Spacing

The layout follows a **structured three-pane architecture**:
1.  **Global Navigation:** A fixed left sidebar (collapsed or expanded) for primary platform modules.
2.  **Configuration Workspace:** A fluid central area that uses a max-width of 1200px for readability, centered within the remaining space.
3.  **Utility Panel:** A right-aligned, fixed-width panel specifically for the "Test your bot" interface.

The grid is fluid between breakpoints, but relies on consistent 8px increments. Gutters are kept wide (24px) to maintain the "airy" feel even when screens are populated with complex list data. On mobile, the sidebar collapses into a hamburger menu and the test panel becomes a full-screen overlay.

## Elevation & Depth

This design system rejects heavy shadows in favor of **Low-Contrast Outlines** and **Tonal Layering**. 

- **Surface Level 0:** The main page background (`#FFFFFF`).
- **Surface Level 1:** Sidebar and secondary panels (`#FAF9F8`) with a 1px border (`#EDEBE9`).
- **Interactive Elements:** Buttons and input fields use a subtle 1px border.
- **Floating Elements:** Only high-context menus and modals receive a soft, diffused shadow (0px 4px 12px, 5% opacity) to signify they exist above the workspace.

Depth is communicated primarily through vertical stacking and color recession rather than physical height metaphors.

## Shapes

The shape language is **Soft** and disciplined. A standard radius of 4px (`rounded-sm`) is used for input fields and small buttons to maintain a professional, sharp look. Larger containers like cards and the chat bubble in the test panel use 8px (`rounded-lg`) to provide a subtle approachable touch without feeling "bubbly."

Chat avatars and status indicators are the only purely circular (pill-shaped) elements, allowing them to stand out against the geometric grid of the configuration UI.

## Components

### Buttons
- **Primary:** Solid `#005A9E` with white text. 4px radius. 
- **Secondary:** White background with `#EDEBE9` border and `#323130` text.
- **Ghost:** No border or background, transitions to a light gray fill on hover.

### Chat Interface (Test Panel)
- **User Bubbles:** Light gray background with right alignment.
- **AI Bubbles:** Transparent background with a subtle left-hand border in primary blue to indicate the bot is speaking.
- **Input Area:** A multi-line text area at the bottom of the panel with a persistent "Send" icon and "Attach" icon.

### Navigation Sidebar
- **Active State:** A 3px vertical "primary blue" bar on the left edge of the menu item, accompanied by a subtle light blue tint across the background of the item.
- **Icons:** Thin-stroke 20px icons aligned with text.

### Inputs & Cards
- **Form Fields:** 1px solid border. Focus state uses a 2px primary blue ring.
- **Cards:** White background, 1px border, 8px radius. Used to group configuration sections (e.g., "Bot Identity," "Model Settings").