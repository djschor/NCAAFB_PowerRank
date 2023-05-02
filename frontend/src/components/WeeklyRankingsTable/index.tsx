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

export type QBWeekType = {
  player: string;
  team: string;
  opponent_name: string;
  week: number;
  year: number;
  aqs: number;
  qpi: number;
  sei: number;
  crae: number;
  dmi: number;
  ppi: number;
  adpsr: number;
  reer: number;
  defense_score: number;
  aqs_relative_score: number;
  aqs_relative_rank: number;
  qpi_relative_score: number;
  qpi_relative_rank: number;
  sei_relative_score: number;
  sei_relative_rank: number;
  crae_relative_score: number;
  crae_relative_rank: number;
  dmi_relative_score: number;
  dmi_relative_rank: number;
  ppi_relative_score: number;
  ppi_relative_rank: number;
  adpsr_relative_score: number;
  adpsr_relative_rank: number;
  reer_relative_score: number;
  reer_relative_rank: number;
  defense_score_relative_score: number;
  defense_score_relative_rank: number;
  aqs_competitive_score: number;
  aqs_competitive_rank: number;
  qpi_competitive_score: number;
  qpi_competitive_rank: number;
  sei_competitive_score: number;
  sei_competitive_rank: number;
  crae_competitive_score: number;
  crae_competitive_rank: number;
  dmi_competitive_score: number;
  dmi_competitive_rank: number;
  ppi_competitive_score: number;
  ppi_competitive_rank: number;
  adpsr_competitive_score: number;
  adpsr_competitive_rank: number;
  reer_competitive_score: number;
  reer_competitive_rank: number;
  defense_score_competitive_score: number;
  defense_score_competitive_rank: number;
  qb_relative_score: number;
  qb_competitive_score: number;
  qb_total_score: number;
  qb_total_rank: number;
};

interface MainProps {
    data: QBWeekType[];
  }
interface Response {
    headers: Headers;
    ok: boolean;
    redirected: boolean;
    status: number;
    statusText: string;
    type: ResponseType;
    url: string;
    data: QBWeekType[];
  }
  
  

function Main({ data }: MainProps) {
  const tableRef = createRef<HTMLDivElement>();
  const tabulator = useRef<Tabulator>();
  const [filter, setFilter] = useState({
    field: "player",
    type: "like",
    value: "",
  });
  const getColor = (score: number, min: number, max:number) => {
    const range = max - min;
    const value = (score - min) / range;

    if (value < 0.5) {
      return `hsl(348, ${(1 - value * 2) * 100}%, 40%)`;
    } else {
      return `hsl(112, ${(value - 0.5) * 2 * 100}%, 40%)`;
    }
  };
  const applyFilter = () => {
    if (tabulator.current) {
      tabulator.current.setFilter(filter.field, filter.type, filter.value);
    }
  };
  const imageAssets = import.meta.glob<{
    default: string;
  }>("/src/assets/images/fakers/*.{jpg,jpeg,png,svg}", { eager: true });

  const initTabulator = () => {
    if (tableRef.current) {
      tabulator.current = new Tabulator(tableRef.current, {
        data: data,
        paginationMode: "local",
        filterMode: "local",
        sortMode: "local",
        printAsHtml: true,
        pagination: true,
        printStyled: true,
        tableBuilt: function () {
          applyFilter();
        },
  
        paginationSize: 10,
        paginationSizeSelector: [10, 20, 30, 40],
        // layout: "fitColumns",
        responsiveLayout: "collapse",
        placeholder: "No matching records found",
        columns: [
          {
            title: "RANK",
            minWidth: 50,
            maxWidth: 80,
            field: "qb_total_rank",
            vertAlign: "middle",
            print: false,
            download: false,
            },
          {
            title: "PLAYER",
            minWidth: 100,
            maxWidth: 130,
            field: "player",
            vertAlign: "middle",
            print: false,
            download: false,
            formatter(cell) {
                const response: QBWeekType = cell.getData() as QBWeekType;
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
              title: "TEAM",
              minWidth: 100,
              maxWidth: 100,
              field: "team",
              vertAlign: "middle",
              print: false,
              download: false,
              formatter(cell) {
                  const response: QBWeekType = cell.getData() as QBWeekType;
                  const team_url = teamLogoUrls[response.team] || "";
                
                  return `<div className="flex flex-col items-center">
                    <div class="intro-x w-10 h-10 image-fit">
                      <img alt="${response.team}" class="rounded-full" src="${team_url}">
                    </div>
                    <div class="ml-1 -mt-1">
                      <div class="text-gray-600">${response.team}</div>
                    </div>
                  </div>`;
                },
              },  
            {
              title: "WEEK",
              minWidth: 50,
              maxWidth: 80,
              field: "week",
              vertAlign: "middle",
              print: false,
              download: false,
              },
              {
                title: "OPPONENT",
                minWidth: 100,
                maxWidth: 100,
                field: "opponent",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter(cell) {
                    const response: QBWeekType = cell.getData() as QBWeekType;
                    const team_url = teamLogoUrls[response.opponent_name] || "";
                  
                    return `<div className="flex flex-col items-center">
                      <div class="intro-x w-10 h-10 image-fit">
                        <img alt="${response.opponent_name}" class="rounded-full" src="${team_url}">
                      </div>
                      <div class="ml-1 -mt-1">
                        <div class="text-gray-600">${response.opponent_name}</div>
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
            download: false,
            formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 0, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={2}  />);
                return `<div style="-ml-10  display: flex; flex-direction: column; align-items: center;">
                              <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                              <div>${progress}</div>
                            </div>`;
                  },
            },
           
            {
                title: "AQS SCORE",
                minWidth: 50,
                maxWidth: 85,
                field: "aqs_competitive_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 0, 100);
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
                field: "qpi_competitive_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 0, 100);
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
                field: "ppi_competitive_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 0, 100);
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
                field: "sei_competitive_score",
                vertAlign: "middle",
                print: false,
                download: false,
                formatter: (cell) => {
                const score = cell.getValue();
                const color = getColor(score, 0, 100);
                const progress = ReactDOMServer.renderToString(<CategoryProgress percentage={Number(score.toFixed(2))} colorNumber={3} />);
                return `<div style="display: flex; flex-direction: column; align-items: center;">
                            <div style="color: ${color}; font-weight: bold; font-size: 16px; margin-bottom: 5px;">${score.toFixed(2)}</div>
                            <div>${progress}</div>
                        </div>`;
                },
            },
            ],
        });
        }
    };

    useEffect(() => {
      initTabulator();
      }, []);

    useEffect(() => {
      applyFilter();
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