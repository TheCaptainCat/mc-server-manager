<template>
  <v-container>
    <v-row>
      <v-col v-for="(tile, index) of tiles" :key="index" md="4">
        <v-card link :to="tile.link">
          <v-card-title>
            <v-icon left>{{ tile.icon }}</v-icon> {{ tile.label }}
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class AdminPanel extends Vue {
  public tiles = [
    {
      label: "User Management",
      link: { name: "UserTable" },
      icon: "mdi-account-box"
    }
  ];
}
</script>
