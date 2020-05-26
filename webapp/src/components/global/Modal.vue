<template>
  <v-dialog v-model="isOpen" :max-width="width">
    <v-card>
      <v-card-title>
        <slot name="title" />
      </v-card-title>
      <v-card-text>
        <slot name="default" />
      </v-card-text>
      <v-card-actions>
        <slot name="actions" />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

@Component
export default class Modal extends Vue {
  @Prop({ default: false }) public value!: boolean;
  @Prop({ default: "750" }) public width!: string;

  public get isOpen(): boolean {
    return this.value;
  }

  public set isOpen(value: boolean) {
    this.$emit("input", false);
  }
}
</script>
