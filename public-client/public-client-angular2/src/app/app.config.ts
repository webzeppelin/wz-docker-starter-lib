import { Injectable } from '@angular/core';

@Injectable()
export class Configuration {
    public ApiServer: string = "http://"+window.location.hostname+":8081/";
    public ApiBasePath: string = "api/v1/";
    public ApiBaseUrl: string = this.ApiServer + this.ApiBasePath;

    constructor() {
        // console.log("This is window info: "+window.location.hostname);
    }
}