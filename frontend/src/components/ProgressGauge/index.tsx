import React, { FC } from 'react';
import { VictoryPie, VictoryContainer } from 'victory';

interface ProgressGaugeProps {
  percentage: number;
}

const ProgressGauge: FC<ProgressGaugeProps> = ({ percentage }) => {
  const data = [
    { x: 'Progress', y: percentage },
    { x: 'Remaining', y: 100 - percentage },
  ];

  const gradientColors = [
    { offset: '0%', stopColor: '#b22222' },
    { offset: '50%', stopColor: '#ff8c00' },
    { offset: '100%', stopColor: '#228b22' },
  ];

  return (
    <svg width="100" height="50">
      <defs>
        <linearGradient id="chart-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          {gradientColors.map((color, index) => (
            <stop key={index} offset={color.offset} stopColor={color.stopColor} />
          ))}
        </linearGradient>
      </defs>
      <VictoryPie
        standalone={false}
        data={data}
        width={100}
        height={100}
        innerRadius={30}
        cornerRadius={12}
        padAngle={2}
        startAngle={-90}
        endAngle={90}
        containerComponent={<VictoryContainer responsive={false} />}
        style={{
          data: {
            fill: ({ datum }) => (datum.x === 'Progress' ? 'url(#chart-gradient)' : 'transparent'),
          },
        }}
      />
    </svg>
  );
};

export default ProgressGauge;
