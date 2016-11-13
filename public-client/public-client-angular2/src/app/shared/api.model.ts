export interface ServerTime {
    hour: number;
    minute: number;
    second: number;
    tz_name: string;
    tz_offset: string;
    bogus: string;
}

export class GuestbookEntry {
  constructor(
    public id: string,
    public name: string,
    public message: string,
    public timestamp: Date
  ) {  }
}

export class GuestbookEntrySet {
    constructor(
        public entries: GuestbookEntry[],
        public count: number,
        public last_id: string,
        public has_more: boolean
    ) { }
}

export class LoginResponse {
    constructor(
        public session_id: string,
        public state: string,
        public scope: string,
        public redirect_uri: string,
        public login_url: string
    ) { }
}

export class TokenRequest {
    constructor(
        public session_id: string,
        public state: string,
        public code: string
    ) { }
}
export class TokenResponse {
    constructor(
        public id_token: string,
        public token_type: string,
        public access_token: string,
        public expires_in: string
    ) { }
}

export class UserInfo {
    constructor(
        public name: string,
        public sub: string,
        public email: string
    ) { }
}