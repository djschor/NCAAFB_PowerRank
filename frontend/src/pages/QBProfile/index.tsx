import _ from "lodash";
import React, { useEffect, useState } from 'react';
import Tippy from "../../base-components/Tippy";

import fakerData from "../../utils/faker";
import Button from "../../base-components/Button";
import { FormSwitch } from "../../base-components/Form";
import Progress from "../../base-components/Progress";
import Lucide from "../../base-components/Lucide";
import StackedBarChart1 from "../../components/StackedBarChart1";
import SimpleLineChart from "../../components/SimpleLineChart";
import ApexSparkline from "../../components/ApexSparkLine";
import ScoreRow from "../../components/ScoreRow";
import WeekRanks from "./WeekRanks"
import { Menu, Tab } from "../../base-components/Headless";
import { Tab as HeadlessTab } from "@headlessui/react";
import { useParams } from 'react-router-dom'
import { useQuery } from '@apollo/client';
import { playerNames, formattedPlayerNames } from '../../data/playerNames';
import { QBUrls, teamLogoUrls } from '../../data/imageUrls';
import { getPlayerData, getQBOverallData, getQBOverallDataPlayer, getPlayerMeta } from '../../queries/restQueries';

// import { GetQbDataQuery, GetQbDataQueryVariables } from '../../__generated__/graphql';

// import gql from __generated__/gql folder 
// import { GetQBData } from '../../__generated__/gql';

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

export type QBWeekType = {
  player: string;
  team: string;
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


export const getColorRank = (rank: number): string => {
  const maxRank = 100; // set the maximum rank to 100
  // calculate the hue value based on the rank
  const hue = Math.floor((1 - rank / maxRank) * 120);
  // convert the hue value to an RGB value
  const rgb = `hsl(${hue}, 60%, 50%)`;
  return rgb; // return the RGB color value
};

export const getWeeklyPerformance = (playerData: any[], key: string): any[] => {
  const weeklyPerformance: number[] = [];
  playerData.forEach((weekData) => {
    const value = weekData[key];
    if (value !== undefined) {
      weeklyPerformance.push(value);
    }
  });

  return weeklyPerformance;
};

export function formatHeight(heightInInches: number): string {
  const feet = Math.floor(heightInInches / 12);
  const inches = heightInInches % 12;

  if (feet === 0) {
    return `${inches}"`;
  } else if (inches === 0) {
    return `${feet}'0"`;
  } else {
    return `${feet}' ${inches}"`;
  }
}

function Main() {
  interface FormattedPlayerNames {
    [key: string]: string;
  }
  const formattedPlayerNamesTyped = formattedPlayerNames as FormattedPlayerNames;
  const { qb_name } = useParams<{ qb_name: string | undefined }>();
  const formatted_qb_name = qb_name ? formattedPlayerNamesTyped[qb_name] || "" : "";
  const qb_url = QBUrls[formatted_qb_name] || "";
  const [overallData, setOverallData] = useState<any>(null);

  useEffect(() => {
    // fetching qb overall data
    const fetchOverallPlayerData = async () => {
      const baseUrl = 'https://shrouded-shore-60391.herokuapp.com';
      const data = await getQBOverallDataPlayer(baseUrl, formatted_qb_name);
      console.log('qb overall player:', data);
      setOverallData(data);
      
    };

    if (formatted_qb_name) {
      fetchOverallPlayerData();
    }
  }, [formatted_qb_name]); // Add formatted_qb_name as a dependency

  const [playerData, setPlayerData] = useState<any>(null);
  const [weeklyQbCompetitiveRank, setWeeklyQbCompetitiveRank] = useState<number[]>([]);
  const [weeklyQbRelativeRank, setWeeklyQbRelativeRank] = useState<number[]>([]);
  const [weeklyLabels, setWeeklyLabels] = useState<string[]>([]);
  console.log('weeklyLabels', weeklyLabels)
  const [teamColor, setTeamColor] = useState<any>(null);
  const [teamColorSecondary, setTeamColorSecondary] = useState<any>(null);

  useEffect(() => {
    // fetching qbWeeklyData
    const fetchData = async () => {
        const baseUrl = 'https://shrouded-shore-60391.herokuapp.com';
        const playerName = formatted_qb_name;
        const year = 2022;

        const data = await getPlayerData(baseUrl, playerName, year);
        console.log('qbdata:',  data)
        // const idata: QBWeekType[] = JSON.parse(data);

        function sortDataByWeek(data: QBWeekType[]): QBWeekType[] {
          return data.sort((a, b) => a.week - b.week);
        }
        setPlayerData(sortDataByWeek(data));

        setWeeklyQbCompetitiveRank(getWeeklyPerformance(data, 'qb_total_score'));
        setWeeklyQbRelativeRank(getWeeklyPerformance(data, 'qb_relative_score'));
        const weekLabels = getWeeklyPerformance(data, 'week');
        // sort the weekLabel array of strings containing week numbers
        weekLabels.sort((a, b) => {
          return parseInt(a) - parseInt(b);
        });
        setWeeklyLabels(weekLabels);
        console.log('weeklyLabelsSorted', weeklyLabels)
  
    };
    fetchData();
  }, []);
  const [playerMetaData, setPlayerMetaData] = useState<any>(null);
  const [teamLogo, setTeamLogo] = useState<any>(null);
  console.log('qb META! data:', playerMetaData, typeof playerMetaData)
  useEffect(() => {
    // fetching qbMetaData
    const fetchData = async () => {
        const baseUrl = 'https://shrouded-shore-60391.herokuapp.com';
        const playerName = formatted_qb_name;
        console.log('playerName:', playerName)
        const data = await getPlayerMeta(baseUrl, playerName);
        console.log('qb META data:', data)
        setPlayerMetaData(data);
        setTeamColor(data.teamColor)
        setTeamColorSecondary(data.teamColorSecondary)
        const team_logo_url = teamLogoUrls[data.team] || "";
        setTeamLogo(team_logo_url);

    };
    fetchData();
  }, []);

  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const handleButtonClick = (year: number) => {
    setSelectedYear(year);
  };

  const years = [2022];

  const avgQbTotalScore = overallData?.avg_qb_total_score || 0;
  const qbTotalScoreRank = overallData?.qb_total_score_rank || 50;
  return (
    <>
      <div className="flex items-center mt-8 intro-y">
        <h2 className="mr-auto text-lg font-medium">PowerScore QB Profile</h2>
      </div>
      <div className="container mx-auto">
        <div className="flex space-x-4">
          {years.map((year) => (
            <button
              key={year}
              className={`px-4 py-2 bg-gray-200 rounded ${
                selectedYear === year ? 'bg-blue-500 text-white' : ''
              }`}
              onClick={() => handleButtonClick(year)}
            >
              {year}
            </button>
          ))}
        </div>
      </div>
      <Tab.Group>
        {/* BEGIN: Profile Info */}
        <div className="px-5 pt-5 mt-5 intro-y box">
          <div className="flex flex-col pb-5 -mx-5 border-b lg:flex-row border-slate-200/60 dark:border-darkmode-400">
            <div className="flex items-center justify-center flex-1 px-5 lg:justify-start">
              <div className="relative flex-none w-20 h-20 sm:w-24 sm:h-24 lg:w-32 lg:h-32 image-fit">
                <img
                  alt="QB Image"
                  className="rounded-full"
                  src={qb_url}
                />
              </div>
              <div className="ml-5">
                <div className="w-24 text-lg font-medium truncate sm:w-40 sm:whitespace-normal">
                  {formatted_qb_name}
                </div>
                <div className="relative flex-none w-20 h-20 sm:w-7 sm:h-7 lg:w-7 lg:h-7 image-fit">
                  <img
                    alt="QB Image"
                    className="rounded-full"
                    src={teamLogo}
                  />
                </div>
                <div className="text-slate-500">{playerMetaData ? playerMetaData.team : ''}</div>
                <div className="text-slate-500">#{playerMetaData ? playerMetaData.jersey : ''}</div>
              </div>
            </div>
            <div className="flex-1 px-5 pt-5 mt-6 border-t border-l border-r lg:mt-0 border-slate-200/60 dark:border-darkmode-400 lg:border-t-0 lg:pt-0">
              <div className="font-medium text-center lg:text-left lg:mt-3">
                Player Info
              </div>
              <div className="flex flex-col items-center justify-center mt-4 lg:items-start">
                <div className="flex items-center truncate sm:whitespace-normal">
                  {/* <Lucide icon="Home" className="w-4 h-4 mr-2" /> */}
                  {/* <div className="text-slate-500">{playerMetaData && playerMetaData.length > 0 ? playerMetaData[0].team : ''}</div> */}
                  <p className="text-slate-500">Hometown: </p> {playerMetaData? playerMetaData.hometown: ''}
                </div>
                <div className="flex items-center mt-3 truncate sm:whitespace-normal">
                  {/* <Lucide icon="Instagram" className="w-4 h-4 mr-2" /> Instagram */}
                   <p className="text-slate-500">Height: </p> {playerMetaData? formatHeight(playerMetaData.height): ''}
                </div>
                <div className="flex items-center mt-3 truncate sm:whitespace-normal">
                  
                <p className="text-slate-500">Weight: </p>  {playerMetaData? playerMetaData.weight: ''}
                </div>
              </div>
            </div>
            <div className="flex-1 px-5 pt-5 mt-6 border-t lg:mt-0 lg:border-0 border-slate-200/60 dark:border-darkmode-400 lg:pt-0">
              <div className="font-medium text-center lg:text-left lg:mt-5">
              Weekly PowerScore Rankings
              </div>
              <div className="flex items-center justify-center mt-2 lg:justify-start">
                <div className="flex w-20 mr-2">
                   FBS:{" "}
                </div>
                <div className="col-span-1 -py-2 -ml-5">
                <Tippy content="Relative: ">
                    <Lucide icon="Info" className="w-3 h-3 -ml-1.5" />
                  </Tippy >
                </div>
                <div className="w-3/4">
                {playerData && (
                  <ApexSparkline
                    labels={weeklyLabels}
                    data={weeklyQbCompetitiveRank}
                    lineColor={teamColor}
                    height={"55px"}
                    width={"100%"}
                    className="-mr-5"
                  />
                )}

                  {/* <SimpleLineChart1 labels={weeklyLabels} data={weeklyQbCompetitiveRank} lineColor={playerMetaData? playerMetaData.teamColor: '#FFFF'} height={55} className="-mr-5" /> */}
                </div>
              </div>
              <div className="flex items-center justify-center lg:justify-start">
                <div className="flex w-20 mr-2">
                  Relative: 
                </div>
                <div className="col-span-1 -py-2 -ml-5">
                  <Tippy content="Relative: ">
                    <Lucide icon="Info" className="w-3 h-3 -ml-1.5" />
                  </Tippy >
               </div>
                <div className="w-3/4">
                {/* <ProgressGauge percentage={overallData? overallData.avg_qb_total_score.toFixed(2): 50} /> */}

                {/* <SimpleLineChart1 labels={weeklyLabels} data={weeklyQbCompetitiveRank} lineColor={playerMetaData? playerMetaData.teamColorSecondary: '#FFFF'} height={55} className="-mr-5" /> */}
                {playerData && (
                  <ApexSparkline
                    labels={weeklyLabels}
                    data={weeklyQbCompetitiveRank}
                    lineColor={teamColorSecondary}
                    height={"55"}
                    width={"100%"}
                    className="-mr-5"
                  />
                )}
                </div>
              </div>
            </div>
          </div>
          <Tab.List
            variant="link-tabs"
            className="flex-col justify-center text-center sm:flex-row lg:justify-start"
          >
            <Tab fullWidth={false}>
              <Tab.Button className="py-4 cursor-pointer">Season</Tab.Button>
            </Tab>
            <Tab fullWidth={false}>
              <Tab.Button className="py-4 cursor-pointer">
                Weekly
              </Tab.Button>
            </Tab>
            
          </Tab.List>
        </div>
        {/* END: Profile Info */}
        <Tab.Panels className="mt-5 intro-y">
          <Tab.Panel>
            <div className="col-span-12 intro-y box lg:col-span-6 mb-4">
              <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
                <h2 className="mr-auto text-base font-medium">
                  2022 Total PowerScore
                </h2>
              </div>
              <ScoreRow 
                rank={qbTotalScoreRank} 
                score={avgQbTotalScore} 
                label="QB PowerScore"  
                text={"The QB PowerScore is a composite metric that combines a quarterback's adaptability, passing performance, scramble efficiency, decision-making ability, pocket presence, deep pass success rate, and red zone efficiency rating."}
                big={true}
                // rankColor={rankColor}
                // percentageColor={percentageColor}
              />         
            </div>
            <div className="col-span-12 intro-y box lg:col-span-6 mb-6">
              <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
                <h2 className="mr-auto text-base font-medium">
                  2022 PowerScore Category Breakdown
                </h2>
              </div>
        
              <ScoreRow 
                rank={overallData? overallData.aqs_rank: 99} 
                score={overallData? overallData.aqs_score: 99} 
                label="Adaptive Quarterback Score (AQS)"  
                text={"The AQS is a composite metric that evaluates a quarterback's adaptability, timing, and proficiency in various game scenarios."}
                big={false}
              />    
              <ScoreRow 
                rank={overallData? overallData.qpi_rank: 99} 
                score={overallData? overallData.qpi_score: 99} 
                label="Quarterback Passing Index (QPI)"  
                text={"The QPI measures a quarterback's passing performance by considering completion percentage, yards per attempt, touchdown ratio, and interception ratio."}
                big={false}
              />    
              <ScoreRow 
                rank={overallData? overallData.sei_rank: 99} 
                score={overallData? overallData.sei_score: 99} 
                label="Scramble Efficiency Index"  
                text={"The SEI quantifies a quarterback's effectiveness in gaining yards during scramble plays."}
                big={false}
              />    
              <ScoreRow 
                rank={overallData? overallData.crae_rank: 99} 
                score={overallData? overallData.crae_score: 99} 
                label="Completion Rate Above Expected (CRAE)"  
                text={"The CRAE measures the difference between a quarterback's actual completion rate and their expected completion rate on the difficulty of attempted passes."}
                big={false}
              />     
              <ScoreRow 
                rank={overallData? overallData.dmi_rank: 99} 
                score={overallData? overallData.dmi_score: 99} 
                label="Decision-making Index (DMI)"  
                text={"The DMI  evaluates a quarterback's decision-making ability by considering completed passes, interceptions, sacks, and fumbles. "}
                big={false}
              />     
              <ScoreRow 
                rank={overallData? overallData.ppi_rank: 99} 
                score={overallData? overallData.ppi_score: 99} 
                label="Pocket Presence Index (PPI)"  
                text={"The PPI evaluates a quarterback's ability to make plays under pressure by considering sack avoidance, completion percentage under pressure, and yards per attempt under pressure."}
                big={false}
              />     
              <ScoreRow 
                rank={overallData? overallData.adpsr_rank: 99} 
                score={overallData? overallData.adpsr_score: 99} 
                label="Adjusted Deep Pass Success Rate (ADPSR)"  
                text={"The ADPSR evaluates a quarterback's performance on deep pass plays (20 yards or more) by taking into account touchdowns, interceptions, and the number of deep pass attempts."}
                big={false}
              />     
              <ScoreRow 
                rank={overallData? overallData.reer_rank: 99} 
                score={overallData? overallData.reer_score: 99} 
                label="Red Zone Efficiency Rating (RZER)"  
                text={"The RZER quantifies a quarterback's effectiveness in scoring touchdowns inside the red zone."}
                big={false}
              />         
            </div>
          </Tab.Panel>
          <Tab.Panel>
            <div className="col-span-12 intro-y box lg:col-span-6 mb-4">
              <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
                <h2 className="mr-auto text-base font-medium">
                  2022 Total PowerScore
                </h2>
              </div>
              <ScoreRow 
                rank={qbTotalScoreRank} 
                score={avgQbTotalScore} 
                label="QB PowerScore"  
                text={"The QB PowerScore is a composite metric that combines a quarterback's adaptability, passing performance, scramble efficiency, decision-making ability, pocket presence, deep pass success rate, and red zone efficiency rating."}
                big={true}
                // rankColor={rankColor}
                // percentageColor={percentageColor}
              />         
            </div>
            <Tab.Group className="col-span-12 intro-y box lg:col-span-6 mb-6">
           {/* start menu */}
              <div className="flex items-center px-5 py-5 border-b sm:py-2 border-slate-200/60 dark:border-darkmode-400">
                <h2 className="mr-auto text-base font-medium">Weekly PowerScore Breakdown</h2>
                <div className="hidden sm:block">
                  <span className="mr-2 text-gray-500">Week:</span>
                  <Tab.List variant="link-tabs" className="flex items-center">
                    {weeklyLabels.map((week: string, index: number) => (
                      <Tab key={index} fullWidth={false}>
                        <Tab.Button className="px-2 py-1 mx-2 text-base font-medium rounded-full hover:bg-gray-200 focus:bg-gray-200">
                          {week}
                        </Tab.Button>
                      </Tab>
                    ))}
                  </Tab.List>
                </div>
                <div className="ml-auto sm:hidden">
                  <Menu>
                    <Menu.Button className="p-2 text-gray-500 rounded-full hover:bg-gray-200 focus:bg-gray-200">
                      <Lucide icon="MoreHorizontal" className="w-5 h-5" />
                    </Menu.Button>
                    <Menu.Items className="w-40 py-2">
                      <Menu.Item as={HeadlessTab}>
                        <Tab.List variant="link-tabs" className="flex flex-col">
                          {weeklyLabels.map((week: string, index: number) => (
                            <Tab key={index} fullWidth={false}>
                              <Tab.Button className="px-2 py-1 text-base font-medium hover:bg-gray-200 focus:bg-gray-200">
                                Week {week}
                              </Tab.Button>
                            </Tab>
                          ))}
                        </Tab.List>
                      </Menu.Item>
                    </Menu.Items>
                  </Menu>
                </div>
              </div>
              {/* end menu  */}
                <div className="p-5">
                  <Tab.Panels>
                    {playerData && playerData.map((data: QBWeekType, index:number) => (
                      <Tab.Panel key={index}>
                        <ScoreRow 
                          rank={data.aqs_competitive_rank} 
                          score={data.aqs_competitive_score} 
                          label="Red Zone Efficiency Rating (RZER)"  
                          text={"The RZER quantifies a quarterback's effectiveness in scoring touchdowns inside the red zone."}
                          big={false}
                        />         
                        <ScoreRow 
                          rank={data.qpi_competitive_rank} 
                          score={data.qpi_competitive_score} 
                          label="Quarterback Passing Index (QPI)"  
                          text={"The QPI measures a quarterback's passing performance by considering completion percentage, yards per attempt, touchdown ratio, and interception ratio."}
                          big={false}
                        />    
                        <ScoreRow 
                          rank={data.sei_competitive_rank} 
                          score={data.sei_competitive_score} 
                          label="Scramble Efficiency Index"  
                          text={"The SEI quantifies a quarterback's effectiveness in gaining yards during scramble plays."}
                          big={false}
                        />    
                        <ScoreRow 
                          rank={data.crae_competitive_rank} 
                          score={data.crae_competitive_score} 
                          label="Completion Rate Above Expected (CRAE)"  
                          text={"The CRAE measures the difference between a quarterback's actual completion rate and their expected completion rate on the difficulty of attempted passes."}
                          big={false}
                        />     
                        <ScoreRow 
                          rank={data.dmi_competitive_rank} 
                          score={data.dmi_competitive_score} 
                          label="Decision-making Index (DMI)"  
                          text={"The DMI  evaluates a quarterback's decision-making ability by considering completed passes, interceptions, sacks, and fumbles. "}
                          big={false}
                        />     
                        <ScoreRow 
                          rank={data.ppi_competitive_rank} 
                          score={data.ppi_competitive_score} 
                          label="Pocket Presence Index (PPI)"  
                          text={"The PPI evaluates a quarterback's ability to make plays under pressure by considering sack avoidance, completion percentage under pressure, and yards per attempt under pressure."}
                          big={false}
                        />     
                        <ScoreRow 
                          rank={data.adpsr_competitive_rank} 
                          score={data.adpsr_competitive_score} 
                          label="Adjusted Deep Pass Success Rate (ADPSR)"  
                          text={"The ADPSR evaluates a quarterback's performance on deep pass plays (20 yards or more) by taking into account touchdowns, interceptions, and the number of deep pass attempts."}
                          big={false}
                        />     
                        <ScoreRow 
                          rank={data.reer_competitive_rank} 
                          score={data.reer_competitive_score} 
                          label="Red Zone Efficiency Rating (RZER)"  
                          text={"The RZER quantifies a quarterback's effectiveness in scoring touchdowns inside the red zone."}
                          big={false}
                        />         
                      </Tab.Panel>
                    ))}
                  </Tab.Panels>

                  </div>
                  </Tab.Group>
                  <WeekRanks 
                    data={playerData} 
                  />
                
             
          
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    </>
  );
}

export default Main;


