import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

import { BackButton, ExternalLink, Modal } from "@/components/global";

Vue.config.productionTip = false;

Vue.component("back-btn", BackButton);
Vue.component("external-link", ExternalLink);
Vue.component("modal", Modal);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
