---
name: Deep Sea Tech
colors:
  surface: '#0b1420'
  surface-dim: '#0b1420'
  surface-bright: '#313a47'
  surface-container-lowest: '#060e1a'
  surface-container-low: '#141c28'
  surface-container: '#18202d'
  surface-container-high: '#222a37'
  surface-container-highest: '#2d3543'
  on-surface: '#dbe3f4'
  on-surface-variant: '#bac9cb'
  inverse-surface: '#dbe3f4'
  inverse-on-surface: '#29313e'
  outline: '#859395'
  outline-variant: '#3b494b'
  surface-tint: '#1edaec'
  primary: '#66efff'
  on-primary: '#00363c'
  primary-container: '#00d4e6'
  on-primary-container: '#00575f'
  inverse-primary: '#006972'
  secondary: '#59d8e5'
  on-secondary: '#00363b'
  secondary-container: '#00a6b3'
  on-secondary-container: '#003439'
  tertiary: '#ccddff'
  on-tertiary: '#1e314e'
  tertiary-container: '#aec1e6'
  on-tertiary-container: '#3d4f6e'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#8df2ff'
  primary-fixed-dim: '#1edaec'
  on-primary-fixed: '#001f23'
  on-primary-fixed-variant: '#004f56'
  secondary-fixed: '#87f3ff'
  secondary-fixed-dim: '#59d8e5'
  on-secondary-fixed: '#001f23'
  on-secondary-fixed-variant: '#004f55'
  tertiary-fixed: '#d6e3ff'
  tertiary-fixed-dim: '#b4c7ec'
  on-tertiary-fixed: '#061b38'
  on-tertiary-fixed-variant: '#354766'
  background: '#0b1420'
  on-background: '#dbe3f4'
  surface-variant: '#2d3543'
typography:
  headline-xl:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  gutter: 24px
  margin-desktop: 48px
  margin-mobile: 20px
  stack-gap: 16px
---

## Brand & Style
The design system is engineered for a premium, high-tech corporate environment, reflecting the innovative and industrial scale of Karadeniz Holding. It utilizes a sophisticated **Glassmorphism** aesthetic blended with **Futuristic Neon** accents to evoke a sense of deep-sea exploration and advanced energy technology.

The UI should feel like a high-end command center: professional, expansive, and precise. By layering semi-transparent surfaces over deep navy gradients and applying vibrant turquoise glows, the system achieves a sense of immense depth and physical presence. The emotional response is one of reliability, prestige, and cutting-edge intelligence.

## Colors
This design system utilizes a "Deep Dark" palette to emphasize luminosity and depth.

- **Primary & Secondary:** Vibrant turquoise (#00d4e6) and cyan (#00a8b5) are reserved for interactive elements, status indicators, and luminous accents. These colors must always appear as though they are emitting light.
- **Backgrounds:** A rich, dark navy gradient moving from `#060e1a` to `#0f2340`.
- **Surfaces:** Semi-transparent variations of the secondary color with 10-15% opacity to create the "glass" effect.
- **Overlays:** Use a subtle mesh gradient in the background to provide texture beneath the glass layers.

## Typography
The typographic scale prioritizes clarity and a modern corporate feel. 

- **Headlines:** Uses **Outfit** for its geometric, clean, and optimistic character. High-level headers should utilize tighter letter spacing to maintain a "tight" professional look.
- **Body & Data:** Uses **Inter** for maximum legibility in technical and data-heavy contexts.
- **Accents:** Use uppercase labels with increased tracking for categorizing data or indicating status, reinforcing the "instrument panel" aesthetic.

## Layout & Spacing
The layout follows a **Fluid Grid** model with generous white space (or "dark space") to prevent the glass elements from feeling cluttered.

- **Grid:** A 12-column grid for desktop with 24px gutters.
- **Sidebar:** A fixed 280px "Glassy" sidebar on desktop, transitioning to a full-screen blurred overlay on mobile.
- **Padding:** Elements within cards should maintain a minimum of 24px internal padding to uphold the premium feel.
- **Breakpoints:** 
  - Mobile: < 768px (1 column)
  - Tablet: 768px - 1024px (6 columns/Adaptive)
  - Desktop: > 1024px (12 columns)

## Elevation & Depth
Elevation is achieved through optical physics rather than standard shadows:

- **Backdrop Blur:** All glass surfaces must have a `16px` to `24px` backdrop-blur filter.
- **Glass Border:** Use a `1px` solid border with 20% white opacity on the top/left and 10% on the bottom/right to simulate light catching the edge.
- **Inner Glow:** Use a subtle `2px` inner-shadow (white or turquoise) with 5% opacity to give surfaces volume.
- **Outer Glow:** Interactive elements (buttons, active cards) use a soft cyan outer glow (`box-shadow: 0 0 20px rgba(0, 212, 230, 0.15)`).
- **Z-Axis:** Higher elevation layers have higher transparency (less opaque) and more blur.

## Shapes
The shape language is sophisticated and modern. A base roundedness of **16px** (Level 2) is applied to all primary containers to soften the high-tech aesthetic and make it feel more approachable.

- **Small Components (Inputs/Chips):** 8px (rounded-md).
- **Standard Cards:** 16px (rounded-lg).
- **Large Sections/Modals:** 24px (rounded-xl).
- **Buttons:** 12px for a balanced, modern touch.

## Components

- **Glass Cards:** The fundamental unit. Background: `rgba(15, 35, 64, 0.6)`. Backdrop-blur: `16px`. Border: `1px solid rgba(255, 255, 255, 0.1)`.
- **Primary Buttons:** Solid Turquoise (#00d4e6) background with black text for high contrast. On hover, apply a 15px cyan glow.
- **Secondary Buttons:** Transparent with a 1px turquoise border and turquoise text. Background becomes `rgba(0, 212, 230, 0.1)` on hover.
- **Input Fields:** Dark navy background (darker than the card) with a subtle inner shadow. On focus, the border glows cyan.
- **Sidebar & Top Bar:** High blur (`32px`) and very low opacity background (`0.4`). Top bar should have a 1px border on the bottom only.
- **Progress Bars & Gauges:** Use linear gradients from Cyan to Turquoise. Add a "bloom" effect (blur) to the filled portion of the bar to simulate energy.
- **Chips:** Small, pill-shaped elements with `rgba(0, 212, 230, 0.15)` background and `0.5px` turquoise border.