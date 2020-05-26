import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import { loginModule } from "@/store";

@Module({ name: "login" })
export default class UIStateStore extends VuexModule {
  private _openState: boolean = false;
  private _refresh: boolean = false;
  private _callback: (() => Promise<void>) | null = null;
  private _cancelCallback: (() => Promise<void>) | null = null;

  public get openState(): boolean {
    return this._openState;
  }

  public get refresh(): boolean {
    return this._refresh;
  }

  public get callback(): (() => Promise<void>) | null {
    return this._callback;
  }

  public get cancelCallback(): (() => Promise<void>) | null {
    return this._cancelCallback;
  }

  @Mutation
  public setOpenState(value: boolean) {
    this._openState = value;
  }

  @Mutation
  public setRefresh(value: boolean) {
    this._refresh = value;
  }

  @Mutation
  public setCallback(callback: (() => Promise<void>) | null) {
    this._callback = callback;
  }

  @Mutation
  public setCancelCallback(callback: (() => Promise<void>) | null) {
    this._cancelCallback = callback;
  }

  @Action
  public openLogin() {
    loginModule.setRefresh(false);
    loginModule.setOpenState(true);
  }

  @Action
  public openRefreshLogin() {
    loginModule.setRefresh(true);
    loginModule.setOpenState(true);
  }
}
