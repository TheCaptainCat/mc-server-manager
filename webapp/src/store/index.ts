import Vue from "vue";
import Vuex from "vuex";
import { getModule } from "vuex-module-decorators";
import SocketStore from "./SocketStore";
import LoginStore from "./LoginStore";
import ToastStore from "./ToastStore";
import UIStateStore from "./UIStateStore";
import UserStore from "./UserStore";
import GameStore from "./GameStore";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    socket: SocketStore,
    login: LoginStore,
    ui: UIStateStore,
    user: UserStore,
    toast: ToastStore,
    game: GameStore
  }
});

export default store;
export const socketModule = getModule(SocketStore, store);
export const userModule = getModule(UserStore, store);
export const uiStateModule = getModule(UIStateStore, store);
export const toastModule = getModule(ToastStore, store);
export const loginModule = getModule(LoginStore, store);
export const gameModule = getModule(GameStore, store);
