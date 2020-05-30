import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

import { BackButton, ExternalLink, Modal, SlimCard } from "@/components/global";

Vue.config.productionTip = false;

Vue.component("back-btn", BackButton);
Vue.component("external-link", ExternalLink);
Vue.component("modal", Modal);
Vue.component("slim-card", SlimCard);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
