<template>
  <v-app-bar app clipped-left>
    <v-app-bar-nav-icon @click="toggleLeftDrawer()" />

    <v-toolbar-title>
      <router-link :to="{ name: 'Home' }">
        <span class="blnt-menu-title">Minecraft Server Manager</span>
      </router-link>
    </v-toolbar-title>

    <div class="flex-grow-1"></div>

    <v-skeleton-loader class="mr-5" type="chip" v-if="loading" />
    <v-skeleton-loader type="chip" v-if="loading" />

    <user-menu v-if="!loading" />

    <v-btn @click="openLogin()" text v-if="!loading && !logged">
      Login
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { uiStateModule, userModule, loginModule } from "@/store";
import { UserMenu } from "@/components/navigation";

@Component({
  components: { UserMenu }
})
export default class NavBar extends Vue {
  public get logged(): boolean {
    return userModule.loggedIn;
  }

  public get loading(): boolean {
    return userModule.loadingUserInfo;
  }

  public openLogin() {
    loginModule.openLogin();
  }

  public toggleLeftDrawer() {
    uiStateModule.setLeftDrawer(!uiStateModule.leftDrawer);
  }
}
</script>

<style lang="scss" scoped>
.blnt-menu-title {
  cursor: pointer;
  color: inherit;
}
</style>
