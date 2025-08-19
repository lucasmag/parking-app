/** @type {import('tailwindcss').Config} */
import colors from "./colors";
export const content = [
  './app/**/*.{js,ts,jsx,tsx}',
  './components/**/*.{js,ts,jsx,tsx}',
];
export const presets = [require("nativewind/preset")];
export const theme = {
  extend: {
    colors: colors,
    fontFamily: {
        // Default body font
        'sans': ['Inter-Regular'],
        
        // Display fonts (Space Grotesk)
        'display': ['SpaceGrotesk-Regular'],
        'display-light': ['SpaceGrotesk-Light'],
        'display-medium': ['SpaceGrotesk-Medium'],
        'display-semibold': ['SpaceGrotesk-SemiBold'],
        'display-bold': ['SpaceGrotesk-Bold'],
        
        // Body fonts (Inter)
        'body': ['Inter-Regular'],
        'body-light': ['Inter-Light'],
        'body-medium': ['Inter-Medium'],
        'body-semibold': ['Inter-SemiBold'],
        'body-bold': ['Inter-Bold'],
      },
    borderRadius: {
      DEFAULT: "0.5rem",
      md: "0.75rem",
      lg: "1rem",
      full: "9999px",
    },
    boxShadow: {
      card: "0 2px 8px 0 rgba(16, 30, 54, 0.06)",
      button: "0 1px 3px 0 rgba(37, 99, 235, 0.15)",
    },
  },
};
export const plugins = [];

