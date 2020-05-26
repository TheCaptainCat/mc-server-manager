<template>
  <with-navigation :routes="navigationRoutes">
    <router-view />
  </with-navigation>
</template>

<script lang="ts">
import { Component, Mixins } from "vue-property-decorator";
import UserMixin from "@/mixins/UserMixin";
import WithNavigation from "@/components/containers/WithNavigation.vue";

@Component({
  components: { WithNavigation }
})
export default class AccountRoot extends Mixins(UserMixin) {
  public get navigationRoutes() {
    return [
      { name: "AccountDetails", label: "Info" },
      { name: "AccountManagement", label: "Modify" }
    ];
  }
}
</script>
