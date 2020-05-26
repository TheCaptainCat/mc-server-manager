<template>
  <modal v-model="isOpen">
    <template v-slot:title>User: {{ user.username }}</template>
    <v-card v-if="!user.roles.length" outlined class="mb-3">
      <v-card-text>No roles</v-card-text>
    </v-card>
    <v-card v-else outlined class="mb-3">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th>
                Roles
              </th>
              <th class="min-cell" />
            </tr>
          </thead>
          <tbody>
            <tr v-for="role in user.roles" :key="role.name">
              <td>{{ role.name }}</td>
              <td class="min-cell">
                <v-progress-circular
                  v-if="deleteLoading"
                  indeterminate
                  size="20"
                  width="2"
                />
                <v-icon
                  v-else-if="isRoleDeletable(role.name)"
                  @click="deleteRole(role)"
                >
                  mdi-delete
                </v-icon>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
    <v-card outlined>
      <v-card-text>
        <div>
          <v-select
            label="Add a role"
            single-line
            :items="roleOptions"
            v-model="selectedRole"
          />
          <v-btn
            @click="addRole"
            :loading="addRoleLoading"
            :disabled="addRoleLoading"
          >
            Add
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    <template v-slot:actions>
      <div class="flex-grow-1"></div>
      <v-btn @click="isOpen = false" text>
        Close
      </v-btn>
    </template>
  </modal>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import User from "@/models/User";
import Role from "@/models/Role";
import ApiRequest from "@/utils/ApiRequest";
import ApiResponse from "@/utils/ApiResponse";

@Component
export default class UserDetails extends Vue {
  public selectedRole: string = "";
  public addRoleLoading: boolean = false;
  public deleteLoading: boolean = false;

  @Prop() public user!: User;
  @Prop() public currentUser!: User;
  @Prop({ default: false }) public value!: boolean;
  @Prop({ default: () => [] }) public roles!: Role[];

  public get isOpen(): boolean {
    return this.value;
  }

  public set isOpen(value: boolean) {
    this.$emit("input", value);
  }

  public get roleOptions(): string[] {
    return this.roles
      .filter(
        r => r.name != "root" && !UserDetails.userHasRole(this.user, r.name)
      )
      .map(r => r.name);
  }

  public isRoleDeletable(role: string) {
    if (role === "root") return false;
    return !(
      role === "admin" &&
      this.currentUser.username === this.user.username &&
      !UserDetails.userHasRole(this.user, "root")
    );
  }

  public async deleteRole(role: Role) {
    this.deleteLoading = true;
    await new ApiRequest(
      `/user/${this.user.username}/roles/${role.name}`,
      "DELETE"
    ).fetch<User>({
      success: async (res: ApiResponse<User>) => {
        this.$emit("user-updated", res.data);
      },
      finally: async () => {
        this.deleteLoading = false;
      }
    });
  }

  public async addRole() {
    this.addRoleLoading = true;
    if (!this.selectedRole) return;
    await new ApiRequest<Role>(`/user/${this.user.username}/roles`, "POST", {
      name: this.selectedRole
    }).fetch<User>({
      success: async (res: ApiResponse<User>) => {
        this.$emit("user-updated", res.data);
      },
      finally: async () => {
        this.addRoleLoading = false;
      }
    });
  }

  @Watch("value")
  public onOpenChanged() {
    this.selectedRole = "";
  }

  @Watch("user")
  public onUserChanged() {
    this.selectedRole = "";
  }

  public static userHasRole(user: User, role: string) {
    return user.roles.map(r => r.name).includes(role);
  }
}
</script>

<style lang="scss" scoped>
td {
  width: auto;

  &.min-cell {
    width: 1%;
    white-space: nowrap;
  }
}

.cursor-pointer {
  cursor: pointer;
}
</style>
