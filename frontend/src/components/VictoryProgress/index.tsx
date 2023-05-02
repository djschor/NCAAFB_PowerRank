import React, { FC } from 'react';

interface VictoryProgressProps {
  percentage: number;
  height: number;
}

const VictoryProgress: FC<VictoryProgressProps> = ({ percentage, height }) => {
  const colorMap = [
    { value: 0, color: '#93051D' },
    { value: 40, color: '#C47118' },
    { value: 60, color: '#E6BC00' },
    { value: 80, color: '#7EA40D' },
    { value: 100, color: '#095615' },
  ];

  function calculateColor(value: number) {
    const matchedColor = colorMap.reduce((prev, curr) => (value >= curr.value ? curr : prev));
    return matchedColor.color;
  }

  const createNotches = () => {
    const notches = [];
    for (let i = 0; i <= 100; i += 10) {
      notches.push(
        <rect key={i} x={`${i}%`} y={0} width={1} height={height} fill="rgba(255, 255, 255, 0.4)" />
      );
    }
    return notches;
  };

  const createColoredRects = () => {
    const rects = [];
    for (let i = 0; i < percentage; i++) {
      rects.push(
        <rect key={i} x={`${i}%`} y={0} width="1%" height={height} fill={calculateColor(i)} />
      );
    }
    return rects;
  };

  return (
    <svg width="100%" height={height}>
      {createColoredRects()}
      <rect x={`${percentage}%`} y="0" width={`${100 - percentage}%`} height={height} rx="0" ry="0" fill="#eee" />
      <g>{createNotches()}</g>
      <text
        x="50%"
        y="50%"
        dominantBaseline="central"
        textAnchor="middle"
        fontSize={`${height / 2.3}px`}
        fontWeight="bold"
        fill="#fff"
      >
        {`${percentage}`}
      </text>
    </svg>
  );
};

export default VictoryProgress;
