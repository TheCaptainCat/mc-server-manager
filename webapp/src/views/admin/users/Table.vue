<template>
  <v-container>
    <div class="d-flex">
      <back-btn :to="{ name: 'AdminPanel' }" />
      <span class="flex-grow-1" />
      <v-btn large @click="newUserOpen = true">
        <v-icon left>mdi-plus</v-icon>
        Create user
      </v-btn>
    </div>
    <v-card>
      <v-card-title>
        Users
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        />
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :loading="loading"
        :sort-by="['username']"
      >
        <template v-slot:item.profile_picture="{ value }">
          <v-icon v-if="!value">mdi-account-circle</v-icon>
          <v-avatar v-else :size="24">
            <img
              :src="getProfilePicture({ profile_picture: value })"
              alt="profile picture"
            />
          </v-avatar>
        </template>
        <template v-slot:item.roles="{ value }">
          <v-chip
            v-for="(role, index) of value"
            :key="index"
            outlined
            class="mr-3"
          >
            {{ role.name }}
          </v-chip>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon @click="onRowClick(item)">mdi-pencil</v-icon>
        </template>
      </v-data-table>
    </v-card>
    <user-details
      v-model="userDetailsOpen"
      :user="selectedUser"
      :current-user="currentUser"
      :roles="roles"
      @user-updated="onUserUpdated"
    />
    <new-user v-model="newUserOpen" @user-created="onUserUpdated" />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { userModule } from "@/store";
import UserDetails from "@/views/admin/users/Details.vue";
import NewUser from "@/views/admin/users/New.vue";
import User from "@/models/User";
import Role from "@/models/Role";
import ApiRequest from "@/utils/ApiRequest";
import ApiResponse from "@/utils/ApiResponse";
import { UserHelper } from "@/helpers";

@Component({
  components: { UserDetails, NewUser }
})
export default class UserTable extends Vue {
  public loading: boolean = true;
  public users: User[] = [];
  public headers = [
    { text: "", value: "profile_picture", sortable: false, width: "1%" },
    { text: "Username", value: "username" },
    { text: "Email", value: "email" },
    { text: "Roles", value: "roles", sortable: false },
    { test: "", value: "actions", sortable: false, width: "1%" }
  ];
  public search: string = "";
  public userDetailsOpen: boolean = false;
  public newUserOpen: boolean = false;
  public selectedUser: User = UserHelper.empty();
  public roles: Role[] = [];
  public currentUser: User = userModule.currentUser as User;

  public get filteredUsers(): User[] {
    return this.users.filter(
      u =>
        u.username.includes(this.search) ||
        u.roles.some(r => r.name.includes(this.search))
    );
  }

  public mounted() {
    this.fetchUsers();
    this.fetchRoles();
  }

  public async fetchUsers() {
    await new ApiRequest("/user", "GET").fetch<User[]>({
      success: async (res: ApiResponse<User[]>) => {
        this.users = res.data;
      },
      finally: async () => {
        this.loading = false;
      }
    });
  }

  public async fetchRoles() {
    await new ApiRequest("/role", "GET").fetch<Role[]>({
      success: async (res: ApiResponse<Role[]>) => {
        this.roles = res.data;
      }
    });
  }

  public onRowClick(user: User) {
    this.selectedUser = user;
    this.userDetailsOpen = true;
  }

  public onUserUpdated(user: User) {
    this.users = this.users
      .filter(u => u.username !== user.username)
      .concat([user]);
    if (this.selectedUser.username === user.username) this.selectedUser = user;
  }

  public getProfilePicture(user: Partial<User>): string | null {
    return UserHelper.profilePictureUrl(user as User);
  }
}
</script>
