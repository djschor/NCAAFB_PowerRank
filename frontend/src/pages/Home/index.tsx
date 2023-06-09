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
import SimpleLineChart1 from "../../components/SimpleLineChart1";
import SimpleLineChart2 from "../../components/SimpleLineChart2";
import ProgressBar from "../../components/ProgressBar";
import ProgressGauge from "../../components/VictoryProgress";
import ApexSparkline from "../../components/ApexSparkLine";
import ScoreRow from "../../components/ScoreRow";
import OverallMainTable from "../../components/OverallMainTable";
import WeeklyRankingsTable from "../../components/WeeklyRankingsTable";
import logoUrl from "../../assets/images/powerscore_logo.png";
import './home.css';


import { Menu, Tab } from "../../base-components/Headless";
import { Tab as HeadlessTab } from "@headlessui/react";
import { useParams } from 'react-router-dom'
import { playerNames, formattedPlayerNames } from '../../data/playerNames';
import { QBUrls, teamLogoUrls } from '../../data/imageUrls';
import { getQBWeekData, getQBOverallData, getQBOverallDataPlayer, getPlayerMeta } from '../../queries/restQueries';

function Main() {
    const [overallData, setOverallData] = useState<any>(null);
  
    useEffect(() => {
      // fetching qb overall data
      const fetchOverallPlayerData = async () => {
        
        
        const baseUrl = "https://shrouded-shore-60391.herokuapp.com";
        const data = await getQBOverallData(baseUrl, "50", "avg_qb_total_score");
        console.log("qb overall ranks:", data);
        setOverallData(data);
      };
  
      fetchOverallPlayerData();
    }, []);

    const [weekRankingsData, setWeekRankingsData] = useState<any>(null);
    useEffect(() => {
        // fetching qb overall data
        const fetchWeekRankings = async () => {
          const baseUrl = "https://shrouded-shore-60391.herokuapp.com";
          const data = await getQBWeekData(baseUrl, "50");
          console.log("qb week ranks:", data);
          setWeekRankingsData(data);
        };
    
        fetchWeekRankings();
      }, []);
    
  

    
    
    // Add a conditional statement to check if overallData has been fetched
    if (!overallData) {
      return <Progress />;
    }
  
    return (
      <>
      <div className="flex items-center mt-8 intro-y">
        <h2 className="mr-auto text-lg font-medium">PowerScore Home</h2>
      </div>
      <div className="col-span-12 intro-y box lg:col-span-6 mt-6">
        <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
          <h2 className="mr-auto text-base font-medium">
            About NCAAFB PowerScore
          </h2>
        </div>
      {/* <div className="about-container"> */}
        <div className="col-span-12 intro-y box lg:col-span-6 mb-6">
          <div className="logo-title -pl-1/4">
            <img src={logoUrl} alt="NCAAFB PowerScore Logo" className="logo -mt-3" />
          </div>
          <p className="about-text ml-10 pl-10 -mt-10 pb-5">
            <span className="brand-name">NCAAFB PowerScore</span> is a project created to better assess Quarterback performance by using a comprehensive range of new metrics. More information about the metrics can be accessed at the <a href="/about" className="highlight-link">about page</a> or at the project <a href="https://github.com/djschor/NCAAFB_PowerRank" className="highlight-link">github</a>.
          </p>
    {/* </div> */}
        </div>

      </div>
        {/* <div className="flex items-center mt-8 intro-y">
          <h2 className="mr-auto text-lg font-medium">PowerScore Home</h2>
        </div> */}
        <div className="col-span-12 intro-y box lg:col-span-6 mb-6 mt-6">
          <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
            <h2 className="mr-auto text-base font-medium">
              Top 2022 QB's by Total Season PowerScore
            </h2>
          </div>
          <OverallMainTable overallData={overallData} />
        </div>
        <div className="col-span-12 intro-y box lg:col-span-6 mb-6 mt-6">
          <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
            <h2 className="mr-auto text-base font-medium">
              Top 2022 QB Game Performances by PowerScore
            </h2>
          </div>
          {weekRankingsData && <WeeklyRankingsTable data={weekRankingsData} />}
        </div>

        
      </>
    );
  }
  
  export default Main;
  

 