import { RouteConfig } from "vue-router";
import router from "@/router/default";
import {
  AccountRoot,
  AccountDetails,
  AccountManagement
} from "@/views/account";

const AccountRoutes: RouteConfig[] = [
  {
    path: "/account",
    component: AccountRoot,
    redirect: { name: "AccountDetails" },
    children: [
      {
        path: "details",
        name: "AccountDetails",
        component: AccountDetails
      },
      {
        path: "manage",
        name: "AccountManagement",
        component: AccountManagement
      }
    ]
  }
];

router.addRoutes(AccountRoutes);

export default AccountRoutes;
