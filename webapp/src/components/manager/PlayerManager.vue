<template>
  <v-dialog v-model="open">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-account-group</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <div class="headline">Players</div>
      </v-card-title>
      <v-card-text>
        <slim-card class="d-flex align-center">
          <v-text-field v-model="playerName" class="mx-4" />
          <v-btn
            color="primary"
            class="mr-4"
            :disabled="!playerName"
            @click="createUser"
          >
            <v-icon class="mr-3">mdi-account-plus</v-icon> Add player
          </v-btn>
        </slim-card>
        <v-data-table :headers="tableHeaders" :items="players" />
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="open = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { Player } from "@/components/manager/GameStatus.vue";
import ApiRequest from "@/utils/ApiRequest";

@Component({})
export default class PlayerManager extends Vue {
  public open: boolean = false;
  public playerName: string = "";
  public tableHeaders = [
    { value: "uid", text: "UID" },
    { value: "name", text: "Name" },
    { value: "balance", text: "XP points in bank" }
  ];

  @Prop()
  public players!: Player[];

  public async createUser() {
    await new ApiRequest<{ name: string }>("/player", "POST", {
      name: this.playerName
    }).fetch<Player>({
      success: async res => {
        this.players.push(res.data);
      },
      finally: async () => {
        this.playerName = "";
      }
    });
  }
}
</script>

<style lang="scss" scoped>
.full-width {
  min-width: 100%;
}
</style>
