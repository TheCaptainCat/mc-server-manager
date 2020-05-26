import { Component, Vue } from "vue-property-decorator";
import { userModule } from "@/store";

@Component
export default class UserMixin extends Vue {
  public isLoggedIn() {
    if (!userModule.loggedIn) {
      this.$router.push({ name: "Home" });
    }
  }

  public hasRole(role: string) {
    this.isLoggedIn();
    if (!UserMixin.hasRole(role)) {
      this.$router.push({ name: "Home" });
    }
  }

  public static hasRole(role: string): boolean {
    const user = userModule.currentUser;
    if (user == null) return false;
    const roles = user.roles.map(r => r.name);
    return roles.includes("root") || roles.includes(role);
  }
}
