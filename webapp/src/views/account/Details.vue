<template>
  <div>
    <div class="d-flex align-center">
      <div>
        <v-avatar :size="150" v-if="user.profile_picture">
          <img :src="pictureUrl" :alt="user.username" />
        </v-avatar>
        <v-icon v-else :size="150">mdi-account-circle</v-icon>
      </div>
      <div class="ml-3">
        <h1>{{ user.username }}</h1>
        <h2>{{ user.email }}</h2>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import User from "@/models/User";
import { userModule } from "@/store";
import Env from "@/utils/Env";

@Component
export default class AccountDetails extends Vue {
  public get user() {
    return userModule.currentUser as User;
  }

  public get pictureUrl(): string {
    if (this.user.profile_picture !== null)
      return `${Env.API_URL}/file/${this.user.profile_picture.key}/download`;
    return "";
  }
}
</script>
