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

import { getQBOverallData} from '../../queries/restQueries';

function Main() {
    const [overallData, setOverallData] = useState<any>(null);
  
    useEffect(() => {
      // fetching qb overall data
      const fetchOverallPlayerData = async () => {
        const baseUrl = "http://localhost:8000";
        const data = await getQBOverallData(baseUrl, "50", "avg_qb_total_score");
        console.log("qb overall ranks:", data);
        setOverallData(data);
      };
  
      fetchOverallPlayerData();
    }, []);


    
    
    // Add a conditional statement to check if overallData has been fetched
    if (!overallData) {
      return <Progress />;
    }
  
    return (
      <>
        <div className="flex items-center mt-8 intro-y">
          <h2 className="mr-auto text-lg font-medium">QBs</h2>
        </div>
        <div className="col-span-12 intro-y box lg:col-span-6 mb-6 mt-6">
          <div className="flex items-center p-5 border-b border-slate-200/60 dark:border-darkmode-400">
            <h2 className="mr-auto text-base font-medium">
            QB PowerScore by Conference
            </h2>
          </div>
          <OverallMainTable overallData={overallData} />
        </div>
        
      </>
    );
  }
  
  export default Main;
  

 