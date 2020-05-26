import User from "@/models/User";
import router from "@/router";
import { toastModule, userModule, socketModule } from "@/store";
import ApiRequest from "@/utils/ApiRequest";
import ApiResponse from "@/utils/ApiResponse";
import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

@Module({ name: "user" })
export default class UserStore extends VuexModule {
  private _currentUser: User | null = null;
  private _loadingUserInfo: boolean = true;

  public get currentUser(): User | null {
    return this._currentUser;
  }

  public get loadingUserInfo(): boolean {
    return this._loadingUserInfo;
  }

  public get loggedIn(): boolean {
    return this._currentUser != null;
  }

  @Mutation
  public _setUser(user: User | null) {
    this._currentUser = user;
  }

  @Mutation
  public loadingUserState(loading: boolean) {
    this._loadingUserInfo = loading;
  }

  @Action
  public async setUser(user: User | null) {
    userModule._setUser(user);
    await socketModule.resetConnection();
    if (user) {
      await socketModule.subscribe({
        topic: "user",
        channel: user.username,
        callback: async () => {}
      });
    }
  }

  @Action
  public async info() {
    userModule.loadingUserState(true);
    await new ApiRequest("/user/info", "GET", null, false).fetch<User>({
      success: async (res: ApiResponse<User>) => {
        await userModule.setUser(res.data);
      },
      error: async () => {
        await userModule.setUser(null);
      },
      finally: async () => {
        userModule.loadingUserState(false);
      }
    });
  }

  @Action
  public async logout() {
    await new ApiRequest("/user/logout", "POST").fetch({
      success: async () => {
        await userModule.setUser(null);
        router.push({ name: "Home" }).catch(() => "");
        toastModule.addToast({ type: "success", message: "Bye!" });
      }
    });
  }
}
