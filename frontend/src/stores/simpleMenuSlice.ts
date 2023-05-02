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

export interface SimpleMenuState {
  menu: Array<Menu | "divider">;
}

const initialState: SimpleMenuState = {
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
  ],
};

export const simpleMenuSlice = createSlice({
  name: "simpleMenu",
  initialState,
  reducers: {},
});

export const selectSimpleMenu = (state: RootState) => state.simpleMenu.menu;

export default simpleMenuSlice.reducer;
