import React, { useEffect, useState, useRef, createRef } from 'react';
import { TabulatorFull as Tabulator } from 'tabulator-tables';
import { teamLogoUrls } from '../../../data/imageUrls';
import ProgressGauge from "../../../components/VictoryProgress";
import ReactDOMServer from 'react-dom/server';

type PlayerData = {
  player: string;
  opponent_name: string;
  team: string;
  week: number;
  qb_total_score: number;
  qb_total_rank: number;
  excitement_index: number;
};

type Props = {
  data: PlayerData[];
};

const Main: React.FC<Props> = ({ data }) => {
  console.log('WEEKRANKS PROPS: ', data)
  const [sortedData, setSortedData] = useState<PlayerData[]>([]);
  const tableRef = createRef<HTMLDivElement>();
  const tabulator = useRef<Tabulator>();
  const gaugeHeight = 20;

  const getColor = (score: number, min: number, max:number) => {
    const range = max - min;
    const value = (score - min) / range;

    if (value < 0.5) {
      return `hsl(348, ${(1 - value * 2) * 100}%, 40%)`;
    } else {
      return `hsl(112, ${(value - 0.5) * 2 * 100}%, 40%)`;
    }
  };

  useEffect(() => {
    async function sortDataByWeek(data: PlayerData[]) {
      const dataCopy = data.slice();
      dataCopy.sort((a, b) => b.qb_total_score - a.qb_total_score);
      setSortedData(dataCopy);
    }

    sortDataByWeek(data);
  }, [data]);

  useEffect(() => {
    if (tableRef.current) {
      tabulator.current = new Tabulator(tableRef.current, {
        data: sortedData,
        layout: 'fitColumns',
        responsiveLayout: 'collapse',
        columns: [
          { title: 'Week #', field: 'week', hozAlign: 'center', width: 90 },
          
          {
            title: 'Opponent',
            field: 'opponent_name',
            hozAlign: 'left',
            width: 150,
            formatter: (cell) => {
              const team = cell.getValue();
              return `<img src="${teamLogoUrls[team]}" alt="${team} logo" class="h-6 w-6 mr-2" />${team}`;
            },
          },
          {
            title: 'QB PowerScore',
            field: 'qb_total_score',
            hozAlign: 'center',
            width: 200,
            formatter: (cell) => {
              const score = cell.getValue();
              const color = getColor(score, 0, 100);
              const progress = ReactDOMServer.renderToString(<ProgressGauge percentage={Number(score.toFixed(2))} height={gaugeHeight} />);
              return `<div>
                        <div style="color: ${color}; font-weight: bold; font-size: 16px;">${score.toFixed(2)}</div>
                        <div>${progress}</div>
                      </div>`;
            },
          },
          {
            title: 'FBS Rank',
            field: 'qb_total_rank',
            hozAlign: 'center',
            width: 120,
            formatter: (cell) => {
              const rank = cell.getValue();
              return `#${rank}`;
            },
          },
          {
            title: 'Relative Rank',
            field: 'qb_total_rank',
            hozAlign: 'center',
            width: 120,
            formatter: (cell) => {
              const rank = cell.getValue();
              return `#${rank}`;
            },
          }
          
          
        ],
    });
  }
}, [sortedData]);

return (
  <div className="col-span-12 intro-y box lg:col-span-6 mb-6">
    <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
      <h2 className="mr-auto text-base font-medium">Top Performances by Week</h2>
    </div>
    <div className="p-5 mt-5 intro-y box">
      <div className="overflow-x-auto scrollbar-hidden">
        <div id="tabulator" ref={tableRef} className="w-full"></div>
      </div>
    </div>
  </div>
);
};

export default Main;

