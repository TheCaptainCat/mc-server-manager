<template>
  <router-view />
</template>

<script lang="ts">
import { Component, Mixins, Vue } from "vue-property-decorator";
import UserMixin from "@/mixins/UserMixin";

@Component
export default class AdminRoot extends Mixins(UserMixin) {
  public created() {
    this.hasRole("admin");
  }
}
</script>
