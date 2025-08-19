import React from 'react';
import Svg, { Path, Rect } from 'react-native-svg';

export default function Chart(props: { solid?: boolean }) {
  if (props.solid) {
    return (
      <Svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <Path d="M17 2C19.8284 2 21.2424 2.00023 22.1211 2.87891C22.9998 3.75759 23 5.17157 23 8V16C23 18.8284 22.9998 20.2424 22.1211 21.1211C21.2424 21.9998 19.8284 22 17 22H7C4.17157 22 2.75759 21.9998 1.87891 21.1211C1.00023 20.2424 1 18.8284 1 16V8C1 5.17157 1.00023 3.75759 1.87891 2.87891C2.75759 2.00023 4.17157 2 7 2H17ZM8 10.001C7.44783 10.0011 7 10.4488 7 11.001V17.001C7.00035 17.5529 7.44804 18.0008 8 18.001C8.55196 18.0008 8.99965 17.5529 9 17.001V11.001C9 10.4488 8.55217 10.0011 8 10.001ZM12 12C11.4479 12.0001 11.0001 12.4479 11 13V17C11.0003 17.552 11.448 17.9999 12 18C12.552 17.9999 12.9998 17.552 13 17V13C12.9999 12.4479 12.5521 12.0001 12 12ZM16 8C15.448 8.00013 15.0002 8.44797 15 9V17C15.0003 17.552 15.448 17.9999 16 18C16.552 17.9999 16.9998 17.552 17 17V9C16.9998 8.44797 16.552 8.00013 16 8Z" fill="#1F1F1F" />
      </Svg>
    );
  }

  return (
    <Svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <Path d="M8 11L8 17" stroke="#1F1F1F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <Path d="M12 13V17" stroke="#1F1F1F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <Path d="M16 9V17" stroke="#1F1F1F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <Rect x="2" y="3" width="20" height="18" rx="2" stroke="#1F1F1F" strokeWidth="2" />
    </Svg>

  );
}