import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "./store";
import { icons } from "../base-components/Lucide";

export interface Menu {
  icon: keyof typeof icons;
  title: string;
  pathname?: string;
  subMenu?: Menu[];
  ignore?: boolean;
}

export interface TopMenuState {
  menu: Array<Menu>;
}

const initialState: TopMenuState = {
  menu: [
    {
      icon: "Home",
      pathname: "/",
      title: "PowerScore Home",
    },
    {
      icon: "Target",
      pathname: "/qb",
      title: "QBs",
    },
    {
      icon: "Info",
      pathname: "/about",
      title: "About",
    },
    // {
    //   icon: "MessageCircle",
    //   pathname: "/about",
    //   title: "Contact",
    // },
  ],
};

export const topMenuSlice = createSlice({
  name: "topMenu",
  initialState,
  reducers: {},
});

export const selectTopMenu = (state: RootState) => state.topMenu.menu;

export default topMenuSlice.reducer;
