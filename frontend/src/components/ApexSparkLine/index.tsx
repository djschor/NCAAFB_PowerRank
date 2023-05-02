import React from "react";
import ApexCharts from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import { getColor } from "../../utils/colors";
import { selectColorScheme } from "../../stores/colorSchemeSlice";
import { useAppSelector } from "../../stores/hooks";

interface MainProps extends React.ComponentPropsWithoutRef<"div"> {
  width: string;
  height: string;
  lineColor: string;
  labels: string[];
  data: number[];
  className: string;
}

function Main(props: MainProps) {
  const colorScheme = useAppSelector(selectColorScheme);

  const chartOptions: ApexOptions = {
    chart: {
      id: "sparkline",
      type: "line",
      width: props.width,
      height: props.height,
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
    },
    markers: {
      size: 0,
    },
    stroke: {
      curve: "smooth",
      width: 2,
      colors:
        colorScheme && props.lineColor.length
          ? [props.lineColor]
          : [getColor("primary", 0.8)],
    },
    xaxis: {
      categories: props.labels,
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    tooltip: {
      enabled: true,
      x: {
        show: true,
        formatter: (val: any) => `Week ${val}`,
      },
    },
    legend: {
      show: false,
    },
    grid: {
      show: false,
    },
    dataLabels: {
      enabled: false,
    },
  };
  
  const chartSeries = [
    {
      name: "Weekly PowerScore Ranking (FBS)",
      data: props.data,
    },
  ];

  return (
    <div className={props.className}>
      <ApexCharts
        options={chartOptions}
        series={chartSeries}
        type="line"
        width={props.width}
        height={props.height}
      />
    </div>
  );
}

Main.defaultProps = {
  width: "100%",
  height: "50%",
  lineColor: "",
  className: "",
};

export default Main;
