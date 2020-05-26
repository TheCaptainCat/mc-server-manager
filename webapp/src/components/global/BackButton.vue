<template>
  <v-btn link :to="to" large class="mb-3" exact>
    <v-icon left>mdi-arrow-left</v-icon> Back
  </v-btn>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class BackButton extends Vue {
  @Prop()
  public to!: string;
}
</script>
