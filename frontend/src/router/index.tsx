import { useRoutes } from "react-router-dom";
import SideMenu from "../layouts/SideMenu";
import SimpleMenu from "../layouts/SimpleMenu";
import TopMenu from "../layouts/TopMenu";
import Page1 from "../pages/Page1";
import Page2 from "../pages/Page2";
import QBProfile from "../pages/QBProfile";
import Home from "../pages/Home";
import QBHome from "../pages/QBHome";
import About from "../pages/About";

function Router() {
  const routes = [
    {
      path: "/",
      element: <TopMenu />,
      children: [
        {
          path: "/",
          element: <Home />,
        },
        {
          path: "qb/",
          element: <QBHome />,
        },
        {
          path: "qb/:qb_name",
          element: <QBProfile />,
        },
        {
          path: "about/",
          element: <About />,
        },
      ],
    },
    {
      path: "/simple-menu",
      element: <SimpleMenu />,
      children: [
        {
          path: "page-1",
          element: <Home />,
        },
        {
          path: "qb/",
          element: <QBHome />,
        },
        {
          path: "qb/:qb_name",
          element: <QBProfile />,
        },
      ],
    },
    {
      path: "/top-menu",
      element: <TopMenu />,
      children: [
        {
          path: "page-1",
          element: <Home />,
        },
        {
          path: "qb/",
          element: <QBHome />,
        },
        {
          path: "qb/:qb_name",
          element: <QBProfile />,
        },
        {
          path: "about/",
          element: <About />,
        },
      ],
    },
  ];

  return useRoutes(routes);
}

export default Router;
