import { getCookie } from "@/plugins/cookies";
import { loginModule, toastModule } from "@/store";
import ApiResponse from "@/utils/ApiResponse";
import Env from "@/utils/Env";
import _ from "lodash";

export default class ApiRequest<T> {
  public readonly method: string;
  public readonly path: string;
  public readonly body: T | null;
  public readonly toastErrors: boolean;

  public constructor(
    path: string,
    method: string,
    body?: T,
    toastErrors?: boolean
  ) {
    this.path = path;
    this.method = method;
    this.body = body || null;
    this.toastErrors = toastErrors === undefined ? true : toastErrors;
  }

  public async fetch<R>(params: Partial<FetchParams<R>>) {
    let body = null;
    const headers = new Headers({
      Accept: "application/json"
    });
    const token = getCookie("csrf_access_token");
    if (token) {
      headers.set("X-CSRF-TOKEN", token);
    }
    if (this.body !== null) {
      if (this.body instanceof File) {
        body = new FormData();
        body.append("file", this.body);
      } else {
        body = JSON.stringify(this.body);
        headers.set("Content-Type", "application/json");
      }
    }
    await this.doFetch<R>(body, headers, params);
  }

  private async refreshToken<R>(
    params: Partial<FetchParams<R>>,
    errors: string[]
  ): Promise<boolean> {
    const token = getCookie("csrf_refresh_token");
    if (_.isNil(token)) {
      params.error && (await params.error(errors));
      return false;
    }
    const headers = new Headers({
      Accept: "application/json",
      "X-CSRF-TOKEN": token
    });
    const refreshRequest = new ApiRequest("/user/token/refresh", "POST");
    await refreshRequest.doFetch(null, headers, {
      refresh: false,
      success: async () => {
        await this.fetch(params);
      }
    });
    return true;
  }

  private async doFetch<R>(
    body: string | FormData | null,
    headers: Headers,
    params: Partial<FetchParams<R>>
  ) {
    const init: object = {
      body,
      credentials: "include",
      headers,
      method: this.method,
      mode: "cors"
    };
    let doFinally = true;
    try {
      const fetchResponse = await fetch(
        new Request(Env.API_URL + this.path, init),
        init
      );
      const response = (await fetchResponse.json()) as ApiResponse<R>;
      if (Math.floor(response.code / 100) !== 2) {
        if (
          response.messages.includes("user.token.expired") &&
          (params.refresh === undefined || params.refresh)
        ) {
          doFinally = !(await this.refreshToken(params, response.messages));
        } else if (
          response.messages.includes("user.token.fresh_required") &&
          (params.openLogin === undefined || params.openLogin)
        ) {
          doFinally = false;
          loginModule.setCallback(async () => {
            await this.fetch(params);
          });
          loginModule.setCancelCallback(async () => {
            if (params.error) {
              await params.error([]);
            }
          });
          loginModule.openRefreshLogin();
        } else {
          if (this.toastErrors) {
            this.doToastErrors(response.messages);
          }
          if (params.error) {
            await params.error(response.messages);
          }
        }
      } else if (params.success) {
        await params.success(response);
      }
    } catch (e) {
      if (this.toastErrors) {
        this.doToastErrors([e]);
      }
      if (params.error) {
        await params.error([e]);
      }
    }
    if (params.finally && doFinally) {
      await params.finally();
    }
  }

  private doToastErrors(errors: Array<string | Error>) {
    for (const error of errors) {
      if (error instanceof Error) console.error(error);
      if (typeof error === "string")
        toastModule.addToast({ message: error, type: "error" });
    }
  }
}

export interface FetchParams<T> {
  error: (errors: string[]) => Promise<void>;
  finally: () => Promise<void>;
  openLogin: boolean;
  refresh: boolean;
  success: (res: ApiResponse<T>) => Promise<void>;
}
