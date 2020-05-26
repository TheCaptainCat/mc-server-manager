<template>
  <v-container>
    <div v-if="$vuetify.breakpoint.xsOnly">
      <v-card>
        <v-card-subtitle>Navigation</v-card-subtitle>
        <v-card-text>
          <v-btn-toggle>
            <v-btn
              v-for="route of routes"
              :key="route.name"
              link
              exact
              :to="{ name: route.name }"
            >
              {{ route.label }}
            </v-btn>
          </v-btn-toggle>
        </v-card-text>
      </v-card>
    </div>
    <div class="d-flex">
      <div>
        <v-card v-if="$vuetify.breakpoint.smAndUp" class="mr-5" width="300">
          <v-list nav>
            <v-subheader>Navigation</v-subheader>
            <v-list-item-group>
              <v-list-item
                v-for="route of routes"
                :key="route.name"
                link
                exact
                :to="{ name: route.name }"
              >
                <v-list-item-title>{{ route.label }}</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>
      </div>
      <div class="flex-grow-1">
        <slot />
      </div>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { RouteConfig } from "vue-router";

@Component
export default class WithNavigation extends Vue {
  @Prop() routes!: NavigationItem[];
}

export interface NavigationItem {
  name: string;
  label: string;
}
</script>
