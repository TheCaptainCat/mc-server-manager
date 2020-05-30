<template>
  <div v-if="userAllowed" class="mc-game-mgr">
    <game-status class="mc-game-status" />
    <game-log id="mc-game-log" class="mc-game-log my-4" :log="log" />
    <game-command class="mc-game-cmd" />
  </div>
  <div v-else>
    Please login
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import GameStatus from "@/components/manager/GameStatus.vue";
import GameLog from "@/components/manager/GameLog.vue";
import GameCommand from "@/components/manager/GameCommand.vue";
import { gameModule, userModule } from "@/store";

@Component({
  components: { GameStatus, GameLog, GameCommand }
})
export default class GameManager extends Vue {
  public get log() {
    return gameModule.log.map((line, index) => ({ text: line, index: index }));
  }

  public get userAllowed() {
    return userModule.currentUser !== null;
  }

  @Watch("log")
  public onLogChange() {
    const div = document.getElementById("mc-game-log");
    if (div) {
      setTimeout(() => {
        div.scrollTop = div.scrollHeight;
      }, 50);
    }
  }
}
</script>

<style lang="scss" scoped>
.mc-game-mgr {
  height: calc(100vh - 124px);
  display: flex;
  flex-flow: column;

  .mc-game-status {
    flex: 0 1 auto;
  }

  .mc-game-log {
    flex: 1 1 auto;
    overflow-y: auto;
  }

  .mc-game-cmd {
    flex: 0 1 auto;
  }
}
</style>
