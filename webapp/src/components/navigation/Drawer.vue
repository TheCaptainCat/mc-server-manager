<template>
  <v-navigation-drawer v-model="open" absolute temporary>
    <v-list dense>
      <v-list-item @click="toggleLeftDrawer()">
        <v-list-item-action>
          <v-icon>mdi-menu</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Minecraft Server Manager</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item v-if="isAdmin" link :to="{ name: 'AdminPanel' }">
        <v-list-item-action>
          <v-icon>mdi-cogs</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Admin Panel</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{ name: 'About' }">
        <v-list-item-action>
          <v-icon>mdi-help-box</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>About</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { uiStateModule } from "@/store";
import UserMixin from "@/mixins/UserMixin";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Drawer extends Vue {
  public get open(): boolean {
    return uiStateModule.leftDrawer;
  }

  public get isAdmin(): boolean {
    return UserMixin.hasRole("admin");
  }

  public set open(value: boolean) {
    uiStateModule.setLeftDrawer(value);
  }

  public toggleLeftDrawer() {
    uiStateModule.setLeftDrawer(!uiStateModule.leftDrawer);
  }
}
</script>

<style lang="scss" scoped />
