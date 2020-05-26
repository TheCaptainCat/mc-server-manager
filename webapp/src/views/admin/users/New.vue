<template>
  <modal v-model="isOpen">
    <template v-slot:title>Create a user</template>
    <v-form ref="form" v-model="formValid">
      <v-text-field
        v-model="username"
        label="Username"
        required
        :rules="usernameRules"
      />
      <v-text-field
        v-model="email"
        label="Email"
        required
        :rules="emailRules"
      />
      <v-checkbox v-model="sendMail" label="Send email" />
    </v-form>
    <template v-slot:actions>
      <div class="flex-grow-1"></div>
      <v-btn @click="isOpen = false" text>
        Cancel
      </v-btn>
      <v-btn
        @click="createUser"
        text
        :disabled="!formValid || loading"
        :loading="loading"
      >
        Create
      </v-btn>
    </template>
  </modal>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { isValidEmail } from "@/utils/Validators";
import ApiRequest from "@/utils/ApiRequest";
import ApiResponse from "@/utils/ApiResponse";
import User from "@/models/User";

@Component
export default class NewUser extends Vue {
  @Prop({ default: false }) public value!: boolean;

  public formValid: boolean = false;
  public username: string = "";
  public email: string = "";
  public sendMail: boolean = true;
  public loading: boolean = false;

  public usernameRules = [
    (v: string) => !!v || "Username is required",
    (v: string) =>
      (!!v && v.length >= 3) || "Username must at least 3 characters long"
  ];
  public emailRules = [
    (v: string) => !!v || "Email is required",
    (v: string) => isValidEmail(v) || "Invalid email format"
  ];

  public get isOpen(): boolean {
    return this.value;
  }

  public set isOpen(value: boolean) {
    this.$emit("input", value);
  }

  public async createUser() {
    this.loading = true;
    await new ApiRequest<CreateUserPayload>("/user/register/admin", "POST", {
      username: this.username,
      email: this.email,
      send_mail: this.sendMail
    }).fetch<User>({
      success: async (res: ApiResponse<User>) => {
        this.$emit("user-created", res.data);
        this.isOpen = false;
      },
      finally: async () => {
        this.loading = false;
      }
    });
  }

  @Watch("value")
  public onOpenChanged() {
    this.username = "";
    this.email = "";
    if (this.$refs.form) (this.$refs.form as any).resetValidation();
  }
}

interface CreateUserPayload {
  username: string;
  email: string;
  send_mail: boolean;
}
</script>
