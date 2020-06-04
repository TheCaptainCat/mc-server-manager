<template>
  <div
    :class="[
      'v-card',
      'v-sheet',
      $vuetify.theme.dark ? 'theme--dark' : 'theme--light'
    ]"
  >
    <slot name="default" />
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";

@Component({})
export default class SlimCard extends Vue {}
</script>

<style lang="scss" scoped></style>
