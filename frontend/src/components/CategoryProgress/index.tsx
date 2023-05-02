import React, { FC } from 'react';

interface mainProps {
  percentage: number;
  colorNumber: number;
}

const colors = [
    ["#fce4ec", "#f8bbd0", "#f48fb1", "#f06292", "#ec407a", "#e91e63", "#d81b60", "#c2185b", "#ad1457"],
    ["#fce8b2", "#fadb6a", "#f7c41f", "#f2a900", "#e68700", "#dc6100", "#c43e00", "#a21700", "#7f0000"],
    ["#ebf5fb", "#d0eafb", "#a8d7f7", "#7ebff2", "#55a8ed", "#3d8ee2", "#2b6fbd", "#1a5199", "#093375"],
    ["#e0f2f1", "#b2dfdb", "#80cbc4", "#4db6ac", "#26a69a", "#009688", "#00897b", "#00796b", "#00695c"],
    ["#fff3e0", "#ffe0b2", "#ffcc80", "#ffb74d", "#ffa726", "#ff9800", "#f57c00", "#ef6c00", "#e65100"],
    ["#efebe9", "#d7ccc8", "#bcaaa4", "#a1887f", "#8d6e63", "#795548", "#6d4c41", "#5d4037", "#4e342e"],
    ["#fff8e1", "#ffecb3", "#ffe082", "#ffd54f", "#ffca28", "#ffc107", "#ffb300", "#ffa000", "#ff8f00"],
    ["#f1f8e9", "#dcedc8", "#c5e1a5", "#aed581", "#9ccc65", "#8bc34a", "#7cb342", "#689f38", "#558b2f"],
    ["#f3e5f5", "#e1bee7", "#ce93d8", "#ba68c8", "#ab47bc", "#9c27b0", "#8e24aa", "#7b1fa2", "#6a1b9a"],
  ];
  
  const height = 15;

  const main: FC<mainProps> = ({ percentage, colorNumber }) => {
    const colorSet = colors[colorNumber % colors.length];
  
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
      const numColors = colorSet.length;
      const step = 100 / numColors;
      for (let i = 0; i < percentage; i++) {
        const fillColor = colorSet[Math.floor(i / step)];
        rects.push(
          <rect key={i} x={`${i}%`} y={0} width="1%" height={height} fill={fillColor} />
        );
      }
      return rects;
    };
  
    return (
      <svg width="100%" height={height}>
        {createColoredRects()}
        <rect x={`${percentage}%`} y="0" width={`${100 - percentage}%`} height={height} rx="0" ry="0" fill="#eee" />
        <g>{createNotches()}</g>
      </svg>
    );
  };
  
  export default main;
  