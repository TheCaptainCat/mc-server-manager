import Env from "@/utils/Env";

interface ISocketSubscription {

}

export default class SocketConnection {
  private readonly _url: string;
  private readonly _retryTimeout: number;
  private _connection: WebSocket | null;
  private readonly _subscriptions: Record<
    string,
    Record<string, (response: SocketResponse<any>) => Promise<void>>
  >;
  private _open: boolean = false;
  private _messageQueue: SocketMessage[];

  public constructor(url?: string, retryTimeout?: number) {
    if (url) this._url = `${Env.WS_URL}${url}`;
    else this._url = Env.WS_URL as string;
    this._retryTimeout = retryTimeout || 5000;
    this._subscriptions = {};
    this._messageQueue = [];
    this._connection = null;
  }

  public async resetConnection() {
    this.close();
    this._connection = new WebSocket(this._url);
    this._connection.onopen = async () => {
      this._open = true;
      await this.renewSubscriptions();
      await this.dequeueMessages();
    };
    const retry = () => {
      if (this._open) {
        this._open = false;
        setTimeout(async () => {
          await this.resetConnection();
        }, this._retryTimeout);
      }
    };
    this._connection.onerror = retry;
    this._connection.onclose = retry;
    this._connection.onmessage = ev => {
      const response = JSON.parse(ev.data) as SocketResponse<any>;
      if (
        response.topic in this._subscriptions &&
        response.channel in this._subscriptions[response.topic]
      ) {
        this._subscriptions[response.topic][response.channel](response);
      }
    };
  }

  public async subscribe<T>(
    topic: string,
    channel: string,
    callback: (response: SocketResponse<T>) => Promise<void>
  ) {
    if (!(topic in this._subscriptions)) {
      this._subscriptions[topic] = {};
    }
    await this.send({ action: "subscribe", topic: topic, channel: channel });
    this._subscriptions[topic][channel] = callback;
  }

  public async renewSubscriptions() {
    if (this._connection && this._open) {
      for (const [topic, channels] of Object.entries(this._subscriptions)) {
        for (const channel of Object.keys(channels)) {
          await this.send({
            action: "subscribe",
            topic: topic,
            channel: channel
          });
        }
      }
    }
  }

  public async dequeueMessages() {
    if (this._open) {
      let message = this._messageQueue.shift();
      while (message) {
        await this.send(message);
        message = this._messageQueue.shift();
      }
    }
  }

  public async send(message: SocketMessage) {
    if (this._connection && this._open)
      this._connection.send(JSON.stringify(message));
    else this._messageQueue.push(message);
  }

  public close() {
    if (this._connection) {
      this._open = false;
      this._connection.close();
    }
  }
}

export interface SocketMessage {
  action: string;
  channel?: string;
  topic?: string;
  message?: object;
}

export interface SocketResponse<T> {
  topic: string;
  channel: string;
  message: T;
}
