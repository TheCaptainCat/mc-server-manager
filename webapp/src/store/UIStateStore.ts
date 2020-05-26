import { getCookie, setCookie } from "@/plugins/cookies";
import vuetify from "@/plugins/vuetify";
import { uiStateModule } from "@/store";
import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

@Module({ name: "ui" })
export default class UIStateStore extends VuexModule {
  private _darkTheme: boolean = false;
  private _leftDrawer: boolean = false;

  public get darkTheme(): boolean {
    return this._darkTheme;
  }

  public get leftDrawer(): boolean {
    return this._leftDrawer;
  }

  @Mutation
  public setDarkTheme(value: boolean) {
    this._darkTheme = value;
    vuetify.framework.theme.dark = value;
    setCookie("blnt-theme", value ? "dark" : "light");
  }

  @Action
  public initTheme() {
    const theme = getCookie("blnt-theme");
    if (theme) {
      uiStateModule.setDarkTheme(theme === "dark");
    } else {
      setCookie("blnt-theme", "light");
    }
  }

  @Mutation
  public setLeftDrawer(value: boolean) {
    this._leftDrawer = value;
  }
}
