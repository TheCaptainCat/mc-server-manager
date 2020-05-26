import { Module, Mutation, VuexModule } from "vuex-module-decorators";

@Module({ name: "game" })
export default class GameStore extends VuexModule {
  private _running: boolean = false;
  private _version: string | null = null;
  private _latest: string | null = null;

  public get running(): boolean {
    return this._running;
  }

  public get version(): string | null {
    return this._version;
  }

  public get latest(): string | null {
    return this._latest;
  }

  @Mutation
  public setRunningState(value: boolean) {
    this._running = value;
  }

  @Mutation
  public setCurrentVersion(value: string | null) {
    this._version = value;
  }

  @Mutation
  public setLatestVersion(value: string | null) {
    this._latest = value;
  }
}
