import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/LoginComponent.vue";
import HomeView from "../views/HomeView.vue";
import PageNotFound from "@/layout/PageNotFound.vue";
import ServerError from "@/layout/ServerError.vue";

const routes = [
  { path: "/", name: "HomeView", component: HomeView, meta: { auth: true, layout: 'main' } },
  { path: "/login", name: "Login", component: Login, meta: { auth: false, layout: 'empty' } },
  { path: "/station", name: "Station", component: () => import("../views/StationView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/station/:number(\\d+)", name: "StationSingle", component: () => import("../views/StationSingleView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/melio", name: "Melio", component: () => import("../views/MelioView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/meteo", name: "Meteo", component: () => import("../views/MeteoView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/500", component: ServerError },
  { path: "/:pathMatch(.*)*", component: PageNotFound }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
