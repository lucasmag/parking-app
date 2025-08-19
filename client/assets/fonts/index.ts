export const fonts = {
  // Display font for headers, buttons, prices
  display: {
    light: 'SpaceGrotesk-Light',
    regular: 'SpaceGrotesk-Regular',
    medium: 'SpaceGrotesk-Medium',
    semiBold: 'SpaceGrotesk-SemiBold',
    bold: 'SpaceGrotesk-Bold',
  },
  // Body font for readable text
  body: {
    light: 'Inter-Light',
    regular: 'Inter-Regular',
    medium: 'Inter-Medium',
    semiBold: 'Inter-SemiBold',
    bold: 'Inter-Bold',
  },
} as const;

export type FontFamily = 'display' | 'body';
export type FontWeight = keyof typeof fonts.display;
