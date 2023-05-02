import { selectDarkMode, setDarkMode } from "../../stores/darkModeSlice";
import { useAppSelector, useAppDispatch } from "../../stores/hooks";

function Main() {
  const dispatch = useAppDispatch();
  const darkMode = useAppSelector(selectDarkMode);

  const setDarkModeClass = () => {
    const el = document.querySelectorAll("html")[0];
    darkMode ? el.classList.add("dark") : el.classList.remove("dark");
  };

  setDarkModeClass();

  return null;
}

export default Main;