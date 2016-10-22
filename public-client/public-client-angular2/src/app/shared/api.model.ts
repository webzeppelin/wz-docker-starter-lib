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