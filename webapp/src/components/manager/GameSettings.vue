<template>
  <v-dialog v-model="open">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on" :disabled="status !== 'STANDING_BY'">
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Server settings</span>
      </v-card-title>
      <v-card-text>
        <v-card>
          <v-card-title>Version</v-card-title>
          <v-container class="d-flex align-center">
            <v-select :items="selectItems" v-model="selectedVersion" />
            <v-btn
              class="ml-4"
              color="primary"
              :disabled="selectedVersion === currentVersion"
              @click="updateGame"
            >
              Update
            </v-btn>
          </v-container>
        </v-card>
        <v-card class="mt-4">
          <v-card-title>Settings</v-card-title>
          <v-container class="d-flex align-center">
            <div>
              To start the server you must accept
              <a href="https://account.mojang.com/documents/minecraft_eula"
                >Mojang's EULA</a
              >
            </div>
            <v-spacer />
            <v-btn class="ml-4" color="primary" @click="acceptEULA">
              Accept
            </v-btn>
          </v-container>
          <v-container>
            <v-row>
              <v-col
                v-for="prop of properties"
                :key="prop.name"
                :cols="12"
                :md="6"
              >
                <v-text-field :label="prop.name" v-model="prop.value" />
              </v-col>
            </v-row>
            <div class="d-flex">
              <v-spacer /><v-btn
                color="green"
                @click="() => $emit('save-props')"
                >Save</v-btn
              >
            </div>
          </v-container>
        </v-card>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="open = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import _ from "lodash";
import moment from "moment";
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import ApiRequest from "@/utils/ApiRequest";
import { Property } from "@/components/manager/GameStatus.vue";

@Component({})
export default class GameSettings extends Vue {
  public open: boolean = false;
  public selectedVersion: string | null = null;
  public versions: { name: string; date: Date; type: string }[] = [];

  @Prop() public currentVersion!: string | null;
  @Prop() public status!: string | null;
  @Prop() public properties!: Property[];

  public mounted() {
    this.fetchVersions();
  }

  public get selectItems() {
    return this.versions.map(v => ({
      value: v.name,
      text: `${v.name} (${v.type})`
    }));
  }

  public async fetchVersions() {
    await new ApiRequest("/game/versions", "GET").fetch<
      {
        name: string;
        date: string;
        type: string;
      }[]
    >({
      success: async res => {
        let versions = [];
        for (const version of res.data) {
          versions.push({
            name: version.name,
            type: version.type,
            date: moment(version.date).toDate()
          });
        }
        this.versions = versions;
        if (this.currentVersion) {
          const opt = _.find(versions, v => v.name === this.currentVersion);
          if (opt) this.selectedVersion = opt.name;
        }
      }
    });
  }

  public async updateGame() {
    await new ApiRequest(`/game/install/${this.selectedVersion}`, "POST").fetch(
      {}
    );
  }

  public async acceptEULA() {
    await new ApiRequest(`/prop/eula/accept`, "POST").fetch({});
  }

  @Watch("status")
  public onStatusChange(value: string) {
    if (value !== "STANDING_BY") this.open = false;
  }
}
</script>

<style lang="scss" scoped></style>
