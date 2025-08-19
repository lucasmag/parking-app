import React from 'react';
import { Text, TextProps, TextStyle } from 'react-native';
import { fonts, FontFamily, FontWeight } from '@/assets/fonts';

interface TypographyProps extends TextProps {
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'body' | 'body-large' | 'body-small' | 'caption' | 'button' | 'price' | 'label';
  family?: FontFamily;
  weight?: FontWeight;
  color?: string;
  children: React.ReactNode;
}

const getVariantStyles = (
  variant: TypographyProps['variant'], 
  family?: FontFamily
): TextStyle => {
  const baseStyles: Record<string, TextStyle> = {
    // Headers - Use display font by default
    h1: { fontSize: 32, lineHeight: 38, fontFamily: fonts.display.bold },
    h2: { fontSize: 28, lineHeight: 34, fontFamily: fonts.display.bold },
    h3: { fontSize: 24, lineHeight: 30, fontFamily: fonts.display.semiBold },
    h4: { fontSize: 20, lineHeight: 26, fontFamily: fonts.display.semiBold },
    h5: { fontSize: 18, lineHeight: 24, fontFamily: fonts.display.medium },
    
    // Body text - Use body font
    'body-large': { fontSize: 18, lineHeight: 26, fontFamily: fonts.body.regular },
    body: { fontSize: 16, lineHeight: 24, fontFamily: fonts.body.regular },
    'body-small': { fontSize: 14, lineHeight: 20, fontFamily: fonts.body.regular },
    caption: { fontSize: 12, lineHeight: 16, fontFamily: fonts.body.regular },
    
    // Special variants
    button: { fontSize: 16, lineHeight: 20, fontFamily: fonts.display.semiBold },
    price: { fontSize: 20, lineHeight: 24, fontFamily: fonts.display.bold },
    label: { fontSize: 14, lineHeight: 18, fontFamily: fonts.body.medium },
  };

  const style = baseStyles[variant || 'body'];
  
  if (family) {
    style.fontFamily = fonts[family].regular;
  }

  return style;
};

const getFontFamily = (family: FontFamily, weight: FontWeight) => {
  return fonts[family][weight];
};

export const Typography: React.FC<TypographyProps> = ({
  variant = 'body',
  family,
  weight,
  color = '#000000',
  style,
  children,
  ...props
}) => {
  const variantStyles = getVariantStyles(variant, family);
  
  // Determine final font family
  let fontFamily = variantStyles.fontFamily;
  if (family && weight) {
    fontFamily = getFontFamily(family, weight);
  } else if (weight) {
    // Default to body family if only weight is specified
    fontFamily = getFontFamily(family || 'body', weight);
  }

  const textStyle: TextStyle = {
    ...variantStyles,
    fontFamily,
    color,
  };

  return (
    <Text style={[textStyle, style]} {...props}>
      {children}
    </Text>
  );
};
