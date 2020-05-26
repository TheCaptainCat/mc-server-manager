<template>
  <v-dialog max-width="750" v-model="isOpen">
    <v-card>
      <v-card-title class="headline">
        {{ isRefreshing ? "Enter you credentials" : "Log in" }}
      </v-card-title>

      <v-card-text>
        <v-form @submit="login">
          <v-text-field label="Username" required v-model="username" />
          <v-text-field
            label="Password"
            required
            type="password"
            v-model="password"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <div class="flex-grow-1"></div>

        <v-btn @click="isOpen = false" text>
          Cancel
        </v-btn>

        <v-btn @click="login" color="blue">
          Log in
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import User from "@/models/User";
import { toastModule, loginModule, userModule } from "@/store";
import ApiRequest from "@/utils/ApiRequest";
import { Component, Vue, Watch } from "vue-property-decorator";

@Component
export default class LoginForm extends Vue {
  public loggedIn: boolean = false;
  public username: string = "";
  public password: string = "";

  public get isOpen(): boolean {
    return loginModule.openState;
  }

  public set isOpen(value: boolean) {
    loginModule.setOpenState(value);
  }

  public get isRefreshing(): boolean {
    return loginModule.refresh;
  }

  @Watch("isOpen")
  public onOpenStateChange(value: boolean) {
    if (value) {
      this.username = "";
      this.password = "";
    } else {
      if (!this.loggedIn && loginModule.cancelCallback) {
        loginModule.cancelCallback();
      }
      loginModule.setCallback(null);
      loginModule.setCancelCallback(null);
    }
  }

  public async login() {
    await new ApiRequest<{ username: string; password: string }>(
      "/user/login",
      "POST",
      {
        username: this.username,
        password: this.password
      }
    ).fetch<User>({
      success: async res => {
        await userModule.setUser(res.data);
        this.loggedIn = true;
        if (loginModule.callback) {
          await loginModule.callback();
        }
        this.isOpen = false;
        if (!loginModule.refresh) {
          toastModule.addToast({ type: "success", message: "Welcome back!" });
        }
      }
    });
  }
}
</script>

<style lang="scss" scoped />
