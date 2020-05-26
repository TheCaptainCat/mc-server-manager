<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="updating">
      <v-progress-linear :value="updateProgress" />
    </div>
    <div v-else class="d-flex align-center">
      <div>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn icon color="green" :disabled="!currentVersion" v-on="on">
              <v-icon x-large>mdi-play</v-icon>
            </v-btn>
          </template>
          <span>Start server</span>
        </v-tooltip>
      </div>
      <div>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              icon
              color="blue"
              :disabled="!latestVersion || latestVersion === currentVersion"
              @click="updateGame"
              v-on="on"
            >
              <v-icon x-large>mdi-arrow-up-bold-box-outline</v-icon>
            </v-btn>
          </template>
          <span>Update server</span>
        </v-tooltip>
      </div>
      <div>Version: {{ currentVersion || "Not installed" }}</div>
      <div v-if="currentVersion !== latestVersion" class="d-flex align-center">
        <v-icon color="orange">mdi-alert</v-icon> New version available
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import {gameModule, socketModule} from "@/store";
import ApiRequest from "@/utils/ApiRequest";

@Component({
  components: {}
})
export default class GameManager extends Vue {
  public loading: boolean = true;
  public updating: boolean = false;
  public updateProgress: number = 0;

  public get currentVersion() {
    return gameModule.version;
  }

  public get latestVersion() {
    return gameModule.latest;
  }

  public async mounted() {
    await socketModule.subscribe({
      topic: "game",
      channel: "update",
      callback: async response => {
        this.updateProgress = (response.message.done / response.message.total) * 100;
      }
    })
    await this.loadVersion();
  }

  public async loadVersion() {
    await new ApiRequest("/game/installed", "GET").fetch<Versions>({
      success: async res => {
        gameModule.setCurrentVersion(res.data.installed);
        gameModule.setLatestVersion(res.data.latest);
        this.loading = false;
      }
    });
  }

  public async updateGame() {
    this.updating = true;
    await new ApiRequest(`/game/install/${this.latestVersion}`, "POST").fetch({
      success: async () => {
        this.updating = false;
      }
    });
  }
}

export interface Versions {
  installed: string | null;
  latest: string | null;
}
</script>

<style scoped></style>
