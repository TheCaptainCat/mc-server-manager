import Env from "@/utils/Env";
import User from "@/models/User";

export default class UserHelper {
  public static profilePictureUrl(user: User | null): string | null {
    if (!user) return null;
    if (!user.profile_picture) return null;
    return `${Env.API_URL}/file/${user.profile_picture.key}/download`;
  }

  public static empty(): User {
    return {
      username: "",
      email: "",
      roles: [],
      profile_picture: null,
      timezone: null
    };
  }
}
