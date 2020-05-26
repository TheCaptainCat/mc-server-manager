import { Action, Module, VuexModule } from "vuex-module-decorators";
import SocketConnection, {
  SocketMessage,
  SocketResponse
} from "@/utils/SocketConnection";
import { socketModule } from "@/store/index";

@Module({ name: "socket" })
export default class SocketStore extends VuexModule {
  private _connection: SocketConnection = new SocketConnection();

  public get connection(): SocketConnection {
    return this._connection;
  }

  @Action
  public async resetConnection() {
    await socketModule.connection.resetConnection();
  }

  @Action
  public async sendMessage(message: SocketMessage) {
    await socketModule.connection.send(message);
  }

  @Action
  public async subscribe(options: {
    topic: string;
    channel: string;
    callback: (response: SocketResponse) => Promise<void>;
  }) {
    await socketModule.connection.subscribe(
      options.topic,
      options.channel,
      options.callback
    );
  }
}
