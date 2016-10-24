import { Injectable } from '@angular/core';

@Injectable()
export class Configuration {
    public ApiServer: string = "https://"+window.location.hostname+"/";
    public ApiBasePath: string = "api/v1/";
    public ApiBaseUrl: string = this.ApiServer + this.ApiBasePath;

    constructor() {
        // console.log("This is window info: "+window.location.hostname);
    }
}