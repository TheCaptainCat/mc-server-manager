<template>
  <div>
    <v-card>
      <div class="d-flex align-center">
        <v-text-field v-model="command" class="mx-4" />
        <v-btn class="mr-4" @click="send">
          Send
        </v-btn>
      </div>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ApiRequest from "@/utils/ApiRequest";

@Component({
  components: {}
})
export default class GameCommand extends Vue {
  public command: string = "";

  public async send() {
    await new ApiRequest<{ command: string }>("/game/command", "POST", {
      command: this.command
    }).fetch<{ result: string }>({
      success: async res => {
        console.log(res.data);
      }
    });
  }
}
</script>

<style scoped></style>
