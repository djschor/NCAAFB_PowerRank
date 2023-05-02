import { QBUrls, teamLogoUrls } from '../../data/imageUrls';
import { useEffect, useRef, createRef, useState } from "react";
import { createIcons, icons } from "lucide";
import { TabulatorFull as Tabulator } from "tabulator-tables";
import ProgressGauge from "../../components/VictoryProgress";
import CategoryProgress from "../../components/CategoryProgress";

import ReactDOMServer from 'react-dom/server';
import Progress from "../../base-components/Progress";
import { playerNames } from '../../data/playerNames';
import { Link } from 'react-router-dom';

interface Player {
  player: string;
  team:string;
  year: number;
  aqs_rank: number;
  aqs_score: number;
  avg_aqs: number;
  adpsr_rank: number;
  adpsr_score: number;
  avg_adpsr: number;
  crae_rank: number;
  crae_score: number;
  avg_crae: number;
  defense_score_rank: number;
  defense_score: number;
  dmi_rank: number;
  dmi_score: number;
  avg_dmi: number;
  ppi_rank: number;
  ppi_score: number;
  avg_ppi: number;
  qb_competitive_score_rank: number;
  qb_competitive_score: number;
  avg_qb_competitive_score: number;
  qb_relative_score_rank: number;
  qb_relative_score: number;
  avg_qb_relative_score: number;
  qb_total_score_rank: number;
  qb_total_score: number;
  avg_qb_total_score: number;
  qpi_rank: number;
  qpi_score: number;
  avg_qpi: number;
  reer_rank: number;
  reer_score: number;
  avg_reer: number;
  sei_rank: number;
  sei_score: number;
  avg_sei: number;
}
interface MainProps {
    overallData: Player[];
  }
interface Response {
    headers: Headers;
    ok: boolean;
    redirected: boolean;
    status: number;
    statusText: string;
    type: ResponseType;
    url: string;
    data: Player[];
  }
  
  

function Main({ overallData }: MainProps) {
  const tableRef = createRef<HTMLDivElement>();
  
  const tabulator = useRef<Tabulator>();
  const [filter, setFilter] = useState({
    field: "player",
    type: "like",
    value: "",
  });
  const getColor = (score: number, min: number, max: number): string => {
    const range = max - min;
    const value = (score - min) / range;
  
    // Hue values: 0 (red) to 120 (green)
    const hue = value * 120;
  
    // Saturation values: 100% (no change)
    const saturation = 100;
  
    // Lightness values: 30% (dark green) to 50% (red)
    const lightness = 50 - value * 20;
  
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  };
  
//   const getColorRank = (rank: number): string => {
//     if (rank >= 1 && rank <= 10) {
//       const hue = 120 - (rank - 1) * 8;
//       return `hsl(${hue}, 100%, 30%)`;
//     } else if (rank > 10 && rank <= 30) {
//       const hue = 80 - (rank - 11) * 4;
//       return `hsl(${hue}, 100%, 50%)`;
//     } else if (rank > 30 && rank <= 50) {
//       const hue = 40 - (rank - 31) * 4;
//       return `hsl(${hue}, 100%, 50%)`;
//     } else {
//       const hue = 0;
//       const lightness = 70 - (rank - 50) * 0.6;
//       return `hsl(${hue}, 100%, ${Math.max(lightness, 30)}%)`;
//     }
//   };
  const getColorRank = (rank: number, min: number, max: number): string => {
    const range = max - min;
    const value = (rank - min) / range;
  
    const hue = 120 - value * 120; // Hue values: 120 (green) to 0 (red)
    const saturation = 100;
    const lightness = 30 + value * 30; // Lightness values: 30% (dark green) to 60% (dark red)
  
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  };
  
  
  const imageAssets = import.meta.glob<{
    default: string;
  }>("/src/assets/images/fakers/*.{jpg,jpeg,png,svg}", { eager: true });

  const initTabulator = () => {
    if (tableRef.current) {
        tabulator.current = new Tabulator(tableRef.current, {
        data: overallData,
        layout:"fitColumns",
        paginationMode: "local",
        filterMode: "local",
        sortMode: "local",
        printAsHtml: true,
        pagination: true,
        printStyled: true,
        paginationSize: 10,
        paginationSizeSelector: [10, 20, 30, 40],
        // layout: "fitColumns",
        responsiveLayout: "collapse",
        placeholder: "No matching records found",
        columns: [
          {
            title: "PLAYER",
            minWidth: 100,
            maxWidth: 150,
            field: "player",
            vertAlign: "middle",
            print: false,
            headerSort: false,
            download: false,
            formatter(cell) {
                const response: Player = cell.getData() as Player;
                const qb_url = QBUrls[response.player] || "";
                const lastSpaceIndex = response.player.lastIndexOf(" ");
                const firstName = response.player.slice(0, lastSpaceIndex);
                const lastName = response.player.slice(lastSpaceIndex + 1);
                const formatted_player_name = playerNames[response.player];
                const playerLink = `/qb/${formatted_player_name}`;
              
                return `<div class="flex items-center">
                  <div class="intro-x w-10 h-10 image-fit">
                    <img alt="${response.player}" class="rounded-full" src="${qb_url}">
                  </div>
                  <div class="ml-4">
                    <a href="${playerLink}" class="font-medium">${firstName}</a>
                    <div class="text-gray-600">${lastName}</div>
                  </div>
                </div>`;
              },
              
            },  
            
            {
            title: "QB TOTAL SCORE",
            minWidth: 50,
            maxWidth: 150,
            field: "qb_total_score",
            vertAlign: "middle",
            print: false,
            headerSort: false,
            download: false,
            formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={2}  />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                              <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                              <div>${progress}</div>
                            </div>`;
                  },
            },
            {
                title: "RANK",
                minWidth: 50,
                maxWidth: 85,
                field: "qb_total_score_rank",
                vertAlign: "middle",
                headerSort: false,
                print: false,
                download: false,
                formatter: (cell) => {
                    const rank = cell.getValue();
                    const color = getColorRank(rank, 1, 200);
                    return `<div style="display: flex; flex-direction: column; align-items: center;">
                                    <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${rank.toFixed(2)}</div>
                                </div>`;
                        },
                },
            {
                title: "AQS SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "aqs_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                // const progress = ReactDOMServer.renderToString(<ProgressGauge percentage={Number(score.toFixed(2))} height={15} />);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={1} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            {
                title: "QPI SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "qpi_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={9} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            {
                title: "PPI SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "ppi_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={8} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            {
                title: "SEI SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "sei_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={3} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            {
                title: "CRAE SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "sei_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={4} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            // {
            //     title: "DMI SCORE",
            //     minWidth: 50,
            //     maxWidth: 85,
            //     field: "sei_score",
            //     vertAlign: "middle",
            //     print: false,
            //     download: false,
            //     formatter: (cell) => {
            //     const score = cell.getValue();
            //     const color = getColor(score, 0, 100);
            //     const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={5}/>);
            //     return `<div style="display: flex; flex-direction: column; align-items: center;">
            //                 <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
            //                 <div>${progress}</div>
            //             </div>`;
            //     },
            // },
            {
                title: "ADPSR SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "adpsr_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={6} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            {
                title: "RZER SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "reer_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 60, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={7} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            ],
            // tableBuilt() {
            //     // Call the setFilter function here
            //     tabulator.current.setFilter(filter.field, filter.type, filter.value);
            //   },
      
        });
        }
    };

    useEffect(() => {
    initTabulator();
    }, []);

    useEffect(() => {
    if (tabulator.current) {
    tabulator.current.setFilter(filter.field, filter.type, filter.value);
    }
    }, [filter]);

    return (
    <div className="flex flex-col mt-0">
        <div className="intro-y col-span-12 overflow-auto lg:overflow-visible">
        <div ref={tableRef} />
        </div>
    </div>
    );
}
export default Main;