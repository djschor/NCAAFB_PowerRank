import ScrollToTop from "./base-components/ScrollToTop";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "./stores/store";
import Router from "./router";
import "./assets/css/app.css";
import {
  ApolloProvider,
  ApolloClient,
  createHttpLink,
  InMemoryCache
} from '@apollo/client';

const httpLink = createHttpLink({
  uri: 'http://127.0.0.1:8000/graphql',
});

// const client = new ApolloClient({
//   ssrMode: true,
//   link: httpLink,
//   cache: new InMemoryCache()
// });

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  // <ApolloProvider client={client}>
    <BrowserRouter>
      <Provider store={store}>
        <Router />
      </Provider>
      <ScrollToTop />
    </BrowserRouter>
  // </ApolloProvider>
);
