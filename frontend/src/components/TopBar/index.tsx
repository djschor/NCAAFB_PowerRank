import { useState, Fragment } from "react";
import { Link } from "react-router-dom";
import Lucide from "../../base-components/Lucide";
import logoUrl from "../../assets/images/powerscore_logo.png";
import Breadcrumb from "../../base-components/Breadcrumb";
import { FormInput } from "../../base-components/Form";
import { Menu, Popover } from "../../base-components/Headless";
import fakerData from "../../utils/faker";
import _ from "lodash";
import clsx from "clsx";
import { Transition } from "@headlessui/react";

function Main(props: { layout?: "side-menu" | "simple-menu" | "top-menu" }) {
  const [searchDropdown, setSearchDropdown] = useState(false);
  const showSearchDropdown = () => {
    setSearchDropdown(true);
  };
  const hideSearchDropdown = () => {
    setSearchDropdown(false);
  };
  const titleStyle = {
    fontFamily: 'Roboto, sans-serif', // Change the font family to Roboto or any other modern font
    fontWeight: '700', // Adjust the font-weight to a higher value for better visibility over the semi-transparent background
    fontSize: '1.6rem',
    lineHeight: '1.2',
    letterSpacing: '-0.1em', // Slightly reduce the letter spacing
    textTransform: 'uppercase',
    color: '#ffffff', // Change the color to white for better contrast over the blue menu
    textShadow: '2px 2px 4px rgba(0, 0, 0, 0.25)', // Add a subtle shadow to make the text more readable
    marginTop: '3rem',
    marginLeft: '-5.3rem',
    marginBottom: '3rem',
    // backgroundColor: 'rgba(0, 123, 255, 0.5)', // Add a semi-transparent blue background
    borderRadius: '0.5rem', // Add border-radius to make the background shape more appealing
  };
    return (
    <>
      <div
        className={clsx([
          "h-[70px] md:h-[65px] z-[51] border-b border-white/[0.08] mt-12 md:mt-0 -mx-5 sm:-mx-8 md:-mx-0 px-3 md:border-b-0 relative md:fixed md:inset-x-0 md:top-0 sm:px-8 md:px-10 md:pt-10 md:bg-gradient-to-b md:from-slate-100 md:to-transparent dark:md:from-darkmode-700",
          props.layout == "top-menu" && "dark:md:from-darkmode-800",
          "before:content-[''] before:absolute before:h-[65px] before:inset-0 before:top-0 before:mx-7 before:bg-amber-400/30 before:mt-3 before:rounded-xl before:hidden before:md:block before:dark:bg-darkmode-600/30",
          "after:content-[''] after:absolute after:inset-0 after:h-[65px] after:mx-5 after:bg-blue-900/30 after:mt-5 after:rounded-xl after:shadow-md after:hidden after:md:block after:dark:bg-darkmode-600",
        ])}
      >
        
        <div className="flex items-center h-full">
          {/* BEGIN: Logo */}
          <Link
            to="/"
            className={clsx([
              "-intro-x hidden md:flex",
              props.layout == "side-menu" && "xl:w-[180px]",
              props.layout == "simple-menu" && "xl:w-auto",
              props.layout == "top-menu" && "w-auto",
            ])}
          >
            <img
              alt="NCAAFB PowerScore"
              // className="w-12"
              style={{ height: "auto", width: "150px" }}
              src={logoUrl}
            />
            <span
              className={clsx([
                "ml-3 text-lg text-white",
                props.layout == "side-menu" && "hidden xl:block",
                props.layout == "simple-menu" && "hidden",
              ])}
            >
              {" "}
              NCAAFB ;n{" "}
            </span>
          </Link>
          {/* END: Logo */}
          {/* BEGIN: Breadcrumb */}
          <Breadcrumb
            light
            className={clsx([
              "h-[45px] md:ml-10 md:border-l border-white/[0.08] dark:border-white/[0.08] mr-auto -intro-x",
              props.layout != "top-menu" && "md:pl-6",
              props.layout == "top-menu" && "md:pl-10",
            ])}
          >
            <Breadcrumb.Link style={titleStyle} to="/">
              <h1 style={titleStyle}>NCAAFB PowerScore</h1>
            </Breadcrumb.Link>
            {/* <Breadcrumb.Link to="/" active={true}>
            </Breadcrumb.Link> */}
          </Breadcrumb>
          {/* END: Breadcrumb */}
          
        </div>
      </div>
    </>
  );
}

export default Main;
