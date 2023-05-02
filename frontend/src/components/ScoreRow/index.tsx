import React, { useEffect, useState } from 'react';
import ProgressGauge from "../../components/VictoryProgress";
import Tippy from "../../base-components/Progress";
import Lucide from "../../base-components/Lucide";
import _ from "lodash";

type MainProps = {
  rank: number;
  score: number;
  text: string;
  big: boolean;
  label: string;
  
};

export const getColorScore = (value: number): string => {
  const colors = ["#f44336", "#ff5722", "#ffc107", "#8bc34a", "#4caf50"];
  const min = 0;
  const max = 100;
  const range = max - min;
  const valueRange = value - min;
  let index = Math.round((valueRange / range) * (colors.length - 1));
  if (index >= colors.length) {
    index = colors.length - 1;
  } else if (index === 1) {
    index = 2;
  } else if (index === 2) {
    index = 3;
  }
  return colors[index];
};

export const getColorRank = (rank: number): string => {
  const maxRank = 100;
  const hue = Math.floor((1 - rank / maxRank) * 120);
  const rgb = `hsl(${hue}, 60%, 50%)`;
  return rgb;
};


const Main: React.FC<MainProps> = (props) => {
  const rank = props.rank;
  const rankColor = getColorRank(rank);

  const score = props.score;
  const scoreColor = getColorScore(score);

  const text = props.text;
  const big = props.big;

  const textSize = big ? 'text-lg' : 'text-md';
  const gaugeHeight = big ? 25 : 20;

  const marginSize = big ? 'mb-4' : '-mb-.5';
  const progressBarWidthClass = big ? 'w-full' : 'w-1/2';

  return (
<div className="px-5 py-2 h-50">
  <div className={`${marginSize} flex items-center`}>
    <div className="w-1/5 flex items-center">
      <span className={`font-medium mr-4 font-extrabold ${textSize}`} style={{ minWidth: '100px' }}>{props.label}:</span>
      <div className="">
        <Lucide icon="Info" className="w-3 h-3" />
      </div>
    </div>
    <div className="flex-grow">
      <div className="flex items-center">
        <div className="w-1/5 ml-6">
          <span className={`font-medium font-bold ${textSize}`} style={{ color: scoreColor }}>
            {score.toFixed(2)}
          </span>
        </div>
        <div className="w-3/5">
          <ProgressGauge percentage={Number(score.toFixed(2))} height={gaugeHeight} />
        </div>
        <div className="w-1/5 ml-4">
          <span className={`font-medium mr-4 ${textSize}`}>FBS Rank:</span>
          <span className={`font-medium ${textSize}`} style={{ color: rankColor }}>
            # {rank}
          </span>
        </div>
      </div>
    </div>
  </div>
  {text}
</div>



  
    // </div>
  );
};

export default Main;
