<template>
  <v-container fluid>
    <game-manager />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import GameManager from "@/components/manager/GameManager.vue";

@Component({
  components: { GameManager }
})
export default class Home extends Vue {}
</script>

<style lang="scss" scoped></style>
