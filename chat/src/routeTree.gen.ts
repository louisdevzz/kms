/* eslint-disable */
// @ts-nocheck
// noinspection JSUnusedGlobalSymbols

import { Route as rootRoute } from "./routes/__root";
import { Route as IndexImport } from "./routes/index";
import { Route as ChatIdImport } from "./routes/chat/$chatId";

const IndexRoute = IndexImport.update({
  id: "/",
  path: "/",
  getParentRoute: () => rootRoute,
} as any);

const ChatIdRoute = ChatIdImport.update({
  id: "/chat/$chatId",
  path: "/chat/$chatId",
  getParentRoute: () => rootRoute,
} as any);

declare module "@tanstack/react-router" {
  interface FileRoutesByPath {
    "/": {
      id: "/";
      path: "/";
      fullPath: "/";
      preLoaderRoute: typeof IndexImport;
      parentRoute: typeof rootRoute;
    };
    "/chat/$chatId": {
      id: "/chat/$chatId";
      path: "/chat/$chatId";
      fullPath: "/chat/$chatId";
      preLoaderRoute: typeof ChatIdImport;
    };
  }
}

export interface FileRoutesByFullPath {
  "/": typeof IndexRoute;
  "/chat/$chatId": typeof ChatIdRoute;
}

export interface FileRoutesByTo {
  "/": typeof IndexRoute;
  "/chat/$chatId": typeof ChatIdRoute;
}

export interface FileRoutesById {
  __root__: typeof rootRoute;
  "/": typeof IndexRoute;
  "/chat/$chatId": typeof ChatIdRoute;
}

export interface FileRouteTypes {   
  fileRoutesByFullPath: FileRoutesByFullPath;
  fullPaths: "/" | "/chat/$chatId";
  fileRoutesByTo: FileRoutesByTo;
  to: "/" | "/chat/$chatId";
  id: "__root__" | "/" | "/chat/$chatId";
  fileRoutesById: FileRoutesById;
}

export interface RootRouteChildren {
  IndexRoute: typeof IndexRoute;
  ChatIdRoute: typeof ChatIdRoute;
}

const rootRouteChildren: RootRouteChildren = {
  IndexRoute: IndexRoute,
  ChatIdRoute: ChatIdRoute,
};

export const routeTree = rootRoute
  ._addFileChildren(rootRouteChildren)
  ._addFileTypes<FileRouteTypes>(); 