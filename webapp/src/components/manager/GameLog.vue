<template>
  <slim-card>
    <div class="mx-4">
      <div v-for="line in log" :key="line.index">
        {{ line.text }}
      </div>
    </div>
  </slim-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  components: {}
})
export default class GameLog extends Vue {
  @Prop()
  public log!: { text: string; index: any }[];
}
</script>

<style lang="scss" scoped></style>
