import React, { FC } from 'react';
import './ProgressBar.css';

interface ProgressBarProps {
  percentage: number;
}

const ProgressBar: FC<ProgressBarProps> = ({ percentage }) => {
  const filledWidth = Math.max(0, Math.min(100, percentage));
  return (
    <div className="progress-container">
      <div className="progress-bar" style={{ width: `${filledWidth}%` }}>
        <div className="progress-notch" />
      </div>
    </div>
  );
};

export default ProgressBar;
