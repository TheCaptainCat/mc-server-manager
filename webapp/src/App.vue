<template>
  <v-app id="bolinette">
    <nav-bar />

    <drawer />

    <login-form ref="login" />

    <v-content>
      <v-overlay v-if="isFetchingUserInfo">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
      <router-view v-else />
    </v-content>

    <toasts />

    <v-footer app>
      <span>Bolinette</span>
      <div class="flex-grow-1"></div>
      <span>&copy; 2020</span>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { uiStateModule, userModule } from "@/store";
import { Drawer, NavBar } from "@/components/navigation";
import { Toasts } from "@/components/toasts";
import LoginForm from "@/components/LoginForm.vue";

@Component({
  components: {
    Drawer,
    NavBar,
    LoginForm,
    Toasts
  }
})
export default class App extends Vue {
  public async created() {
    uiStateModule.initTheme();
    await userModule.info();
  }

  public get isFetchingUserInfo() {
    return userModule.loadingUserInfo;
  }
}
</script>

<style lang="scss">
.v-application a {
  text-decoration: none;
  color: inherit !important;
}
</style>
