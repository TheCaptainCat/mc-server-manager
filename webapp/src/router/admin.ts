import { RouteConfig } from "vue-router";
import router from "@/router/default";
import { AdminRoot, AdminPanel, UserTable } from "@/views/admin";

const AdminRoutes: RouteConfig[] = [
  {
    path: "/admin",
    component: AdminRoot,
    redirect: { name: "AdminRoot" },
    children: [
      {
        path: "",
        name: "AdminPanel",
        component: AdminPanel
      },
      {
        path: "users",
        name: "UserTable",
        component: UserTable
      }
    ]
  }
];

router.addRoutes(AdminRoutes);

export default AdminRoutes;
