<template>
  <div>
    <h1>My account</h1>
    <div v-if="loading">
      <v-skeleton-loader class="mt-5" type="article" />
      <v-skeleton-loader class="mt-5" type="article" />
      <v-skeleton-loader class="mt-5" type="article" />
    </div>
    <div v-if="error">
      <p>
        There was an error fetching data from the API.
      </p>
      <p>
        <v-btn @click="loadPrivateUserInfo">
          Retry
        </v-btn>
      </p>
    </div>
    <div v-if="!loading && !error">
      <v-card class="mt-5">
        <v-form ref="picture" v-model="pictureValid">
          <v-card-title>Upload a new profile picture</v-card-title>
          <v-card-text>
            <v-file-input
              v-model="picture"
              accept="image/*"
              label="Image file"
              :rules="pictureRules"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn :disabled="!pictureValid" @click="uploadPicture()" text>
              Upload
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <v-card class="mt-5">
        <v-form ref="username" v-model="usernameValid">
          <v-card-title>Change your username</v-card-title>
          <v-card-text>
            <v-text-field
              :rules="usernameRules"
              label="Username"
              required
              v-model="username"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn :disabled="!usernameValid" @click="saveUsername()" text>
              Save
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <v-card class="mt-5">
        <v-form ref="email" v-model="emailValid">
          <v-card-title>Change your email</v-card-title>
          <v-card-text>
            <v-text-field
              :rules="emailRules"
              label="Email"
              required
              type="email"
              v-model="email"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn :disabled="!emailValid" @click="saveEmail()" text>
              Save
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <v-card class="mt-5">
        <v-form ref="password" v-model="passwordValid">
          <v-card-title>Change your password</v-card-title>
          <v-card-text>
            <v-text-field
              :rules="passwordRules"
              label="Password"
              required
              type="password"
              v-model="password"
            />
            <v-text-field
              :rules="password2Rules"
              label="Confirm password"
              required
              type="password"
              v-model="password2"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn :disabled="!passwordValid" @click="savePassword()" text>
              Save
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <v-card class="mt-5">
        <v-form ref="timezone" v-model="timezoneValid">
          <v-card-title>Change your timezone</v-card-title>
          <v-card-text>
            <v-autocomplete
              v-model="timezone"
              clearable
              :items="timezones"
              :loading="timezonesLoading"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn :disabled="!timezoneValid" @click="saveTimezone()" text>
              Save
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </div>
  </div>
</template>

<script lang="ts">
import User from "@/models/User";
import { toastModule, userModule } from "@/store";
import ApiRequest from "@/utils/ApiRequest";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class AccountManagement extends Vue {
  public $refs!: {
    picture: HTMLFormElement;
    username: HTMLFormElement;
    email: HTMLFormElement;
    password: HTMLFormElement;
    timezone: HTMLFormElement;
  };
  public loading: boolean = true;
  public error: boolean = false;

  public picture: File | null = null;
  public pictureValid: boolean = false;
  public pictureRules: Array<(v: File) => boolean | string> = [
    v => !!v || "File is required"
  ];

  public username: string = "";
  public usernameRules: Array<(v: string) => boolean | string> = [
    v => !!v || "Username is required",
    v => (v || "").length > 2 || "Username must be 3 characters long"
  ];
  public usernameValid: boolean = true;

  public email: string = "";
  public emailRules: Array<(v: string) => boolean | string> = [
    v => !!v || "Email is required",
    v => /.+@.+\..+/.test(v) || "Email must be valid"
  ];
  public emailValid: boolean = true;

  public password: string = "";
  public password2: string = "";
  public passwordRules: Array<(v: string) => boolean | string> = [
    v => !!v || "Password is required",
    v => (!!v && (v || "").length > 5) || "Password must be 6 characters long"
  ];
  public passwordValid: boolean = true;
  public get password2Rules(): Array<(v: string) => boolean | string> {
    return [v => (!!v && v) === this.password || "Passwords must match"];
  }

  public timezone: string | null = "";
  public timezoneValid: boolean = true;
  public timezones: string[] = [];
  public timezonesLoading: boolean = true;

  public created() {
    this.loadPrivateUserInfo();
    this.loadTimezones();
  }

  public async loadPrivateUserInfo() {
    this.loading = true;
    this.error = false;
    await new ApiRequest("/user/me", "GET").fetch<User>({
      success: async res => {
        this.username = res.data.username;
        this.email = res.data.email;
        this.timezone = res.data.timezone;
      },
      error: async () => {
        this.error = true;
      },
      finally: async () => {
        this.loading = false;
      }
    });
  }

  public async loadTimezones() {
    this.timezonesLoading = true;
    await new ApiRequest("/tz", "GET").fetch<string[]>({
      success: async res => {
        this.timezones = res.data;
        this.timezonesLoading = false;
      }
    });
  }

  public uploadPicture() {
    if (this.$refs.picture.validate() && this.picture) {
      new ApiRequest<File>("/user/picture", "POST", this.picture).fetch<User>({
        success: async res => {
          await userModule.setUser(res.data);
        }
      });
    }
  }

  public saveUsername() {
    if (this.$refs.username.validate()) {
      this.sendUpdate({ username: this.username });
    }
  }

  public saveEmail() {
    if (this.$refs.email.validate()) {
      this.sendUpdate({ email: this.email });
    }
  }

  public savePassword() {
    if (this.$refs.password.validate()) {
      this.sendUpdate({ password: this.password });
    }
  }

  public saveTimezone() {
    if (this.$refs.timezone.validate()) {
      this.sendUpdate({ timezone: this.timezone });
    }
  }

  public async sendUpdate(params: object) {
    await new ApiRequest<object>("/user/me", "PATCH", params).fetch<User>({
      success: async res => {
        await userModule.setUser(res.data);
        for (const message of res.messages) {
          toastModule.addToast({ message, type: "success" });
        }
      }
    });
  }
}
</script>

<style lang="scss" scoped />
