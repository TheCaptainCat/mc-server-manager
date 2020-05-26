<template>
  <game-status />
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import GameStatus from "@/components/manager/GameStatus.vue";

@Component({
  components: { GameStatus }
})
export default class GameManager extends Vue {}
</script>

<style scoped></style>
