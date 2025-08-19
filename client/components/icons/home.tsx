import React from 'react';
import Svg, { Path } from 'react-native-svg';

export default function Home(props: { solid?: boolean }) {
  const color = props.solid ? "#1F1F1F" : "none";

  return (
    <Svg width="24" height="24" viewBox="0 0 24 24" fill={color}>
      <Path d="M8.55993 21.7439H6.2666C3.73345 21.7439 1.67993 19.7292 1.67993 17.2439V10.165C1.67993 8.5914 2.5177 7.13214 3.88932 6.31656L9.62265 2.90747C11.0839 2.03866 12.916 2.03866 14.3772 2.90747L20.1105 6.31656C21.4822 7.13214 22.3199 8.5914 22.3199 10.165V17.2439C22.3199 19.7292 20.2664 21.7439 17.7333 21.7439H15.4399V17.2439C15.4399 15.3799 13.8998 13.8689 11.9999 13.8689C10.1 13.8689 8.55993 15.3799 8.55993 17.2439V21.7439Z" stroke="#1F1F1F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </Svg>
  );
}