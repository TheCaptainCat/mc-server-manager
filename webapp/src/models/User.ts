import Role from "@/models/Role";

interface ProfilePicture {
  key: string;
}

export default interface User {
  username: string;
  email: string;
  profile_picture: ProfilePicture | null;
  timezone: string | null;
  roles: Role[];
}
