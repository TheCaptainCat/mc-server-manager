<template>
  <slim-card>
    <div v-if="loading" class="ma-3 text-lg-start">Loading...</div>
    <div v-else class="d-flex align-center ma-3">
      <div v-if="status === 'UPDATING'" class="full-width">
        <v-progress-linear :value="progress" />
      </div>
      <div v-else class="d-flex align-center full-width">
        <div v-if="status === 'STANDING_BY'" class="d-flex align-center">
          <v-btn icon color="green" :disabled="!currentVersion">
            <v-icon x-large @click="startGame">mdi-play</v-icon>
          </v-btn>
          <div>Server is stopped</div>
        </div>
        <div v-if="status === 'RUNNING'" class="d-flex align-center">
          <v-btn icon color="red">
            <v-icon x-large @click="stopGame">mdi-stop</v-icon>
          </v-btn>
          <div>Server is running</div>
        </div>
        <v-spacer />
        <div class="mr-6">
          <player-manager :players="players" />
        </div>
        <div>
          <span v-if="currentVersion !== latestVersion">
            <v-icon
              :color="$vuetify.theme.dark ? 'yellow accent-2' : 'blue accent-2'"
            >
              mdi-alert-decagram
            </v-icon>
          </span>
          {{ currentVersion }}
        </div>
        <div>
          <game-settings
            :current-version="currentVersion"
            :status="status"
            :properties="properties"
            @save-props="saveProps"
          />
        </div>
      </div>
    </div>
  </slim-card>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { gameModule } from "@/store";
import GameSettings from "@/components/manager/GameSettings.vue";
import PlayerManager from "@/components/manager/PlayerManager.vue";
import ApiRequest from "@/utils/ApiRequest";

@Component({
  components: { GameSettings, PlayerManager }
})
export default class GameStatus extends Vue {
  public loading: boolean = true;
  public players: Player[] = [];
  public properties: Property[] = [];

  public get currentVersion() {
    return gameModule.version;
  }

  public get status() {
    return gameModule.status;
  }

  public get progress() {
    const progress = gameModule.progress;
    if (progress.total === 0) return 0;
    return (progress.done / progress.total) * 100;
  }

  public get latestVersion() {
    return gameModule.latest;
  }

  public async mounted() {
    const versionTask = this.loadVersion();
    const playerTask = this.loadPlayers();
    const propTask = this.loadProps();

    await Promise.all([versionTask, playerTask, propTask]);
    this.loading = false;
  }

  public async loadVersion() {
    await new ApiRequest("/game/status", "GET").fetch<Version>({
      success: async res => {
        gameModule.setCurrentVersion(res.data.installed);
        gameModule.setLatestVersion(res.data.latest);
      }
    });
  }

  public async loadPlayers() {
    await new ApiRequest("/player", "GET").fetch<Player[]>({
      success: async res => {
        this.players = res.data || [];
      }
    });
  }

  public async loadProps() {
    await new ApiRequest("/prop", "GET").fetch<Property[]>({
      success: async res => {
        this.properties = res.data || [];
      }
    });
  }

  public async startGame() {
    await new ApiRequest(`/game/run`, "POST").fetch({});
  }

  public async stopGame() {
    await new ApiRequest(`/game/stop`, "POST").fetch({});
  }

  public async saveProps() {
    await new ApiRequest<Property[]>("/prop", "PUT", this.properties).fetch<
      Property[]
    >({
      success: async res => {
        this.properties = res.data;
      }
    });
  }
}

export interface Version {
  installed: string | null;
  latest: string | null;
}

export interface Player {
  name: string;
  uid: string;
  balance: number;
}

export interface Property {
  name: string;
  value: string;
}
</script>

<style lang="scss" scoped>
.full-width {
  min-width: 100%;
}
</style>
