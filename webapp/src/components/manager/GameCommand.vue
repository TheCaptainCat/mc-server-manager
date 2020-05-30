<template>
  <div>
    <v-card>
      <div class="d-flex align-center">
        <v-text-field class="mx-4" />
        <v-btn class="mr-4">
          Send
        </v-btn>
      </div>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {}
})
export default class GameCommand extends Vue {}
</script>

<style scoped></style>
