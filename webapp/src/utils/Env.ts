export default class Env {
  public static get API_URL() {
    return process.env.VUE_APP_API_URL;
  }

  public static get WS_URL() {
    return process.env.VUE_APP_WS_URL;
  }
}
