import { Module, Mutation, VuexModule } from "vuex-module-decorators";

@Module({ name: "game" })
export default class GameStore extends VuexModule {
  private _status: string = "STANDING_BY";
  private _version: string | null = null;
  private _latest: string | null = null;
  private _log: string[] = [];
  private _done: number = 0;
  private _total: number = 0;

  public get version(): string | null {
    return this._version;
  }

  public get latest(): string | null {
    return this._latest;
  }

  public get log(): string[] {
    return this._log;
  }

  public get status(): string {
    return this._status;
  }

  public get progress(): { done: number; total: number } {
    return {
      done: this._done,
      total: this._total
    };
  }

  @Mutation
  public setCurrentVersion(value: string | null) {
    this._version = value;
  }

  @Mutation
  public setLatestVersion(value: string | null) {
    this._latest = value;
  }

  @Mutation
  public setStatus(value: string) {
    this._status = value;
  }

  @Mutation
  public addLogEntry(line: string) {
    this._log = this._log.concat(line);
  }

  @Mutation
  public setProgress(progress: { done: number; total: number }) {
    this._done = progress.done;
    this._total = progress.total;
  }
}
