<template>
  <a :href="href" class="blue-link" target="_blank" rel="noopener noreferrer">
    <slot /> <v-icon dense class="icon">mdi-open-in-new</v-icon>
  </a>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class ExternalLink extends Vue {
  @Prop({ default: "" })
  public href!: string;
}
</script>

<style lang="scss" scoped>
.blue-link {
  color: #2196f3 !important;

  .icon {
    color: #2196f3;
  }
}
</style>
